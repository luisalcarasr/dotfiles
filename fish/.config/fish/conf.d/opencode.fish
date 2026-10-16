# opencode.fish
# XDG_CONFIG_HOME: ensures XDG-aware tools (mods, etc.) read from
# ~/.config instead of macOS-default ~/Library/Application Support.
set -gx XDG_CONFIG_HOME $HOME/.config

# AICHAT_CONFIG_DIR: aichat on macOS defaults to ~/Library/Application Support/aichat;
# this overrides it to follow the XDG convention alongside other dotfiles.
set -gx AICHAT_CONFIG_DIR $HOME/.config/aichat