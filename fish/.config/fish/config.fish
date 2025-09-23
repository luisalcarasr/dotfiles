set fish_greeting

# Aliases
alias ls='eza --group-directories-first'
alias ll='eza -l --group-directories-first'
alias la='eza -la --group-directories-first'
alias gd='cd $(git rev-parse --show-toplevel)'
alias ai='ollama run gemma3:4b --'

# Google Cloud SDK.
if [ -f '/Users/l.alcaras/.google-cllooud-sdk/google-cloud-sdk/path.fish.inc' ]
    . '/Users/l.alcaras/.google-cllooud-sdk/google-cloud-sdk/path.fish.inc'
end

# Python
if [ -f '/Library/Frameworks/Python.framework/Versions/3.12/bin' ]
    set -x PATH '/Library/Frameworks/Python.framework/Versions/3.12/bin' "$PATH"
end
