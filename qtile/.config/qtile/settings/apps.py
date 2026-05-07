"""
Application configuration for Qtile.

This module centralizes all application commands and paths used throughout
the Qtile configuration. Modify these values to customize your setup.

Example:
    >>> from settings.apps import Apps
    >>> Apps.TERMINAL  # Get the terminal command
    'kitty'
    >>> Apps.launcher()  # Get the application launcher command
    'rofi -show drun -show-icons'
"""

from dataclasses import dataclass
from typing import ClassVar

from libqtile.utils import guess_terminal


@dataclass(frozen=True)
class Apps:
    """
    Default applications and commands.

    This class provides a centralized location for all application
    commands used in keybindings and scripts.

    Attributes:
        TERMINAL: Terminal emulator command.
        BROWSER: Web browser command.
        FILE_MANAGER: File manager command.
        EDITOR: Text editor command.
        LAUNCHER: Application launcher base command.
        EMOJI_PICKER: Emoji picker command.

    Class Attributes:
        PROJECTS_DIR: Directory containing development projects.
        STEAM_LIBRARY: Path to Steam library folders configuration.
    """

    # Core applications
    TERMINAL: str = guess_terminal() or "kitty"
    BROWSER: str = "brave"
    FILE_MANAGER: str = "thunar"
    EDITOR: str = "nvim"

    # Launcher
    LAUNCHER: str = "rofi"

    # Emoji
    EMOJI_PICKER: str = "rofi -show emoji -modi emoji"

    # Paths (class variables, not instance attributes)
    PROJECTS_DIR: ClassVar[str] = "~/Projects/"
    STEAM_LIBRARY: ClassVar[str] = "~/.steam/steam/steamapps/libraryfolders.vdf"

    @classmethod
    def launcher(cls, mode: str = "drun", icons: bool = True) -> str:
        """
        Generate a rofi launcher command.

        Args:
            mode: Rofi mode to use ('drun', 'run', 'window', 'ssh').
            icons: Whether to show application icons.

        Returns:
            Complete rofi command string.

        Example:
            >>> Apps.launcher()
            'rofi -show drun -show-icons'
            >>> Apps.launcher(mode='window', icons=False)
            'rofi -show window'
        """
        cmd = f"{cls.LAUNCHER} -show {mode}"
        if icons:
            cmd += " -show-icons"
        return cmd

    @classmethod
    def terminal_with_command(cls, command: str) -> str:
        """
        Generate a terminal command that executes a specific command.

        Args:
            command: The command to execute inside the terminal.

        Returns:
            Complete terminal command string.

        Example:
            >>> Apps.terminal_with_command("htop")
            'kitty -e htop'
        """
        return f"{cls.TERMINAL} -e {command}"

    @classmethod
    def editor_in_terminal(cls, path: str = "") -> str:
        """
        Generate a command to open the editor in a terminal.

        Args:
            path: Optional path to open in the editor.

        Returns:
            Complete terminal + editor command string.

        Example:
            >>> Apps.editor_in_terminal("~/Projects/myapp")
            'kitty -e fish -c "nvm use $nvm_default_version; nvim ~/Projects/myapp"'
        """
        editor_cmd = f"nvm use $nvm_default_version; {cls.EDITOR}"
        if path:
            editor_cmd += f" {path}"
        return f'{cls.TERMINAL} -e fish -c "{editor_cmd}"'


@dataclass(frozen=True)
class MediaCommands:
    """
    Media player control commands using D-Bus.

    These commands interact with Spotify through the MPRIS D-Bus interface.
    They can be adapted for other media players that implement MPRIS.

    Attributes:
        PLAY_PAUSE: Toggle play/pause.
        STOP: Stop playback.
        NEXT: Skip to next track.
        PREVIOUS: Skip to previous track.
    """

    _DBUS_BASE: ClassVar[str] = (
        "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify "
        "/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."
    )

    PLAY_PAUSE: str = f"{_DBUS_BASE}PlayPause"
    STOP: str = f"{_DBUS_BASE}Stop"
    NEXT: str = f"{_DBUS_BASE}Next"
    PREVIOUS: str = f"{_DBUS_BASE}Previous"
