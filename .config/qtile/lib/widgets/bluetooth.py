from libqtile import widget
from utils.bluetooth import get_hci
from utils.theme import colors

class Bluetooth(widget.Bluetooth):

    defaults = [
        (
            "hci",
            get_hci(),
            "hci0 device path.",
        )
    ]

    def __init__(self, **config):
        widget.Bluetooth.__init__(self, **config)
        self.add_defaults(Bluetooth.defaults)

    def update_text(self):
        text = ""
        self.foreground = colors["white"] if self.powered else colors["dark"]
        if not self.powered:
            text = ""
            self.mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn('bluetoothctl power on')}
        else:
            self.mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn('bluetoothctl power off')}
            if not self.connected:
                text = ""
            else:
                if self.device == "Xbox Wireless Controller":
                    text = "調" 
                else:
                    text = ""
        self.update(text)
