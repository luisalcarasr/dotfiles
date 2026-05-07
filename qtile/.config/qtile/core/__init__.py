"""
Core module for Qtile configuration.

This module exports all core Qtile configuration components including
groups, layouts, keybindings, mouse bindings, bar configuration,
screens, and hooks.

Example:
    >>> from core import groups, layouts, keys, mouse, screens
    >>> from core.hooks import setup_hooks
"""

from core.bar import main_bar
from core.groups import floating_layout, groups, layouts
from core.hooks import setup_hooks
from core.keys import keys, mod
from core.layouts import VerticalTile
from core.mouse import mouse
from core.screens import screens

__all__ = [
    # Groups and layouts
    "groups",
    "layouts",
    "floating_layout",
    "VerticalTile",
    # Keybindings
    "keys",
    "mod",
    # Mouse
    "mouse",
    # Bar and screens
    "main_bar",
    "screens",
    # Hooks
    "setup_hooks",
]
