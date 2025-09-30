import os
import vdf
from rofi import Rofi


def launch_game(qtile):
    rofi = Rofi()
    file = os.path.expanduser("~/.steam/steam/steamapps/libraryfolders.vdf")
    try:
        with open(file, encoding="utf-8") as f:
            libraries = vdf.load(f)["libraryfolders"]
    except (FileNotFoundError, OSError, KeyError, UnicodeDecodeError) as e:
        print(f"Error leyendo {file}: {e}")
        return

    shared = {"228980", "1391110", "1493710", "1826330"}
    names = []
    games = {}
    for key in libraries:
        apps = libraries[key].get("apps", {})
        path = libraries[key].get("path")
        if not path:
            continue
        for app in apps:
            if app in shared:
                continue
            manifest_path = os.path.expanduser(
                os.path.join(path, "steamapps", f"appmanifest_{app}.acf")
            )
            try:
                with open(manifest_path, encoding="utf-8") as mf:
                    manifest = vdf.load(mf)
                name = manifest["AppState"]["name"]
            except (FileNotFoundError, OSError, KeyError, UnicodeDecodeError):
                # Saltar entradas problemáticas
                continue
            names.append(name)
            games[name] = app
    names.sort()
    index, _ = rofi.select("Games", names)
    if index >= 0:
        app = games[names[index]]
        qtile.cmd_spawn(f"steam steam://run/{app}")
