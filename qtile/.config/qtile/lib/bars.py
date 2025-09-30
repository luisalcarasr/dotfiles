from typing import List  # noqa: F401

from libqtile import bar, qtile
from qtile_extras import widget
from qtile_extras.widget import decorations

from lib import widgets as custom
from utils.queries import can_control_brightness, has_batery
from utils.theme import colors

decor = {
    "decorations": [
        decorations.RectDecoration(
            colour="#111111", radius=5, filled=True, padding_y=5)
    ],
}

try:
    volumen = custom.Volumen(
        **decor
    )
except:
    volumen = widget.TextBox("")

main = bar.Bar(
    [
        widget.Sep(padding=8, foreground=colors["black"]),

        # Groups
        widget.GroupBox(
            highlight_method="text",
            urgent_text=colors["red"],
            foreground=colors["white"],
            active=colors["light"],
            inactive=colors["dark"],
            this_current_screen_border=colors["white"],
            other_current_screen_border=colors["white"],
            margin_x=0,
            margin_y=3,
            border=10,
            **decor
        ),

        widget.Sep(padding=8, foreground=colors["black"]),

        widget.Spacer(),

        # Background Applications
        widget.Systray(icon_size=18),
        widget.Sep(padding=16, foreground=colors["black"]),

        # Pomodoro
        widget.Pomodoro(
            prefix_active="",
            prefix_inactive="0:00:00",
            prefix_long_break="",
            prefix_break="",
            prefix_paused="PAUSED",
            color_active=colors["white"],
            color_break=colors["green"],
            color_inactive=colors["dark"],
            **decor
        ),

        widget.Sep(padding=8, foreground=colors["black"]),

        # VPN
        # custom.VirtualPrivateNetwork(
        #     **decor
        # ),
        # widget.Sep(padding=8, foreground=colors["black"]),

        # Bluetooth
        custom.Bluetooth(
            **decor
        ),
        widget.Sep(padding=8, foreground=colors["black"]),

        # Wireless
        custom.Wireless(
            interface='wlp3s0',
            **decor
        ),
        widget.Sep(padding=8, foreground=colors["black"]),

        # Volume
        volumen,
        widget.Sep(padding=8, foreground=colors["black"]),

        # Brightness
        widget.WidgetBox(
            text_closed=" ",
            text_open=" ",
            widgets=[
                widget.Backlight(
                    backlight_name='intel_backlight',
                    change_command='brightnessctl set {0}%',
                    brightnessfile='/sys/class/backlight/intel_backlight/brightness',
                    max_brightness_file='/sys/class/backlight/intel_backlight/max_brightness',
                ),
            ],
        ) if can_control_brightness else widget.TextBox(""),
        widget.Sep(padding=12, foreground=colors["black"])
        if can_control_brightness else widget.TextBox(""),

        # Battery
        widget.WidgetBox(
            text_closed="  ",
            text_open="  ",
            widgets=[
                widget.Battery(
                    format="{percent:2.1%}",
                    low_foreground=colors["red"],
                    show_short_text=False,
                ),
            ],
        ) if has_batery else widget.TextBox(""),
        widget.Sep(
            padding=8, foreground=colors["black"]) if has_batery else widget.TextBox(""),

        # Date
        # widget.Clock(format='%a %d', **decor),
        # widget.Sep(padding=8, foreground=colors["black"]),

        # Clock
        widget.Clock(format='%H:%M', **decor),
        widget.Sep(padding=8, foreground=colors["black"]),
    ],
    28,
    background=colors["black"],
    border_width=1
)
