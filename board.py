import pygame
import math
import time

from constants import *
import themes


class Board:

    def __init__(self, logic):

        self.logic = logic
        self.animations_enabled = True
        # Difficulty artwork is loaded and scaled only once.  Drawing the
        # cached surface each frame keeps it suitable for both desktop and
        # phone screens without adding per-frame image work.
        self.difficulty_backgrounds = {}
        self.difficulty_background_cache = {}
        self.daily_background_source = pygame.image.load("assets/images/dailybg.png").convert()
        self.daily_background_cache = {}
        self.difficulty_headers = {}
        for difficulty in ("easy", "medium", "hard"):
            artwork = pygame.image.load(
                f"assets/images/{difficulty}.png"
            ).convert()
            self.difficulty_backgrounds[difficulty] = artwork
            header = pygame.image.load(
                f"assets/images/{difficulty}_header.png"
            ).convert_alpha()
            header_width = WIDTH - 40 if PORTRAIT_MODE else 700
            header_height = int(header.get_height() * header_width / header.get_width())
            self.difficulty_headers[difficulty] = pygame.transform.smoothscale(
                header, (header_width, header_height)
            )
        daily_header = pygame.image.load("assets/images/daily.png").convert_alpha()
        daily_width = WIDTH - 40 if PORTRAIT_MODE else 700
        daily_height = int(daily_header.get_height() * daily_width / daily_header.get_width())
        self.daily_header = pygame.transform.smoothscale(daily_header, (daily_width, daily_height))

        # ---------- Icons ----------

        self.trophy = pygame.image.load(
            "assets/images/won.png"
        ).convert_alpha()
        self.win_result_source = pygame.image.load("assets/images/gamewon.png").convert()
        self.win_result_background = pygame.transform.smoothscale(
            self.win_result_source, (WIDTH, HEIGHT)
        )
        win_panel_size = (650, 1000) if PORTRAIT_MODE else (860, 790)
        self.win_panel_fade = pygame.transform.smoothscale(
            self.win_result_background, win_panel_size
        )
        self.win_panel_fade.set_alpha(32)
        self.win_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.win_overlay_color = None
        # Reuse result-card assets on phones instead of building alpha
        # surfaces and dimmed stars during every frame.
        self.win_popup_fill_cache = {}
        self.dim_star_icon = None
        self.sparkle_angle = 0

        self.timer_icon = pygame.image.load(
            "assets/images/timer.png"
        ).convert_alpha()

        self.mistake_icon = pygame.image.load(
            "assets/images/mistake.png"
        ).convert_alpha()

        self.target_icon = pygame.image.load(
            "assets/images/target.png"
        ).convert_alpha()
        self.accuracy_icon = pygame.image.load(
            "assets/images/accuracy.png"
        ).convert_alpha()

        self.score_icon = pygame.image.load(
            "assets/images/score.png"
        ).convert_alpha()

        self.star_icon = pygame.image.load(
            "assets/images/star.png"
        ).convert_alpha()

        self.exit_icon = pygame.image.load(
            "assets/images/exit.png"
        ).convert_alpha()
        self.score_icon = pygame.image.load(
            "assets/images/score.png"
        ).convert_alpha()


        trophy_size = 250 if PORTRAIT_MODE else 180
        self.trophy = pygame.transform.smoothscale(self.trophy, (trophy_size, trophy_size))

        self.timer_icon = pygame.transform.smoothscale(self.timer_icon, (40, 40))

        self.mistake_icon = pygame.transform.smoothscale(self.mistake_icon, (40, 40))

        self.target_icon = pygame.transform.smoothscale(self.target_icon, (40, 40))
        self.accuracy_icon = pygame.transform.smoothscale(
            self.accuracy_icon,
            (40, 40)
        )

        self.score_icon = pygame.transform.smoothscale(
            self.score_icon,
            (40, 40)
        )
        star_icon_size = 100 if PORTRAIT_MODE else 72
        self.star_icon = pygame.transform.smoothscale(self.star_icon, (star_icon_size, star_icon_size))

        self.exit_icon = pygame.transform.smoothscale(self.exit_icon, (30, 30))
        
        self.score_icon = pygame.transform.smoothscale(
            self.score_icon,
            (34, 34)
        )

        # ---------- Fonts ----------

        self.number_font = pygame.font.SysFont(
            "Arial",
            42,
            bold=True
        )
        self.note_font = pygame.font.SysFont(
            "Arial",
            15 if PORTRAIT_MODE else 18,
            bold=True
        )

        self.info_font = pygame.font.Font(
            "assets/fonts/Poppins-Regular.ttf",
            26
        )

        self.header_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            30
        )

        self.title_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            50
        )

        self.win_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            58
        )
        self.win_mobile_title_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf", 48
        )
        self.win_label_font = pygame.font.Font(
            "assets/fonts/Poppins-Regular.ttf", 28 if PORTRAIT_MODE else 22
        )
        self.win_value_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf", 30 if PORTRAIT_MODE else 25
        )

        self.popup_font = pygame.font.Font(
            "assets/fonts/Poppins-Regular.ttf",
            28
        )

        self.star_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            36
        )
        self.score_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            34
        )
        self.mobile_stat_label_font = pygame.font.Font(
            "assets/fonts/Poppins-Regular.ttf", 18
        )
        self.mobile_stat_value_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf", 25
        )
        # ---------- Smooth Selection Animation ----------
        self.highlight_x = BOARD_X
        self.highlight_y = BOARD_Y

        self.target_x = BOARD_X
        self.target_y = BOARD_Y
        self.pulse_time = 0
        self.display_score = 0

    def select(self, mouse_pos):

        x, y = mouse_pos

        if (BOARD_X <= x < BOARD_X + CELL_SIZE * 9 and
                BOARD_Y <= y < BOARD_Y + CELL_SIZE * 9):

            col = (x - BOARD_X) // CELL_SIZE
            row = (y - BOARD_Y) // CELL_SIZE

            self.logic.select(row, col)
    def draw_background(self, screen, theme):
        # Daily Challenge has its own artwork, separate from the Medium board.
        if getattr(self.logic, "daily_challenge", False):
            screen_size = screen.get_size()
            if screen_size not in self.daily_background_cache:
                self.daily_background_cache[screen_size] = pygame.transform.smoothscale(
                    self.daily_background_source, screen_size
                )
            screen.blit(self.daily_background_cache[screen_size], (0, 0))
        else:
            difficulty = str(getattr(self.logic, "difficulty", "easy")).lower()
            artwork = self.difficulty_backgrounds.get(difficulty)
            if artwork:
                screen_size = screen.get_size()
                cache_key = (difficulty, screen_size)
                if cache_key not in self.difficulty_background_cache:
                    self.difficulty_background_cache[cache_key] = pygame.transform.smoothscale(artwork, screen_size)
                screen.blit(self.difficulty_background_cache[cache_key], (0, 0))
            else:
                screen.fill(theme["background"])
        background = theme["background"]
        board = theme["board"]
        grid = theme["grid"]
        shadow = theme["shadow"]
        text = theme["text"]
        secondary = theme["secondary"]
        popup = theme["popup"]
        popup_border = theme["popup_border"]
        # ---------- Shadow ----------
        shadow_rect = pygame.Rect(
            BOARD_X - 7,
            BOARD_Y - 7,
            CELL_SIZE * 9 + 24,
            CELL_SIZE * 9 + 24
        )

        pygame.draw.rect(
            screen,
            shadow,
            shadow_rect,
            border_radius=14
        )

        # ---------- Board Card ----------
        board_rect = pygame.Rect(
            BOARD_X - 12,
            BOARD_Y - 12,
            CELL_SIZE * 9 + 24,
            CELL_SIZE * 9 + 24
        )

        pygame.draw.rect(
            screen,
            board,
            board_rect,
            border_radius=28
        )

        pygame.draw.rect(
            screen,
            grid,
            board_rect,
            3,
            border_radius=28
        )

    def _draw_stat_card(self, screen, theme, rect, icon, label, value, value_color=None):
        """Draw a compact, consistent information card without text overflow."""
        shadow = rect.copy()
        shadow.y += 4
        pygame.draw.rect(screen, theme["shadow"], shadow, border_radius=18)
        pygame.draw.rect(screen, theme["board"], rect, border_radius=18)
        pygame.draw.rect(screen, theme["grid"], rect, 2, border_radius=18)
        pygame.draw.rect(
            screen, theme["accent"],
            pygame.Rect(rect.x + 18, rect.y + 10, rect.width - 36, 5),
            border_radius=3
        )

        if icon is not None:
            icon_center = (rect.x + 35, rect.y + 43)
            screen.blit(icon, icon.get_rect(center=icon_center))
            text_x = rect.x + 70
        else:
            text_x = rect.x + 18

        compact = rect.height < 100
        label_font = self.mobile_stat_label_font if PORTRAIT_MODE else self.info_font
        value_font = self.mobile_stat_value_font if PORTRAIT_MODE else self.score_font
        label_surface = label_font.render(label, True, theme["secondary"])
        screen.blit(label_surface, (text_x, rect.y + (17 if compact else 26)))
        value_surface = value_font.render(
            str(value), True, value_color or theme["text"]
        )
        value_rect = value_surface.get_rect(
            center=(rect.centerx, rect.y + (61 if compact else 79))
        )
        screen.blit(value_surface, value_rect)

    def draw_ui(self, screen, theme):
        elapsed = self.logic.get_elapsed_time()
        minutes, seconds = elapsed // 60, elapsed % 60
        game_mode = getattr(self.logic, "game_mode", "classic")
        if game_mode == "timed":
            remaining = max(0, getattr(self.logic, "time_limit", 600) - elapsed)
            time_label = "TIME LEFT"
            time_value = f"{remaining // 60:02}:{remaining % 60:02}"
        else:
            time_label = "TIME"
            time_value = f"{minutes:02}:{seconds:02}"
        mistake_value = (
            str(self.logic.mistakes)
            if game_mode in ("zen", "practice")
            else f"{self.logic.mistakes} / 3"
        )

        card_w, card_h = 220, 110
        difficulty = str(getattr(self.logic, "difficulty", "easy")).lower()
        is_daily = getattr(self.logic, "daily_challenge", False)
        header_art = self.daily_header if is_daily else self.difficulty_headers.get(difficulty)
        if PORTRAIT_MODE:
            header_rect = (header_art.get_rect(center=(WIDTH // 2, 28 + header_art.get_height() // 2))
                           if header_art else pygame.Rect(WIDTH // 2 - 220, 28, 440, 68))
            # Compact horizontal cards free vertical space for the board.
            card_w, card_h = 210, 90
            card_gap = 15
            cards_x = (WIDTH - (card_w * 3 + card_gap * 2)) // 2
            cards_y = header_rect.bottom + 15
            score_card = pygame.Rect(cards_x, cards_y, card_w, card_h)
            time_card = pygame.Rect(cards_x + card_w + card_gap, cards_y, card_w, card_h)
            mistakes_card = pygame.Rect(cards_x + (card_w + card_gap) * 2, cards_y, card_w, card_h)
        else:
            header_rect = (header_art.get_rect(center=(WIDTH // 2, 75 + header_art.get_height() // 2))
                           if header_art else pygame.Rect(WIDTH // 2 - 220, 50, 440, 60))
            card_h = 100
            score_card = pygame.Rect(BOARD_X + CELL_SIZE * 9 + 30, BOARD_Y + 20, card_w, card_h)
            time_card = pygame.Rect(score_card.x, score_card.bottom + 8, card_w, card_h)
            mistakes_card = pygame.Rect(score_card.x, time_card.bottom + 8, card_w, card_h)

        # Each mode supplies its own header artwork, replacing the text card.
        if header_art:
            screen.blit(header_art, header_rect)
        if game_mode != "classic":
            badge_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 13 if PORTRAIT_MODE else 14)
            badge = badge_font.render(game_mode.upper(), True, theme["accent"])
            badge_box = badge.get_rect(topright=(header_rect.right - 15, header_rect.y + 12))
            screen.blit(badge, badge_box)

        if abs(self.logic.score - self.display_score) < 1:
            self.display_score = self.logic.score
        else:
            self.display_score += (self.logic.score - self.display_score) * 0.15
        if self.logic.score == 0:
            self.display_score = 0

        score_color = (130, 60, 210)
        score_elapsed = time.time() - self.logic.score_pop_time
        if score_elapsed < 0.20:
            if self.logic.score_pop_type == "up":
                score_color = (35, 185, 70)
            elif self.logic.score_pop_type == "down":
                score_color = (220, 45, 45)

        self._draw_stat_card(
            screen, theme, score_card, self.score_icon, "SCORE",
            f"{int(self.display_score):,}", score_color
        )
        self._draw_stat_card(
            screen, theme, time_card, self.timer_icon, time_label,
            time_value, theme["accent"] if game_mode == "timed" else theme["text"]
        )
        self._draw_stat_card(
            screen, theme, mistakes_card, self.mistake_icon, "MISTAKES",
            mistake_value, (220, 45, 45) if self.logic.mistakes else theme["text"]
        )

        # Restore the short, fading score-change indicator above the score
        # card.  It stays separate from the card text, so values never clash.
        if self.logic.score_popup_text:
            popup_elapsed = time.time() - self.logic.score_popup_time
            if popup_elapsed < 1:
                self.logic.score_popup_y -= 1
                popup_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 32)
                popup = popup_font.render(
                    self.logic.score_popup_text, True, self.logic.score_popup_color
                )
                popup.set_alpha(int(255 * (1 - popup_elapsed)))
                popup_rect = popup.get_rect(
                    center=(score_card.centerx, score_card.y - 18 + self.logic.score_popup_y)
                )
                screen.blit(popup, popup_rect)
            else:
                self.logic.score_popup_text = None


    def draw_highlights(self, screen, theme):
        if self.logic.hover:
            hover_row, hover_col = self.logic.hover

            if self.logic.selected != (hover_row, hover_col):
                hover_rect = pygame.Rect(
                    BOARD_X + hover_col * CELL_SIZE + 3,
                    BOARD_Y + hover_row * CELL_SIZE + 3,
                    CELL_SIZE - 6,
                    CELL_SIZE - 6
                )

                pygame.draw.rect(
                    screen,
                    theme["highlight"],
                    hover_rect,
                    border_radius=10
                )

                pygame.draw.rect(
                    screen,
                    theme["highlight"],
                    hover_rect,
                    2,
                    border_radius=10
                )
               

                
        # If nothing is selected and no number is highlighted,
        # there is nothing to draw.
        if self.logic.selected is None and self.logic.highlight_number is None:
            return

        # Only get row/col if a cell is actually selected
        if self.logic.selected is not None:
            row, col = self.logic.selected
        if self.logic.selected is not None:

            # ---------- Smooth Selection Animation ----------
            self.target_x = BOARD_X + col * CELL_SIZE
            self.target_y = BOARD_Y + row * CELL_SIZE

            speed = 0.25

            self.highlight_x += (self.target_x - self.highlight_x) * speed
            self.highlight_y += (self.target_y - self.highlight_y) * speed

            # -------------------------
            # Highlight 3×3 Box
            # -------------------------

            box_row = (row // 3) * 3
            box_col = (col // 3) * 3

            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    pygame.draw.rect(
                        screen,
                        theme["box_highlight"],
                        pygame.Rect(
                            BOARD_X + c*CELL_SIZE + 3,
                            BOARD_Y + r*CELL_SIZE + 3,
                            CELL_SIZE - 6,
                            CELL_SIZE - 6
                            ),
                            border_radius=10
                        )

            # -------------------------
            # Highlight Row
            # -------------------------

            for c in range(9):
                pygame.draw.rect(
                    screen,
                    theme["row_highlight"],
                    pygame.Rect(
                        BOARD_X + c * CELL_SIZE + 3,
                        BOARD_Y + row * CELL_SIZE + 3,
                        CELL_SIZE - 6,
                        CELL_SIZE - 6
                    ),
                    border_radius=8
                )

            # -------------------------
            # Highlight Column
            # -------------------------

            for r in range(9):
                pygame.draw.rect(
                    screen,
                    theme["column_highlight"],
                    pygame.Rect(
                        BOARD_X + col * CELL_SIZE + 3,
                        BOARD_Y + r * CELL_SIZE + 3,
                        CELL_SIZE - 6,
                        CELL_SIZE - 6
                    ),
                    border_radius=8
                )
            # -------------------------
            # Selected Cell
            # -------------------------

            cell_rect = pygame.Rect(
                int(self.highlight_x) + 3,
                int(self.highlight_y) + 3,
                CELL_SIZE - 6,
                CELL_SIZE - 6
            )

            # ---------- Soft Glow ----------
            glow = pygame.Surface(
                (CELL_SIZE + 20, CELL_SIZE + 20),
                pygame.SRCALPHA
            )

            # pulsing value for glow and border
            pulse = (math.sin(time.time() * 4) + 1) / 2

            alpha = int(25 + pulse * 30)

            pygame.draw.circle(
                glow,
                (
                    *theme["selected_glow"],
                    alpha
                ),
                (
                    (CELL_SIZE + 20) // 2,
                    (CELL_SIZE + 20) // 2
                ),
                CELL_SIZE // 2 + 8
            )

            screen.blit(
                glow,
                (
                    int(self.highlight_x) - 10,
                    int(self.highlight_y) - 10
                )
            )

            # ---------- Fill ----------
            pygame.draw.rect(
                screen,
                theme["selected_fill"],
                cell_rect,
                border_radius=12
            )

            # ---------- White Inner Border ----------
            pygame.draw.rect(
                screen,
                theme["selected_border"],
                cell_rect,
                2,
                border_radius=12
            )

            # ---------- Blue Border ----------
            border_width = int(3 + pulse * 2)

            gold = theme["selected_outline"]

            pygame.draw.rect(
                screen,
                gold,
                cell_rect,
                border_width,
                border_radius=12
            )
        elapsed = time.time() - self.logic.flash_start

        if self.logic.highlight_number is not None:
            for r in range(9):
                for c in range(9):
                    if self.logic.grid[r][c] == self.logic.highlight_number:
                        pygame.draw.rect(
                            screen,
                            theme["same_number"],
                            pygame.Rect(
                                BOARD_X + c * CELL_SIZE + 3,
                                BOARD_Y + r * CELL_SIZE + 3,
                                CELL_SIZE - 6,
                                CELL_SIZE - 6
                            ),
                            border_radius=8
                        )

            
        if elapsed < self.logic.flash_duration:

            alpha = 1 - (elapsed / self.logic.flash_duration)

            flash = (
                40,
                90,
                255,
                int(140 * alpha)
            )

            overlay = pygame.Surface(
                (CELL_SIZE, CELL_SIZE),
                pygame.SRCALPHA
            )

            overlay.fill(flash)

            # ---------- Flash Row ----------
            if self.logic.flash_row is not None:

                r = self.logic.flash_row

                for c in range(9):

                    screen.blit(
                        overlay,
                        (
                            BOARD_X + c * CELL_SIZE,
                            BOARD_Y + r * CELL_SIZE
                        )
                    )

            # ---------- Flash Column ----------
            if self.logic.flash_col is not None:

                c = self.logic.flash_col

                for r in range(9):

                    screen.blit(
                        overlay,
                        (
                            BOARD_X + c * CELL_SIZE,
                            BOARD_Y + r * CELL_SIZE
                        )
                    )

            # ---------- Flash Box ----------
            if self.logic.flash_box is not None:

                box_r, box_c = self.logic.flash_box

                for r in range(box_r, box_r + 3):
                    for c in range(box_c, box_c + 3):

                        screen.blit(
                            overlay,
                            (
                                BOARD_X + c * CELL_SIZE,
                                BOARD_Y + r * CELL_SIZE
                            )
                        )

        else:

            self.logic.flash_row = None
            self.logic.flash_col = None
            self.logic.flash_box = None


    def draw_numbers(self, screen, theme):
        is_dark_theme = sum(theme["background"]) < 200
        for row in range(9):
            for col in range(9):
                value = self.logic.grid[row][col]
                if value == 0:
                    # Candidate notes are arranged as a mini 3x3 keypad.
                    for note in self.logic.notes[row][col]:
                        note_row, note_col = divmod(note - 1, 3)
                        note_text = self.note_font.render(str(note), True, theme["accent"])
                        note_x = BOARD_X + col * CELL_SIZE + (note_col + 0.5) * CELL_SIZE / 3
                        note_y = BOARD_Y + row * CELL_SIZE + (note_row + 0.5) * CELL_SIZE / 3
                        screen.blit(note_text, note_text.get_rect(center=(note_x, note_y)))
                    continue

                if self.logic.fixed[row][col]:
                    color = theme["text"]
                elif value != self.logic.solution[row][col]:
                    color = (215, 40, 40)
                elif self.logic.selected == (row, col):
                    if is_dark_theme:
                        color = (160, 210, 255)
                    else:
                        color = (25, 70, 220)
                else:
                    if is_dark_theme:
                        color = (130, 185, 255)
                    else:
                        color = (55, 95, 235)
                
                text = self.number_font.render(str(value), True, color)

                # -------- Pop Animation --------
                if self.logic.pop_cell == (row, col):
                    elapsed = time.time() - self.logic.pop_time

                    if elapsed < 0.18:
                        progress = elapsed / 0.18

                        # Smooth ease-out animation
                        scale = 1 + (1.6 - 1) * ((1 - progress) ** 2)

                        new_size = (
                            int(text.get_width() * scale),
                            int(text.get_height() * scale)
                        )
                        glow = pygame.Surface(
                            (CELL_SIZE, CELL_SIZE),
                            pygame.SRCALPHA
                        )

                        alpha = int(60 * (1 - progress))

                        pygame.draw.circle(
                            glow,
                            (70, 120, 255, alpha),
                            (CELL_SIZE // 2, CELL_SIZE // 2),
                            int(18 * scale)
                        )

                        screen.blit(
                            glow,
                            (
                                BOARD_X + col * CELL_SIZE,
                                BOARD_Y + row * CELL_SIZE
                            )
                        )

                        text = pygame.transform.smoothscale(text, new_size)

                rect = text.get_rect(
                    center=(
                        BOARD_X + col * CELL_SIZE + CELL_SIZE // 2,
                        BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2
                    )
                )

                # ---------- Soft Shadow ----------
                shadow = self.number_font.render(
                    str(value),
                    True,
                    theme["shadow"]
                )

                shadow_rect = shadow.get_rect(
                    center=(
                        rect.centerx + 1,
                        rect.centery + 2
                    )
                )

                screen.blit(shadow, shadow_rect)

                # ---------- Main Number ----------
                screen.blit(text, rect)
        
        if self.logic.invalid_cell:
            if time.time() - self.logic.invalid_time < 0.5:
                row, col = self.logic.invalid_cell
                self.target_x = BOARD_X + col * CELL_SIZE
                self.target_y = BOARD_Y + row * CELL_SIZE

                speed = 0.22

                self.highlight_x += (self.target_x - self.highlight_x) * speed
                self.highlight_y += (self.target_y - self.highlight_y) * speed
                if self.logic.grid[row][col] == 0:
                    x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
                    y = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2

                    # Shake animation
                    elapsed = time.time() - self.logic.invalid_time

                    if elapsed < 0.20:
                        shake = 4 if int(elapsed * 40) % 2 == 0 else -4
                        x += shake

                    text = self.number_font.render(
                        str(self.logic.invalid_number),
                        True,
                        RED
                    )

                    rect = text.get_rect(center=(x, y))
                    screen.blit(text, rect)
            else:
                self.logic.invalid_cell = None

    def draw_grid(self, screen, theme):
        
        # ---------- Thin Lines ----------
        for i in range(10):
            if i % 3 != 0:
                pygame.draw.line(
                    screen,
                    theme["secondary"],
                    (BOARD_X + i * CELL_SIZE, BOARD_Y),
                    (BOARD_X + i * CELL_SIZE, BOARD_Y + 9 * CELL_SIZE),
                    2
                )

                pygame.draw.line(
                    screen,
                    theme["secondary"],
                    (BOARD_X, BOARD_Y + i * CELL_SIZE),
                    (BOARD_X + 9 * CELL_SIZE, BOARD_Y + i * CELL_SIZE),
                    2
                )

        # ---------- Thick Lines ----------
        for i in range(0, 10, 3):
            pygame.draw.line(
                screen,
                theme["grid"],
                (BOARD_X + i * CELL_SIZE, BOARD_Y),
                (BOARD_X + i * CELL_SIZE, BOARD_Y + 9 * CELL_SIZE),
                4
            )

            pygame.draw.line(
                screen,
                theme["grid"],
                (BOARD_X, BOARD_Y + i * CELL_SIZE),
                (BOARD_X + 9 * CELL_SIZE, BOARD_Y + i * CELL_SIZE),
                4
            )

    def draw_win(self, screen, theme):
        if not self.logic.game_won:
            return

        if PORTRAIT_MODE:
            # Skipping the large zoom animation removes a major source of
            # stutter on Pydroid while preserving the finished result design.
            self.logic.popup_scale = 1.0
        elif self.logic.popup_scale < 1:
            self.logic.popup_scale += (1 - self.logic.popup_scale) * 0.14

        scale = min(self.logic.popup_scale, 1)

        if self.win_result_background.get_size() != screen.get_size():
            self.win_result_background = pygame.transform.smoothscale(
                self.win_result_source, screen.get_size()
            )
        screen.blit(self.win_result_background, (0, 0))
        overlay_color = (*theme["overlay"], 100)
        if self.win_overlay_color != overlay_color:
            self.win_overlay.fill(overlay_color)
            self.win_overlay_color = overlay_color
        screen.blit(self.win_overlay, (0, 0))


        popup_width = int((650 if PORTRAIT_MODE else 860) * scale)
        popup_height = int((1000 if PORTRAIT_MODE else 790) * scale)

        popup = pygame.Rect(
            WIDTH//2 - popup_width//2,
            HEIGHT//2 - popup_height//2,
            popup_width,
            popup_height
        )


        fill_key = (popup.size, theme["popup"])
        popup_fill = self.win_popup_fill_cache.get(fill_key)
        if popup_fill is None:
            popup_fill = pygame.Surface(popup.size, pygame.SRCALPHA)
            pygame.draw.rect(
                popup_fill,
                (*theme["popup"], 191),  # 75% opacity
                popup_fill.get_rect(),
                border_radius=30
            )
            self.win_popup_fill_cache[fill_key] = popup_fill
        screen.blit(popup_fill, popup.topleft)

        pygame.draw.rect(
            screen,
            theme["popup_border"],
            popup,
            3,
            border_radius=30
        )



        if scale < 0.95:
            return

        # A restrained copy of the victory scene inside the card adds depth
        # while the opaque text and stats remain easy to read.
        screen.blit(
            self.win_panel_fade,
            self.win_panel_fade.get_rect(center=popup.center)
        )


        # ---------------- TROPHY ----------------

        trophy_x = WIDTH//2 - self.trophy.get_width()//2
        trophy_y = popup.y + (1 if PORTRAIT_MODE else 5)
        screen.blit(
            self.trophy,
            (trophy_x, trophy_y)
        )


        # ---------------- TITLE ----------------

        win_title_font = self.win_mobile_title_font if PORTRAIT_MODE else self.win_font
        title = win_title_font.render(
            "CONGRATULATIONS!",
            True,
            theme["success"]
        )

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH//2, popup.y + (300 if PORTRAIT_MODE else 225))
            )
        )


        # ---------------- STARS ----------------

        count = self.logic.stars


        star_size = 100 if PORTRAIT_MODE else 72
        spacing = 100 if PORTRAIT_MODE else 82

        total_width = spacing * 4 + star_size
        start_x = WIDTH//2 - total_width//2

        star_y = popup.y + (340 if PORTRAIT_MODE else 270)


        for i in range(5):
            pulse = 1 + 0.08 * math.sin(time.time() * 4 + i * 0.5) if (self.animations_enabled and not PORTRAIT_MODE) else 1

            size = int(star_size * pulse)

            star = self.star_icon if size == star_size else pygame.transform.smoothscale(self.star_icon, (size, size))

            if i >= count:
                if self.dim_star_icon is None:
                    self.dim_star_icon = self.star_icon.copy()
                    self.dim_star_icon.fill(
                        (120,120,120,180),
                        special_flags=pygame.BLEND_RGBA_MULT
                    )
                star = self.dim_star_icon if size == star_size else pygame.transform.smoothscale(self.dim_star_icon, (size, size))

            x = start_x + i*spacing + (star_size-size)//2
            y = star_y + (star_size-size)//2

            screen.blit(
                star,
                (x,y)
            )

        # ---------------- STATS CARD ----------------

        stats_card = pygame.Rect(
            popup.x + (80 if PORTRAIT_MODE else 70),
            popup.y + (420 if PORTRAIT_MODE else 360),
            popup.width - (160 if PORTRAIT_MODE else 140),
            300 if PORTRAIT_MODE else 250
        )

        pygame.draw.rect(
            screen,
            theme["board"],
            stats_card,
            border_radius=25
        )

        pygame.draw.rect(
            screen,
            theme["grid"],
            stats_card,
            3,
            border_radius=25
        )


        if self.logic.game_won:
            elapsed = int(
                self.logic.end_time -
                self.logic.start_time
            )
        else:
            elapsed = int(
                time.time() -
                self.logic.start_time
            )

        minutes = elapsed//60
        seconds = elapsed%60

        stats = [
            (self.timer_icon, "TIME", f"{minutes:02}:{seconds:02}"),
            (self.mistake_icon, "MISTAKES", str(self.logic.mistakes)),
            (self.target_icon, "DIFFICULTY", self.logic.difficulty.title()),
            (self.accuracy_icon, "MODE", getattr(self.logic, "game_mode", "classic").upper()),
            (self.score_icon, "SCORE", f"{self.logic.score:,}")
        ]
        

        label_font = self.win_label_font
        value_font = self.win_value_font
        y = stats_card.y + (35 if PORTRAIT_MODE else 27)

        for icon,label,value in stats:
            if icon:
                screen.blit(
                    icon,
                    (
                        stats_card.x + (25 if PORTRAIT_MODE else 22),
                        y - 4
                    )
                )

            l = label_font.render(
                label,
                True,
                theme["secondary"]
            )

            # ---------- Value Colors ----------
            if label == "TIME":
                value_color = (40, 110, 255)      # Blue
            elif label == "MISTAKES":
                value_color = (225, 50, 50)       # Red
            elif label == "DIFFICULTY":
                value_color = theme["text"]        # Black
            elif label == "MODE":
                value_color = theme["accent"]
            elif label == "SCORE":
                value_color = (145, 70, 255)      # Purple
            else:
                value_color = TEXT

            v = value_font.render(
                value,
                True,
                value_color
            )
            screen.blit(
                l,
                (
                    stats_card.x + (75 if PORTRAIT_MODE else 68),
                    y
                )
            )

            screen.blit(
                v,
                v.get_rect(
                    midright=(
                        stats_card.right - (45 if PORTRAIT_MODE else 35),
                        y + (18 if PORTRAIT_MODE else 14)
                    )
                )
            )

            y += 52 if PORTRAIT_MODE else 43

        rewards = getattr(self.logic, "result_rewards", None)
        if rewards:
            pieces = [
                f"+{rewards.get('coins', 0)} COINS",
                f"+{rewards.get('xp', 0)} XP",
                f"{rewards.get('stars', 0)} STARS",
            ]
            if rewards.get("hints", 0):
                pieces.append(f"+{rewards['hints']} HINT")
            if rewards.get("auto_notes", 0):
                pieces.append(f"+{rewards['auto_notes']} AUTO")
            reward_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 16 if PORTRAIT_MODE else 18)
            reward = reward_font.render("  •  ".join(pieces), True, theme["accent"])
            screen.blit(reward, reward.get_rect(center=(popup.centerx, stats_card.bottom + 28)))


        
        
    
    def draw_cell_backgrounds(self, screen, theme):
        # ---------- 3x3 Region Backgrounds ----------
        for box_row in range(3):
            for box_col in range(3):

                region = pygame.Rect(
                    BOARD_X + box_col * CELL_SIZE * 3 + 3,
                    BOARD_Y + box_row * CELL_SIZE * 3 + 3,
                    CELL_SIZE * 3 - 6,
                    CELL_SIZE * 3 - 6
                )

                if sum(theme["background"]) < 200:
                    color = (
                        (48,52,62)
                        if (box_row + box_col) % 2 == 0
                        else
                        (58,62,72)
                    )
                else:
                    color = (
                        theme["board"]
                        if (box_row + box_col) % 2 == 0
                        else
                        (255,255,255)
                    )

                pygame.draw.rect(
                    screen,
                    color,
                    region,
                    border_radius=12
                )

    def draw(self, screen, theme):
        # The win screen covers the game completely, so avoid drawing the
        # entire board behind it every frame on phones.
        if self.logic.game_won:
            self.draw_win(screen, theme)
            return

        self.draw_background(screen, theme)
        self.draw_ui(screen, theme)
        self.draw_cell_backgrounds(screen, theme)
        self.draw_grid(screen, theme)          # <-- moved here
        self.draw_highlights(screen, theme)
        self.draw_numbers(screen, theme)
        self.draw_win(screen, theme)
