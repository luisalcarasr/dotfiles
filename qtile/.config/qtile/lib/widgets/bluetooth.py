from libqtile import qtile
from utils.bluetooth import get_devices
from utils.theme import colors
from dbus_next.aio.message_bus import MessageBus
from dbus_next.constants import BusType

from libqtile.widget import base

BLUEZ = "org.bluez"
BLUEZ_PATH = "/org/bluez/hci0"
BLUEZ_ADAPTER = "org.bluez.Adapter1"
BLUEZ_DEVICE = "org.bluez.Device1"
BLUEZ_PROPERTIES = "org.freedesktop.DBus.Properties"

ICON_BLUETOOTH_ON = ""
ICON_BLUETOOTH_OFF = ""
ICON_BLUETOOTH_CONNECTED = ""
ICON_CONTROLLER = "調"


class Device:
    def __init__(self, path, name="", connected=False):
        self.path = path
        self.name = name
        self.connected = connected


class Bluetooth(base._TextBox):
    """
    Displays bluetooth status for a particular connected device.
    (For example your bluetooth headphones.)
    Uses dbus-next to communicate with the system bus.
    Widget requirements: dbus-next_.
    .. _dbus-next: https://pypi.org/project/dbus-next/
    """

    defaults = [
        (
            "hci",
            "/dev_XX_XX_XX_XX_XX_XX",
            "hci0 device path, can be found with d-feet or similar dbus explorer.",
        )
    ]

    devices = []

    def __init__(self, **config):
        base._TextBox.__init__(self, "", **config)
        self.add_defaults(Bluetooth.defaults)
        # initialize attributes to satisfy linters and ensure instance state
        self.powered = False
        self.icon = ""
        self.devices = []
        self.mouse_callbacks = {}

    async def _config_async(self):
        # set initial values
        self.powered = await self._init_adapter()
        # get_devices() is async; await it before iterating
        for path in await get_devices():
            device = Device(path)
            device.connected, device.name = await self._init_device(device)
            self.devices.append(device)

        self.update_text()

    async def _init_adapter(self):
        # set up interface to adapter properties using high-level api
        bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
        introspect = await bus.introspect(BLUEZ, BLUEZ_PATH)
        obj = bus.get_proxy_object(BLUEZ, BLUEZ_PATH, introspect)
        iface = obj.get_interface(BLUEZ_ADAPTER)
        props = obj.get_interface(BLUEZ_PROPERTIES)

        powered = await iface.get_powered()
        # subscribe receiver to property changed
        props.on_properties_changed(self._adapter_signal_received)
        return powered

    async def _init_device(self, device):
        # set up interface to device properties using high-level api
        bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
        introspect = await bus.introspect(BLUEZ, BLUEZ_PATH + device.path)
        obj = bus.get_proxy_object(BLUEZ, BLUEZ_PATH + device.path, introspect)
        iface = obj.get_interface(BLUEZ_DEVICE)
        props = obj.get_interface(BLUEZ_PROPERTIES)

        connected = await iface.get_connected()
        name = await iface.get_name()
        # subscribe receiver to property changed
        props.on_properties_changed(self._signal_received(device))
        return connected, name

    def _adapter_signal_received(
        self, interface_name, changed_properties, _invalidated_properties
    ):
        powered = changed_properties.get("Powered", None)
        if powered is not None:
            self.powered = powered.value
            self.update_text()

    def _signal_received(self, device):
        def _(interface_name, changed_properties, _invalidated_properties):
            connected = changed_properties.get("Connected", None)
            if connected is not None:
                device.connected = connected.value
                self.update_text()

            name = changed_properties.get("Name", None)
            if name is not None:
                device.name = name.value
                self.update_text()

        return _

    def update_text(self):
        self.foreground = colors["white"] if self.powered else colors["dark"]
        if not self.powered:
            self.icon = ICON_BLUETOOTH_OFF
            self.mouse_callbacks = {
                "Button1": lambda: qtile.cmd_spawn("bluetoothctl power on")
            }
        else:
            self.mouse_callbacks = {
                "Button1": lambda: qtile.cmd_spawn("bluetoothctl power off")
            }
            # show a specific icon when a device is connected, otherwise generic ON icon
            if self.connected:
                self.icon = self._get_icon_device()
            else:
                self.icon = ICON_BLUETOOTH_ON
        self.update(self.icon)

    def _get_icon_device(self):
        icon = ICON_BLUETOOTH_CONNECTED
        names = [device.name for device in self.devices if device.connected]
        if len(names) == 1:
            if "Xbox Wireless Controller" in names:
                icon = ICON_CONTROLLER
        return icon

    @property
    def connected(self):
        # True if any device is connected
        return any(device.connected for device in self.devices)

    def mouse_enter(self, *args, **kwargs):
        connected_devices = [device for device in self.devices if device.connected]
        length = len(connected_devices)
        if length == 1:
            name = connected_devices[0].name
            if name:
                self.update(self.icon + " " + name)
        else:
            self.update(self.icon + " " + str(length))

    def mouse_leave(self, *args, **kwargs):
        self.update(self.icon)
