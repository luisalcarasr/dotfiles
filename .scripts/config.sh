rm -rf $HOME/**
git clone https://github.com/luisalcarasr/ssh.git $HOME/.ssh
echo ".cfg" >> $HOME/.gitignore
git clone --bare --recursive git@github.com:luisalcarasr/dotfiles.git $HOME/.cfg
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
config checkout
rm $HOME/.gitignore
config config --local status.showUntrackedFiles no
