if status is-interactive
    # Commands to run in interactive sessions can go here
end
set fish_greeting
alias dotctl='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
alias ls='exa -la --git'