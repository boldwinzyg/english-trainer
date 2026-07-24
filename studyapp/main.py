# English Word Study App
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Register fonts BEFORE any kivy imports
from kivy.core.text import LabelBase
from kivy.config import Config

_fonts_dir = os.path.join(BASE_DIR, 'studyapp', 'data', 'fonts')
_cjk_path = os.path.join(_fonts_dir, 'simhei.ttf')
_latin_path = os.path.join(_fonts_dir, 'Charis-MediumItalic.ttf')

LabelBase.register(name='CJK', fn_regular=_cjk_path)
LabelBase.register(name='Latin', fn_regular=_latin_path)
_emoji_path = os.path.join(_fonts_dir, 'seguiemj.ttf')
LabelBase.register(name='Emoji', fn_regular=_emoji_path)

# Single default font - CJK (it contains most common symbols)
Config.set('kivy', 'default_font', ['CJK', _cjk_path])

# Mobile window: 390x844 (most common 2026 phone)
Config.set('graphics', 'width', '390')
Config.set('graphics', 'height', '844')
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, NoTransition

from studyapp.models.data_manager import DataManager
from studyapp.screens.home_screen import HomeScreen
from studyapp.screens.study_screen import StudyScreen
from studyapp.screens.challenge_screen import ChallengeScreen
from studyapp.screens.error_words_screen import ErrorWordsScreen
from studyapp.screens.settings_screen import SettingsScreen
from studyapp.screens.calendar_screen import CalendarScreen
from studyapp.screens.about_screen import AboutScreen


class StudyApp(App):
    title = '\u66e6\u66e6\u5355\u8bcd'

    def build(self):
        self.data_manager = DataManager(os.path.join(BASE_DIR, 'studyapp'))
        from studyapp.kv_styles import KV_STRING
        Builder.load_string(KV_STRING)
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(StudyScreen(name='study'))
        sm.add_widget(ChallengeScreen(name='challenge'))
        sm.add_widget(ErrorWordsScreen(name='error_words'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(CalendarScreen(name='calendar'))
        sm.add_widget(AboutScreen(name='about'))
        return sm


if __name__ == '__main__':
    StudyApp().run()
