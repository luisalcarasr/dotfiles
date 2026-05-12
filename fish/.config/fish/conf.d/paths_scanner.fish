# paths_scanner.fish
# Dynamically finds bin directories under ~/.* (dotfiles/hidden dirs) and adds them to PATH.
# Also ensures Homebrew paths are configured.

if status is-interactive
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

    # Scan hidden directories (~/.something) for bin/ folders, max 3 levels deep
    # NOTE: fish does not expand regex-style globs like ".[^.]*", so we use
    # find from $HOME with -path "$HOME/.*" to match only hidden directories.
    for dir in (find $HOME -mindepth 1 -maxdepth 4 -type d -name bin \
        -path "$HOME/.*" \
        -not -path "*/.git/*" \
        -not -path "*/node_modules/*" \
        -not -path "*/vendor/*" \
        -not -path "*/.cache/*" \
        -not -path "*/.Trash/*" \
        -not -path "*/.venv/*" \
        -not -path "*/venv/*" \
        -not -path "*/.tox/*" \
        -not -path "*/__pypackages__/*" \
        -not -path "*/.mypy_cache/*" \
        -not -path "*/site-packages/*" \
        -not -path "*/target/debug/*" \
        -not -path "*/target/release/*" \
        2>/dev/null)
        fish_add_path -g $dir
    end
end
