# Desktop Environment with [Qtile](http://www.qtile.org/)

## Installation

### Required Software
```sh
sudo pacman -Sy xorg xorg-server 
```

```sh
sudo pacman -Sy lightdm lightdm-gtk-greeter
sudo systemctl enable lightdm
```

```sh
sudo pacman -Sy qtile python-pip 
pip install psutil
```

```sh
sudo pacman -Sy xcb-util-cursor
```

```sh
sudo pacman -Sy kitty firefox neovim zsh 
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
