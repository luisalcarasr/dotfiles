from typing import List  # noqa: F401
from lib.shortcuts import keys, mouse
from lib.workspaces import groups, layouts, floating_layout
from lib.defaults import defaults, mod
from lib.screens import screens
import lib.hooks

widget_defaults = defaults.copy()
extension_defaults = defaults.copy()

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = False
