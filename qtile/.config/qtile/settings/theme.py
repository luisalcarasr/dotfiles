"""
Theme configuration for Qtile.

This module defines the visual appearance of the window manager including
colors, fonts, and widget decorations.

Example:
    >>> from settings.theme import Colors, Fonts
    >>> Colors.PRIMARY  # Get the primary accent color
    '#41a7fc'
    >>> Fonts.DEFAULT  # Get the default font family
    'Arimo Nerd Font Bold'
"""

from dataclasses import dataclass
from typing import Any

from qtile_extras.widget.decorations import RectDecoration


@dataclass(frozen=True)
class Colors:
    """
    Color palette for the Qtile theme.

    All colors are defined as hex strings. The palette follows a dark theme
    with accent colors inspired by One Dark.

    Attributes:
        WHITE: Pure white for primary text and active elements.
        LIGHT: Light gray for secondary text.
        BLACK: Pure black for backgrounds.
        DARK: Dark gray for inactive elements and borders.
        PRIMARY: Primary accent color (blue).
        SKY: Secondary blue for highlights.
        RED: Error and warning states.
        GREEN: Success states and breaks.
        YELLOW: Warning and attention states.
        AQUA: Accent for special elements.
    """

    # Neutrals
    WHITE: str = "#ffffff"
    LIGHT: str = "#909090"
    BLACK: str = "#000000"
    DARK: str = "#282C34"

    # Accents
    PRIMARY: str = "#41a7fc"
    SKY: str = "#1793d1"
    RED: str = "#e06c75"
    GREEN: str = "#98c379"
    YELLOW: str = "#e6c07b"
    AQUA: str = "#56b6c2"

    @classmethod
    def as_dict(cls) -> dict[str, str]:
        """
        Return colors as a dictionary for compatibility with legacy code.

        Returns:
            Dictionary mapping lowercase color names to hex values.
        """
        return {
            "white": cls.WHITE,
            "light": cls.LIGHT,
            "black": cls.BLACK,
            "dark": cls.DARK,
            "blue": cls.PRIMARY,
            "sky": cls.SKY,
            "red": cls.RED,
            "green": cls.GREEN,
            "yellow": cls.YELLOW,
            "aqua": cls.AQUA,
        }


@dataclass(frozen=True)
class Fonts:
    """
    Font configuration for Qtile widgets.

    Attributes:
        DEFAULT: Default font family for all widgets.
        SIZE: Default font size in pixels.
        SIZE_SMALL: Smaller font size for compact widgets.
        SIZE_LARGE: Larger font size for prominent elements.
    """

    DEFAULT: str = "Arimo Nerd Font Bold"
    SIZE: int = 14
    SIZE_SMALL: int = 12
    SIZE_LARGE: int = 16


@dataclass(frozen=True)
class Decorations:
    """
    Widget decoration configuration.

    Provides factory methods for creating consistent widget decorations
    using qtile-extras RectDecoration.

    Attributes:
        BACKGROUND: Background color for decorated widgets.
        RADIUS: Border radius for decorations.
        PADDING_Y: Vertical padding for decorations.
    """

    BACKGROUND: str = "#111111"
    RADIUS: int = 5
    PADDING_Y: int = 5

    @classmethod
    def rect(cls, **overrides: Any) -> dict[str, list[RectDecoration]]:
        """
        Create a RectDecoration configuration for widgets.

        Args:
            **overrides: Override default decoration parameters.
                - colour: Background color (default: BACKGROUND)
                - radius: Border radius (default: RADIUS)
                - filled: Whether to fill the rectangle (default: True)
                - padding_y: Vertical padding (default: PADDING_Y)

        Returns:
            Dictionary with 'decorations' key containing a list with
            the configured RectDecoration.

        Example:
            >>> widget.TextBox("Hello", **Decorations.rect())
            >>> widget.TextBox("Custom", **Decorations.rect(colour="#ff0000"))
        """
        config = {
            "colour": cls.BACKGROUND,
            "radius": cls.RADIUS,
            "filled": True,
            "padding_y": cls.PADDING_Y,
        }
        config.update(overrides)
        return {"decorations": [RectDecoration(**config)]}


# Legacy compatibility: dictionary-style color access
colors = Colors.as_dict()
