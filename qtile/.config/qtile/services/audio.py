"""
PulseAudio audio control service.

This module provides a high-level interface for controlling system audio
through PulseAudio, including volume adjustment and mute toggling.

Example:
    >>> from services.audio import OutputAudio
    >>> audio = OutputAudio()
    >>> audio.volume_up()
    >>> audio.toggle_mute()
    >>> print(f"Volume: {audio.volume * 100:.0f}%")
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Callable

from pulsectl import Pulse, PulseError
from pulsectl_asyncio import PulseAsync

from settings.hardware import Audio

if TYPE_CHECKING:
    from pulsectl import PulseSinkInfo, PulseVolumeInfo

logger = logging.getLogger(__name__)


class OutputAudio:
    """
    PulseAudio output (sink) controller.

    Provides methods for controlling the default audio output device
    including volume adjustment and mute toggling.

    Attributes:
        max_volume: Maximum allowed volume level (default: 1.0 = 100%).

    Example:
        >>> output = OutputAudio()
        >>> output.volume = 0.5  # Set to 50%
        >>> output.toggle_mute()
        >>> if output.is_muted():
        ...     print("Audio is muted")
    """

    def __init__(self, max_volume: float = Audio.MAX_VOLUME) -> None:
        """
        Initialize the audio controller.

        Args:
            max_volume: Maximum volume level (1.0 = 100%). Prevents
                accidental volume spikes that could damage speakers
                or hearing.
        """
        self._pulse = Pulse("qtile-volume-control")
        self.max_volume = max_volume

    def on_init(self, callback: Callable[[], None]) -> None:
        """
        Register a callback to be called when PulseAudio connection is ready.

        This sets up an async connection to PulseAudio and calls the
        callback when the connection is established.

        Args:
            callback: Function to call when connection is ready.
        """

        async def connect() -> None:
            try:
                pulse = PulseAsync("qtile-volume-async")
                await pulse.connect()
                pulse.close()
            except Exception as e:
                logger.warning(f"Failed to connect to PulseAudio async: {e}")

        def done_callback(_: asyncio.Task[None]) -> None:
            try:
                callback()
            except Exception as e:
                logger.warning(f"Callback failed: {e}")

        task = asyncio.create_task(connect())
        task.add_done_callback(done_callback)

    def volume_up(self, step: float = 0.05) -> None:
        """
        Increase volume by a step amount.

        Args:
            step: Amount to increase (default: 0.05 = 5%).
        """
        self.volume += abs(step)

    def volume_down(self, step: float = 0.05) -> None:
        """
        Decrease volume by a step amount.

        Args:
            step: Amount to decrease (default: 0.05 = 5%).
        """
        self.volume -= abs(step)

    def toggle_mute(self) -> None:
        """Toggle mute state of the default sink."""
        try:
            sink = self._get_sink()
            if sink is not None:
                self._pulse.mute(sink, mute=not sink.mute)
        except PulseError as e:
            logger.warning(f"Failed to toggle mute: {e}")

    def is_muted(self) -> bool:
        """
        Check if the default sink is muted.

        Returns:
            True if muted, False otherwise. Returns True on error
            to indicate audio is unavailable.
        """
        try:
            sink = self._get_sink()
            return bool(sink.mute) if sink else True
        except PulseError as e:
            logger.warning(f"Failed to get mute state: {e}")
            return True

    @property
    def volume(self) -> float:
        """
        Get current volume level.

        Returns:
            Volume level from 0.0 to max_volume. Returns 0 on error.
        """
        try:
            sink = self._get_sink()
            if sink is not None:
                return round(sink.volume.value_flat, 3)
        except PulseError as e:
            logger.warning(f"Failed to get volume: {e}")
        return 0.0

    @volume.setter
    def volume(self, value: float) -> None:
        """
        Set volume level.

        Args:
            value: Desired volume level. Will be clamped to [0, max_volume].
        """
        # Clamp value to valid range
        value = max(0.0, min(value, self.max_volume))

        try:
            sink = self._get_sink()
            if sink is not None:
                sink_volume: PulseVolumeInfo = sink.volume
                sink_volume.value_flat = value
                self._pulse.volume_set(sink, sink_volume)
        except PulseError as e:
            logger.warning(f"Failed to set volume: {e}")

    def _get_sink(self) -> PulseSinkInfo | None:
        """
        Get the default audio sink.

        Returns:
            The default sink, or None if not found.
        """
        try:
            default_name = self._pulse.server_info().default_sink_name
            return self._pulse.get_sink_by_name(default_name)
        except PulseError as e:
            logger.warning(f"Failed to get default sink: {e}")
            return None
