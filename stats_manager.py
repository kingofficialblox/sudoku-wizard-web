import json
import os
from datetime import date

from app_paths import load_player_data, save_player_data


class StatsManager:
    """Persistent lifetime statistics and level progression."""

    FILE_NAME = "stats.json"
    MODES = ("easy", "medium", "hard")
    COSMETICS = {
        "violet": {"name": "VIOLET ARC", "cost": 0, "accent": (128, 70, 255)},
        "ocean": {"name": "OCEAN AURA", "cost": 5_000, "accent": (45, 155, 255)},
        "emerald": {"name": "EMERALD AURA", "cost": 7_500, "accent": (42, 190, 125)},
        "sunset": {"name": "SUNSET AURA", "cost": 10_000, "accent": (245, 120, 70)},
    }

    def __init__(self):
        self.data = self._load()
        self.last_match_rewards = {"coins": 0, "xp": 0, "hints": 0, "auto_notes": 0}

    @staticmethod
    def _mode_defaults():
        return {
            "wins": 0, "matches": 0, "hints": 0, "numbers": 0,
            "mistakes": 0, "score_total": 0, "best_time": None,
            "least_mistakes": None, "most_hints": 0, "hint_tokens": 0,
        }

    def _defaults(self):
        return {
            "level": 1,
            "xp": 0,
            "coins": 0,
            "hint_tokens": 0,
            "auto_notes_tokens": 0,
            "erase_all_tokens": 0,
            "achievements": {},
            "win_streak": 0,
            "best_streak": 0,
            "daily": {"last_completed": "", "streak": 0, "best_streak": 0, "attempted": "", "best_score": 0, "best_time": None, "completed": 0, "completed_dates": []},
            "cosmetics": {"owned": ["violet"], "equipped": "violet"},
            "modes": {mode: self._mode_defaults() for mode in self.MODES},
        }

    def _load(self):
        data = self._defaults()
        try:
            saved = load_player_data(self.FILE_NAME)
            if not saved:
                return data
            data.update({key: saved[key] for key in data if key in saved})
            # Upgrade older profiles that stored tokens separately per
            # difficulty. Their earned tokens become one shared balance.
            if "hint_tokens" not in saved:
                data["hint_tokens"] = sum(
                    saved.get("modes", {}).get(mode, {}).get("hint_tokens", 0)
                    for mode in self.MODES
                )
            for mode in self.MODES:
                data["modes"].setdefault(mode, self._mode_defaults())
                for key, value in self._mode_defaults().items():
                    data["modes"][mode].setdefault(key, value)
            # These temporary mode-based tiers were replaced by universal
            # I–III achievement progressions and must not linger in saves.
            for obsolete_id in (
                "easy_i", "easy_ii", "easy_iii",
                "medium_i", "medium_ii", "medium_iii",
                "hard_i", "hard_ii", "hard_iii",
            ):
                data["achievements"].pop(obsolete_id, None)
            data["cosmetics"].setdefault("owned", ["violet"])
            data["cosmetics"].setdefault("equipped", "violet")
            if "violet" not in data["cosmetics"]["owned"]:
                data["cosmetics"]["owned"].append("violet")
            data["daily"].setdefault("last_completed", "")
            data["daily"].setdefault("streak", 0)
            data["daily"].setdefault("best_streak", 0)
            data["daily"].setdefault("attempted", "")
            data["daily"].setdefault("best_score", 0)
            data["daily"].setdefault("best_time", None)
            data["daily"].setdefault("completed", 0)
            data["daily"].setdefault("completed_dates", [])
        except (OSError, json.JSONDecodeError):
            pass
        return data

    def save(self):
        if not save_player_data(self.FILE_NAME, self.data):
            print("Statistics could not be saved")

    def xp_required(self):
        return 2500 + (self.data["level"] - 1) * 600

    def add_xp(self, amount):
        self.data["xp"] += max(0, amount)
        while self.data["xp"] >= self.xp_required():
            self.data["xp"] -= self.xp_required()
            self.data["level"] += 1

    def record_match(self, difficulty, won, score, elapsed, mistakes, hints, numbers, game_mode="classic"):
        coins_before = self.data["coins"]
        hints_before = self.data.get("hint_tokens", 0)
        auto_notes_before = self.data.get("auto_notes_tokens", 0)
        mode = self.data["modes"][difficulty.lower()]
        mode["matches"] += 1
        mode["hints"] += hints
        mode["numbers"] += numbers
        mode["mistakes"] += mistakes
        mode["score_total"] += score
        mode["most_hints"] = max(mode["most_hints"], hints)

        reward_multiplier = {"classic": 1.0, "zen": 0.60, "timed": 1.65, "practice": 0.35}.get(game_mode, 1.0)
        if won:
            mode["wins"] += 1
            mode["best_time"] = elapsed if mode["best_time"] is None else min(mode["best_time"], elapsed)
            mode["least_mistakes"] = mistakes if mode["least_mistakes"] is None else min(mode["least_mistakes"], mistakes)
            self.data["win_streak"] += 1
            self.data["best_streak"] = max(self.data["best_streak"], self.data["win_streak"])
            # Every completed puzzle awards Coins, with harder modes paying more.
            win_coins = {"easy": 20, "medium": 35, "hard": 55}[difficulty.lower()]
            score_coins = min(50, score // 1_000)
            self.data["coins"] += max(1, int((win_coins + score_coins) * reward_multiplier))
        else:
            self.data["win_streak"] = 0

        xp_award = max(10, int(max(25, score // 5) * reward_multiplier))
        self.add_xp(xp_award)
        # One shared rule for every difficulty and game mode: earn a Hint
        # Token at 20,000 points, whether the round ends in a win or loss.
        if score >= 20_000:
            self.data["hint_tokens"] += 1
        if score >= 30_000:
            self.data["auto_notes_tokens"] += 1

        unlocked = self._check_achievements(difficulty, won, score, mistakes, hints, elapsed)
        self.last_match_rewards = {
            "coins": self.data["coins"] - coins_before,
            "xp": xp_award,
            "hints": self.data.get("hint_tokens", 0) - hints_before,
            "auto_notes": self.data.get("auto_notes_tokens", 0) - auto_notes_before,
        }
        self.save()
        return unlocked

    def _check_achievements(self, difficulty, won, score, mistakes, hints, elapsed):
        """Unlock milestones once and award their permanent Coin reward."""
        achievements = self.data["achievements"]
        modes = self.data["modes"]
        difficulty = difficulty.lower()
        total_wins = sum(mode["wins"] for mode in modes.values())
        total_matches = sum(mode["matches"] for mode in modes.values())
        total_numbers = sum(mode["numbers"] for mode in modes.values())
        total_hints = sum(mode["hints"] for mode in modes.values())
        total_score = sum(mode["score_total"] for mode in modes.values())
        total_mistakes = sum(mode["mistakes"] for mode in modes.values())
        total_losses = total_matches - total_wins
        checks = (
            ("first_win", won, 50),
            ("perfect_win", won and mistakes == 0, 75),
            ("score_10000", won and score >= 10_000, 100),
            ("streak_3", self.data["win_streak"] >= 3, 100),
            ("all_modes", all(modes[mode]["wins"] > 0 for mode in self.MODES), 150),
            ("streak_5", self.data["win_streak"] >= 5, 175),
            ("hintless_win", won and hints == 0, 100),
            ("speed_demon", won and elapsed <= 300, 125),
            ("hard_hero", won and difficulty.lower() == "hard", 125),
            ("coin_collector", self.data["coins"] >= 500, 150),
            ("easy_graduate", won and difficulty == "easy", 25),
            ("medium_conqueror", won and difficulty == "medium", 45),
            ("easy_trio", modes["easy"]["wins"] >= 3, 60),
            ("medium_trio", modes["medium"]["wins"] >= 3, 90),
            ("hard_trio", modes["hard"]["wins"] >= 3, 150),
            ("wins_10", total_wins >= 10, 125),
            ("wins_25", total_wins >= 25, 250),
            ("matches_10", total_matches >= 10, 75),
            ("matches_50", total_matches >= 50, 200),
            ("streak_10", self.data["win_streak"] >= 10, 300),
            ("score_20000", won and score >= 20_000, 175),
            ("score_30000", won and score >= 30_000, 300),
            ("lightning_easy", won and difficulty == "easy" and elapsed <= 120, 100),
            ("rapid_medium", won and difficulty == "medium" and elapsed <= 240, 150),
            ("flawless_hard", won and difficulty == "hard" and mistakes == 0, 225),
            ("number_scribe", total_numbers >= 100, 75),
            ("number_legend", total_numbers >= 500, 200),
            ("hint_vault", total_hints >= 20, 80),
            ("coin_tycoon", self.data["coins"] >= 1_000, 300),
            ("all_modes_three", all(modes[mode]["wins"] >= 3 for mode in self.MODES), 350),
            ("score_i", won and score >= 5_000, 50),
            ("score_ii", won and score >= 15_000, 150),
            ("score_iii", won and score >= 30_000, 300),
            ("streak_i", self.data["win_streak"] >= 2, 50),
            ("streak_ii", self.data["win_streak"] >= 5, 175),
            ("streak_iii", self.data["win_streak"] >= 10, 300),
            ("coins_i", self.data["coins"] >= 100, 50),
            ("coins_ii", self.data["coins"] >= 500, 150),
            ("coins_iii", self.data["coins"] >= 1_000, 300),
            ("wins_i", total_wins >= 3, 50),
            ("wins_ii", total_wins >= 10, 125),
            ("wins_iii", total_wins >= 25, 250),
            ("wins_50", total_wins >= 50, 400),
            ("wins_75", total_wins >= 75, 550),
            ("wins_100", total_wins >= 100, 750),
            ("wins_150", total_wins >= 150, 1_000),
            ("wins_250", total_wins >= 250, 1_500),
            ("matches_100", total_matches >= 100, 350),
            ("matches_200", total_matches >= 200, 650),
            ("matches_500", total_matches >= 500, 1_250),
            ("numbers_1000", total_numbers >= 1_000, 250),
            ("numbers_2500", total_numbers >= 2_500, 450),
            ("numbers_5000", total_numbers >= 5_000, 750),
            ("numbers_10000", total_numbers >= 10_000, 1_250),
            ("hints_50", total_hints >= 50, 125),
            ("hints_100", total_hints >= 100, 225),
            ("hints_250", total_hints >= 250, 450),
            ("hints_500", total_hints >= 500, 750),
            ("streak_15", self.data["best_streak"] >= 15, 450),
            ("streak_20", self.data["best_streak"] >= 20, 600),
            ("streak_30", self.data["best_streak"] >= 30, 900),
            ("streak_50", self.data["best_streak"] >= 50, 1_500),
            ("coins_2500", self.data["coins"] >= 2_500, 400),
            ("coins_5000", self.data["coins"] >= 5_000, 650),
            ("coins_10000", self.data["coins"] >= 10_000, 1_000),
            ("coins_25000", self.data["coins"] >= 25_000, 2_000),
            ("easy_wins_10", modes["easy"]["wins"] >= 10, 150),
            ("easy_wins_25", modes["easy"]["wins"] >= 25, 300),
            ("easy_wins_50", modes["easy"]["wins"] >= 50, 550),
            ("medium_wins_10", modes["medium"]["wins"] >= 10, 225),
            ("medium_wins_25", modes["medium"]["wins"] >= 25, 425),
            ("medium_wins_50", modes["medium"]["wins"] >= 50, 750),
            ("hard_wins_10", modes["hard"]["wins"] >= 10, 350),
            ("hard_wins_25", modes["hard"]["wins"] >= 25, 650),
            ("hard_wins_50", modes["hard"]["wins"] >= 50, 1_100),
            ("total_score_100k", total_score >= 100_000, 200),
            ("total_score_250k", total_score >= 250_000, 400),
            ("total_score_500k", total_score >= 500_000, 700),
            ("total_score_1m", total_score >= 1_000_000, 1_250),
            ("mistakes_100", total_mistakes >= 100, 100),
            ("mistakes_250", total_mistakes >= 250, 225),
            ("mistakes_500", total_mistakes >= 500, 450),
            ("losses_10", total_losses >= 10, 100),
            ("losses_25", total_losses >= 25, 225),
            ("losses_50", total_losses >= 50, 400),
            ("perfect_easy", won and difficulty == "easy" and mistakes == 0, 75),
            ("perfect_medium", won and difficulty == "medium" and mistakes == 0, 125),
            ("hintless_easy", won and difficulty == "easy" and hints == 0, 75),
            ("hintless_medium", won and difficulty == "medium" and hints == 0, 125),
            ("hintless_hard", won and difficulty == "hard" and hints == 0, 200),
            ("swift_hard", won and difficulty == "hard" and elapsed <= 600, 250),
            ("score_40000", won and score >= 40_000, 500),
        )
        unlocked = []
        for achievement_id, achieved, reward in checks:
            if achieved and not achievements.get(achievement_id, False):
                achievements[achievement_id] = True
                self.data["coins"] += reward
                unlocked.append(achievement_id)
        return unlocked

    def get_hint_tokens(self, difficulty=None):
        """Return the single hint balance shared by every difficulty and mode."""
        return self.data.get("hint_tokens", 0)

    def set_hint_tokens(self, difficulty, amount):
        """Persist the shared lifetime Hint Token balance immediately."""
        self.data["hint_tokens"] = max(0, amount)
        self.save()

    def buy_hint(self, difficulty, cost):
        if self.data["coins"] < cost:
            return False
        self.data["coins"] -= cost
        self.data["hint_tokens"] += 1
        self.save()
        return True

    def get_auto_notes_tokens(self):
        return self.data.get("auto_notes_tokens", 0)

    def set_auto_notes_tokens(self, amount):
        self.data["auto_notes_tokens"] = max(0, amount)
        self.save()

    def buy_auto_notes(self, cost):
        if self.data["coins"] < cost:
            return False
        self.data["coins"] -= cost
        self.data["auto_notes_tokens"] += 1
        self.save()
        return True

    def get_erase_all_tokens(self):
        return self.data.get("erase_all_tokens", 0)

    def set_erase_all_tokens(self, amount):
        self.data["erase_all_tokens"] = max(0, amount)
        self.save()

    def buy_erase_all(self, cost):
        if self.data["coins"] < cost:
            return False
        self.data["coins"] -= cost
        self.data["erase_all_tokens"] += 1
        self.save()
        return True

    def buy_or_equip_cosmetic(self, cosmetic_id):
        """Buy a visual aura once, or equip it if it is already owned."""
        item = self.COSMETICS.get(cosmetic_id)
        if item is None:
            return "invalid"
        cosmetics = self.data["cosmetics"]
        if cosmetic_id not in cosmetics["owned"]:
            if self.data["coins"] < item["cost"]:
                return "not_enough"
            self.data["coins"] -= item["cost"]
            cosmetics["owned"].append(cosmetic_id)
        cosmetics["equipped"] = cosmetic_id
        self.save()
        return "equipped"

    def complete_daily_challenge(self):
        """Claim today's one-time Daily Challenge reward and maintain its streak."""
        today = date.today().isoformat()
        daily = self.data["daily"]
        if daily["last_completed"] == today:
            return False, daily["streak"]
        try:
            previous = date.fromisoformat(daily["last_completed"])
            daily["streak"] = daily["streak"] + 1 if (date.today() - previous).days == 1 else 1
        except ValueError:
            daily["streak"] = 1
        daily["last_completed"] = today
        if today not in daily["completed_dates"]:
            daily["completed_dates"].append(today)
        daily["completed"] += 1
        daily["best_streak"] = max(daily["best_streak"], daily["streak"])
        self.data["coins"] += 250 + daily["streak"] * 25
        self.save()
        return True, daily["streak"]

    def begin_daily_attempt(self, recover_stale_attempt=False):
        today = date.today().isoformat()
        daily = self.data["daily"]
        if daily.get("last_completed") == today:
            return False
        if daily.get("attempted") == today and not recover_stale_attempt:
            return False
        daily["attempted"] = today
        self.save()
        return True

    def record_daily_result(self, score, elapsed):
        daily = self.data["daily"]
        daily["best_score"] = max(daily["best_score"], score)
        daily["best_time"] = elapsed if daily["best_time"] is None else min(daily["best_time"], elapsed)
        self.save()
