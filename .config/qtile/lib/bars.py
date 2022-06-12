from typing import List  # noqa: F401
from libqtile import bar, widget, qtile
from utils.theme import colors
from utils.queries import can_control_brightness, has_batery
from lib.widgets import widgets as custom
from lib.defaults import nerd_font

main=bar.Bar(
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
            margin=5,
            border=10
        ),

        widget.Spacer(),

        # Pomodoro
        widget.Pomodoro(
            prefix_active="",
            prefix_inactive="0:00:00",
            prefix_long_break="",
            prefix_break="",
            prefix_paused="Paused",
            color_active=colors["white"],
            color_break=colors["green"],
            color_inactive=colors["dark"],
        ),
        
        widget.Spacer(),
        
        # Background Applications
        widget.Systray(icon_size=20),
        widget.Sep(padding=16, foreground=colors["black"]),

        # VPN
        custom.VirtualPrivateNetwork(
            vpn_name="VPN",
            font=nerd_font,
        ),
        widget.Sep(padding=8, foreground=colors["black"]),

        # Bluetooth
        custom.Bluetooth(
            hci='/dev_44_16_22_6F_8F_0C',
            font=nerd_font,
            fontsize=16,
        ),
        widget.Sep(padding=0, foreground=colors["black"]),

        # Wireless
        custom.Wireless(
            interface='wlp3s0',
            font=nerd_font,
        ),
        widget.Sep(padding=15, foreground=colors["black"]),

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
        widget.Clock(format='%a %d  %H:%M'),

        # Apps
        widget.TextBox(
            (" "),
            mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn('rofi -show drun -show-icons -theme minimal-app-menu')},
            font=nerd_font,
        ),

        widget.Sep(padding=8, foreground=colors["black"]),
    ],
    32,
    background=colors["black"],
)
