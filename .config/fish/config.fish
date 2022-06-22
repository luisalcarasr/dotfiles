if status is-interactive
    # Commands to run in interactive sessions can go here
end
set fish_greeting
alias dotctl='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
alias ls='exa --git'
alias py=python
alias htb='nmcli c up HTB && sudo route del -net default gw 10.10.14.1 netmask 0.0.0.0 dev tun0'
