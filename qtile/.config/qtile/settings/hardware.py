"""
Hardware configuration for Qtile.

This module contains hardware-specific settings like network interface names,
audio device aliases, and system paths. Modify these values to match your
system's hardware configuration.

Example:
    >>> from settings.hardware import Network, Audio
    >>> Network.WIRELESS_INTERFACE
    'wlp3s0'
    >>> Audio.OUTPUT_ALIASES
    {'Built-in Audio Analog Stereo': '   Headphones', ...}
"""

from dataclasses import dataclass, field
from os import path
from typing import ClassVar


@dataclass(frozen=True)
class Network:
    """
    Network interface configuration.

    Attributes:
        WIRELESS_INTERFACE: Name of the wireless network interface.
            Find yours with: `ip link show` or `iwconfig`
    """

    WIRELESS_INTERFACE: str = "wlp3s0"


@dataclass(frozen=True)
class Audio:
    """
    Audio device configuration and aliases.

    Provides human-readable aliases for PulseAudio sink and source names.
    These make the audio selection menus more user-friendly.

    Attributes:
        OUTPUT_ALIASES: Mapping of PulseAudio sink descriptions to display names.
        INPUT_ALIASES: Mapping of PulseAudio source descriptions to display names.
        INPUT_IGNORE: List of source descriptions to hide from selection menus.
        MAX_VOLUME: Maximum volume level (1.0 = 100%).
    """

    OUTPUT_ALIASES: ClassVar[dict[str, str]] = {
        "TU116 High Definition Audio Controller Digital Stereo (HDMI)": "蓼 Right Monitor",
        "TU116 High Definition Audio Controller Digital Stereo (HDMI 2)": "蓼 Speakers",
        "TU116 High Definition Audio Controller Digital Stereo (HDMI 3)": "蓼 Left Monitor",
        "Built-in Audio Analog Stereo": "   Headphones",
    }

    INPUT_ALIASES: ClassVar[dict[str, str]] = {
        "GameFactor MCG601 Mono": "   Microphone",
        "HD Pro Webcam C920 Analog Stereo": "犯 Webcam",
    }

    INPUT_IGNORE: ClassVar[list[str]] = [
        "Monitor of Built-in Audio Analog Stereo",
        "Monitor of TU116 High Definition Audio Controller Digital Stereo (HDMI)",
        "Monitor of TU116 High Definition Audio Controller Digital Stereo (HDMI 2)",
        "Monitor of TU116 High Definition Audio Controller Digital Stereo (HDMI 3)",
        "Monitor of Audio Adapter (Unitek Y-247A) Analog Stereo",
    ]

    MAX_VOLUME: float = 1.0


@dataclass(frozen=True)
class Bluetooth:
    """
    Bluetooth configuration.

    Attributes:
        ADAPTER_PATH: D-Bus path to the Bluetooth adapter.
        SERVICE_NAME: D-Bus service name for BlueZ.
    """

    ADAPTER_PATH: str = "/org/bluez/hci0"
    SERVICE_NAME: str = "org.bluez"


@dataclass(frozen=True)
class Display:
    """
    Display and backlight configuration.

    Attributes:
        BACKLIGHT_NAME: Name of the backlight device for brightness control.
        BACKLIGHT_PATH: Path to the backlight brightness file.
        MAX_BRIGHTNESS_PATH: Path to the maximum brightness file.
    """

    BACKLIGHT_NAME: str = "intel_backlight"
    BACKLIGHT_PATH: str = "/sys/class/backlight/intel_backlight/brightness"
    MAX_BRIGHTNESS_PATH: str = "/sys/class/backlight/intel_backlight/max_brightness"


@dataclass(frozen=True)
class System:
    """
    System capability detection.

    These flags are automatically detected based on the presence of
    system files. They're used to conditionally show/hide widgets.

    Attributes:
        CAN_CONTROL_BRIGHTNESS: Whether brightness control is available.
        HAS_BATTERY: Whether a battery is present (laptop detection).
    """

    CAN_CONTROL_BRIGHTNESS: bool = field(
        default_factory=lambda: path.exists("/sys/class/backlight/intel_backlight/brightness")
    )
    HAS_BATTERY: bool = field(
        default_factory=lambda: path.exists("/sys/class/power_supply/BAT0")
    )


# Create singleton instances for easy access
system = System()


@dataclass(frozen=True)
class Steam:
    """
    Steam gaming platform configuration.

    Attributes:
        SHARED_APP_IDS: Steam app IDs to exclude from the games menu.
            These are typically redistributables and tools, not actual games.
    """

    SHARED_APP_IDS: ClassVar[frozenset[str]] = frozenset({
        "228980",   # Steamworks Common Redistributables
        "1391110",  # Proton EasyAntiCheat Runtime
        "1493710",  # Proton Experimental
        "1826330",  # Proton BattlEye Runtime
    })
