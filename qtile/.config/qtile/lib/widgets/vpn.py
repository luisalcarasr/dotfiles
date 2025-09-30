from libqtile.widget import base
from utils.theme import colors
from utils.network import is_vpn_connected

class VirtualPrivateNetwork(base.ThreadPoolText):

    defaults = [
        ('update_interval', 1, 'Update interval in seconds.'),
        ('mouse_callbacks', {},'Mouse callbacks')
    ]

    icon = "嬨"

    def __init__(self, **config):
        super().__init__(self.icon, **config)
        self.add_defaults(self.defaults)

    def poll(self):
        self.foreground = colors["white"] if is_vpn_connected() else colors["dark"]
        return self.icon

