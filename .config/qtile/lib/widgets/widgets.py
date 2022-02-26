from libqtile.widget import base
from utils.nvidia import get_used_gpu, get_used_memory
from utils.network import is_wireless_connected, is_vpn_connected
from utils.theme import colors

class GPU(base.ThreadPoolText):

    defaults = [
        ('update_interval', 2, 'Update interval in seconds.'),
    ]

    def __init__(self, **config):
        super().__init__("0.0%", **config)
        self.add_defaults(self.defaults)

    def poll(self):
        return str(get_used_gpu()) + ".0%"

class VRAM(base.ThreadPoolText):

    defaults = [
        ('update_interval', 2, 'Update interval in seconds.'),
    ]

    def __init__(self, **config):
        auper().__init__("0.0%", **config)
        self.add_defaults(self.defaults)

    def poll(self):
        return str(round(get_used_memory(), 1)) + "%"

class Wireless(base.ThreadPoolText):

    defaults = [
        ('update_interval', 1, 'Update interval in seconds.'),
        ('interface', 'wlo1', 'Network Interface.'),
    ]

    interface = "wlo1"
    icon = ""

    def __init__(self, interface, **config):
        super().__init__(self.icon, **config)
        self.add_defaults(self.defaults)
        self.interface = interface

    def poll(self):
        self.foreground = colors["white"] if is_wireless_connected(self.interface) else colors["dark"]
        return self.icon

class VirtualPrivateNetwork(base.ThreadPoolText):

    defaults = [
        ('update_interval', 1, 'Update interval in seconds.'),
        ('vpn_name', 'vpn', 'Network Interface.'),
    ]

    vpn_name= "vpn"
    icon = "嬨"

    def __init__(self, vpn_name, **config):
        super().__init__(self.icon, **config)
        self.add_defaults(self.defaults)
        self.vpn_name = vpn_name

    def poll(self):
        self.foreground = colors["white"] if is_vpn_connected() else colors["dark"]
        return self.icon

