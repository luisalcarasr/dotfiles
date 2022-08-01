from libqtile.widget.base import _TextBox 
from pulsectl import Pulse
from lib.defaults import nerd_font
from utils.theme import colors

class Volumen(_TextBox):

    pulse = Pulse()

    def __init__(self, **config):
        super().__init__(self.icon, **config)
        self.add_defaults(Volumen.defaults)
        self.font = nerd_font
        self.update_foreground()
        self.add_callbacks(
            {
                "Button1": self.toggle_mute,
                "Button4": self.volume_up,
                "Button5": self.volume_down,
            }
        )

    @property
    def sink(self):
        return self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)

    @property
    def icon(self):
        return " " if self.sink.mute else " "

    def draw_volume(self):
        self.font = _TextBox.font
        self.fontsize = 10,
        self.update_foreground()
        self.update(self.icon + " " + str(int(round(self.sink.volume.value_flat * 100, 0))) + "%")

    def mouse_enter(self, *args, **kwargs):
        self.draw_volume()

    def mouse_leave(self, *args, **kwargs):
        self.font = self.nerd_font
        self.fontsize = 14
        self.update_foreground()
        self.update(self.icon)

    def volume_up(self):
        volume = self.sink.volume
        volume.value_flat = volume.value_flat + .05
        volume.value_flat = 1 if volume.value_flat > 1 else volume.value_flat;
        self.pulse.volume_set(self.sink, volume)
        self.draw_volume()

    def volume_down(self):
        volume = self.sink.volume
        volume.value_flat = volume.value_flat - .05
        volume.value_flat = 0 if volume.value_flat < 0 else volume.value_flat;
        self.pulse.volume_set(self.sink, volume)
        self.draw_volume()

    def toggle_mute(self):
        is_muted = self.sink.mute == 1
        self.update_foreground()
        self.pulse.mute(self.sink, mute=not is_muted)
        self.draw_volume()

    def update_foreground(self):
        if self.sink.mute:
            self.foreground = colors["red"]
        elif self.sink.volume.value_flat <= 0:
            self.foreground = colors["dark"]
        else:
            self.foreground = colors["white"]

