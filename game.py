import pygame

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

        self.solve_icon = pygame.image.load(
            "assets/images/solve.png"
        ).convert_alpha()

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

        self.solve_icon = pygame.transform.smoothscale(
            self.solve_icon,
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
            "New",
            self.new_icon,
            bg_color=(255,255,255),
            hover_color=(245,248,255)
        )

        self.restart_button = Button(
            start_x,
            button_y1 + 70,
            button_width,
            button_height,
            "Reset",
            self.restart_icon,
            bg_color=(255,255,255),
            hover_color=(245,248,255)
        )

        self.undo_button = Button(
            start_x,
            button_y1 + 140,
            button_width,
            button_height,
            "Undo",
            self.undo_icon,
            bg_color=(255,255,255),
            hover_color=(245,248,255)
        )

        self.hint_button = Button(
            start_x,
            button_y1 + 210,
            button_width,
            button_height,
            "Hint",
            self.hint_icon,
            bg_color=(255,255,255),
            hover_color=(245,248,255)
        )

        self.solve_button = Button(
            start_x,
            button_y1 + 280,
            button_width,
            button_height,
            "Solve",
            self.solve_icon,
            bg_color=(255,255,255),
            hover_color=(245,248,255)
        )

        # ---------- Second Row ----------
        difficulty_width = 140

        difficulty_start = (WIDTH - (3 * difficulty_width + 2 * gap)) // 2

        self.easy_button = Button(
            difficulty_start,
            button_y2,
            difficulty_width,
            button_height,
            "Easy",
            bg_color=(52, 152, 219),
            hover_color=(90, 185, 255)
        )

        self.medium_button = Button(
            difficulty_start + difficulty_width + gap,
            button_y2,
            difficulty_width,
            button_height,
            "Medium",
            bg_color=(243, 156, 18),
            hover_color=(255, 190, 50)
        )

        self.hard_button = Button(
            difficulty_start + (difficulty_width + gap) * 2,
            button_y2,
            difficulty_width,
            button_height,
            "Hard",
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
                pos = pygame.mouse.get_pos()

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
                    self.new_game("Easy")

                elif self.medium_button.clicked(pos):
                    self.click_sound.play()
                    self.new_game("Medium")

                elif self.hard_button.clicked(pos):
                    self.click_sound.play()
                    self.new_game("Hard")

                elif self.hint_button.clicked(pos):
                    self.click_sound.play()
                    self.hint_sound.play()
                    self.logic.give_hint()

                elif self.undo_button.clicked(pos):
                    self.click_sound.play()
                    self.logic.undo()

                elif self.solve_button.clicked(pos):
                    self.click_sound.play()
                    self.logic.solve()

                elif self.restart_button.clicked(pos):
                    self.click_sound.play()
                    self.logic.restart()
                    self.board.display_score = 0

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
        if not self.logic.game_won:

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
            self.solve_button.draw(self.screen)

            self.easy_button.draw(self.screen)
            self.medium_button.draw(self.screen)
            self.hard_button.draw(self.screen)

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
