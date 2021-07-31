git clone https://aur.archlinux.org/yay.git $HOME/yay
cd $HOME/yay
makepkg -si
gpg --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 --recv 27EDEAF22F3ABCEB50DB9A125CC908FDB71E12C2
yay -Syy polybar yay xcursor-breeze spotify mongodb-bin teams discord xbanish autotiling upd72020x-fw wd719x-firmware aic94xx-firmware google-chrome 
