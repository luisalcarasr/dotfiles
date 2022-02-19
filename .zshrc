ZSH_ANTIGEN=$HOME/.config/zsh/antigen.zsh
ZSH_CUSTOM=$HOME/.config/zsh
ZSH_THEME="powerline"

source $ZSH_ANTIGEN 2>/dev/null || {
  printf '\033[34m'
  echo "Installing Antigen Plugin Manager..."
  printf '\033[0m'
  curl -L git.io/antigen > $ZSH_ANTIGEN
  source $ZSH_ANTIGEN
}

antigen use oh-my-zsh

antigen bundle zsh-users/zsh-autosuggestions
antigen bundle zsh-users/zsh-completions
antigen bundle zsh-users/zsh-syntax-highlighting
antigen bundle zpm-zsh/colors
antigen bundle zuxfoucault/colored-man-pages_mod
antigen bundle akoenig/npm-run.plugin.zsh
antigen bundle g-plane/zsh-yarn-autocompletions
antigen bundle jessarcher/zsh-artisan
antigen bundle jeffreytse/zsh-vi-mode
# antigen bundle zshzoo/cd-ls

antigen theme gentoo

antigen apply

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
