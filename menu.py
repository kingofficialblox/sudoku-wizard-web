import pygame

from button import Button
from constants import *


class Menu:

    def __init__(self, game):

        self.game = game

        self.screen = game.screen

        self.theme = game.theme
        self.settings_button = pygame.Rect(
            WIDTH - 110,   # move slightly left
            120,           # move lower
            75,            # larger click area
            75
        )

        self.settings_hover = False
        self.settings_pressed = False
        self.settings_scale = 1.0

        self.title_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            72
        )

        self.subtitle_font = pygame.font.Font(
            "assets/fonts/Poppins-Regular.ttf",
            22
        )
        self.title_font = pygame.font.Font(
            "assets/fonts/Poppins-ExtraBold.ttf",
            96
        )

        self.subtitle_font = pygame.font.Font(
            "assets/fonts/Poppins-ExtraBold.ttf",
            96
        )
        self.credit_font = pygame.font.Font(
            "assets/fonts/Poppins-Regular.ttf",
            20
        )

        self.creator_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            28
        )

        self.play_button = Button(
            WIDTH//2 - 180,
            455,
            360,
            75,
            "PLAY"
        )

        self.continue_button = Button(
            WIDTH//2 - 180,
            555,
            360,
            75,
            "CONTINUE"
        )

        self.choose_difficulty = False
        self.difficulty_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            30
        )
        choice_width = 150
        choice_gap = 20
        choice_x = (WIDTH - (choice_width * 3 + choice_gap * 2)) // 2
        self.easy_button = Button(choice_x, 500, choice_width, 70, "EASY")
        self.medium_button = Button(choice_x + choice_width + choice_gap, 500, choice_width, 70, "MEDIUM")
        self.hard_button = Button(choice_x + (choice_width + choice_gap) * 2, 500, choice_width, 70, "HARD")

        self.exit_button = Button(
            WIDTH//2 - 180,
            655,
            360,
            75,
            "EXIT"
        )
        self.stats_button = Button(
            WIDTH//2 - 180,
            755,
            360,
            75,
            "STATISTICS"
        )
        

    def update(self):

        self.theme = self.game.theme

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        pos = event.pos
        self.settings_pressed = False

        if self.choose_difficulty:
            for difficulty, button in (
                ("EASY", self.easy_button),
                ("MEDIUM", self.medium_button),
                ("HARD", self.hard_button),
            ):
                if button.clicked(pos):
                    self.game.play_sound(self.game.click_sound)
                    self.game.new_game(difficulty)
                    self.game.current_screen = "game"
                    self.choose_difficulty = False
                    return

        elif self.continue_button.clicked(pos):
            if self.game.game_started:
                self.game.play_sound(self.game.click_sound)
                self.game.logic.resume()
                self.game.paused = False
                self.game.play_music_track(self.game.difficulty)
                self.game.current_screen = "game"
            else:
                self.continue_message_until = pygame.time.get_ticks() + 2200

        elif self.play_button.clicked(pos):

            self.game.play_sound(
                self.game.click_sound
            )

            self.choose_difficulty = True
        elif self.exit_button.clicked(pos):

            self.game.play_sound(
                self.game.click_sound
            )

            self.game.running = False

        elif self.stats_button.clicked(pos):
            self.game.play_sound(self.game.click_sound)
            self.game.stats_open = True

        elif self.settings_button.collidepoint(pos):

            self.settings_pressed = True

            self.game.play_sound(
                self.game.click_sound
            )

            self.game.settings_open = True
    def draw(self):

        self.screen.fill(
            self.theme["background"]
        )
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        pygame.draw.circle(
            overlay,
            self.theme["circle"],
            (WIDTH//2, HEIGHT//2),
            480
        )

        self.screen.blit(overlay,(0,0))

        # Subtle Sudoku grid gives the menu depth without competing with controls.
        grid_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        grid_color = (*self.theme["accent"], 28)
        grid_size = 58
        for index, x in enumerate(range(-grid_size, WIDTH + grid_size, grid_size)):
            width = 2 if index % 3 == 0 else 1
            pygame.draw.line(grid_overlay, grid_color, (x, 0), (x, HEIGHT), width)
        for index, y in enumerate(range(-grid_size, HEIGHT + grid_size, grid_size)):
            width = 2 if index % 3 == 0 else 1
            pygame.draw.line(grid_overlay, grid_color, (0, y), (WIDTH, y), width)
        self.screen.blit(grid_overlay, (0, 0))

        title1 = self.title_font.render(
            "SUDOKU",
            True,
            self.theme["text"]
        )

        title2 = self.subtitle_font.render(
            "WIZARD",
            True,
            self.theme["accent"]
        )

        self.screen.blit(
            title1,
            title1.get_rect(center=(WIDTH//2,190))
        )

        self.screen.blit(
            title2,
            title2.get_rect(center=(WIDTH//2,295))
        )

        

        if self.choose_difficulty:
            buttons = (self.easy_button, self.medium_button, self.hard_button)
        else:
            buttons = (self.play_button, self.continue_button, self.exit_button, self.stats_button)
        for b in buttons:
            b.bg_color = self.theme["button"]
            b.hover_color = self.theme["button_hover"]
            b.border_color = self.theme["grid"]
            b.text_color = self.theme["text"]

        if self.choose_difficulty:
            prompt = self.difficulty_font.render("CHOOSE DIFFICULTY", True, self.theme["text"])
            self.screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 425)))
            self.easy_button.draw(self.screen)
            self.medium_button.draw(self.screen)
            self.hard_button.draw(self.screen)
        else:
            self.play_button.draw(self.screen)
            self.continue_button.draw(self.screen)
            self.exit_button.draw(self.screen)
            self.stats_button.draw(self.screen)
            if getattr(self, "continue_message_until", 0) > pygame.time.get_ticks():
                message = self.credit_font.render("No game available to continue", True, self.theme["accent"])
                self.screen.blit(message, message.get_rect(center=(WIDTH // 2, 820)))
        mouse = pygame.mouse.get_pos()

        self.settings_hover = self.settings_button.collidepoint(mouse)

        target = 1.0

        if self.settings_hover:
            target = 1.12

        if self.settings_pressed:
            target = 0.90

        self.settings_scale += (
            target - self.settings_scale
        ) * 0.22

        size = int(60 * self.settings_scale)

        icon = pygame.transform.smoothscale(
            self.game.settings_icon,
            (65,65)
        )

        rect = icon.get_rect(
            center=(
                WIDTH - 65,
                150
            )
        )

        shadow = pygame.Surface(
            (size + 10, size + 10),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            shadow,
            (0,0,0,35),
            (
                shadow.get_width()//2,
                shadow.get_height()//2
            ),
            size//2 + 4
        )

        shadow_rect = shadow.get_rect(
            center=(
                rect.centerx,
                rect.centery + 4
            )
        )

        self.screen.blit(shadow, shadow_rect)

        if self.settings_hover:

            glow = pygame.Surface(
                (size + 18, size + 18),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                glow,
                (120,120,120,45),
                (
                    glow.get_width()//2,
                    glow.get_height()//2
                ),
                size//2 + 5
            )

            glow_rect = glow.get_rect(
                center=rect.center
            )

            self.screen.blit(glow, glow_rect)

        self.screen.blit(icon, rect)
        # ---------- Bottom Credit ----------

        line_y = HEIGHT - 180       

        pygame.draw.line(
            self.screen,
            (170,120,255),
            (WIDTH//2 - 180, line_y),
            (WIDTH//2 - 30, line_y),
            2
        )

        pygame.draw.line(
            self.screen,
            (170,120,255),
            (WIDTH//2 + 30, line_y),
            (WIDTH//2 + 180, line_y),
            2
        )

        pygame.draw.circle(
            self.screen,
            (170,120,255),
            (WIDTH//2, line_y),
            5
        )

        made = self.credit_font.render(
            "MADE BY",
            True,
            (90,90,90)
        )

        creator = self.credit_font.render(
            "META_CREATORS",
            True,
            (128,70,255)
        )

        self.screen.blit(
            made,
            made.get_rect(center=(WIDTH//2, HEIGHT-140))
        )

        self.screen.blit(
            creator,
            creator.get_rect(center=(WIDTH//2, HEIGHT-100))
        )
