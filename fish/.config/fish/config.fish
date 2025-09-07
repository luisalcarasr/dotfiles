set fish_greeting

# Aliases
alias ls='exa --group-directories-first'
alias ll='exa -l --group-directories-first'
alias la='exa -la --group-directories-first'
alias gd='cd $(git rev-parse --show-toplevel)'

# Google Cloud SDK.
if [ -f '/Users/l.alcaras/.google-cllooud-sdk/google-cloud-sdk/path.fish.inc' ]
    . '/Users/l.alcaras/.google-cllooud-sdk/google-cloud-sdk/path.fish.inc'
end

# Python
if [ -f '/Library/Frameworks/Python.framework/Versions/3.12/bin' ]
    set -x PATH '/Library/Frameworks/Python.framework/Versions/3.12/bin' "$PATH"
end
