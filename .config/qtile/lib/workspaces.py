from libqtile import layout
from libqtile.config import Group, Match
from utils.theme import colors
from lib.layouts.vertical import VerticalTile

workspaces = list(map(lambda n: str(n + 1) if n + 1 != 10 else str(0), range(10)))

vertical_screen_layouts = [
    layout.Columns(
        border_focus=colors["blue"],
        border_normal=colors["dark"],
        border_width=1,
        margin=16,
        grow_amount=3,
        num_columns=1,
        border_on_single=1,
        margin_on_single=16,
    ),
]

groups = map(lambda ws: Group(ws, label=""), workspaces)

layouts = [
    layout.MonadTall(
        border_focus=colors["blue"],
        border_normal=colors["dark"],
        border_width=1,
        margin=16,
        single_border_width=1,
        single_margin=16,
    ),
    VerticalTile(
        border_focus=colors["blue"],
        border_normal=colors["dark"],
        border_width=1,
        margin=16,
        single_border_width=1,
        single_margin=16,
    ),
]

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry
        Match(wm_class="steam_app_1182480", title="Origin"), # Origin
        Match(wm_class="steam_app_*"), # Steam Apps
    ],
    border_focus=colors["blue"],
    border_normal=colors["dark"],
    border_width=1,
)
