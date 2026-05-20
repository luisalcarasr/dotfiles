pragma Singleton
pragma ComponentBehavior: Bound

import QtQuick
import Quickshell
import Quickshell.Io

// Persistent configuration backed by ~/.config/quickshell/shell/config.json
Singleton {
    id: root

    // Accent colors from GNOME HIG palette (shade 5 only, excluding Light/Dark)
    readonly property var accentOptions: ({
        "blue":   "#1a5fb4",
        "green":  "#26a269",
        "yellow": "#e5a50a",
        "orange": "#c64600",
        "red":    "#a51d2d",
        "purple": "#613583",
        "brown":  "#63452c"
    })

    // The currently active accent key — written to disk on change
    property string accentKey: "blue"

    // Derived accent color hex from the map
    readonly property string accentColor: accentOptions[accentKey] ?? accentOptions["blue"]

    // Bar settings
    property int barHeight: 32

    // Config file path
    readonly property string configPath: StandardPaths.writableLocation(StandardPaths.AppConfigLocation) + "/shell/config.json"

    // --- Persistence ---
    property bool _loaded: false

    FileView {
        id: configFile
        path: Qt.resolvedUrl(root.configPath)
        watchChanges: false
        onLoadedChanged: {
            if (!root._loaded) {
                root._load(configFile.text())
                root._loaded = true
            }
        }
    }

    function _load(text) {
        try {
            const data = JSON.parse(text)
            if (data.accentKey && root.accentOptions[data.accentKey] !== undefined) {
                root.accentKey = data.accentKey
            }
        } catch (e) {
            // First run — defaults apply
        }
    }

    function save() {
        const data = JSON.stringify({ accentKey: root.accentKey }, null, 2)
        configFile.setText(data)
    }

    // Auto-save on accent change after first load
    onAccentKeyChanged: {
        if (_loaded) save()
    }

    Component.onCompleted: {
        configFile.reload()
    }
}
