import pygame

from button import Button
from constants import HEIGHT, WIDTH, PORTRAIT_MODE


class TutorialMenu:
    """A short, readable guide that works equally well with mouse or touch."""

    def __init__(self, game):
        self.game = game
        self.page = 0
        self.title_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 42 if PORTRAIT_MODE else 48)
        self.heading_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 25 if PORTRAIT_MODE else 28)
        self.body_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 18 if PORTRAIT_MODE else 20)
        button_y = HEIGHT - (220 if PORTRAIT_MODE else 130)
        self.back_button = Button(WIDTH // 2 - 235, button_y, 190, 58, "BACK")
        self.next_button = Button(WIDTH // 2 - 95, button_y, 190, 58, "NEXT")
        self.close_button = Button(WIDTH // 2 - 95, button_y, 190, 58, "GOT IT")

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        if self.page == 0 and self.next_button.clicked(event.pos):
            self.page = 1
            self.game.play_sound(self.game.click_sound)
        elif self.page == 1 and self.back_button.clicked(event.pos):
            self.page = 0
            self.game.play_sound(self.game.click_sound)
        elif self.page == 1 and self.next_button.clicked(event.pos):
            self.page = 2
            self.game.play_sound(self.game.click_sound)
        elif self.page == 2 and self.back_button.clicked(event.pos):
            self.page = 1
            self.game.play_sound(self.game.click_sound)
        elif self.page == 2 and self.close_button.clicked(event.pos):
            self.game.play_sound(self.game.click_sound)
            self.game.tutorial_seen = True
            self.game.save_settings()
            self.game.tutorial_open = False

    def _line(self, surface, text, center_x, y, color):
        rendered = self.body_font.render(text, True, color)
        self.game.screen.blit(rendered, rendered.get_rect(center=(center_x, y)))

    def draw(self):
        screen = self.game.screen
        theme = self.game.theme
        screen.fill(theme["background"])

        panel_width = min(WIDTH - 56, 760)
        panel_top = 90 if PORTRAIT_MODE else 60
        panel_bottom = HEIGHT - (300 if PORTRAIT_MODE else 210)
        panel = pygame.Rect(WIDTH // 2 - panel_width // 2, panel_top, panel_width, panel_bottom - panel_top)
        pygame.draw.rect(screen, theme["shadow"], panel.move(0, 8), border_radius=28)
        pygame.draw.rect(screen, theme["popup"], panel, border_radius=28)
        pygame.draw.rect(screen, theme["popup_border"], panel, 2, border_radius=28)

        title = self.title_font.render("HOW TO PLAY", True, theme["text"])
        screen.blit(title, title.get_rect(center=(WIDTH // 2, panel.y + 60)))
        pygame.draw.line(screen, theme["accent"], (panel.x + 55, panel.y + 100), (panel.right - 55, panel.y + 100), 2)

        if self.page == 0:
            heading = self.heading_font.render("THE SUDOKU RULES", True, theme["accent"])
            screen.blit(heading, heading.get_rect(center=(WIDTH // 2, panel.y + 150)))
            lines = (
                "Fill every empty square with a number from 1 to 9.",
                "Each row must contain every number once.",
                "Each column must contain every number once.",
                "Every 3 x 3 box must also contain every number once.",
                "A number cannot repeat in its row, column, or box.",
            )
            for index, line in enumerate(lines):
                y = panel.y + 210 + index * (62 if PORTRAIT_MODE else 54)
                pygame.draw.circle(screen, theme["accent"], (panel.x + 70, y), 6)
                self._line(screen, line, WIDTH // 2 + 25, y, theme["text"])
            self._line(screen, "Tap NEXT to learn the controls and progression.", WIDTH // 2, panel.bottom - 70, theme["secondary"])

        elif self.page == 1:
            heading = self.heading_font.render("GAME CONTROLS", True, theme["accent"])
            screen.blit(heading, heading.get_rect(center=(WIDTH // 2, panel.y + 150)))
            lines = (
                ("1. Tap an empty square to select it."),
                ("2. Tap a number on the number pad to place it."),
                ("3. Hint Tokens are shared across every difficulty and mode."),
                ("4. Pencil toggles Notes mode for possible numbers."),
                ("5. Eraser clears notes; Undo reverses your last move."),
            )
            for index, line in enumerate(lines):
                y = panel.y + 210 + index * (62 if PORTRAIT_MODE else 54)
                self._line(screen, line, WIDTH // 2, y, theme["text"])
            self._line(screen, "Classic and Timed have a 3-mistake limit; Zen and Practice do not.", WIDTH // 2, panel.bottom - 70, theme["secondary"])

        else:
            heading = self.heading_font.render("MODES & PROGRESSION", True, theme["accent"])
            screen.blit(heading, heading.get_rect(center=(WIDTH // 2, panel.y + 150)))
            lines = (
                "Classic is balanced; Zen has no game-over limit.",
                "Timed: 10-minute bonus round. Practice reveals wrong answers.",
                "Each match can earn Coins, XP, Stars, and shared Hint Tokens.",
                "Daily Challenge offers one competitive puzzle every day.",
                "Stats track wins, streaks, records, levels, and achievements.",
            )
            for index, line in enumerate(lines):
                y = panel.y + 210 + index * (62 if PORTRAIT_MODE else 54)
                pygame.draw.circle(screen, theme["success"], (panel.x + 70, y), 6)
                self._line(screen, line, WIDTH // 2 + 25, y, theme["text"])
            self._line(screen, "Good luck, Sudoku Wizard!", WIDTH // 2, panel.bottom - 70, theme["accent"])

        page_label = self.body_font.render(f"{self.page + 1} / 3", True, theme["secondary"])
        screen.blit(page_label, page_label.get_rect(center=(WIDTH // 2, panel.bottom - 30)))

        if self.page == 0:
            self.next_button.rect.center = (WIDTH // 2, self.next_button.rect.centery)
            buttons = (self.next_button,)
        elif self.page == 1:
            self.back_button.rect.center = (WIDTH // 2 - 140, self.back_button.rect.centery)
            self.next_button.rect.center = (WIDTH // 2 + 140, self.next_button.rect.centery)
            buttons = (self.back_button, self.next_button)
        else:
            buttons = (self.close_button,)
        for button in buttons:
            button.bg_color = theme["button"]
            button.hover_color = theme["button_hover"]
            button.border_color = theme["grid"]
            button.text_color = theme["text"]
            button.draw(screen)
