from libqtile.utils import lazify_imports
from libqtile.widget.import_error import make_error

widgets = {
    "Bluetooth": "bluetooth",
    "Volumen": "volumen",
    "VirtualPrivateNetwork": "vpn",
    "Wireless": "wireless",
}

__all__, __dir__, __getattr__ = lazify_imports(widgets, __package__, fallback=make_error)
