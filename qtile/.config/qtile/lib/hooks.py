from libqtile import qtile, hook
from lib.workspaces import workspaces as ws

@hook.subscribe.startup
def _():
    if len(qtile.screens) > 1:
        size = len(qtile.groups_map)
        qtile.groups_map[ws[-1]].cmd_toscreen(2, toggle=False)
        qtile.groups_map[ws[-2]].cmd_toscreen(1, toggle=False)

@hook.subscribe.startup
@hook.subscribe.setgroup
def _():
    if len(qtile.screens) > 1:
        qtile.screens[0].group.use_layout(0)
        qtile.screens[1].group.use_layout(1)
        qtile.screens[2].group.use_layout(1)
