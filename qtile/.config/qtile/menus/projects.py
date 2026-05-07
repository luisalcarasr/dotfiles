"""
Projects launcher menu.

This module provides a Rofi-based menu for quickly opening
development projects in your preferred editor.

Example:
    >>> from menus.projects import launch_project
    >>> Key([mod], "comma", lazy.function(launch_project))
"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from rofi import Rofi

from settings.apps import Apps

if TYPE_CHECKING:
    from libqtile.core.manager import Qtile

logger = logging.getLogger(__name__)


def _get_projects() -> list[str]:
    """
    Get list of project directories.

    Returns:
        List of directory names in the projects folder.
    """
    projects_dir = os.path.expanduser(Apps.PROJECTS_DIR)

    try:
        # List only directories
        entries = os.listdir(projects_dir)
        return sorted([
            e for e in entries
            if os.path.isdir(os.path.join(projects_dir, e))
        ])
    except FileNotFoundError:
        logger.warning(f"Projects directory not found: {projects_dir}")
        return []
    except OSError as e:
        logger.error(f"Error reading projects directory: {e}")
        return []


def launch_project(qtile: Qtile) -> None:
    """
    Show a Rofi menu to open a project in the editor.

    Lists all directories in the configured projects folder and
    opens the selected one in a terminal with the editor.

    Args:
        qtile: Qtile manager instance (provided by lazy.function).

    Example:
        >>> Key([mod], "comma", lazy.function(launch_project))
    """
    try:
        rofi = Rofi()
        projects = _get_projects()

        if not projects:
            logger.warning("No projects found")
            return

        # Show menu
        selected_index, _ = rofi.select("Projects ", projects)

        if selected_index >= 0:
            project_name = projects[selected_index]
            project_path = os.path.join(
                os.path.expanduser(Apps.PROJECTS_DIR),
                project_name,
            )

            logger.info(f"Opening project: {project_name}")
            command = Apps.editor_in_terminal(project_path)
            qtile.spawn(command)

    except Exception as e:
        logger.error(f"Failed to launch project: {e}")
