import iwlib
import dbus, sys
import socket
import subprocess


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(("10.255.255.255", 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        st.close()
    return IP


def get_essid(interface):
    iwconfig = subprocess.Popen(["iwconfig", interface], stdout=subprocess.PIPE)
    output, errors = iwconfig.communicate()
    return output.decode("UTF-8").split('"')[1]


def is_wireless_connected(interface_name):
    essid, quality = get_wireless_status(interface_name)
    return essid is not None


def get_wireless_status(interface_name):
    interface = iwlib.get_iwconfig(interface_name)
    if "stats" not in interface:
        return None, None
    quality = interface["stats"]["quality"]
    essid = bytes(interface["ESSID"]).decode()
    return essid, quality


def is_vpn_connected():
    bus = dbus.SystemBus()
    m_proxy = bus.get_object(
        "org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager"
    )
    manager = dbus.Interface(m_proxy, "org.freedesktop.NetworkManager")
    mgr_props = dbus.Interface(m_proxy, "org.freedesktop.DBus.Properties")

    s_proxy = bus.get_object(
        "org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings"
    )
    settings = dbus.Interface(s_proxy, "org.freedesktop.NetworkManager.Settings")

    active = mgr_props.Get("org.freedesktop.NetworkManager", "ActiveConnections")
    for a in active:
        a_proxy = bus.get_object("org.freedesktop.NetworkManager", a)
        a_props = dbus.Interface(a_proxy, "org.freedesktop.DBus.Properties")
        name = a_props.Get("org.freedesktop.NetworkManager.Connection.Active", "Id")
        vpn = a_props.Get("org.freedesktop.NetworkManager.Connection.Active", "Vpn")
        if vpn != 0:
            return True
    return False
