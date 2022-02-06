# Copyright (c) 2021-2022 Luis Alcaras
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import environ 
from typing import List  # noqa: F401
from libqtile import bar, widget
from libqtile.config import Screen


device = environ.get("DEVICE")
mod = "mod4"

from utils.theme import colors
from utils.network import extract_ip
from lib.widgets import GPU, VRAM, Wireless
from shortcuts import keys, mouse
from workspaces import groups, layouts, floating_layout

widget_defaults = dict(
    font='Cantarell Bold',
    fontsize=14,
    padding=8,
    borderwidth=0,
    foreground=colors["white"]
)
extension_defaults = widget_defaults.copy()

nerd_font = 'BlexMono Nerd Font'

screens = [
    Screen(
        top=bar.Bar(
            [
                # Arch Logo
                widget.Sep(padding=8, foreground=colors["black"]),
                widget.TextBox("", foreground=colors["blue"], fontsize=18, font=nerd_font),

                # Workspace
                widget.Sep(padding=8, foreground=colors["black"]),
                widget.GroupBox(
                    highlight_method="text",
                    urgent_text=colors["red"],
                    foreground=colors["white"],
                    active=colors["light"],
                    inactive=colors["dark"],
                    this_current_screen_border=colors["white"],
                    other_current_screen_border=colors["white"],
                    borderwidth=0,
                ),
                widget.Spacer(),

                # Background Applications
                widget.Systray(icon_size=20),
                widget.Sep(padding=16, foreground=colors["black"]),
                
                # Volume
                widget.WidgetBox(
                    text_closed=" ",
                    text_open=" ",
                    font=nerd_font,
                    widgets=[
                        widget.PulseVolume(
                            limit_max_volume=True,
                            fontsize=12,
                        ),
                    ],
                ),
                widget.Sep(padding=12, foreground=colors["black"]),

                # Brightness
                widget.WidgetBox(
                    text_closed=" ",
                    text_open=" ",
                    font=nerd_font,
                    widgets=[
                        widget.Backlight(
                            backlight_name='intel_backlight',
                            change_command='brightnessctl set {0}%',
                            brightnessfile='/sys/class/backlight/intel_backlight/brightness',
                            max_brightness_file='/sys/class/backlight/intel_backlight/max_brightness',
                            fontsize=12,
                        ),
                    ],
                ),
                widget.Sep(padding=12, foreground=colors["black"]),

                # Battery
                widget.WidgetBox(
                    text_closed="  ",
                    text_open="  ",
                    font=nerd_font,
                    widgets=[
                        widget.Battery(
                            format="{percent:2.1%}",
                            low_foreground=colors["red"],
                            show_short_text=False,
                            fontsize=12,
                        ),
                    ],
                ),
                widget.Sep(padding=8, foreground=colors["black"]),

                # Clock
                widget.Clock(format='%a %d  %H:%M'),
                widget.Sep(padding=8, foreground=colors["black"]),
            ],
            32,
            background=colors["black"]
        ),
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
