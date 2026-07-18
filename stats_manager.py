import json
import os


class StatsManager:
    """Persistent lifetime statistics and level progression."""

    FILE_NAME = "stats.json"
    MODES = ("easy", "medium", "hard")

    def __init__(self):
        self.data = self._load()

    @staticmethod
    def _mode_defaults():
        return {
            "wins": 0, "matches": 0, "hints": 0, "numbers": 0,
            "mistakes": 0, "score_total": 0, "best_time": None,
            "least_mistakes": None, "most_hints": 0,
        }

    def _defaults(self):
        return {
            "level": 1,
            "xp": 0,
            "win_streak": 0,
            "best_streak": 0,
            "modes": {mode: self._mode_defaults() for mode in self.MODES},
        }

    def _load(self):
        data = self._defaults()
        try:
            with open(self.FILE_NAME, "r") as file:
                saved = json.load(file)
            data.update({key: saved[key] for key in data if key in saved})
            for mode in self.MODES:
                data["modes"].setdefault(mode, self._mode_defaults())
                for key, value in self._mode_defaults().items():
                    data["modes"][mode].setdefault(key, value)
        except (OSError, json.JSONDecodeError):
            pass
        return data

    def save(self):
        with open(self.FILE_NAME, "w") as file:
            json.dump(self.data, file, indent=4)

    def xp_required(self):
        return 2500 + (self.data["level"] - 1) * 600

    def add_xp(self, amount):
        self.data["xp"] += max(0, amount)
        while self.data["xp"] >= self.xp_required():
            self.data["xp"] -= self.xp_required()
            self.data["level"] += 1

    def record_match(self, difficulty, won, score, elapsed, mistakes, hints, numbers):
        mode = self.data["modes"][difficulty.lower()]
        mode["matches"] += 1
        mode["hints"] += hints
        mode["numbers"] += numbers
        mode["mistakes"] += mistakes
        mode["score_total"] += score
        mode["most_hints"] = max(mode["most_hints"], hints)

        if won:
            mode["wins"] += 1
            mode["best_time"] = elapsed if mode["best_time"] is None else min(mode["best_time"], elapsed)
            mode["least_mistakes"] = mistakes if mode["least_mistakes"] is None else min(mode["least_mistakes"], mistakes)
            self.data["win_streak"] += 1
            self.data["best_streak"] = max(self.data["best_streak"], self.data["win_streak"])
        else:
            self.data["win_streak"] = 0

        self.add_xp(max(25, score // 5))
        self.save()
