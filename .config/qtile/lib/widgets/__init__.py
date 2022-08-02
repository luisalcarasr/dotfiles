import importlib
import traceback

from libqtile.log_utils import logger
from libqtile.widget import widgets as qtile_widgets
from libqtile.widget import widgets as extra_widgets
from libqtile.widget.import_error import make_error

from qtile_extras.widget.decorations import inject_decorations

widgets = {
    "Bluetooth": "bluetooth",
    "Volumen": "volumen",
    "VirtualPrivateNetwork": "vpn",
    "Wireless": "wireless",
}

def modify(classdef, *args, initialise=True, **config):
    """
    Function to add additional code needed by widgets to use mods
    provided by qtile-extras.
    The function can also be used to inject code into user-defined
    widgets e.g.
        modify(CustomWidget, **config)
    """

    # Inject the decorations code into the widget
    inject_decorations(classdef)

    if initialise:
        return classdef(*args, **config)

    return classdef

def import_class(module_path, class_name, fallback=None):
    """Import a class safely
    Try to import the class module, and if it fails because of an ImporError
    it logs on WARNING, and logs the traceback on DEBUG level
    """
    try:
        module = importlib.import_module(module_path)
        classdef = getattr(module, class_name)

        classdef = modify(classdef, initialise=False)

        return classdef

    except ImportError as error:
        logger.warning("Unmet dependencies for '%s.%s': %s", module_path, class_name, error)
        if fallback:
            logger.debug("%s", traceback.format_exc())
            return fallback(module_path, class_name)
        raise


def lazify_imports(registry, fallback=None):
    """Leverage PEP 562 to make imports lazy in an __init__.py
    The registry must be a dictionary with the items to import as keys and the
    modules they belong to as a value.
    """
    __all__ = tuple(registry.keys())

    def __dir__():
        return __all__

    def __getattr__(name):
        if name not in registry:
            raise AttributeError

        if name in widgets:
            package = "lib.widgets"
        elif name in extra_widgets:
            package = "qtile_extras.widget"
        else:
            package = "libqtile.widget"

        module_path = f"{package}.{registry[name]}"

        return import_class(module_path, name, fallback=fallback)

    return __all__, __dir__, __getattr__


# We need all widgets, not just the qtile_extras ones so we can inject code into
# everything and have all widgets available in qtile_extras.widget
all_widgets = {**widgets, **extra_widgets, **qtile_widgets}

__all__, __dir__, __getattr__ = lazify_imports(all_widgets, fallback=make_error)
