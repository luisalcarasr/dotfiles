from libqtile.widget.base import _TextBox 
from utils.audio import OuputAudio
from utils.theme import colors

ICON_DEFAULT = " "
ICON_MUTED = " "

class Volumen(_TextBox):

    output = OuputAudio()

    def __init__(self, **config):
        super().__init__(self.icon, **config)
        self.add_defaults(Volumen.defaults)
        self.update_foreground()
        self.output.on_init(self.mouse_leave)
        self.add_callbacks(
            {
                "Button1": self.toggle_mute,
                "Button4": self.volume_up,
                "Button5": self.volume_down,
            }
        )

    @property
    def icon(self):
        return ICON_MUTED if self.output.is_muted() else ICON_DEFAULT

    def draw_volume(self):
        self.font = _TextBox.font
        self.update_foreground()
        self.update(self.icon + " " + str(int(self.output.volume * 100)) + "%")

    def mouse_enter(self, *args, **kwargs):
        self.draw_volume()

    def mouse_leave(self, *args, **kwargs):
        self.update_foreground()
        self.update(self.icon)

    def volume_up(self):
        self.output.volume_up()
        self.draw_volume()

    def volume_down(self):
        self.output.volume_down()
        self.draw_volume()

    def toggle_mute(self):
        self.output.toggle_mute()
        self.update_foreground()
        self.draw_volume()

    def update_foreground(self):
        if self.output.is_muted():
            self.foreground = colors["red"]
        elif self.output.volume <= 0:
            self.foreground = colors["dark"]
        else:
            self.foreground = colors["white"]
