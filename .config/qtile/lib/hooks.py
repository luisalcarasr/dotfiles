from libqtile import qtile, hook

@hook.subscribe.startup
def _():
    if len(qtile.screens) > 1:
        qtile.groups_map["6"].cmd_toscreen(2, toggle=False)
        qtile.groups_map["7"].cmd_toscreen(1, toggle=False)
