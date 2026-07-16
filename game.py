import pygame
import time

from constants import *
from board import Board
from sudoku_logic import SudokuLogic
from button import Button
from confetti import Confetti
from themes import LIGHT, DARK

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
        self.theme = LIGHT

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
        self.settings_icon = pygame.image.load(
            "assets/images/settings.png"
        ).convert_alpha()
        self.theme_icon = pygame.image.load(
            "assets/images/theme.png"
        ).convert_alpha()

        self.theme_icon = pygame.transform.smoothscale(
            self.theme_icon,
            (32, 32)
        )

        self.resume_icon = pygame.image.load(
            "assets/images/resume.png"
        ).convert_alpha()
        self.pause_popup_icon = pygame.image.load(
            "assets/images/pause.png"
        ).convert_alpha()
        self.music_icon = pygame.image.load(
            "assets/images/music.png"
        ).convert_alpha()

        self.sfx_icon = pygame.image.load(
            "assets/images/sfx.png"
        ).convert_alpha()
        self.close_icon = pygame.image.load(
            "assets/images/close.png"
        ).convert_alpha()
        

        self.close_icon = pygame.transform.smoothscale(
            self.close_icon,
            (50, 50)
        )
        self.close_rect = self.close_icon.get_rect()

        self.music_icon = pygame.transform.smoothscale(
            self.music_icon,
            (28, 28)
        )

        self.sfx_icon = pygame.transform.smoothscale(
            self.sfx_icon,
            (28, 28)
        )

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
        self.settings_icon = pygame.transform.smoothscale(
            self.settings_icon,
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
        self.settings_open = False
        self.settings_popup_scale = 0.85
        self.settings_overlay_alpha = 0
        self.settings_buttons_offset = 25
        self.music_on = True
        self.sfx_on = True
        self.music_volume = 0.30
        self.sfx_volume = 0.45

        self.drag_music = False
        self.drag_sfx = False
        self.last_sfx_preview = 0
        self.sfx_preview_delay = 120
        self.music_slider = pygame.Rect(0, 0, 300, 6)
        self.sfx_slider = pygame.Rect(0, 0, 300, 6)

        
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
            42,
            42
        )
        # ---------- Settings Button ----------
        self.settings_button = pygame.Rect(
            WIDTH - 75,
            270,
            42,
            42
        )
        self.settings_hover = False
        self.settings_scale = 1.0
        self.settings_pressed = False
        self.pause_hover = False
        self.pause_scale = 1.0
        self.pause_pressed = False
        self.pause_buttons_offset = 25
        self.win_buttons_offset = 120
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
        self.pause_exit_button = Button(
            WIDTH//2 - 130,
            HEIGHT//2 + 195,
            260,
            60,
            "EXIT",
            self.exit_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        # ---------- Settings Popup Buttons ----------
        self.theme_button = Button(
            WIDTH//2 - 130,
            HEIGHT//2 + 50,
            260,
            60,
            "CHANGE THEME",
            icon=self.theme_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        self.close_button = Button(
            0,
            0,
            32,
            32,
            ""
        )    
        
        # ---------- Background Music ----------
        pygame.mixer.music.load(
            "assets/sounds/background.mp3"
        )
        self.music_normal_volume = 0.25
        self.music_win_volume = 0.10
        pygame.mixer.music.set_volume(
            self.music_normal_volume
        )
        pygame.mixer.music.set_volume(0.25)

        pygame.mixer.music.play(-1, fade_ms=2000)
        # ---------- Sounds ----------

        self.click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
        self.correct_sound = pygame.mixer.Sound("assets/sounds/correct.wav")
        self.wrong_sound = pygame.mixer.Sound("assets/sounds/wrong.wav")
        self.hint_sound = pygame.mixer.Sound("assets/sounds/hint.wav")
        self.win_sound = pygame.mixer.Sound("assets/sounds/win.wav")

        # Volume
        pygame.mixer.music.set_volume(self.music_volume)
        self.click_sound.set_volume(self.sfx_volume)
        self.correct_sound.set_volume(self.sfx_volume)
        self.wrong_sound.set_volume(self.sfx_volume)
        self.hint_sound.set_volume(self.sfx_volume)
        self.win_sound.set_volume(self.sfx_volume)
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
                pygame.mixer.music.fadeout(800)
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.drag_music = False
                self.drag_sfx = False

                pos = event.pos

                self.pause_pressed = False
                self.settings_pressed = False
                

                # -------------------------------------------------
                # SETTINGS POPUP
                # -------------------------------------------------

                if self.settings_open:

                    # ---------- Music Slider ----------
                    if self.music_slider.collidepoint(pos):
                        self.drag_music = True

                    # ---------- SFX Slider ----------
                    elif self.sfx_slider.collidepoint(pos):
                        self.drag_sfx = True
                    elif self.theme_button.clicked(pos):

                        

                        self.play_sound(self.click_sound)

                        if self.theme == LIGHT:
                            
                            self.theme = DARK
                        else:
                            
                            self.theme = LIGHT

                    # ---------- Close ----------
                    
                    elif self.close_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.settings_open = False

                    continue

                # -------------------------------------------------
                # PAUSE POPUP
                # -------------------------------------------------

                if self.paused:

                    if self.resume_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.logic.resume()
                        self.paused = False

                    elif self.pause_reset_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.logic.restart()
                        self.logic.resume()
                        self.paused = False

                    elif self.pause_new_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.new_game(self.logic.difficulty)
                        self.paused = False

                    elif self.pause_exit_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        pygame.mixer.music.fadeout(800)
                        self.running = False

                    continue
                
                # -------------------------------------------------
                # WIN POPUP
                # -------------------------------------------------

                if self.logic.game_won:

                    if self.popup_new_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.new_game(self.logic.difficulty)

                    elif self.popup_exit_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        pygame.mixer.music.fadeout(800)
                        self.running = False

                    continue

                # -------------------------------------------------
                # TOP ICONS
                # -------------------------------------------------

                if self.pause_button.collidepoint(pos):

                    self.pause_pressed = True
                    self.play_sound(self.click_sound)

                    self.logic.pause()
                    self.paused = True

                    self.pause_popup_scale = 0.85
                    self.pause_overlay_alpha = 0

                    continue

                if self.settings_button.collidepoint(pos):

                    self.settings_pressed = True
                    self.play_sound(self.click_sound)

                    self.settings_open = True

                    self.settings_popup_scale = 0.85
                    self.settings_overlay_alpha = 0
                    self.settings_buttons_offset = 25

                    continue

                # -------------------------------------------------
                # SIDE BUTTONS
                # -------------------------------------------------

                if self.new_game_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.new_game(self.logic.difficulty)

                elif self.restart_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.logic.restart()
                    self.board.display_score = 0

                elif self.undo_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.logic.undo()

                elif self.hint_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.play_sound(self.hint_sound)
                    self.logic.give_hint()

                elif self.exit_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    pygame.mixer.music.fadeout(800)
                    self.running = False

                elif self.easy_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.new_game("EASY")

                elif self.medium_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.new_game("MEDIUM")

                elif self.hard_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.new_game("HARD")

                else:

                    number_clicked = False

                    for i, button in enumerate(self.number_buttons):

                        if button.clicked(pos):

                            number_clicked = True

                            number = i + 1

                            # If a selected cell exists and it is EMPTY,
                            # place the number normally.
                            if (
                                self.logic.selected is not None
                                and self.logic.grid[
                                    self.logic.selected[0]
                                ][
                                    self.logic.selected[1]
                                ] == 0
                            ):
                                result = self.logic.place_number(
                                    number,
                                    self.notes_mode
                                )

                            else:
                                # Only highlight this number.
                                self.logic.selected = None
                                self.logic.highlight_number = number
                                result = None

                            if result == "WIN":
                                self.play_sound(self.correct_sound)
                                self.play_sound(self.win_sound)

                            elif result is True:
                                self.play_sound(self.correct_sound)

                            elif result is False:
                                self.play_sound(self.wrong_sound)

                            break

                            if result == "WIN":
                                self.play_sound(self.correct_sound)
                                self.play_sound(self.win_sound)

                            elif result is True:
                                self.play_sound(self.correct_sound)

                            elif result is False:
                                self.play_sound(self.wrong_sound)

                            break

                    if not number_clicked:
                        self.board.select(pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.drag_music = False
                self.drag_sfx = False
            elif event.type == pygame.MOUSEMOTION:

                if self.drag_music:

                        x = max(
                            self.music_slider.left,
                            min(event.pos[0], self.music_slider.right)
                        )

                        self.music_volume = max(
                            0,
                            min(
                                1,
                                (x - self.music_slider.left)
                                / self.music_slider.width
                            )
                        )

                        pygame.mixer.music.set_volume(self.music_volume)

                if self.drag_sfx:

                    x = max(
                        self.sfx_slider.left,
                        min(event.pos[0], self.sfx_slider.right)
                    )

                    self.sfx_volume = max(
                        0,
                        min(
                            1,
                            (x - self.sfx_slider.left) / self.sfx_slider.width
                        )
                    )

                    self.click_sound.set_volume(self.sfx_volume)
                    self.correct_sound.set_volume(self.sfx_volume)
                    self.wrong_sound.set_volume(self.sfx_volume)
                    self.hint_sound.set_volume(self.sfx_volume)
                    self.win_sound.set_volume(self.sfx_volume)
                    now = pygame.time.get_ticks()

                    if now - self.last_sfx_preview >= self.sfx_preview_delay:
                        self.play_sound(self.click_sound)
                        self.last_sfx_preview = now

                        

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
                        self.play_sound(self.correct_sound)
                        self.play_sound(self.win_sound)

                    elif result is True:
                        self.play_sound(self.correct_sound)

                    elif result is False:
                        self.play_sound(self.wrong_sound)

                elif event.key == pygame.K_UP:
                    self.logic.move_selection(-1, 0)

                elif event.key == pygame.K_DOWN:
                    self.logic.move_selection(1, 0)

                elif event.key == pygame.K_LEFT:
                    self.logic.move_selection(0, -1)

                elif event.key == pygame.K_RIGHT:
                    self.logic.move_selection(0, 1)
            


    def draw(self):
        self.screen.fill(self.theme["background"])
        mouse_pos = pygame.mouse.get_pos()
        self.pause_hover = self.pause_button.collidepoint(mouse_pos)
        self.settings_hover = self.settings_button.collidepoint(mouse_pos)
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
        self.board.draw(
            self.screen,
            self.theme
        )
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

        size = int(52 * self.pause_scale)

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
        # ---------- Settings Button Animation ----------
        target_scale = 1.0
        if self.settings_hover:
            target_scale = 1.12
        if self.settings_pressed:
            target_scale = 0.90
        self.settings_scale += (
            target_scale - self.settings_scale
        ) * 0.22
        size = int(52 * self.settings_scale)
        icon = pygame.transform.smoothscale(
            self.settings_icon,
            (size, size)
        )
        rect = icon.get_rect(
            center=self.settings_button.center
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
        if self.settings_hover:
            glow = pygame.Surface(
                (size + 30, size + 30),
                pygame.SRCALPHA
            )
            pygame.draw.circle(
                glow,
                (120,120,120,45),
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
        
        # Draw buttons only if the game hasn't been won
        if not self.logic.game_won and not self.paused:
            # ---------- Update Button Theme ----------
            for b in (
                self.new_game_button,
                self.restart_button,
                self.undo_button,
                self.hint_button,
                self.exit_button,
            ):
                b.bg_color = self.theme["button"]
                b.hover_color = self.theme["button_hover"]
            for i, button in enumerate(self.number_buttons):
                button.bg_color = self.theme["button"]
                button.hover_color = self.theme["button_hover"]
                button.text_color = self.theme["text"]
                button.border_color = self.theme["grid"]
                number = i + 1

                button.count = self.logic.remaining_count(number)

                button.selected = (
                    self.logic.highlight_number == number
                )

                button.draw(self.screen)
            for b in (
                self.new_game_button,
                self.restart_button,
                self.undo_button,
                self.hint_button,
                self.exit_button,
            ):
                b.bg_color = self.theme["button"]
                b.hover_color = self.theme["button_hover"]
                b.border_color = self.theme["grid"]
                b.text_color = self.theme["text"]

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
            popup_height = int(520 * scale)

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
                self.theme["popup"],
                popup,
                border_radius=25
            )

            # Border
            pygame.draw.rect(
                self.screen,
                self.theme["popup_border"],
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
                self.theme["text"]
            )

            self.screen.blit(
                title,
                title.get_rect(center=(WIDTH//2, popup.y + 135))
            )
            # Divider
            pygame.draw.line(
                self.screen,
                self.theme["popup_border"],
                (popup.x + 40, popup.y + 160),
                (popup.right - 40, popup.y + 160),
                2
            )
                        
            self.resume_button.rect.center = (
                WIDTH // 2,
                popup.y + 200 + int(self.pause_buttons_offset)
            )

            self.pause_reset_button.rect.center = (
                WIDTH // 2,
                popup.y + 275 + int(self.pause_buttons_offset)
            )

            self.pause_new_button.rect.center = (
                WIDTH // 2,
                popup.y + 350 + int(self.pause_buttons_offset)
            )
            self.pause_exit_button.rect.center = (
                WIDTH // 2,
                popup.y + 425 + int(self.pause_buttons_offset)
            )
            for b in (
                self.resume_button,
                self.pause_reset_button,
                self.pause_new_button,
                self.pause_exit_button,
            ):
                b.bg_color = self.theme["button"]
                b.hover_color = self.theme["button_hover"]
                b.border_color = self.theme["grid"]
                b.text_color = self.theme["text"]

            self.resume_button.draw(self.screen)
            self.pause_reset_button.draw(self.screen)
            self.pause_new_button.draw(self.screen)
            self.pause_exit_button.draw(self.screen)
        # ---------- SETTINGS POPUP ----------

        
        if self.settings_open:
            self.settings_popup_scale += (
                1 - self.settings_popup_scale
            ) * 0.22

            self.settings_buttons_offset += (
                0 - self.settings_buttons_offset
            ) * 0.18

            self.settings_overlay_alpha += (
                120 - self.settings_overlay_alpha
            ) * 0.18

            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill(
                (
                    0,
                    0,
                    0,
                    int(self.settings_overlay_alpha)
                )
            )

            self.screen.blit(overlay, (0, 0))

            scale = self.settings_popup_scale

            if scale > 0.96:
                scale = 1 + (0.96 - scale) * 0.35

            popup_width = int(500 * scale)
            popup_height = int(560 * scale)

            popup = pygame.Rect(
                WIDTH//2 - popup_width//2,
                HEIGHT//2 - popup_height//2,
                popup_width,
                popup_height
            )
            shadow = pygame.Surface(
                (popup.width + 30, popup.height + 30),
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                shadow,
                (190,195,205,120),
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

            pygame.draw.rect(
                self.screen,
                self.theme["popup"],
                popup,
                border_radius=25
            )

            pygame.draw.rect(
                self.screen,
                self.theme["popup_border"],
                popup,
                2,
                border_radius=25
            )

            # ---------- Settings Icon ----------

            circle_center = (WIDTH // 2, popup.y + 72)

            pygame.draw.circle(
                self.screen,
                self.theme["board"],
                circle_center,
                42
            )

            pygame.draw.circle(
                self.screen,
                self.theme["grid"],
                circle_center,
                2
            )

            icon_rect = self.settings_icon.get_rect(
                center=circle_center
            )

            self.screen.blit(
                self.settings_icon,
                icon_rect
            )

            # ---------- Title ----------

            title = self.board.header_font.render(
                "Settings",
                True,
                self.theme["text"]
            )

            self.screen.blit(
                title,
                title.get_rect(
                    center=(WIDTH//2, popup.y + 145)
                )
            )

            pygame.draw.line(
                self.screen,
                self.theme["grid"],
                (popup.x + 40, popup.y + 170),
                (popup.right - 40, popup.y + 170),
                2
            )
            # ---------- MUSIC ----------

            icon_size = 24

            music_y = popup.y + 195

            # Music icon
            self.screen.blit(
                self.music_icon,
                (
                    popup.x + 60,
                    music_y + (self.board.info_font.get_height() - icon_size) // 2
                )
            )

            # Music text
            music_text = self.board.info_font.render(
                "Music",
                True,
                self.theme["text"]
            )

            self.screen.blit(
                music_text,
                (popup.x + 95, music_y)
            )

            self.music_slider = pygame.Rect(
                popup.x + 60,
                popup.y + 235,
                300,
                6
            )

            music_bar = self.music_slider

            pygame.draw.rect(
                self.screen,
                self.theme["grid"],
                music_bar,
                border_radius=3
            )

            music_fill = pygame.Rect(
                music_bar.x,
                music_bar.y,
                int(300 * self.music_volume),
                6
            )

            pygame.draw.rect(
                self.screen,
                PRIMARY,
                music_fill,
                border_radius=3
            )

            music_knob_x = music_bar.x + int(300 * self.music_volume)

            pygame.draw.circle(
                self.screen,
                self.theme["board"],
                (music_knob_x, music_bar.centery),
                10
            )

            pygame.draw.circle(
                self.screen,
                self.theme["text"],
                (music_knob_x, music_bar.centery),
                10,
                2
            )

            music_percent = self.board.info_font.render(
                f"{int(self.music_volume * 100)}%",
                True,
                self.theme["text"]
            )

            self.screen.blit(
                music_percent,
                (music_bar.right + 18, music_bar.centery - music_percent.get_height() // 2)
            )

            self.music_slider = music_bar

            self.music_slider = music_bar
            
            # ---------- SFX ----------

            icon_size = 24

            sfx_y = popup.y + 285

            # SFX icon
            self.screen.blit(
                self.sfx_icon,
                (
                    popup.x + 60,
                    sfx_y + (self.board.info_font.get_height() - icon_size) // 2
                )
            )

            # SFX text
            sfx_text = self.board.info_font.render(
                "Sound Effects",
                True,
                self.theme["text"]
            )

            self.screen.blit(
                sfx_text,
                (popup.x + 95, sfx_y)
            )

            self.sfx_slider = pygame.Rect(
                popup.x + 60,
                popup.y + 325,
                300,
                6
            )

            sfx_bar = self.sfx_slider

            pygame.draw.rect(
                self.screen,
                self.theme["grid"],
                sfx_bar,
                border_radius=3
            )

            sfx_fill = pygame.Rect(
                sfx_bar.x,
                sfx_bar.y,
                int(300 * self.sfx_volume),
                6
            )

            pygame.draw.rect(
                self.screen,
                PRIMARY,
                sfx_fill,
                border_radius=3
            )

            sfx_knob_x = sfx_bar.x + int(300 * self.sfx_volume)

            pygame.draw.circle(
                self.screen,
                self.theme["board"],
                (sfx_knob_x, sfx_bar.centery),
                10
            )

            pygame.draw.circle(
                self.screen,
                self.theme["text"],
                (sfx_knob_x, sfx_bar.centery),
                10,
                2
            )

            sfx_percent = self.board.info_font.render(
                f"{int(self.sfx_volume * 100)}%",
                True,
                self.theme["text"]
            )

            self.screen.blit(
                sfx_percent,
                (sfx_bar.right + 18, sfx_bar.centery - sfx_percent.get_height() // 2)
            )

            self.sfx_slider = sfx_bar

            self.sfx_slider = sfx_bar
            self.theme_button.rect.center = (
                WIDTH//2,
                popup.y + 395
            )
            self.theme_button.bg_color = self.theme["button"]
            self.theme_button.hover_color = self.theme["button_hover"]
            for b in (
                self.theme_button,
            ):
                b.bg_color = self.theme["button"]
                b.hover_color = self.theme["button_hover"]
                b.border_color = self.theme["grid"]
                b.text_color = self.theme["text"]
                # ---------- Close (X) ----------

                self.close_button.rect.topleft = (
                    popup.right - 44,
                    popup.y + 12
                )

                self.close_button.bg_color = self.theme["button"]
                self.close_button.hover_color = self.theme["button_hover"]
                self.close_button.border_color = self.theme["grid"]
                self.screen.blit(
                    self.close_icon,
                    (
                        popup.right - 62,
                        popup.y + 14
                    )
                )
                mouse = pygame.mouse.get_pos()

                if self.close_rect.collidepoint(mouse):

                    glow = pygame.Surface(
                        (
                            self.close_rect.width + 18,
                            self.close_rect.height + 18
                        ),
                        pygame.SRCALPHA
                    )

                    pygame.draw.circle(
                        glow,
                        (*self.theme["text"], 45),
                        glow.get_rect().center,
                        glow.get_width() // 2
                    )

                    self.screen.blit(
                        glow,
                        (
                            self.close_rect.x - 9,
                            self.close_rect.y - 9
                        )
                    )
                self.screen.blit(
                    self.close_icon,
                    self.close_rect
                )

                rect = self.close_button.rect

                
                

                

                mouse = pygame.mouse.get_pos()

                hover = self.close_button.rect.collidepoint(mouse)

                

                

            self.theme_button.draw(self.screen)            
            
            
            
            
            
            
        # ---------- WIN POPUP BUTTONS ----------
        if self.logic.game_won:
            self.win_buttons_offset += (
                0 - self.win_buttons_offset
            ) * 0.18
            self.popup_new_button.rect.center = (
                WIDTH//2 - 120,
                HEIGHT//2 + 360 + int(self.win_buttons_offset)
            )
            self.popup_exit_button.rect.center = (
                WIDTH//2 + 120,
                HEIGHT//2 + 360 + int(self.win_buttons_offset)
            )
            self.popup_new_button.draw(self.screen)
            self.popup_exit_button.draw(self.screen)
        # ---------- Dynamic Music Volume ----------
        current = pygame.mixer.music.get_volume()
        if self.logic.game_won:
            target = self.music_win_volume
        else:
            target = self.music_volume
        if abs(current-target) < 0.01:
            current = target
        else:
            current += (target-current)*0.06
        pygame.mixer.music.set_volume(current)

        pygame.display.flip()
        # ---------- Win Popup Buttons ----------
        if self.logic.game_won:

            self.win_buttons_offset += (
                0 - self.win_buttons_offset
            ) * 0.18

            self.popup_new_button.rect.center = (
                WIDTH // 2 - 120,
                HEIGHT // 2 + 335 + int(self.win_buttons_offset)
            )

            self.popup_exit_button.rect.center = (
                WIDTH // 2 + 120,
                HEIGHT // 2 + 335 + int(self.win_buttons_offset)
            )

            self.popup_new_button.draw(self.screen)
            self.popup_exit_button.draw(self.screen)
    def play_sound(self, sound):

        if self.sfx_on:
            sound.play()
    def new_game(self, difficulty):
        self.win_buttons_offset = 60
        self.difficulty = difficulty.lower()

        self.logic = SudokuLogic(
            self.difficulty
        )

        self.logic.difficulty = self.difficulty.capitalize()

        self.board.logic = self.logic

        self.board.display_score = 0
        self.win_buttons_offset = 120
        pygame.mixer.music.set_volume(
            self.music_normal_volume
        )

    def run(self):

        while self.running:

            self.clock.tick(FPS)

            self.handle_events()

            self.draw()

        pygame.quit()
