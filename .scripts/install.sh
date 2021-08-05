sudo pacman -Syy git i3-gaps xorg xorg-server dialog openssh openssl neovim zsh alacritty firefox arc-gtk-theme arc-icon-theme archlinux-wallpaper steam pulseaudio alsa-utils jq nodejs-lts-fermium npm yarn lib32-fontconfig ttf-liberation vifm exa axel feh neofetch catimg intel-ucode obs-studio htop bat ripgrep zip unzip jdk11-openjdk conky code bluez bluez-utils dunst piper git lightdm

git clone https://aur.archlinux.org/yay.git $HOME/yay
cd $HOME/yay
makepkg -si
gpg --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 --recv 27EDEAF22F3ABCEB50DB9A125CC908FDB71E12C2
yay -Syy polybar yay xcursor-breeze spotify mongodb-bin teams discord xbanish autotiling upd72020x-fw wd719x-firmware aic94xx-firmware google-chrome xpadneo-dkms 

sudo modprobe btusb
sudo systemctl enable bluetooth
sudo systemctl enable lightdm

rm -rf $HOME/**
git clone https://github.com/luisalcarasr/ssh.git $HOME/.ssh
echo ".cfg" >> $HOME/.gitignore
git clone --bare --recursive git@github.com:luisalcarasr/dotfiles.git $HOME/.cfg
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
config checkout
rm $HOME/.gitignore
config config --local status.showUntrackedFiles no

source $HOME/.scripts/vscode-extensions.sh
sleep 5
clear
neofetch
sleep 5
sudo reboot
