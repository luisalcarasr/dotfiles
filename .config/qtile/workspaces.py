from libqtile import layout
from libqtile.config import Group, Match
from utils.theme import colors

groups = [
    Group("0"),
    Group("1"),
    Group("2"),
]

layouts = [
    layout.MonadTall(
        border_focus=colors["sky"],
        border_normal=colors["dark"],
        border_width=1,
        margin=16,
    ),
    layout.Columns(
        border_focus=colors["sky"],
        border_normal=colors["dark"],
        border_width=1,
        margin=16,
        grow_amount=3,
        num_columns=1,
        margin_on_single=8,
        border_on_single=True,
    ),
    layout.Max(),
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
    border_focus=colors["sky"],
    border_normal=colors["dark"],
    border_width=1,
)
