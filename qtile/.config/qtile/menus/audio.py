"""
Audio device selection menus.

This module provides Rofi-based menus for selecting audio input
and output devices through PulseAudio.

Example:
    >>> from menus.audio import select_audio_input, select_audio_output
    >>> # Bind to keys:
    >>> Key([mod], "r", lazy.function(select_audio_input))
    >>> Key([mod], "t", lazy.function(select_audio_output))
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pulsectl
from rofi import Rofi

from settings.hardware import Audio

if TYPE_CHECKING:
    from libqtile.core.manager import Qtile

logger = logging.getLogger(__name__)


def _get_display_name(description: str, aliases: dict[str, str]) -> str:
    """
    Get the display name for an audio device.

    Args:
        description: PulseAudio device description.
        aliases: Dictionary mapping descriptions to friendly names.

    Returns:
        Friendly name if available, otherwise the original description.
    """
    return aliases.get(description, description)


def select_audio_input(qtile: Qtile) -> None:
    """
    Show a Rofi menu to select the default audio input device.

    Displays all available audio sources (microphones, webcams, etc.)
    except for monitor sources which are filtered out. The selected
    device becomes the system default.

    Args:
        qtile: Qtile manager instance (provided by lazy.function).

    Example:
        >>> Key([mod], "r", lazy.function(select_audio_input))
    """
    try:
        pulse = pulsectl.Pulse("qtile-audio-input-selector")
        rofi = Rofi()

        # Filter out monitor sources
        sources = [
            s for s in pulse.source_list()
            if s.description not in Audio.INPUT_IGNORE
        ]

        if not sources:
            logger.warning("No audio input devices found")
            return

        # Find current default
        current_default_name = pulse.server_info().default_source_name
        current_default_index = None

        for i, source in enumerate(sources):
            if source.name == current_default_name:
                current_default_index = i
                break

        if current_default_index is None:
            logger.warning("Could not find current default source")
            return

        # Build display names
        display_names = [
            _get_display_name(s.description, Audio.INPUT_ALIASES)
            for s in sources
        ]

        # Show menu
        selected_index, _ = rofi.select(
            "",
            display_names,
            select=current_default_index,
        )

        if selected_index >= 0:
            pulse.default_set(sources[selected_index])
            logger.info(f"Set default input to: {sources[selected_index].description}")

    except pulsectl.PulseError as e:
        logger.error(f"PulseAudio error: {e}")
    except Exception as e:
        logger.error(f"Failed to select audio input: {e}")


def select_audio_output(qtile: Qtile) -> None:
    """
    Show a Rofi menu to select the default audio output device.

    Displays all available audio sinks (speakers, headphones, HDMI, etc.)
    The selected device becomes the system default.

    Args:
        qtile: Qtile manager instance (provided by lazy.function).

    Example:
        >>> Key([mod], "t", lazy.function(select_audio_output))
    """
    try:
        pulse = pulsectl.Pulse("qtile-audio-output-selector")
        rofi = Rofi()

        sinks = pulse.sink_list()

        if not sinks:
            logger.warning("No audio output devices found")
            return

        # Find current default
        current_default_name = pulse.server_info().default_sink_name
        current_default_index = None

        for i, sink in enumerate(sinks):
            if sink.name == current_default_name:
                current_default_index = i
                break

        if current_default_index is None:
            logger.warning("Could not find current default sink")
            return

        # Build display names
        display_names = [
            _get_display_name(s.description, Audio.OUTPUT_ALIASES)
            for s in sinks
        ]

        # Show menu
        selected_index, _ = rofi.select(
            "奔",
            display_names,
            select=current_default_index,
        )

        if selected_index >= 0:
            pulse.default_set(sinks[selected_index])
            logger.info(f"Set default output to: {sinks[selected_index].description}")

    except pulsectl.PulseError as e:
        logger.error(f"PulseAudio error: {e}")
    except Exception as e:
        logger.error(f"Failed to select audio output: {e}")
