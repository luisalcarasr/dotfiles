from libqtile.widget import base
from utils.theme import colors
from utils.network import is_vpn_connected

class VirtualPrivateNetwork(base.ThreadPoolText):

    defaults = [
        ('update_interval', 1, 'Update interval in seconds.'),
        ('vpn_name', 'vpn', 'Network Interface.'),
        ('mouse_callbacks', {},'Mouse callbacks')
    ]

    vpn_name= "vpn"
    icon = "嬨 "

    def __init__(self, vpn_name, **config):
        super().__init__(self.icon, **config)
        self.add_defaults(self.defaults)
        self.vpn_name = vpn_name

    def poll(self):
        self.foreground = colors["white"] if is_vpn_connected() else colors["dark"]
        return self.icon

