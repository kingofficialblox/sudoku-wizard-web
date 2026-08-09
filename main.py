#Pydroid run pygame
# The directive above must stay on the first line.  It tells Pydroid to create
# its Android SDL/Pygame surface instead of using the generic script runner.

import os
import sys

from app_paths import RESOURCE_DIR

# Pydroid may launch a script with a different working directory.
# Anchor all relative assets and save files to the project folder.
PROJECT_DIR = RESOURCE_DIR
os.chdir(PROJECT_DIR)
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from game import Game

game = Game()
game.run()
