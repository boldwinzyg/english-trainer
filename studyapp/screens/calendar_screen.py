"""Calendar screen with clickable dates and daily detail popup."""
import calendar
from datetime import date
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle, Line


class CalendarDayCell(BoxLayout):
    """A single day cell in the calendar grid."""

    def __init__(self, day_num=0, planned=0, finished=0, is_today=False, is_selected=False, on_click=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [2]
        self.spacing = 1
        self.day_num = day_num
        self.planned = planned
        self.finished = finished
        self.is_today = is_today
        self.is_selected = is_selected
        self.on_click_fn = on_click
        self.size_hint_y = None
        self.height = 50
        with self.canvas.before:
            if day_num == 0:
                Color(0, 0, 0, 0)
            elif is_selected:
                Color(*get_color_from_hex('#4a6cf7'))
            elif planned > 0 and finished >= planned:
                Color(*get_color_from_hex('#51cf66'))
            elif planned > 0 and finished < planned:
                Color(*get_color_from_hex('#ff6b6b'))
            else:
                Color(*get_color_from_hex('#f1f3f5'))
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[6])
            if is_today and not is_selected:
                Color(*get_color_from_hex('#4a6cf7'))
                self._border = Line(
                    rounded_rectangle=(self.x, self.y, self.width, self.height, 6),
                    width=2.5,
                )
            else:
                self._border = None
        self.bind(pos=self._update_rect, size=self._update_rect)
        if day_num > 0:
            text_color = '#ffffff' if (planned > 0 or is_selected) else '#555555'
            self.add_widget(
                Label(
                    text=str(day_num),
                    font_size=11,
                    bold=is_today or is_selected,
                    color=get_color_from_hex(text_color),
                    size_hint_y=0.5,
                )
            )
            if planned > 0:
                self.add_widget(
                    Label(
                        text='{}/{}'.format(finished, planned),
                        font_size=9,
                        color=get_color_from_hex('#ffffff'),
                        size_hint_y=0.35,
                    )
                )
            else:
                self.add_widget(Label(text='', size_hint_y=0.35))
            # Make clickable
            if on_click:
                self.bind(on_touch_down=self._on_touch)
        else:
            self.add_widget(Label(text=''))

    def _on_touch(self, instance, touch):
        if self.collide_point(*touch.pos) and self.day_num > 0:
            if self.on_click_fn:
                self.on_click_fn(self.day_num)
            return True
        return False

    def _update_rect(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size
        if self._border:
            self._border.rounded_rectangle = (self.x, self.y, self.width, self.height, 6)


class CalendarScreen(Screen):
    _month_offset = 0
    _selected_day = None

    def on_enter(self):
        self._month_offset = 0
        self._selected_day = date.today().day
        self._render_calendar()

    def _render_calendar(self):
        dm = App.get_running_app().data_manager
        today = date.today()
        year = today.year
        month = today.month + self._month_offset
        while month > 12:
            month -= 12
            year += 1
        while month < 1:
            month += 12
            year -= 1
        title = self.ids.get('cal_title')
        if title:
            title.text = '{}年{}月'.format(year, month)
        grid = self.ids.get('cal_grid')
        if not grid:
            return
        grid.clear_widgets()
        week_labels = ['一', '二', '三', '四', '五', '六', '日']
        for label in week_labels:
            grid.add_widget(
                Label(
                    text=label,
                    font_size=10,
                    bold=True,
                    color=get_color_from_hex('#666666'),
                    size_hint_y=None,
                    height=24,
                )
            )
        cal = calendar.monthcalendar(year, month)
        month_records = dm.get_month_records(year, month)
        for week in cal:
            for day_num in week:
                if day_num == 0:
                    grid.add_widget(Label(text=''))
                else:
                    rec = month_records.get(day_num, {'planned': 0, 'finished': 0})
                    is_today = (year == today.year and month == today.month and day_num == today.day)
                    is_selected = (day_num == self._selected_day)
                    cell = CalendarDayCell(
                        day_num=day_num,
                        planned=rec.get('planned', 0),
                        finished=rec.get('finished', 0),
                        is_today=is_today,
                        is_selected=is_selected,
                        on_click=self._on_day_click,
                    )
                    grid.add_widget(cell)
        summary = self.ids.get('cal_summary')
        if summary:
            total_planned = sum(r.get('planned', 0) for r in month_records.values())
            total_finished = sum(r.get('finished', 0) for r in month_records.values())
            completed_days = sum(
                1 for r in month_records.values()
                if r.get('planned', 0) > 0 and r.get('finished', 0) >= r.get('planned', 0)
            )
            summary.text = '本月累计: {}/{}  完成天数: {}'.format(
                total_finished, total_planned, completed_days
            )

    def _on_day_click(self, day_num):
        self._selected_day = day_num
        self._render_calendar()
        dm = App.get_running_app().data_manager
        today = date.today()
        year = today.year
        month = today.month + self._month_offset
        while month > 12:
            month -= 12
            year += 1
        while month < 1:
            month += 12
            year -= 1
        day_str = '{}-{:02d}-{:02d}'.format(year, month, day_num)
        record = dm.get_daily_record(day_str)
        learned = record.get('learned_words', [])
        errors = record.get('error_words', [])
        planned = record.get('words', [])
        completed_set = set(w.get('word', '') for w in learned)
        error_set = set(w.get('word', '') for w in errors)
                # Show popup - clean modern design
        from kivy.graphics import Color as Gc, RoundedRectangle as Rr
        # Main container
        box = BoxLayout(orientation='vertical', padding=[0, 0], spacing=0,
                         size_hint_y=None, height=440)
        # ---- Header ----
        header_box = BoxLayout(orientation='horizontal', padding=[20, 0], size_hint_y=None, height=80)
        header = BoxLayout(orientation='vertical', padding=[0, 0, 0, 14], spacing=4,
                            size_hint_y=None, height=80)
        with header.canvas.before:
            Gc(*get_color_from_hex('#4a6cf7'))
            Rr(pos=header.pos, size=header.size, radius=[14, 14, 0, 0])
        def _upd_header(*args):
            header.canvas.before.clear()
            with header.canvas.before:
                Gc(*get_color_from_hex('#4a6cf7'))
                Rr(pos=header.pos, size=header.size, radius=[14, 14, 0, 0])
        header.bind(pos=_upd_header, size=_upd_header)
        header.add_widget(Label(
            text='[b]{} \u5b66\u4e60\u8be6\u60c5[/b]'.format(day_str),
            markup=True, font_size=22,
            color=(1, 1, 1, 1),
            halign='left', text_size=(310, None),
            size_hint_y=None, height=30,
        ))
        finished = record.get('finished', 0)
        planned_cnt = record.get('planned', 0)
        pct = int(finished / planned_cnt * 100) if planned_cnt > 0 else 0
        header.add_widget(Label(
            text='\u5b8c\u6210\u8fdb\u5ea6: {}/{} ({}\u0025)'.format(finished, planned_cnt, pct),
            font_size=14,
            color=(1, 1, 1, 0.9),
            halign='left', text_size=(310, None),
            size_hint_y=None, height=24,
        ))
        header_box.add_widget(header)
        box.add_widget(header_box)
        box.add_widget(Widget(size_hint_y=None, height=14))
        # ---- Content area ----
        content = BoxLayout(orientation='vertical', padding=[20, 12], spacing=6,
                             size_hint_y=None, height=280)
        # Section: 今日单词
        content.add_widget(Label(
            text='[b]\u4eca\u65e5\u5355\u8bcd[/b]', markup=True,
            font_size=16, color=get_color_from_hex('#6c757d'),
            halign='left', text_size=(300, None),
            size_hint_y=None, height=24,
        ))
        # Words card
        words_card = BoxLayout(orientation='vertical', padding=[16, 12], spacing=6,
                                size_hint_y=None, height=100)
        with words_card.canvas.before:
            Gc(*get_color_from_hex('#f8f9fa'))
            Rr(pos=words_card.pos, size=words_card.size, radius=[10])
        def _upd_words(*args):
            words_card.canvas.before.clear()
            with words_card.canvas.before:
                Gc(*get_color_from_hex('#f8f9fa'))
                Rr(pos=words_card.pos, size=words_card.size, radius=[10])
        words_card.bind(pos=_upd_words, size=_upd_words)
        words_data = record.get('words', [])
        if words_data:
            words_row = []
            for w in words_data:
                wd = w.get('word', '')
                if wd in error_set:
                    words_row.append('[color=e74c3c]{}[/color]'.format(wd))
                elif wd in completed_set:
                    words_row.append('[color=27ae60]{}[/color]'.format(wd))
                else:
                    words_row.append('[color=#6c757d]{}[/color]'.format(wd))
            words_card.add_widget(Label(
                text=', '.join(words_row), markup=True,
                font_size=18, color=get_color_from_hex('#212529'),
                text_size=(280, None), halign='left', valign='top',
                size_hint_y=None, height=60,
            ))
        else:
            words_card.add_widget(Label(
                text='\u6682\u65e0\u6570\u636e', font_size=16,
                color=get_color_from_hex('#adb5bd'),
                halign='left', text_size=(280, None),
                size_hint_y=None, height=30,
            ))
        content.add_widget(words_card)
        # Spacer between sections
        content.add_widget(Widget(size_hint_y=None, height=10))
        # Section: 错误单词
        content.add_widget(Label(
            text='[b]\u9519\u8bef\u5355\u8bcd[/b]', markup=True,
            font_size=16, color=get_color_from_hex('#e74c3c'),
            halign='left', text_size=(300, None),
            size_hint_y=None, height=24,
        ))
        # Error card
        error_card = BoxLayout(orientation='vertical', padding=[16, 12], spacing=6,
                                size_hint_y=None, height=60)
        with error_card.canvas.before:
            Gc(*get_color_from_hex('#fff5f5'))
            Rr(pos=error_card.pos, size=error_card.size, radius=[10])
        def _upd_error(*args):
            error_card.canvas.before.clear()
            with error_card.canvas.before:
                Gc(*get_color_from_hex('#fff5f5'))
                Rr(pos=error_card.pos, size=error_card.size, radius=[10])
        error_card.bind(pos=_upd_error, size=_upd_error)
        if errors:
            error_text = ', '.join(w.get('word', '') for w in errors)
            error_card.add_widget(Label(
                text=error_text, font_size=18,
                color=get_color_from_hex('#c0392b'),
                text_size=(280, None), halign='left', valign='top',
                size_hint_y=None, height=30,
            ))
        else:
            error_card.add_widget(Label(
                text='\u6682\u65e0\u6570\u636e', font_size=16,
                color=get_color_from_hex('#adb5bd'),
                halign='left', text_size=(280, None),
                size_hint_y=None, height=30,
            ))
        content.add_widget(error_card)
        box.add_widget(content)
        # ---- Close button ----
        box.add_widget(Widget(size_hint_y=None, height=12))
        close_btn = Button(
            text='\u5173\u95ed',
            size_hint_y=None, height=44, font_size=18,
            background_color=get_color_from_hex('#4a6cf7'),
            background_normal='', color=(1, 1, 1, 1),
        )
        btn_box = BoxLayout(orientation='horizontal', padding=[20, 0], size_hint_y=None, height=44)
        btn_box.add_widget(close_btn)
        box.add_widget(btn_box)
        popup = Popup(title='', content=box, size_hint=(0.88, 0.6),
                      separator_height=0, background='',
                      background_color=(1, 1, 1, 1), padding=0)
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def prev_month(self):
        self._month_offset -= 1
        self._selected_day = None
        self._render_calendar()

    def next_month(self):
        self._month_offset += 1
        self._selected_day = None
        self._render_calendar()

    def go_back(self):
        self.manager.current = 'home'
