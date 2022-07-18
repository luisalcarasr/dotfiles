from rofi import Rofi
import pulsectl

SINK_ALIASES = {
  'TU116 High Definition Audio Controller Digital Stereo (HDMI)': "蓼 Right Monitor",
  'TU116 High Definition Audio Controller Digital Stereo (HDMI 2)': "蓼 Speakers",
  'TU116 High Definition Audio Controller Digital Stereo (HDMI 3)': "蓼 Left Monitor",
  'Built-in Audio Analog Stereo': "   Headphones",
}

def select_audio_output(qtile):
  pulse = pulsectl.Pulse()
  rofi = Rofi()

  sinks = pulse.sink_list()
  current_default_name = pulse.server_info().default_sink_name
  for i, s in enumerate(sinks):
    if s.name == current_default_name:
      current_default = i

  if current_default == None:
    print("Couldn't find the default sink?")
    return

  sink_index, _ = rofi.select("奔", [s.description if s.description not in SINK_ALIASES else SINK_ALIASES[s.description] for s in sinks], select=current_default)
  if sink_index == -1:
    return

  pulse.default_set(sinks[sink_index])
