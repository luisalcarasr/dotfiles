"""
Custom layouts for Qtile.

This module contains custom layout implementations that extend
the base Qtile layouts with additional features.

Example:
    >>> from core.layouts import VerticalTile
    >>> layout = VerticalTile(margin=16, border_width=1)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from libqtile.layout.verticaltile import VerticalTile as BaseVerticalTile

if TYPE_CHECKING:
    from libqtile.backend.base import Window
    from libqtile.config import ScreenRect


class VerticalTile(BaseVerticalTile):
    """
    Enhanced vertical tiling layout.

    This layout arranges windows vertically with an optional maximized
    window that takes up more space. It improves on the base VerticalTile
    by providing proper margin handling for single windows and better
    spacing between windows.

    Features:
        - Vertical window stacking
        - Maximized window support (main window gets more space)
        - Smart margins (no margins for single window)
        - Proper border handling

    Attributes:
        ratio: Ratio of screen height for the maximized window (default: 0.65).
        margin: Margin around windows in pixels.
        single_margin: Margin when only one window (None = no margin).
        border_width: Border width for multiple windows.
        single_border_width: Border width for single window.

    Example:
        >>> layout = VerticalTile(
        ...     margin=16,
        ...     border_width=1,
        ...     border_focus="#41a7fc",
        ...     border_normal="#282C34",
        ... )
    """

    def configure(self, window: Window, screen_rect: ScreenRect) -> None:
        """
        Configure window position and size within the layout.

        Args:
            window: The window to configure.
            screen_rect: The available screen area.
        """
        if not self.clients or window not in self.clients:
            window.hide()
            return

        n = len(self.clients)
        index = self.clients.index(window)

        # Determine border width
        border_width = self.border_width if n > 1 else self.single_border_width

        # Determine margin
        if n == 1 and self.single_margin is not None:
            margin: int | list[int] = self.single_margin
        else:
            m = self.margin
            # Bottom margin only for last window, creates visual gap
            margin = [m, m, m if index == n - 1 else 0, m]

        # Determine border color
        border_color = self.border_focus if window.has_focus else self.border_normal

        # Calculate width (full width minus borders)
        if n > 1:
            width = screen_rect.width - border_width * 2
        else:
            width = screen_rect.width

        # Calculate height based on maximized state
        if n > 1:
            main_area_height = int(screen_rect.height * self.ratio)
            sec_area_height = screen_rect.height - main_area_height

            main_pane_height = main_area_height - border_width * 2
            sec_pane_height = sec_area_height // (n - 1) - border_width * 2
            normal_pane_height = (screen_rect.height // n) - (border_width * 2)

            if self.maximized:
                if window is self.maximized:
                    height = main_pane_height
                else:
                    height = sec_pane_height
            else:
                height = normal_pane_height
        else:
            height = screen_rect.height

        # Calculate Y position
        y = screen_rect.y

        if n > 1:
            if self.maximized:
                y += (index * sec_pane_height) + (border_width * 2 * index)
            else:
                y += (index * normal_pane_height) + (border_width * 2 * index)

            # Adjust Y for windows below the maximized one
            if self.maximized and window is not self.maximized:
                if index > self.clients.index(self.maximized):
                    y = y - sec_pane_height + main_pane_height

        # Place and show the window
        window.place(
            screen_rect.x,
            y,
            width,
            height,
            border_width,
            border_color,
            margin=margin,
        )
        window.unhide()
