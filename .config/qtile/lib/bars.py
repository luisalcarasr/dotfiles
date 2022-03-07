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
        
        # Spotify
        widget.Mpris2(
            name="spotify",
            fmt="",
            objname="org.mpris.MediaPlayer2.spotify",
            display_metadata=[],
            scroll_chars=None,
            scroll_interval=0,
            scroll_wait_intervals=0,
            stop_pause_text='',
            font=nerd_font,
            padding=8,
        ),
        widget.Mpris2(
            name="spotify",
            objname="org.mpris.MediaPlayer2.spotify",
            display_metadata=['xesam:title', 'xesam:artist'],
            scroll_chars=20,
            scroll_interval=0,
            scroll_wait_intervals=0,
            stop_pause_text='',
            font_size=12,
        ),
        widget.Mpris2(
            name="spotify",
            fmt=" ",
            objname="org.mpris.MediaPlayer2.spotify",
            display_metadata=['xesam:title', 'xesam:artist'],
            scroll_chars=20,
            scroll_interval=0,
            scroll_wait_intervals=0,
            stop_pause_text='',
            padding=32
        ),
        
        # Background Applications
        widget.Systray(icon_size=20),
        widget.Sep(padding=16, foreground=colors["black"]),

        # VPN
        custom.VirtualPrivateNetwork(
            vpn_name="VPN",
            font=nerd_font,
        ),
        widget.Sep(padding=8, foreground=colors["black"]),

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

        # 
        widget.Sep(padding=8, foreground=colors["black"]),
    ],
    32,
    background=colors["black"],
)

monitor = bar.Bar(
    [
        widget.Sep(padding=8, foreground=colors["black"]),

        # CPU
        widget.TextBox("", font=nerd_font),
        widget.CPU(format="{load_percent}%", fontsize=12),

        # Memory
        widget.TextBox("", font=nerd_font, fontsize=18, padding=4),
        widget.Memory(format="{MemUsed: .0f} {mm}B", fontsize=12),

        # Network
        widget.TextBox("", font=nerd_font, padding=6),
        widget.Net(format="{down}", fontsize=12),

        widget.Spacer(),

        # Clock
        widget.Clock(format='%a %d  %H:%M'),

        widget.Sep(padding=8, foreground=colors["black"]),
    ],
    32,
    background=colors["black"]
)

status = bar.Bar(
    [
        widget.Sep(padding=8, foreground=colors["black"]),

        widget.Spacer(),

        # Clock
        widget.Clock(format='%a %d  %H:%M'),
        
        widget.Sep(padding=8, foreground=colors["black"]),

    ],
    32,
    background=colors["black"]
)
