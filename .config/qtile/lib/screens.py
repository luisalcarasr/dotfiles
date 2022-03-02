from typing import List  # noqa: F401
from libqtile.config import Screen
from lib.bars import main as main_bar

screens = [
    Screen(
        top = main_bar,
    ),
]
