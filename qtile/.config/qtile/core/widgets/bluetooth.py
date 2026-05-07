"""
Bluetooth widget for Qtile.

Displays Bluetooth adapter status and connected devices using D-Bus.
Supports click to toggle Bluetooth power and hover to show device names.

Example:
    >>> from core.widgets import Bluetooth
    >>> from settings.theme import Decorations
    >>>
    >>> bluetooth_widget = Bluetooth(**Decorations.rect())
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from dbus_next.aio.message_bus import MessageBus
from dbus_next.constants import BusType
from libqtile import qtile
from libqtile.widget import base

from services.bluetooth import get_devices
from settings.hardware import Bluetooth as BluetoothConfig
from settings.theme import Colors

logger = logging.getLogger(__name__)

# D-Bus constants
_BLUEZ = "org.bluez"
_BLUEZ_PATH = BluetoothConfig.ADAPTER_PATH
_BLUEZ_ADAPTER = "org.bluez.Adapter1"
_BLUEZ_DEVICE = "org.bluez.Device1"
_BLUEZ_PROPERTIES = "org.freedesktop.DBus.Properties"

# Icons for different states
_ICON_ON = ""
_ICON_OFF = ""
_ICON_CONNECTED = ""
_ICON_CONTROLLER = "調"


@dataclass
class _BluetoothDevice:
    """
    Represents a paired Bluetooth device.

    Attributes:
        path: D-Bus object path for the device.
        name: Human-readable device name.
        connected: Whether the device is currently connected.
    """

    path: str
    name: str = ""
    connected: bool = False


class Bluetooth(base._TextBox):
    """
    A widget displaying Bluetooth status with interactive controls.

    Features:
        - Shows Bluetooth on/off status
        - Shows when devices are connected
        - Special icon for Xbox controllers
        - Hover to see connected device names
        - Click to toggle Bluetooth power

    Mouse Bindings:
        - Button1 (left click): Toggle Bluetooth power

    Note:
        Requires dbus-next for async D-Bus communication.

    Example:
        >>> bluetooth = Bluetooth()
        >>> # In bar configuration:
        >>> bar.Bar([bluetooth, ...], 28)
    """

    defaults: list[tuple[str, object, str]] = [
        (
            "hci",
            "/dev_XX_XX_XX_XX_XX_XX",
            "HCI device path, found with d-feet or similar D-Bus explorer.",
        ),
    ]

    def __init__(self, **config: Any) -> None:
        """
        Initialize the Bluetooth widget.

        Args:
            **config: Widget configuration passed to _TextBox.
        """
        base._TextBox.__init__(self, "", **config)
        self.add_defaults(Bluetooth.defaults)

        # Instance state
        self._powered: bool = False
        self._icon: str = _ICON_OFF
        self._devices: list[_BluetoothDevice] = []
        self._mouse_callbacks: dict[str, Any] = {}

    async def _config_async(self) -> None:
        """
        Async initialization after widget is added to bar.

        Sets up D-Bus connections and initializes device states.
        """
        self._powered = await self._init_adapter()

        # Get paired devices
        device_paths = await get_devices()
        for path in device_paths:
            device = _BluetoothDevice(path=path)
            device.connected, device.name = await self._init_device(device)
            self._devices.append(device)

        self._update_text()

    async def _init_adapter(self) -> bool:
        """
        Initialize connection to the Bluetooth adapter.

        Returns:
            Whether the adapter is currently powered on.
        """
        try:
            bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
            introspect = await bus.introspect(_BLUEZ, _BLUEZ_PATH)
            obj = bus.get_proxy_object(_BLUEZ, _BLUEZ_PATH, introspect)
            iface = obj.get_interface(_BLUEZ_ADAPTER)
            props = obj.get_interface(_BLUEZ_PROPERTIES)

            powered = await iface.get_powered()
            props.on_properties_changed(self._on_adapter_changed)
            return bool(powered)
        except Exception as e:
            logger.warning(f"Failed to initialize Bluetooth adapter: {e}")
            return False

    async def _init_device(
        self,
        device: _BluetoothDevice,
    ) -> tuple[bool, str]:
        """
        Initialize connection to a Bluetooth device.

        Args:
            device: The device to initialize.

        Returns:
            Tuple of (connected, name) for the device.
        """
        try:
            bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
            device_path = _BLUEZ_PATH + device.path
            introspect = await bus.introspect(_BLUEZ, device_path)
            obj = bus.get_proxy_object(_BLUEZ, device_path, introspect)
            iface = obj.get_interface(_BLUEZ_DEVICE)
            props = obj.get_interface(_BLUEZ_PROPERTIES)

            connected = await iface.get_connected()
            name = await iface.get_name()

            # Subscribe to property changes
            props.on_properties_changed(self._make_device_callback(device))

            return bool(connected), str(name)
        except Exception as e:
            logger.warning(f"Failed to initialize device {device.path}: {e}")
            return False, ""

    def _on_adapter_changed(
        self,
        interface_name: str,
        changed_properties: dict[str, Any],
        invalidated_properties: list[str],
    ) -> None:
        """Handle adapter property changes."""
        powered = changed_properties.get("Powered")
        if powered is not None:
            self._powered = powered.value
            self._update_text()

    def _make_device_callback(
        self,
        device: _BluetoothDevice,
    ) -> Any:
        """
        Create a property change callback for a specific device.

        Args:
            device: The device to create a callback for.

        Returns:
            Callback function for D-Bus property changes.
        """

        def callback(
            interface_name: str,
            changed_properties: dict[str, Any],
            invalidated_properties: list[str],
        ) -> None:
            connected = changed_properties.get("Connected")
            if connected is not None:
                device.connected = connected.value
                self._update_text()

            name = changed_properties.get("Name")
            if name is not None:
                device.name = name.value
                self._update_text()

        return callback

    def _update_text(self) -> None:
        """Update widget display based on current state."""
        self.foreground = Colors.WHITE if self._powered else Colors.DARK

        if not self._powered:
            self._icon = _ICON_OFF
            self._mouse_callbacks = {
                "Button1": lambda: qtile.spawn("bluetoothctl power on"),
            }
        else:
            self._mouse_callbacks = {
                "Button1": lambda: qtile.spawn("bluetoothctl power off"),
            }
            if self._is_connected:
                self._icon = self._get_device_icon()
            else:
                self._icon = _ICON_ON

        self.update(self._icon)

    def _get_device_icon(self) -> str:
        """Get the appropriate icon for connected devices."""
        connected_names = [d.name for d in self._devices if d.connected]
        if len(connected_names) == 1 and "Xbox Wireless Controller" in connected_names:
            return _ICON_CONTROLLER
        return _ICON_CONNECTED

    @property
    def _is_connected(self) -> bool:
        """Check if any device is connected."""
        return any(d.connected for d in self._devices)

    def mouse_enter(self, *args: object, **kwargs: object) -> None:
        """Show connected device info on hover."""
        connected = [d for d in self._devices if d.connected]
        count = len(connected)

        if count == 1 and connected[0].name:
            self.update(f"{self._icon} {connected[0].name}")
        elif count > 0:
            self.update(f"{self._icon} {count}")

    def mouse_leave(self, *args: object, **kwargs: object) -> None:
        """Return to icon-only display."""
        self.update(self._icon)
