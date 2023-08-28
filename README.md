# Desktop Environment with [AwesomeWM](https://awesomewm.org/)

## Installation

The instructions intended for Arch Linux.

### Required Software

**Arch Official Repository**
```sh
sudo pacstrap /mnt awesome axel base base-devel bluez bluez-utils btop cpupower discord docker efibootmgr exa firefox fish git gnome-backgrounds gnome-keyring grub inkscape intel-ucode kitty lazygit lightdm-gtk-greeter linux linux-firmware linux-headers lua-language-server neofetch neovim networkmanager nvidia nvidia-settings openssh pacman-contrib pavucontrol picom pipewire-alsa pipewire-jack pipewire-pulse ripgrep rofi rofi-emoji rust-analyzer steam ttf-ibm-plex ttf-ibmplex-mono-nerd ttf-joypixels unzip xclip xdotool xorg-xrdb xorg-xset
```

**Arch User Repository**

_An AUR Helper Written in Go_
```sh
git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
makepkg -si
cd ..
rm -rf yay-bin
```

_Dependencies_
```sh
yay -Sy ttf-symbola-free spotify notion-app slack-desktop protonup-rs
```

### Implementation

```sh
git clone --bare --recursive git@github.com:luisalcarasr/dotfiles.git $HOME/.cfg
```

```sh
alias dotctl='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
```

```sh
dotctl checkout
```

```sh
dotctl config --local status.showUntrackedFiles no
```

## Troubleshooting and Enhacements

### Fisher

Plugins for fish shell.
```sh
# Plugin Manager installation.
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source
fisher install jorgebucaran/fisher

# Prompt
fisher install IlanCosman/tide@v5

# Node Version Manager
fisher install jorgebucaran/nvm.fish
set --universal nvm_default_packages yarn npm
set --universal nvm_default_version lts/gallium
nvm install lts/gallium
```

### Disabling mouse acceleration

To completely disable any sort of acceleration/deceleration, create the following file:

```sh
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
