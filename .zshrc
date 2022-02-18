# Path
export PATH=$PATH:$HOME/.local/bin:$HOME/.config/rofi/menus

# Oh My Zsh
export ZSH=$HOME/.oh-my-zsh
export ZSH_CUSTOM=$HOME/.config/zsh
export ZSH_THEME="powerline"

# ZSH Plugin Manager
if [[ ! -f ~/.zpm/zpm.zsh ]]; then
  git clone --recursive https://github.com/zpm-zsh/zpm ~/.zpm
fi
source ~/.zpm/zpm.zsh

zpm load @github/zsh-users/zsh-autosuggestions
zpm load @github/zsh-users/zsh-completions
zpm load @github/zsh-users/zsh-syntax-highlighting
zpm load @github/zpm-zsh/colors
zpm load @github/zuxfoucault/colored-man-pages_mod
zpm load @github/akoenig/npm-run.plugin.zsh
zpm load @github/g-plane/zsh-yarn-autocompletions
zpm load @github/jessarcher/zsh-artisan
zpm load @github/jeffreytse/zsh-vi-mode

# Autoload Oh My Zsh
autoload -U compinit && compinit
source $ZSH/oh-my-zsh.sh

# Aliases
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
alias pacman='sudo pacman'
alias ls='exa'
alias la='exa -la'
alias ll='exa -l'

# TODO: Remove this when we have a better way to do this.
export MAIN_PROJECT=$HOME/Projects/ace
alias main="cd $MAIN_PROJECT && git status && clear"
alias edit="cd $MAIN_PROJECT && nvim ."
