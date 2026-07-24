"""Settings screen."""
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.utils import get_color_from_hex


class SettingsScreen(Screen):
    _grade_names = [
        "\u4e09\u5e74\u7ea7\u4e0a\u518c",
        "\u4e09\u5e74\u7ea7\u4e0b\u518c",
        "\u56db\u5e74\u7ea7\u4e0a\u518c",
        "\u56db\u5e74\u7ea7\u4e0b\u518c",
        "\u4e94\u5e74\u7ea7\u4e0a\u518c",
        "\u4e94\u5e74\u7ea7\u4e0b\u518c",
        "\u516d\u5e74\u7ea7\u4e0a\u518c",
        "\u516d\u5e74\u7ea7\u4e0b\u518c",
    ]

    def on_enter(self):
        dm = App.get_running_app().data_manager
        # Mode buttons
        mode_read = self.ids.get("mode_read")
        mode_spell = self.ids.get("mode_spell")
        if mode_read and mode_spell:
            if dm.study_mode == "\u62fc\u5199":
                mode_read.background_color = get_color_from_hex("#74c0fc")
                mode_spell.background_color = get_color_from_hex("#4a6cf7")
            else:
                mode_read.background_color = get_color_from_hex("#4a6cf7")
                mode_spell.background_color = get_color_from_hex("#74c0fc")
        # Update hint toggles
        hint_map = {
            'letters': 'hint_letters_btn',
            'phonetic': 'hint_phonetic_btn',
            'tts': 'hint_tts_btn',
        }
        val_map = {
            'letters': dm.hint_letters,
            'phonetic': dm.hint_phonetic,
            'tts': dm.hint_tts,
        }
        for key, btn_id in hint_map.items():
            btn = self.ids.get(btn_id)
            if btn:
                if val_map[key]:
                    btn.text = '\u5f00\u542f'
                    btn.background_color = get_color_from_hex('#51cf66')
                else:
                    btn.text = '\u5173\u95ed'
                    btn.background_color = get_color_from_hex('#868e96')
        # Update goal button colors
        goal_ids = {5: 'goal_5', 10: 'goal_10', 15: 'goal_15', 20: 'goal_20'}
        for goal_val, gid in goal_ids.items():
            btn = self.ids.get(gid)
            if btn:
                if dm.daily_goal == goal_val:
                    btn.background_color = get_color_from_hex('#4a6cf7')
                else:
                    btn.background_color = get_color_from_hex('#74c0fc')
        # Update grade button colors
        for i in range(8):
            gid = "grade_{}".format(i)
            btn = self.ids.get(gid)
            if btn:
                grade_name = self._grade_names[i]
                count = len(dm.get_words_for_grade(grade_name))
                btn.text = "{} [{}\u4e2a\u5355\u8bcd]".format(grade_name, count)
                if grade_name == dm.current_grade:
                    btn.background_color = get_color_from_hex("#ff922b")
                else:
                    btn.background_color = get_color_from_hex("#8899dd")

    def set_grade(self, grade):
        dm = App.get_running_app().data_manager
        dm.current_grade = grade
        dm.today_index = 0
        dm._recalc_today()
        dm.save_progress()
        self.on_enter()

    def set_goal(self, count):
        dm = App.get_running_app().data_manager
        dm.daily_goal = count
        dm.today_index = 0
        dm._recalc_today()
        dm.save_progress()
        self.on_enter()

    def set_mode(self, mode):
        dm = App.get_running_app().data_manager
        dm.study_mode = mode
        dm.save_progress()
        self.on_enter()

    def toggle_hint(self, name):
        dm = App.get_running_app().data_manager
        if name == 'letters':
            dm.hint_letters = 0 if dm.hint_letters else 1
        elif name == 'phonetic':
            dm.hint_phonetic = 0 if dm.hint_phonetic else 1
        elif name == 'tts':
            dm.hint_tts = 0 if dm.hint_tts else 1
        dm.save_progress()
        self.on_enter()

    def goto_about(self):
        self.manager.current = "about"

    def go_back(self):
        self.manager.current = "home"
