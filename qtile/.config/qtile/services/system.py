"""
System capability detection service.

This module provides functions and flags for detecting system hardware
capabilities. Used to conditionally enable/disable widgets based on
available hardware.

Example:
    >>> from services.system import has_battery, can_control_brightness
    >>> if has_battery:
    ...     # Show battery widget
    ...     pass
    >>> if can_control_brightness:
    ...     # Show brightness widget
    ...     pass
"""

from __future__ import annotations

from os import path

from settings.hardware import Display


def _check_file_exists(filepath: str) -> bool:
    """
    Check if a file exists at the given path.

    Args:
        filepath: Path to check.

    Returns:
        True if the file exists, False otherwise.
    """
    return path.exists(filepath)


# System capability flags
# These are evaluated at module load time

can_control_brightness: bool = _check_file_exists(Display.BACKLIGHT_PATH)
"""
Whether brightness control is available.

True if the backlight brightness file exists at the configured path.
This typically indicates a laptop with Intel graphics.
"""

has_battery: bool = _check_file_exists("/sys/class/power_supply/BAT0")
"""
Whether a battery is present.

True if BAT0 exists in sysfs, indicating this is likely a laptop.
"""


def get_brightness() -> int | None:
    """
    Get the current screen brightness level.

    Returns:
        Current brightness value, or None if brightness control
        is not available.

    Example:
        >>> brightness = get_brightness()
        >>> if brightness is not None:
        ...     print(f"Brightness: {brightness}")
    """
    if not can_control_brightness:
        return None

    try:
        with open(Display.BACKLIGHT_PATH) as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return None


def get_max_brightness() -> int | None:
    """
    Get the maximum screen brightness level.

    Returns:
        Maximum brightness value, or None if brightness control
        is not available.

    Example:
        >>> max_bright = get_max_brightness()
        >>> current = get_brightness()
        >>> if max_bright and current:
        ...     percent = (current / max_bright) * 100
        ...     print(f"Brightness: {percent:.0f}%")
    """
    if not can_control_brightness:
        return None

    try:
        with open(Display.MAX_BRIGHTNESS_PATH) as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return None


def get_brightness_percent() -> float | None:
    """
    Get the current screen brightness as a percentage.

    Returns:
        Brightness percentage (0.0 to 100.0), or None if
        brightness control is not available.

    Example:
        >>> percent = get_brightness_percent()
        >>> if percent is not None:
        ...     print(f"Brightness: {percent:.0f}%")
    """
    current = get_brightness()
    maximum = get_max_brightness()

    if current is None or maximum is None or maximum == 0:
        return None

    return (current / maximum) * 100
