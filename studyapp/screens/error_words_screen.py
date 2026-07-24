"""Error words screen - list view with practice button."""
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle


class ErrorWordsScreen(Screen):

    def on_enter(self):
        self._build_list()

    def on_kv_post(self, base_widget):
        pass

    def _build_list(self):
        dm = App.get_running_app().data_manager
        list_container = self.ids.get("error_list")
        if not list_container:
            return
        list_container.clear_widgets()
        if not dm.error_words:
            empty = Label(
                text="\u6682\u65e0\u5bb9\u9519\u5355\u8bcd",
                font_size=18,
                color=get_color_from_hex("#999999"),
                size_hint_y=None,
                height=64,
            )
            list_container.add_widget(empty)
            return
        for i, w in enumerate(dm.error_words):
            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=64,
                spacing=8,
                padding=[8, 4],
            )
            with row.canvas.before:
                Color(*get_color_from_hex("#ffffff"))
                row._rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[8])
            row.bind(pos=lambda inst, val, r=row: setattr(r._rect, "pos", val),
                     size=lambda inst, val, r=row: setattr(r._rect, "size", val))
            row.add_widget(Label(
                text=w.get("word", ""),
                font_size=20,
                bold=True,
                color=get_color_from_hex("#333333"),
                size_hint_x=0.35,
                halign="left",
                valign="middle",
                text_size=(None, None),
            ))
            row.add_widget(Label(
                text=w.get("meaning", ""),
                font_size=16,
                color=get_color_from_hex("#666666"),
                size_hint_x=0.45,
                halign="left",
                valign="middle",
                text_size=(None, None),
            ))
            emoji = w.get("emoji", "")
            count = w.get("count", 1)
            if emoji:
                count_text = "[font=Emoji]{}[/font]x{}".format(emoji, count)
            else:
                count_text = "x{}".format(count)
            row.add_widget(Label(
                text=count_text,
                markup=True,
                font_size=16,
                color=get_color_from_hex("#ff6b6b"),
                size_hint_x=0.2,
                halign="right",
                valign="middle",
                text_size=(None, None),
            ))
            list_container.add_widget(row)

    def start_practice(self):
        dm = App.get_running_app().data_manager
        if not dm.error_words:
            return
        # Pick up to 10 random words
        pool = list(dm.error_words)
        practice_words = random.sample(pool, min(10, len(pool)))
        # Set practice mode on challenge screen
        challenge = self.manager.get_screen("challenge")
        challenge.start_practice(practice_words)
        self.manager.current = "challenge"

    def go_back(self):
        self.manager.current = "home"
