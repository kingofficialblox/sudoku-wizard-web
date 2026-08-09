import pygame
import time
import json
import os
import math
import ctypes
import random
from datetime import date

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
from tutorial_menu import TutorialMenu
from achievements_menu import AchievementsMenu
from store_menu import StoreMenu
from daily_calendar_menu import DailyCalendarMenu
from app_paths import user_file
class Game:

    SAVE_GAME_FILE = user_file("saved_game.json")

    def __init__(self):

        # The desktop layout is taller than some 900 px screens.  SDL centres
        # an oversized window by default, which can put its title bar above
        # the monitor.  Pin it to the visible top-left corner instead.
        if os.name == "nt":
            os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"

        # Pydroid's runner prepares SDL through pygame.init(); unlike a direct
        # pygame.display.init() call, this correctly marks SDL as main-ready.
        pygame.init()

        # Give Windows a game-specific taskbar identity instead of grouping
        # this window beneath the Python executable's icon.
        if os.name == "nt":
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    "MetaCreators.SudokuWizard"
                )
            except (AttributeError, OSError):
                pass

        # Use the game's own branding in the desktop window and taskbar.
        self.window_icon = None
        try:
            self.window_icon = pygame.transform.smoothscale(
                pygame.image.load("assets/images/game_logo.png"), (64, 64)
            )
            pygame.display.set_icon(self.window_icon)
        except (pygame.error, OSError):
            pass

        # Every desktop platform uses a fixed internal canvas and displays a
        # proportional copy fitted to the current monitor. This keeps layout,
        # text, hitboxes and artwork consistent across resolutions and DPI
        # settings without cropping on smaller computers.
        self.desktop_scaled = not PORTRAIT_MODE
        if self.desktop_scaled:
            # Desktop starts in real full-screen.  The game still renders to
            # its fixed design canvas, then fits it proportionally below.
            display_info = pygame.display.Info()
            self.windowed_size = (
                min(WIDTH, max(640, int(display_info.current_w * 0.85)), display_info.current_w),
                min(HEIGHT, max(480, int(display_info.current_h * 0.85)), display_info.current_h),
            )
            self.is_fullscreen = True
            self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.window_size = self.display_surface.get_size()
            self.screen = pygame.Surface((WIDTH, HEIGHT)).convert()
            self._physical_mouse_get_pos = pygame.mouse.get_pos
            pygame.mouse.get_pos = self.get_logical_mouse_pos
        else:
            self.window_size = (WIDTH, HEIGHT)
            self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
            self.screen = self.display_surface

        # SDL applies the final window icon only once the display exists.
        if self.window_icon is not None:
            pygame.display.set_icon(self.window_icon)

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
        # Reuse the full-screen dim layer on result screens.  Allocating this
        # large transparent surface every frame is costly on phones.
        self.game_over_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.game_over_overlay.fill((0, 0, 0, 90))
        self.window_bar_height = 38
        self.window_min_button = pygame.Rect(WIDTH - 126, 0, 42, self.window_bar_height)
        self.window_max_button = pygame.Rect(WIDTH - 84, 0, 42, self.window_bar_height)
        self.window_close_button = pygame.Rect(WIDTH - 42, 0, 42, self.window_bar_height)
        self.window_bar_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 17)
        self.last_finger_tap = None
        self.last_pointer_down = None
        self.last_number_pad_input = None
        self.last_notes_toggle_time = 0

        self.logic = SudokuLogic()
        self.base_theme = LIGHT
        self.theme = LIGHT.copy()
        self.load_settings()
        

        self.board = Board(self.logic)
        self.board.animations_enabled = self.animations_enabled
        self.current_screen = "splash"
        self.game_started = False
        self.daily_challenge_active = False
        self.daily_challenge_date = ""
        self.menu = Menu(self)
        self.settings_menu = SettingsMenu(self)
        self.stats = StatsManager()
        self.apply_cosmetic_aura()
        self.logic.hint_tokens = self.stats.get_hint_tokens(self.logic.difficulty)
        self.logic.auto_notes_tokens = self.stats.get_auto_notes_tokens()
        self.logic.erase_all_tokens = self.stats.get_erase_all_tokens()
        self.stats_menu = StatsMenu(self)
        self.stats_open = False
        self.achievements_menu = AchievementsMenu(self)
        self.achievements_open = False
        self.store_menu = StoreMenu(self)
        self.store_open = False
        self.daily_calendar_menu = DailyCalendarMenu(self)
        self.daily_calendar_open = False
        self.tutorial_menu = TutorialMenu(self)
        self.tutorial_open = False
        self.match_recorded = False
        self.achievement_notice = None
        self.achievement_notice_started = 0
        self.achievement_notice_queue = []
        self.achievement_notice_duration = 3200
        self.last_game_save = 0
        self.load_saved_game()
        # ---------- Popup Icons ----------

        self.game_logo = pygame.image.load(
            "assets/images/game_logo.png"
        ).convert_alpha()
        self.lost_image = pygame.image.load(
            "assets/images/lost.png"
        ).convert_alpha()
        self.achievement_icon = pygame.transform.smoothscale(
            pygame.image.load("assets/images/medal.png").convert_alpha(), (52, 52)
        )
        self.game_over_background_source = pygame.image.load("assets/images/gameover.png").convert()
        self.game_over_background = pygame.transform.smoothscale(
            self.game_over_background_source, self.screen.get_size()
        )
        self.game_over_panel_fade = pygame.transform.smoothscale(
            self.game_over_background, (650, 640)
        )
        self.game_over_panel_fade.set_alpha(32)
        self.game_over_panel_fill_cache = {}
        self.game_over_title_font = pygame.font.Font(
            "assets/fonts/Poppins-ExtraBold.ttf", 58
        )

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
        self.pencil_icon = pygame.image.load(
            "assets/images/pencil.png"
        ).convert_alpha()
        self.erase_icon = pygame.image.load(
            "assets/images/erase.png"
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
        self.store_icon = pygame.image.load("assets/images/store.png").convert_alpha()
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

        side_icon_size = 58 if PORTRAIT_MODE else 44
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
        self.pencil_icon = pygame.transform.smoothscale(
            self.pencil_icon,
            (side_icon_size, side_icon_size)
        )
        self.erase_icon = pygame.transform.smoothscale(
            self.erase_icon,
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
        self.store_icon = pygame.transform.smoothscale(self.store_icon, (50, 50))

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
        
        
        
        
        icon_button_size = 58 if PORTRAIT_MODE else 46
        icon_button_x = start_x
        # On desktop the side actions follow the score, time and mistakes
        # cards; portrait keeps them beside the board for touch-friendly room.
        # Leave room for the Hint Token display between Settings and Hint on phones.
        icon_button_y = BOARD_Y + 184 if PORTRAIT_MODE else BOARD_Y + 344
        action_gap = 5 if PORTRAIT_MODE else 3

        if PORTRAIT_MODE:
            first_control_x = second_control_x = icon_button_x
            notes_y = icon_button_y + (icon_button_size + action_gap)
            auto_notes_y = icon_button_y + (icon_button_size + action_gap) * 2
            erase_y = icon_button_y + (icon_button_size + action_gap) * 3
            erase_all_y = icon_button_y + (icon_button_size + action_gap) * 4
            undo_y = icon_button_y + (icon_button_size + action_gap) * 5
            menu_x = icon_button_x
            menu_y = icon_button_y + (icon_button_size + action_gap) * 6
        else:
            pair_gap = 12
            pair_width = icon_button_size * 2 + pair_gap
            first_control_x = side_x + (button_width - pair_width) // 2
            second_control_x = first_control_x + icon_button_size + pair_gap
            notes_y = auto_notes_y = icon_button_y
            erase_y = erase_all_y = icon_button_y + icon_button_size + 9
            undo_y = icon_button_y + (icon_button_size + 9) * 2
            menu_x = side_x + (button_width - icon_button_size) // 2
            menu_y = icon_button_y + (icon_button_size + 9) * 3

        self.undo_button = Button(
            second_control_x,
            undo_y,
            icon_button_size,
            icon_button_size,
            "",
            self.undo_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )

        self.hint_button = Button(
            first_control_x,
            icon_button_y if PORTRAIT_MODE else undo_y,
            icon_button_size,
            icon_button_size,
            "",
            self.hint_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        self.notes_button = Button(
            first_control_x,
            notes_y,
            icon_button_size,
            icon_button_size,
            "",
            self.pencil_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        self.erase_notes_button = Button(
            first_control_x,
            erase_y,
            icon_button_size,
            icon_button_size,
            "",
            self.erase_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        self.board_menu_button = Button(
            menu_x,
            menu_y,
            icon_button_size,
            icon_button_size,
            "",
            self.menu_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        self.auto_notes_button = Button(
            second_control_x,
            auto_notes_y,
            icon_button_size,
            icon_button_size,
            "",
            self.pencil_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        self.erase_all_button = Button(
            second_control_x,
            erase_all_y,
            icon_button_size,
            icon_button_size,
            "",
            self.erase_icon,
            bg_color=(255,255,255),
            hover_color=(255,248,235)
        )
        # -------- Number Buttons --------

        self.number_buttons = []

        key_width = 60 if PORTRAIT_MODE else 75
        key_height = 60 if PORTRAIT_MODE else 55
        key_gap = 8 if PORTRAIT_MODE else 12

        start_x = BOARD_X - 100
        start_y = BOARD_Y + 10

        for i in range(9):
            if PORTRAIT_MODE:
                total_width = key_width * 9 + key_gap * 8
                key_x = WIDTH // 2 - total_width // 2 + i * (key_width + key_gap)
                key_y = BOARD_Y + CELL_SIZE * 9 + 35
            else:
                key_x = start_x
                key_y = start_y + i * (key_height + key_gap)
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
        # On phones these controls belong with the board actions, above Hint.
        # This keeps them clear of the compact status cards.
        if PORTRAIT_MODE:
            control_size = 58
            control_x = self.hint_button.rect.centerx - control_size // 2
            self.pause_button = pygame.Rect(control_x, self.hint_button.rect.y - 184, control_size, control_size)
            self.settings_button = pygame.Rect(control_x, self.hint_button.rect.y - 117, control_size, control_size)
            self.store_game_button = pygame.Rect(control_x, self.hint_button.rect.y - 50, control_size, control_size)
        else:
            self.pause_button = pygame.Rect(WIDTH - 75, 200, 42, 42)
            self.settings_button = pygame.Rect(WIDTH - 75, 270, 42, 42)
            self.store_game_button = pygame.Rect(WIDTH - 75, 340, 42, 42)
        self.hint_token_value_font = pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 16 if PORTRAIT_MODE else 17)
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

        # ---------- Background Music ----------
        self.current_music_track = "background"
        self.result_music_active = False
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
    def apply_cosmetic_aura(self):
        """Apply the equipped Store aura to every game screen and card."""
        self.theme = self.base_theme.copy()
        if not hasattr(self, "stats"):
            return
        cosmetic_id = self.stats.data.get("cosmetics", {}).get("equipped", "violet")
        cosmetic = self.stats.COSMETICS.get(cosmetic_id, self.stats.COSMETICS["violet"])
        accent = cosmetic["accent"]
        self.theme["accent"] = accent
        self.theme["selected_outline"] = accent
        self.theme["selected_glow"] = accent

    def save_settings(self):
        data = {
            "music": self.music_volume,
            "sfx": self.sfx_volume,
            "theme": "dark" if self.base_theme == DARK else "light",
            "animations": self.animations_enabled,
            "tutorial_seen": self.tutorial_seen,
        }

        try:
            with open(user_file("settings.json"), "w") as f:
                json.dump(data, f, indent=4)
        except OSError as error:
            print("Settings could not be saved:", error)

    def save_game_state(self):
        """Persist an unfinished puzzle so Continue survives closing the app."""
        if (
            not self.game_started
            or self.logic.game_won
            or self.logic.game_over
        ):
            return
        data = {
            "difficulty": self.logic.difficulty.lower(),
            "grid": self.logic.grid,
            "solution": self.logic.solution,
            "original_grid": self.logic.original_grid,
            "fixed": self.logic.fixed,
            "notes": [[sorted(cell) for cell in row] for row in self.logic.notes],
            "score": self.logic.score,
            "mistakes": self.logic.mistakes,
            "hints_used": self.logic.hints_used,
            "numbers_entered": self.logic.numbers_entered,
            "stars": self.logic.stars,
            "accuracy": self.logic.accuracy,
            "elapsed": self.logic.get_elapsed_time(),
            "daily_challenge": self.daily_challenge_active,
            "daily_challenge_date": self.daily_challenge_date,
            "game_mode": getattr(self.logic, "game_mode", "classic"),
            "time_limit": getattr(self.logic, "time_limit", None),
        }
        try:
            with open(self.SAVE_GAME_FILE, "w") as file:
                json.dump(data, file)
        except OSError as error:
            print("Game could not be saved:", error)

    def load_saved_game(self):
        try:
            with open(self.SAVE_GAME_FILE, "r") as file:
                data = json.load(file)
            difficulty = data["difficulty"].lower()
            if difficulty not in ("easy", "medium", "hard"):
                return
            logic = SudokuLogic(difficulty)
            logic.grid = data["grid"]
            logic.solution = data["solution"]
            logic.original_grid = data["original_grid"]
            logic.fixed = data["fixed"]
            logic.notes = [[set(cell) for cell in row] for row in data.get("notes", [[[] for _ in range(9)] for _ in range(9)])]
            logic.score = data.get("score", 0)
            logic.mistakes = data.get("mistakes", 0)
            logic.hints_used = data.get("hints_used", 0)
            logic.numbers_entered = data.get("numbers_entered", 0)
            logic.stars = data.get("stars", 0)
            logic.accuracy = data.get("accuracy", 100)
            logic.hint_tokens = self.stats.get_hint_tokens(difficulty)
            logic.auto_notes_tokens = self.stats.get_auto_notes_tokens()
            logic.erase_all_tokens = self.stats.get_erase_all_tokens()
            logic.daily_challenge = data.get("daily_challenge", False)
            logic.game_mode = data.get("game_mode", "classic")
            logic.time_limit = data.get("time_limit")
            if logic.game_mode == "zen":
                logic.mistake_limit = None
            elif logic.game_mode == "practice":
                logic.reveal_mistakes = True
            logic.start_time = time.time() - data.get("elapsed", 0)
            logic.paused = True
            logic.pause_start = time.time()
            self.logic = logic
            self.board.logic = logic
            self.difficulty = difficulty
            self.daily_challenge_active = data.get("daily_challenge", False)
            self.daily_challenge_date = data.get("daily_challenge_date", "")
            if self.daily_challenge_active and not self.daily_challenge_date:
                self.daily_challenge_date = date.today().isoformat()
            self.game_started = True
        except (OSError, KeyError, TypeError, json.JSONDecodeError):
            return

    def delete_saved_game(self):
        try:
            if os.path.exists(self.SAVE_GAME_FILE):
                os.remove(self.SAVE_GAME_FILE)
        except OSError:
            pass


    def load_settings(self):
        try:
            with open(user_file("settings.json"), "r") as f:
                data = json.load(f)

            self.base_theme = DARK if data.get("theme") == "dark" else LIGHT
            self.theme = self.base_theme.copy()

            self.music_volume = data.get("music", 0.5)
            self.sfx_volume = data.get("sfx", 0.5)
            self.animations_enabled = data.get("animations", True)
            self.tutorial_seen = data.get("tutorial_seen", False)

        except:
            self.base_theme = LIGHT
            self.theme = LIGHT.copy()
            self.music_volume = 0.5
            self.sfx_volume = 0.5
            self.animations_enabled = True
            self.tutorial_seen = False

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
            is_finger_event = event.type in finger_events
            if is_finger_event:
                event_type = {
                    getattr(pygame, "FINGERDOWN", None): pygame.MOUSEBUTTONDOWN,
                    getattr(pygame, "FINGERUP", None): pygame.MOUSEBUTTONUP,
                    getattr(pygame, "FINGERMOTION", None): pygame.MOUSEMOTION,
                }[event.type]
                event = pygame.event.Event(
                    event_type,
                    {"pos": (
                        int(event.x * self.screen.get_width()),
                        int(event.y * self.screen.get_height()),
                    ), "button": 1}
                )

            # The visible desktop window may be smaller than the logical game
            # canvas. Convert its pointer events back into canvas coordinates.
            if (
                self.desktop_scaled
                and event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION)
                and hasattr(event, "pos")
            ):
                render_area = self.get_render_area()
                logical_pos = (
                    max(0, min(WIDTH - 1, int((event.pos[0] - render_area.x) * WIDTH / max(1, render_area.width)))),
                    max(0, min(HEIGHT - 1, int((event.pos[1] - render_area.y) * HEIGHT / max(1, render_area.height)))),
                )
                event_data = dict(event.dict)
                event_data["pos"] = logical_pos
                event = pygame.event.Event(event.type, event_data)

            # Pydroid can also emit a synthetic mouse click after FINGERDOWN.
            # Process the actual finger event once and discard its duplicate.
            if event.type == pygame.MOUSEBUTTONDOWN:
                now = pygame.time.get_ticks()
                if is_finger_event:
                    self.last_finger_tap = (event.pos, now)
                elif self.last_finger_tap:
                    previous_pos, previous_time = self.last_finger_tap
                    if (
                        now - previous_time < 300
                        and abs(event.pos[0] - previous_pos[0]) < 18
                        and abs(event.pos[1] - previous_pos[1]) < 18
                    ):
                        continue

                # Some Android devices send mouse and finger events in either
                # order.  This final guard deduplicates the tap regardless of
                # which event arrives first.
                if self.last_pointer_down:
                    previous_pos, previous_time = self.last_pointer_down
                    if (
                        now - previous_time < 160
                        and abs(event.pos[0] - previous_pos[0]) < 24
                        and abs(event.pos[1] - previous_pos[1]) < 24
                    ):
                        continue
                self.last_pointer_down = (event.pos, now)

            if event.type == pygame.QUIT:
                self.save_game_state()
                self.running = False
                continue

            # Full-screen has no Windows frame, so its slim in-game bar owns
            # the same window actions.
            if self.desktop_scaled and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.window_close_button.collidepoint(event.pos):
                    self.save_game_state()
                    self.running = False
                    continue
                if self.window_min_button.collidepoint(event.pos):
                    pygame.display.iconify()
                    continue
                if self.window_max_button.collidepoint(event.pos):
                    self.toggle_window_maximize()
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

            if self.tutorial_open:
                self.tutorial_menu.handle_event(event)
                continue

            if self.achievements_open:
                self.achievements_menu.handle_event(event)
                continue

            if self.store_open:
                self.store_menu.handle_event(event)
                continue

            if self.daily_calendar_open:
                self.daily_calendar_menu.handle_event(event)
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

                        if self.base_theme == LIGHT:
                            self.base_theme = DARK
                        else:
                            self.base_theme = LIGHT
                        self.apply_cosmetic_aura()
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
                        self.new_game(self.logic.difficulty, getattr(self.logic, "game_mode", "classic"))
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

                    if not self.daily_challenge_active and self.popup_new_button.clicked(pos):
                        self.play_sound(self.click_sound)
                        self.new_game(self.logic.difficulty, getattr(self.logic, "game_mode", "classic"))

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

                if self.store_game_button.collidepoint(pos):
                    self.play_sound(self.click_sound)
                    self.store_open = True
                    continue

                # -------------------------------------------------
                # SIDE BUTTONS
                # -------------------------------------------------

                if self.undo_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    undo_result = self.logic.undo()
                    if undo_result == "HINT_LOCKED":
                        self.hint_locked_until = pygame.time.get_ticks() + 1800

                elif self.hint_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    hint_result = self.logic.give_hint()
                    if hint_result == "HINT":
                        self.stats.set_hint_tokens(self.logic.difficulty, self.logic.hint_tokens)
                        self.play_sound(self.hint_sound)

                elif self.auto_notes_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    auto_result = self.logic.apply_auto_notes()
                    if auto_result == "AUTO_NOTES":
                        self.stats.set_auto_notes_tokens(self.logic.auto_notes_tokens)
                        self.play_sound(self.hint_sound)

                elif self.notes_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.toggle_notes_mode()

                elif self.erase_notes_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    self.logic.clear_notes()

                elif self.erase_all_button.clicked(pos):
                    self.play_sound(self.click_sound)
                    erase_result = self.logic.erase_all()
                    if erase_result == "ERASE_ALL":
                        self.stats.set_erase_all_tokens(self.logic.erase_all_tokens)
                        self.play_sound(self.hint_sound)

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
                            selected_before = self.logic.selected

                            # Some Android runtimes dispatch a delayed second
                            # press for one number-pad tap. Ignore only that
                            # exact duplicate press.
                            last_input = self.last_number_pad_input
                            if (
                                last_input
                                and last_input[0] == number
                                and last_input[1] == selected_before
                                and pygame.time.get_ticks() - last_input[2] < 500
                            ):
                                break

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
                                self.record_match(True)

                            elif result is True:
                                self.play_sound(self.correct_sound)

                            elif result is False or result in ("GAME_OVER", "PRACTICE_REVEAL"):
                                self.play_sound(self.wrong_sound)
                                if result == "GAME_OVER":
                                    self.record_match(False)

                            if result not in (None, "DUPLICATE"):
                                self.last_number_pad_input = (
                                    number,
                                    selected_before,
                                    pygame.time.get_ticks(),
                                )

                            break

                            if result == "WIN":
                                self.play_sound(self.correct_sound)
                            elif result is True:
                                self.play_sound(self.correct_sound)

                            elif result is False or result == "PRACTICE_REVEAL":
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
                    self.toggle_notes_mode()

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
                        self.record_match(True)

                    elif result is True:
                        self.play_sound(self.correct_sound)

                    elif result is False or result in ("GAME_OVER", "PRACTICE_REVEAL"):
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
                if not self.tutorial_seen:
                    self.tutorial_menu.page = 0
                    self.tutorial_open = True
            self.draw_window_bar()
            self.present()
            return

        if self.settings_open:
            self.settings_menu.draw()
            self.draw_window_bar()
            self.present()
            return

        if self.stats_open:
            self.stats_menu.draw()
            self.draw_window_bar()
            self.present()
            return

        if self.tutorial_open:
            self.tutorial_menu.draw()
            self.draw_window_bar()
            self.present()
            return

        if self.achievements_open:
            self.achievements_menu.draw()
            self.draw_window_bar()
            self.present()
            return

        if self.store_open:
            self.store_menu.draw()
            self.draw_window_bar()
            self.present()
            return

        if self.daily_calendar_open:
            self.daily_calendar_menu.draw()
            self.draw_window_bar()
            self.present()
            return

        if self.current_screen == "menu":

            self.menu.update()

            self.menu.draw()

            self.draw_window_bar()
            self.present()

            return

        if self.current_screen == "menu":
            self.draw_menu()
            self.present()
            return

        self.screen.fill(self.theme["background"])
        mouse_pos = pygame.mouse.get_pos()
        self.pause_hover = self.pause_button.collidepoint(mouse_pos)
        self.settings_hover = self.settings_button.collidepoint(mouse_pos)
        self.pause_hover = self.pause_button.collidepoint(mouse_pos)
        self.update_result_music()
        # Timed Mode ends cleanly when its ten-minute round expires.
        if (
            getattr(self.logic, "game_mode", "classic") == "timed"
            and not self.logic.game_won
            and not self.logic.game_over
            and self.logic.get_elapsed_time() >= getattr(self.logic, "time_limit", 600)
        ):
            self.logic.game_over = True
            self.logic.end_time = time.time()
            self.logic.popup_scale = 0.0
            self.record_match(False)
        # ---------- End-of-game effects (each plays/spawns once) ----------
        if self.logic.game_won and not self.previous_win_state:

            self.confetti = []

            for _ in range(CONFETTI_COUNT if self.animations_enabled else 0):
                self.confetti.append(Confetti())

            self.previous_win_state = True
            self.start_result_music("win")

        elif not self.logic.game_won:
            self.previous_win_state = False

        if self.logic.game_over and not self.previous_game_over_state:
            self.start_result_music("lose")
            self.previous_game_over_state = True
        elif not self.logic.game_over:
            self.previous_game_over_state = False

        # Game Over replaces the board with its own themed screen, so there
        # is no reason to spend phone GPU time drawing it underneath.
        if not self.logic.game_over and not self.logic.game_won:
            self.board.draw(
                self.screen,
                self.theme
            )

        # Keep the celebration alive while the win screen is open.
        if self.logic.game_won and self.animations_enabled:
            for particle in self.confetti:
                particle.update()
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

        # In-game Store shortcut follows Settings in the same icon-only style.
        store_hover = self.store_game_button.collidepoint(mouse_pos)
        store_size = 52 if not store_hover else 58
        store_icon = pygame.transform.smoothscale(self.store_icon, (store_size, store_size))
        store_rect = store_icon.get_rect(center=self.store_game_button.center)
        store_shadow = pygame.Surface((store_size + 10, store_size + 10), pygame.SRCALPHA)
        pygame.draw.circle(store_shadow, (0, 0, 0, 45), (store_shadow.get_width() // 2, store_shadow.get_height() // 2), store_size // 2)
        self.screen.blit(store_shadow, store_shadow.get_rect(center=(store_rect.centerx, store_rect.centery + 4)))
        self.screen.blit(store_icon, store_rect)
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
                self.notes_button,
                self.erase_notes_button,
                self.erase_all_button,
                self.board_menu_button,
                self.auto_notes_button,
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
                self.notes_button,
                self.erase_notes_button,
                self.erase_all_button,
                self.board_menu_button,
                self.auto_notes_button,
            ):
                b.bg_color = self.theme["button"]
                b.hover_color = self.theme["button_hover"]
                b.border_color = self.theme["grid"]
                b.text_color = self.theme["text"]

            self.notes_button.selected = self.notes_mode
            self.hint_button.count = None

            self.undo_button.draw(self.screen)
            self.hint_button.draw(self.screen)
            self.notes_button.draw(self.screen)
            self.erase_notes_button.draw(self.screen)
            self.erase_all_button.draw(self.screen)
            self.board_menu_button.draw(self.screen)
            self.auto_notes_button.draw(self.screen)

            # Draw this after the PNG icon so the number always stays visible.
            token_center = (
                self.hint_button.rect.right - 14,
                self.hint_button.rect.y + 14,
            )
            pygame.draw.circle(self.screen, self.theme["shadow"], (token_center[0], token_center[1] + 2), 13)
            pygame.draw.circle(self.screen, self.theme["accent"], token_center, 13)
            pygame.draw.circle(self.screen, self.theme["popup_border"], token_center, 13, 2)
            token_value = self.hint_token_value_font.render(str(self.logic.hint_tokens), True, self.theme["text"])
            self.screen.blit(token_value, token_value.get_rect(center=token_center))
            auto_center = (self.auto_notes_button.rect.right - 11, self.auto_notes_button.rect.y + 12)
            pygame.draw.circle(self.screen, self.theme["shadow"], (auto_center[0], auto_center[1] + 2), 12)
            pygame.draw.circle(self.screen, self.theme["accent"], auto_center, 12)
            pygame.draw.circle(self.screen, self.theme["popup_border"], auto_center, 12, 2)
            auto_value = self.hint_token_value_font.render(str(self.logic.auto_notes_tokens), True, self.theme["text"])
            self.screen.blit(auto_value, auto_value.get_rect(center=auto_center))
            erase_center = (self.erase_all_button.rect.right - 11, self.erase_all_button.rect.y + 12)
            pygame.draw.circle(self.screen, self.theme["shadow"], (erase_center[0], erase_center[1] + 2), 12)
            pygame.draw.circle(self.screen, self.theme["accent"], erase_center, 12)
            pygame.draw.circle(self.screen, self.theme["popup_border"], erase_center, 12, 2)
            erase_value = self.hint_token_value_font.render(str(self.logic.erase_all_tokens), True, self.theme["text"])
            self.screen.blit(erase_value, erase_value.get_rect(center=erase_center))
            erase_all_label_font = pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 9 if PORTRAIT_MODE else 8)
            erase_all_label = erase_all_label_font.render("ALL", True, self.theme["text"])
            self.screen.blit(
                erase_all_label,
                erase_all_label.get_rect(center=(self.erase_all_button.rect.centerx, self.erase_all_button.rect.bottom - 7)),
            )

            if getattr(self, "hint_locked_until", 0) > pygame.time.get_ticks():
                notice_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 16 if PORTRAIT_MODE else 18)
                notice = notice_font.render("EARN A HINT TO UNDO A CLUE", True, self.theme["accent"])
                self.screen.blit(notice, notice.get_rect(center=(WIDTH // 2, BOARD_Y - 28)))
            elif time.time() - self.logic.hint_earned_time < 1.7:
                reward_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 18 if PORTRAIT_MODE else 20)
                reward = reward_font.render("+1 HINT EARNED!", True, self.theme["success"])
                self.screen.blit(reward, reward.get_rect(center=(WIDTH // 2, BOARD_Y - 28)))

            if self.notes_mode and PORTRAIT_MODE:
                notes_label = self.board.header_font.render(
                    "NOTES ON", True, self.theme["accent"]
                )
                notes_rect = notes_label.get_rect(
                    center=(WIDTH // 2, BOARD_Y - 28)
                )
                self.screen.blit(notes_label, notes_rect)
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
                if PORTRAIT_MODE:
                    self.logic.popup_scale = 1.0
                elif self.logic.popup_scale < 1:
                    self.logic.popup_scale += (1 - self.logic.popup_scale) * 0.14
                popup_scale = min(self.logic.popup_scale, 1)
                self.screen.blit(self.game_over_background, (0, 0))
                self.screen.blit(self.game_over_overlay, (0, 0))
                panel_width = int(650 * popup_scale)
                panel_height = int(640 * popup_scale)
                panel = pygame.Rect(
                    WIDTH // 2 - panel_width // 2,
                    HEIGHT // 2 - panel_height // 2,
                    panel_width,
                    panel_height
                )
                pygame.draw.rect(self.screen, self.theme["shadow"], panel.move(0, 9), border_radius=30)
                fill_key = (panel.size, self.theme["popup"])
                panel_fill = self.game_over_panel_fill_cache.get(fill_key)
                if panel_fill is None:
                    panel_fill = pygame.Surface(panel.size, pygame.SRCALPHA)
                    pygame.draw.rect(
                        panel_fill,
                        (*self.theme["popup"], 242),  # 95% opacity
                        panel_fill.get_rect(),
                        border_radius=26
                    )
                    self.game_over_panel_fill_cache[fill_key] = panel_fill
                self.screen.blit(panel_fill, panel.topleft)
                pygame.draw.rect(self.screen, (220, 70, 70), panel, 3, border_radius=26)
                if popup_scale >= 0.95:
                    self.screen.blit(
                        self.game_over_panel_fade,
                        self.game_over_panel_fade.get_rect(center=panel.center)
                    )
                    title = self.game_over_title_font.render("GAME OVER", True, (235, 75, 80))
                    over_message = (
                        "Time is up — great effort!"
                        if getattr(self.logic, "game_mode", "classic") == "timed"
                        else "You reached the 3-mistake limit"
                    )
                    subtitle = self.board.info_font.render(over_message, True, self.theme["secondary"])
                    self.screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 105)))
                    self.screen.blit(subtitle, subtitle.get_rect(center=(panel.centerx, panel.y + 158)))
                    self.screen.blit(
                        self.lost_image,
                        self.lost_image.get_rect(center=(panel.centerx, panel.y + 260))
                    )
                    stat_y = panel.y + 365
                    elapsed = self.logic.get_elapsed_time()
                    game_mode = getattr(self.logic, "game_mode", "classic")
                    time_label = "TIME LEFT" if game_mode == "timed" else "TIME"
                    time_value = "00:00" if game_mode == "timed" else f"{elapsed // 60:02}:{elapsed % 60:02}"
                    stats = (
                        (time_label, time_value),
                        ("MODE", game_mode.upper()),
                        ("MISTAKES", f"{self.logic.mistakes} / 3"),
                    )
                    for index, (label, value) in enumerate(stats):
                        card = pygame.Rect(panel.x + 35 + index * 195, stat_y, 175, 90)
                        pygame.draw.rect(self.screen, self.theme["button"], card, border_radius=16)
                        pygame.draw.rect(self.screen, self.theme["popup_border"], card, 2, border_radius=16)
                        label_surface = self.board.info_font.render(label, True, self.theme["secondary"])
                        value_surface = self.board.header_font.render(
                            value,
                            True,
                            (235, 75, 80) if label == "MISTAKES" else (self.theme["accent"] if label == "MODE" else self.theme["text"]),
                        )
                        self.screen.blit(label_surface, label_surface.get_rect(center=(card.centerx, card.y + 28)))
                        self.screen.blit(value_surface, value_surface.get_rect(center=(card.centerx, card.y + 62)))
                    rewards = getattr(self.logic, "result_rewards", None)
                    if rewards:
                        reward_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 17)
                        reward_text = f"+{rewards.get('coins', 0)} COINS  •  +{rewards.get('xp', 0)} XP  •  {rewards.get('stars', 0)} STARS"
                        reward = reward_font.render(reward_text, True, self.theme["accent"])
                        self.screen.blit(reward, reward.get_rect(center=(panel.centerx, panel.bottom - 112)))

            # Draw the result screen last, so pause/settings are never visible
            # above either result card on desktop or phone.
            if self.logic.game_won:
                self.board.draw(self.screen, self.theme)
                for particle in self.confetti:
                    particle.draw(self.screen)

            button_y = (panel.bottom - 65 if self.logic.game_over else HEIGHT // 2 + 360) + int(self.win_buttons_offset)
            if self.daily_challenge_active:
                self.popup_menu_button.rect.center = (WIDTH // 2, button_y)
                result_buttons = (self.popup_menu_button,)
            else:
                self.popup_new_button.rect.center = (WIDTH // 2 - 95, button_y)
                self.popup_menu_button.rect.center = (WIDTH // 2 + 95, button_y)
                result_buttons = (self.popup_new_button, self.popup_menu_button)
            for button in result_buttons:
                button.bg_color = self.theme["button"]
                button.hover_color = self.theme["button_hover"]
                button.border_color = self.theme["grid"]
                button.text_color = self.theme["text"]
                button.draw(self.screen)

        # Newly unlocked achievements are shown one at a time, with a gentle
        # fade, so several rewards from one game are all visible.
        notice_now = pygame.time.get_ticks()
        if self.achievement_notice and notice_now - self.achievement_notice_started >= self.achievement_notice_duration:
            self.achievement_notice = None
        if self.achievement_notice is None and self.achievement_notice_queue:
            self.achievement_notice = self.achievement_notice_queue.pop(0)
            self.achievement_notice_started = notice_now

        if self.achievement_notice:
            # Show every reward earned by this result together, rather than
            # silently leaving later achievements in a long queue.
            visible_notices = [self.achievement_notice] + self.achievement_notice_queue
            self.achievement_notice_queue = []
            titles = {
                "first_win": "FIRST SPELL",
                "perfect_win": "PERFECT FOCUS",
                "score_10000": "HIGH SCORER",
                "streak_3": "ON FIRE",
                "all_modes": "TRUE WIZARD",
                "streak_5": "UNSTOPPABLE",
                "hintless_win": "CLEAR MIND",
                "speed_demon": "SPEED DEMON",
                "hard_hero": "HARD HERO",
                "coin_collector": "COIN COLLECTOR",
                "easy_graduate": "EASY GRADUATE",
                "medium_conqueror": "MEDIUM CONQUEROR",
                "easy_trio": "GENTLE HAT-TRICK",
                "medium_trio": "STEADY SPELLCASTER",
                "hard_trio": "HARD HAT-TRICK",
                "wins_10": "TENFOLD",
                "wins_25": "PUZZLE VETERAN",
                "matches_10": "DEDICATED PLAYER",
                "matches_50": "SUDOKU REGULAR",
                "streak_10": "BLAZING TRAIL",
                "score_20000": "ARCANE SCORE",
                "score_30000": "LEGENDARY SCORE",
                "lightning_easy": "LIGHTNING LEARNER",
                "rapid_medium": "RAPID RUNE",
                "flawless_hard": "IRON FOCUS",
                "number_scribe": "NUMBER SCRIBE",
                "number_legend": "NUMBER LEGEND",
                "hint_vault": "HINT VAULT",
                "coin_tycoon": "COIN TYCOON",
                "all_modes_three": "TRIPLE CROWN",
                "score_i": "HIGH SCORER I",
                "score_ii": "HIGH SCORER II",
                "score_iii": "HIGH SCORER III",
                "streak_i": "ON FIRE I",
                "streak_ii": "ON FIRE II",
                "streak_iii": "ON FIRE III",
                "coins_i": "COIN COLLECTOR I",
                "coins_ii": "COIN COLLECTOR II",
                "coins_iii": "COIN COLLECTOR III",
                "wins_i": "PUZZLE WINNER I",
                "wins_ii": "PUZZLE WINNER II",
                "wins_iii": "PUZZLE WINNER III",
            }
            titles.update(
                {achievement_id: title for achievement_id, title, _, _ in self.achievements_menu.ACHIEVEMENTS}
            )
            elapsed_notice = notice_now - self.achievement_notice_started
            fade_length = 450
            fade_ratio = min(1.0, elapsed_notice / fade_length, (self.achievement_notice_duration - elapsed_notice) / fade_length)
            alpha = max(0, min(255, int(255 * fade_ratio)))
            toast_width, toast_height = (300, 82) if PORTRAIT_MODE else (240, 82)
            title_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 13 if PORTRAIT_MODE else 12)
            value_font = pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 19 if PORTRAIT_MODE else 17)
            base_y = HEIGHT // 2 - 160 if not PORTRAIT_MODE else HEIGHT // 2 - 180
            for notice_index, notice_id in enumerate(visible_notices[:5]):
                toast = (
                    pygame.Rect(WIDTH // 2 - toast_width // 2, base_y + notice_index * 90, toast_width, toast_height)
                    if PORTRAIT_MODE else pygame.Rect(22, base_y + notice_index * 90, toast_width, toast_height)
                )
                toast_surface = pygame.Surface(toast.size, pygame.SRCALPHA)
                pygame.draw.rect(toast_surface, (*self.theme["shadow"], 230), toast_surface.get_rect().move(0, 5), border_radius=18)
                pygame.draw.rect(toast_surface, (*self.theme["popup"], 245), toast_surface.get_rect(), border_radius=18)
                pygame.draw.rect(toast_surface, (*self.theme["accent"], 255), toast_surface.get_rect(), 2, border_radius=18)
                icon = pygame.transform.smoothscale(self.achievement_icon, (40, 40))
                toast_surface.blit(icon, icon.get_rect(center=(34, toast.height // 2)))
                label = title_font.render("ACHIEVEMENT UNLOCKED", True, self.theme["secondary"])
                value_text = titles.get(notice_id, "ACHIEVEMENT")
                while value_text and value_font.size(value_text)[0] > toast.width - 72:
                    value_text = value_text[:-1]
                if value_text != titles.get(notice_id, "ACHIEVEMENT"):
                    value_text = value_text[:-3].rstrip() + "..."
                value = value_font.render(value_text, True, self.theme["text"])
                toast_surface.blit(label, (64, 17))
                toast_surface.blit(value, (64, 42))
                toast_surface.set_alpha(alpha)
                self.screen.blit(toast_surface, toast.topleft)
        # ---------- Dynamic Music Volume ----------
        if self.audio_available:
            current = pygame.mixer.music.get_volume()
            target = self.music_volume
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

        self.draw_window_bar()
        self.present()

    def get_logical_mouse_pos(self):
        """Return pointer coordinates in the fixed design canvas."""
        if not self.desktop_scaled:
            return pygame.mouse.get_pos()
        x, y = self._physical_mouse_get_pos()
        render_area = self.get_render_area()
        return (
            max(0, min(WIDTH - 1, int((x - render_area.x) * WIDTH / max(1, render_area.width)))),
            max(0, min(HEIGHT - 1, int((y - render_area.y) * HEIGHT / max(1, render_area.height)))),
        )

    def get_render_area(self):
        """Largest centred rectangle that keeps the design's aspect ratio."""
        window_width, window_height = self.display_surface.get_size()
        scale = min(window_width / WIDTH, window_height / HEIGHT)
        render_width = max(1, int(WIDTH * scale))
        render_height = max(1, int(HEIGHT * scale))
        return pygame.Rect(
            (window_width - render_width) // 2,
            (window_height - render_height) // 2,
            render_width,
            render_height,
        )

    def present(self):
        """Show the canvas, proportionally scaled to the desktop window."""
        if self.desktop_scaled:
            self.display_surface = pygame.display.get_surface()
            window_size = self.display_surface.get_size()
            if window_size != self.window_size:
                self.window_size = window_size
            render_area = self.get_render_area()
            # Blend the letterbox areas into the active theme rather than
            # leaving black strips at the sides of wide displays.
            self.display_surface.fill(self.theme["background"])
            frame = pygame.transform.smoothscale(self.screen, render_area.size)
            self.display_surface.blit(frame, render_area.topleft)
        pygame.display.flip()

    def draw_window_bar(self):
        """Provide window controls only when true full-screen hides Windows' bar."""
        if not self.desktop_scaled:
            return
        bar = pygame.Rect(0, 0, WIDTH, self.window_bar_height)
        pygame.draw.rect(self.screen, self.theme["popup"], bar)
        pygame.draw.line(self.screen, self.theme["popup_border"], (0, bar.bottom - 1), (WIDTH, bar.bottom - 1), 1)
        title = self.window_bar_font.render("SUDOKU WIZARD", True, self.theme["secondary"])
        self.screen.blit(title, (16, (self.window_bar_height - title.get_height()) // 2))

        mouse = pygame.mouse.get_pos()
        controls = (
            (self.window_min_button, "-", self.theme["popup_border"]),
            (self.window_max_button, "[]", self.theme["popup_border"]),
            (self.window_close_button, "X", self.theme["accent"]),
        )
        for rect, label, hover_color in controls:
            hovered = rect.collidepoint(mouse)
            if hovered:
                pygame.draw.rect(self.screen, hover_color, rect)
            label_color = self.theme["text"]
            if rect == self.window_close_button:
                label_color = self.theme["popup"] if hovered else self.theme["accent"]
            label_surface = self.window_bar_font.render(label, True, label_color)
            self.screen.blit(label_surface, label_surface.get_rect(center=rect.center))

    def toggle_window_maximize(self):
        """Toggle reliably between monitor-filling and restored window modes."""
        if not self.desktop_scaled:
            return

        if self.is_fullscreen:
            self.display_surface = pygame.display.set_mode(
                self.windowed_size,
                pygame.RESIZABLE | pygame.NOFRAME,
            )
            self.is_fullscreen = False
        else:
            # Preserve a manually resized window for the next restore.
            self.windowed_size = self.display_surface.get_size()
            self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.is_fullscreen = True

        self.window_size = self.display_surface.get_size()
        pygame.display.set_caption("Sudoku Wizard")
        if self.window_icon is not None:
            pygame.display.set_icon(self.window_icon)
    def play_sound(self, sound):

        if self.audio_available and self.sfx_on and self.sfx_volume > 0 and sound is not None:
            sound.play()

    def toggle_notes_mode(self):
        """Toggle Pencil mode once even if Android sends a duplicate tap."""
        now = pygame.time.get_ticks()
        if now - self.last_notes_toggle_time < 350:
            return
        self.last_notes_toggle_time = now
        self.notes_mode = not self.notes_mode

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
        coins_before = self.stats.data.get("coins", 0)
        hints_before = self.stats.get_hint_tokens()
        unlocked = self.stats.record_match(
            self.difficulty,
            won,
            self.logic.score,
            self.logic.get_elapsed_time(),
            self.logic.mistakes,
            self.logic.hints_used,
            self.logic.numbers_entered,
            getattr(self.logic, "game_mode", "classic"),
        )
        if won and self.daily_challenge_active:
            claimed, daily_streak = self.stats.complete_daily_challenge()
            self.stats.record_daily_result(self.logic.score, self.logic.get_elapsed_time())
            rank = "PLATINUM" if self.logic.score >= 18_000 and self.logic.mistakes == 0 else ("GOLD" if self.logic.score >= 12_000 else ("SILVER" if self.logic.score >= 7_000 else "BRONZE"))
            if claimed:
                self.logic.score_popup_text = f"DAILY {rank}  •  +{250 + daily_streak * 25} COINS"
                self.logic.score_popup_color = self.theme["success"]
                self.logic.score_popup_time = time.time()
                self.logic.score_popup_y = 0
        # A high-scoring win may have awarded a permanent Hint Token.
        self.logic.hint_tokens = self.stats.get_hint_tokens(self.logic.difficulty)
        self.logic.auto_notes_tokens = self.stats.get_auto_notes_tokens()
        self.logic.erase_all_tokens = self.stats.get_erase_all_tokens()
        self.logic.result_rewards = {
            "coins": self.stats.data.get("coins", 0) - coins_before,
            "xp": self.stats.last_match_rewards.get("xp", 0),
            "hints": self.stats.get_hint_tokens() - hints_before,
            "auto_notes": self.stats.last_match_rewards.get("auto_notes", 0),
            "stars": self.logic.stars,
        }
        if unlocked:
            self.achievement_notice_queue.extend(unlocked)
        self.match_recorded = True
        self.delete_saved_game()

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

        self.result_music_active = False
        pygame.mixer.music.fadeout(250)
        pygame.mixer.music.load(tracks[track])
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1, fade_ms=350)
        self.current_music_track = track

    def start_result_music(self, result):
        """Play the win/loss cue once as music, then return to menu music."""
        if not self.audio_available:
            return

        result_tracks = {
            "win": "assets/sounds/win.wav",
            "lose": "assets/sounds/loose.wav",
        }
        try:
            pygame.mixer.music.fadeout(150)
            pygame.mixer.music.load(result_tracks[result])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(0)
            self.current_music_track = f"result_{result}"
            self.result_music_active = True
        except pygame.error as error:
            print("Result music disabled:", error)
            self.result_music_active = False

    def update_result_music(self):
        if (
            self.result_music_active
            and self.audio_available
            and not pygame.mixer.music.get_busy()
        ):
            self.result_music_active = False
            self.current_music_track = None
            self.play_menu_music()

    def play_menu_music(self):
        self.play_music_track("background")

    def new_game(self, difficulty, mode="classic"):
        self.win_buttons_offset = 60
        self.daily_challenge_active = False
        self.daily_challenge_date = ""
        self.difficulty = difficulty.lower()
        self.game_started = True
        self.match_recorded = False

        self.play_music_track(self.difficulty)

        self.logic = SudokuLogic(
            self.difficulty
        )
        self.logic.daily_challenge = False
        self.logic.game_mode = mode
        score_multiplier = {"classic": 1.0, "zen": 0.75, "timed": 1.5, "practice": 0.4}[mode]
        self.logic.scoring = {
            key: max(1, int(value * score_multiplier))
            for key, value in self.logic.scoring.items()
        }
        if mode == "zen":
            self.logic.mistake_limit = None
        elif mode == "practice":
            self.logic.reveal_mistakes = True
        elif mode == "timed":
            # Timed mode uses the usual Sudoku rules with a 10-minute round.
            self.logic.time_limit = 10 * 60

        self.logic.hint_tokens = self.stats.get_hint_tokens(self.difficulty)
        self.logic.auto_notes_tokens = self.stats.get_auto_notes_tokens()
        self.logic.erase_all_tokens = self.stats.get_erase_all_tokens()

        self.logic.difficulty = self.difficulty.capitalize()

        self.board.logic = self.logic

        self.board.display_score = 0
        self.win_buttons_offset = 120
        if self.audio_available:
            pygame.mixer.music.set_volume(self.music_volume)
        self.save_game_state()

    def new_daily_challenge(self):
        """Create the same Medium challenge for every player on this date."""
        # A Daily Challenge is a single attempt. A completed or failed puzzle
        # cannot be started again until the next calendar day.
        if not self.stats.begin_daily_attempt():
            return False
        self.win_buttons_offset = 60
        self.difficulty = "medium"
        self.game_started = True
        self.match_recorded = False
        self.daily_challenge_active = True
        self.daily_challenge_date = date.today().isoformat()
        random_state = random.getstate()
        random.seed(int(date.today().strftime("%Y%m%d")))
        try:
            self.logic = SudokuLogic("medium")
        finally:
            random.setstate(random_state)
        self.logic.daily_challenge = True
        self.logic.hint_tokens = self.stats.get_hint_tokens("medium")
        self.logic.auto_notes_tokens = self.stats.get_auto_notes_tokens()
        self.logic.erase_all_tokens = self.stats.get_erase_all_tokens()
        self.board.logic = self.logic
        self.board.display_score = 0
        self.play_music_track("medium")
        self.save_game_state()
        return True

    def run(self):

        while self.running:

            self.clock.tick(FPS)

            self.handle_events()

            self.draw()

            if pygame.time.get_ticks() - self.last_game_save >= 1000:
                self.save_game_state()
                self.last_game_save = pygame.time.get_ticks()

        pygame.quit()
