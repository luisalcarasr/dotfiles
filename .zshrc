# Path
export PATH=$PATH:$HOME/.local/bin:$HOME/.config/rofi/menus

# OH MY ZSH
export ZSH=$HOME/.oh-my-zsh
export ZSH_CUSTOM=$HOME/.config/zsh
export ZSH_THEME="powerline"

plugins=(
  sudo
  yarn
)
autoload -U compinit && compinit
source $ZSH/oh-my-zsh.sh

# Aliases
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
alias pacman='sudo pacman'
alias ls='exa'
alias la='exa -la'
alias ll='exa -l'

# TODO: Remove this when we have a better way to do this.
alias ace="cd $ACE && git status && clear"
export ACE=$HOME/Projects/ace
