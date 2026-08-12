"""Stable resource and per-user data locations for development and releases."""

import os
import sys
import json
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
WEB_MODE = sys.platform == "emscripten"
WEB_STORAGE_PREFIX = "sudoku_wizard_"


def user_file(name):
    return USER_DATA_DIR / name


def load_player_data(name):
    """Load player data from localStorage online or from disk offline."""
    try:
        if WEB_MODE:
            import platform
            raw = platform.window.localStorage.getItem(WEB_STORAGE_PREFIX + name)
            return json.loads(str(raw)) if raw else None
        with open(user_file(name), "r") as file:
            return json.load(file)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return None


def save_player_data(name, data):
    """Save player data permanently in the current browser or desktop app."""
    try:
        if WEB_MODE:
            import platform
            platform.window.localStorage.setItem(WEB_STORAGE_PREFIX + name, json.dumps(data))
            return True
        with open(user_file(name), "w") as file:
            json.dump(data, file, indent=4)
        return True
    except (OSError, TypeError, ValueError):
        return False


def delete_player_data(name):
    try:
        if WEB_MODE:
            import platform
            platform.window.localStorage.removeItem(WEB_STORAGE_PREFIX + name)
        else:
            path = user_file(name)
            if path.exists():
                path.unlink()
    except OSError:
        pass
