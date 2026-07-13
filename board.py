import pygame
import math
import time

from constants import *


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

        self.star_icon = pygame.image.load(
            "assets/images/star.png"
        ).convert_alpha()

        self.exit_icon = pygame.image.load(
            "assets/images/exit.png"
        ).convert_alpha()
        self.new_icon = pygame.image.load(
            "assets/images/new_game.png"
        ).convert_alpha()
        self.trophy = pygame.transform.smoothscale(self.trophy, (120, 120))

        self.timer_icon = pygame.transform.smoothscale(self.timer_icon, (40, 40))

        self.mistake_icon = pygame.transform.smoothscale(self.mistake_icon, (40, 40))

        self.target_icon = pygame.transform.smoothscale(self.target_icon, (40, 40))

        self.star_icon = pygame.transform.smoothscale(self.star_icon, (100, 100))     

        self.exit_icon = pygame.transform.smoothscale(self.exit_icon, (30, 30))
        
        self.new_icon = pygame.transform.smoothscale(self.new_icon,(30, 30))

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
        # ---------- Smooth Selection Animation ----------
        self.highlight_x = BOARD_X
        self.highlight_y = BOARD_Y

        self.target_x = BOARD_X
        self.target_y = BOARD_Y
        self.pulse_time = 0

    def select(self, mouse_pos):

        x, y = mouse_pos

        if (BOARD_X <= x < BOARD_X + CELL_SIZE * 9 and
                BOARD_Y <= y < BOARD_Y + CELL_SIZE * 9):

            col = (x - BOARD_X) // CELL_SIZE
            row = (y - BOARD_Y) // CELL_SIZE

            self.logic.select(row, col)
    def draw_background(self, screen):
        screen.fill(BACKGROUND)
        # ---------- Header Background ----------
        pygame.draw.rect(
            screen,
            (235, 240, 248),      # light blue-grey
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

        # Shadow
        shadow = header_rect.copy()
        shadow.y += 4

        pygame.draw.rect(
            screen,
            (195, 200, 210),
            shadow,
            border_radius=20
        )

        # Header Card
        pygame.draw.rect(
            screen,
            (250, 252, 255),
            header_rect,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            header_rect,
            2,
            border_radius=20
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
            (210, 215, 225),
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
            (255, 255, 255),
            board_rect,
            border_radius=28
        )

        pygame.draw.rect(
            screen,
            (70, 70, 70),
            board_rect,
            3,
            border_radius=28
        )

    def draw_ui(self, screen):

        # Header
        # ---------- Header Stat Cards ----------

        card_w = 300
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
                (205, 210, 220),
                shadow,
                border_radius=18
            )

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                card,
                border_radius=18
            )

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                card,
                2,
                border_radius=18
            )

        if self.logic.game_won:
            elapsed = int(self.logic.end_time - self.logic.start_time)
        else:
            elapsed = int(time.time() - self.logic.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        

        # ---------- Left ----------
        difficulty = self.header_font.render(
            f"Difficulty : {self.logic.difficulty}",
            True,
            TEXT
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
            f"Time : {minutes:02}:{seconds:02}",
            True,
            TEXT
        )

        

        screen.blit(
            timer,
            timer.get_rect(center=center_card.center)
            )

        # ---------- Right ----------
        mistakes = self.header_font.render(
            f"Mistakes : {self.logic.mistakes}",
            True,
            RED
        )

        

        screen.blit(
            mistakes,
            mistakes.get_rect(center=right_card.center)
        )

    def draw_highlights(self, screen):
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
                    (242, 247, 255),
                    hover_rect,
                    border_radius=10
                )

                pygame.draw.rect(
                    screen,
                    (170, 205, 255),
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
                   (244,247,255),
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
                HIGHLIGHT,
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
                HIGHLIGHT,
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
                            (255,245,170),
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
            (70, 120, 255, alpha),
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
            (225, 238, 255),
            cell_rect,
            border_radius=12
        )

        # ---------- White Inner Border ----------
        pygame.draw.rect(
            screen,
            (255,255,255),
            cell_rect,
            2,
            border_radius=12
        )

        # ---------- Blue Border ----------
        border_width = int(3 + pulse * 2)

        blue = (
            50,
            int(110 + pulse * 40),
            255
        )

        pygame.draw.rect(
            screen,
            blue,
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


    def draw_numbers(self, screen):
        for row in range(9):
            for col in range(9):
                value = self.logic.grid[row][col]
                if value == 0:
                    continue

                if self.logic.fixed[row][col]:
                    color = (30, 30, 30)
                elif value != self.logic.solution[row][col]:
                    color = (215, 40, 40)
                elif self.logic.selected == (row, col):
                    color = (25, 70, 220)
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
                    (185, 185, 185)
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

    def draw_grid(self, screen):
        
        # ---------- Thin Lines ----------
        for i in range(10):
            if i % 3 != 0:
                pygame.draw.line(
                    screen,
                    (220, 225, 235),
                    (BOARD_X + i * CELL_SIZE, BOARD_Y),
                    (BOARD_X + i * CELL_SIZE, BOARD_Y + 9 * CELL_SIZE),
                    2
                )

                pygame.draw.line(
                    screen,
                    (220, 225, 235),
                    (BOARD_X, BOARD_Y + i * CELL_SIZE),
                    (BOARD_X + 9 * CELL_SIZE, BOARD_Y + i * CELL_SIZE),
                    2
                )

        # ---------- Thick Lines ----------
        for i in range(0, 10, 3):
            pygame.draw.line(
                screen,
                (55, 60, 70),
                (BOARD_X + i * CELL_SIZE, BOARD_Y),
                (BOARD_X + i * CELL_SIZE, BOARD_Y + 9 * CELL_SIZE),
                4
            )

            pygame.draw.line(
                screen,
                (55, 60, 70),
                (BOARD_X, BOARD_Y + i * CELL_SIZE),
                (BOARD_X + 9 * CELL_SIZE, BOARD_Y + i * CELL_SIZE),
                4
            )

    def draw_win(self, screen):
        if not self.logic.game_won:
            return

        if self.logic.popup_scale < 1:
            self.logic.popup_scale += (1 - self.logic.popup_scale) * 0.14

        scale = min(self.logic.popup_scale, 1)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
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
            (255,255,255),
            popup,
            border_radius=30
        )

        pygame.draw.rect(
            screen,
            PRIMARY,
            popup,
            5,
            border_radius=30
        )


        if scale < 0.95:
            return


        # ---------------- TROPHY ----------------

        trophy_x = WIDTH//2 - self.trophy.get_width()//2
        trophy_y = popup.y + 60
        # ---------- Golden Shining Rays Behind Trophy ----------

        cx = WIDTH//2
        cy = trophy_y + self.trophy.get_height() // 2

        rotation = time.time() * 60

        for i in range(16):
            angle = math.radians(i * 22.5 + rotation)
            inner = 45
            outer = 75
            x1 = cx + math.cos(angle) * inner
            y1 = cy + math.sin(angle) * inner

            x2 = cx + math.cos(angle) * outer
            y2 = cy + math.sin(angle) * outer

            pygame.draw.line(
                screen,
                (255, 220, 80),
                (x1, y1),
                (x2, y2),
                4
            )

        screen.blit(
            self.trophy,
            (trophy_x, trophy_y)
        )


        # ---------------- TITLE ----------------

        title = self.win_font.render(
            "CONGRATULATIONS!",
            True,
            GREEN
        )

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH//2,popup.y+245)
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
            (248,250,255),
            stats_card,
            border_radius=25
        )

        pygame.draw.rect(
            screen,
            (210,215,225),
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
            ("Time", f"{minutes:02}:{seconds:02}", self.timer_icon),
            ("Mistakes", str(self.logic.mistakes), self.mistake_icon),
            ("Difficulty", self.logic.difficulty.title(), self.target_icon),
            ("Accuracy", f"{self.logic.accuracy}%", None),
            ("Score", f"{self.logic.score:,}", None)
        ]

        label_font = pygame.font.SysFont(
            "Segoe UI",
            28,
            bold=True
        )

        value_font = pygame.font.SysFont(
            "Segoe UI",
            28
        )

        y = stats_card.y + 35

        for label, value, icon in stats:
            if icon:
                screen.blit(
                    icon,
                    (
                        stats_card.x + 20,
                        y
                    )
                )

            l = label_font.render(
                label,
                True,
                (90, 90, 90)
            )

            v = value_font.render(
                value,
                True,
                TEXT
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


        
        
    
    def draw_cell_backgrounds(self, screen):
        # ---------- 3x3 Region Backgrounds ----------
        for box_row in range(3):
            for box_col in range(3):

                region = pygame.Rect(
                    BOARD_X + box_col * CELL_SIZE * 3 + 3,
                    BOARD_Y + box_row * CELL_SIZE * 3 + 3,
                    CELL_SIZE * 3 - 6,
                    CELL_SIZE * 3 - 6
                )

                color = (
                    (248, 250, 255)
                    if (box_row + box_col) % 2 == 0
                    else (255, 255, 255)
                )

                pygame.draw.rect(
                    screen,
                    color,
                    region,
                    border_radius=12
                )

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_ui(screen)
        self.draw_cell_backgrounds(screen)
        self.draw_grid(screen)          # <-- moved here
        self.draw_highlights(screen)
        self.draw_numbers(screen)
        self.draw_win(screen)