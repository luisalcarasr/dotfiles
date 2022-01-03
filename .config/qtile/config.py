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
    font='CaskaydiaCove Nerd Font',
    fontsize=14,
    padding=0,
    foreground=colors["white"]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                # Arch Logo
                widget.Sep(padding=16, background=colors["blue"], foreground=colors["blue"]),
                widget.TextBox("", fontsize=18, background=colors["blue"], foreground=colors["black"], padding=8),
                widget.TextBox("luis@arch", background=colors["blue"], foreground=colors["black"], padding=8),

                # Laucher
                widget.TextBox("\u25e3", foreground=colors["blue"], background=colors["green"], fontsize=64, padding=-1),
                widget.TextBox("", fontsize=18, background=colors["green"], foreground=colors["black"], padding=8),
                widget.Prompt(prompt=' ', background=colors["green"], foreground=colors['black'], cursor_color=colors['black']),
                widget.TextBox("\u25e3", foreground=colors["green"], background=colors["black"],fontsize=64, padding=-1),

                widget.Spacer(),
                widget.GroupBox(
                    highlight_color=colors["dark"],
                    highlight_method="line",
                    highlight_border=colors["blue"],
                    urgent_alert_method="line",
                    urgent_text=colors["red"],
                    inactive=colors["white"],
                    active=colors["blue"],
                    fontsize=16
                ),
                widget.Spacer(),

                # Systray
                widget.Systray(icon_size=18, padding=8),

                # Bluetooth
                widget.TextBox("\u25e2", foreground=colors["aqua"], background=colors["black"],fontsize=64, padding=-0.1),
                widget.TextBox("", foreground=colors["black"], background=colors["aqua"], fontsize=18, padding=16),
                widget.Bluetooth(background=colors["aqua"], foreground=colors["black"]),

                # Disk
                widget.TextBox("\u25e2", foreground=colors["green"], background=colors["aqua"],fontsize=64, padding=-0.1),
                widget.TextBox("", foreground=colors["black"], background=colors["green"], fontsize=18, padding=16),
                widget.DF(format="{r:.1f}%",background=colors["green"], foreground=colors["black"], visible_on_warn=False),

                # Clock
                widget.TextBox("\u25e2", foreground=colors["blue"], background=colors["green"],fontsize=64, padding=-0.1),
                widget.TextBox("", foreground=colors["black"], background=colors["blue"], fontsize=18, padding=16),
                widget.Clock(format='%H:%M', background=colors["blue"], foreground=colors["black"]),
                widget.Sep(padding=16, background=colors["blue"], foreground=colors["blue"]),
            ],
            24,
            background=colors["black"]
        ),
        bottom=bar.Bar(
            [
                # Wi-Fi
                widget.Sep(padding=16, background=colors["blue"], foreground=colors["blue"]),
                widget.TextBox("", fontsize=18, background=colors["blue"], foreground=colors["black"], padding=16),
                # widget.Wlan(format="{essid}", foreground=colors["black"], background=colors["blue"], interface="wlp2s0"),
                Wireless(foreground=colors["black"], background=colors["blue"], interface="wlo1"),

                # Uploadl Speed
                widget.TextBox("\u25e3", foreground=colors["blue"], background=colors["green"], fontsize=64, padding=-1),
                widget.TextBox("", fontsize=18, background=colors["green"], foreground=colors["black"], padding=16),
                widget.Net(format="{up}/s", foreground=colors["black"], background=colors["green"]),

                # Download Speed
                widget.TextBox("\u25e3", foreground=colors["green"], background=colors["yellow"],fontsize=64, padding=-1),
                widget.TextBox("", fontsize=18, background=colors["yellow"], foreground=colors["black"], padding=16),
                widget.Net(format="{down}/s", foreground=colors["black"], background=colors["yellow"]),

                # IP
                widget.TextBox("\u25e3", foreground=colors["yellow"], background=colors["aqua"], fontsize=64, padding=-1),
                widget.TextBox("歷", foreground=colors["black"], background=colors["aqua"],fontsize=18, padding=16),
                widget.TextBox(extract_ip(), foreground=colors["black"], background=colors["aqua"]),
                widget.TextBox("\u25e3", foreground=colors["aqua"], fontsize=64, padding=-1),

                widget.Spacer(),
                widget.Spacer(),

                # Battery
                widget.TextBox("\u25e2", foreground=colors["aqua"], background=colors["black"], fontsize=64, padding=-0.1),
                widget.Battery(format="{char}", fontsize=18, padding=16, background=colors["aqua"], foreground=colors["black"], low_foreground=colors["red"], full_char="", charge_char="", discharge_char="", empty_char="", unknown_char="", show_short_text=False),
                widget.Battery(format="{percent:2.0%}",background=colors["aqua"], foreground=colors["black"], low_foreground=colors["red"], show_short_text=False),
                widget.TextBox("\u25e2", foreground=colors["yellow"], background=colors["aqua"], fontsize=64, padding=-0.1),

                # Thermal
                widget.TextBox("", foreground=colors["black"], background=colors["yellow"],fontsize=18, padding=16),
                widget.ThermalSensor(foreground=colors["black"], background=colors["yellow"]),
                widget.TextBox("\u25e2", foreground=colors["green"], background=colors["yellow"],fontsize=64, padding=-0.1),

                # RAM
                widget.TextBox("", foreground=colors["black"], background=colors["green"], fontsize=18, padding=16),
                widget.Memory(format="{MemPercent}%", foreground=colors["black"], background=colors["green"]),
                widget.TextBox("\u25e2", foreground=colors["blue"], background=colors["green"],fontsize=64, padding=-0.1),

                # CPU
                widget.TextBox("﬙", foreground=colors["black"], background=colors["blue"], fontsize=18, padding=16),
                widget.CPU(format="{load_percent}%",background=colors["blue"], foreground=colors["black"]),
                widget.Sep(padding=16, background=colors["blue"], foreground=colors["blue"]),
            ],
            24,
            background=colors["black"]
        ) if device == "mobile" else None,
    ),
    Screen(
        top=bar.Bar(
            [
                # Intel Logo
                widget.Sep(padding=16, background=colors["light"], foreground=colors["light"]),
                widget.Image(filename='~/intel.svg', background=colors["light"], margin=5),

                # CPU
                widget.TextBox("\u25e3", foreground=colors["light"], background=colors["blue"], fontsize=64, padding=-1),
                widget.TextBox("﬙", foreground=colors["black"], background=colors["blue"], fontsize=18, padding=16),
                widget.CPU(format="{load_percent}%",background=colors["blue"], foreground=colors["black"]),

                # Thermal
                widget.TextBox("\u25e3", foreground=colors["blue"], background=colors["yellow"],fontsize=64, padding=-1),
                widget.TextBox("", foreground=colors["black"], background=colors["yellow"],fontsize=18, padding=16),
                widget.ThermalSensor(foreground=colors["black"], background=colors["yellow"]),

                # RAM
                widget.TextBox("\u25e3", foreground=colors["yellow"], background=colors["aqua"], fontsize=64, padding=-1),
                widget.TextBox("", foreground=colors["black"], background=colors["aqua"],fontsize=18, padding=16),
                widget.Memory(format="{MemPercent}%", foreground=colors["black"], background=colors["aqua"]),
                widget.TextBox("\u25e3", foreground=colors["aqua"], fontsize=64, padding=-0.1),

                widget.Spacer(),
                widget.GroupBox(
                    highlight_color=colors["dark"],
                    highlight_method="line",
                    highlight_border=colors["blue"],
                    urgent_alert_method="line",
                    urgent_text=colors["red"],
                    inactive=colors["white"],
                    active=colors["blue"],
                    fontsize=16
                ),
                widget.Spacer(),

                # Clock
                widget.TextBox("\u25e2", foreground=colors["blue"], background=colors["black"],fontsize=64, padding=-0.1),
                widget.TextBox("", foreground=colors["black"], background=colors["blue"], fontsize=18, padding=16),
                widget.Clock(format='%H:%M', background=colors["blue"], foreground=colors["black"]),
                widget.Sep(padding=16, background=colors["blue"], foreground=colors["blue"]),
            ],
            24,
            background=colors["black"]
        ) if device != "mobile" else None
    ),
    Screen(
        top=bar.Bar(
            [
                # Wi-Fi
                widget.Sep(padding=16, background=colors["blue"], foreground=colors["blue"]),
                widget.TextBox("  ", fontsize=18, background=colors["blue"], foreground=colors["black"]),
                widget.Wlan(format="{essid}", foreground=colors["black"], background=colors["blue"], interface="wlp2s0"),

                # Upload Speed
                widget.TextBox("\u25e3", foreground=colors["blue"], background=colors["green"], fontsize=64, padding=-1),
                widget.TextBox("", fontsize=18, background=colors["green"], foreground=colors["black"], padding=16),
                widget.Net(format="{up}/s", foreground=colors["black"], background=colors["green"]),

                # Download Speed
                widget.TextBox("\u25e3", foreground=colors["green"], background=colors["yellow"],fontsize=64, padding=-1),
                widget.TextBox("", fontsize=18, background=colors["yellow"], foreground=colors["black"], padding=16),
                widget.Net(format="{down}/s", foreground=colors["black"], background=colors["yellow"]),

                # IP
                widget.TextBox("\u25e3", foreground=colors["yellow"], background=colors["aqua"], fontsize=64, padding=-1),
                widget.TextBox("歷", foreground=colors["black"], background=colors["aqua"],fontsize=18, padding=16),
                widget.TextBox(extract_ip(), foreground=colors["black"], background=colors["aqua"]),
                widget.TextBox("\u25e3", foreground=colors["aqua"], fontsize=64, padding=-0.1),

                widget.Spacer(),
                widget.GroupBox(
                    highlight_color=colors["dark"],
                    highlight_method="line",
                    highlight_border=colors["blue"],
                    urgent_alert_method="line",
                    urgent_text=colors["red"],
                    inactive=colors["white"],
                    active=colors["blue"],
                    fontsize=16
                ),
                widget.Spacer(),


                # VRAM
                widget.TextBox("\u25e2", foreground=colors["aqua"], fontsize=64, padding=-0.1),
                widget.TextBox("", foreground=colors["black"], background=colors["aqua"],fontsize=18, padding=16),
                VRAM(foreground=colors["black"], background=colors["aqua"]),
                widget.TextBox("\u25e2", foreground=colors["yellow"], background=colors["aqua"], fontsize=64, padding=-0.1),

                # Thermal
                widget.TextBox("", foreground=colors["black"], background=colors["yellow"],fontsize=18, padding=16),
                widget.NvidiaSensors(format="{temp}°C", foreground=colors["black"], background=colors["yellow"]),
                widget.TextBox("\u25e2", foreground=colors["green"], background=colors["yellow"],fontsize=64, padding=-0.1),

                # GPU
                widget.TextBox("﬙", foreground=colors["black"], background=colors["green"], fontsize=18, padding=16),
                # widget.NvidiaSensors(format="{temp}°C " + str(get_used_gpu()) + "%", foreground=colors["black"], background=colors["yellow"]),
                GPU(foreground=colors["black"], background=colors["green"]),
                widget.TextBox("\u25e2", foreground=colors["light"], background=colors["green"],fontsize=64, padding=-0.1),

                # Nvidia Logo
                widget.Image(filename='~/nvidia.svg', background=colors["light"], margin=5),
                widget.Sep(padding=16, background=colors["light"], foreground=colors["light"]),
            ],
            24,
            background=colors["black"]
        ) if device != "mobile" else None,
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
