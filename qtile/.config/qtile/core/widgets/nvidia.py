"""
NVIDIA GPU widgets for Qtile.

Displays GPU utilization and VRAM usage using nvidia-smi.
Useful for monitoring GPU load in gaming or compute workloads.

Example:
    >>> from core.widgets import Nvidia, VRAM
    >>> from settings.theme import Decorations
    >>>
    >>> gpu_widget = Nvidia(**Decorations.rect())
    >>> vram_widget = VRAM(**Decorations.rect())
"""

from __future__ import annotations

import logging
from typing import Any

from libqtile.widget import base

from services.nvidia import get_used_gpu, get_used_memory

logger = logging.getLogger(__name__)


class Nvidia(base.ThreadPoolText):
    """
    A widget displaying NVIDIA GPU utilization percentage.

    Features:
        - Shows GPU usage as percentage
        - Updates periodically

    Note:
        Requires nvidia-smi (NVIDIA driver) to be installed.

    Example:
        >>> gpu = Nvidia()
        >>> # In bar configuration:
        >>> bar.Bar([gpu, ...], 28)
    """

    defaults: list[tuple[str, object, str]] = [
        ("update_interval", 2.0, "Update interval in seconds."),
    ]

    def __init__(self, **config: Any) -> None:
        """
        Initialize the Nvidia widget.

        Args:
            **config: Widget configuration passed to ThreadPoolText.
        """
        super().__init__("0%", **config)
        self.add_defaults(Nvidia.defaults)

    def poll(self) -> str:
        """
        Poll for GPU utilization.

        Returns:
            GPU utilization as a percentage string (e.g., "45%").
        """
        usage = get_used_gpu()
        return f"{usage}%"


class VRAM(base.ThreadPoolText):
    """
    A widget displaying NVIDIA GPU memory (VRAM) usage percentage.

    Features:
        - Shows VRAM usage as percentage
        - Updates periodically

    Note:
        Requires nvidia-smi (NVIDIA driver) to be installed.

    Example:
        >>> vram = VRAM()
        >>> # In bar configuration:
        >>> bar.Bar([vram, ...], 28)
    """

    defaults: list[tuple[str, object, str]] = [
        ("update_interval", 2.0, "Update interval in seconds."),
    ]

    def __init__(self, **config: Any) -> None:
        """
        Initialize the VRAM widget.

        Args:
            **config: Widget configuration passed to ThreadPoolText.
        """
        super().__init__("0.0%", **config)
        self.add_defaults(VRAM.defaults)

    def poll(self) -> str:
        """
        Poll for VRAM usage.

        Returns:
            VRAM usage as a percentage string (e.g., "45.2%").
        """
        usage = get_used_memory()
        return f"{usage:.1f}%"
