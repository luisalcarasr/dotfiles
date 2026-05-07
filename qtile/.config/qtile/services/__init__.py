"""
Services module for system interactions.

This module provides interfaces to system services including:
- Audio: PulseAudio volume control
- Bluetooth: Device discovery and status via D-Bus
- Network: WiFi and VPN status
- NVIDIA: GPU metrics
- System: Hardware capability detection
"""

from services.audio import OutputAudio
from services.bluetooth import get_devices, get_hci
from services.network import (
    extract_ip,
    get_essid,
    get_wireless_status,
    is_vpn_connected,
    is_wireless_connected,
)
from services.nvidia import get_used_gpu, get_used_memory
from services.system import can_control_brightness, has_battery

__all__ = [
    # Audio
    "OutputAudio",
    # Bluetooth
    "get_devices",
    "get_hci",
    # Network
    "extract_ip",
    "get_essid",
    "get_wireless_status",
    "is_vpn_connected",
    "is_wireless_connected",
    # NVIDIA
    "get_used_gpu",
    "get_used_memory",
    # System
    "can_control_brightness",
    "has_battery",
]
