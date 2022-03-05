from libqtile.lazy import lazy

@lazy.function
def poweroff(qtile):
    qtile.cmd_spawn('poweroff')

