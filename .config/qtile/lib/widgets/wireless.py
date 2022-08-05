from libqtile.widget import base 
from utils.theme import colors
from utils.network import is_wireless_connected, get_wireless_status

class Wireless(base.ThreadPoolText):

    defaults = [
        ('update_interval', 1, 'Update interval in seconds.'),
        ('interface', 'wlo1', 'Network Interface.'),
    ]

    interface = "wlo1"
    icon = " "

    def __init__(self, interface, **config):
        super().__init__(self.icon, **config)
        self.add_defaults(self.defaults)
        self.interface = interface

    def poll(self):
        self.foreground = colors["white"] if is_wireless_connected(self.interface) else colors["dark"]
        return self.text

    def mouse_enter(self, *args, **kwargs):
        name, _ = get_wireless_status(self.interface)
        if (name):
            self.update(self.icon + " " + name)

    def mouse_leave(self, *args, **kwargs):
        self.update(self.icon)


