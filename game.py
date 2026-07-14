import pygame
import time

from constants import *
from board import Board
from sudoku_logic import SudokuLogic
from button import Button
from confetti import Confetti

class Game:

    def __init__(self):

        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption("Sudoku")

        self.clock = pygame.time.Clock()

        self.logic = SudokuLogic()

        self.board = Board(self.logic)
        # ---------- Popup Icons ----------

        self.new_icon = pygame.image.load(
            "assets/images/new_game.png"
        ).convert_alpha()

        self.exit_icon = pygame.image.load(
            "assets/images/exit.png"
        ).convert_alpha()

        self.restart_icon = pygame.image.load(
            "assets/images/restart.png"
        ).convert_alpha()

        self.undo_icon = pygame.image.load(
            "assets/images/undo.png"
        ).convert_alpha()

        self.hint_icon = pygame.image.load(
            "assets/images/hint.png"
        ).convert_alpha()        
        self.pause_icon = pygame.image.load(
            "assets/images/pause.png"
        ).convert_alpha()

        self.resume_icon = pygame.image.load(
            "assets/images/resume.png"
        ).convert_alpha()
        self.pause_popup_icon = pygame.image.load(
            "assets/images/pause.png"
        ).convert_alpha()

        self.pause_popup_icon = pygame.transform.smoothscale(
            self.pause_popup_icon,
            (70, 70)
        )

        self.new_icon = pygame.transform.smoothscale(
            self.new_icon,
            (30, 30)
        )

        self.exit_icon = pygame.transform.smoothscale(
            self.exit_icon,
            (30, 30)
        )

        self.restart_icon = pygame.transform.smoothscale(
            self.restart_icon,
            (30, 30)
        )

        self.undo_icon = pygame.transform.smoothscale(
            self.undo_icon,
            (30, 30)
        )

        self.hint_icon = pygame.transform.smoothscale(
            self.hint_icon,
            (30, 30)
        )               
        self.pause_icon = pygame.transform.smoothscale(
            self.pause_icon,
            (50, 50)
        )

        self.resume_icon = pygame.transform.smoothscale(
            self.resume_icon,
            (30, 30)
        )
        side_x = BOARD_X + CELL_SIZE * 9 + 30
        button_width = 220
        button_height = 52
        gap = 15
        button_y1 = BOARD_Y + 150
        start_x = side_x
        board_bottom = BOARD_Y + CELL_SIZE * 9
        button_y2 = board_bottom + 25
        
        
        
        
        self.new_game_button = Button(
            start_x,
            button_y1 + 0,
            button_width,
            button_height,
            "NEW",
            self.new_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )

        self.restart_button = Button(
            start_x,
            button_y1 + 70,
            button_width,
            button_height,
            "RESET",
            self.restart_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )

        self.undo_button = Button(
            start_x,
            button_y1 + 140,
            button_width,
            button_height,
            "UNDO",
            self.undo_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )

        self.hint_button = Button(
            start_x,
            button_y1 + 210,
            button_width,
            button_height,
            "HINT",
            self.hint_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        self.exit_button = Button(
            start_x,
            button_y1 + 280,
            button_width,
            button_height,
            "EXIT",
            self.exit_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )

        # ---------- Second Row ----------
        difficulty_width = 140

        difficulty_start = (WIDTH - (3 * difficulty_width + 2 * gap)) // 2

        self.easy_button = Button(
            difficulty_start,
            button_y2,
            difficulty_width,
            button_height,
            "EASY",
            bg_color=(52, 152, 219),
            hover_color=(90, 185, 255)
        )

        self.medium_button = Button(
            difficulty_start + difficulty_width + gap,
            button_y2,
            difficulty_width,
            button_height,
            "MEDIUM",
            bg_color=(243, 156, 18),
            hover_color=(255, 190, 50)
        )

        self.hard_button = Button(
            difficulty_start + (difficulty_width + gap) * 2,
            button_y2,
            difficulty_width,
            button_height,
            "HARD",
            bg_color=(192, 57, 43),
            hover_color=(220, 80, 65)
        )

        # -------- Number Buttons --------

        self.number_buttons = []

        key_width = 75
        key_height = 55
        gap = 12

        start_x = BOARD_X - 100
        start_y = BOARD_Y + 10

        for i in range(9):
            self.number_buttons.append(
                Button(
                    start_x,
                    start_y + i * (key_height + gap),
                    key_width,
                    key_height,
                    str(i + 1)
                )
            )

        self.running = True
        self.paused = False
        self.pause_popup_scale = 0.85
        self.pause_overlay_alpha = 0

        
        self.notes_mode = False
        

        # ---------- Win Popup Buttons ----------

        self.popup_new_button = Button(
            WIDTH//2 - 230,
            HEIGHT//2 + 300,
            220,
            70,
            "NEW GAME",
            self.new_icon,
            bg_color=(46, 204, 113),
            hover_color=(72, 230, 140)
        )

        self.popup_exit_button = Button(
            WIDTH//2 + 10,
            HEIGHT//2 + 300,
            220,
            70,
            "EXIT",
            self.exit_icon,
            bg_color=(231, 76, 60),
            hover_color=(255, 110, 90)
        )
        # ---------- Pause Button ----------
        self.pause_button = pygame.Rect(
            WIDTH - 75,
            200,
            36,
            36
        )
        self.pause_hover = False
        self.pause_scale = 1.0
        self.pause_pressed = False
        self.pause_buttons_offset = 25
        # ---------- Pause Popup Buttons ----------
        self.resume_button = Button(
            WIDTH//2 - 130,
            HEIGHT//2 - 60,
            260,
            60,
            "RESUME",
            self.resume_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        # ---------- Pause Popup Buttons ----------
        self.pause_reset_button = Button(
            WIDTH//2 - 130,HEIGHT//2 + 25,
            260,
            60,
            "RESET",
            self.restart_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        self.pause_new_button = Button(
            WIDTH//2 - 130,
            HEIGHT//2 + 110,
            260,
            60,
            "NEW",
            self.new_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        # ---------- Sounds ----------

        self.click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
        self.correct_sound = pygame.mixer.Sound("assets/sounds/correct.wav")
        self.wrong_sound = pygame.mixer.Sound("assets/sounds/wrong.wav")
        self.hint_sound = pygame.mixer.Sound("assets/sounds/hint.wav")
        self.win_sound = pygame.mixer.Sound("assets/sounds/win.wav")

        # Volume
        self.click_sound.set_volume(0.35)
        self.correct_sound.set_volume(0.45)
        self.wrong_sound.set_volume(0.45)
        self.hint_sound.set_volume(0.40)
        self.win_sound.set_volume(0.60)
        # ---------- Confetti ----------
        self.confetti = []
        self.previous_win_state = False
        

    def handle_events(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if (
            BOARD_X <= mouse_x < BOARD_X + CELL_SIZE * 9
            and
            BOARD_Y <= mouse_y < BOARD_Y + CELL_SIZE * 9
        ):

            row = (mouse_y - BOARD_Y) // CELL_SIZE
            col = (mouse_x - BOARD_X) // CELL_SIZE

            self.logic.hover = (row, col)

        else:
            self.logic.hover = None

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.pause_pressed = False
                pos = pygame.mouse.get_pos()
                self.pause_hover = self.pause_button.collidepoint(pos)
                if self.paused:
                    if self.resume_button.clicked(pos):
                        self.click_sound.play()
                        self.logic.resume()
                        self.paused = False
                        

                    elif self.pause_reset_button.clicked(pos):
                        self.click_sound.play()
                        self.logic.restart()
                        self.logic.paused = False
                        self.paused = False

                    elif self.pause_new_button.clicked(pos):
                        self.click_sound.play()
                        self.new_game(self.logic.difficulty)
                        self.paused = False

                    continue

                if self.logic.game_won:
                    if self.popup_new_button.clicked(pos):
                        self.click_sound.play()
                        self.new_game(self.logic.difficulty)

                    elif self.popup_exit_button.clicked(pos):
                        self.click_sound.play()
                        self.running = False

                    # Ignore every other click while popup is open
                    continue

                if self.new_game_button.clicked(pos):
                    self.click_sound.play()
                    self.new_game(self.logic.difficulty)

                elif self.easy_button.clicked(pos):
                    self.click_sound.play()
                    self.new_game("EASY")

                elif self.medium_button.clicked(pos):
                    self.click_sound.play()
                    self.new_game("MEDIUM")

                elif self.hard_button.clicked(pos):
                    self.click_sound.play()
                    self.new_game("HARD")

                elif self.hint_button.clicked(pos):
                    self.click_sound.play()
                    self.hint_sound.play()
                    self.logic.give_hint()

                elif self.undo_button.clicked(pos):
                    self.click_sound.play()
                    self.logic.undo()              
                elif self.exit_button.clicked(pos):
                    self.click_sound.play()
                    self.running = False

                elif self.restart_button.clicked(pos):
                    self.click_sound.play()
                    self.logic.restart()
                    self.board.display_score = 0
                elif self.pause_button.collidepoint(pos):
                    self.pause_pressed = True
                    self.click_sound.play()

                    if self.logic.paused:
                        self.logic.resume()
                    else:
                        self.logic.pause()
                        self.pause_popup_scale = 0.85
                        self.pause_overlay_alpha = 0

                    self.paused = self.logic.paused

                for i, button in enumerate(self.number_buttons):
                    if button.clicked(pos):
                        self.logic.highlight_number = i + 1

                        result = self.logic.place_number(
                            i + 1,
                            self.notes_mode
                        )

                        if result == "WIN":
                            self.correct_sound.play()
                            self.win_sound.play()

                        elif result is True:
                            self.correct_sound.play()

                        elif result is False:
                            self.wrong_sound.play()
                        break
                else:
                    self.board.select(pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.logic.undo()

                elif event.key == pygame.K_n:
                    self.notes_mode = not self.notes_mode

                elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    self.logic.clear_cell()

                elif pygame.K_1 <= event.key <= pygame.K_9:
                    self.logic.highlight_number = event.key - pygame.K_0
                    result = self.logic.place_number(
                        event.key - pygame.K_0,
                        self.notes_mode
                    )

                    if result == "WIN":
                        self.correct_sound.play()
                        self.win_sound.play()

                    elif result is True:
                        self.correct_sound.play()

                    elif result is False:
                        self.wrong_sound.play()

                # Arrow Keys
                elif event.key == pygame.K_UP:
                    self.logic.move_selection(-1, 0)

                elif event.key == pygame.K_DOWN:
                    self.logic.move_selection(1, 0)

                elif event.key == pygame.K_LEFT:
                    self.logic.move_selection(0, -1)

                elif event.key == pygame.K_RIGHT:
                    self.logic.move_selection(0, 1)
            


    def draw(self):
        self.screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        self.pause_hover = self.pause_button.collidepoint(mouse_pos)
        # ---------- Spawn confetti once ----------
        if self.logic.game_won and not self.previous_win_state:

            self.confetti = []

            for _ in range(800):
                self.confetti.append(Confetti())

            self.previous_win_state = True

        elif not self.logic.game_won:
            self.previous_win_state = False

        # Draw the Sudoku board
        self.board.draw(self.screen)
        # ---------- Pause Button ----------
        # ---------- Pause Button Animation ----------

        target_scale = 1.0
        

        if self.pause_hover:
            target_scale = 1.12

        if self.pause_pressed:
            target_scale = 0.90

        self.pause_scale += (
            target_scale - self.pause_scale
        ) * 0.22

        size = int(64 * self.pause_scale)

        icon = pygame.transform.smoothscale(
            self.pause_icon,
            (size, size)
        )

        rect = icon.get_rect(
            center=self.pause_button.center
        )
        shadow = pygame.Surface(
            (size + 10, size + 10),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            shadow,
            (0, 0, 0, 35),
            (
                shadow.get_width() // 2,
                shadow.get_height() // 2
            ),
            size // 2 + 4
        )

        shadow_rect = shadow.get_rect(
            center=(
                rect.centerx,
                rect.centery + 4
            )
        )

        self.screen.blit(shadow, shadow_rect)
        if self.pause_hover:
            glow = pygame.Surface(
                (size + 30, size + 30),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                glow,
                (120, 120, 120, 45),
                (
                    glow.get_width() // 2,
                    glow.get_height() // 2
                ),
                size // 2 + 8
            )

            glow_rect = glow.get_rect(center=rect.center)

            self.screen.blit(glow, glow_rect)

        self.screen.blit(icon, rect)

        # ---------- Draw Confetti ----------
        if self.logic.game_won:

            # Update & draw
            for particle in self.confetti:
                particle.update()
                particle.draw(self.screen)
            # Remove particles that leave the screen
            self.popup_new_button.draw(self.screen)
            self.popup_exit_button.draw(self.screen)

        # Draw buttons only if the game hasn't been won
        if not self.logic.game_won and not self.paused:
            for i, button in enumerate(self.number_buttons):
                number = i + 1

                button.count = self.logic.remaining_count(number)

                button.selected = (
                    self.logic.highlight_number == number
                )

                button.draw(self.screen)

            self.new_game_button.draw(self.screen)
            self.restart_button.draw(self.screen)
            self.undo_button.draw(self.screen)
            self.hint_button.draw(self.screen)            
            self.exit_button.draw(self.screen)
            self.easy_button.draw(self.screen)
            self.medium_button.draw(self.screen)
            self.hard_button.draw(self.screen)
        if self.paused:
            self.pause_popup_scale += (
                1 - self.pause_popup_scale
            ) * 0.22
            self.pause_buttons_offset += (
                0 - self.pause_buttons_offset
            ) * 0.18
            # Dark overlay
            self.pause_overlay_alpha += (
                120 - self.pause_overlay_alpha
            ) * 0.18

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(
                (
                    0,
                    0,
                    0,
                    int(self.pause_overlay_alpha)
                )
            )
            self.screen.blit(overlay, (0, 0))

            # Popup
            # Bounce popup animation
            scale = self.pause_popup_scale

            if scale > 0.96:
                scale = 1 + (0.96 - scale) * 0.35

            popup_width = int(500 * scale)
            popup_height = int(430 * scale)

            popup = pygame.Rect(
                WIDTH//2 - popup_width//2,
                HEIGHT//2 - popup_height//2,
                popup_width,
                popup_height
            )

            # Shadow behind popup
            shadow = pygame.Surface(
                (popup.width + 30, popup.height + 30),
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                shadow,
                (190, 195, 205, 120),
                shadow.get_rect(),
                border_radius=25
            )

            self.screen.blit(
                shadow,
                (
                    popup.x - 15,
                    popup.y - 5
                )
            )

            # Main popup
            pygame.draw.rect(
                self.screen,
                (255,255,255),
                popup,
                border_radius=25
            )

            # Border
            pygame.draw.rect(
                self.screen,
                (210,210,210),
                popup,
                2,
                border_radius=25
            )

            
            circle_center = (WIDTH // 2, popup.y + 72)

            pygame.draw.circle(
                self.screen,
                (235, 235, 235),
                circle_center,
                42
            )

            pygame.draw.circle(
                self.screen,
                (180, 180, 180),
                circle_center,
                2,
            )
            icon_rect = self.pause_popup_icon.get_rect(
                center=circle_center
            )

            self.screen.blit(
                self.pause_popup_icon,
                icon_rect
            )

            title = self.board.header_font.render(
                "Paused",
                True,
                (45,45,45)
            )

            self.screen.blit(
                title,
                title.get_rect(center=(WIDTH//2, popup.y + 135))
            )
            # Divider
            pygame.draw.line(
                self.screen,
                (225, 225, 225),
                (popup.x + 40, popup.y + 160),
                (popup.right - 40, popup.y + 160),
                2
            )
                        
            self.resume_button.rect.center = (
                WIDTH // 2,
                popup.y + 220 + int(self.pause_buttons_offset)
            )

            self.pause_reset_button.rect.center = (
                WIDTH // 2,
                popup.y + 300 + int(self.pause_buttons_offset)
            )

            self.pause_new_button.rect.center = (
                WIDTH // 2,
                popup.y + 380 + int(self.pause_buttons_offset)
            )

            self.resume_button.draw(self.screen)
            self.pause_reset_button.draw(self.screen)
            self.pause_new_button.draw(self.screen)

        pygame.display.flip()

    def new_game(self, difficulty):
        self.difficulty = difficulty.lower()

        self.logic = SudokuLogic(
            self.difficulty
        )

        self.logic.difficulty = self.difficulty.capitalize()

        self.board.logic = self.logic

        self.board.display_score = 0

    def run(self):

        while self.running:

            self.clock.tick(FPS)

            self.handle_events()

            self.draw()

        pygame.quit()
