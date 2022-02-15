from libqtile import layout
from libqtile.config import Group, Match
from utils.theme import colors

workspaces = [
    "Home",
    "Browser",
    "Virtual",
    "Logs",
    "Social",
];

groups = map(lambda ws: Group(ws), workspaces)

layouts = [
    layout.MonadTall(
        border_focus=colors["sky"],
        border_normal=colors["dark"],
        border_width=1,
        margin=0,
        single_border_width=0,
    ),
    layout.Columns(
        border_focus=colors["sky"],
        border_normal=colors["dark"],
        border_width=1,
        margin=0,
        grow_amount=3,
        num_columns=1,
        margin_on_single=0,
        border_on_single=False,
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
