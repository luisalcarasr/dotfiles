#!/usr/bin/env python3
"""Navigate between workspaces that currently contain windows.

Cycles through existing workspaces by id (cyclic). When the target workspace
lives on another monitor, it is swapped onto the current monitor via
`hl.dsp.workspace.swap_monitors`, so the active workspace follows arrow keys
across screens. Workspaces without windows are skipped.
"""

import json
import subprocess
import sys


def hypr(*args):
    try:
        return subprocess.check_output(
            ["hyprctl", *args], text=True
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return ""


def eval_lua(code):
    """Execute a Lua snippet via `hyprctl eval` (Hyprland >= 0.55)."""
    try:
        subprocess.run(["hyprctl", "eval", code], check=False)
    except FileNotFoundError:
        pass


def load_workspaces():
    try:
        data = json.loads(hypr("workspaces", "-j") or "[]")
    except (ValueError, TypeError):
        return []
    return [w for w in data if w.get("id", 0) > 0]


def active_workspace():
    try:
        return json.loads(hypr("activeworkspace", "-j") or "{}")
    except (ValueError, TypeError):
        return {}


def focus_workspace(ws_id):
    eval_lua('hl.dispatch(hl.dsp.focus({ workspace = %d }))' % ws_id)


def swap_workspaces(cur_mon, target_mon, target_id):
    """Bring the target workspace to the current monitor, swapping the
    current one to the target monitor, then focus it."""
    eval_lua(
        'hl.dispatch(hl.dsp.workspace.swap_monitors({ monitor1 = "%s", monitor2 = "%s" }))'
        % (target_mon, cur_mon)
    )
    focus_workspace(target_id)


def main():
    if len(sys.argv) < 2:
        print("usage: workspace-nav.py next|prev|goto <workspace>", file=sys.stderr)
        return 1

    action = sys.argv[1]
    if action not in ("next", "prev", "goto"):
        print("usage: workspace-nav.py next|prev|goto <workspace>", file=sys.stderr)
        return 1

    all_ws = load_workspaces()
    cur = active_workspace()
    cur_id = cur.get("id", -1)
    cur_mon = cur.get("monitor", "")

    if action == "goto":
        try:
            target_id = int(sys.argv[2])
        except (IndexError, ValueError):
            print("usage: workspace-nav.py next|prev|goto <workspace>", file=sys.stderr)
            return 1
        # consider any existing workspace (windowed or not); focus creates it
        target = next((w for w in all_ws if w["id"] == target_id), None)
        if target is None or target["monitor"] == cur_mon:
            focus_workspace(target_id)
        else:
            swap_workspaces(cur_mon, target["monitor"], target_id)
        return 0

    # only workspaces that currently contain windows
    ws = sorted(
        [w for w in all_ws if w.get("windows", 0) > 0],
        key=lambda w: w["id"],
    )
    if not ws:
        return 0

    # find current workspace in the filtered list
    idx = next(
        (i for i, w in enumerate(ws) if w["id"] == cur_id),
        None,
    )

    if idx is None:
        # current workspace has no windows (e.g. just emptied it);
        # jump to the nearest workspace in the requested direction
        if action == "next":
            target = ws[0]
        else:
            target = ws[-1]
    else:
        step = 1 if action == "next" else -1
        target = ws[(idx + step) % len(ws)]

    if target["monitor"] == cur_mon:
        focus_workspace(target["id"])
    else:
        swap_workspaces(cur_mon, target["monitor"], target["id"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
