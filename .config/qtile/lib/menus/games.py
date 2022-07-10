import os
import vdf
from rofi import Rofi

def launch_game(qtile):
  rofi = Rofi()
  file = os.path.expanduser('~/.steam/steam/steamapps/libraryfolders.vdf');
  libraries = vdf.load(open(file))["libraryfolders"];
  shared = ["228980", "1391110", "1493710"]
  names = []
  games = {}
  for key in libraries:
    apps = libraries[key]["apps"]
    path = libraries[key]["path"]
    for app in apps:
      if app in shared:
        continue
      file = os.path.expanduser( path + '/steamapps/appmanifest_' + app + '.acf');
      try:
        manifest = vdf.load(open(file));
      except:
        print(file)
      name = manifest["AppState"]["name"]
      names.append(name)
      games[name] = app;
  names.sort()
  index, _ = rofi.select("Games", names)
  app = games[names[index]]
  if index >= 0:
    qtile.cmd_spawn('steam steam://run/' + app )
