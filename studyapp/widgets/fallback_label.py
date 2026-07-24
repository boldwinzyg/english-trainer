"""FallbackLabel and FallbackButton - automatic font fallback for mixed content."""
from kivy.uix.widget import Widget
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.properties import (
    StringProperty, NumericProperty, ListProperty,
    BooleanProperty, OptionProperty
)
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.text import Label as CoreLabel


def _classify(code):
    """Classify a unicode codepoint to a font key."""
    if ((0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF) or
        (0x20000 <= code <= 0x2CEAF) or (0xF900 <= code <= 0xFAFF) or
        (0x2F800 <= code <= 0x2FA1F) or (0x3000 <= code <= 0x303F) or
        (0xFF00 <= code <= 0xFFEF)):
        return 'CJK'
    if ((0x1F600 <= code <= 0x1F64F) or (0x1F300 <= code <= 0x1F5FF) or
        (0x1F680 <= code <= 0x1F6FF) or (0x1F1E0 <= code <= 0x1F1FF) or
        (0x2600 <= code <= 0x26FF) or (0x2700 <= code <= 0x27BF) or
        (0x1F900 <= code <= 0x1F9FF) or (0x1FA00 <= code <= 0x1FAFF) or
        (0xFE00 <= code <= 0xFE0F)):
        return 'Emoji'
    return 'Latin'


class FallbackLabel(Widget):
    """A label that renders each character with its appropriate font."""
    text = StringProperty('')
    font_size = NumericProperty(14)
    font_name = StringProperty('CJK')
    color = ListProperty((0, 0, 0, 1))
    bold = BooleanProperty(False)
    italic = BooleanProperty(False)
    markup = BooleanProperty(False)
    halign = OptionProperty('left', options=['left', 'center', 'right'])
    valign = OptionProperty('bottom', options=['bottom', 'middle', 'top'])
    text_size = ListProperty([None, None])
    padding = ListProperty([0, 0])
    size_hint_y = NumericProperty(None, allownone=True)
    size_hint_x = NumericProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.bind(
            text=self._schedule_refresh,
            font_size=self._schedule_refresh,
            color=self._schedule_refresh,
            bold=self._schedule_refresh,
            italic=self._schedule_refresh,
            markup=self._schedule_refresh,
            halign=self._schedule_refresh,
            valign=self._schedule_refresh,
        )
        self.bind(pos=self._redraw)

    def _schedule_refresh(self, *args):
        from kivy.clock import Clock
        Clock.unschedule(self._refresh)
        Clock.schedule_once(self._refresh, 0)

    def _refresh(self, dt=None):
        if not self.text:
            self.canvas.clear()
            self.size = (0, self.font_size)
            return
        font_map = {'CJK': 'CJK', 'Latin': 'Latin', 'Emoji': 'Emoji'}
        segments = []
        cur_font = None
        cur_text = ''
        for ch in self.text:
            key = _classify(ord(ch))
            if key != cur_font:
                if cur_text:
                    segments.append((cur_font, cur_text))
                cur_font = key
                cur_text = ch
            else:
                cur_text += ch
        if cur_text:
            segments.append((cur_font, cur_text))
        rects = []
        total_w = 0
        max_h = 0
        for fk, txt in segments:
            cl = CoreLabel(
                text=txt,
                font_name=font_map.get(fk, 'CJK'),
                font_size=self.font_size,
                bold=self.bold,
            )
            cl.refresh()
            tex = cl.texture
            w, h = tex.size if tex else cl.size
            rects.append((tex, w, h))
            total_w += w
            if h > max_h:
                max_h = h
        new_w = total_w if total_w > 0 else 1
        new_h = max_h if max_h > 0 else self.font_size
        self.width = new_w
        self.height = new_h
        self._rects = rects
        self._total_w = total_w
        self._max_h = max_h
        self._redraw()

    def _redraw(self, *args):
        if not hasattr(self, '_rects'):
            return
        self.canvas.clear()
        total_w = getattr(self, '_total_w', 0)
        max_h = getattr(self, '_max_h', self.font_size)
        if self.halign == 'center':
            x = self.x + (self.width - total_w) / 2
        elif self.halign == 'right':
            x = self.x + self.width - total_w
        else:
            x = self.x
        if self.valign == 'middle':
            y = self.y + (self.height - max_h) / 2
        elif self.valign == 'top':
            y = self.y + self.height - max_h
        else:
            y = self.y
        for tex, w, h in self._rects:
            if tex:
                self.canvas.add(Color(1, 1, 1, 1))
                self.canvas.add(Rectangle(texture=tex, pos=(x, y), size=(w, h)))
            x += w


class FallbackButton(ButtonBehavior, Widget):
    """A button with font-fallback text rendering."""
    text = StringProperty('')
    font_size = NumericProperty(14)
    font_name = StringProperty('CJK')
    color = ListProperty((1, 1, 1, 1))
    bold = BooleanProperty(False)
    markup = BooleanProperty(False)
    background_color = ListProperty((0.3, 0.5, 1, 1))
    background_normal = StringProperty('')
    halign = OptionProperty('center', options=['left', 'center', 'right'])
    valign = OptionProperty('middle', options=['bottom', 'middle', 'top'])
    text_size = ListProperty([None, None])
    padding = ListProperty([0, 0])
    size_hint_y = NumericProperty(None, allownone=True)
    size_hint_x = NumericProperty(None, allownone=True)
    radius = ListProperty([8])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._state = 'normal'
        self._fallback_lbl = FallbackLabel(
            font_size=self.font_size,
            bold=self.bold,
            color=self.color,
            halign=self.halign,
            valign=self.valign,
        )
        self.add_widget(self._fallback_lbl)
        self.bind(
            text=self._update_fallback,
            font_size=self._update_fallback,
            bold=self._update_fallback,
            color=self._update_fallback,
            halign=self._update_fallback,
            valign=self._update_fallback,
            pos=self._update_graphics,
            size=self._update_graphics,
            background_color=self._update_graphics,
            radius=self._update_graphics,
        )
        self._update_graphics()

    def _update_fallback(self, *args):
        if hasattr(self, '_fallback_lbl') and self._fallback_lbl:
            self._fallback_lbl.text = self.text
            self._fallback_lbl.font_size = self.font_size
            self._fallback_lbl.bold = self.bold
            self._fallback_lbl.color = self.color
            self._fallback_lbl.halign = self.halign
            self._fallback_lbl.valign = self.valign

    def _update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            c = self.background_color
            if self._state == 'down' and c[3] > 0:
                c = [max(0, v - 0.15) for v in c[:3]] + [c[3]]
            Color(*c)
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._state = 'down'
            self._update_graphics()
            return True
        return False

    def on_touch_up(self, touch):
        if self._state == 'down':
            self._state = 'normal'
            self._update_graphics()
            if self.collide_point(*touch.pos):
                self.dispatch('on_release')
        return False
