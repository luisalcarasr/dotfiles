from typing import List  # noqa: F401
from libqtile import bar, qtile
from utils.theme import colors
from utils.queries import can_control_brightness, has_batery
from lib import widgets as custom
from qtile_extras import widget
from lib.defaults import nerd_font
from qtile_extras.widget import decorations 

decor = {
    "decorations": [
        decorations.RectDecoration(colour="#111111", radius=5, filled=True, padding_y=5)
    ],
}

try:
    volumen = custom.Volumen(
        **decor
    )
except:
    volumen = widget.TextBox("")

main=bar.Bar(
    [
        widget.Sep(padding=8, foreground=colors["black"]),
        
        # Logo
        widget.TextBox(" ", font=nerd_font, **decor),
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
            margin_x=5,
            margin_y=3,
            border=10,
            fontsize=16,
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
            fontsize=14,
            **decor
        ),
        
        widget.Sep(padding=8, foreground=colors["black"]),

        # VPN
        custom.VirtualPrivateNetwork(
            vpn_name="VPN",
            font=nerd_font,
            **decor
        ),
        widget.Sep(padding=8, foreground=colors["black"]),

        # Bluetooth
        custom.Bluetooth(
            font=nerd_font,
            fontsize=16,
            **decor
        ),
        widget.Sep(padding=8, foreground=colors["black"]),

        # Wireless
        custom.Wireless(
            interface='wlp3s0',
            font=nerd_font,
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
        ) if can_control_brightness else widget.TextBox(""),
        widget.Sep(padding=12, foreground=colors["black"])
            if can_control_brightness else widget.TextBox(""),

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
        ) if has_batery else widget.TextBox(""),
        widget.Sep(padding=8, foreground=colors["black"]) if has_batery else widget.TextBox(""),

        # Clock
        widget.Clock(format='%a %d  %H:%M', fontsize=14, **decor),
        widget.Sep(padding=8, foreground=colors["black"]),

        # Apps
        widget.TextBox(
            (" "),
            mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn('rofi -show drun')},
            font=nerd_font,
            **decor
        ),
        widget.Sep(padding=8, foreground=colors["black"]),
    ],
    32,
    background=colors["black"],
    border_width=5
)
