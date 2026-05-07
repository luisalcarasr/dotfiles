"""
Status bar configuration.

This module defines the status bar (panel) layout including all widgets
and their configuration.

Example:
    >>> from core.bar import main_bar
    >>> screen = Screen(bottom=main_bar)
"""

from __future__ import annotations

import logging

from libqtile import bar
from qtile_extras import widget

from core import widgets as custom
from services.system import can_control_brightness, has_battery
from settings.hardware import Display, Network
from settings.theme import Colors, Decorations

logger = logging.getLogger(__name__)

# Shared decoration configuration
_decor = Decorations.rect()


def _create_separator(padding: int = 8) -> widget.Sep:
    """Create an invisible separator widget."""
    return widget.Sep(padding=padding, foreground=Colors.BLACK)


def _create_volume_widget() -> widget.base._Widget:
    """
    Create the volume widget with fallback.

    Returns:
        Volume widget or empty TextBox on failure.
    """
    try:
        return custom.Volume(**_decor)
    except Exception as e:
        logger.warning(f"Failed to create Volume widget: {e}")
        return widget.TextBox("")


def _create_brightness_widgets() -> list[widget.base._Widget]:
    """
    Create brightness control widgets if available.

    Returns:
        List of widgets (empty if brightness control unavailable).
    """
    if not can_control_brightness:
        return []

    return [
        widget.WidgetBox(
            text_closed=" ",
            text_open=" ",
            widgets=[
                widget.Backlight(
                    backlight_name=Display.BACKLIGHT_NAME,
                    change_command="brightnessctl set {0}%",
                    brightnessfile=Display.BACKLIGHT_PATH,
                    max_brightness_file=Display.MAX_BRIGHTNESS_PATH,
                ),
            ],
        ),
        _create_separator(padding=12),
    ]


def _create_battery_widgets() -> list[widget.base._Widget]:
    """
    Create battery widgets if available.

    Returns:
        List of widgets (empty if no battery present).
    """
    if not has_battery:
        return []

    return [
        widget.WidgetBox(
            text_closed="  ",
            text_open="  ",
            widgets=[
                widget.Battery(
                    format="{percent:2.1%}",
                    low_foreground=Colors.RED,
                    show_short_text=False,
                ),
            ],
        ),
        _create_separator(),
    ]


# Build the main bar widget list
_widgets: list[widget.base._Widget] = [
    # Left section: Padding and workspaces
    _create_separator(),
    widget.GroupBox(
        highlight_method="text",
        urgent_text=Colors.RED,
        foreground=Colors.WHITE,
        active=Colors.LIGHT,
        inactive=Colors.DARK,
        this_current_screen_border=Colors.WHITE,
        other_current_screen_border=Colors.WHITE,
        margin_x=0,
        margin_y=3,
        border=10,
        **_decor,
    ),
    _create_separator(),

    # Center section: Spacer
    widget.Spacer(),

    # Right section: System widgets
    widget.Systray(icon_size=18),
    _create_separator(padding=16),

    # Pomodoro timer
    widget.Pomodoro(
        prefix_active="",
        prefix_inactive="0:00:00",
        prefix_long_break="",
        prefix_break="",
        prefix_paused="PAUSED",
        color_active=Colors.WHITE,
        color_break=Colors.GREEN,
        color_inactive=Colors.DARK,
        **_decor,
    ),
    _create_separator(),

    # Bluetooth
    custom.Bluetooth(**_decor),
    _create_separator(),

    # Wireless
    custom.Wireless(interface=Network.WIRELESS_INTERFACE, **_decor),
    _create_separator(),

    # Volume
    _create_volume_widget(),
    _create_separator(),
]

# Add conditional widgets
_widgets.extend(_create_brightness_widgets())
_widgets.extend(_create_battery_widgets())

# Clock (always last)
_widgets.extend([
    widget.Clock(format="%H:%M", **_decor),
    _create_separator(),
])

# Create the main bar
main_bar = bar.Bar(
    _widgets,
    size=28,
    background=Colors.BLACK,
    border_width=1,
)
