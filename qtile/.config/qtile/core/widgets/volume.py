"""
Volume widget for Qtile.

Displays and controls the system audio volume using PulseAudio.
Supports mouse wheel for volume adjustment and click for mute toggle.

Example:
    >>> from core.widgets import Volume
    >>> from settings.theme import Decorations
    >>>
    >>> volume_widget = Volume(**Decorations.rect())
"""

from __future__ import annotations

import logging

from libqtile.widget.base import _TextBox

from services.audio import OutputAudio
from settings.theme import Colors

logger = logging.getLogger(__name__)

# Icons for volume states
_ICON_DEFAULT = " "
_ICON_MUTED = " "


class Volume(_TextBox):
    """
    A widget displaying current volume level with interactive controls.

    Features:
        - Shows volume icon (speaker or muted)
        - Hover to see volume percentage
        - Left click to toggle mute
        - Scroll wheel to adjust volume

    Mouse Bindings:
        - Button1 (left click): Toggle mute
        - Button4 (scroll up): Volume up 5%
        - Button5 (scroll down): Volume down 5%

    Attributes:
        output: OutputAudio instance for controlling PulseAudio.

    Example:
        >>> volume = Volume()
        >>> # In bar configuration:
        >>> bar.Bar([volume, ...], 28)
    """

    defaults: list[tuple[str, object, str]] = [
        ("update_interval", 1.0, "Update interval in seconds."),
    ]

    def __init__(self, **config: object) -> None:
        """
        Initialize the Volume widget.

        Args:
            **config: Widget configuration passed to _TextBox.
        """
        self._output = OutputAudio()
        super().__init__(self._icon, **config)
        self.add_defaults(Volume.defaults)
        self._update_foreground()
        self._output.on_init(self.mouse_leave)
        self.add_callbacks({
            "Button1": self._toggle_mute,
            "Button4": self._volume_up,
            "Button5": self._volume_down,
        })

    @property
    def _icon(self) -> str:
        """Get the appropriate volume icon based on mute state."""
        return _ICON_MUTED if self._output.is_muted() else _ICON_DEFAULT

    def _draw_volume(self) -> None:
        """Update the widget to show volume percentage."""
        self._update_foreground()
        volume_percent = int(self._output.volume * 100)
        self.update(f"{self._icon} {volume_percent}%")

    def mouse_enter(self, *args: object, **kwargs: object) -> None:
        """Show volume percentage on hover."""
        self._draw_volume()

    def mouse_leave(self, *args: object, **kwargs: object) -> None:
        """Return to icon-only display when mouse leaves."""
        self._update_foreground()
        self.update(self._icon)

    def _volume_up(self) -> None:
        """Increase volume by 5%."""
        self._output.volume_up()
        self._draw_volume()

    def _volume_down(self) -> None:
        """Decrease volume by 5%."""
        self._output.volume_down()
        self._draw_volume()

    def _toggle_mute(self) -> None:
        """Toggle mute state."""
        self._output.toggle_mute()
        self._update_foreground()
        self._draw_volume()

    def _update_foreground(self) -> None:
        """Update text color based on volume/mute state."""
        if self._output.is_muted():
            self.foreground = Colors.RED
        elif self._output.volume <= 0:
            self.foreground = Colors.DARK
        else:
            self.foreground = Colors.WHITE
