# Dotfiles

This repository contains my personal configuration files managed with [GNU Stow](https://www.gnu.org/software/stow/).  
Each directory represents a "package" of configurations.  

## General requirements

You need to have `stow` installed before using these dotfiles:

- **Arch Linux**  

	```bash
	sudo pacman -S stow
	````

* **Ubuntu/Debian**

  ```bash
  sudo apt install stow
  ```

* **macOS (Homebrew)**

  ```bash
  brew install stow
  ```

Clone the repository and enter the directory:

```bash
git clone git@github.com:luisalcarasr/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
```

To apply a package:

```bash
stow <package>
```

To remove it:

```bash
stow -D <package>
```

---

## Packages

### awesome

Dependencies:

* Window manager [awesome](https://awesomewm.org/).
* [xorg](https://wiki.archlinux.org/title/Xorg) must be installed.

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S awesome xorg-xinit
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install awesome xorg
  ```
* **macOS**
  ⚠️ Not officially available.

---

### btop

Dependencies:

* [btop](https://github.com/aristocratos/btop), a system monitor.

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S btop
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install btop
  ```
* **macOS**

  ```bash
  brew install btop
  ```

---

### fish

Dependencies:

* [fish](https://fishshell.com/) shell.

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S fish
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install fish
  ```
* **macOS**

  ```bash
  brew install fish
  ```

---

### fonts

Dependencies:

* [fontconfig](https://www.freedesktop.org/wiki/Software/fontconfig/).

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S fontconfig
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install fontconfig
  ```
* **macOS**
  Already included by default.

---

### git

Dependencies:

* [git](https://git-scm.com/).
* Optional: `git-ai` script (may require `python` or `node` depending on configuration).

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S git
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install git
  ```
* **macOS**

  ```bash
  brew install git
  ```

---

### gtk

Dependencies:

* GTK 2/3/4 libraries.

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S gtk3 gtk4
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install libgtk-3-dev libgtk-4-dev
  ```
* **macOS**

  ```bash
  brew install gtk+3
  ```

---

### kitty

Dependencies:

* [kitty](https://sw.kovidgoyal.net/kitty/) terminal emulator.

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S kitty
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install kitty
  ```
* **macOS**

  ```bash
  brew install kitty
  ```

---

### nvim

Dependencies:

* [Neovim](https://neovim.io/) >= 0.9.
* [git](https://git-scm.com/).
* [nodejs](https://nodejs.org/) and [npm](https://www.npmjs.com/) for some plugins.
* [ripgrep](https://github.com/BurntSushi/ripgrep) for searching.

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S neovim git nodejs npm ripgrep
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install neovim git nodejs npm ripgrep
  ```
* **macOS**

  ```bash
  brew install neovim git node ripgrep
  ```

---

### picom

Dependencies:

* [picom](https://github.com/yshui/picom), a compositor.

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S picom
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install picom
  ```
* **macOS**
  ⚠️ Not available.

---

### rofi

Dependencies:

* [rofi](https://github.com/davatorium/rofi) launcher.

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S rofi
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install rofi
  ```
* **macOS**
  ⚠️ Not available.

---

### tmux

Dependencies:

* [tmux](https://github.com/tmux/tmux), terminal multiplexer.

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S tmux
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install tmux
  ```
* **macOS**

  ```bash
  brew install tmux
  ```

---

### xorg

Dependencies:

* [xorg-xinit](https://wiki.archlinux.org/title/Xinit).

Installation:

* **Arch Linux**

  ```bash
  sudo pacman -S xorg-xinit
  ```
* **Ubuntu/Debian**

  ```bash
  sudo apt install xinit
  ```
* **macOS**
  ⚠️ Not applicable.

# Desktop Environment with [AwesomeWM](https://awesomewm.org/)

## Installation

The instructions intended for Arch Linux.

### Required Software

**Arch Official Repository**
```sh
sudo pacstrap /mnt awesome axel base base-devel bluez bluez-utils btop cpupower discord docker efibootmgr exa firefox fish git gnome-backgrounds gnome-keyring grub inkscape intel-ucode kitty lazygit lightdm-gtk-greeter linux linux-firmware linux-headers lua-language-server neofetch neovim networkmanager nvidia nvidia-settings openssh pacman-contrib pavucontrol picom pipewire-alsa pipewire-jack pipewire-pulse ripgrep rofi rofi-emoji rust-analyzer steam ttf-ibm-plex ttf-ibmplex-mono-nerd ttf-joypixels unzip xclip xdotool xorg-xrdb xorg-xset 
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
git clone --bare --recursive git@github.com:luisalcarasr/dotfiles.git $HOME/.cfg
alias dotctl='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
dotctl checkout
dotctl config --local status.showUntrackedFiles no
```

## Troubleshooting and Enhacements

### Fisher

Plugins for fish shell.
```fish
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
