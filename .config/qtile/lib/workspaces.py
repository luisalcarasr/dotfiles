from libqtile import layout
from libqtile.config import Group, Match
from utils.theme import colors

workspaces = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
];

vertical_screen_layouts = [
    layout.Columns(
        border_focus=colors["blue"],
        border_normal=colors["dark"],
        border_width=1,
        margin=16,
        grow_amount=3,
        num_columns=1,
        margin_on_single=16,
        border_on_single=1,
    ),
]

groups = [
    Group("1", label=""),
    Group("2", label=""),
    Group("3", label=""),
    Group("4", label=""),
    Group("5", label=""),
    Group("6", label="", layouts=vertical_screen_layouts),
    Group("7", label="", layouts=vertical_screen_layouts),
];
# groups = map(lambda ws: Group(ws), workspaces)

layouts = [
    layout.MonadTall(
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
