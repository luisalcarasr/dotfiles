from typing import List  # noqa: F401
from libqtile.config import Screen
from lib.bars import main as main_bar

screens = [
    Screen(
        bottom = main_bar,
    ),
]
