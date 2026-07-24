"""KV language string - mobile-first design for 390x844."""

KV_STRING = r"""
#:import get_color_from_hex kivy.utils.get_color_from_hex

<Label>:
    font_name: 'CJK'

<Button>:
    font_name: 'CJK'

<PhoneticLabel@Label>:
    font_name: 'Latin'

<InfoTag@Label>:
    font_name: 'CJK'
    font_size: 15
    size_hint_y: None
    height: 32
    color: (1, 1, 1, 1)
    halign: 'left'
    valign: 'middle'
    padding: [8, 0]
    text_size: self.size

<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'data/bj.png'
            Color:
                rgba: (1,1,1,0.85)
            Rectangle:
                pos: self.pos
                size: self.size
        # Top bar
        BoxLayout:
            size_hint_y: None
            height: '52dp'
            canvas.before:
                Color:
                    rgba: get_color_from_hex('#4a6cf7')
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: "[font=Emoji]\u2715[/font]"
                font_size: '20sp'
                markup: True
                size_hint_x: None
                width: '52dp'
                background_color: (0,0,0,0)
                on_release: root.quit_app()
            Label:
                text: '\u66e6\u66e6\u7231\u5355\u8bcd'
                font_size: '20sp'
                bold: True
                color: (1,1,1,1)
                size_hint_x: 1
            Button:
                text: "[font=Emoji]\u2699[/font]"
                font_size: '20sp'
                markup: True
                size_hint_x: None
                width: '52dp'
                background_color: (0,0,0,0)
                on_release: root.open_menu()
        # Content
        BoxLayout:
            orientation: 'vertical'
            padding: ['14dp', '10dp', '14dp', '24dp']
            spacing: '10dp'
            # Info area - card style
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: '200dp'
                padding: ['12dp', '8dp']
                spacing: '5dp'
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#ffffff')
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [14]
                # Top spacer for vertical centering
                Widget:
                    size_hint_y: 1
                # Row 1
                BoxLayout:
                    size_hint_y: None
                    height: '44dp'
                    spacing: '8dp'
                    InfoTag:
                        id: tag_today
                        text: ''
                        color: (1,1,1,1)
                        canvas.before:
                            Color:
                                rgba: get_color_from_hex('#ff922b')
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [8]
                    InfoTag:
                        id: tag_total
                        text: ''
                        color: (1,1,1,1)
                        canvas.before:
                            Color:
                                rgba: get_color_from_hex('#51cf66')
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [8]
                # Row 2
                BoxLayout:
                    size_hint_y: None
                    height: '44dp'
                    spacing: '8dp'
                    InfoTag:
                        id: tag_grade
                        text: ''
                        color: (1,1,1,1)
                        canvas.before:
                            Color:
                                rgba: get_color_from_hex('#ffa94d')
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [8]
                    InfoTag:
                        id: tag_words
                        text: ''
                        color: (1,1,1,1)
                        canvas.before:
                            Color:
                                rgba: get_color_from_hex('#845ef7')
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [8]
                # Row 3
                BoxLayout:
                    size_hint_y: None
                    height: '44dp'
                    spacing: '8dp'
                    InfoTag:
                        id: tag_remain
                        text: ''
                        color: (1,1,1,1)
                        canvas.before:
                            Color:
                                rgba: get_color_from_hex('#ff6b6b')
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [8]
                    InfoTag:
                        id: tag_streak
                        text: ''
                        color: (1,1,1,1)
                        canvas.before:
                            Color:
                                rgba: get_color_from_hex('#74c0fc')
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [8]
                # Bottom spacer for vertical centering
                Widget:
                    size_hint_y: 1
            # Function buttons at bottom
            Widget:
            GridLayout:
                cols: 2
                spacing: '10dp'
                size_hint_y: None
                height: '160dp'
                GridLayout:
                    cols: 2
                    spacing: '8dp'
                    row_default_height: '80dp'
                    row_force_default: True
                    Button:
                        markup: True
                        text: "[font=Emoji]\U0001f4da[/font] [font=CJK]\u5b66\u4e60[/font]"
                        font_size: '18sp'
                        halign: 'center'
                        background_color: (0,0,0,0)
                        background_normal: ''
                        color: (1,1,1,1)
                        on_release: root.goto_study()
                        canvas.before:
                            Color:
                                rgba: get_color_from_hex('#4a6cf7')
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [16]
                    Button:
                        markup: True
                        text: "[font=Emoji]\U0001f3af[/font] [font=CJK]\u901a\u5173[/font]"
                        font_size: '18sp'
                        halign: 'center'
                        background_color: (0,0,0,0)
                        background_normal: ''
                        color: (1,1,1,1)
                        on_release: root.goto_challenge()
                        canvas.before:
                            Color:
                                rgba: get_color_from_hex('#ff6b6b')
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [16]
                    Button:
                        markup: True
                        text: "[font=Emoji]\u2753[/font] [font=CJK]\u6613\u9519[/font]"
                        font_size: '18sp'
                        halign: 'center'
                        background_color: (0,0,0,0)
                        background_normal: ''
                        color: (1,1,1,1)
                        on_release: root.goto_error_words()
                        canvas.before:
                            Color:
                                rgba: get_color_from_hex('#ffa94d')
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [16]
                    Button:
                        markup: True
                        text: "[font=Emoji]\U0001f4ca[/font] [font=CJK]\u7edf\u8ba1[/font]"
                        font_size: '18sp'
                        halign: 'center'
                        background_color: (0,0,0,0)
                        background_normal: ''
                        color: (1,1,1,1)
                        on_release: root.goto_calendar()
                        canvas.before:
                            Color:
                                rgba: get_color_from_hex('#51cf66')
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [16]

<StudyScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: get_color_from_hex('#f0f4ff')
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: '52dp'
            canvas.before:
                Color:
                    rgba: get_color_from_hex('#4a6cf7')
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: "[font=Emoji]\u2b05[/font]"
                markup: True
                font_size: '20sp'
                size_hint_x: None
                width: '52dp'
                background_color: (0,0,0,0)
                on_release: root.go_back()
            Label:
                text: '\u4eca\u65e5\u5b66\u4e60'
                font_size: '20sp'
                bold: True
                color: (1,1,1,1)
            Label:
                id: progress_label
                text: ''
                font_size: '16sp'
                size_hint_x: None
                width: '60dp'
                color: (1,1,1,1)
        BoxLayout:
            orientation: 'vertical'
            padding: ['20dp', '16dp']
            spacing: '12dp'
            # Spacer
            Widget:
                size_hint_y: None
                height: '30dp'
            # Square card centered
            BoxLayout:
                size_hint_y: None
                height: '300dp'
                orientation: 'vertical'
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#ffffff')
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [20]
                    Color:
                        rgba: get_color_from_hex('#e0e8ff')
                    Line:
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 20)
                        width: 2
                # Spacer for vertical centering
                Widget:
                    size_hint_y: 0.1
                # Image/emoji at top
                Label:
                    id: image_label
                    text: ''
                    font_size: '80sp'
                    size_hint_y: 0.3
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'
                # Word
                Label:
                    id: word_label
                    text: ''
                    font_size: '36sp'
                    bold: True
                    color: get_color_from_hex('#333333')
                    size_hint_y: 0.15
                # Phonetic row
                BoxLayout:
                    size_hint_y: 0.12
                    spacing: '6dp'
                    Widget:
                        size_hint_x: None
                        width: '36dp'
                    PhoneticLabel:
                        id: phonetic_label
                        text: ''
                        font_size: '24sp'
                        color: get_color_from_hex('#666666')
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                    Button:
                        id: speaker_btn
                        text: '\U0001f50a'
                        font_name: 'Emoji'
                        font_size: '20sp'
                        size_hint_x: None
                        width: '36dp'
                        background_color: (0,0,0,0)
                        color: get_color_from_hex('#4a6cf7')
                        on_press: root.on_speaker_press()
                        on_release: root.on_speaker_release()
                # Meaning
                Label:
                    id: meaning_label
                    text: ''
                    font_size: '22sp'
                    color: get_color_from_hex('#555555')
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'
                    size_hint_y: 0.25
                # Spacer
                Widget:
                    size_hint_y: 0.08
            # Next button (disabled for 3s)
            Button:
                id: next_btn
                text: '\u4e0b\u4e00\u4e2a'
                font_size: '18sp'
                size_hint_y: None
                height: '54dp'
                background_color: get_color_from_hex('#4a6cf7')
                background_normal: ''
                color: (1,1,1,1)
                disabled: True
                on_release: root.on_next()
            Widget:

<ChallengeScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: get_color_from_hex('#f0f4ff')
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: '52dp'
            canvas.before:
                Color:
                    rgba: get_color_from_hex('#ff6b6b')
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: "[font=Emoji]\u2b05[/font]"
                markup: True
                font_size: '20sp'
                size_hint_x: None
                width: '52dp'
                background_color: (0,0,0,0)
                on_release: root.go_back()
            Label:
                text: '\u6253\u5361\u901a\u5173'
                font_size: '20sp'
                bold: True
                color: (1,1,1,1)
            Label:
                id: progress_label
                text: ''
                font_size: '16sp'
                size_hint_x: None
                width: '60dp'
                color: (1,1,1,1)
        BoxLayout:
            orientation: 'vertical'
            padding: ['20dp', '16dp']
            spacing: '12dp'
            Widget:
                size_hint_y: None
                height: '30dp'
            BoxLayout:
                size_hint_y: None
                height: '300dp'
                orientation: 'vertical'
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#ffffff')
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [20]
                    Color:
                        rgba: get_color_from_hex('#ffe0e8')
                    Line:
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 20)
                        width: 2
                Widget:
                    size_hint_y: 0.1
                Label:
                    id: image_label
                    text: ''
                    font_size: '80sp'
                    size_hint_y: 0.3
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'
                Label:
                    id: word_label
                    text: ''
                    font_size: '36sp'
                    bold: True
                    color: get_color_from_hex('#333333')
                    size_hint_y: 0.15
                BoxLayout:
                    size_hint_y: 0.12
                    spacing: '6dp'
                    PhoneticLabel:
                BoxLayout:
                    size_hint_y: 0.12
                    spacing: '6dp'
                    Widget:
                        size_hint_x: None
                        width: '36dp'
                    PhoneticLabel:
                        id: phonetic_label
                        text: ''
                        font_size: '24sp'
                        color: get_color_from_hex('#666666')
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                    Button:
                        id: speaker_btn
                        text: '\U0001f50a'
                        font_name: 'Emoji'
                        font_size: '20sp'
                        size_hint_x: None
                        width: '36dp'
                        background_color: (0,0,0,0)
                        color: get_color_from_hex('#4a6cf7')
                        on_press: root.on_speaker_press()
                        on_release: root.on_speaker_release()
                Label:
                    id: meaning_label
                    text: ''
                    font_size: '22sp'
                    color: get_color_from_hex('#555555')
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'
                    size_hint_y: 0.25
                Widget:
                    size_hint_y: 0.08
            GridLayout:
                id: choice_grid
                cols: 2
                spacing: '10dp'
                size_hint_y: None
                height: '110dp'
                Button:
                    id: choice_0
                    text: ''
                    font_size: '20sp'
                    size_hint_y: None
                    height: '50dp'
                    background_color: (0.95, 0.95, 0.97, 1)
                    background_normal: ''
                    color: get_color_from_hex('#333333')
                    on_release: root.select_answer(self, self.text)
                Button:
                    id: choice_1
                    text: ''
                    font_size: '20sp'
                    size_hint_y: None
                    height: '50dp'
                    background_color: (0.95, 0.95, 0.97, 1)
                    background_normal: ''
                    color: get_color_from_hex('#333333')
                    on_release: root.select_answer(self, self.text)
                Button:
                    id: choice_2
                    text: ''
                    font_size: '20sp'
                    size_hint_y: None
                    height: '50dp'
                    background_color: (0.95, 0.95, 0.97, 1)
                    background_normal: ''
                    color: get_color_from_hex('#333333')
                    on_release: root.select_answer(self, self.text)
                Button:
                    id: choice_3
                    text: ''
                    font_size: '20sp'
                    size_hint_y: None
                    height: '50dp'
                    background_color: (0.95, 0.95, 0.97, 1)
                    background_normal: ''
                    color: get_color_from_hex('#333333')
                    on_release: root.select_answer(self, self.text)
            # Spelling mode: display + letter tiles + clear
            Label:
                id: spell_display
                text: ''
                font_size: '22sp'
                bold: True
                size_hint_y: None
                height: '0dp'
                opacity: 0
                color: get_color_from_hex('#333333')
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#f0f4ff')
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [8]
            GridLayout:
                id: letter_grid
                cols: 6
                spacing: '6dp'
                padding: ['8dp', '0dp']
                size_hint_y: None
                height: '0dp'
                opacity: 0
            Button:
                id: spell_clear
                text: '\u5220\u9664'
                font_size: '15sp'
                size_hint_y: None
                height: '0dp'
                opacity: 0
                disabled: True
                background_color: get_color_from_hex('#ff6b6b')
                background_normal: ''
                color: (1,1,1,1)
                on_release: root._on_spell_clear()
            Button:
                id: done_btn
                text: '\u5b8c\u6210\u4e86\uff0c\u56de\u5bb6'
                font_size: '18sp'
                size_hint_y: None
                height: '0dp'
                opacity: 0
                disabled: True
                background_color: get_color_from_hex('#51cf66')
                background_normal: ''
                color: (1,1,1,1)
                on_release: root.on_done()
            Widget:

<ErrorWordsScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: get_color_from_hex('#f0f4ff')
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: '52dp'
            canvas.before:
                Color:
                    rgba: get_color_from_hex('#ffa94d')
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: "[font=Emoji]\u2b05[/font]"
                markup: True
                font_size: '20sp'
                size_hint_x: None
                width: '52dp'
                background_color: (0,0,0,0)
                on_release: root.go_back()
            Label:
                text: '\u6613\u9519\u5355\u8bcd'
                font_size: '20sp'
                bold: True
                color: (1,1,1,1)
            Label:
                id: progress_label
                text: ''
                font_size: '16sp'
                size_hint_x: None
                width: '60dp'
                color: (1,1,1,1)
        BoxLayout:
            orientation: 'vertical'
            padding: ['16dp', '12dp']
            spacing: '10dp'
            ScrollView:
                id: error_scroll
                do_scroll_x: False
                BoxLayout:
                    id: error_list
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: '4dp'
            Button:
                text: '\u968f\u673a\u91cd\u7ec3'
                font_size: '18sp'
                size_hint_y: None
                height: '50dp'
                background_color: get_color_from_hex('#ff6b6b')
                background_normal: ''
                color: (1,1,1,1)
                on_release: root.start_practice()

<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: get_color_from_hex('#f0f4ff')
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: '52dp'
            canvas.before:
                Color:
                    rgba: get_color_from_hex('#4a6cf7')
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: "[font=Emoji]\u2b05[/font]"
                markup: True
                font_size: '20sp'
                size_hint_x: None
                width: '52dp'
                background_color: (0,0,0,0)
                on_release: root.go_back()
            Label:
                font_size: '20sp'
                bold: True
                color: (1,1,1,1)
            Widget:
                size_hint_x: None
                width: '52dp'
        BoxLayout:
            orientation: 'vertical'
            padding: ['16dp', '24dp', '16dp', '14dp']
            spacing: '14dp'
            # Grade selection
            Label:
                text: '\u9009\u62e9\u5e74\u7ea7'
                font_size: '16sp'
                bold: True
                size_hint_y: None
                height: '28dp'
                text_size: self.size
                halign: 'left'
                color: get_color_from_hex('#333333')
            GridLayout:
                cols: 2
                spacing: '8dp'
                size_hint_y: None
                height: '200dp'
                Button:
                    id: grade_0
                    text: '\u4e09\u5e74\u7ea7\u4e0a\u518c'
                    font_size: '15sp'
                    background_color: get_color_from_hex('#4a6cf7')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_grade('\u4e09\u5e74\u7ea7\u4e0a\u518c')
                Button:
                    id: grade_1
                    text: '\u4e09\u5e74\u7ea7\u4e0b\u518c'
                    font_size: '15sp'
                    background_color: get_color_from_hex('#4a6cf7')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_grade('\u4e09\u5e74\u7ea7\u4e0b\u518c')
                Button:
                    id: grade_2
                    text: '\u56db\u5e74\u7ea7\u4e0a\u518c'
                    font_size: '15sp'
                    background_color: get_color_from_hex('#4a6cf7')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_grade('\u56db\u5e74\u7ea7\u4e0a\u518c')
                Button:
                    id: grade_3
                    text: '\u56db\u5e74\u7ea7\u4e0b\u518c'
                    font_size: '15sp'
                    background_color: get_color_from_hex('#4a6cf7')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_grade('\u56db\u5e74\u7ea7\u4e0b\u518c')
                Button:
                    id: grade_4
                    text: '\u4e94\u5e74\u7ea7\u4e0a\u518c'
                    font_size: '15sp'
                    background_color: get_color_from_hex('#4a6cf7')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_grade('\u4e94\u5e74\u7ea7\u4e0a\u518c')
                Button:
                    id: grade_5
                    text: '\u4e94\u5e74\u7ea7\u4e0b\u518c'
                    font_size: '15sp'
                    background_color: get_color_from_hex('#4a6cf7')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_grade('\u4e94\u5e74\u7ea7\u4e0b\u518c')
                Button:
                    id: grade_6
                    text: '\u516d\u5e74\u7ea7\u4e0a\u518c'
                    font_size: '15sp'
                    background_color: get_color_from_hex('#4a6cf7')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_grade('\u516d\u5e74\u7ea7\u4e0a\u518c')
                Button:
                    id: grade_7
                    text: '\u516d\u5e74\u7ea7\u4e0b\u518c'
                    font_size: '15sp'
                    background_color: get_color_from_hex('#4a6cf7')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_grade('\u516d\u5e74\u7ea7\u4e0b\u518c')
            # Daily goal selection
            GridLayout:
                id: goal_grid
                cols: 4
                spacing: '8dp'
                size_hint_y: None
                height: '44dp'
                Button:
                    text: '5'
                    font_size: '16sp'
                    background_color: get_color_from_hex('#74c0fc')
                    id: goal_5
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_goal(5)
                Button:
                    text: '10'
                    font_size: '16sp'
                    background_color: get_color_from_hex('#4a6cf7')
                    id: goal_10
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_goal(10)
                Button:
                    text: '15'
                    font_size: '16sp'
                    background_color: get_color_from_hex('#74c0fc')
                    id: goal_15
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_goal(15)
                Button:
                    text: '20'
                    font_size: '16sp'
                    background_color: get_color_from_hex('#74c0fc')
                    id: goal_20
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_goal(20)
            Widget:
                size_hint_y: None
                height: '8dp'
            # Study mode
            Label:
                text: '\u5b66\u4e60\u6a21\u5f0f'
                font_size: '16sp'
                bold: True
                size_hint_y: None
                height: '28dp'
                text_size: self.size
                halign: 'left'
                color: get_color_from_hex('#333333')
            BoxLayout:
                id: mode_box
                size_hint_y: None
                height: '44dp'
                spacing: '8dp'
                Button:
                    id: mode_read
                    text: '\u8ba4\u8bfb'
                    font_size: '15sp'
                    background_color: get_color_from_hex('#4a6cf7')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_mode('\u8ba4\u8bfb')
                Button:
                    id: mode_spell
                    text: '\u62fc\u5199'
                    font_size: '15sp'
                    background_color: get_color_from_hex('#74c0fc')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.set_mode('\u62fc\u5199')
            # Hints for challenge
            Label:
                text: '\u6253\u5361\u63d0\u793a'
                font_size: '16sp'
                bold: True
                size_hint_y: None
                height: '28dp'
                text_size: self.size
                halign: 'left'
                color: get_color_from_hex('#333333')
            BoxLayout:
                size_hint_y: None
                height: '36dp'
                spacing: '6dp'
                Label:
                    text: '\u5b57\u6bcd\u4e2a\u6570'
                    font_size: '16sp'
                    color: get_color_from_hex('#555555')
                    size_hint_x: 0.5
                    text_size: self.size
                    halign: 'left'
                Button:
                    id: hint_letters_btn
                    text: '\u5f00\u542f'
                    font_size: '15sp'
                    size_hint_x: 0.5
                    background_color: get_color_from_hex('#51cf66')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.toggle_hint('letters')
            BoxLayout:
                size_hint_y: None
                height: '36dp'
                spacing: '6dp'
                Label:
                    text: '\u63d0\u793a\u97f3\u6807'
                    font_size: '16sp'
                    color: get_color_from_hex('#555555')
                    size_hint_x: 0.5
                    text_size: self.size
                    halign: 'left'
                Button:
                    id: hint_phonetic_btn
                    text: '\u5f00\u542f'
                    font_size: '15sp'
                    size_hint_x: 0.5
                    background_color: get_color_from_hex('#51cf66')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.toggle_hint('phonetic')
            BoxLayout:
                size_hint_y: None
                height: '36dp'
                spacing: '6dp'
                Label:
                    text: '\u6717\u8bf5\u63d0\u9192'
                    font_size: '16sp'
                    color: get_color_from_hex('#555555')
                    size_hint_x: 0.5
                    text_size: self.size
                    halign: 'left'
                Button:
                    id: hint_tts_btn
                    text: '\u5f00\u542f'
                    font_size: '15sp'
                    size_hint_x: 0.5
                    background_color: get_color_from_hex('#51cf66')
                    background_normal: ''
                    color: (1,1,1,1)
                    on_release: root.toggle_hint('tts')
            Widget:
                size_hint_y: None
                height: '6dp'
            Button:
                text: '\u5173\u4e8e'
                size_hint_y: None
                height: '44dp'
                font_size: '15sp'
                background_color: get_color_from_hex('#845ef7')
                background_normal: ''
                color: (1,1,1,1)
                on_release: root.goto_about()
            Widget:

<CalendarScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: get_color_from_hex('#f0f4ff')
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: '52dp'
            canvas.before:
                Color:
                    rgba: get_color_from_hex('#4a6cf7')
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: "[font=Emoji]\u2b05[/font]"
                markup: True
                font_size: '20sp'
                size_hint_x: None
                width: '52dp'
                background_color: (0,0,0,0)
                on_release: root.go_back()
            Label:
                text: '\u5b66\u4e60\u7edf\u8ba1'
                font_size: '20sp'
                bold: True
                color: (1,1,1,1)
            Widget:
                size_hint_x: None
                width: '52dp'
        BoxLayout:
            size_hint_y: None
            height: '44dp'
            padding: ['14dp', '4dp']
            spacing: '8dp'
            Button:
                text: '\u4e0a\u6708'
                font_size: '16sp'
                size_hint_x: None
                width: '70dp'
                background_color: get_color_from_hex('#4a6cf7')
                background_normal: ''
                color: (1,1,1,1)
                on_release: root.prev_month()
            Label:
                id: cal_title
                text: ''
                font_size: '20sp'
                bold: True
                color: get_color_from_hex('#333333')
            Button:
                text: '\u4e0b\u6708'
                font_size: '16sp'
                size_hint_x: None
                width: '70dp'
                background_color: get_color_from_hex('#4a6cf7')
                background_normal: ''
                color: (1,1,1,1)
                on_release: root.next_month()
        GridLayout:
            id: cal_grid
            cols: 7
            spacing: '2dp'
            padding: ['10dp', '2dp', '10dp', '0dp']
            row_default_height: '50dp'
            row_force_default: True
        Label:
            id: cal_summary
            text: ''
            size_hint_y: None
            height: '44dp'
            font_size: '18sp'
            color: get_color_from_hex('#333333')
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            canvas.before:
                Color:
                    rgba: get_color_from_hex('#ffffff')
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [8]
        BoxLayout:
            size_hint_y: None
            height: '32dp'
            padding: ['14dp', '0dp']
            spacing: '10dp'
            Label:
                text: '\u5df2\u5b8c\u6210'
                font_size: '15sp'
                color: get_color_from_hex('#51cf66')
                text_size: self.size
                halign: 'left'
            Label:
                text: '\u672a\u5b8c\u6210'
                font_size: '15sp'
                color: get_color_from_hex('#ff6b6b')
                text_size: self.size
                halign: 'left'
        Widget:

<AboutScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: get_color_from_hex('#f0f4ff')
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: '52dp'
            canvas.before:
                Color:
                    rgba: get_color_from_hex('#4a6cf7')
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: "[font=Emoji]\u2b05[/font]"
                markup: True
                font_size: '20sp'
                size_hint_x: None
                width: '52dp'
                background_color: (0,0,0,0)
                on_release: root.go_back()
            Label:
                text: '\u5173\u4e8e'
                font_size: '20sp'
                bold: True
                color: (1,1,1,1)
            Widget:
                size_hint_x: None
                width: '52dp'
        BoxLayout:
            orientation: 'vertical'
            padding: '24dp'
            spacing: '14dp'
            Label:
                text: '\u7248\u672c\uff1a1.0.0\n\n\u4f5c\u8005\uff1a\u6e05\u98ce\n\n\u5fae\u4fe1\uff1aboldwinzyg'
                font_size: '18sp'
                halign: 'center'
                valign: 'middle'
                text_size: self.size
                color: get_color_from_hex('#333333')
                line_height: 1.8
            Widget:
                size_hint_y: None
                height: '20dp'
            Button:
                id: clear_btn
                text: '\u6e05\u7a7a\u5b66\u4e60\u8bb0\u5f55'
                font_size: '16sp'
                size_hint_y: None
                height: '48dp'
                background_color: get_color_from_hex('#ff6b6b')
                background_normal: ''
                color: (1,1,1,1)
                on_release: root.on_clear_records()
            Widget:

"""
