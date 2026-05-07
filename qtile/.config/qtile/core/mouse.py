"""
Mouse bindings configuration.

This module defines mouse actions for Qtile, primarily used for
manipulating floating windows.

Example:
    >>> from core.mouse import mouse
"""

from __future__ import annotations

from libqtile.config import Click, Drag
from libqtile.lazy import lazy

# Primary modifier key (must match keys.py)
mod = "mod4"

# Mouse bindings for floating window manipulation
mouse: list[Click | Drag] = [
    # Drag with mod + left click to move floating window
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    # Drag with mod + right click to resize floating window
    Drag(
        [mod],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    # Click with mod + middle button to bring window to front
    Click(
        [mod],
        "Button2",
        lazy.window.bring_to_front(),
    ),
]
