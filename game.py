import pygame
import time
import json
import os
import math

from constants import *
from board import Board
from sudoku_logic import SudokuLogic
from button import Button
from confetti import Confetti
from themes import LIGHT, DARK
from menu import Menu
from settings_menu import SettingsMenu
from stats_manager import StatsManager
from stats_menu import StatsMenu
class Game:

    def __init__(self):

        # Pydroid's runner prepares SDL through pygame.init(); unlike a direct
        # pygame.display.init() call, this correctly marks SDL as main-ready.
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption("Sudoku Wizard")

        # Android requires a display before attempting to start audio.
        self.audio_available = True
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(
                    frequency=44100,
                    size=-16,
                    channels=2,
                    buffer=512,
                )
            except pygame.error as error:
                print("Audio disabled:", error)
                self.audio_available = False

        self.clock = pygame.time.Clock()

        self.logic = SudokuLogic()
        self.theme = LIGHT
        self.load_settings()
        

        self.board = Board(self.logic)
        self.current_screen = "splash"
        self.game_started = False
        self.menu = Menu(self)
        self.settings_menu = SettingsMenu(self)
        self.stats = StatsManager()
        self.stats_menu = StatsMenu(self)
        self.stats_open = False
        self.match_recorded = False
        # ---------- Popup Icons ----------

        self.game_logo = pygame.image.load(
            "assets/images/game_logo.png"
        ).convert_alpha()
        self.lost_image = pygame.image.load(
            "assets/images/lost.png"
        ).convert_alpha()
        self.game_over_background = pygame.transform.smoothscale(
            pygame.image.load("assets/images/gameover.png").convert(),
            (WIDTH, HEIGHT)
        )
        self.game_over_panel_fade = pygame.transform.smoothscale(
            self.game_over_background, (650, 640)
        )
        self.game_over_panel_fade.set_alpha(32)

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
        self.menu_icon = pygame.image.load(
            "assets/images/menu.png"
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

        self.exit_icon = pygame.transform.smoothscale(
            self.exit_icon,
            (30, 30)
        )

        self.restart_icon = pygame.transform.smoothscale(
            self.restart_icon,
            (30, 30)
        )

        side_icon_size = 70 if PORTRAIT_MODE else 56
        self.undo_icon = pygame.transform.smoothscale(
            self.undo_icon,
            (side_icon_size, side_icon_size)
        )
        self.game_logo = pygame.transform.smoothscale(self.game_logo, (260, 260))
        self.lost_image = pygame.transform.smoothscale(self.lost_image, (190, 190))

        self.hint_icon = pygame.transform.smoothscale(
            self.hint_icon,
            (side_icon_size, side_icon_size)
        )               
        self.menu_icon = pygame.transform.smoothscale(
            self.menu_icon,
            (side_icon_size, side_icon_size)
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
        
        
        
        
        icon_button_size = 70 if PORTRAIT_MODE else 60
        icon_button_x = start_x
        # On desktop the side actions follow the score, time and mistakes
        # cards; portrait keeps them beside the board for touch-friendly room.
        icon_button_y = BOARD_Y + 150 if PORTRAIT_MODE else BOARD_Y + 360

        self.undo_button = Button(
            icon_button_x,
            icon_button_y + (85 if PORTRAIT_MODE else 70),
            icon_button_size,
            icon_button_size,
            "",
            self.undo_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )

        self.hint_button = Button(
            icon_button_x,
            icon_button_y,
            icon_button_size,
            icon_button_size,
            "",
            self.hint_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        self.board_menu_button = Button(
            icon_button_x,
            icon_button_y + (170 if PORTRAIT_MODE else 140),
            icon_button_size,
            icon_button_size,
            "",
            self.menu_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        # -------- Number Buttons --------

        self.number_buttons = []

        key_width = 55 if PORTRAIT_MODE else 75
        key_height = 55
        gap = 12

        start_x = BOARD_X - 100
        start_y = BOARD_Y + 10

        for i in range(9):
            if PORTRAIT_MODE:
                key_x = WIDTH // 2 - (key_width * 3 + gap * 2) // 2 + (i % 3) * (key_width + gap)
                key_y = BOARD_Y + CELL_SIZE * 9 + 35 + (i // 3) * (key_height + gap)
            else:
                key_x = start_x
                key_y = start_y + i * (key_height + gap)
            self.number_buttons.append(
                Button(
                    key_x,
                    key_y,
                    key_width,
                    key_height,
                    str(i + 1)
                )
            )

        self.running = True
        self.splash_started = pygame.time.get_ticks()
        self.splash_exiting = False
        self.splash_exit_started = 0
        self.paused = False
        self.pause_popup_scale = 0.85
        self.pause_overlay_alpha = 0
        self.settings_open = False
        self.settings_popup_scale = 0.85
        self.settings_overlay_alpha = 0
        self.settings_buttons_offset = 25
        self.music_on = True
        self.sfx_on = True
        

        self.drag_music = False
        self.drag_sfx = False
        self.last_sfx_preview = 0
        self.sfx_preview_delay = 120
        self.music_slider = pygame.Rect(0, 0, 300, 6)
        self.sfx_slider = pygame.Rect(0, 0, 300, 6)

        
        self.notes_mode = False
        

        # ---------- Win Popup Buttons ----------

        self.popup_new_button = Button(
            0,
            0,
            160,
            62,
            "NEW GAME",
            bg_color=(46, 204, 113),
            hover_color=(72, 230, 140)
        )
        self.popup_menu_button = Button(
            0,
            0,
            160,
            62,
            "MAIN MENU",
            bg_color=(241, 196, 15),
            hover_color=(255, 218, 68)
        )
        self.popup_exit_button = Button(
            0,
            0,
            160,
            62,
            "EXIT",
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
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        # ---------- Pause Popup Buttons ----------
        self.pause_reset_button = Button(
            WIDTH//2 - 130,HEIGHT//2 + 25,
            260,
            60,
            "RESET",
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        self.pause_new_button = Button(
            WIDTH//2 - 130,
            HEIGHT//2 + 110,
            260,
            60,
            "NEW",
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        self.pause_menu_button = Button(
            WIDTH//2 - 130,
            HEIGHT//2 + 195,
            260,
            60,
            "MENU",
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        # ---------- Settings Popup Buttons ----------
        self.theme_button = Button(
            WIDTH//2 - 130,
            HEIGHT//2 + 50,
            310,
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
        self.play_button = Button(
            WIDTH//2 - 140,
            430,
            280,
            65,
            "PLAY"
        )

        self.menu_settings_button = Button(
            WIDTH//2 - 140,
            515,
            280,
            65,
            "SETTINGS"
        )

        self.menu_exit_button = Button(
            WIDTH//2 - 140,
            600,
            280,
            65,
            "EXIT"
)    
        
        # ---------- Background Music ----------
        self.current_music_track = "background"
        self.music_normal_volume = self.music_volume
        self.music_win_volume = 0.10

        if self.audio_available:
            try:
                pygame.mixer.music.load("assets/sounds/background.mp3")
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1, fade_ms=2000)
                self.click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
                self.correct_sound = pygame.mixer.Sound("assets/sounds/correct.wav")
                self.wrong_sound = pygame.mixer.Sound("assets/sounds/wrong.wav")
                self.hint_sound = pygame.mixer.Sound("assets/sounds/hint.wav")
                self.win_sound = pygame.mixer.Sound("assets/sounds/win.wav")
                self.lose_sound = pygame.mixer.Sound("assets/sounds/loose.wav")
                for sound in (self.click_sound, self.correct_sound, self.wrong_sound,
                              self.hint_sound, self.win_sound, self.lose_sound):
                    sound.set_volume(self.sfx_volume)
            except pygame.error as error:
                print("Audio disabled:", error)
                self.audio_available = False

        if not self.audio_available:
            self.click_sound = None
            self.correct_sound = None
            self.wrong_sound = None
            self.hint_sound = None
            self.win_sound = None
            self.lose_sound = None
        # ---------- Confetti ----------
        self.confetti = []
        self.previous_win_state = False
        self.previous_game_over_state = False
    def save_settings(self):
        data = {
            "music": self.music_volume,
            "sfx": self.sfx_volume,
            "theme": "dark" if self.theme == DARK else "light"
        }

        try:
            with open("settings.json", "w") as f:
                json.dump(data, f, indent=4)
        except OSError as error:
            print("Settings could not be saved:", error)


    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                data = json.load(f)

            self.theme = DARK if data.get("theme") == "dark" else LIGHT

            self.music_volume = data.get("music", 0.5)
            self.sfx_volume = data.get("sfx", 0.5)

        except:
            self.theme = LIGHT
            self.music_volume = 0.5
            self.sfx_volume = 0.5

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
            # Android/iOS report normalized finger coordinates; convert them
            # into the same logical positions used by desktop mouse handlers.
            finger_events = tuple(
                value for value in (
                    getattr(pygame, "FINGERDOWN", None),
                    getattr(pygame, "FINGERUP", None),
                    getattr(pygame, "FINGERMOTION", None),
                ) if value is not None
            )
            if event.type in finger_events:
                event_type = {
                    getattr(pygame, "FINGERDOWN", None): pygame.MOUSEBUTTONDOWN,
                    getattr(pygame, "FINGERUP", None): pygame.MOUSEBUTTONUP,
                    getattr(pygame, "FINGERMOTION", None): pygame.MOUSEMOTION,
                }[event.type]
                event = pygame.event.Event(
                    event_type,
                    {"pos": (int(event.x * WIDTH), int(event.y * HEIGHT)), "button": 1}
                )

            if event.type == pygame.QUIT:
                self.running = False
                continue

            if self.current_screen == "splash":
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                    if not self.splash_exiting:
                        self.splash_exiting = True
                        self.splash_exit_started = pygame.time.get_ticks()
                continue

            if self.settings_open:
                self.settings_menu.handle_event(event)
                continue

            if self.stats_open:
                self.stats_menu.handle_event(event)
                continue

            if self.current_screen == "menu":
                self.menu.handle_event(event)
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.drag_music = False
                self.drag_sfx = False

                pos = event.pos

                self.pause_pressed = False
                self.settings_pressed = False
                if self.current_screen == "menu":

                    if self.play_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.current_screen = "game"

                    elif self.menu_settings_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.settings_open = True

                    elif self.menu_exit_button.clicked(pos):
                        self.fade_out_music(500)
                        self.running = False

                    continue
                

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
                        self.save_settings()

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

                    elif self.pause_menu_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.paused = False
                        self.current_screen = "menu"
                        self.menu.choose_difficulty = False
                        self.play_menu_music()

                    continue
                
                # -------------------------------------------------
                # WIN POPUP
                # -------------------------------------------------

                if self.logic.game_won or self.logic.game_over:

                    if self.popup_new_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.new_game(self.logic.difficulty)

                    elif self.popup_exit_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.fade_out_music(800)
                        self.running = False

                    elif self.popup_menu_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.game_started = False
                        self.current_screen = "menu"
                        self.menu.choose_difficulty = False
                        self.play_menu_music()

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

                if self.undo_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.logic.undo()

                elif self.hint_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.play_sound(self.hint_sound)
                    self.logic.give_hint()

                elif self.board_menu_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.logic.pause()
                    self.current_screen = "menu"
                    self.menu.choose_difficulty = False
                    self.play_menu_music()

                else:

                    number_clicked = False

                    for i, button in enumerate(self.number_buttons):

                        if button.clicked(pos):

                            number_clicked = True
                            self.play_sound(self.click_sound)

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
                                self.record_match(True)

                            elif result is True:
                                self.play_sound(self.correct_sound)

                            elif result is False or result == "GAME_OVER":
                                self.play_sound(self.wrong_sound)
                                if result == "GAME_OVER":
                                    self.record_match(False)

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

                        if self.audio_available:
                            pygame.mixer.music.set_volume(self.music_volume)
                        self.save_settings()

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

                    self.set_sfx_volume(self.sfx_volume)
                    self.save_settings()
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
                        self.record_match(True)

                    elif result is True:
                        self.play_sound(self.correct_sound)

                    elif result is False or result == "GAME_OVER":
                        self.play_sound(self.wrong_sound)
                        if result == "GAME_OVER":
                            self.record_match(False)

                elif event.key == pygame.K_UP:
                    self.logic.move_selection(-1, 0)

                elif event.key == pygame.K_DOWN:
                    self.logic.move_selection(1, 0)

                elif event.key == pygame.K_LEFT:
                    self.logic.move_selection(0, -1)

                elif event.key == pygame.K_RIGHT:
                    self.logic.move_selection(0, 1)
    def draw_menu(self):

        self.screen.fill(self.theme["background"])
        title_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            72
        )

        small_font = pygame.font.Font(
            "assets/fonts/Poppins-Regular.ttf",
            22
        )

        title = title_font.render(
            "SUDOKU",
            True,
            self.theme["text"]
        )

        wizard = title_font.render(
            "WIZARD",
            True,
            PRIMARY
        )

        self.screen.blit(
            title,
            title.get_rect(center=(WIDTH//2,160))
        )

        self.screen.blit(
            wizard,
            wizard.get_rect(center=(WIDTH//2,240))
        )

        creator = small_font.render(
            "META_CREATOR",
            True,
            self.theme["text"]
        )

        version = small_font.render(
            "Version 1.0",
            True,
            self.theme["grid"]
        )

        self.screen.blit(
            creator,
            creator.get_rect(center=(WIDTH//2,720))
        )

        self.screen.blit(
            version,
            version.get_rect(center=(WIDTH//2,750))
        )

        self.play_button.draw(self.screen)
        self.menu_settings_button.draw(self.screen)
        self.menu_exit_button.draw(self.screen)

            


    def draw(self):
        if self.current_screen == "splash":
            self.screen.fill(self.theme["background"])
            now = pygame.time.get_ticks()
            entered = min(1.0, (now - self.splash_started) / 700)
            leaving = min(1.0, (now - self.splash_exit_started) / 500) if self.splash_exiting else 0
            alpha = int(255 * entered * (1 - leaving))
            scale = 0.82 + 0.18 * entered + 0.025 * math.sin(now / 260)
            logo_size = max(1, int(300 * scale))
            logo = pygame.transform.smoothscale(self.game_logo, (logo_size, logo_size))
            logo.set_alpha(alpha)
            self.screen.blit(logo, logo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 65)))
            creator_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 32)
            creator = creator_font.render("META_CREATORS", True, self.theme["accent"])
            creator.set_alpha(alpha)
            self.screen.blit(creator, creator.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 125)))
            prompt_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 20)
            prompt = prompt_font.render("Click anywhere to continue", True, self.theme["secondary"])
            prompt.set_alpha(alpha)
            self.screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 175)))
            if self.splash_exiting and leaving >= 1:
                self.current_screen = "menu"
            pygame.display.flip()
            return

        if self.settings_open:
            self.settings_menu.draw()
            pygame.display.flip()
            return

        if self.stats_open:
            self.stats_menu.draw()
            pygame.display.flip()
            return

        if self.current_screen == "menu":

            self.menu.update()

            self.menu.draw()

            pygame.display.flip()

            return

        if self.current_screen == "menu":
            self.draw_menu()
            pygame.display.flip()
            return

        self.screen.fill(self.theme["background"])
        mouse_pos = pygame.mouse.get_pos()
        self.pause_hover = self.pause_button.collidepoint(mouse_pos)
        self.settings_hover = self.settings_button.collidepoint(mouse_pos)
        self.pause_hover = self.pause_button.collidepoint(mouse_pos)
        # ---------- End-of-game effects (each plays/spawns once) ----------
        if self.logic.game_won and not self.previous_win_state:

            self.confetti = []

            for _ in range(800):
                self.confetti.append(Confetti())

            self.previous_win_state = True

        elif not self.logic.game_won:
            self.previous_win_state = False

        if self.logic.game_over and not self.previous_game_over_state:
            self.play_sound(self.lose_sound)
            self.previous_game_over_state = True
        elif not self.logic.game_over:
            self.previous_game_over_state = False

        # Draw the Sudoku board
        self.board.draw(
            self.screen,
            self.theme
        )

        # Keep the celebration alive while the win screen is open.
        if self.logic.game_won:
            for particle in self.confetti:
                particle.update()
                particle.draw(self.screen)
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
        # -------- Soft Button Shadow --------

        shadow_size = size + 12

        shadow = pygame.Surface(
            (shadow_size, shadow_size),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            shadow,
            (0,0,0,55),
            (
                shadow_size//2,
                shadow_size//2 + 3
            ),
            size//2
        )

        shadow_rect = shadow.get_rect(
            center=rect.center
        )

        self.screen.blit(
            shadow,
            shadow_rect
        )
        pygame.draw.circle(
            self.screen,
            self.theme["popup"],
            rect.center,
            size // 2 - 3
        )
        pygame.draw.circle(
            self.screen,
            self.theme["accent"] if self.pause_hover else self.theme["popup_border"],
            rect.center,
            size // 2 - 3,
            2
        )
        if self.pause_hover:
            glow = pygame.Surface(
                (size + 18, size + 18),
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
        # -------- clean button shadow --------

        shadow = pygame.Surface(
            (size, size),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            shadow,
            (0,0,0,45),
            (
                size//2,
                size//2
            ),
            size//2 - 2
        )

        shadow_rect = shadow.get_rect(
            center=(
                rect.centerx,
                rect.centery + 5
            )
        )

        self.screen.blit(
            shadow,
            shadow_rect
        )
        pygame.draw.circle(
            self.screen,
            self.theme["popup"],
            rect.center,
            size // 2 - 3
        )
        pygame.draw.circle(
            self.screen,
            self.theme["accent"] if self.settings_hover else self.theme["popup_border"],
            rect.center,
            size // 2 - 3,
            2
        )
        if self.settings_hover:
            glow = pygame.Surface(
                (size + 18, size + 18),
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
        if not self.logic.game_won and not self.logic.game_over and not self.paused:
            # ---------- Update Button Theme ----------
            for b in (
                self.undo_button,
                self.hint_button,
                self.board_menu_button,
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
                self.undo_button,
                self.hint_button,
                self.board_menu_button,
            ):
                b.bg_color = self.theme["button"]
                b.hover_color = self.theme["button_hover"]
                b.border_color = self.theme["grid"]
                b.text_color = self.theme["text"]

            self.undo_button.draw(self.screen)
            self.hint_button.draw(self.screen)            
            self.board_menu_button.draw(self.screen)
        if self.paused:
            # Pause uses the same clean full-screen card language as Settings.
            self.screen.fill(self.theme["background"])
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
            overlay.fill((0, 0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            # Popup
            # Bounce popup animation
            scale = self.pause_popup_scale

            if scale > 0.96:
                scale = 1 + (0.96 - scale) * 0.35

            popup_width = int(620 * scale)
            popup_height = int(810 * scale)

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
                (*self.theme["shadow"], 150),
                shadow.get_rect(),
                border_radius=28
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
                border_radius=28
            )

            # Border
            pygame.draw.rect(
                self.screen,
                self.theme["popup_border"],
                popup,
                2,
                border_radius=28
            )

            
            circle_center = (WIDTH // 2, popup.y + 78)

            pygame.draw.circle(
                self.screen,
                self.theme["board"],
                circle_center,
                46
            )

            pygame.draw.circle(
                self.screen,
                self.theme["accent"],
                circle_center,
                3,
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
                title.get_rect(center=(WIDTH//2, popup.y + 150))
            )
            subtitle = self.board.info_font.render(
                "Your game is safely paused", True, self.theme["secondary"]
            )
            self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, popup.y + 185)))
            # Divider
            pygame.draw.line(
                self.screen,
                self.theme["popup_border"],
                (popup.x + 55, popup.y + 210),
                (popup.right - 55, popup.y + 210),
                2
            )
                        
            self.resume_button.rect.center = (
                WIDTH // 2,
                popup.y + 300 + int(self.pause_buttons_offset)
            )

            self.pause_reset_button.rect.center = (
                WIDTH // 2,
                popup.y + 385 + int(self.pause_buttons_offset)
            )

            self.pause_new_button.rect.center = (
                WIDTH // 2,
                popup.y + 470 + int(self.pause_buttons_offset)
            )
            self.pause_menu_button.rect.center = (
                WIDTH // 2,
                popup.y + 555 + int(self.pause_buttons_offset)
            )
            for b in (
                self.resume_button,
                self.pause_reset_button,
                self.pause_new_button,
                self.pause_menu_button,
            ):
                b.bg_color = self.theme["button"]
                b.hover_color = self.theme["button_hover"]
                b.border_color = self.theme["grid"]
                b.text_color = self.theme["text"]

            self.resume_button.draw(self.screen)
            self.pause_reset_button.draw(self.screen)
            self.pause_new_button.draw(self.screen)
            self.pause_menu_button.draw(self.screen)
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
                popup.y + 245,
                320,
                10
            )

            music_bar = self.music_slider

            pygame.draw.rect(
                self.screen,
                self.theme["grid"],
                music_bar,
                border_radius=5
            )

            music_fill = pygame.Rect(
                music_bar.x,
                music_bar.y,
                int(music_bar.width * self.music_volume),
                music_bar.height
            )

            

            pygame.draw.rect(
                self.screen,
                PRIMARY,
                music_fill,
                border_radius=3
            )

            music_knob_x = music_bar.x + int(music_bar.width * self.music_volume)

            pygame.draw.circle(
                self.screen,
                (0,0,0,50),
                (music_knob_x+2, music_bar.centery+2),
                13
            )

            pygame.draw.circle(
                self.screen,
                (255,255,255),
                (music_knob_x, music_bar.centery),
                12
            )

            pygame.draw.circle(
                self.screen,
                PRIMARY,
                (music_knob_x, music_bar.centery),
                12,
                3
            )

            music_percent = self.board.info_font.render(
                f"{int(self.music_volume * 100)}%",
                True,
                self.theme["text"]
            )

            music_percent_rect = music_percent.get_rect(
                midleft=(music_bar.right + 35, music_bar.centery)
            )

            self.screen.blit(
                music_percent,
                music_percent_rect
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
                popup.y + 335,
                320,
                10
            )

            sfx_bar = self.sfx_slider

            pygame.draw.rect(
                self.screen,
                self.theme["grid"],
                sfx_bar,
                border_radius=5
            )

            sfx_fill = pygame.Rect(
                sfx_bar.x,
                sfx_bar.y,
                int(sfx_bar.width * self.sfx_volume),
                sfx_bar.height
            )

            

            pygame.draw.rect(
                self.screen,
                PRIMARY,
                sfx_fill,
                border_radius=3
            )

            sfx_knob_x = sfx_bar.x + int(sfx_bar.width * self.sfx_volume)

            pygame.draw.circle(
                self.screen,
                (0,0,0,50),
                (sfx_knob_x+2, sfx_bar.centery+2),
                13
            )

            pygame.draw.circle(
                self.screen,
                (255,255,255),
                (sfx_knob_x, sfx_bar.centery),
                12
            )

            pygame.draw.circle(
                self.screen,
                PRIMARY,
                (sfx_knob_x, sfx_bar.centery),
                12,
                3
            )

            sfx_percent = self.board.info_font.render(
                f"{int(self.sfx_volume * 100)}%",
                True,
                self.theme["text"]
            )

            sfx_percent_rect = sfx_percent.get_rect(
                midleft=(sfx_bar.right + 35, sfx_bar.centery)
            )

            self.screen.blit(
                sfx_percent,
                sfx_percent_rect
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
            
            
            
            
            
            
        # ---------- WIN / GAME OVER ACTIONS ----------
        if self.logic.game_won or self.logic.game_over:
            self.win_buttons_offset += (0 - self.win_buttons_offset) * 0.18
            self.popup_new_button.text = "PLAY AGAIN" if self.logic.game_over else "NEW GAME"

            if self.logic.game_over:
                if self.logic.popup_scale < 1:
                    self.logic.popup_scale += (1 - self.logic.popup_scale) * 0.14
                popup_scale = min(self.logic.popup_scale, 1)
                self.screen.blit(self.game_over_background, (0, 0))
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 90))
                self.screen.blit(overlay, (0, 0))
                panel_width = int(650 * popup_scale)
                panel_height = int(640 * popup_scale)
                panel = pygame.Rect(
                    WIDTH // 2 - panel_width // 2,
                    HEIGHT // 2 - panel_height // 2,
                    panel_width,
                    panel_height
                )
                pygame.draw.rect(self.screen, self.theme["shadow"], panel.move(0, 9), border_radius=30)
                panel_fill = pygame.Surface(panel.size, pygame.SRCALPHA)
                pygame.draw.rect(
                    panel_fill,
                    (*self.theme["popup"], 242),  # 95% opacity
                    panel_fill.get_rect(),
                    border_radius=26
                )
                self.screen.blit(panel_fill, panel.topleft)
                pygame.draw.rect(self.screen, (220, 70, 70), panel, 3, border_radius=26)
                if popup_scale >= 0.95:
                    self.screen.blit(
                        self.game_over_panel_fade,
                        self.game_over_panel_fade.get_rect(center=panel.center)
                    )
                    title_font = pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 58)
                    title = title_font.render("GAME OVER", True, (235, 75, 80))
                    subtitle = self.board.info_font.render("You reached the 3-mistake limit", True, self.theme["secondary"])
                    self.screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 105)))
                    self.screen.blit(subtitle, subtitle.get_rect(center=(panel.centerx, panel.y + 158)))
                    self.screen.blit(
                        self.lost_image,
                        self.lost_image.get_rect(center=(panel.centerx, panel.y + 260))
                    )
                    stat_y = panel.y + 365
                    elapsed = self.logic.get_elapsed_time()
                    stats = (("TIME", f"{elapsed // 60:02}:{elapsed % 60:02}"), ("DIFFICULTY", self.logic.difficulty), ("MISTAKES", "3 / 3"))
                    for index, (label, value) in enumerate(stats):
                        card = pygame.Rect(panel.x + 35 + index * 195, stat_y, 175, 90)
                        pygame.draw.rect(self.screen, self.theme["button"], card, border_radius=16)
                        pygame.draw.rect(self.screen, self.theme["popup_border"], card, 2, border_radius=16)
                        label_surface = self.board.info_font.render(label, True, self.theme["secondary"])
                        value_surface = self.board.header_font.render(value, True, (235, 75, 80) if label == "MISTAKES" else self.theme["text"])
                        self.screen.blit(label_surface, label_surface.get_rect(center=(card.centerx, card.y + 28)))
                        self.screen.blit(value_surface, value_surface.get_rect(center=(card.centerx, card.y + 62)))

            button_y = (panel.bottom - 65 if self.logic.game_over else HEIGHT // 2 + 360) + int(self.win_buttons_offset)
            self.popup_new_button.rect.center = (WIDTH // 2 - 180, button_y)
            self.popup_menu_button.rect.center = (WIDTH // 2, button_y)
            self.popup_exit_button.rect.center = (WIDTH // 2 + 180, button_y)
            for button in (self.popup_new_button, self.popup_menu_button, self.popup_exit_button):
                button.bg_color = self.theme["button"]
                button.hover_color = self.theme["button_hover"]
                button.border_color = self.theme["grid"]
                button.text_color = self.theme["text"]
                button.draw(self.screen)
        # ---------- Dynamic Music Volume ----------
        if self.audio_available:
            current = pygame.mixer.music.get_volume()
            target = self.music_win_volume if self.logic.game_won else self.music_volume
            if abs(current-target) < 0.01:
                current = target
            else:
                current += (target-current)*0.06
            pygame.mixer.music.set_volume(current)
        try:
            if (
                self.drag_music
                or self.drag_sfx
                or self.music_slider.collidepoint(pygame.mouse.get_pos())
                or self.sfx_slider.collidepoint(pygame.mouse.get_pos())
            ):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        except pygame.error:
            pass

        pygame.display.flip()
    def play_sound(self, sound):

        if self.audio_available and self.sfx_on and self.sfx_volume > 0 and sound is not None:
            sound.play()

    def set_music_volume(self, volume):
        self.music_volume = volume
        if self.audio_available:
            pygame.mixer.music.set_volume(volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
        if self.audio_available:
            for sound in (self.click_sound, self.correct_sound, self.wrong_sound,
                          self.hint_sound, self.win_sound, self.lose_sound):
                if sound is not None:
                    sound.set_volume(volume)

    def fade_out_music(self, duration):
        if self.audio_available:
            pygame.mixer.music.fadeout(duration)

    def record_match(self, won):
        if self.match_recorded:
            return
        self.stats.record_match(
            self.difficulty,
            won,
            self.logic.score,
            self.logic.get_elapsed_time(),
            self.logic.mistakes,
            self.logic.hints_used,
            self.logic.numbers_entered,
        )
        self.match_recorded = True

    def play_music_track(self, track):
        """Switch the looping music only when the requested track changes."""
        tracks = {
            "background": "assets/sounds/background.mp3",
            "easy": "assets/sounds/easy.mp3",
            "medium": "assets/sounds/medium.mp3",
            "hard": "assets/sounds/hard.mp3",
        }

        if not self.audio_available or track == self.current_music_track:
            return

        pygame.mixer.music.fadeout(250)
        pygame.mixer.music.load(tracks[track])
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1, fade_ms=350)
        self.current_music_track = track

    def play_menu_music(self):
        self.play_music_track("background")

    def new_game(self, difficulty):
        self.win_buttons_offset = 60
        self.difficulty = difficulty.lower()
        self.game_started = True
        self.match_recorded = False

        self.play_music_track(self.difficulty)

        self.logic = SudokuLogic(
            self.difficulty
        )

        self.logic.difficulty = self.difficulty.capitalize()

        self.board.logic = self.logic

        self.board.display_score = 0
        self.win_buttons_offset = 120
        if self.audio_available:
            pygame.mixer.music.set_volume(self.music_volume)

    def run(self):

        while self.running:

            self.clock.tick(FPS)

            self.handle_events()

            self.draw()

        pygame.quit()
