from rofi import Rofi
import pulsectl

SOURCE_ALIASES = {
  'GameFactor MCG601 Mono': "   Microphone",
  'HD Pro Webcam C920 Analog Stereo': "犯 Webcam",
}

IGNORE = [
    'Monitor of Built-in Audio Analog Stereo',
    'Monitor of TU116 High Definition Audio Controller Digital Stereo (HDMI)',
    'Monitor of TU116 High Definition Audio Controller Digital Stereo (HDMI 2)',
    'Monitor of TU116 High Definition Audio Controller Digital Stereo (HDMI 3)',
    'Monitor of Audio Adapter (Unitek Y-247A) Analog Stereo',
]

def select_audio_input(qtile):
  pulse = pulsectl.Pulse()
  rofi = Rofi()

  def check(source):
    if not source.description in IGNORE:
      return True
    return False

  sources = list(filter(lambda s: not s.description in IGNORE, pulse.source_list()))
  current_default_name = pulse.server_info().default_source_name
  current_default = None
  for i, s in enumerate(sources):
    if s.name == current_default_name:
      current_default = i

  if current_default == None:
    print("Couldn't find the default source?")
    return

  source_index, _ = rofi.select("", [s.description if s.description not in SOURCE_ALIASES else SOURCE_ALIASES[s.description] for s in sources], select=current_default)
  if source_index == -1:
    return

  pulse.default_set(sources[source_index])
