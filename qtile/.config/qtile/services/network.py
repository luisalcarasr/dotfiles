"""
Network status service.

This module provides functions for checking network connectivity status
including WiFi connection state and VPN status.

Example:
    >>> from services.network import is_wireless_connected, is_vpn_connected
    >>> if is_wireless_connected("wlp3s0"):
    ...     print("WiFi connected!")
    >>> if is_vpn_connected():
    ...     print("VPN active!")
"""

from __future__ import annotations

import logging
import socket
import subprocess

import dbus
import iwlib

logger = logging.getLogger(__name__)


def extract_ip() -> str:
    """
    Extract the local IP address of the machine.

    Uses a UDP socket trick to determine the local IP without
    actually sending any data.

    Returns:
        The local IP address, or '127.0.0.1' if detection fails.

    Example:
        >>> ip = extract_ip()
        >>> print(ip)
        '192.168.1.100'
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a non-routable address to determine local IP
        sock.connect(("10.255.255.255", 1))
        ip = sock.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        sock.close()
    return ip


def get_essid(interface: str) -> str:
    """
    Get the ESSID (network name) of the connected WiFi network.

    Args:
        interface: Network interface name (e.g., 'wlp3s0').

    Returns:
        The ESSID of the connected network.

    Raises:
        IndexError: If no network is connected or output parsing fails.
        subprocess.SubprocessError: If iwconfig command fails.

    Example:
        >>> essid = get_essid("wlp3s0")
        >>> print(essid)
        'MyNetwork'
    """
    result = subprocess.run(
        ["iwconfig", interface],
        capture_output=True,
        text=True,
        check=True,
    )
    # Parse ESSID from output (format: ESSID:"NetworkName")
    return result.stdout.split('"')[1]


def is_wireless_connected(interface_name: str) -> bool:
    """
    Check if a wireless interface is connected to a network.

    Args:
        interface_name: Network interface name (e.g., 'wlp3s0').

    Returns:
        True if connected to a wireless network, False otherwise.

    Example:
        >>> if is_wireless_connected("wlp3s0"):
        ...     print("Connected!")
    """
    essid, _ = get_wireless_status(interface_name)
    return essid is not None


def get_wireless_status(interface_name: str) -> tuple[str | None, int | None]:
    """
    Get wireless connection status for an interface.

    Args:
        interface_name: Network interface name (e.g., 'wlp3s0').

    Returns:
        Tuple of (essid, quality) where:
        - essid: Network name if connected, None otherwise
        - quality: Signal quality (0-100) if connected, None otherwise

    Example:
        >>> essid, quality = get_wireless_status("wlp3s0")
        >>> if essid:
        ...     print(f"Connected to {essid} ({quality}%)")
    """
    try:
        interface = iwlib.get_iwconfig(interface_name)
        if "stats" not in interface:
            return None, None
        quality: int = interface["stats"]["quality"]
        essid: str = bytes(interface["ESSID"]).decode()
        return essid, quality
    except Exception as e:
        logger.debug(f"Failed to get wireless status for {interface_name}: {e}")
        return None, None


def is_vpn_connected() -> bool:
    """
    Check if a VPN connection is currently active.

    Uses NetworkManager D-Bus interface to query active connections
    and checks if any of them are VPN connections.

    Returns:
        True if a VPN connection is active, False otherwise.

    Example:
        >>> if is_vpn_connected():
        ...     print("VPN is active")
    """
    try:
        bus = dbus.SystemBus()

        # Get NetworkManager proxy
        nm_proxy = bus.get_object(
            "org.freedesktop.NetworkManager",
            "/org/freedesktop/NetworkManager",
        )
        nm_props = dbus.Interface(nm_proxy, "org.freedesktop.DBus.Properties")

        # Get active connections
        active_connections = nm_props.Get(
            "org.freedesktop.NetworkManager",
            "ActiveConnections",
        )

        # Check each active connection for VPN flag
        for conn_path in active_connections:
            conn_proxy = bus.get_object("org.freedesktop.NetworkManager", conn_path)
            conn_props = dbus.Interface(conn_proxy, "org.freedesktop.DBus.Properties")

            vpn = conn_props.Get(
                "org.freedesktop.NetworkManager.Connection.Active",
                "Vpn",
            )
            if vpn:
                return True

        return False

    except dbus.DBusException as e:
        logger.warning(f"Failed to check VPN status: {e}")
        return False
