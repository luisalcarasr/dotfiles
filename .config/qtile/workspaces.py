from libqtile import layout
from libqtile.config import Group, Match
from utils.theme import colors

groups = [
    Group('   '),
    Group('   '),
    Group('   '),
    Group('   '),
    Group('   '),
    Group('   '),
    Group('   '),
]

layouts = [
    layout.MonadTall(
        border_focus=colors["sky"],
        border_normal=colors["dark"],
        margin=16,
        # single_margin=0,
        # single_border_width=0
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
    border_width=2,
)
