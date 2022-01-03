from libqtile.lazy import lazy
from libqtile.config import Key, Click, Drag 
from libqtile.utils import guess_terminal

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
    Key([mod], "Return", lazy.spawn(guess_terminal()), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "space", lazy.spawn('rofi -show drun -show-icons'), desc="Spawn a command using a prompt widget"),
    Key([mod], "space", lazy.spawncmd(''), desc="Spawn a command using a prompt widget"),

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
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]
