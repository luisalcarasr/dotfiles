"""
Settings module for Qtile configuration.

This module provides centralized configuration for:
- Theme: Colors, fonts, and visual decorations
- Apps: Default applications and commands
- Hardware: Network interfaces, audio devices, and system paths
"""

from settings.apps import Apps
from settings.hardware import Hardware
from settings.theme import Colors, Decorations, Fonts

__all__ = [
    "Apps",
    "Colors",
    "Decorations",
    "Fonts",
    "Hardware",
]
