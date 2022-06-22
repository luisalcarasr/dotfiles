import os
from rofi import Rofi

def launch_project(qtile):
  rofi = Rofi()
  dir = os.path.expanduser('~/Projects/');
  projects = os.listdir(dir)
  index, _ = rofi.select("Projects ", projects)
  if index >= 0:
    qtile.cmd_spawn('kitty -e fish -c "nvm use $nvm_default_version; vi ' + dir + projects[index] + '"')
