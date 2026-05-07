"""
Steam games launcher menu.

This module provides a Rofi-based menu for launching Steam games
directly from Qtile without opening the Steam client first.

Example:
    >>> from menus.games import launch_game
    >>> Key([mod], "g", lazy.function(launch_game))
"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

import vdf
from rofi import Rofi

from settings.apps import Apps
from settings.hardware import Steam

if TYPE_CHECKING:
    from libqtile.core.manager import Qtile

logger = logging.getLogger(__name__)


def _get_steam_games() -> dict[str, str]:
    """
    Get all installed Steam games.

    Reads the Steam library folders configuration and scans for
    installed games, excluding shared redistributables.

    Returns:
        Dictionary mapping game names to Steam app IDs.
    """
    games: dict[str, str] = {}
    library_file = os.path.expanduser(Apps.STEAM_LIBRARY)

    try:
        with open(library_file, encoding="utf-8") as f:
            libraries = vdf.load(f).get("libraryfolders", {})
    except FileNotFoundError:
        logger.warning(f"Steam library file not found: {library_file}")
        return games
    except (OSError, vdf.VDFDecodeError) as e:
        logger.error(f"Error reading Steam library: {e}")
        return games

    # Iterate through library folders
    for key in libraries:
        library = libraries[key]
        apps = library.get("apps", {})
        path = library.get("path")

        if not path:
            continue

        # Process each app in this library
        for app_id in apps:
            # Skip shared redistributables
            if app_id in Steam.SHARED_APP_IDS:
                continue

            # Read app manifest for game name
            manifest_path = os.path.join(
                path,
                "steamapps",
                f"appmanifest_{app_id}.acf",
            )

            try:
                with open(manifest_path, encoding="utf-8") as mf:
                    manifest = vdf.load(mf)
                name = manifest["AppState"]["name"]
                games[name] = app_id
            except FileNotFoundError:
                logger.debug(f"Manifest not found for app {app_id}")
            except (OSError, KeyError, vdf.VDFDecodeError) as e:
                logger.debug(f"Error reading manifest for app {app_id}: {e}")

    return games


def launch_game(qtile: Qtile) -> None:
    """
    Show a Rofi menu to launch a Steam game.

    Scans Steam library folders for installed games and presents
    a searchable menu. Selected games are launched via Steam's
    steam:// protocol.

    Args:
        qtile: Qtile manager instance (provided by lazy.function).

    Example:
        >>> Key([mod], "g", lazy.function(launch_game))
    """
    try:
        rofi = Rofi()
        games = _get_steam_games()

        if not games:
            logger.warning("No Steam games found")
            return

        # Sort games alphabetically
        sorted_names = sorted(games.keys())

        # Show menu
        selected_index, _ = rofi.select("Games", sorted_names)

        if selected_index >= 0:
            selected_name = sorted_names[selected_index]
            app_id = games[selected_name]
            logger.info(f"Launching game: {selected_name} (ID: {app_id})")
            qtile.spawn(f"steam steam://run/{app_id}")

    except Exception as e:
        logger.error(f"Failed to launch game: {e}")
