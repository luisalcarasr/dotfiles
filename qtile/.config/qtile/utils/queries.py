from os import environ, path 

can_control_brightness = path.exists("/sys/class/backlight/intel_backlight/brightness")
has_batery = path.exists("/sys/class/power_supply/BAT0")

