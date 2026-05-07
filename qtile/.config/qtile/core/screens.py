"""
Screen configuration.

This module defines the screen layout including bar placement
for each monitor.

Example:
    >>> from core.screens import screens
"""

from __future__ import annotations

from libqtile.config import Screen

from core.bar import main_bar

# Screen configuration
# The main bar is placed at the bottom of the primary screen
screens: list[Screen] = [
    Screen(bottom=main_bar),
]
