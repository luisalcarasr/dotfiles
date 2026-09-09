function fp -d "Search and install Flatpak apps with fzf"
    # --- Validate dependencies ---
    command -q flatpak; or begin
        echo "fp: flatpak is not installed" >&2
        return 1
    end
    command -q fzf; or begin
        echo "fp: fzf is not installed" >&2
        return 1
    end

    # --- Validate arguments ---
    if test -z "$argv"
        echo "fp: usage: fp <search-term>" >&2
        return 1
    end

    # --- Search and select apps through fzf ---
    # Show app ID + description, keep only the app ID for installation.
    set -l selected (flatpak search --columns=application,description "$argv" \
        | fzf -m --with-nth=1,2 --delimiter='\t' \
        | string replace -r '\t.*' '')

    if test -z "$selected"
        echo "fp: no selection" >&2
        return 1
    end

    # --- Install each selected app (system, interactive confirmation) ---
    for app in $selected
        echo "==> Installing $app"
        flatpak install flathub "$app"
    end
end