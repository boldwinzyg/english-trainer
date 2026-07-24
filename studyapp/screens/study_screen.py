"""Study screen - flash card with TTS and image area."""
import threading
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock


class StudyScreen(Screen):
    show_meaning = False

    def on_enter(self):
        self.show_meaning = False
        self._render_word()
        # Speak immediately
        self._speak_word(0)
        # Auto-show meaning after 2 seconds
        Clock.schedule_once(self._auto_show_meaning, 2.0)
        # Enable next button after 3 seconds
        btn = self.ids.get("next_btn")
        if btn:
            btn.disabled = True
            btn.text = "3s \u540e\u7ee7\u7eed"
        Clock.schedule_once(self._enable_next, 1.0)
        Clock.schedule_once(self._enable_next_check, 2.0)
        Clock.schedule_once(self._enable_next_done, 3.0)

    def on_kv_post(self, base_widget):
        for wid_id in ('phonetic_label', 'image_label'):
            w = self.ids.get(wid_id)
            if w:
                if wid_id == 'phonetic_label':
                    w.font_name = 'Latin'
                elif wid_id == 'image_label':
                    w.font_name = 'Emoji'

    def _render_word(self):
        dm = App.get_running_app().data_manager
        word = dm.get_current_word(for_study=True)
        word_label = self.ids.get('word_label')
        meaning_label = self.ids.get('meaning_label')
        phonetic_label = self.ids.get('phonetic_label')
        image_label = self.ids.get('image_label')
        progress_label = self.ids.get('progress_label')
        if word:
            if word_label:
                word_label.text = word.get('word', '')
            if phonetic_label:
                phonetic_label.text = word.get('phonetic', '')
            if image_label:
                image_label.text = word.get('emoji', '')
            if meaning_label:
                meaning_label.text = word.get('meaning', '') if self.show_meaning else ''
            if progress_label:
                idx = dm.study_index
                total = len(dm.todays_words)
                progress_label.text = '{}/{}'.format(idx if idx < total else total, total)
        else:
            if word_label:
                word_label.text = '\u4eca\u65e5\u5df2\u5b8c\u6210!'
            if meaning_label:
                meaning_label.text = '\u592a\u68d2\u4e86\uff0c\u660e\u5929\u7ee7\u7eed\u544a'
            if phonetic_label:
                phonetic_label.text = ''
            if image_label:
                image_label.text = '\U0001f389'
            if progress_label:
                progress_label.text = '{}/{}'.format(dm.today_index, len(dm.todays_words))

    def _auto_show_meaning(self, dt):
        if not self.show_meaning:
            self.show_meaning = True
            self._render_word()

    def _speak_word(self, dt):
        from studyapp.tts import speak
        dm = App.get_running_app().data_manager
        word = dm.get_current_word(for_study=True)
        if not word:
            return
        w = word.get('word', '')
        if not w:
            return
        speak(w)

    def _enable_next(self, dt):
        btn = self.ids.get("next_btn")
        if btn:
            btn.text = "2s \u540e\u7ee7\u7eed"

    def _enable_next_check(self, dt):
        btn = self.ids.get("next_btn")
        if btn:
            btn.text = "1s \u540e\u7ee7\u7eed"

    def _enable_next_done(self, dt):
        btn = self.ids.get("next_btn")
        if btn:
            btn.disabled = False
            btn.text = "\u4e0b\u4e00\u4e2a"

    def on_next(self):
        dm = App.get_running_app().data_manager
        btn = self.ids.get("next_btn")
        # If already complete, go home
        if dm.is_study_complete(for_study=True):
            self.manager.current = 'home'
            return
        dm.mark_correct()
        self.show_meaning = False
        if dm.is_study_complete(for_study=True):
            self._render_word()
            if btn:
                btn.disabled = False
                btn.text = "\u5b8c\u6210\u4e86\uff0c\u56de\u5bb6"
        else:
            self._render_word()
            self._speak_word(0)
            Clock.schedule_once(self._auto_show_meaning, 2.0)
            # Disable button again for 3s
            btn = self.ids.get("next_btn")
            if btn:
                btn.disabled = True
                btn.text = "3s \u540e\u7ee7\u7eed"
            Clock.schedule_once(self._enable_next, 1.0)
            Clock.schedule_once(self._enable_next_check, 2.0)
            Clock.schedule_once(self._enable_next_done, 3.0)

    def repeat_speak(self):
        Clock.schedule_once(self._speak_word, 0.05)

    def on_speaker_press(self):
        btn = self.ids.get("speaker_btn")
        if btn:
            btn.color = (0.3, 0.8, 0.3, 1)
            btn.font_size = "24sp"

    def on_speaker_release(self):
        btn = self.ids.get("speaker_btn")
        if btn:
            from kivy.utils import get_color_from_hex
            btn.color = get_color_from_hex('#4a6cf7')
            btn.font_size = "20sp"
        self.repeat_speak()

    def go_back(self):
        self.manager.current = 'home'
