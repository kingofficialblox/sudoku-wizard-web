"""Game constants and responsive layout configuration."""

import os
import sys

# ==================== WINDOW ====================
PORTRAIT_MODE = (
    os.environ.get("SUDOKU_PORTRAIT") == "1"
    or sys.platform == "android"
    or "ANDROID_ARGUMENT" in os.environ
    or hasattr(sys, "getandroidapilevel")
)

WIDTH = 720 if PORTRAIT_MODE else 1450
HEIGHT = 1280 if PORTRAIT_MODE else 1040
FPS = 60

# ==================== BOARD ====================
ROWS = 9
COLS = 9
CELL_SIZE = 54 if PORTRAIT_MODE else 68

BOARD_X = (WIDTH - CELL_SIZE * 9) // 2
BOARD_Y = 555 if PORTRAIT_MODE else 265
HEADER_HEIGHT = 320 if PORTRAIT_MODE else 170
BUTTON_Y = 45

# ==================== COLORS - UI ====================
WHITE = (255, 255, 255)
BLACK = (35, 35, 35)
TEXT = (40, 40, 40)
LIGHT_TEXT = (120, 120, 120)

BACKGROUND = (235, 243, 255)
HEADER_BG = (255, 255, 255)
BOARD_BG = (255, 255, 255)
CARD = (255, 255, 255)
SHADOW = (205, 210, 220)

PRIMARY = (67, 97, 238)
PRIMARY_HOVER = (56, 87, 219)

# ==================== COLORS - BOARD ====================
HIGHLIGHT = (240, 246, 255)          # Row & Column highlight
BOX_HIGHLIGHT = (248, 250, 255)      # 3x3 box highlight
SAME_NUMBER = (232, 248, 232)        # Same number highlight

# ==================== COLORS - STATUS ====================
RED = (220, 53, 69)
GREEN = (40, 167, 69)
BLUE = (41, 98, 255)
LIGHT_BLUE = (140, 190, 255)

# ==================== ANIMATION SPEEDS ====================
ANIMATION_EASING_FACTOR = 0.22
BUTTON_HOVER_SPEED = 0.15
PAUSE_POPUP_SPEED = 0.22
CELL_SHAKE_AMOUNT = 4

# ==================== GAME SCORING ====================
SCORE_CORRECT_CELL = 100
SCORE_ROW_COMPLETE = 500
SCORE_COL_COMPLETE = 500
SCORE_BOX_COMPLETE = 1000
SCORE_PUZZLE_COMPLETE = 2000
SCORE_HINT_PENALTY = -100
SCORE_MISTAKE_PENALTY = -150

# ==================== VISUAL SETTINGS ====================
CONFETTI_COUNT = 800
