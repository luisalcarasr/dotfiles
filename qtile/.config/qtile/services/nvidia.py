"""
NVIDIA GPU metrics service.

This module provides functions for querying NVIDIA GPU metrics using
nvidia-smi. Useful for monitoring GPU usage in status bar widgets.

Example:
    >>> from services.nvidia import get_used_gpu, get_used_memory
    >>> print(f"GPU: {get_used_gpu()}%")
    >>> print(f"VRAM: {get_used_memory():.1f}%")
"""

from __future__ import annotations

import logging
import subprocess

logger = logging.getLogger(__name__)


def nvidia_smi(query: str) -> str:
    """
    Query nvidia-smi for a specific GPU metric.

    Args:
        query: The nvidia-smi query string (e.g., 'utilization.gpu',
            'memory.used', 'memory.total').

    Returns:
        The query result as a string, stripped of whitespace.
        Returns '0' on error.

    Raises:
        No exceptions are raised; errors are logged and '0' is returned.

    Example:
        >>> nvidia_smi("utilization.gpu")
        '45'
        >>> nvidia_smi("memory.used")
        '2048'
    """
    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                f"--query-gpu={query}",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        return result.stdout.strip()
    except FileNotFoundError:
        logger.debug("nvidia-smi not found - NVIDIA driver may not be installed")
        return "0"
    except subprocess.TimeoutExpired:
        logger.warning("nvidia-smi timed out")
        return "0"
    except subprocess.CalledProcessError as e:
        logger.warning(f"nvidia-smi failed: {e}")
        return "0"


def get_used_memory() -> float:
    """
    Get GPU memory usage as a percentage.

    Returns:
        Memory usage percentage (0.0 to 100.0).
        Returns 0.0 on error.

    Example:
        >>> usage = get_used_memory()
        >>> print(f"VRAM: {usage:.1f}%")
        VRAM: 45.2%
    """
    try:
        used = int(nvidia_smi("memory.used"))
        total = int(nvidia_smi("memory.total"))
        if total == 0:
            return 0.0
        return (used * 100) / total
    except ValueError:
        return 0.0


def get_used_gpu() -> int:
    """
    Get GPU utilization percentage.

    Returns:
        GPU utilization percentage (0 to 100).
        Returns 0 on error.

    Example:
        >>> usage = get_used_gpu()
        >>> print(f"GPU: {usage}%")
        GPU: 30%
    """
    try:
        return int(nvidia_smi("utilization.gpu"))
    except ValueError:
        return 0
