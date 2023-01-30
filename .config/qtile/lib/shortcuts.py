from libqtile.lazy import lazy
from libqtile.config import Key, Click, Drag 
from libqtile.utils import guess_terminal
from lib.workspaces import workspaces
from lib.menus.projects import launch_project
from lib.menus.games import launch_game
from lib.menus.audio.input import select_audio_input
from lib.menus.audio.output import select_audio_output
from utils.audio import OuputAudio

mod = "mod4"


output = OuputAudio()

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),

    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Resize windows
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod], 'm', lazy.layout.maximize()),
    Key([mod], 'n', lazy.layout.normalize()),

    # Open Terminal
    Key([mod], "Return", lazy.spawn(guess_terminal())),

    # Browser
    Key([mod], "backslash", lazy.spawn('firefox')),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "f", lazy.layout.toggle_split()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "q", lazy.shutdown()),

    # Close current window
    Key([mod], "c", lazy.window.kill()),

    # Media
    Key([], "XF86AudioRaiseVolume", lazy.function(lambda _: output.volume_up())),
    Key([], "XF86AudioLowerVolume", lazy.function(lambda _: output.volume_down())),
    Key([], "XF86AudioMute", lazy.function(lambda _: output.toggle_mute())),
    Key([], 'XF86AudioPlay',
        lazy.spawn(
            'dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify '
            '/org/mpris/MediaPlayer2 '
            'org.mpris.MediaPlayer2.Player.PlayPause')),
    Key([], 'XF86AudioStop',
        lazy.spawn(
            'dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify '
            '/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop')),
    Key([], 'XF86AudioNext',
        lazy.spawn(
            'dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify '
            '/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next')),
    Key([], 'XF86AudioPrev',
        lazy.spawn(
            'dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify '
            '/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous')),

    # Apps
    Key([mod], "space", lazy.spawn('rofi -show drun -show-icons')),

    # Windows
    Key([mod], "w", lazy.spawn('rofi -show window')),

    # Menus
    Key([mod], "r", lazy.function(select_audio_input)),
    Key([mod], "t", lazy.function(select_audio_output)),

    # Emoji
    Key([mod], "period", lazy.spawn('rofi -show emoji -modi emoji')),

    # Projects
    Key([mod], "comma", lazy.function(launch_project)),

    # Games
    Key([mod], "g", lazy.function(launch_game)),

    # Displays
    Key([mod], "i", lazy.to_screen(2)),
    Key([mod], "o", lazy.to_screen(0)),
    Key([mod], "p", lazy.to_screen(1)),

    # Move window to another screen
    Key([mod, "shift"], "i", lazy.window.toscreen(2)),
    Key([mod, "shift"], "o", lazy.window.toscreen(0)),
    Key([mod, "shift"], "p", lazy.window.toscreen(1)),

    # Workspaces
    Key([mod], "y", lazy.screen.prev_group()),
    Key([mod], "u", lazy.screen.next_group()),

    Key([mod], str(6), lazy.group["5"].toscreen(2)),
]

keys.extend([
    Key([mod, "shift"], ws, lazy.window.togroup(ws)) for ws in workspaces
])

keys.extend([
    Key([mod], ws, lazy.group[ws].toscreen()) for ws in workspaces
])
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

