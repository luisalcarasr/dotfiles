function fish_doctor -d "Check that all required plugins and binaries are installed"
    set -l pass (set_color green)"OK"(set_color normal)
    set -l fail (set_color red)"MISSING"(set_color normal)
    set -l warn (set_color yellow)"WARN"(set_color normal)
    set -l errors 0

    echo (set_color --bold)"=== Fish Doctor ==="(set_color normal)
    echo

    # --- Fish Plugins ---
    echo (set_color --bold)"Plugins"(set_color normal)

    # Fisher
    if functions -q fisher
        echo "  fisher        $pass"
    else
        echo "  fisher        $fail"
        set errors (math $errors + 1)
    end

    # Check installed plugins via fisher list
    set -l installed
    if functions -q fisher
        set installed (fisher list 2>/dev/null)
    end

    set -l required_plugins \
        "nvm.fish:jorgebucaran/nvm.fish" \
        "tide:IlanCosman/tide" \
        "repojump:luisalcarasr/repojump"

    for entry in $required_plugins
        set -l name (string split ":" $entry)[1]
        set -l full (string split ":" $entry)[2]
        set -l found 0

        for item in $installed
            if string match -qi -- "*$name*" $item
                set found 1
                break
            end
        end

        if test $found -eq 1
            echo "  $name"(string repeat -n (math 14 - (string length $name)) " ")"$pass"
        else
            echo "  $name"(string repeat -n (math 14 - (string length $name)) " ")"$fail  (fisher install $full)"
            set errors (math $errors + 1)
        end
    end

    echo

    # --- NVM Configuration ---
    echo (set_color --bold)"NVM Configuration"(set_color normal)

    if set -q nvm_default_version
        echo "  nvm_default_version = $nvm_default_version  $pass"
    else
        echo "  nvm_default_version $fail  (set --universal nvm_default_version lts)"
        set errors (math $errors + 1)
    end

    if command -q node
        echo "  node          $pass  ("(node --version)")"
    else
        echo "  node          $warn  (run: nvm install lts)"
    end

    echo

    # --- Required Binaries ---
    echo (set_color --bold)"Binaries"(set_color normal)

    set -l required_binaries \
        "git:git" \
        "fish:fish" \
        "nvim:neovim" \
        "stow:stow" \
        "curl:curl" \
        "eza:eza" \
        "zoxide:zoxide" \
        "rg:ripgrep" \
        "btop:btop" \
        "kitty:kitty" \
        "lazygit:lazygit" \
        "docker:docker" \
        "fastfetch:fastfetch"

    for entry in $required_binaries
        set -l cmd (string split ":" $entry)[1]
        set -l pkg (string split ":" $entry)[2]

        if command -q $cmd
            set -l _cmd_version ""
            # Try to get version for common tools
            switch $cmd
                case git
                    set _cmd_version (git --version 2>/dev/null | string replace "git version " "")
                case nvim
                    set _cmd_version (nvim --version 2>/dev/null | head -1 | string replace "NVIM " "")
                case node
                    set _cmd_version (node --version 2>/dev/null)
                case fish
                    set _cmd_version (fish --version 2>/dev/null | string replace "fish, version " "")
                case eza
                    set _cmd_version (eza --version 2>/dev/null | head -1)
                case rg
                    set _cmd_version (rg --version 2>/dev/null | head -1 | string replace "ripgrep " "")
                case docker
                    set _cmd_version (docker --version 2>/dev/null | string replace "Docker version " "" | string split ",")[1]
            end

            if test -n "$_cmd_version"
                echo "  $cmd"(string repeat -n (math 14 - (string length $cmd)) " ")"$pass  ($_cmd_version)"
            else
                echo "  $cmd"(string repeat -n (math 14 - (string length $cmd)) " ")"$pass"
            end
        else
            echo "  $cmd"(string repeat -n (math 14 - (string length $cmd)) " ")"$fail  (install $pkg)"
            set errors (math $errors + 1)
        end
    end

    echo

    # --- Optional Binaries ---
    echo (set_color --bold)"Optional"(set_color normal)

    set -l optional_binaries \
        "ollama:ollama" \
        "python3:python3" \
        "pip3:pip3"

    for entry in $optional_binaries
        set -l cmd (string split ":" $entry)[1]
        set -l pkg (string split ":" $entry)[2]

        if command -q $cmd
            echo "  $cmd"(string repeat -n (math 14 - (string length $cmd)) " ")"$pass"
        else
            echo "  $cmd"(string repeat -n (math 14 - (string length $cmd)) " ")"$warn"
        end
    end

    echo

    # --- Summary ---
    if test $errors -eq 0
        echo (set_color green --bold)"All checks passed."(set_color normal)
    else
        echo (set_color red --bold)"$errors issue(s) found."(set_color normal)
        echo "Run the suggested commands to fix them."
    end

    return $errors
end
