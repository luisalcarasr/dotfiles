import dbus
from xml.etree import ElementTree

def get_hci():
    bus = dbus.SystemBus()
    obj = bus.get_object('org.bluez', '/org/bluez/hci0')
    iface = dbus.Interface(obj, 'org.freedesktop.DBus.Introspectable')
    xml_string = iface.Introspect()
    for child in ElementTree.fromstring(xml_string):
        if child.tag == 'node':
            return '/' + child.attrib['name']
