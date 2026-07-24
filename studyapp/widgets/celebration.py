"""Confetti celebration overlay widget."""
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.app import App
import random
import os

_overlay_instance = None


def show_celebrate(parent_widget, x=0.5, y=0.3, big=False):
    """Show confetti at normalized position."""
    global _overlay_instance
    try:
        # Remove any existing celebration first
        if _overlay_instance is not None:
            try:
                _overlay_instance._cancel_all()
                if _overlay_instance.parent:
                    _overlay_instance.parent.remove_widget(_overlay_instance)
            except Exception:
                pass
            _overlay_instance = None
        root = parent_widget.get_parent_window()
        if not root:
            return
        overlay = CelebrateOverlay()
        _overlay_instance = overlay
        root.add_widget(overlay)
        overlay.start_celebration(x, y, big)
    except Exception:
        pass


def dismiss_celebration():
    """Force dismiss any active celebration."""
    global _overlay_instance
    if _overlay_instance is not None:
        try:
            _overlay_instance._cancel_all()
            if _overlay_instance.parent:
                _overlay_instance.parent.remove_widget(_overlay_instance)
        except Exception:
            pass
        _overlay_instance = None


class ConfettiPiece:
    def __init__(self, canvas, x, y, size, color, vx, vy):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.vx = vx
        self.vy = vy
        with canvas:
            c = Color(*color)
            self.rect = Rectangle(pos=(x, y), size=(size, size * 0.6))
        self._color_inst = c

    def update(self, dt, gravity=400):
        self.vy -= gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.pos = (self.x, self.y)


class CelebrateOverlay(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pieces = []
        self._label = None
        self._tick_event = None
        self._closed = False

    def _cancel_all(self):
        self._closed = True
        if self._tick_event:
            try:
                self._tick_event.cancel()
            except Exception:
                pass
            self._tick_event = None

    def start_celebration(self, nx=0.5, ny=0.3, big=False):
        if self._closed:
            return
        # Play sound
        try:
            base = App.get_running_app().data_manager.base_dir
            snd_path = os.path.join(base, "data", "ok.wav")
            snd = SoundLoader.load(snd_path)
            if snd:
                snd.play()
        except Exception:
            pass
        # Wait a frame for layout, then create confetti
        Clock.schedule_once(lambda dt: self._do_celebration(nx, ny, big), 0.05)

    def _do_celebration(self, nx, ny, big):
        if self._closed:
            return
        try:
            pw = max(self.width, 100)
            ph = max(self.height, 100)
            start_x = nx * pw
            start_y = ny * ph
            colors = [
                (1, 0.2, 0.2, 1), (1, 0.8, 0, 1), (0.2, 1, 0.2, 1),
                (0.2, 0.6, 1, 1), (1, 0.4, 1, 1), (1, 1, 0.2, 1),
            ]
            for _ in range(30):
                speed = random.uniform(100, 300)
                vx = speed * random.choice([-1, 1]) * random.uniform(0.3, 1.0)
                vy = speed * random.uniform(0.5, 1.0)
                size = random.uniform(6, 12)
                color = random.choice(colors)
                piece = ConfettiPiece(
                    self.canvas, start_x, start_y, size, color, vx, vy
                )
                self.pieces.append(piece)
            # Show text
            self._label = Label(
                text="[b]OK[/b]",
                markup=True,
                font_size="32sp",
                color=(1, 0.85, 0, 1),
                size_hint=(None, None),
                size=(300, 60),
                center_x=start_x,
                top=start_y + 40,
                halign="center",
                valign="middle",
            )
            self._label.bind(texture_size=self._label.setter("size"))
            self.add_widget(self._label)
            self._tick_event = Clock.schedule_interval(self._update_confetti, 1 / 30)
        except Exception:
            pass

    def _update_confetti(self, dt):
        if self._closed:
            return
        try:
            alive = []
            for p in self.pieces:
                p.update(dt)
                if p.y > -20:
                    alive.append(p)
            self.pieces = alive
            if not self.pieces:
                self._cancel_all()
                if self._label:
                    try:
                        self.parent.remove_widget(self._label)
                    except Exception:
                        pass
                self._cleanup()
        except Exception:
            pass

    def _cleanup(self):
        self._cancel_all()
        try:
            if self.parent:
                self.parent.remove_widget(self)
        except Exception:
            pass
        global _overlay_instance
        _overlay_instance = None

    def on_touch_down(self, touch):
        return True
