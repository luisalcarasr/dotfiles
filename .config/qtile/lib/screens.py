from typing import List  # noqa: F401
from libqtile.config import Screen
from lib.bars import monitor, status, main as main_bar

screens = [
    Screen(top = main_bar),
    Screen(bottom = monitor),
    Screen(bottom = status),
]
