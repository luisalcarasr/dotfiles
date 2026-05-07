"""
Wireless network widget for Qtile.

Displays WiFi connection status using iwlib. Shows connection state
via icon color and network name on hover.

Example:
    >>> from core.widgets import Wireless
    >>> from settings.theme import Decorations
    >>>
    >>> wireless_widget = Wireless(interface='wlp3s0', **Decorations.rect())
"""

from __future__ import annotations

import logging
from typing import Any

from libqtile.widget import base

from services.network import get_wireless_status, is_wireless_connected
from settings.hardware import Network
from settings.theme import Colors

logger = logging.getLogger(__name__)

# WiFi icon
_ICON = " "


class Wireless(base.ThreadPoolText):
    """
    A widget displaying wireless network connection status.

    Features:
        - Shows WiFi icon
        - Color indicates connection state (white=connected, dark=disconnected)
        - Hover to see network name (ESSID)

    Note:
        Requires iwlib for wireless status queries.

    Attributes:
        interface: Name of the wireless network interface.

    Example:
        >>> wireless = Wireless(interface='wlp3s0')
        >>> # In bar configuration:
        >>> bar.Bar([wireless, ...], 28)
    """

    defaults: list[tuple[str, object, str]] = [
        ("update_interval", 1.0, "Update interval in seconds."),
        ("interface", Network.WIRELESS_INTERFACE, "Network interface name."),
    ]

    def __init__(self, interface: str | None = None, **config: Any) -> None:
        """
        Initialize the Wireless widget.

        Args:
            interface: Network interface name (e.g., 'wlp3s0').
                If not provided, uses the default from settings.
            **config: Widget configuration passed to ThreadPoolText.
        """
        super().__init__(_ICON, **config)
        self.add_defaults(Wireless.defaults)
        self._interface = interface or Network.WIRELESS_INTERFACE
        self._icon = _ICON

    def poll(self) -> str:
        """
        Poll for wireless status.

        Called periodically based on update_interval.

        Returns:
            The current widget text (icon).
        """
        connected = is_wireless_connected(self._interface)
        self.foreground = Colors.WHITE if connected else Colors.DARK
        return self.text

    def mouse_enter(self, *args: object, **kwargs: object) -> None:
        """Show network name on hover."""
        essid, _ = get_wireless_status(self._interface)
        if essid:
            self.update(f"{self._icon} {essid}")

    def mouse_leave(self, *args: object, **kwargs: object) -> None:
        """Return to icon-only display."""
        self.update(self._icon)
