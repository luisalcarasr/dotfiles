"""
Bluetooth service for device discovery via D-Bus.

This module provides async functions for discovering Bluetooth devices
using the BlueZ D-Bus interface.

Example:
    >>> import asyncio
    >>> from services.bluetooth import get_devices
    >>> devices = asyncio.run(get_devices())
    >>> print(devices)
    ['/dev_XX_XX_XX_XX_XX_XX', '/dev_YY_YY_YY_YY_YY_YY']
"""

from __future__ import annotations

import asyncio
import logging

from dbus_fast import BusType
from dbus_fast.aio import MessageBus

from settings.hardware import Bluetooth

logger = logging.getLogger(__name__)


async def get_hci() -> str | None:
    """
    Get the first Bluetooth HCI device path.

    Returns:
        The device path (e.g., '/dev_XX_XX_XX_XX_XX_XX') or None if
        no devices are found.

    Example:
        >>> import asyncio
        >>> hci = asyncio.run(get_hci())
        >>> print(hci)
        '/dev_XX_XX_XX_XX_XX_XX'
    """
    try:
        bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
        introspect = await bus.introspect(
            Bluetooth.SERVICE_NAME,
            Bluetooth.ADAPTER_PATH,
        )
        if introspect.nodes:
            node = introspect.nodes[0]
            return f"/{node.name}" if node.name else None
        return None
    except Exception as e:
        logger.warning(f"Failed to get HCI device: {e}")
        return None


async def get_devices() -> list[str]:
    """
    Get all paired Bluetooth device paths.

    Returns:
        List of device paths relative to the adapter path.
        Empty list if no devices found or on error.

    Example:
        >>> import asyncio
        >>> devices = asyncio.run(get_devices())
        >>> for dev in devices:
        ...     print(dev)
        /dev_XX_XX_XX_XX_XX_XX
        /dev_YY_YY_YY_YY_YY_YY
    """
    try:
        bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
        introspect = await bus.introspect(
            Bluetooth.SERVICE_NAME,
            Bluetooth.ADAPTER_PATH,
        )
        return [f"/{node.name}" for node in introspect.nodes if node.name]
    except Exception as e:
        logger.warning(f"Failed to get Bluetooth devices: {e}")
        return []


if __name__ == "__main__":
    # Test the functions when run directly
    logging.basicConfig(level=logging.DEBUG)
    print("Getting HCI...")
    print(asyncio.run(get_hci()))
    print("Getting devices...")
    print(asyncio.run(get_devices()))
