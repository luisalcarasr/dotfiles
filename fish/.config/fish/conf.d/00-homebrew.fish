# 00-homebrew.fish
# Ensures Homebrew paths are on $PATH early, BEFORE 99-aliases.fish runs.
# This must NOT be gated behind `status is-interactive`: aliases guarded by
# `command -v <tool>` need brew-installed tools (eza, zoxide, nvim, ...) to be
# resolvable when 99-aliases.fish is sourced. The `00-` prefix guarantees this
# file loads before the alias definitions.

# Homebrew (macOS Apple Silicon)
if test -d /opt/homebrew/bin
    fish_add_path -g /opt/homebrew/bin
end
if test -d /opt/homebrew/sbin
    fish_add_path -g /opt/homebrew/sbin
end

# Homebrew (Intel Mac)
if test -d /usr/local/bin
    fish_add_path -g /usr/local/bin
end
