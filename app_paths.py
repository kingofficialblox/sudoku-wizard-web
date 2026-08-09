"""Stable resource and per-user data locations for development and releases."""

import os
import sys
from pathlib import Path


APP_FOLDER_NAME = "Sudoku Wizard"


def resource_dir():
    """Return the source/assets directory, including inside a PyInstaller app."""
    bundled = getattr(sys, "_MEIPASS", None)
    return Path(bundled) if bundled else Path(__file__).resolve().parent


def user_data_dir():
    """Return a writable, private folder for the current player's progress."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    target = base / APP_FOLDER_NAME
    target.mkdir(parents=True, exist_ok=True)
    return target


RESOURCE_DIR = resource_dir()
USER_DATA_DIR = user_data_dir()


def user_file(name):
    return USER_DATA_DIR / name
