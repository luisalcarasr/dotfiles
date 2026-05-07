# Changelog

All notable changes to this Qtile configuration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added

- **Modular Architecture**: Complete restructure with clean separation of concerns
  - `settings/` - User-configurable settings (theme, apps, hardware)
  - `core/` - Core Qtile components (keys, layouts, bar, widgets)
  - `services/` - System service interfaces (audio, bluetooth, network)
  - `menus/` - Rofi menu integrations

- **Poetry Support**: Modern Python dependency management
  - `pyproject.toml` with all dependencies
  - Development tools configuration (ruff, black, mypy)

- **Type Hints**: Full type annotations throughout the codebase
  - Improved IDE support and autocompletion
  - Better error detection

- **Google-style Docstrings**: Comprehensive documentation
  - Module-level documentation
  - Function and class documentation
  - Usage examples

- **Custom Widgets**:
  - `Volume`: PulseAudio volume control with hover percentage
  - `Bluetooth`: Device status with D-Bus integration
  - `Wireless`: WiFi status with hover network name
  - `VPN`: NetworkManager VPN status
  - `Nvidia`/`VRAM`: GPU utilization monitoring

- **Rofi Menus**:
  - Audio input/output device selector
  - Steam games launcher
  - Projects launcher

- **Centralized Configuration**:
  - `settings/theme.py`: Colors, fonts, decorations
  - `settings/apps.py`: Default applications
  - `settings/hardware.py`: Hardware-specific settings

### Changed

- Renamed `lib/` to `core/` for clarity
- Renamed `utils/` to `services/` to better reflect purpose
- Renamed `workspaces.py` to `groups.py` (Qtile terminology)
- Renamed `shortcuts.py` to `keys.py` for consistency
- Renamed `volumen.py` to `volume.py` (English)
- Fixed typo `OuputAudio` to `OutputAudio`
- Moved mouse bindings to separate `mouse.py` module
- Consolidated audio menus into single `menus/audio.py`
- Moved theme from `utils/` to `settings/`

### Removed

- `lib/lazies/` directory (unused)
- `requirements.txt` (replaced by pyproject.toml)
- Legacy dictionary-only color definitions (kept for compatibility)

### Fixed

- Bare `except:` clauses replaced with specific exceptions
- Unused imports removed
- Proper error handling with logging
- Type safety improvements

## [0.x.x] - Previous Versions

Previous versions were not formally versioned. See git history for changes.
