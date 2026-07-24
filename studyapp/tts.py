"""Cross-platform TTS module."""
import os
import platform
import subprocess
import tempfile
import threading
import asyncio


_IS_ANDROID = ("ANDROID_ARGUMENT" in os.environ)
_IS_WINDOWS = (platform.system() == "Windows")
_IS_LINUX = (platform.system() == "Linux")


# Global references to prevent garbage collection
_tts_instance = None
_tts_listener = None
_tts_ready = False
_tts_queue = []

class _TtsInitListener:
    """Listener proxy for TTS init callback."""
    def __init__(self):
        self._proxy = None

    def create(self):
        from jnius import PythonJavaClass, java_method
        tts_ref = self
        class Listener(PythonJavaClass):
            __javainterfaces__ = ['android/speech/tts/TextToSpeech$OnInitListener']
            @java_method('(I)V')
            def onInit(self, status):
                tts_ref._on_init(status)
        self._proxy = Listener()
        return self._proxy

    def _on_init(self, status):
        global _tts_ready, _tts_instance
        from jnius import autoclass
        TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
        Locale = autoclass("java.util.Locale")
        if status == TextToSpeech.SUCCESS and _tts_instance is not None:
            _tts_ready = True
            try:
                _tts_instance.setLanguage(Locale.US)
            except Exception:
                try:
                    _tts_instance.setLanguage(Locale("en"))
                except Exception:
                    pass
            # Speak any queued text
            global _tts_queue
            for t in _tts_queue:
                _tts_instance.speak(t, TextToSpeech.QUEUE_FLUSH, None)
            _tts_queue = []

def _tts_android(text: str):
    """Android: use native TextToSpeech via pyjnius."""
    global _tts_instance, _tts_listener, _tts_ready, _tts_queue
    try:
        from jnius import autoclass
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
        Locale = autoclass("java.util.Locale")
        activity = PythonActivity.mActivity
        if activity is None:
            return
        if _tts_ready and _tts_instance is not None:
            _tts_instance.speak(text, TextToSpeech.QUEUE_FLUSH, None)
            return
        if _tts_instance is None:
            _tts_queue.append(text)
            _tts_listener = _TtsInitListener()
            _tts_instance = TextToSpeech(activity, _tts_listener.create())
        else:
            # TTS initializing, queue the text
            _tts_queue.append(text)
    except Exception:
        pass


# TTS audio cache: {text: mp3_path}
_tts_cache = {}

def _get_cache_path(text: str):
    """Get cached MP3 path for text, or None if not cached."""
    import hashlib
    key = hashlib.md5(text.encode()).hexdigest()
    cache_dir = os.path.join(tempfile.gettempdir(), "tts_cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, key + ".mp3")
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
        return cache_path
    return None

def _save_to_cache(text: str, mp3_path: str):
    """Save generated MP3 to cache."""
    import hashlib, shutil
    key = hashlib.md5(text.encode()).hexdigest()
    cache_dir = os.path.join(tempfile.gettempdir(), "tts_cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, key + ".mp3")
    try:
        shutil.copy2(mp3_path, cache_path)
    except Exception:
        pass

def _play_mp3(mp3_path: str):
    """Play MP3 file using best available method (non-blocking)."""
    if not os.path.exists(mp3_path):
        return
    if _IS_WINDOWS:
        import subprocess as _sp
        ps_cmd = (
            'Add-Type -AssemblyName presentationCore; '
            '$player = New-Object System.Windows.Media.MediaPlayer; '
            '$player.Open([uri]"{path}"); '
            '$player.Play(); '
            'Start-Sleep -Milliseconds {ms}; '
            '$player.Close();'
        ).format(
            path=mp3_path.replace(chr(92), chr(92)*2),
            ms=5000
        )
        _sp.Popen(
            ["powershell", "-WindowStyle", "Hidden", "-Command", ps_cmd],
            stdout=_sp.DEVNULL, stderr=_sp.DEVNULL,
            creationflags=0x08000000 if hasattr(_sp, 'CREATE_NO_WINDOW') else 0
        )
    elif _IS_LINUX:
        subprocess.run(["aplay", mp3_path], timeout=5)

def _tts_edge(text: str):
    """Desktop: use edge_tts (Microsoft Edge online TTS) with caching."""
    try:
        import edge_tts
        # Check cache first
        cached = _get_cache_path(text)
        if cached:
            _play_mp3(cached)
            return
        # Generate new MP3
        mp3_path = os.path.join(tempfile.gettempdir(), "tts_word.mp3")

        async def _gen():
            communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
            await communicate.save(mp3_path)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_gen())
        loop.close()

        if os.path.exists(mp3_path):
            # Save to cache for next time
            _save_to_cache(text, mp3_path)
            _play_mp3(mp3_path)
    except Exception:
        pass


def speak(text: str):
    """Speak text using best available TTS backend."""
    if not text:
        return
    if _IS_ANDROID:
        _tts_android(text)
    else:
        t = threading.Thread(target=_tts_edge, args=(text,), daemon=True)
        t.start()
