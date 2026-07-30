# opencode.fish
# Selects the machine-specific opencode overlay via OPENCODE_CONFIG.
# Default: personal machine (Zen, free models).
# The F5 Inc work machine is detected by the presence of F5AI_API_KEY.
#
# XDG_CONFIG_HOME: ensures XDG-aware tools (mods, etc.) read from
# ~/.config instead of macOS-default ~/Library/Application Support.
set -gx XDG_CONFIG_HOME $HOME/.config

# AICHAT_CONFIG_DIR: aichat on macOS defaults to ~/Library/Application Support/aichat;
# this overrides it to follow the XDG convention alongside other dotfiles.
set -gx AICHAT_CONFIG_DIR $HOME/.config/aichat

if set -q F5AI_API_KEY
    set -gx OPENCODE_CONFIG ~/.config/opencode/machines/work.json
    set -gx F5AI_BASE_URL https://f5ai.pd.f5net.com/openai/v1
else
    set -gx OPENCODE_CONFIG ~/.config/opencode/machines/personal.json
end
