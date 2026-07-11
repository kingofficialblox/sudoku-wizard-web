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
        board_bottom = BOARD_Y + CELL_SIZE * 9
        keypad_y = board_bottom + 20
        button_y1 = keypad_y + 60
        button_y2 = button_y1 + 60

        button_width = 140
        button_height = 48
        gap = 15

        # ---------- First Row ----------
        start_x = (WIDTH - (5 * button_width + 4 * gap)) // 2

        self.new_game_button = Button(start_x, button_y1, button_width, button_height, "New")

        self.restart_button = Button(start_x + (button_width + gap) * 1,
                                     button_y1,
                                     button_width,
                                     button_height,
                                     "Restart")

        self.undo_button = Button(start_x + (button_width + gap) * 2,
                                  button_y1,
                                  button_width,
                                  button_height,
                                  "Undo")

        self.hint_button = Button(start_x + (button_width + gap) * 3,
                                  button_y1,
                                  button_width,
                                  button_height,
                                  "Hint")

        self.solve_button = Button(start_x + (button_width + gap) * 4,
                                   button_y1,
                                   button_width,
                                   button_height,
                                   "Solve")

        # ---------- Second Row ----------
        difficulty_width = 140

        difficulty_start = (WIDTH - (3 * difficulty_width + 2 * gap)) // 2

        self.easy_button = Button(
            difficulty_start,
            button_y2,
            difficulty_width,
            button_height,
            "Easy"
        )

        self.medium_button = Button(
            difficulty_start + difficulty_width + gap,
            button_y2,
            difficulty_width,
            button_height,
            "Medium"
        )

        self.hard_button = Button(
            difficulty_start + (difficulty_width + gap) * 2,
            button_y2,
            difficulty_width,
            button_height,
            "Hard"
        )
        # -------- Number Buttons --------

        self.number_buttons = []

        key_width = 70
        key_height = 50
        gap = 10

        start_x = (WIDTH - (9 * key_width + 8 * gap)) // 2
        start_y = keypad_y

        for i in range(9):
            self.number_buttons.append(
                Button(
                    start_x + i * (key_width + gap),
                    start_y,
                    key_width,
                    key_height,
                    str(i + 1)
                )
            )
        

        self.running = True

        self.difficulty = "medium"

        self.notes_mode = False
        # ---------- Popup Icons ----------

        self.new_icon = pygame.image.load(
            "assets/images/new_game.png"
        ).convert_alpha()

        self.exit_icon = pygame.image.load(
            "assets/images/exit.png"
        ).convert_alpha()

        self.new_icon = pygame.transform.smoothscale(
            self.new_icon,
            (30, 30)
        )

        self.exit_icon = pygame.transform.smoothscale(
            self.exit_icon,
            (30, 30)
        )
        # ---------- Win Popup Buttons ----------

        self.popup_new_button = Button(
            WIDTH//2 - 170,
            HEIGHT//2 + 150,
            183,
            50,
            "NEW GAME",
            self.new_icon
        )

        self.popup_exit_button = Button(
            WIDTH//2 + 20,
            HEIGHT//2 + 150,
            170,
            50,
            "EXIT",
            self.exit_icon
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

            for _ in range(20):
                self.confetti.append(Confetti())

            self.previous_win_state = True

        elif not self.logic.game_won:
            self.previous_win_state = False

        # Draw the Sudoku board
        self.board.draw(self.screen)
        # ---------- Draw Confetti ----------
        if self.logic.game_won:

            # Keep spawning new confetti
            import random
            for _ in range(random.randint(3, 8)):
                self.confetti.append(Confetti())

            # Update & draw
            for particle in self.confetti:
                particle.update()
                particle.draw(self.screen)

            # Remove particles that leave the screen
            self.confetti = [
                particle
                for particle in self.confetti
                if particle.y < HEIGHT + 100
            ]
            if len(self.confetti) > 350:
                self.confetti = self.confetti[-350:]

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
        self.difficulty = difficulty
        self.logic = SudokuLogic(difficulty)
        self.board.logic = self.logic
        self.logic.game_won = False
        

    def run(self):

        while self.running:

            self.clock.tick(FPS)

            self.handle_events()

            self.draw()

        pygame.quit()
