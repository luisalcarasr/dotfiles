# dotfiles_bootstrap.fish
# Runs on every fish startup via conf.d.
# Ensures fisher and required plugins are installed.
# Uses a flag to avoid running the full bootstrap on every shell.

if status is-interactive
    # Only bootstrap once per machine - use a universal variable as flag
    if not set -q __dotfiles_bootstrapped
        # Install fisher if not available
        if not functions -q fisher
            echo "[dotfiles] Installing fisher..."
            curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source
            fisher install jorgebucaran/fisher 2>/dev/null
        end

        # Required plugins
        set -l required_plugins \
            jorgebucaran/nvm.fish \
            IlanCosman/tide \
            luisalcarasr/repojump

        if functions -q fisher
            # Get currently installed plugins
            set -l installed (fisher list 2>/dev/null)

            for plugin in $required_plugins
                # Check if plugin is already installed (match by name, case-insensitive)
                set -l found 0
                for item in $installed
                    if string match -qi -- "*"(string split "/" $plugin)[-1]"*" $item
                        set found 1
                        break
                    end
                end

                if test $found -eq 0
                    echo "[dotfiles] Installing plugin: $plugin"
                    fisher install $plugin 2>/dev/null
                end
            end
        end

        # Set nvm default version if not already set
        if not set -q nvm_default_version
            set --universal nvm_default_version lts
        end

        # Mark bootstrap as complete
        set --universal __dotfiles_bootstrapped 1
        echo "[dotfiles] Bootstrap complete."
    end

    # Always ensure fisher is functional on interactive shells
    # (in case the fish_plugins file was restored via stow)
    if not functions -q fisher
        curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source
        fisher install jorgebucaran/fisher 2>/dev/null
        fisher update 2>/dev/null
    end
end
