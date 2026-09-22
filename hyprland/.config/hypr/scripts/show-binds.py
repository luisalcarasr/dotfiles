#!/usr/bin/env python3
"""Hyprland keybindings menu.

Lists every documented bind in wofi. Selecting one with Enter executes the
real action via `hyprctl dispatch 'hl.dsp.X(...)'`.

NOTE: ACTIONS must stay in sync with the binds declared in hyprland.lua.
"""

import json
import subprocess

MOD_BITS = {"SUPER": 64, "CTRL": 4, "ALT": 8, "SHIFT": 1}

# (modmask, key) -> Lua dispatcher invocation for `hyprctl dispatch`
ACTIONS = {
    # Launch programs
    (64, "RETURN"): 'hl.dsp.exec_cmd("kitty")',
    (64, "BACKSLASH"): 'hl.dsp.exec_cmd("flatpak run com.brave.Browser")',
    (64, "SPACE"): 'hl.dsp.exec_cmd("wofi")',
    (64, "G"): 'hl.dsp.exec_cmd("lua " .. home .. "/.config/hypr/scripts/steam-games-menu.lua")',
    (64, "N"): 'hl.dsp.exec_cmd("makoctl mode -t dnd")',
    # Window management
    (64, "Q"): "hl.dsp.window.close()",
    (64, "V"): 'hl.dsp.window.float({ action = "toggle" })',
    (64, "P"): "hl.dsp.window.pseudo()",
    (64, "F"): 'hl.dsp.window.fullscreen({ mode = "fullscreen", action = "toggle" })',
    # Power actions
    (65, "Escape"): "hl.dsp.exit()",
    (68, "Escape"): 'hl.dsp.exec_cmd("systemctl reboot")',
    (72, "Escape"): 'hl.dsp.exec_cmd("systemctl poweroff")',
    # Reload config
    (64, "R"): 'hl.dsp.exec_cmd("hyprctl reload")',
    # Move focus
    (64, "H"): 'hl.dsp.focus({ direction = "l" })',
    (64, "L"): 'hl.dsp.focus({ direction = "r" })',
    (64, "K"): 'hl.dsp.focus({ direction = "u" })',
    (64, "J"): 'hl.dsp.focus({ direction = "d" })',
    # Move window
    (65, "H"): 'hl.dsp.window.move({ direction = "l" })',
    (65, "L"): 'hl.dsp.window.move({ direction = "r" })',
    (65, "K"): 'hl.dsp.window.move({ direction = "u" })',
    (65, "J"): 'hl.dsp.window.move({ direction = "d" })',
    # Resize window
    (72, "H"): "hl.dsp.window.resize({ x = -20, y = 0 })",
    (72, "L"): "hl.dsp.window.resize({ x = 20, y = 0 })",
    (72, "K"): "hl.dsp.window.resize({ x = 0, y = -20 })",
    (72, "J"): "hl.dsp.window.resize({ x = 0, y = 20 })",
    # Navigate workspaces
    (64, "right"): 'hl.dsp.exec_cmd(home .. "/.config/hypr/scripts/workspace-nav.py next")',
    (64, "left"): 'hl.dsp.exec_cmd(home .. "/.config/hypr/scripts/workspace-nav.py prev")',
    # Special workspace
    (64, "S"): 'hl.dsp.workspace.toggle_special("magic")',
    (65, "S"): 'hl.dsp.window.move({ workspace = "special:magic" })',
    # Multimedia keys
    (0, "XF86AudioRaiseVolume"): 'hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+")',
    (0, "XF86AudioLowerVolume"): 'hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-")',
    (0, "XF86AudioMute"): 'hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")',
    (0, "XF86AudioMicMute"): 'hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle")',
    (64, "PLUS"): 'hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+")',
    (64, "MINUS"): 'hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-")',
    (0, "XF86MonBrightnessUp"): 'hl.dsp.exec_cmd("brightnessctl set 5%+")',
    (0, "XF86MonBrightnessDown"): 'hl.dsp.exec_cmd("brightnessctl set 5%-")',
    # Playerctl
    (0, "XF86AudioNext"): 'hl.dsp.exec_cmd("playerctl next")',
    (0, "XF86AudioPause"): 'hl.dsp.exec_cmd("playerctl play-pause")',
    (0, "XF86AudioPlay"): 'hl.dsp.exec_cmd("playerctl play-pause")',
    (0, "XF86AudioPrev"): 'hl.dsp.exec_cmd("playerctl previous")',
    # Toggle secondary monitors
    (64, "X"): 'hl.dsp.exec_cmd(home .. "/.config/hypr/scripts/toggle-secondary-monitors.sh")',
}

