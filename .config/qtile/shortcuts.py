from libqtile.lazy import lazy
from libqtile.config import Key, Click, Drag 
from libqtile.utils import guess_terminal
from workspaces import workspaces

mod = "mod4"

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

    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.


    Key([mod], "comma", lazy.prev_screen()),
    Key([mod], "period", lazy.next_screen()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(guess_terminal()), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "space", lazy.spawn('rofi -show drun -show-icons'), desc="Spawn a command using a prompt widget"),
    # Key([mod], "space", lazy.spawn('~/.config/rofi/launchers/misc/launcher.sh'), desc="Spawn a command using a prompt widget"),

    Key([mod], "i", lazy.to_screen(2)),
    Key([mod], "o", lazy.to_screen(0)),
    Key([mod], "p", lazy.to_screen(1)),

   # Key([mod, "shift"], "i", lazy.window.togroup("2")),
   # Key([mod, "shift"], "o", lazy.window.togroup("0")),
   # Key([mod, "shift"], "p", lazy.window.togroup("1")),
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
