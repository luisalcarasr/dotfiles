#!/bin/bash
# Steam Games Menu for Wofi
# Lists installed Steam games and launches selected game

STEAM_DIR="$HOME/.local/share/Steam/steamapps"
MANIFEST_DIR="$STEAM_DIR"

# Check if Steam directory exists
if [ ! -d "$STEAM_DIR" ]; then
    notify-send "Steam Games" "Steam directory not found" -u critical
    exit 1
fi

# Array to store game names and app IDs
declare -A games

# Blacklist for non-game entries
blacklist=(
    "Proton"
    "Steam Linux Runtime"
    "Steamworks Common Redistributables"
    "SteamVR"
)

# Parse all appmanifest files
for manifest in "$MANIFEST_DIR"/appmanifest_*.acf; do
    if [ -f "$manifest" ]; then
        # Extract app ID from filename
        appid=$(basename "$manifest" | sed 's/appmanifest_//;s/.acf//')
        
        # Extract game name from manifest
        gamename=$(grep '"name"' "$manifest" | head -n1 | sed 's/.*"name"[[:space:]]*"\(.*\)"/\1/')
        
        # Check if game is in blacklist
        skip=0
        for blacklisted in "${blacklist[@]}"; do
            if [[ "$gamename" == *"$blacklisted"* ]]; then
                skip=1
                break
            fi
        done
        
        if [ -n "$gamename" ] && [ $skip -eq 0 ]; then
            games["$gamename"]="$appid"
        fi
    fi
done

# Check if any games were found
if [ ${#games[@]} -eq 0 ]; then
    notify-send "Steam Games" "No games found" -u normal
    exit 1
fi

# Sort game names and display in wofi
selected=$(printf '%s\n' "${!games[@]}" | sort | wofi --dmenu --prompt "Launch Game" --width 600 --height 400)

# Launch selected game
if [ -n "$selected" ]; then
    appid="${games[$selected]}"
    notify-send "Launching" "$selected"
    
    # Launch game via Steam
    if [ -f "$HOME/.local/share/Steam/steam.sh" ]; then
        nohup "$HOME/.local/share/Steam/steam.sh" "steam://rungameid/$appid" > /dev/null 2>&1 &
        disown
    elif command -v xdg-open &> /dev/null; then
        nohup xdg-open "steam://rungameid/$appid" > /dev/null 2>&1 &
        disown
    else
        notify-send "Error" "Could not find Steam launcher" -u critical
    fi
fi
