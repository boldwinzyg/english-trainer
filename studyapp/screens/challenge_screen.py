"""Challenge screen - reading mode (CN->EN) and spelling mode (letter tiles)."""
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.core.audio import SoundLoader
import os


class ChallengeScreen(Screen):
    current_word = None
    score = 0
    question_num = 0
    _challenge_words = []  # shuffled daily words for challenge
    _spell_letters = []  # scrambled letters for spelling
    _spell_selected = []  # indices of selected letters
    _letter_buttons = []  # references to letter tile buttons

    practice_mode = False
    practice_words = []
    practice_correct = {}  # word -> correct count

    def on_enter(self):
        if not self.practice_mode:
            self.score = 0
            self.question_num = 0
            self._challenge_words = []
            self._next_question()

    def start_practice(self, words):
        self.practice_mode = True
        self.practice_words = list(words)
        self.practice_correct = {}
        for w in words:
            self.practice_correct[w.get("word", "")] = 0
        self.score = 0
        self.question_num = 0
        self._next_question()

    def on_kv_post(self, base_widget):
        img = self.ids.get("image_label")
        if img:
            img.font_name = 'Emoji'

    def _next_question(self):
        dm = App.get_running_app().data_manager
        if self.practice_mode:
            words = list(self.practice_words)
        else:
            if not self._challenge_words:
                self._challenge_words = list(dm.todays_words)
                random.shuffle(self._challenge_words)
            words = self._challenge_words
        if not words or self.question_num >= len(words):
            # Show final score
            self._spell_user_letters = []
            self.ids.word_label.text = "\u7ed3\u675f!\n\u5f97\u5206: {}/{}".format(self.score, len(words))
            self.ids.image_label.text = "\U0001f389"
            self.ids.progress_label.text = ""
            self._hide_all_inputs()
            self._clear_letter_grid()
            done_btn = self.ids.get("done_btn")
            if done_btn:
                done_btn.opacity = 1
                done_btn.height = "54dp"
                done_btn.disabled = False
            if self.practice_mode:
                self.practice_mode = False
                self.practice_words = []
            return
        self.question_num += 1
        word = words[self.question_num - 1]
        self.current_word = word
        # Auto TTS if enabled
        if dm.hint_tts:
            Clock.schedule_once(lambda dt: self._auto_speak_word(word), 0.3)
        mode = dm.study_mode
        # Show Chinese meaning + image
        self.ids.word_label.text = word.get("meaning", "")
        self.ids.image_label.text = word.get("emoji", "")
        self.ids.progress_label.text = "{}/{}".format(self.question_num, len(words))
        # Apply hint_phonetic setting
        phonetic_label = self.ids.get("phonetic_label")
        if phonetic_label:
            if dm.hint_phonetic:
                phonetic_label.text = word.get("phonetic", "")
            else:
                phonetic_label.text = ""
        if mode == "\u62fc\u5199":
            self._setup_spelling_mode(word)
        else:
            self._setup_reading_mode(word)

    def _hide_all_inputs(self):
        choice_grid = self.ids.get("choice_grid")
        if choice_grid:
            choice_grid.opacity = 0
            choice_grid.height = "0dp"
        for i in range(4):
            btn = self.ids.get("choice_{}".format(i))
            if btn:
                btn.opacity = 0
                btn.disabled = True
        spell_input = self.ids.get("spell_input")
        if spell_input:
            spell_input.opacity = 0
            spell_input.disabled = True
        submit_btn = self.ids.get("spell_submit")
        if submit_btn:
            submit_btn.opacity = 0
            submit_btn.disabled = True
        word_display = self.ids.get("spell_display")
        if word_display:
            word_display.opacity = 0
            word_display.height = "0dp"
        clear_btn = self.ids.get("spell_clear")
        if clear_btn:
            clear_btn.opacity = 0
            clear_btn.disabled = True
            clear_btn.height = "0dp"
        letter_grid = self.ids.get("letter_grid")
        if letter_grid:
            letter_grid.opacity = 0
            letter_grid.height = "0dp"
        done_btn = self.ids.get("done_btn")
        if done_btn:
            done_btn.opacity = 0
            done_btn.height = "0dp"
            done_btn.disabled = True

    def _setup_reading_mode(self, word):
        dm = App.get_running_app().data_manager
        # Hide spelling stuff
        word_display = self.ids.get("spell_display")
        if word_display:
            word_display.opacity = 0
            word_display.height = "0dp"
        clear_btn = self.ids.get("spell_clear")
        if clear_btn:
            clear_btn.opacity = 0
            clear_btn.disabled = True
            clear_btn.height = "0dp"
        letter_grid = self.ids.get("letter_grid")
        if letter_grid:
            letter_grid.opacity = 0
            letter_grid.height = "0dp"
        done_btn = self.ids.get("done_btn")
        if done_btn:
            done_btn.opacity = 0
            done_btn.height = "0dp"
            done_btn.disabled = True
        # Show choice buttons
        all_words = []
        for ws in dm.words_by_grade.values():
            all_words.extend(ws)
        # Choices are ENGLISH words
        pool = [w for w in all_words if w.get("word", "") != word.get("word", "")]
        wrong = random.sample(pool, min(3, len(pool)))
        options = [word.get("word", "")] + [w.get("word", "") for w in wrong]
        random.shuffle(options)
        choice_grid = self.ids.get("choice_grid")
        if choice_grid:
            choice_grid.opacity = 1
            choice_grid.height = "110dp"
        for i in range(4):
            btn = self.ids.get("choice_{}".format(i))
            if btn:
                btn.opacity = 1
                btn.disabled = False
                btn.text = options[i] if i < len(options) else ""
                btn.background_color = (0.95, 0.95, 0.97, 1)

    def _setup_spelling_mode(self, word):
        dm = App.get_running_app().data_manager
        # Hide choice buttons
        choice_grid = self.ids.get("choice_grid")
        if choice_grid:
            choice_grid.opacity = 0
            choice_grid.height = "0dp"
        for i in range(4):
            btn = self.ids.get("choice_{}".format(i))
            if btn:
                btn.opacity = 0
                btn.disabled = True
        # Show spelling UI
        word_display = self.ids.get("spell_display")
        if word_display:
            word_display.opacity = 1
            word_display.height = "44dp"
            word_display.text = ""
        clear_btn = self.ids.get("spell_clear")
        if clear_btn:
            clear_btn.opacity = 1
            clear_btn.height = "40dp"
            clear_btn.disabled = False
        letter_grid = self.ids.get("letter_grid")
        if letter_grid:
            letter_grid.opacity = 1
            letter_grid.height = "100dp"
        # Show letter count if hint_letters enabled
        word_display = self.ids.get("spell_display")
        if word_display:
            if dm.hint_letters:
                word_display.text = "___ " * len(word.get("word", ""))
                word_display.text = word_display.text.strip()
        # Build letter tiles
        correct_word = word.get("word", "")
        letters = list(correct_word)
        # Add distractor letters
        all_chars = list("abcdefghijklmnopqrstuvwxyz")
        num_distractors = 12 - len(letters)
        distractors = random.sample([c for c in all_chars if c not in correct_word.lower()], num_distractors)
        self._spell_letters = letters + distractors
        random.shuffle(self._spell_letters)
        self._spell_selected = []
        self._spell_user_letters = []
        self._build_letter_tiles(correct_word)

    def _build_letter_tiles(self, correct_word):
        grid = self.ids.get("letter_grid")
        if not grid:
            return
        grid.clear_widgets()
        self._letter_buttons = []
        for i, letter in enumerate(self._spell_letters):
            btn = Button(
                text=letter,
                font_size=28,
                background_color=get_color_from_hex("#4a6cf7"),
                background_normal="",
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=44,
                opacity=1,
                disabled=False,
            )
            btn.bind(on_release=lambda inst, idx=i: self._on_letter_click(idx))
            self._letter_buttons.append(btn)
            grid.add_widget(btn)

    def _clear_letter_grid(self):
        grid = self.ids.get("letter_grid")
        if grid:
            grid.clear_widgets()
        self._letter_buttons = []
        self._spell_letters = []
        self._spell_selected = []

    def _on_letter_click(self, idx):
        if idx in self._spell_selected:
            return
        self._spell_selected.append(idx)
        self._letter_buttons[idx].opacity = 0.3
        self._letter_buttons[idx].disabled = True
        # Update display - rebuild from user letters + underscores
        self._spell_user_letters.append(self._spell_letters[idx])
        word_display = self.ids.get("spell_display")
        correct = self.current_word.get("word", "")
        if word_display:
            displayed = " ".join(self._spell_user_letters)
            remaining = len(correct) - len(self._spell_user_letters)
            if remaining > 0:
                displayed += " " + "___ " * remaining
            word_display.text = displayed.strip()
        # Check if all letters selected
        dm = App.get_running_app().data_manager
        if len(self._spell_selected) == len(correct):
            user_word = "".join(self._spell_user_letters).lower()
            if user_word == correct.lower():
                self.score += 1
                word_display.background_color = (0.6, 0.95, 0.6, 1)
                self._show_celebration()
                if self.practice_mode:
                    self._on_practice_correct()
                # Mark progress after celebration
                try:
                    if not self.practice_mode:
                        dm.mark_challenged()
                except Exception:
                    pass
            else:
                word_display.background_color = (0.95, 0.6, 0.6, 1)
                self._play_sound('wrong')
                if self.practice_mode:
                    self._on_practice_error()
                elif self.current_word:
                    dm.mark_error(self.current_word)
            # Save and advance after delay
            try:
                dm.save_progress()
            except Exception:
                pass
            Clock.schedule_once(self._safe_next, 2.0)

    def _on_spell_clear(self):
        if not self._spell_selected:
            return
        idx = self._spell_selected.pop()
        self._letter_buttons[idx].opacity = 1
        self._letter_buttons[idx].disabled = False
        self._spell_user_letters.pop()
        word_display = self.ids.get("spell_display")
        if word_display:
            correct = self.current_word.get("word", "")
            displayed = " ".join(self._spell_user_letters)
            remaining = len(correct) - len(self._spell_user_letters)
            if remaining > 0:
                displayed += " " + "___ " * remaining
            word_display.text = displayed.strip()

    def select_answer(self, btn, meaning):
        dm = App.get_running_app().data_manager
        user_answer = btn.text.strip().lower()
        correct = self.current_word.get("word", "").lower()
        if user_answer == correct:
            self.score += 1
            btn.background_color = (0.6, 0.95, 0.6, 1)
            self._show_celebration()
            if self.practice_mode:
                self._on_practice_correct()
            else:
                dm.mark_challenged()
        else:
            btn.background_color = (0.95, 0.6, 0.6, 1)
            self._play_sound('wrong')
            if self.practice_mode:
                self._on_practice_error()
            elif self.current_word:
                dm.mark_error(self.current_word)
        for i in range(4):
            b = self.ids.get("choice_{}".format(i))
            if b:
                b.disabled = True
        Clock.schedule_once(lambda dt: self._next_question(), 1.0)

    def _auto_speak_word(self, word):
        from studyapp.tts import speak
        w = word.get('word', '')
        if not w:
            return
        speak(w)

    def _play_sound(self, name):
        try:
            base = App.get_running_app().data_manager.base_dir
            path = os.path.join(base, 'data', name + '.wav')
            if not os.path.exists(path):
                return
            snd = SoundLoader.load(path)
            if snd:
                snd.play()
        except Exception:
            pass

    def _safe_next(self, dt):
        try:
            from studyapp.widgets.celebration import dismiss_celebration
            dismiss_celebration()
            self._next_question()
        except Exception:
            import traceback
            traceback.print_exc()

    def _show_celebration(self, big=False):
        from studyapp.widgets.celebration import show_celebrate
        show_celebrate(self, 0.5, 0.5, big=big)

    def _on_practice_correct(self):
        dm = App.get_running_app().data_manager
        w = self.current_word.get("word", "")
        self.practice_correct[w] = self.practice_correct.get(w, 0) + 1
        if self.practice_correct[w] >= 2:
            # Remove from error_words
            dm.error_words = [ew for ew in dm.error_words if ew.get("word") != w]
            dm.save_progress()

    def _on_practice_error(self):
        w = self.current_word.get("word", "")
        self.practice_correct[w] = 0

    def repeat_speak(self):
        if self.current_word:
            from studyapp.tts import speak
            speak(self.current_word.get("word", ""))

    def on_speaker_press(self):
        btn = self.ids.get("speaker_btn")
        if btn:
            btn.color = (0.3, 0.8, 0.3, 1)
            btn.font_size = "24sp"

    def on_speaker_release(self):
        btn = self.ids.get("speaker_btn")
        if btn:
            from kivy.utils import get_color_from_hex
            btn.color = get_color_from_hex("#4a6cf7")
            btn.font_size = "20sp"
        self.repeat_speak()

    def go_back(self):
        if self.practice_mode:
            self.practice_mode = False
            self.practice_words = []
        self.manager.current = "home"
