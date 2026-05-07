"""
Custom Qtile widgets module.

This module provides custom widgets for the Qtile bar with lazy loading
support. All widgets support qtile-extras decorations.

Available Widgets:
    - Bluetooth: Bluetooth connection status and control
    - Volume: Audio volume display and control
    - VPN: VPN connection status indicator
    - Wireless: WiFi connection status
    - Nvidia: GPU usage display
    - VRAM: GPU memory usage display

Example:
    >>> from core.widgets import Bluetooth, Volume, Wireless
    >>> from settings.theme import Decorations
    >>>
    >>> widgets = [
    ...     Volume(**Decorations.rect()),
    ...     Bluetooth(**Decorations.rect()),
    ...     Wireless(interface='wlp3s0', **Decorations.rect()),
    ... ]
"""

from __future__ import annotations

import importlib
import logging
import traceback
from typing import Any, Callable

from libqtile.widget import widgets as qtile_widgets
from libqtile.widget.import_error import make_error
from qtile_extras.widget import widgets as extra_widgets
from qtile_extras.widget.decorations import inject_decorations

logger = logging.getLogger(__name__)

# Registry of custom widgets: widget_name -> module_name
_CUSTOM_WIDGETS: dict[str, str] = {
    "Bluetooth": "bluetooth",
    "Volume": "volume",
    "VPN": "vpn",
    "Wireless": "wireless",
    "Nvidia": "nvidia",
    "VRAM": "nvidia",
}


def _modify_widget(
    classdef: type,
    *args: Any,
    initialise: bool = True,
    **config: Any,
) -> Any:
    """
    Inject qtile-extras decorations support into a widget class.

    This function modifies widget classes to support the decorations
    feature from qtile-extras.

    Args:
        classdef: The widget class to modify.
        *args: Positional arguments for widget initialization.
        initialise: Whether to instantiate the widget (default: True).
        **config: Configuration passed to the widget constructor.

    Returns:
        If initialise is True, returns an instance of the widget.
        Otherwise, returns the modified class.
    """
    inject_decorations(classdef)

    if initialise:
        return classdef(*args, **config)
    return classdef


def _import_class(
    module_path: str,
    class_name: str,
    fallback: Callable[[str, str], type] | None = None,
) -> type:
    """
    Safely import a widget class from a module.

    Args:
        module_path: Full module path (e.g., 'core.widgets.bluetooth').
        class_name: Name of the class to import.
        fallback: Optional fallback function to create an error widget.

    Returns:
        The imported class with decoration support injected.

    Raises:
        ImportError: If the import fails and no fallback is provided.
    """
    try:
        module = importlib.import_module(module_path)
        classdef = getattr(module, class_name)
        return _modify_widget(classdef, initialise=False)

    except ImportError as error:
        logger.warning(
            "Unmet dependencies for '%s.%s': %s",
            module_path,
            class_name,
            error,
        )
        if fallback:
            logger.debug("%s", traceback.format_exc())
            return fallback(module_path, class_name)
        raise


def _lazify_imports(
    registry: dict[str, str],
    fallback: Callable[[str, str], type] | None = None,
) -> tuple[tuple[str, ...], Callable[[], tuple[str, ...]], Callable[[str], type]]:
    """
    Create lazy import functions for PEP 562 module-level __getattr__.

    This enables lazy loading of widgets, only importing them when
    they're actually accessed.

    Args:
        registry: Dictionary mapping widget names to their modules.
        fallback: Optional fallback function for import errors.

    Returns:
        Tuple of (__all__, __dir__, __getattr__) for module-level use.
    """
    __all__ = tuple(registry.keys())

    def __dir__() -> tuple[str, ...]:
        return __all__

    def __getattr__(name: str) -> type:
        if name not in registry:
            raise AttributeError(f"module 'core.widgets' has no attribute '{name}'")

        # Determine which package the widget belongs to
        if name in _CUSTOM_WIDGETS:
            package = "core.widgets"
        elif name in extra_widgets:
            package = "qtile_extras.widget"
        else:
            package = "libqtile.widget"

        module_path = f"{package}.{registry[name]}"
        return _import_class(module_path, name, fallback=fallback)

    return __all__, __dir__, __getattr__


# Combine all widget registries for lazy loading
_ALL_WIDGETS = {**_CUSTOM_WIDGETS, **extra_widgets, **qtile_widgets}

__all__, __dir__, __getattr__ = _lazify_imports(_ALL_WIDGETS, fallback=make_error)
