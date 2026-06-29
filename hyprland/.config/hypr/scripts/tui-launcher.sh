#!/bin/bash
TUI_NAME="$1"
shift
kitty --class "tui-floating" --title "TUI: $TUI_NAME" -e "$TUI_NAME" "$@"
