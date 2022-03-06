# Desktop Environment with [Qtile](http://www.qtile.org/)

## Installation

The instructions in this tutorial are intended for Arch Linux or distros based on it.

### Required Software

#### Display Server

##### Xorg 
[Xorg](https://wiki.archlinux.org/title/xorg) is the most popular
display server among Linux users. It an ever-present requisite for
GUI applications. Alternatively you can use 
[Wayland](https://wiki.archlinux.org/title/Wayland), but this is not 
supported by NVIDIA. If you want to play, you'll have to use xorg.

```sh
sudo pacman -Sy xorg xorg-server 
```

#### Display Manager

A display manager, or login manager, is typically a graphical user interface
that is displayed at the end of the boot process in place of the default shell.

##### LightDM

[LightDM](https://wiki.archlinux.org/title/LightDM) is chosen for this
installation, as it works out-of-the-box. You will probably want to install a
greeter.

```sh
sudo pacman -Sy lightdm
```

##### Greeter

A [greeter](https://wiki.archlinux.org/title/LightDM#Greeter) is a GUI that
prompts the user for credentials, it's basically the login screen. The
default greeter is a GTK implementation and it will be used in this case.

```sh
sudo pacman -Sy lightdm-gtk-greeter
```

Once installed the Display Manager and its greeter, it will have to be enabled.
It is possible to have multiple display managers installed, but having more
than one installed could cause conflicts between them.

```sh
sudo systemctl enable lightdm
```

#### Window Manager
A [window manager](https://wiki.archlinux.org/title/window_manager) (WM) is
system software that controls the placement and appearance of windows
within a windowing system in a graphical user interface (GUI).

##### Qtile
```sh
sudo pacman -Sy qtile
```

##### Python Libraries
```sh
sudo pacman -Sy python-pip 
```
```sh
pip install psutil
```
```sh
sudo pacman -Sy xcb-util-cursor
```

```sh
sudo pacman -Sy kitty firefox neovim fish
```

```sh
sudo pacman -Sy feh 
```

```sh
sudo pacman -Sy dunst 
```

```sh
sudo pacman -Sy exa 
```

```
yay -Sy xbanish
```

### Implementation

```sh
cd $HOME
```

```sh
find . -not -name '.ssh' -delete
```

```sh
git clone --bare --recursive git@github.com:luisalcarasr/dotfiles.git $HOME/.cfg
```

```sh
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
```

```sh
config checkout
```

```sh
config config --local status.showUntrackedFiles no
```

### System Utilities

```sh
sudo pacman -Syyu zip unzip htop axel neofeth 
```

## References

https://wiki.archlinux.org/title/xorg
https://wiki.archlinux.org/title/LightDM
