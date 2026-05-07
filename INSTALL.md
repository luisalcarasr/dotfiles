# Installation Instructions

This document contains installation instructions for different distributions.

## [Arch Linux](https://archlinux.org/) + [AwesomeWM](https://awesomewm.org/)

The instructions intended for Arch Linux.

### Required Software

**Arch Official Repository**
```sh
sudo pacstrap /mnt awesome axel base base-devel bluez bluez-utils btop cpupower docker efibootmgr exa firefox fish git gnome-keyring grub hyprland intel-ucode kitty lazygit sddm linux linux-firmware linux-headers fastfetch neovim networkmanager nvidia openssh pacman-contrib pipewire-alsa pipewire-jack pipewire-pulse ripgrep wofi steam stow ttf-ibm-plex ttf-ibmplex-mono-nerd unzip waybar
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

## Troubleshooting and Enhancements

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
