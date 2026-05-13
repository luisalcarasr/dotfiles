# aliases.fish
# Centralized aliases for commands and tools

# eza - modern ls replacement
if command -v eza &> /dev/null
    alias ls='eza --group-directories-first'
    alias ll='eza -l --group-directories-first'
    alias la='eza -la --group-directories-first'
end

# git aliases
if command -v git &> /dev/null
    alias gd='cd $(git rev-parse --show-toplevel)'
end

# ollama - local AI
if command -v ollama &> /dev/null
    alias ai='ollama run gemma3:4b --'
end

# neovim
if command -v nvim &> /dev/null
    alias vim=nvim
    alias vi=vim
end

# python
if command -v python3 &> /dev/null
    alias py=python3
    alias python=python3
end

# pip
if command -v pip3 &> /dev/null
    alias pip=pip3
end

# zoxide - smart cd
if command -v zoxide &> /dev/null
    alias cd=z
end

# docker
alias compose=docker-compose

# opencode - AI coding agent
if command -v opencode &> /dev/null
    alias oc=opencode
end
