# opencode.fish
# Selects the machine-specific opencode overlay via OPENCODE_CONFIG.
# Default: personal machine (Zen, free models).
#
# XDG_CONFIG_HOME: ensures XDG-aware tools (mods, etc.) read from
# ~/.config instead of macOS-default ~/Library/Application Support.
set -gx XDG_CONFIG_HOME $HOME/.config

# AICHAT_CONFIG_DIR: aichat on macOS defaults to ~/Library/Application Support/aichat;
# this overrides it to follow the XDG convention alongside other dotfiles.
set -gx AICHAT_CONFIG_DIR $HOME/.config/aichat

set -gx OPENCODE_CONFIG ~/.config/opencode/machines/personal.json