"""About screen."""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.utils import get_color_from_hex


class AboutScreen(Screen):

    def go_back(self):
        self.manager.current = 'home'

    def on_clear_records(self):
        self._show_password_dialog()

    def _show_password_dialog(self):
        content = BoxLayout(orientation='vertical', padding=[20, 15], spacing=12)
        content.add_widget(Label(
            text='\u8bf7\u8f93\u5165\u7ba1\u7406\u5458\u5bc6\u7801',
            font_size=16, color=get_color_from_hex('#333333'),
            size_hint_y=None, height=30,
        ))
        pwd_input = TextInput(
            password=True, multiline=False,
            font_size=16, size_hint_y=None, height=44,

        )
        content.add_widget(pwd_input)

        def on_confirm(instance):
            pwd = pwd_input.text.strip()
            popup.dismiss()
            if pwd == '123321':
                self._show_confirm_dialog()
            else:
                self._show_error_dialog()

        btn_box = BoxLayout(size_hint_y=None, height=44, spacing=10)
        btn_box.add_widget(Button(
            text='\u786e\u8ba4', font_size=15,
            background_color=get_color_from_hex('#4a6cf7'),
            background_normal='', color=(1,1,1,1),
            on_release=on_confirm,
        ))
        btn_box.add_widget(Button(
            text='\u53d6\u6d88', font_size=15,
            background_color=get_color_from_hex('#adb5bd'),
            background_normal='', color=(1,1,1,1),
            on_release=lambda x: popup.dismiss(),
        ))
        content.add_widget(btn_box)

        popup = Popup(
            title='', content=content,
            size_hint=(0.8, 0.35),
            separator_height=0, background='',
            background_color=(1,1,1,1),
        )
        popup.open()

    def _show_error_dialog(self):
        content = BoxLayout(orientation='vertical', padding=[20, 15], spacing=12)
        content.add_widget(Label(
            text='\u5bc6\u7801\u9519\u8bef\uff01',
            font_size=16, color=get_color_from_hex('#e74c3c'),
            size_hint_y=None, height=50,
            halign='center',
        ))

        def on_ok(instance):
            popup.dismiss()
            self.manager.current = 'home'

        btn_box = BoxLayout(size_hint_y=None, height=44, spacing=10)
        btn_box.add_widget(Button(
            text='\u786e\u5b9a', font_size=15,
            background_color=get_color_from_hex('#4a6cf7'),
            background_normal='', color=(1,1,1,1),
            on_release=on_ok,
        ))
        content.add_widget(btn_box)

        popup = Popup(
            title='', content=content,
            size_hint=(0.8, 0.3),
            separator_height=0, background='',
            background_color=(1,1,1,1),
        )
        popup.open()

    def _show_confirm_dialog(self):
        content = BoxLayout(orientation='vertical', padding=[20, 15], spacing=12)
        content.add_widget(Label(
            text='\u662f\u5426\u786e\u8ba4\u8981\u6e05\u7a7a\uff0c\u6e05\u7a7a\u540e\u4e0d\u53ef\u6062\u590d\uff01',
            font_size=15, color=get_color_from_hex('#e74c3c'),
            size_hint_y=None, height=50,
            halign='center', text_size=(250, None),
        ))

        def on_confirm(instance):
            popup.dismiss()
            self._clear_all_records()

        btn_box = BoxLayout(size_hint_y=None, height=44, spacing=10)
        btn_box.add_widget(Button(
            text='\u786e\u8ba4\u6e05\u7a7a', font_size=15,
            background_color=get_color_from_hex('#ff6b6b'),
            background_normal='', color=(1,1,1,1),
            on_release=on_confirm,
        ))
        btn_box.add_widget(Button(
            text='\u53d6\u6d88', font_size=15,
            background_color=get_color_from_hex('#adb5bd'),
            background_normal='', color=(1,1,1,1),
            on_release=lambda x: popup.dismiss(),
        ))
        content.add_widget(btn_box)

        popup = Popup(
            title='', content=content,
            size_hint=(0.8, 0.35),
            separator_height=0, background='',
            background_color=(1,1,1,1),
        )
        popup.open()

    def _clear_all_records(self):
        dm = App.get_running_app().data_manager
        dm.today_index = 0
        dm.study_index = 0
        dm.total_learned = 0
        dm.total_cleared = 0
        dm.streak_days = 0
        dm.today_progress = 0
        dm.study_dates = []
        dm.error_words = []
        dm.daily_records = {}
        dm.todays_words = []
        dm.cleared_words = []
        dm.daily_words_date = ''
        dm.last_study_date = ''
        dm.daily_goal = 10
        dm.study_mode = '\u8ba4\u8bfb'
        dm.hint_letters = 1
        dm.hint_phonetic = 1
        dm.hint_tts = 1
        dm.current_grade = '\u4e09\u5e74\u7ea7\u4e0a\u518c'
        dm.total_words = len(dm.words_by_grade.get(dm.current_grade, []))
        dm._recalc_today()
        dm.save_progress()
        # Refresh home screen before navigating
        home = self.manager.get_screen('home')
        if hasattr(home, 'on_enter'):
            home.on_enter()
        self.manager.current = 'home'
