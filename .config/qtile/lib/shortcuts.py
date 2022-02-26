from libqtile.lazy import lazy
from libqtile.config import Key, Click, Drag 
from libqtile.utils import guess_terminal
from lib.workspaces import workspaces

mod = "mod4"

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

    # Open Terminal
    Key([mod], "Return", lazy.spawn(guess_terminal())),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "f", lazy.layout.toggle_split()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "q", lazy.shutdown()),

    # Close current window
    Key([mod], "c", lazy.window.kill()),

    # Apps
    Key([mod], "space", lazy.spawn('rofi -show drun -show-icons -theme minimal-app-menu')),

    # Menus
    Key([mod], 'r', lazy.spawn('python /home/luis/.config/rofi/menus/rofi_audio_input')),
    Key([mod], "t", lazy.spawn('python /home/luis/.config/rofi/menus/rofi_audio_output')),

    # Emoji
    Key([mod], "period", lazy.spawn('rofi -show emoji -modi emoji -theme minimal-app-menu')),

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
    Key([mod, "shift"], str(i + 1), lazy.window.togroup(ws)) for i,ws in enumerate(workspaces)
])

keys.extend([
    Key([mod], str(i + 1), lazy.group[ws].toscreen()) for i,ws in enumerate(workspaces)
])
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

