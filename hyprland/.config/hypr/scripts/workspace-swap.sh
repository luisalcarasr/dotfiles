#!/bin/bash
# Script to swap workspaces between monitors in Hyprland
# If the target workspace is visible on another monitor, swap them
# Otherwise, just switch to that workspace

TARGET_WS=$1

if [ -z "$TARGET_WS" ]; then
    echo "Usage: $0 <workspace_id>"
    exit 1
fi

# Get current monitor and workspace
CURRENT_MONITOR=$(hyprctl monitors -j | jq -r '.[] | select(.focused == true) | .name')
CURRENT_WS=$(hyprctl monitors -j | jq -r '.[] | select(.focused == true) | .activeWorkspace.id')

# Find which monitor has the target workspace
TARGET_MONITOR=$(hyprctl monitors -j | jq -r ".[] | select(.activeWorkspace.id == $TARGET_WS) | .name")

# If target workspace is not visible on any monitor, just switch to it
if [ -z "$TARGET_MONITOR" ]; then
    hyprctl dispatch workspace "$TARGET_WS"
    exit 0
fi

# If target workspace is on the current monitor, do nothing (already there)
if [ "$TARGET_MONITOR" == "$CURRENT_MONITOR" ]; then
    exit 0
fi

# Swap workspaces between monitors
# Move target workspace to current monitor
hyprctl dispatch focusmonitor "$TARGET_MONITOR"
hyprctl dispatch workspace "$CURRENT_WS"
hyprctl dispatch focusmonitor "$CURRENT_MONITOR"
hyprctl dispatch workspace "$TARGET_WS"
