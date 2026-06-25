# opencode.fish
# Selects the machine-specific opencode overlay via OPENCODE_CONFIG.
# Default: personal machine (Zen, free models).
# The F5 Inc work machine is detected by the presence of F5AI_API_KEY.

if set -q F5AI_API_KEY
    set -gx OPENCODE_CONFIG ~/.config/opencode/machines/work.json
    set -gx F5AI_BASE_URL https://f5ai.pd.f5net.com/openai/v1
else
    set -gx OPENCODE_CONFIG ~/.config/opencode/machines/personal.json
end
