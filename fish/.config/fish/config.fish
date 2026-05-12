set fish_greeting

# Initialize zoxide if available
if command -v zoxide &> /dev/null
    zoxide init fish | source
end

# Aliases - only create if commands exist
if command -v eza &> /dev/null
    alias ls='eza --group-directories-first'
    alias ll='eza -l --group-directories-first'
    alias la='eza -la --group-directories-first'
end

if command -v git &> /dev/null
    alias gd='cd $(git rev-parse --show-toplevel)'
end

if command -v ollama &> /dev/null
    alias ai='ollama run gemma3:4b --'
end

if command -v nvim &> /dev/null
    alias vim=nvim
    alias vi=vim
end

if command -v python3 &> /dev/null
    alias py=python3
    alias python=python3
end

if command -v pip3 &> /dev/null
    alias pip=pip3
end

# Replace cd with zoxide only if zoxide is installed
if command -v zoxide &> /dev/null
    alias cd=z
end

alias compose=docker-compose

# Google Cloud SDK.
if [ -f '/Users/l.alcaras/.google-cllooud-sdk/google-cloud-sdk/path.fish.inc' ]
    . '/Users/l.alcaras/.google-cllooud-sdk/google-cloud-sdk/path.fish.inc'
end

# Python
if test -d '/Library/Frameworks/Python.framework/Versions/3.12/bin'
    fish_add_path -g '/Library/Frameworks/Python.framework/Versions/3.12/bin'
end

# opencode and antigravity paths are handled by conf.d/paths_scanner.fish

# If tide is installed but not configured, run tide configure
if status is-interactive
    if type -q tide; and not set -q tide_left_prompt_items
        echo "Tide is not configured. Running tide configure..."
        tide configure
    end
end
