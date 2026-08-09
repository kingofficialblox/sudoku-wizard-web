import pygame
from datetime import datetime, timedelta

from button import Button
from constants import *


class Menu:

    def __init__(self, game):

        self.game = game

        self.screen = game.screen
        # Leave a little breathing room below the native Windows title bar.
        self.desktop_y_offset = 0 if PORTRAIT_MODE else 45

        self.theme = game.theme
        side_icon_y = 730 if PORTRAIT_MODE else 120 + self.desktop_y_offset
        self.settings_button = pygame.Rect(
            WIDTH - 110,   # move slightly left
            side_icon_y,
            75,            # larger click area
            75
        )

        self.settings_hover = False
        self.settings_pressed = False
        self.settings_scale = 1.0
        self.store_button = pygame.Rect(WIDTH - 110, side_icon_y + 90, 75, 75)
        self.store_hover = False
        self.store_pressed = False
        self.achievements_button = pygame.Rect(WIDTH - 110, side_icon_y + 180, 75, 75)
        self.achievements_hover = False
        self.stats_icon_button = pygame.Rect(WIDTH - 110, side_icon_y + 270, 75, 75)
        self.stats_icon_hover = False

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
        self.streak_fire = pygame.image.load(
            "assets/images/streak_fire.png"
        ).convert_alpha()
        self.streak_fire_large = pygame.transform.smoothscale(
            self.streak_fire, (122, 122)
        )
        self.streak_fire_small = pygame.transform.smoothscale(
            self.streak_fire, (76, 76)
        )
        self.streak_label_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf", 17
        )
        self.streak_value_font = pygame.font.Font(
            "assets/fonts/Poppins-ExtraBold.ttf", 38
        )
        self.coin_font = pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 18)
        self.coin_label_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 13)
        self.coin_icon = pygame.transform.smoothscale(pygame.image.load("assets/images/coin.png").convert_alpha(), (54, 54))
        self.store_icon = pygame.transform.smoothscale(pygame.image.load("assets/images/store.png").convert_alpha(), (62, 62))
        self.medal_icon = pygame.transform.smoothscale(pygame.image.load("assets/images/medal.png").convert_alpha(), (62, 62))
        self.stats_icon = pygame.transform.smoothscale(pygame.image.load("assets/images/stats.png").convert_alpha(), (62, 62))
        self.info_icon = pygame.transform.smoothscale(
            pygame.image.load("assets/images/info.png").convert_alpha(), (38, 38)
        )

        # Desktop leaves room for the large Daily Challenge card above Play.
        # Portrait has plenty of vertical room.  Use it so the featured daily
        # card and the main actions do not feel stacked together.
        menu_button_y = 850 if PORTRAIT_MODE else 545
        menu_gap = 125 if PORTRAIT_MODE else 88
        self.play_button = Button(
            WIDTH//2 - 180,
            menu_button_y,
            360,
            75,
            "PLAY"
        )

        self.continue_button = Button(
            WIDTH//2 - 180,
            menu_button_y + menu_gap,
            360,
            75,
            "CONTINUE"
        )
        # Daily Challenge keeps its large featured-card size above Play.
        self.daily_button = Button(
            WIDTH//2 - 180,
            menu_button_y - menu_gap if PORTRAIT_MODE else 320,
            360,
            75 if PORTRAIT_MODE else 190,
            "DAILY CHALLENGE"
        )
        # The calendar is a secondary action inside the Daily Challenge card.
        # Its dedicated hit area lets players open progress without starting a puzzle.
        self.daily_calendar_button = pygame.Rect(self.daily_button.rect.x + 10, self.daily_button.rect.y + 8, 62, 59)
        self.daily_hover_amount = 0.0
        self.daily_calendar_hover_amount = 0.0

        self.choose_difficulty = False
        self.choose_mode = False
        self.selected_difficulty = None
        self.difficulty_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            30
        )
        choice_width = 150
        choice_gap = 20
        choice_x = (WIDTH - (choice_width * 3 + choice_gap * 2)) // 2
        # Keep the choice row well below Play on phones.  Android can emit a
        # second touch event, so overlapping hit areas would select Hard.
        difficulty_y = 900 if PORTRAIT_MODE else 540 + self.desktop_y_offset
        self.easy_button = Button(choice_x, difficulty_y, choice_width, 70, "EASY")
        self.medium_button = Button(choice_x + choice_width + choice_gap, difficulty_y, choice_width, 70, "MEDIUM")
        self.hard_button = Button(choice_x + (choice_width + choice_gap) * 2, difficulty_y, choice_width, 70, "HARD")
        self.difficulty_back_button = Button(WIDTH // 2 - 110, difficulty_y + 95, 220, 58, "BACK")
        mode_y = 900 if PORTRAIT_MODE else 535 + self.desktop_y_offset
        mode_w, mode_h = 205, 68
        self.classic_mode_button = Button(WIDTH // 2 - mode_w - 12, mode_y, mode_w, mode_h, "CLASSIC")
        self.zen_mode_button = Button(WIDTH // 2 + 12, mode_y, mode_w, mode_h, "ZEN")
        self.timed_mode_button = Button(WIDTH // 2 - mode_w - 12, mode_y + 88, mode_w, mode_h, "TIMED")
        self.practice_mode_button = Button(WIDTH // 2 + 12, mode_y + 88, mode_w, mode_h, "PRACTICE")
        self.mode_back_button = Button(WIDTH // 2 - 110, mode_y + 185, 220, 58, "BACK")

        self.stats_button = Button(
            WIDTH//2 - 180,
            menu_button_y + menu_gap * 3,
            360,
            75,
            "STATISTICS"
        )
        self.tutorial_button = pygame.Rect(
            WIDTH // 2 + (215 if PORTRAIT_MODE else 200),
            (690 if PORTRAIT_MODE else 250),
            40,
            40,
        )
        

    def update(self):
        # The equipped store aura personalizes the main-menu accent without
        # changing the player's chosen Light/Dark readability setting.
        self.theme = self.game.theme.copy()
        cosmetic_id = self.game.stats.data.get("cosmetics", {}).get("equipped", "violet")
        cosmetic = self.game.stats.COSMETICS.get(cosmetic_id)
        if cosmetic:
            self.theme["accent"] = cosmetic["accent"]

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        pos = event.pos
        self.settings_pressed = False

        if self.choose_mode:
            if self.mode_back_button.clicked(pos):
                self.game.play_sound(self.game.click_sound)
                self.choose_mode = False
                self.choose_difficulty = True
                return
            for mode, button in (("classic", self.classic_mode_button), ("zen", self.zen_mode_button), ("timed", self.timed_mode_button), ("practice", self.practice_mode_button)):
                if button.clicked(pos):
                    self.game.play_sound(self.game.click_sound)
                    self.game.new_game(self.selected_difficulty, mode)
                    self.game.current_screen = "game"
                    self.choose_mode = False
                    self.choose_difficulty = False
                    return
        elif self.choose_difficulty:
            if self.difficulty_back_button.clicked(pos):
                self.game.play_sound(self.game.click_sound)
                self.choose_difficulty = False
                return
            for difficulty, button in (
                ("EASY", self.easy_button),
                ("MEDIUM", self.medium_button),
                ("HARD", self.hard_button),
            ):
                if button.clicked(pos):
                    self.game.play_sound(self.game.click_sound)
                    self.selected_difficulty = difficulty
                    self.choose_mode = True
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
        elif self.daily_calendar_button.collidepoint(pos):
            self.game.play_sound(self.game.click_sound)
            self.game.daily_calendar_open = True
        elif self.daily_button.clicked(pos):
            self.game.play_sound(self.game.click_sound)
            today = datetime.now().date().isoformat()
            if (
                self.game.game_started
                and self.game.daily_challenge_active
                and self.game.daily_challenge_date == today
                and not self.game.logic.game_won
                and not self.game.logic.game_over
            ):
                self.game.logic.resume()
                self.game.paused = False
                self.game.current_screen = "game"
            elif self.game.new_daily_challenge():
                self.game.current_screen = "game"
            else:
                self.daily_message_until = pygame.time.get_ticks() + 2200
        elif self.tutorial_button.collidepoint(pos):
            self.game.play_sound(self.game.click_sound)
            self.game.tutorial_menu.page = 0
            self.game.tutorial_open = True

        elif self.settings_button.collidepoint(pos):

            self.settings_pressed = True

            self.game.play_sound(
                self.game.click_sound
            )

            self.game.settings_open = True
        elif self.store_button.collidepoint(pos):
            self.store_pressed = True
            self.game.play_sound(self.game.click_sound)
            self.game.store_open = True
        elif self.achievements_button.collidepoint(pos):
            self.game.play_sound(self.game.click_sound)
            self.game.achievements_open = True
        elif self.stats_icon_button.collidepoint(pos):
            self.game.play_sound(self.game.click_sound)
            self.game.stats_open = True
    def draw(self):

        self.screen.fill(
            self.theme["background"]
        )
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        pygame.draw.circle(
            overlay,
            self.theme["circle"],
            (WIDTH//2, HEIGHT//2 + self.desktop_y_offset),
            600 if not PORTRAIT_MODE else 480
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

        # Persistent Coin balance is always visible from the menu.
        coins = self.game.stats.data.get("coins", 0)
        # Keep the balance below device/window cut-off areas and away from title.
        coin_card = pygame.Rect(42 if PORTRAIT_MODE else 70, 170 if PORTRAIT_MODE else 300 + self.desktop_y_offset, 255, 82)
        coin_glow = pygame.Surface((coin_card.width + 26, coin_card.height + 26), pygame.SRCALPHA)
        pygame.draw.rect(coin_glow, (*self.theme["accent"], 38), coin_glow.get_rect(), border_radius=28)
        self.screen.blit(coin_glow, (coin_card.x - 13, coin_card.y - 13))
        pygame.draw.rect(self.screen, self.theme["shadow"], coin_card.move(0, 7), border_radius=22)
        pygame.draw.rect(self.screen, self.theme["popup"], coin_card, border_radius=22)
        pygame.draw.rect(self.screen, self.theme["accent"], coin_card, 2, border_radius=22)
        self.screen.blit(self.coin_icon, self.coin_icon.get_rect(center=(coin_card.x + 50, coin_card.centery)))
        coin_text = self.coin_font.render(str(coins), True, self.theme["text"])
        coin_label = self.coin_label_font.render("COINS", True, self.theme["secondary"])
        self.screen.blit(coin_label, coin_label.get_rect(midleft=(coin_card.x + 95, coin_card.y + 27)))
        self.screen.blit(coin_text, coin_text.get_rect(midleft=(coin_card.x + 95, coin_card.y + 53)))

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
            title1.get_rect(center=(WIDTH//2,510 if PORTRAIT_MODE else 145))
        )

        self.screen.blit(
            title2,
            title2.get_rect(center=(WIDTH//2,615 if PORTRAIT_MODE else 250))
        )

        

        if self.choose_difficulty:
            buttons = (self.easy_button, self.medium_button, self.hard_button)
        else:
            buttons = (self.play_button, self.continue_button, self.daily_button)
        for b in buttons:
            b.bg_color = self.theme["button"]
            b.hover_color = self.theme["button_hover"]
            b.border_color = self.theme["grid"]
            b.text_color = self.theme["text"]

        if self.choose_difficulty:
            prompt = self.difficulty_font.render("CHOOSE DIFFICULTY", True, self.theme["text"])
            self.screen.blit(
                prompt,
                prompt.get_rect(center=(WIDTH // 2, 820 if PORTRAIT_MODE else 465 + self.desktop_y_offset))
            )
            self.easy_button.draw(self.screen)
            self.medium_button.draw(self.screen)
            self.hard_button.draw(self.screen)
            self.difficulty_back_button.bg_color = self.theme["button"]
            self.difficulty_back_button.hover_color = self.theme["button_hover"]
            self.difficulty_back_button.border_color = self.theme["grid"]
            self.difficulty_back_button.text_color = self.theme["text"]
            self.difficulty_back_button.draw(self.screen)
        elif self.choose_mode:
            prompt = self.difficulty_font.render("CHOOSE GAME MODE", True, self.theme["text"])
            self.screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 820 if PORTRAIT_MODE else 460 + self.desktop_y_offset)))
            subtitle_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 15)
            subtitle = subtitle_font.render(f"{self.selected_difficulty.title()} difficulty", True, self.theme["secondary"])
            self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 850 if PORTRAIT_MODE else 492 + self.desktop_y_offset)))
            mode_cards = (
                (self.classic_mode_button, "CLASSIC", "3 mistakes · full rewards"),
                (self.zen_mode_button, "ZEN", "No game over · relaxed pace"),
                (self.timed_mode_button, "TIMED", "10 minutes · bonus rewards"),
                (self.practice_mode_button, "PRACTICE", "Wrong answers are revealed"),
            )
            for button, _, _ in mode_cards:
                button.bg_color = self.theme["button"]
                button.hover_color = self.theme["button_hover"]
                button.border_color = {
                    self.classic_mode_button: self.theme["accent"],
                    self.zen_mode_button: (42, 190, 125),
                    self.timed_mode_button: (245, 130, 55),
                    self.practice_mode_button: (55, 150, 255),
                }[button]
                button.text_color = self.theme["text"]
                button.text = ""
                button.draw(self.screen)
            for button in (self.mode_back_button,):
                button.bg_color = self.theme["button"]
                button.hover_color = self.theme["button_hover"]
                button.border_color = self.theme["grid"]
                button.text_color = self.theme["text"]
                button.draw(self.screen)
            mode_title_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 19)
            mode_detail_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 11)
            for button, title, detail in mode_cards:
                color = button.border_color
                pygame.draw.circle(self.screen, color, (button.rect.x + 24, button.rect.centery), 7)
                title_surface = mode_title_font.render(title, True, color)
                detail_surface = mode_detail_font.render(detail, True, self.theme["secondary"])
                self.screen.blit(title_surface, title_surface.get_rect(center=(button.rect.centerx + 10, button.rect.centery - 11)))
                self.screen.blit(detail_surface, detail_surface.get_rect(center=(button.rect.centerx + 10, button.rect.centery + 14)))
        else:
            self.daily_button.text = ""
            self.play_button.draw(self.screen)
            self.continue_button.draw(self.screen)
            self._draw_daily_challenge_button()

            streak = self.game.stats.data.get("win_streak", 0)
            self._draw_streak_panel(streak)
            if getattr(self, "continue_message_until", 0) > pygame.time.get_ticks():
                message = self.credit_font.render("No game available to continue", True, self.theme["accent"])
                self.screen.blit(
                    message,
                message.get_rect(center=(WIDTH // 2, 1_220 if PORTRAIT_MODE else 820 + self.desktop_y_offset))
                )
            if getattr(self, "daily_message_until", 0) > pygame.time.get_ticks():
                message = self.credit_font.render("Today's Daily Challenge is already complete", True, self.theme["accent"])
                self.screen.blit(message, message.get_rect(center=(WIDTH // 2, 1_260 if PORTRAIT_MODE else 855)))
        # Compact icon-only information control placed close to the title.
        info_hover = self.tutorial_button.collidepoint(pygame.mouse.get_pos())
        info_center = self.tutorial_button.center
        info_size = 42 if info_hover else 38
        info_icon = pygame.transform.smoothscale(self.info_icon, (info_size, info_size))
        self.screen.blit(info_icon, info_icon.get_rect(center=info_center))
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

        rect = icon.get_rect(center=self.settings_button.center)

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
        # Store icon sits directly below Settings with matching interaction style.
        self.store_hover = self.store_button.collidepoint(mouse)
        store_size = 62 if not self.store_hover else 68
        store_icon = pygame.transform.smoothscale(self.store_icon, (store_size, store_size))
        store_rect = store_icon.get_rect(center=self.store_button.center)
        store_shadow = pygame.Surface((store_size + 10, store_size + 10), pygame.SRCALPHA)
        pygame.draw.circle(store_shadow, (0, 0, 0, 35), (store_shadow.get_width() // 2, store_shadow.get_height() // 2), store_size // 2)
        self.screen.blit(store_shadow, store_shadow.get_rect(center=(store_rect.centerx, store_rect.centery + 4)))
        self.screen.blit(store_icon, store_rect)
        # Achievement shortcut uses the same icon-only treatment as Store.
        self.achievements_hover = self.achievements_button.collidepoint(mouse)
        medal_size = 62 if not self.achievements_hover else 68
        medal_icon = pygame.transform.smoothscale(self.medal_icon, (medal_size, medal_size))
        medal_rect = medal_icon.get_rect(center=self.achievements_button.center)
        medal_shadow = pygame.Surface((medal_size + 10, medal_size + 10), pygame.SRCALPHA)
        pygame.draw.circle(medal_shadow, (0, 0, 0, 35), (medal_shadow.get_width() // 2, medal_shadow.get_height() // 2), medal_size // 2)
        self.screen.blit(medal_shadow, medal_shadow.get_rect(center=(medal_rect.centerx, medal_rect.centery + 4)))
        self.screen.blit(medal_icon, medal_rect)
        self.stats_icon_hover = self.stats_icon_button.collidepoint(mouse)
        stats_size = 62 if not self.stats_icon_hover else 68
        stats_icon = pygame.transform.smoothscale(self.stats_icon, (stats_size, stats_size))
        stats_rect = stats_icon.get_rect(center=self.stats_icon_button.center)
        stats_shadow = pygame.Surface((stats_size + 10, stats_size + 10), pygame.SRCALPHA)
        pygame.draw.circle(stats_shadow, (0, 0, 0, 35), (stats_shadow.get_width() // 2, stats_shadow.get_height() // 2), stats_size // 2)
        self.screen.blit(stats_shadow, stats_shadow.get_rect(center=(stats_rect.centerx, stats_rect.centery + 4)))
        self.screen.blit(stats_icon, stats_rect)

    def _draw_daily_challenge_button(self):
        """Featured Daily button with the same motion and glow as other controls."""
        rect = self.daily_button.rect
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        self.daily_hover_amount = min(1.0, self.daily_hover_amount + 0.15) if hovered else max(0.0, self.daily_hover_amount - 0.15)
        pressed = pygame.mouse.get_pressed()[0] and hovered
        lift = 1 if pressed else int(-3 * self.daily_hover_amount)
        draw_rect = rect.move(0, lift)
        shadow = draw_rect.move(0, 5 + int(self.daily_hover_amount * 2))
        # Daily is a featured mode, so it keeps its distinct orange outline.
        border = (255, 106, 61)

        if hovered:
            glow = pygame.Surface((draw_rect.width + 18, draw_rect.height + 18), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*border, 45), glow.get_rect(), border_radius=18)
            self.screen.blit(glow, (draw_rect.x - 9, draw_rect.y - 9))
        pygame.draw.rect(self.screen, border, shadow, border_radius=12)
        fill = tuple(
            int(self.theme["button"][i] + (self.theme["button_hover"][i] - self.theme["button"][i]) * self.daily_hover_amount)
            for i in range(3)
        )
        pygame.draw.rect(self.screen, fill, draw_rect, border_radius=12)
        pygame.draw.rect(self.screen, border, draw_rect, 2, border_radius=12)

        side_card = draw_rect.height > 100
        # Reposition with the card and draw it as a clearly separate calendar button.
        self.daily_calendar_button = (
            pygame.Rect(draw_rect.x + 20, draw_rect.bottom - 64, draw_rect.width - 40, 45)
            if side_card else pygame.Rect(draw_rect.x + 10, draw_rect.y + 8, 62, 59)
        )
        calendar_hover = self.daily_calendar_button.collidepoint(pygame.mouse.get_pos())
        self.daily_calendar_hover_amount = min(1.0, self.daily_calendar_hover_amount + 0.18) if calendar_hover else max(0.0, self.daily_calendar_hover_amount - 0.18)
        cal_rect = self.daily_calendar_button.move(0, -2 if calendar_hover else 0)
        if calendar_hover:
            glow = pygame.Surface((cal_rect.width + 12, cal_rect.height + 12), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*self.theme["accent"], 70), glow.get_rect(), border_radius=13)
            self.screen.blit(glow, (cal_rect.x - 6, cal_rect.y - 6))
        pygame.draw.rect(self.screen, self.theme["accent"], cal_rect.move(0, 3), border_radius=10)
        pygame.draw.rect(self.screen, self.theme["popup"], cal_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.theme["accent"], cal_rect, 2, border_radius=10)
        icon_box = pygame.Rect(
            cal_rect.x + (18 if side_card else 16),
            cal_rect.y + (8 if side_card else 7),
            28 if side_card else 30,
            28 if side_card else 30,
        )
        pygame.draw.rect(self.screen, self.theme["accent"], icon_box, border_radius=6)
        pygame.draw.rect(self.screen, self.theme["popup"], (icon_box.x + 4, icon_box.y + 9, 22, 17), border_radius=3)
        pygame.draw.line(self.screen, self.theme["popup"], (icon_box.x + 7, icon_box.y + 4), (icon_box.x + 7, icon_box.y + 12), 2)
        pygame.draw.line(self.screen, self.theme["popup"], (icon_box.right - 7, icon_box.y + 4), (icon_box.right - 7, icon_box.y + 12), 2)
        calendar_label = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 12 if side_card else 9).render(
            "VIEW CALENDAR" if side_card else "CALENDAR", True, self.theme["accent"]
        )
        calendar_pos = (cal_rect.centerx + 18, cal_rect.centery) if side_card else (cal_rect.centerx, cal_rect.bottom - 9)
        self.screen.blit(calendar_label, calendar_label.get_rect(center=calendar_pos))

        title_font = pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 20 if side_card else 21)
        subtitle_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 13)
        title = title_font.render("DAILY CHALLENGE", True, self.theme["text"])
        daily = self.game.stats.data.get("daily", {})
        if daily.get("last_completed") == datetime.now().date().isoformat():
            remaining = datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time()) - datetime.now()
            subtitle_text = f"Next puzzle in {remaining.seconds // 3600:02}:{(remaining.seconds // 60) % 60:02}:{remaining.seconds % 60:02}"
        else:
            subtitle_text = "A fresh puzzle awaits"
        subtitle = subtitle_font.render(subtitle_text, True, self.theme["secondary"])
        if side_card:
            self.screen.blit(title, title.get_rect(center=(draw_rect.centerx, draw_rect.y + 30)))
            self.screen.blit(subtitle, subtitle.get_rect(center=(draw_rect.centerx, draw_rect.y + 60)))
            play_today = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 14).render("PLAY TODAY", True, border)
            self.screen.blit(play_today, play_today.get_rect(center=(draw_rect.centerx, draw_rect.y + 96)))
        else:
            self.screen.blit(title, (draw_rect.x + 82, draw_rect.y + 14))
            self.screen.blit(subtitle, (draw_rect.x + 83, draw_rect.y + 43))
        arrow_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 24)
        arrow = arrow_font.render(">", True, self.theme["success"] if hovered else self.theme["accent"])
        if not side_card:
            self.screen.blit(arrow, arrow.get_rect(center=(draw_rect.right - 28, draw_rect.centery)))

    def _draw_desktop_title_bar(self):
        """Menu-level bar, drawn last so it can never be covered by the menu."""
        bar = pygame.Rect(0, 0, WIDTH, 44)
        pygame.draw.rect(self.screen, (28, 30, 38), bar)
        pygame.draw.line(self.screen, self.theme["accent"], (0, 43), (WIDTH, 43), 2)
        font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 17)
        title = font.render("SUDOKU WIZARD", True, self.theme["text"])
        self.screen.blit(title, (16, 12))
        controls = ((WIDTH - 132, "-"), (WIDTH - 88, "[]"), (WIDTH - 44, "X"))
        mouse = pygame.mouse.get_pos()
        for index, (x, label) in enumerate(controls):
            rect = pygame.Rect(x, 0, 44, 44)
            is_close = index == 2
            if rect.collidepoint(mouse):
                pygame.draw.rect(self.screen, (220, 70, 70) if is_close else self.theme["accent"], rect)
            symbol = font.render(label, True, (255, 255, 255))
            self.screen.blit(symbol, symbol.get_rect(center=rect.center))

    def _draw_streak_panel(self, streak):
        """Use one desktop side as a focused reward for the active win streak."""
        if PORTRAIT_MODE:
            # Keep both reward cards together down the left side, with a
            # clear gap before the central title begins.
            card = pygame.Rect(42, 270, 255, 150)
            fire_icon = self.streak_fire_large
            label_y = card.y + 30
            value_y = card.centery + 3
            unit_y = card.bottom - 25
        else:
            card = pygame.Rect(70, 405 + self.desktop_y_offset, 255, 190)
            fire_icon = self.streak_fire_large
            label_y = card.y + 34
            value_y = card.centery + 8
            unit_y = card.bottom - 30
        glow = pygame.Surface((card.width + 26, card.height + 26), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*self.theme["accent"], 38), glow.get_rect(), border_radius=28)
        self.screen.blit(glow, (card.x - 13, card.y - 13))
        pygame.draw.rect(self.screen, self.theme["shadow"], card.move(0, 8), border_radius=22)
        fill = pygame.Surface(card.size, pygame.SRCALPHA)
        pygame.draw.rect(fill, (*self.theme["popup"], 235), fill.get_rect(), border_radius=22)
        self.screen.blit(fill, card.topleft)
        pygame.draw.rect(self.screen, self.theme["accent"], card, 2, border_radius=22)
        icon_rect = fire_icon.get_rect(center=(card.x + 74, card.centery))
        self.screen.blit(fire_icon, icon_rect)
        label_surface = self.streak_label_font.render("CURRENT STREAK", True, self.theme["secondary"])
        self.screen.blit(label_surface, label_surface.get_rect(center=(card.centerx + 42, label_y)))
        value_surface = self.streak_value_font.render(str(streak), True, self.theme["accent"])
        self.screen.blit(value_surface, value_surface.get_rect(center=(card.centerx + 42, value_y)))
        unit = self.streak_label_font.render("WINS" if streak != 1 else "WIN", True, self.theme["text"])
        self.screen.blit(unit, unit.get_rect(center=(card.centerx + 42, unit_y)))
