# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2021 Luis Alcaras
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

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.

    Key([mod], "i", lazy.to_screen(2)),
    Key([mod], "o", lazy.to_screen(0)),
    Key([mod], "p", lazy.to_screen(1)),

    Key([mod], "comma", lazy.prev_screen()),
    Key([mod], "period", lazy.next_screen()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "space", lazy.spawn('rofi -show drun -show-icons'), desc="Spawn a command using a prompt widget"),
]

groups = [
    Group('   '),
    Group('   '),
    Group('   '),
    Group('   '),
    Group('   '),
    Group('   '),
    Group('   '),
]

keys.extend([
    Key([mod], '1', lazy.group['   '].toscreen()),
    Key([mod], '2', lazy.group['   '].toscreen()),
    Key([mod], '3', lazy.group['   '].toscreen()),
    Key([mod], '4', lazy.group['   '].toscreen()),
    Key([mod], '5', lazy.group['   '].toscreen()),
    Key([mod], '6', lazy.group['   '].toscreen()),
    Key([mod], '7', lazy.group['   '].toscreen()),


    Key([mod, "shift"], "1", lazy.window.togroup('   ')),
    Key([mod, "shift"], "2", lazy.window.togroup('   ')),
    Key([mod, "shift"], "3", lazy.window.togroup('   ')),
    Key([mod, "shift"], "4", lazy.window.togroup('   ')),
    Key([mod, "shift"], "5", lazy.window.togroup('   ')),
    Key([mod, "shift"], "6", lazy.window.togroup('   ')),
    Key([mod, "shift"], "7", lazy.window.togroup('   ')),
])

layouts = [
    layout.MonadTall(
        border_focus='#1793d1',
        border_normal='#282C34',
        margin=16,
        single_margin=16,
        single_border_width=0
    ),
    layout.Max(),
]

widget_defaults = dict(
    font='Hack Nerd Font',
    fontsize=14,
    padding=4,
    foreground="#ffffff"
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(padding=16, foreground='#000000'),
                widget.TextBox(" ", fontsize=16),
                widget.Prompt(padding=16, prompt='> ', foreground='#98c379'),
                widget.Spacer(),
                widget.GroupBox(
                    highlight_color="#282C34",
                    highlight_method="line",
                    highlight_border="#61afef",
                    urgent_alert_method="line",
                    urgent_text="#e06c75",
                    inactive="#ffffff",
                    active="#61afef",
                    fontsize=16
                ),
                widget.Spacer(),
                widget.Systray(icon_size=18, padding=8),
                widget.Clock(format=' %H:%M'),
                widget.Sep(padding=16, foreground='#000000'),
            ],
            30,
            background="#000000"
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry
        Match(wm_class="steam_app_1182480", title="Origin"), # Origin
        Match(wm_class="steam_app_*"), # Steam Apps
    ],
    border_focus='#1793d1',
    border_normal='#282C34',
    border_width=2,
)
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
