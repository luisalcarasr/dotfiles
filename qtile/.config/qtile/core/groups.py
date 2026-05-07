"""
Workspace groups and layouts configuration.

This module defines the workspace groups (virtual desktops) and
the layouts available for window arrangement.

Example:
    >>> from core.groups import groups, layouts, floating_layout
"""

from __future__ import annotations

from libqtile import layout
from libqtile.config import Group, Match

from core.layouts import VerticalTile
from settings.theme import Colors

# Generate workspace names: "1", "2", ..., "9", "0"
WORKSPACE_NAMES: list[str] = [str(i) if i != 10 else "0" for i in range(1, 11)]

# Create groups with empty labels (icon-only in bar)
groups: list[Group] = [Group(name=ws, label="") for ws in WORKSPACE_NAMES]

# Layout configuration shared between all layouts
_LAYOUT_DEFAULTS = {
    "border_focus": Colors.PRIMARY,
    "border_normal": Colors.DARK,
    "border_width": 1,
    "margin": 16,
    "single_border_width": 0,
    "single_margin": 0,
}

# Available layouts
layouts: list[layout.base.Layout] = [
    layout.MonadTall(**_LAYOUT_DEFAULTS),
    VerticalTile(**_LAYOUT_DEFAULTS),
]

# Floating layout with rules for specific windows
floating_layout = layout.Floating(
    float_rules=[
        # Default float rules from Qtile
        *layout.Floating.default_float_rules,
        # Git tools
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(title="branchdialog"),
        # Authentication dialogs
        Match(wm_class="ssh-askpass"),
        Match(title="pinentry"),
        # Gaming - Origin launcher
        Match(wm_class="steam_app_1182480", title="Origin"),
        # Generic Steam apps
        Match(wm_class="steam_app_*"),
    ],
    border_focus=Colors.PRIMARY,
    border_normal=Colors.DARK,
    border_width=1,
)