# Workspace binds (SUPER + N and SUPER + SHIFT + N)
for i in range(1, 11):
    key = str(i % 10)
    ACTIONS[(64, key)] = f'hl.dsp.exec_cmd(home .. "/.config/hypr/scripts/workspace-nav.py goto {i}")'
    ACTIONS[(65, key)] = f"hl.dsp.window.move({{ workspace = {i} }})"

HOME = subprocess.run(
    ["sh", "-c", "printf %s \"$HOME\""], capture_output=True, text=True, check=True
).stdout

KEY_LABELS = {
    "RETURN": "Enter",
    "SPACE": "Space",
    "BACKSLASH": "\\",
    "slash": "?",
    "escape": "Escape",
    "right": "→",
    "left": "←",
    "up": "↑",
    "down": "↓",
    "mouse_down": "Scroll↓",
    "mouse_up": "Scroll↑",
    "mouse:272": "LMB",
    "mouse:273": "RMB",
    "PLUS": "=",
    "MINUS": "-",
    "XF86AudioRaiseVolume": "Volume up key",
    "XF86AudioLowerVolume": "Volume down key",
    "XF86AudioMute": "Mute key",
    "XF86AudioMicMute": "Mic mute key",
    "XF86MonBrightnessUp": "Brightness up key",
    "XF86MonBrightnessDown": "Brightness down key",
    "XF86AudioNext": "Next track key",
    "XF86AudioPause": "Play/Pause key",
    "XF86AudioPlay": "Play key",
    "XF86AudioPrev": "Previous track key",
}

MOD_NAMES = [(64, "SUPER"), (8, "ALT"), (4, "CTRL"), (1, "SHIFT")]


def mods_to_names(modmask):
    return " + ".join(name for bit, name in MOD_NAMES if modmask & bit)


def expand_dsl(dsl):
    return dsl.replace("home", f'"{HOME}"')


def format_combo(bind):
    mods = mods_to_names(bind["modmask"])
    key = KEY_LABELS.get(bind["key"], bind["key"])
    return " + ".join(part for part in (mods, key) if part)


def main():
    result = subprocess.run(
        ["hyprctl", "binds", "-j"], capture_output=True, check=True, text=True
    )
    binds = json.loads(result.stdout)

    rows = []  # (modmask, key, combo, display_line)
    for bind in binds:
        desc = bind.get("description", "")
        if not desc:
            continue
        combo = format_combo(bind)
        rows.append((bind["modmask"], bind["key"], combo, f"{combo}  →  {desc}"))
    rows = sorted(rows, key=lambda row: row[2].upper())

    selection = subprocess.run(
        ["wofi", "--dmenu", "--prompt", "Keybindings (Enter to run)"],
        input="\n".join(line for *_, line in rows) + "\n",
        text=True,
        capture_output=True,
    ).stdout.strip()
    if not selection:
        return

    for modmask, key, _, line in rows:
        if line == selection:
            dsl = ACTIONS.get((modmask, key))
            if dsl is None:
                subprocess.run(["notify-send", "Keybindings", "Not runnable from menu"])
            else:
                subprocess.run(
                    ["hyprctl", "dispatch", expand_dsl(dsl)], check=True
                )
            return


if __name__ == "__main__":
    main()