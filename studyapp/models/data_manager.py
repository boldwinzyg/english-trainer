# Study Word Data Manager
import json
import os
import random
from datetime import datetime, date, timedelta
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import DictProperty, ListProperty, NumericProperty, StringProperty


class DataManager(EventDispatcher):

    words_by_grade = DictProperty({})
    current_grade = StringProperty("\u4e09\u5e74\u7ea7\u4e0a\u518c")
    todays_words = ListProperty([])
    today_progress = NumericProperty(0)
    total_learned = NumericProperty(0)
    total_cleared = NumericProperty(0)
    study_index = NumericProperty(0)
    cleared_words = ListProperty([])
    total_words = NumericProperty(0)
    streak_days = NumericProperty(0)
    error_words = ListProperty([])
    study_dates = ListProperty([])
    today_index = NumericProperty(0)
    daily_records = DictProperty({})
    daily_goal = NumericProperty(10)
    daily_words_date = StringProperty('')
    study_mode = StringProperty("\u8ba4\u8bfb")  # \u8ba4\u8bfb or \u62fc\u5199
    hint_letters = NumericProperty(1)
    hint_phonetic = NumericProperty(1)
    hint_tts = NumericProperty(1)

    def __init__(self, base_dir, **kwargs):
        super().__init__(**kwargs)
        self.base_dir = base_dir
        Clock.schedule_once(self._init_data, 0)

    def _init_data(self, dt):
        self.load_words()
        self.load_progress()
        self._recalc_today()

    def load_words(self):
        path = os.path.join(self.base_dir, 'data', 'xx.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.words_by_grade = data
        self.total_words = len(data.get(self.current_grade, []))

    def load_progress(self):
        path = os.path.join(self.base_dir, 'user_data', 'progress.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                p = json.load(f)
            self.current_grade = p.get('current_grade', "\u4e09\u5e74\u7ea7\u4e0a\u518c")
            self.total_learned = p.get('total_learned', 0)
            self.total_cleared = p.get('total_cleared', 0)
            self.study_index = p.get('study_index', 0)
            self.cleared_words = p.get('cleared_words', [])
            self.streak_days = p.get('streak_days', 0)
            self.today_index = p.get('today_index', 0)
            self.last_study_date = p.get('last_study_date', '')
            self.daily_words_date = p.get('daily_words_date', '')
            self.study_dates = p.get('study_dates', [])
            self.error_words = p.get('error_words', [])
            self.daily_records = p.get('daily_records', {})
            self.daily_goal = p.get('daily_goal', 10)
            self.study_mode = p.get('study_mode', "\u8ba4\u8bfb")

    def save_progress(self):
        path = os.path.join(self.base_dir, 'user_data', 'progress.json')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        p = {
            'current_grade': self.current_grade,
            'total_learned': self.total_learned,
            'total_cleared': self.total_cleared,
            'study_index': self.study_index,
            'cleared_words': self.cleared_words,
            'streak_days': self.streak_days,
            'today_index': self.today_index,
            'study_dates': self.study_dates,
            'error_words': self.error_words,
            'daily_records': self.daily_records,
            'daily_goal': self.daily_goal,
            'study_mode': self.study_mode,
            'hint_letters': int(self.hint_letters),
            'hint_phonetic': int(self.hint_phonetic),
            'hint_tts': int(self.hint_tts),
            'last_study_date': self.last_study_date,
            'daily_words_date': self.daily_words_date,
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(p, f, ensure_ascii=False, indent=2)

    def _recalc_today(self):
        words = self.words_by_grade.get(self.current_grade, [])
        if not words:
            self.todays_words = []
            return
        today_str = date.today().isoformat()
        # Reset today_index if it's a new day or today's words are missing
        existing = self.daily_records.get(today_str, {})
        stored_words = existing.get('words', [])
        if self.daily_words_date != today_str or not stored_words:
            self.today_index = 0
            self.study_index = 0
            self.daily_words_date = today_str
        # Filter out already cleared words from study pool
        cleared_set = set(w for w in self.cleared_words)
        study_pool = [w for w in words if w.get('word', '') not in cleared_set]
        expected_count = min(self.daily_goal, len(study_pool))
        if stored_words and len(stored_words) == expected_count:
            # Use previously stored words for consistency
            self.todays_words = [w for w in stored_words if w]
        else:
            # New day: randomly select uncleared words and store them
            seed = hash(today_str + self.current_grade) % (2**31)
            rng = random.Random(seed)
            count = min(self.daily_goal, len(study_pool))
            if count > 0:
                self.todays_words = rng.sample(study_pool, count)
            else:
                self.todays_words = []
            self.daily_words_date = today_str
            # Store the selected words in the daily record
            if today_str not in self.daily_records:
                self.daily_records[today_str] = {
                    'planned': count,
                    'finished': 0,
                    'learned_words': [],
                    'error_words': [],
                    'words': self.todays_words,
                }
            else:
                self.daily_records[today_str]['planned'] = count
                self.daily_records[today_str]['words'] = self.todays_words
        if self.todays_words:
            self.today_progress = min(100, int(self.today_index / len(self.todays_words) * 100))
        else:
            self.today_progress = 0

    def get_current_word(self, for_study=False):
        if for_study:
            if self.study_index < len(self.todays_words):
                return self.todays_words[self.study_index]
        else:
            if self.today_index < len(self.todays_words):
                return self.todays_words[self.today_index]
        return None

    def mark_correct(self):
        if self.study_index < len(self.todays_words):
            word = self.todays_words[self.study_index]
            self.study_index += 1
            self.total_learned += 1
            self._record_study_date()
            # Update progress without resetting indices
            total = len(self.todays_words)
            self.today_progress = min(100, int(self.study_index / total * 100)) if total > 0 else 0
            self.save_progress()

    def mark_challenged(self):
        if self.today_index < len(self.todays_words):
            self.today_index += 1
            today_str = date.today().isoformat()
            if today_str in self.daily_records:
                rec = self.daily_records[today_str]
                rec['finished'] = rec.get('finished', 0) + 1
            self.total_cleared += 1
            # Add cleared word to cleared_words list
            w = self.todays_words[self.today_index - 1].get("word", "") if self.today_index > 0 and self.todays_words else ""
            if w and w not in self.cleared_words:
                self.cleared_words.append(w)
            # Update progress
            total = len(self.todays_words)
            self.today_progress = min(100, int(self.today_index / total * 100)) if total > 0 else 0
            self.save_progress()

    def mark_error(self, word_dict):
        w = word_dict.get('word', '')
        found = False
        for ew in self.error_words:
            if ew.get('word') == w:
                ew['count'] = ew.get('count', 1) + 1
                found = True
                break
        if not found:
            entry = dict(word_dict)
            entry['count'] = 1
            self.error_words.append(entry)
        # Also record in daily record
        today_str = date.today().isoformat()
        if today_str in self.daily_records:
            if 'error_words' not in self.daily_records[today_str]:
                self.daily_records[today_str]['error_words'] = []
            self.daily_records[today_str]['error_words'].append(word_dict)
        self.save_progress()

    def _record_study_date(self):
        today = date.today().isoformat()
        if today not in self.study_dates:
            self.study_dates.append(today)
            self.study_dates.sort()
            if len(self.study_dates) >= 2:
                last = date.fromisoformat(self.study_dates[-2])
                if (date.today() - last).days == 1:
                    self.streak_days += 1
                elif (date.today() - last).days > 1:
                    self.streak_days = 1
            else:
                self.streak_days = 1

    def get_daily_record(self, day_str):
        return self.daily_records.get(day_str, {'planned': 0, 'finished': 0, 'learned_words': [], 'error_words': []})

    def get_month_records(self, year, month):
        result = {}
        for day in range(1, 32):
            try:
                d = date(year, month, day)
            except ValueError:
                break
            ds = d.isoformat()
            if ds in self.daily_records:
                result[day] = self.daily_records[ds]
        return result

    def get_words_for_grade(self, grade):
        return self.words_by_grade.get(grade, [])

    def get_all_grades(self):
        return list(self.words_by_grade.keys())

    def is_study_complete(self, for_study=False):
        if for_study:
            return self.study_index >= len(self.todays_words)
        return self.today_index >= len(self.todays_words)
