"""
Keyboard shortcuts configuration.

This module defines all keyboard shortcuts (keybindings) for Qtile.
Shortcuts are organized by category for easier maintenance.

Modifier key reference:
    - mod4: Super/Windows key (primary modifier)
    - shift: Shift key
    - control: Control key

Example:
    >>> from core.keys import keys, mod
"""

from __future__ import annotations

from libqtile.config import Key
from libqtile.lazy import lazy

from menus.audio import select_audio_input, select_audio_output
from menus.games import launch_game
from menus.projects import launch_project
from services.audio import OutputAudio
from settings.apps import Apps, MediaCommands

# Primary modifier key (Super/Windows)
mod = "mod4"

# Audio controller for volume keys
_audio = OutputAudio()


def _create_keys() -> list[Key]:
    """
    Create and return all keybindings.

    Returns:
        List of Key objects for Qtile configuration.
    """
    keys: list[Key] = []

    # =========================================================================
    # Window Navigation
    # =========================================================================
    keys.extend([
        Key([mod], "h", lazy.layout.left(), desc="Focus window left"),
        Key([mod], "l", lazy.layout.right(), desc="Focus window right"),
        Key([mod], "j", lazy.layout.down(), desc="Focus window down"),
        Key([mod], "k", lazy.layout.up(), desc="Focus window up"),
    ])

    # =========================================================================
    # Window Movement
    # =========================================================================
    keys.extend([
        Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window left"),
        Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window right"),
        Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
        Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    ])

    # =========================================================================
    # Window Resizing
    # =========================================================================
    keys.extend([
        Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window left"),
        Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window right"),
        Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
        Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
        Key([mod], "m", lazy.layout.maximize(), desc="Maximize focused window"),
        Key([mod], "n", lazy.layout.normalize(), desc="Reset window sizes"),
    ])

    # =========================================================================
    # Applications
    # =========================================================================
    keys.extend([
        Key([mod], "Return", lazy.spawn(Apps.TERMINAL), desc="Launch terminal"),
        Key([mod], "backslash", lazy.spawn(Apps.BROWSER), desc="Launch browser"),
        Key([mod], "space", lazy.spawn(Apps.launcher()), desc="Application launcher"),
        Key([mod], "w", lazy.spawn(Apps.launcher(mode="window")), desc="Window switcher"),
        Key([mod], "period", lazy.spawn(Apps.EMOJI_PICKER), desc="Emoji picker"),
    ])

    # =========================================================================
    # Layout Control
    # =========================================================================
    keys.extend([
        Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
        Key([mod], "f", lazy.layout.toggle_split(), desc="Toggle split"),
        Key([mod], "c", lazy.window.kill(), desc="Close focused window"),
    ])

    # =========================================================================
    # Qtile Control
    # =========================================================================
    keys.extend([
        Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
        Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    ])

    # =========================================================================
    # Media Keys
    # =========================================================================
    keys.extend([
        Key(
            [], "XF86AudioRaiseVolume",
            lazy.function(lambda _: _audio.volume_up()),
            desc="Volume up",
        ),
        Key(
            [], "XF86AudioLowerVolume",
            lazy.function(lambda _: _audio.volume_down()),
            desc="Volume down",
        ),
        Key(
            [], "XF86AudioMute",
            lazy.function(lambda _: _audio.toggle_mute()),
            desc="Toggle mute",
        ),
        Key([], "XF86AudioPlay", lazy.spawn(MediaCommands.PLAY_PAUSE), desc="Play/Pause"),
        Key([], "XF86AudioStop", lazy.spawn(MediaCommands.STOP), desc="Stop"),
        Key([], "XF86AudioNext", lazy.spawn(MediaCommands.NEXT), desc="Next track"),
        Key([], "XF86AudioPrev", lazy.spawn(MediaCommands.PREVIOUS), desc="Previous track"),
    ])

    # =========================================================================
    # Custom Menus
    # =========================================================================
    keys.extend([
        Key([mod], "r", lazy.function(select_audio_input), desc="Select audio input"),
        Key([mod], "t", lazy.function(select_audio_output), desc="Select audio output"),
        Key([mod], "comma", lazy.function(launch_project), desc="Launch project"),
        Key([mod], "g", lazy.function(launch_game), desc="Launch game"),
    ])

    # =========================================================================
    # Multi-Monitor
    # =========================================================================
    keys.extend([
        # Focus screen
        Key([mod], "i", lazy.to_screen(2), desc="Focus screen 3"),
        Key([mod], "o", lazy.to_screen(0), desc="Focus screen 1"),
        Key([mod], "p", lazy.to_screen(1), desc="Focus screen 2"),
        # Move window to screen
        Key([mod, "shift"], "i", lazy.window.toscreen(2), desc="Move to screen 3"),
        Key([mod, "shift"], "o", lazy.window.toscreen(0), desc="Move to screen 1"),
        Key([mod, "shift"], "p", lazy.window.toscreen(1), desc="Move to screen 2"),
    ])

    # =========================================================================
    # Workspace Navigation
    # =========================================================================
    keys.extend([
        Key([mod], "y", lazy.screen.prev_group(), desc="Previous workspace"),
        Key([mod], "u", lazy.screen.next_group(), desc="Next workspace"),
        Key([mod], "6", lazy.group["5"].toscreen(2), desc="Group 5 to screen 3"),
    ])

    return keys


# Generate workspace keybindings
def _add_workspace_keys(keys: list[Key]) -> None:
    """
    Add workspace-related keybindings.

    Adds keys for switching to workspaces and moving windows to workspaces.
    Workspaces are named "1" through "9" and "0".

    Args:
        keys: List to append keys to.
    """
    from core.groups import WORKSPACE_NAMES

    for ws in WORKSPACE_NAMES:
        keys.extend([
            # Switch to workspace
            Key([mod], ws, lazy.group[ws].toscreen(), desc=f"Switch to workspace {ws}"),
            # Move window to workspace
            Key(
                [mod, "shift"], ws,
                lazy.window.togroup(ws),
                desc=f"Move window to workspace {ws}",
            ),
        ])


# Create the keys list
keys = _create_keys()
_add_workspace_keys(keys)
