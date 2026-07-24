"""Home screen - info area with tags, function buttons at bottom."""
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
from kivy.base import stopTouchApp


class HomeScreen(Screen):

    def on_enter(self):
        Clock.schedule_once(self._update_info, 0)
        self._set_bg()

    def _set_bg(self):
        import os
        from kivy.graphics import Rectangle as Rc, Color
        try:
            base = App.get_running_app().data_manager.base_dir
            bg_path = os.path.join(base, 'data', 'bj.png')
            self.canvas.before.clear()
            with self.canvas.before:
                Rc(source=bg_path, pos=self.pos, size=self.size)
        except Exception:
            pass
        self._set_bg()

    def _set_bg(self):
        from kivy.uix.image import Image
        from kivy.graphics import Rectangle, Color
        # Remove existing bg image if any
        for child in self.children:
            if hasattr(child, '_is_bg'):
                self.remove_widget(child)
                break
        import os
        try:
            base = App.get_running_app().data_manager.base_dir
            bg_path = os.path.join(base, 'data', 'bj.png')
            bg = Image(source=bg_path, allow_stretch=True, keep_ratio=False,
                       opacity=0.3, size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
            bg._is_bg = True
            self.add_widget(bg, index=len(self.children))
        except Exception:
            pass

    def _update_info(self, dt):
        app = App.get_running_app()
        if not app:
            return
        dm = getattr(app, 'data_manager', None)
        if not dm:
            return
        # Update info tags
        self._set_text('tag_today', '\u4eca\u65e5\u5f85\u5b8c\u6210: {}\u4e2a'.format(max(0, len(dm.todays_words) - dm.today_index)))
        self._set_text('tag_total', '\u7d2f\u8ba1\u901a\u5173: {}\u4e2a'.format(dm.total_cleared))
        self._set_text('tag_grade', '\u8bcd\u5e93: {}'.format(dm.current_grade))
        grade_total = len(dm.get_words_for_grade(dm.current_grade))
        grade_learned = dm.total_learned % grade_total if grade_total > 0 else 0
        self._set_text('tag_words', '\u5355\u8bcd\u603b\u6570: {}\u4e2a'.format(grade_total))
        self._set_text('tag_remain', '\u5269\u4f59: {}\u4e2a'.format(max(0, grade_total - grade_learned)))
        self._set_text('tag_streak', '\u6253\u5361: {}\u5929'.format(dm.streak_days))

    def _set_text(self, widget_id, text):
        w = self.ids.get(widget_id)
        if w:
            w.text = text

    def open_calendar(self):
        pass

    def open_menu(self):
        self.manager.current = 'settings'

    def quit_app(self):
        stopTouchApp()

    def goto_study(self):
        self.manager.current = 'study'

    def goto_challenge(self):
        self.manager.current = 'challenge'

    def goto_error_words(self):
        self.manager.current = 'error_words'

    def goto_calendar(self):
        self.manager.current = 'calendar'
