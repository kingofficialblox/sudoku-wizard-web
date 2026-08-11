"""Game constants and responsive layout configuration."""

import os
import sys

APP_VERSION = "1.0.0"

# ==================== WINDOW ====================
WEB_MODE = sys.platform == "emscripten"
PORTRAIT_MODE = (
    os.environ.get("SUDOKU_PORTRAIT") == "1"
    or sys.platform == "android"
    or "ANDROID_ARGUMENT" in os.environ
    or hasattr(sys, "getandroidapilevel")
)

# 20:9 is the common modern phone layout.  Pydroid renders directly into this
# portrait canvas, keeping the board square while using the full screen.
WIDTH = 720 if PORTRAIT_MODE else 1450
# The desktop UI ends just below the board at roughly 880 px. Keeping a
# 1040 px design canvas only added unused space and forced the entire game to
# shrink on common 900/1080 px monitors. This near-16:10 canvas fills laptop
# and desktop displays much more naturally while still scaling proportionally.
HEIGHT = 1600 if PORTRAIT_MODE else 900
# Phones benefit more from stable frame pacing than from a costly 60 FPS draw.
# A steady 30 FPS is substantially smoother than dropped frames on Pydroid.
FPS = 30 if PORTRAIT_MODE else 60

# ==================== BOARD ====================
ROWS = 9
COLS = 9
CELL_SIZE = 60 if PORTRAIT_MODE else 62

BOARD_X = (WIDTH - CELL_SIZE * 9) // 2
BOARD_Y = 400 if PORTRAIT_MODE else 235
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
CONFETTI_COUNT = 8 if PORTRAIT_MODE else 800
