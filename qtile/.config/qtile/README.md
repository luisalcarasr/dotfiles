# Qtile Configuration

A modular, well-documented [Qtile](http://www.qtile.org/) window manager configuration with custom widgets, Rofi integration, and multi-monitor support.

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for settings, core components, services, and menus
- **Custom Widgets**: Volume, Bluetooth, WiFi, VPN, and NVIDIA GPU widgets with hover details
- **Rofi Integration**: Quick launchers for applications, projects, Steam games, and audio devices
- **Multi-Monitor Support**: Automatic workspace and layout assignment per screen
- **PulseAudio Control**: Full volume control with visual feedback
- **Steam Integration**: Launch games directly from a searchable menu
- **Type Hints**: Full type annotations for better IDE support and code quality
- **Google-style Docstrings**: Comprehensive documentation throughout

## Screenshots

*Coming soon*

## Requirements

### System Dependencies

```bash
# Arch Linux
sudo pacman -Syu \
    qtile \
    python \
    python-pip \
    rofi \
    wireless_tools \
    bluez \
    bluez-utils \
    pulseaudio \
    brightnessctl

# For NVIDIA GPU monitoring (optional)
sudo pacman -S nvidia-utils
```

### Python Dependencies

This configuration uses [Poetry](https://python-poetry.org/) for dependency management:

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
cd ~/.config/qtile
poetry install
```

Alternatively, install dependencies manually:

```bash
pip install --user \
    qtile-extras \
    dbus-next \
    dbus-fast \
    dbus-python \
    iwlib \
    psutil \
    pulsectl \
    pulsectl-asyncio \
    python-rofi \
    vdf
```

## Installation

1. **Clone or copy the configuration:**

   ```bash
   # If using GNU Stow from dotfiles
   cd ~/.dotfiles
   stow qtile

   # Or copy directly
   cp -r qtile/.config/qtile ~/.config/
   ```

2. **Install dependencies:**

   ```bash
   cd ~/.config/qtile
   poetry install
   ```

3. **Configure hardware settings:**

   Edit `settings/hardware.py` to match your system:

   ```python
   # Network interface (find with: ip link show)
   WIRELESS_INTERFACE: str = "wlp3s0"

   # Audio device aliases (customize for your setup)
   OUTPUT_ALIASES: dict[str, str] = {
       "Your Audio Device": "Friendly Name",
   }
   ```

4. **Restart Qtile:**

   Press `Mod + Shift + R` or log out and back in.

## Project Structure

```
~/.config/qtile/
├── config.py              # Main entry point
├── settings/              # User configuration
│   ├── apps.py            # Applications (terminal, browser, etc.)
│   ├── hardware.py        # Hardware settings (network, audio)
│   └── theme.py           # Colors, fonts, decorations
├── core/                  # Qtile components
│   ├── bar.py             # Status bar configuration
│   ├── groups.py          # Workspaces and layouts
│   ├── hooks.py           # Event hooks
│   ├── keys.py            # Keyboard shortcuts
│   ├── layouts.py         # Custom layouts
│   ├── mouse.py           # Mouse bindings
│   ├── screens.py         # Screen configuration
│   └── widgets/           # Custom widgets
│       ├── bluetooth.py
│       ├── nvidia.py
│       ├── volume.py
│       ├── vpn.py
│       └── wireless.py
├── services/              # System interfaces
│   ├── audio.py           # PulseAudio control
│   ├── bluetooth.py       # Bluetooth D-Bus
│   ├── network.py         # Network status
│   ├── nvidia.py          # GPU metrics
│   └── system.py          # System capabilities
├── menus/                 # Rofi menus
│   ├── audio.py           # Audio device selector
│   ├── games.py           # Steam games launcher
│   └── projects.py        # Projects launcher
├── pyproject.toml         # Poetry configuration
├── LICENSE
└── README.md
```

## Keybindings

### Window Management

| Key | Action |
|-----|--------|
| `Mod + h/j/k/l` | Focus window left/down/up/right |
| `Mod + Shift + h/j/k/l` | Move window left/down/up/right |
| `Mod + Ctrl + h/j/k/l` | Resize window |
| `Mod + m` | Maximize focused window |
| `Mod + n` | Normalize window sizes |
| `Mod + c` | Close focused window |
| `Mod + Tab` | Toggle between layouts |
| `Mod + f` | Toggle split mode |

### Applications

| Key | Action |
|-----|--------|
| `Mod + Return` | Open terminal |
| `Mod + \` | Open browser |
| `Mod + Space` | Application launcher (Rofi) |
| `Mod + w` | Window switcher |
| `Mod + .` | Emoji picker |

### Custom Menus

| Key | Action |
|-----|--------|
| `Mod + r` | Select audio input |
| `Mod + t` | Select audio output |
| `Mod + ,` | Launch project |
| `Mod + g` | Launch Steam game |

### Workspaces

| Key | Action |
|-----|--------|
| `Mod + 1-9, 0` | Switch to workspace |
| `Mod + Shift + 1-9, 0` | Move window to workspace |
| `Mod + y` | Previous workspace |
| `Mod + u` | Next workspace |

### Multi-Monitor

| Key | Action |
|-----|--------|
| `Mod + i/o/p` | Focus screen 3/1/2 |
| `Mod + Shift + i/o/p` | Move window to screen 3/1/2 |

### Media Keys

| Key | Action |
|-----|--------|
| `XF86AudioRaiseVolume` | Volume up |
| `XF86AudioLowerVolume` | Volume down |
| `XF86AudioMute` | Toggle mute |
| `XF86AudioPlay/Stop/Next/Prev` | Media controls |

### Qtile Control

| Key | Action |
|-----|--------|
| `Mod + Shift + r` | Restart Qtile |
| `Mod + Shift + q` | Quit Qtile |

## Customization

### Changing Colors

Edit `settings/theme.py`:

```python
@dataclass(frozen=True)
class Colors:
    PRIMARY: str = "#41a7fc"  # Change accent color
    # ...
```

### Adding Applications

Edit `settings/apps.py`:

```python
@dataclass(frozen=True)
class Apps:
    TERMINAL: str = "alacritty"  # Change terminal
    BROWSER: str = "firefox"     # Change browser
    # ...
```

### Adding Keybindings

Edit `core/keys.py`:

```python
keys.extend([
    Key([mod], "x", lazy.spawn("my-command"), desc="My action"),
])
```

### Adding Widgets

1. Create widget in `core/widgets/my_widget.py`
2. Register in `core/widgets/__init__.py`
3. Add to bar in `core/bar.py`

## Troubleshooting

### Bluetooth widget not working

Ensure BlueZ is running:

```bash
sudo systemctl start bluetooth
sudo systemctl enable bluetooth
```

### WiFi widget not updating

Check your interface name:

```bash
ip link show
# Update WIRELESS_INTERFACE in settings/hardware.py
```

### Volume widget not working

Ensure PulseAudio is running:

```bash
pulseaudio --start
```

### Steam games not showing

Ensure Steam is installed and has games:

```bash
ls ~/.steam/steam/steamapps/libraryfolders.vdf
```

## Development

### Code Quality

```bash
# Format code
poetry run black .

# Lint code
poetry run ruff check .

# Type check
poetry run mypy .
```

### Testing Configuration

```bash
# Check for syntax errors
python -m py_compile config.py

# Test in nested X session
Xephyr :1 -screen 1920x1080 &
DISPLAY=:1 qtile start
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper type hints and docstrings
4. Run code quality checks
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [Qtile](http://www.qtile.org/) - The window manager
- [qtile-extras](https://github.com/elParaguayo/qtile-extras) - Extended widgets and decorations
- [Rofi](https://github.com/davatorium/rofi) - Application launcher
