# Installing Arch Linux

## Installation

fdisk /dev/nvme0n1
fdisk /dev/sda

mkfs.fat -FAT32 /dev/nvme0n1p0
mkfs.ext4 /dev/nvme0n1p1
mkfs.ext4 /dev/sda1

mount /dev/nvme0n1p1 /mnt
mkdir -P /mnt/boot/efi
mount /dev/nvme0n1p1 /mnt

pacstrap /mnt base base-devel linux-zen linux-zen-headers linux-firmware neovim grub efibootmgr intel-ucode networkmanager

genfstab -U /mnt >> /mnt/etc/fstab

arch-chroot /mnt

ln -s /bin/nvim vim
ln -s /bin/nvim vi

ln -sf /usr/share/zoneinfo/America/Mexico_City /etc/localtime

hwclock --systohc

Edit /etc/locale.gen and uncomment en_US.UTF-8 UTF-8

Create the locale.conf

LANG=en_US.UTF-8

Create the hostname file /etc/hostname

echo 'arch' >> /etc/hostname

mkinitcpio -P

passwd

grub-install --target=x86_64-efi --efi-directory=/boot/efi --removable

grub-mkconfig -o /boot/grub/grub.cfg

exit

reboot

## Setup

### User setup

useradd luis -U -d /home/luis

mkdir /home/luis

sudo chown luis:luis /home/luis

passwd luis

Add user to sudoers file

sudo vi /etc/sudoers

exit

Login as luis

### Installing a Window Manager

sudo systemctl enable NetworkManager

Enable multilib in /etc/pacman.conf

sudo pacman -Syyu xorg xorg-server alacritty firefox lightdm lightdm-gtk-greeter qtile python-pip xcb-util-cursor

sudo pacman -Syyu arc-gtk-theme arc-icon-theme archlinux-wallpaper feh 

pip install psutil

sudo systemctl enable lightdm

### Installing AUR utility

sudo pacman -Syyu git

git clone https://aur.archlinux.org/yay.git ~/yay

cd ~/yay

makepkg -si

yay -Syyu

### Configurate a new OpenSSH key.

sudo pacman -Syyu openssh 

ssh-keygen -t ed25519 -C luisalcarasr@gmail.com

eval "$(ssh-agent -s)"

ssh-add ~/.ssh/id_ed25519

cat ~/.ssh/id_ed25519.pub

Then select and copy the contents of the id_ed25519.pub file displayed in the terminal to your clipboard

### Git

Configure your git user name and email.

git config --global user.name 'Luis Alcaras'
git config --global user.email luisalcarasr@gmail.com

Don't forget set your corporative email for private projects.

### DotFiles

cd
find . -not -name '.ssh' -delete
git clone --bare --recursive git@github.com:luisalcarasr/dotfiles.git $HOME/.cfg
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
config checkout
config config --local status.showUntrackedFiles no

### Configuring Audio and Bluetooth

sudo pacman -Syyu pulseaudio alsa-utils bluez bluez-utils

sudo modprobe btusb
sudo systemctl enable bluetooth

### Missing firmware

yay -Syyu upd72020x-fw wd719x-firmware aic94xx-firmware 

mkinitcpio -P

### Development

sudo pacman -Syyu nodejs-lts-fermium jdk11-openjdk bat ripgrep npm yarn 

gpg --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 --recv 27EDEAF22F3ABCEB50DB9A125CC908FDB71E12C2

yay -Syyu teams mongodb-bin

cd ~/.config

git clone git@github.com:luisalcarasr/nvim.git

## Shell

sudo pacman -Syyu zsh

sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

## Gaming

sudo pacman -Syyu steam lib32-fontconfig ttf-liberation

sudo yay -Syyu xpadneo-dkms discord

## System Utilities

sudo pacman -Syyu zip unzip htop exa axel neofetch xbanish piper 

## Multimedia

sudo pacman -Syyu obs-studio gimp inkscape

yay -Syyu google-chrome spotify davinci-resolve

## Others (Opcional)

sudo pacman -Syyu openssl jq vifm catimg dunst 
