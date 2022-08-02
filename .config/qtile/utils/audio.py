import asyncio
from pulsectl import Pulse
from pulsectl_asyncio import PulseAsync

class OuputAudio:

    pulse = Pulse()

    max_volume = 1

    def __init__(self):
        pass

    def on_init(self, callback):
        async def connect():
            pulse = PulseAsync()
            await pulse.connect()
            pulse.close()
            callback()
        task = asyncio.create_task(connect())
        task.add_done_callback(callback)

    def volume_up(self, step = 0.05):
        self.volume += abs(step)

    def volume_down(self, step = 0.05):
        self.volume -= abs(step)

    def toggle_mute(self):
        is_muted = self.sink.mute == 1
        self.pulse.mute(self.sink, mute=not is_muted)

    def is_muted(self):
        try:
            return True if self.sink.mute else False
        except:
            return True

    @property
    def volume(self):
        try:
            return round(self.sink.volume.value_flat, 3)
        except:
            return 0

    @volume.setter
    def volume(self, volume):
        if volume > self.max_volume:
            volume = self.max_volume
        elif volume < 0:
            volume = 0

        sink_volume = self.sink.volume
        sink_volume.value_flat = volume
        self.pulse.volume_set(self.sink, sink_volume)
    
    @property
    def sink(self):
        return self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)

