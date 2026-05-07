"""
VPN status widget for Qtile.

Displays VPN connection status using NetworkManager D-Bus interface.
Color indicates connection state.

Example:
    >>> from core.widgets import VPN
    >>> from settings.theme import Decorations
    >>>
    >>> vpn_widget = VPN(**Decorations.rect())
"""

from __future__ import annotations

import logging
from typing import Any

from libqtile.widget import base

from services.network import is_vpn_connected
from settings.theme import Colors

logger = logging.getLogger(__name__)

# VPN icon
_ICON = "嬨"


class VPN(base.ThreadPoolText):
    """
    A widget displaying VPN connection status.

    Features:
        - Shows VPN icon
        - Color indicates connection state (white=connected, dark=disconnected)

    Note:
        Requires NetworkManager and dbus-python for VPN status detection.

    Example:
        >>> vpn = VPN()
        >>> # In bar configuration:
        >>> bar.Bar([vpn, ...], 28)
    """

    defaults: list[tuple[str, object, str]] = [
        ("update_interval", 1.0, "Update interval in seconds."),
    ]

    def __init__(self, **config: Any) -> None:
        """
        Initialize the VPN widget.

        Args:
            **config: Widget configuration passed to ThreadPoolText.
        """
        super().__init__(_ICON, **config)
        self.add_defaults(VPN.defaults)
        self._icon = _ICON

    def poll(self) -> str:
        """
        Poll for VPN status.

        Called periodically based on update_interval.

        Returns:
            The VPN icon.
        """
        connected = is_vpn_connected()
        self.foreground = Colors.WHITE if connected else Colors.DARK
        return self._icon
