from dbus_fast.aio import MessageBus
from dbus_fast import BusType
import asyncio

BLUEZ_SERVICE_NAME = 'org.bluez'
ADAPTER_PATH = '/org/bluez/hci0'

async def get_hci():
    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
    introspect = await bus.introspect(BLUEZ_SERVICE_NAME, ADAPTER_PATH)
    node = introspect.nodes[0] if introspect.nodes else None
    return f'/{node.name}' if node else None

async def get_devices():
    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
    introspect = await bus.introspect(BLUEZ_SERVICE_NAME, ADAPTER_PATH)
    devices = [f'/{node.name}' for node in introspect.nodes if node.name]
    return devices

# Ejecutar y probar
if __name__ == '__main__':
    print("Getting HCI...")
    print(asyncio.run(get_hci()))
    print("Getting devices...")
    print(asyncio.run(get_devices()))
