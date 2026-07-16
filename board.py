import pygame
import math
import time

from constants import *
import themes


class Board:

    def __init__(self, logic):

        self.logic = logic
        # ---------- Icons ----------

        self.trophy = pygame.image.load(
            "assets/images/trophy.png"
        ).convert_alpha()
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
        self.new_icon = pygame.image.load(
            "assets/images/new_game.png"
        ).convert_alpha()
        self.score_icon = pygame.image.load(
            "assets/images/score.png"
        ).convert_alpha()


        self.trophy = pygame.transform.smoothscale(self.trophy, (250, 250))

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
        self.star_icon = pygame.transform.smoothscale(self.star_icon, (100, 100))     

        self.exit_icon = pygame.transform.smoothscale(self.exit_icon, (30, 30))
        
        self.new_icon = pygame.transform.smoothscale(self.new_icon,(30, 30))

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
            68
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

        screen.fill(theme["background"])
        background = theme["background"]
        board = theme["board"]
        grid = theme["grid"]
        shadow = theme["shadow"]
        text = theme["text"]
        secondary = theme["secondary"]
        popup = theme["popup"]
        popup_border = theme["popup_border"]
        # ---------- Header Background ----------
        pygame.draw.rect(
            screen,
            (115,95,190),      # light blue-grey
            (0, 0, WIDTH, HEADER_HEIGHT)
        )

        pygame.draw.line(
            screen,
            (180, 185, 195),
            (0, HEADER_HEIGHT),
            (WIDTH, HEADER_HEIGHT),
            2
        )

        
        header_rect = pygame.Rect(
            15,
            15,
            WIDTH - 30,
            HEADER_HEIGHT - 15
        )      
        pygame.draw.line(
            screen,
            (212, 218, 228),
            (0, HEADER_HEIGHT),
            (WIDTH, HEADER_HEIGHT),
            2
        )
        
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

    def draw_ui(self, screen, theme):

        # Header
        # ---------- Header Stat Cards ----------

        card_w = 360
        card_h = 72
        card_y = 80

        left_card = pygame.Rect(30, card_y, card_w, card_h)

        center_card = pygame.Rect(
            WIDTH // 2 - card_w // 2,
            card_y,
            card_w,
            card_h
        )

        right_card = pygame.Rect(
            WIDTH - card_w - 30,
            card_y,
            card_w,
            card_h
        )

        for card in (left_card, center_card, right_card):

            shadow = card.copy()
            shadow.y += 3

            pygame.draw.rect(
                screen,
                theme["shadow"],
                shadow,
                border_radius=18
            )

            pygame.draw.rect(
                screen,
                theme["board"],
                card,
                border_radius=18
            )

            pygame.draw.rect(
                screen,
                theme["grid"],
                card,
                2,
                border_radius=18
            )

        elapsed = self.logic.get_elapsed_time()
        
        minutes = elapsed // 60
        seconds = elapsed % 60

        # ---------- Left ----------
        difficulty = self.header_font.render(
            f"DIFFICULTY : {self.logic.difficulty}",
            True,
            theme["text"]
        )

        screen.blit(
            difficulty,
            (
            left_card.centerx - difficulty.get_width()//2,
            left_card.centery - difficulty.get_height()//2
            )
        )

        # ---------- Centre ----------
        timer = self.header_font.render(
            f"TIME : {minutes:02}:{seconds:02}",
            True,
            theme["text"]
        )

        

        screen.blit(
            timer,
            timer.get_rect(center=center_card.center)
            )

        # ---------- Right ----------
        mistakes = self.header_font.render(
            f"MISTAKES : {self.logic.mistakes}",
            True,
            theme["text"]
        )

        

        screen.blit(
            mistakes,
            mistakes.get_rect(center=right_card.center)
        )
        
        score_card = pygame.Rect(
            BOARD_X + CELL_SIZE * 9 + 30,
            BOARD_Y + 20,
            220,
            110
        )

        shadow = score_card.copy()
        shadow.y += 4

        pygame.draw.rect(
            screen,
            theme["shadow"],
            shadow,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            theme["board"],
            score_card,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            theme["grid"],
            score_card,
            2,
            border_radius=18
        )
        screen.blit(
            self.score_icon,
            (score_card.x + 15,
             score_card.y + 13)
        )
        label = self.info_font.render(
            "SCORE",
            True,
            theme["secondary"]
        )

        screen.blit(
            label,
            (score_card.x + 58,
             score_card.y + 15)
        )
        if abs(self.logic.score - self.display_score) < 1:
            self.display_score = self.logic.score
        else:
            self.display_score += (
                self.logic.score - self.display_score
            ) * 0.15
        if self.logic.score == 0:
            self.display_score = 0

        # ---------- Score Pop Animation ----------
        elapsed = time.time() - self.logic.score_pop_time

        score_color = (130, 60, 210)      # Default purple
        scale = 1.0

        if elapsed < 0.20:

            progress = elapsed / 0.20

            # Same easing as Sudoku number pop
            scale = 1 + (1.6 - 1) * ((1 - progress) ** 2)

            if self.logic.score_pop_type == "up":
                score_color = (35, 185, 70)

            elif self.logic.score_pop_type == "down":
                score_color = (220, 45, 45)

        score = self.score_font.render(
            f"{int(self.display_score):,}",
            True,
            score_color
        )

        if scale != 1.0:

            new_size = (
                int(score.get_width() * scale),
                int(score.get_height() * scale)
            )

            score = pygame.transform.smoothscale(
                score,
                new_size
            )

        score_rect = score.get_rect(
            center=(
                score_card.centerx,
                score_card.y + 70
            )
        )

        screen.blit(score, score_rect)
        # ---------- Floating Score Popup ----------

        if self.logic.score_popup_text:

            elapsed = time.time() - self.logic.score_popup_time

            if elapsed < 1:

                self.logic.score_popup_y -= 1

                popup_font = pygame.font.Font(
                    "assets/fonts/Poppins-Bold.ttf",
                    32
                )

                popup = popup_font.render(
                    self.logic.score_popup_text,
                    True,
                    self.logic.score_popup_color
                )

                popup.set_alpha(
                    int(255 * (1 - elapsed))
                )

                popup_rect = popup.get_rect(
                    center=(
                        score_card.centerx,
                        score_card.y - 20 + self.logic.score_popup_y
                    )
                )

                screen.blit(
                    popup,
                    popup_rect
                )

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
               

                
        if not self.logic.selected:
            return

        row, col = self.logic.selected
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
        for row in range(9):
            for col in range(9):
                value = self.logic.grid[row][col]
                if value == 0:
                    continue

                if self.logic.fixed[row][col]:
                    color = theme["text"]
                elif value != self.logic.solution[row][col]:
                    color = (215, 40, 40)
                elif self.logic.selected == (row, col):
                    if theme == themes.DARK:
                        color = (160, 210, 255)
                    else:
                        color = (25, 70, 220)
                else:
                    if theme == themes.DARK:
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

        if self.logic.popup_scale < 1:
            self.logic.popup_scale += (1 - self.logic.popup_scale) * 0.14

        scale = min(self.logic.popup_scale, 1)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((*theme["overlay"],170))
        screen.blit(overlay, (0,0))


        popup_width = int(900 * scale)
        popup_height = int(900 * scale)

        popup = pygame.Rect(
            WIDTH//2 - popup_width//2,
            HEIGHT//2 - popup_height//2,
            popup_width,
            popup_height
        )


        pygame.draw.rect(
            screen,
            theme["popup"],
            popup,
            border_radius=30
        )

        pygame.draw.rect(
            screen,
            theme["popup_border"],
            popup,
            5,
            border_radius=30
        )


        if scale < 0.95:
            return


        # ---------------- TROPHY ----------------

        trophy_x = WIDTH//2 - self.trophy.get_width()//2
        trophy_y = popup.y + 1
        # ---------- Golden Shining Rays Behind Trophy ----------

        cx = WIDTH//2
        cy = trophy_y + self.trophy.get_height() // 2

        rotation = time.time() * 60

        # Long rays
        for i in range(20):
            angle = math.radians(i * 18 + rotation)

            pygame.draw.line(
                screen,
                (255, 220, 80),
                (
                    cx + math.cos(angle) * 100,
                    cy + math.sin(angle) * 100
                ),
                (
                    cx + math.cos(angle) * 165,
                    cy + math.sin(angle) * 165
                ),
                4
            )

        # Short rays between them
        for i in range(20):
            angle = math.radians(i * 18 + 9 + rotation)

            pygame.draw.line(
                screen,
                (255, 240, 170),
                (
                    cx + math.cos(angle) * 110,
                    cy + math.sin(angle) * 110
                ),
                (
                    cx + math.cos(angle) * 155,
                    cy + math.sin(angle) * 155
                ),
                2
            )

        screen.blit(
            self.trophy,
            (trophy_x, trophy_y)
        )


        # ---------------- TITLE ----------------

        title = self.win_font.render(
            "CONGRATULATIONS!",
            True,
            theme["success"]
        )

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH//2,popup.y+300)
            )
        )


        # ---------------- STARS ----------------

        if self.logic.mistakes == 0:
            count = 5
        elif self.logic.mistakes <= 3:
            count = 4
        elif self.logic.mistakes <= 8:
            count = 3
        elif self.logic.mistakes <= 15:
            count = 2
        else:
            count = 1


        star_size = 100
        spacing = 100

        total_width = spacing * 4 + star_size
        start_x = WIDTH//2 - total_width//2

        star_y = popup.y + 340


        for i in range(5):
            pulse = 1 + 0.08 * math.sin(
                time.time()*4 + i*0.5
            )

            size = int(star_size * pulse)

            star = pygame.transform.smoothscale(
                self.star_icon,
                (size,size)
            )

            if i >= count:
                star = star.copy()
                star.fill(
                    (120,120,120,180),
                    special_flags=pygame.BLEND_RGBA_MULT
                )

            x = start_x + i*spacing + (star_size-size)//2
            y = star_y + (star_size-size)//2

            screen.blit(
                star,
                (x,y)
            )

        # ---------------- STATS CARD ----------------

        stats_card = pygame.Rect(
            popup.x + 80,
            popup.y + 420,
            popup.width - 160,
            300
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
            (self.accuracy_icon, "ACCURACY", f"{self.logic.accuracy}%"),
            (self.score_icon, "SCORE", f"{self.logic.score:,}")
        ]
        

        label_font = pygame.font.Font(
            "assets/fonts/Poppins-Regular.ttf",
            28
        )

        value_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            30
        )
        y = stats_card.y + 35

        for icon,label,value in stats:
            if icon:
                screen.blit(
                    icon,
                    (
                        stats_card.x + 25,
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
            elif label == "ACCURACY":
                value_color = (34, 170, 70)       # Green
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
                    stats_card.x + 75,
                    y
                )
            )

            screen.blit(
                v,
                v.get_rect(
                    midright=(
                        stats_card.right - 45,
                        y + 18
                    )
                )
            )

            y += 52


        
        
    
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

                if theme == themes.DARK:
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
        self.draw_background(screen, theme)
        self.draw_ui(screen, theme)
        self.draw_cell_backgrounds(screen, theme)
        self.draw_grid(screen, theme)          # <-- moved here
        self.draw_highlights(screen, theme)
        self.draw_numbers(screen, theme)
        self.draw_win(screen, theme)