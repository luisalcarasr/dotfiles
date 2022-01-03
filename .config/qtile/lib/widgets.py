from libqtile.widget import base
from utils.nvidia import get_used_gpu, get_used_memory

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
        super().__init__("0.0%", **config)
        self.add_defaults(self.defaults)

    def poll(self):
        return str(round(get_used_memory(), 1)) + "%"
