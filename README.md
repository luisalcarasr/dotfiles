# Dotfiles

This repository contains my dotfiles managed with [GNU Stow](https://www.gnu.org/software/stow/); its goal is to provide a reproducible and modular workstation environment (window manager, shell, editor, terminal, productivity tooling, theming and X/org tweaks) focused on Linux (Arch / Debian/Ubuntu) with partial macOS support, relying on declaratively managed symlinks (`stow`) and aiming for minimalist, consistent, easily versioned configuration.  

## Quick Start

You need to have `stow` installed before using these dotfiles:


| Operative System | Command                 |
| ---------------- | ----------------------- |
| Arch Linux       | `sudo pacman -S stow`   |
| Ubuntu/Debian    | `sudo apt install stow` |
| Fedora           | `sudo dnf install stow` |
| MacOS            | `brew install stow`     |

Clone the repository and enter the directory:

```bash
git clone git@github.com:luisalcarasr/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
```

To apply all packages:

```sh
stow .
```

To apply a package:

```bash
stow <package>
```

To remove it:

```bash
stow -D <package>
```

## Dependencies

Install system packages:

```sh
sudo pacman -S --needed - < packages.txt
```

AUR packages (via yay):

```sh
yay -S ttf-symbola-free protonup-rs
```

Flatpak theme extension:

```sh
flatpak install -y flathub org.gtk.Gtk3theme.adw-gtk3-dark
```

### Post-install

Enable services:

```sh
sudo systemctl enable --now NetworkManager bluetooth
```

Apply GTK settings:

```sh
gsettings set org.gnome.desktop.interface gtk-theme    "adw-gtk3-dark"
gsettings set org.gnome.desktop.interface icon-theme   "Adwaita"
gsettings set org.gnome.desktop.interface cursor-theme "Adwaita"
gsettings set org.gnome.desktop.interface font-name    "Adwaita Sans 11"
gsettings set org.gnome.desktop.interface color-scheme "prefer-dark"
```

## Packages

For platform-specific setup instructions, see [SETUP.md](SETUP.md).
