"""
Qtile Window Manager Configuration.

This is the main configuration file for Qtile. It imports all components
from the modular configuration and exports them for Qtile to use.

Configuration Structure:
    settings/   - User-configurable settings (theme, apps, hardware)
    core/       - Core Qtile components (keys, layouts, bar, etc.)
    services/   - System service interfaces (audio, bluetooth, etc.)
    menus/      - Rofi menu integrations

For customization, see:
    - settings/theme.py    - Colors, fonts, decorations
    - settings/apps.py     - Default applications
    - settings/hardware.py - Hardware-specific settings
    - core/keys.py         - Keyboard shortcuts

Author: Luis Alcaras
License: MIT
"""

from __future__ import annotations

# Import all Qtile configuration components
from core import (
    floating_layout,
    groups,
    keys,
    layouts,
    mod,
    mouse,
    screens,
    setup_hooks,
)
from settings.theme import Colors, Fonts

# =============================================================================
# Widget Defaults
# =============================================================================

widget_defaults: dict[str, object] = {
    "font": Fonts.DEFAULT,
    "fontsize": Fonts.SIZE,
    "padding": 8,
    "borderwidth": 0,
    "foreground": Colors.WHITE,
}

extension_defaults = widget_defaults.copy()

# =============================================================================
# Qtile Behavior Settings
# =============================================================================

# Group key binder (None = use manual keybindings from core/keys.py)
dgroups_key_binder = None

# Rules for automatically assigning windows to groups
dgroups_app_rules: list = []

# Mouse focus behavior
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

# Window behavior
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = False

# WM name (for compatibility with some applications)
wmname = "LG3D"

# =============================================================================
# Initialize Hooks
# =============================================================================

# Ensure hooks module is loaded and hooks are registered
setup_hooks()

# =============================================================================
# Exports for Qtile
# =============================================================================

# These variables are read by Qtile:
# - keys: Keyboard shortcuts
# - mouse: Mouse bindings
# - groups: Workspace groups
# - layouts: Available window layouts
# - floating_layout: Rules for floating windows
# - screens: Screen configuration with bars
# - widget_defaults: Default widget settings
# - extension_defaults: Default extension settings

__all__ = [
    "keys",
    "mouse",
    "groups",
    "layouts",
    "floating_layout",
    "screens",
    "widget_defaults",
    "extension_defaults",
    "dgroups_key_binder",
    "dgroups_app_rules",
    "follow_mouse_focus",
    "bring_front_click",
    "cursor_warp",
    "auto_fullscreen",
    "focus_on_window_activation",
    "reconfigure_screens",
    "auto_minimize",
    "wmname",
]
