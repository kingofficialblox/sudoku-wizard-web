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
        self.trophy = pygame.transform.smoothscale(self.trophy, (90, 90))

        self.timer_icon = pygame.transform.smoothscale(self.timer_icon, (28, 28))

        self.mistake_icon = pygame.transform.smoothscale(self.mistake_icon, (28, 28))

        self.target_icon = pygame.transform.smoothscale(self.target_icon, (28, 28))

        self.star_icon = pygame.transform.smoothscale(self.star_icon, (50, 50))     

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
            25
        )

        self.title_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            50
        )

        self.win_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            56
        )

        self.popup_font = pygame.font.Font(
            "assets/fonts/Poppins-Regular.ttf",
            28
        )

        self.star_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            36
        )

    def select(self, mouse_pos):

        x, y = mouse_pos

        if (BOARD_X <= x < BOARD_X + CELL_SIZE * 9 and
                BOARD_Y <= y < BOARD_Y + CELL_SIZE * 9):

            col = (x - BOARD_X) // CELL_SIZE
            row = (y - BOARD_Y) // CELL_SIZE

            self.logic.select(row, col)
    def draw_background(self, screen):
        screen.fill(BACKGROUND)
        
        pygame.draw.rect(
            screen,
            HEADER_BG,
            (0, 0, WIDTH, HEADER_HEIGHT)
        )

        pygame.draw.line(
            screen,
            (180, 180, 180),
            (0, HEADER_HEIGHT),
            (WIDTH, HEADER_HEIGHT),
            2
        )

        # ---------- Shadow ----------
        shadow_rect = pygame.Rect(
            BOARD_X + 5,
            BOARD_Y + 5,
            CELL_SIZE * 9,
            CELL_SIZE * 9
        )

        pygame.draw.rect(
            screen,
            (210, 215, 225),
            shadow_rect,
            border_radius=14
        )

        # ---------- Board Card ----------
        board_rect = pygame.Rect(
            BOARD_X,
            BOARD_Y,
            CELL_SIZE * 9,
            CELL_SIZE * 9
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            board_rect,
            border_radius=14
        )

        pygame.draw.rect(
            screen,
            (225, 228, 235),
            board_rect,
            2,
            border_radius=14
        )

    def draw_ui(self, screen):
        

        # Header
        pygame.draw.rect(
            screen,
            HEADER_BG,
            (0, 0, WIDTH, HEADER_HEIGHT)
        )

        pygame.draw.line(
            screen,
            (210, 210, 210),
            (0, HEADER_HEIGHT),
            (WIDTH, HEADER_HEIGHT),
            2
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

        screen.blit(difficulty, (40, 90))

        # ---------- Centre ----------
        timer = self.header_font.render(
            f"Time : {minutes:02}:{seconds:02}",
            True,
            TEXT
        )

        timer_rect = timer.get_rect(
            center=(WIDTH // 2, 110)
        )

        screen.blit(timer, timer_rect)

        # ---------- Right ----------
        mistakes = self.header_font.render(
            f"Mistakes : {self.logic.mistakes}",
            True,
            RED
        )

        mistakes_rect = mistakes.get_rect(
            topright=(WIDTH - 40, 90)
        )

        screen.blit(mistakes, mistakes_rect)

    def draw_highlights(self, screen):
        if self.logic.hover:
            hover_row, hover_col = self.logic.hover

            if self.logic.selected != (hover_row, hover_col):
                pygame.draw.rect(
                    screen,
                    (247, 250, 255),
                    (
                        BOARD_X + hover_col * CELL_SIZE,
                        BOARD_Y + hover_row * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                )
        if self.logic.highlight_number is not None:
            for r in range(9):
                for c in range(9):
                    if self.logic.grid[r][c] == self.logic.highlight_number:
                        pygame.draw.rect(
                            screen,
                            (255, 248, 196),
                            (
                                BOARD_X + c * CELL_SIZE,
                                BOARD_Y + r * CELL_SIZE,
                                CELL_SIZE,
                                CELL_SIZE
                            )
                        )

        if not self.logic.selected:
            return

        row, col = self.logic.selected

        # -------------------------
        # Highlight 3×3 Box
        # -------------------------

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3

        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                pygame.draw.rect(
                    screen,
                    BOX_HIGHLIGHT,
                    (
                        BOARD_X + c * CELL_SIZE,
                        BOARD_Y + r * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                )

        # -------------------------
        # Highlight Row
        # -------------------------

        pygame.draw.rect(
            screen,
            HIGHLIGHT,
            (
                BOARD_X,
                BOARD_Y + row * CELL_SIZE,
                CELL_SIZE * 9,
                CELL_SIZE
            )
        )

        # -------------------------
        # Highlight Column
        # -------------------------

        pygame.draw.rect(
            screen,
            HIGHLIGHT,
            (
                BOARD_X + col * CELL_SIZE,
                BOARD_Y,
                CELL_SIZE,
                CELL_SIZE * 9
            )
        )

        # -------------------------
        # Selected Cell
        # -------------------------

        pygame.draw.rect(
            screen,
            LIGHT_BLUE,
            (
                BOARD_X + col * CELL_SIZE,
                BOARD_Y + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )
        pygame.draw.rect(
            screen,
            PRIMARY,
            (
                BOARD_X + col * CELL_SIZE,
                BOARD_Y + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            ),
            3,
            border_radius=6
        )
        
    def draw_numbers(self, screen):
        for row in range(9):
            for col in range(9):
                value = self.logic.grid[row][col]
                if value == 0:
                    continue

                if self.logic.fixed[row][col]:
                    color = BLACK
                elif value != self.logic.solution[row][col]:
                    color = RED
                else:
                    color = BLUE
                text = self.number_font.render(str(value), True, color)

                # -------- Pop Animation --------
                if self.logic.pop_cell == (row, col):
                    elapsed = time.time() - self.logic.pop_time
                    if elapsed < 0.12:
                        scale = 1.35 - elapsed * 2.5
                        new_size = (
                            int(text.get_width() * scale),
                            int(text.get_height() * scale)
                        )
                        text = pygame.transform.smoothscale(text, new_size)

                rect = text.get_rect(
                    center=(
                        BOARD_X + col * CELL_SIZE + CELL_SIZE // 2,
                        BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2
                    )
                )

                screen.blit(text, rect)
        
        if self.logic.invalid_cell:

                    if time.time() - self.logic.invalid_time < 0.5:

                        row, col = self.logic.invalid_cell
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
                    (195, 200, 210),
                    (BOARD_X + i * CELL_SIZE, BOARD_Y),
                    (BOARD_X + i * CELL_SIZE, BOARD_Y + 9 * CELL_SIZE),
                    1
                )

                pygame.draw.line(
                    screen,
                    (195, 200, 210),
                    (BOARD_X, BOARD_Y + i * CELL_SIZE),
                    (BOARD_X + 9 * CELL_SIZE, BOARD_Y + i * CELL_SIZE),
                    1
                )

        # ---------- Thick Lines ----------
        for i in range(0, 10, 3):

            pygame.draw.line(
                screen,
                (45, 45, 45),
                (BOARD_X + i * CELL_SIZE, BOARD_Y),
                (BOARD_X + i * CELL_SIZE, BOARD_Y + 9 * CELL_SIZE),
                3
            )

            pygame.draw.line(
                screen,
                (45, 45, 45),
                (BOARD_X, BOARD_Y + i * CELL_SIZE),
                (BOARD_X + 9 * CELL_SIZE, BOARD_Y + i * CELL_SIZE),
                3
            )

    def draw_win(self, screen):
        if self.logic.popup_scale < 1:
            self.logic.popup_scale += (1 - self.logic.popup_scale) * 0.14
            scale = self.logic.popup_scale

        scale = min(self.logic.popup_scale, 1)
        self.sparkle_angle += 2
        
        if not self.logic.game_won:
            return

        # Dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        popup_width = int(500 * scale)
        popup_height = int(470* scale)

        popup_rect = pygame.Rect(
            WIDTH//2 - popup_width//2,
            HEIGHT//2 - popup_height//2,
            popup_width,
            popup_height
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            popup_rect,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            PRIMARY,
            popup_rect,
            4,
            border_radius=20
        )
        if scale < 0.95:
            return
        # Floating animation
        float_offset = math.sin(time.time() * 2.5) * 4

        trophy_x = WIDTH // 2 - self.trophy.get_width() // 2
        trophy_y = popup_rect.y + 8 + float_offset
        # ---------- Golden Rays ----------
        center_x = WIDTH // 2
        center_y = trophy_y + self.trophy.get_height() // 2

        rotation = time.time() * 40

        for i in range(16):
            angle = math.radians(i * (360 / 16) + rotation)

            inner = 42
            outer = 70

            x1 = center_x + math.cos(angle) * inner
            y1 = center_y + math.sin(angle) * inner

            x2 = center_x + math.cos(angle) * outer
            y2 = center_y + math.sin(angle) * outer

            pygame.draw.line(
                screen,
                (255, 225, 120),
                (x1, y1),
                (x2, y2),
                3
            )

        screen.blit(
            self.trophy,
            (trophy_x, trophy_y)
        )
        # ---------- Trophy Sparkles ----------
        center_x = WIDTH // 2
        center_y = popup_rect.y + 55

        radius = 55

        for i in range(4):
            angle = math.radians(self.sparkle_angle + i * 90)

            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius

            # Outer glow
            pygame.draw.circle(
                screen,
                (255, 235, 120),
                (int(x), int(y)),
                6
            )

            # Bright center
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (int(x), int(y)),
                2
            )

        title_font = pygame.font.SysFont("Segoe UI", 48, bold=True)

        title = title_font.render(
            "CONGRATULATIONS!",
            True,
            GREEN
        )

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH//2, popup_rect.y +155)
            )
        )
        if self.logic.game_won:
            elapsed = int(self.logic.end_time - self.logic.start_time)
        else:
            elapsed = int(time.time() - self.logic.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        time_text = self.popup_font.render(
            f"Time : {minutes:02}:{seconds:02}",
            True,
            TEXT
        )

        icon_x = popup_rect.x + 120

        screen.blit(
            self.timer_icon,
            (icon_x, popup_rect.y + 190)
        )

        screen.blit(
            time_text,
            (icon_x + 45, popup_rect.y + 190)
        )

        mistake_text = self.popup_font.render(
            f"Mistakes : {self.logic.mistakes}",
            True,
            RED
        )

        screen.blit(
            self.mistake_icon,
            (icon_x, popup_rect.y + 235)
        )

        screen.blit(
            mistake_text,
            (icon_x + 45, popup_rect.y + 235)
        )
        difficulty_text = self.popup_font.render(
            f"Difficulty : {self.logic.difficulty.title()}",
            True,
            PRIMARY
        )

        screen.blit(
            self.target_icon,
            (icon_x, popup_rect.y + 280)
        )

        screen.blit(
            difficulty_text,
            (icon_x + 45, popup_rect.y + 280)
        )

        star_y = popup_rect.y + 360

        start_x = WIDTH//2 - 75

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

        for i in range(count):
            pulse = 1 + 0.12 * math.sin(time.time() * 5 + i * 0.6)
            size = int(30 * pulse)
            star = pygame.transform.smoothscale(
                self.star_icon,
                (size, size)
            )
            x = start_x + i * 35 + (30 - size) // 2
            y = star_y + (30 - size) // 2
            screen.blit(star, (x, y))

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_ui(screen)
        self.draw_highlights(screen)
        self.draw_numbers(screen)
        self.draw_grid(screen)
        self.draw_win(screen)

        