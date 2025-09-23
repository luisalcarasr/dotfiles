# Dotfiles

This repository contains my dotfiles managed with [GNU Stow](https://www.gnu.org/software/stow/); its goal is to provide a reproducible and modular workstation environment (window manager, shell, editor, terminal, productivity tooling, theming and X/org tweaks) focused on Linux (Arch / Debian/Ubuntu) with partial macOS support, relying on declaratively managed symlinks (`stow`) and aiming for minimalist, consistent, easily versioned configuration.  

## Quick Start

You need to have `stow` installed before using these dotfiles:


| Operative System | Command                 |
| ---------------- | ----------------------- |
| Arch Linux       | `sudo pacman -S stow`   |
| Ubuntu           | `sudo apt install stow` |
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

## Packages

## [Arch Linux](https://archlinux.org/) + [AwesomeWM](https://awesomewm.org/)

The instructions intended for Arch Linux.

### Required Software

**Arch Official Repository**
```sh
sudo pacstrap /mnt awesome axel base base-devel bluez bluez-utils btop cpupower discord docker efibootmgr exa firefox fish git gnome-backgrounds gnome-keyring grub inkscape intel-ucode kitty lazygit lightdm-gtk-greeter linux linux-firmware linux-headers lua-language-server neofetch neovim networkmanager nvidia nvidia-settings openssh pacman-contrib pavucontrol picom pipewire-alsa pipewire-jack pipewire-pulse ripgrep rofi rofi-emoji rust-analyzer steam stow ttf-ibm-plex ttf-ibmplex-mono-nerd ttf-joypixels unzip xclip xdotool xorg-xrdb xorg-xset 
```

**Arch User Repository**

```fish
# An AUR Helper Written in Go
git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
makepkg -si
cd ..
rm -rf yay-bin

# Dependencies
yay -Sy ttf-symbola-free spotify notion-app slack-desktop protonup-rs
```

### Implementation

```fish
git clone git@github.com:luisalcarasr/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
stow .
```

## Troubleshooting and Enhacements

### Disabling mouse acceleration

To completely disable any sort of acceleration/deceleration, create the following file:

```fish
vi /etc/X11/xorg.conf.d/50-mouse-acceleration.conf
```

```conf
Section "InputClass"
	Identifier "My Mouse"
	MatchIsPointer "yes"
	Option "AccelerationProfile" "-1"
	Option "AccelerationScheme" "none"
	Option "AccelSpeed" "-1"
EndSection
```

## References

- https://www.atlassian.com/git/tutorials/dotfiles
- https://wiki.archlinux.org/title/xorg
- https://wiki.archlinux.org/title/lightdm
