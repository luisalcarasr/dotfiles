from typing import List  # noqa: F401
from libqtile.config import Screen
from lib.bars import main

screens = [
    Screen(bottom = main),
]
