"""
Qtile hooks for event handling.

This module defines hooks that respond to Qtile events such as
startup and group changes. Used for multi-monitor setup and
automatic layout assignment.

Example:
    >>> from core.hooks import setup_hooks
    >>> setup_hooks()  # Called in config.py
"""

from __future__ import annotations

import logging

from libqtile import hook, qtile

from core.groups import WORKSPACE_NAMES

logger = logging.getLogger(__name__)


def _assign_groups_to_screens() -> None:
    """
    Assign specific workspace groups to screens on startup.

    For multi-monitor setups, this assigns:
    - Last workspace (0) to screen 3
    - Second to last workspace (9) to screen 2

    This is only applied when more than one screen is connected.
    """
    if len(qtile.screens) <= 1:
        return

    try:
        # Assign last workspace to screen 3 (index 2)
        qtile.groups_map[WORKSPACE_NAMES[-1]].cmd_toscreen(2, toggle=False)
        # Assign second-to-last workspace to screen 2 (index 1)
        qtile.groups_map[WORKSPACE_NAMES[-2]].cmd_toscreen(1, toggle=False)
    except (KeyError, IndexError) as e:
        logger.warning(f"Failed to assign groups to screens: {e}")


def _apply_screen_layouts() -> None:
    """
    Apply specific layouts to each screen.

    Layout assignments:
    - Screen 1 (index 0): Layout 0 (MonadTall)
    - Screen 2 (index 1): Layout 1 (VerticalTile)
    - Screen 3 (index 2): Layout 1 (VerticalTile)

    This creates a workflow where the main screen uses horizontal
    tiling while secondary screens use vertical tiling.
    """
    if len(qtile.screens) <= 1:
        return

    try:
        qtile.screens[0].group.use_layout(0)  # MonadTall
        qtile.screens[1].group.use_layout(1)  # VerticalTile
        qtile.screens[2].group.use_layout(1)  # VerticalTile
    except (IndexError, AttributeError) as e:
        logger.debug(f"Could not apply screen layouts: {e}")


@hook.subscribe.startup
def on_startup() -> None:
    """
    Hook called when Qtile starts.

    Performs initial screen and group setup for multi-monitor configurations.
    """
    _assign_groups_to_screens()


@hook.subscribe.startup
@hook.subscribe.setgroup
def on_group_change() -> None:
    """
    Hook called on startup and when the active group changes.

    Ensures each screen maintains its preferred layout.
    """
    _apply_screen_layouts()


def setup_hooks() -> None:
    """
    Placeholder function to ensure hooks module is imported.

    The hooks are registered automatically when this module is imported
    via the @hook.subscribe decorators. This function exists to make
    the import explicit in config.py.

    Example:
        >>> from core.hooks import setup_hooks
        >>> setup_hooks()  # Ensures hooks are registered
    """
    logger.debug("Hooks module loaded and registered")
