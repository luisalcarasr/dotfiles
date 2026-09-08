#!/usr/bin/env python3
"""Toggle secondary monitors on/off for Hyprland.

Keeps only the primary monitor (DELL P2423D) active and disables every other
connected monitor. Re-enables them at their fixed geometry when toggled again.

Monitors are identified by their description (model/serial), which is stable,
because Hyprland can reassign output names (e.g. DP-1 <-> DP-4) after a
disable/enable cycle. Output names are resolved dynamically at runtime.

Hyprland >= 0.55 uses the Lua config parser, so monitor changes go through
`hyprctl eval 'hl.monitor({...})'`.
"""

import json
import os
import subprocess
import sys

PRIMARY_DESCRIPTION = "Dell Inc. DELL P2423D B0MQVP3"
STATE_FILE = os.path.join(
    os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "hypr-secondary-monitors.txt"
)

# Fixed geometry for every monitor, keyed by description prefix.
# Kept only when toggled on, so the layout never depends on DP-* names.
MONITOR_LAYOUT = [
    {
        "description": PRIMARY_DESCRIPTION,
        "mode": "2560x1440@60",
        "position": "0x0",
        "scale": 1,
        "vrr": 0,
    },
    {
        "description": "GGF MG700 0000000000000",
        "mode": "2560x1440@144",
        "position": "2560x0",
        "scale": 1,
        "vrr": 1,
    },
    {
        "description": "Dell Inc. DELL P2423DE B87GXR3",
        "mode": "2560x1440@60",
        "position": "5120x0",
        "scale": 1,
        "vrr": 0,
    },
]


def notify(message, urgent=False):
    """Send a desktop notification if a notifier is available."""
    for cmd in ("notify-send", "dunstify"):
        if _which(cmd):
            args = [cmd, "Monitors", message]
            if urgent:
                args += ["-u", "critical"]
            try:
                subprocess.run(args, check=False)
            except OSError:
                pass
            return


def _which(name):
    for path in os.environ.get("PATH", "").split(os.pathsep):
        candidate = os.path.join(path, name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def _match(desc, prefix):
    return desc and desc.startswith(prefix)


def _resolve_name(monitors, desc_prefix):
    """Return the current output name for the first matching description."""
    for m in monitors:
        if _match(m.get("description", ""), desc_prefix):
            return m["name"]
    return None


def hypr_monitors(include_disabled=False):
    """Return a list of monitor info dicts from Hyprland IPC.

    `hyprctl monitors -j` omits disabled monitors, so use `all` when needed.
    """
    args = ["hyprctl", "monitors"]
    if include_disabled:
        args.append("all")
    args.append("-j")
    try:
        out = subprocess.check_output(args)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return []
    try:
        return json.loads(out)
    except (ValueError, TypeError):
        return []


def apply_monitor(name_or_desc, fields):
    """Apply a monitor spec via the Lua config API (hyprctl eval)."""
    parts = ['output = "{}"'.format(name_or_desc)]
    for key, value in fields.items():
        if isinstance(value, bool):
            parts.append("{} = {}".format(key, str(value).lower()))
        elif isinstance(value, (int, float)):
            parts.append("{} = {}".format(key, value))
        else:
            parts.append('{} = "{}"'.format(key, value))
    spec = "hl.monitor({ " + ", ".join(parts) + " })"
    subprocess.run(["hyprctl", "eval", spec], check=False)


def main():
    if os.path.exists(STATE_FILE):
        # Currently in "primary only" mode -> re-enable every secondary
        # at its fixed geometry so the layout is always correct.
        # `hyprctl eval` cannot resolve `desc:` for disabled monitors, so
        # resolve real output names from IPC and apply geometry by identity.
        monitors = hypr_monitors(include_disabled=True)
        for entry in MONITOR_LAYOUT:
            if _match(entry["description"], PRIMARY_DESCRIPTION):
                continue
            name = _resolve_name(monitors, entry["description"])
            if not name:
                continue
            fields = {
                "mode": entry["mode"],
                "position": entry["position"],
                "scale": entry["scale"],
                "vrr": entry["vrr"],
                "disabled": False,
            }
            apply_monitor(name, fields)
        os.remove(STATE_FILE)
        notify("All monitors active")
        return 0

    # Otherwise: disable all secondary monitors except the primary.
    monitors = hypr_monitors()
    if not monitors:
        notify("Could not query monitors", urgent=True)
        return 1

    disabled_any = False
    for m in monitors:
        desc = m.get("description", "")
        if not desc:
            continue
        if _match(desc, PRIMARY_DESCRIPTION):
            continue
        disabled_any = True
        apply_monitor(m["name"], {"disabled": True})

    if disabled_any:
        open(STATE_FILE, "w", encoding="utf-8").close()
        notify("Only " + PRIMARY_DESCRIPTION + " active")
    else:
        notify("No secondary monitors detected")

    return 0


if __name__ == "__main__":
    sys.exit(main())