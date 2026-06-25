# opencode.fish
# Selects the machine-specific opencode overlay via OPENCODE_CONFIG.
# Default: personal machine (Zen, free models).
# Only the F5 Inc work machine is detected explicitly by hostname.

if test (hostname) = LRXK600KY0
    set -gx OPENCODE_CONFIG ~/.config/opencode/machines/work.json
    set -gx F5AI_BASE_URL https://f5ai.pd.f5net.com/openai/v1
else
    set -gx OPENCODE_CONFIG ~/.config/opencode/machines/personal.json
end
