import pygame

from button import Button
from constants import HEIGHT, WIDTH, PORTRAIT_MODE


class StatsMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.selected = "overall"
        self.title_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 54)
        # Compact values prevent long lifetime-stat labels from crowding cards.
        self.font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 19 if PORTRAIT_MODE else 23)
        self.value_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 24 if PORTRAIT_MODE else 27)
        labels = ("OVERALL", "EASY", "MEDIUM", "HARD")
        self.mode_buttons = [Button(0, 0, 140, 52, label) for label in labels]
        back_y = HEIGHT - (320 if PORTRAIT_MODE else 165)
        self.back_button = Button(WIDTH // 2 - 110, back_y, 220, 55, "BACK")

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        for label, button in zip(("overall", "easy", "medium", "hard"), self.mode_buttons):
            if button.clicked(event.pos):
                self.selected = label
                self.game.play_sound(self.game.click_sound)
                return
        if self.back_button.clicked(event.pos):
            self.game.play_sound(self.game.click_sound)
            self.game.stats_open = False

    @staticmethod
    def _time(seconds):
        if seconds is None:
            return "—"
        return f"{seconds // 60:02}:{seconds % 60:02}"

    def _values(self):
        data = self.game.stats.data
        if self.selected == "overall":
            modes = list(data["modes"].values())
            matches = sum(mode["matches"] for mode in modes)
            wins = sum(mode["wins"] for mode in modes)
            hints = sum(mode["hints"] for mode in modes)
            numbers = sum(mode["numbers"] for mode in modes)
            mistakes = sum(mode["mistakes"] for mode in modes)
            scores = sum(mode["score_total"] for mode in modes)
            times = [mode["best_time"] for mode in modes if mode["best_time"] is not None]
            least = [mode["least_mistakes"] for mode in modes if mode["least_mistakes"] is not None]
            most_hints = max((mode["most_hints"] for mode in modes), default=0)
            return [
                ("Matches won", str(wins)), ("Total matches", str(matches)),
                ("Current win streak", str(data["win_streak"])), ("Best win streak", str(data["best_streak"])),
                ("Win percentage", f"{(wins / matches * 100) if matches else 0:.0f}%"),
                ("Average score", f"{scores // matches if matches else 0:,}"),
                ("Fastest solve", self._time(min(times) if times else None)),
                ("Least mistakes", str(min(least)) if least else "—"),
                ("Most hints in a game", str(most_hints)), ("Hints used", str(hints)),
                ("Numbers entered", str(numbers)), ("Mistakes", str(mistakes)),
            ]
        mode = data["modes"][self.selected]
        matches = mode["matches"]
        return [
            ("Matches won", str(mode["wins"])), ("Total matches", str(matches)),
            ("Win percentage", f"{(mode['wins'] / matches * 100) if matches else 0:.0f}%"),
            ("Average score", f"{mode['score_total'] // matches if matches else 0:,}"),
            ("Fastest solve", self._time(mode["best_time"])),
            ("Least mistakes", str(mode["least_mistakes"]) if mode["least_mistakes"] is not None else "—"),
            ("Most hints in a game", str(mode["most_hints"])), ("Hints used", str(mode["hints"])),
            ("Numbers entered", str(mode["numbers"])), ("Mistakes", str(mode["mistakes"])),
        ]

    def draw(self):
        theme = self.game.theme
        self.screen.fill(theme["background"])
        panel_width = 620 if WIDTH < 900 else 820
        panel_bottom_margin = 250 if PORTRAIT_MODE else 160
        panel = pygame.Rect(WIDTH // 2 - panel_width // 2, 60, panel_width, HEIGHT - panel_bottom_margin)
        pygame.draw.rect(self.screen, theme["shadow"], panel.move(0, 8), border_radius=28)
        pygame.draw.rect(self.screen, theme["popup"], panel, border_radius=28)
        pygame.draw.rect(self.screen, theme["popup_border"], panel, 2, border_radius=28)
        title = self.title_font.render("PLAYER STATS", True, theme["text"])
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 115)))

        for index, button in enumerate(self.mode_buttons):
            button.rect.center = (WIDTH // 2 - 240 + index * 160, 185)
            button.selected = (self.selected == ("overall", "easy", "medium", "hard")[index])
            button.bg_color = theme["button"]
            button.hover_color = theme["button_hover"]
            button.border_color = theme["grid"]
            button.text_color = theme["text"]
            button.draw(self.screen)

        data = self.game.stats.data
        level = self.value_font.render(f"Level {data['level']}", True, theme["accent"])
        xp = self.font.render(f"{data['xp']} / {self.game.stats.xp_required()} XP", True, theme["secondary"])
        self.screen.blit(level, (panel.x + 55, 245))
        self.screen.blit(xp, (panel.right - xp.get_width() - 55, 250))
        pygame.draw.rect(self.screen, theme["popup_border"], (panel.x + 55, 290, panel.width - 110, 10), border_radius=5)
        fill = (panel.width - 110) * data["xp"] / self.game.stats.xp_required()
        pygame.draw.rect(self.screen, theme["accent"], (panel.x + 55, 290, fill, 10), border_radius=5)

        values = self._values()
        for index, (label, value) in enumerate(values):
            col, row = index % 2, index // 2
            card_width = 250 if WIDTH < 900 else 330
            card_gap = 10 if WIDTH < 900 else 30
            card_x = panel.x + 55 + col * (card_width + card_gap)
            card = pygame.Rect(card_x, 335 + row * 82, card_width, 64)
            pygame.draw.rect(self.screen, theme["button"], card, border_radius=14)
            pygame.draw.rect(self.screen, theme["popup_border"], card, 1, border_radius=14)
            label_surface = self.font.render(label, True, theme["secondary"])
            value_surface = self.value_font.render(value, True, theme["text"])
            self.screen.blit(label_surface, (card.x + 15, card.y + 8))
            self.screen.blit(value_surface, (card.right - value_surface.get_width() - 15, card.y + 30))

        self.back_button.bg_color = theme["button"]
        self.back_button.hover_color = theme["button_hover"]
        self.back_button.border_color = theme["grid"]
        self.back_button.text_color = theme["text"]
        self.back_button.draw(self.screen)
