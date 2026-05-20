pragma ComponentBehavior: Bound

import QtQuick
import Quickshell
import Quickshell.Wayland
import Quickshell.Hyprland

// Top bar — one instance per connected monitor.
Scope {
    Variants {
        model: Quickshell.screens

        delegate: PanelWindow {
            id: root
            required property ShellScreen modelData
            screen: modelData

            // WlrLayershell config
            WlrLayershell.namespace: "quickshell:bar"
            WlrLayershell.layer: WlrLayer.Top
            WlrLayershell.keyboardFocus: WlrKeyboardFocus.None

            // Anchor to top, full width
            anchors {
                top:   true
                left:  true
                right: true
            }

            // Reserve space so windows don't go under the bar
            exclusiveZone: Appearance.barHeight
            implicitHeight: Appearance.barHeight
            color: "transparent"

            BarContent {
                anchors.fill: parent
            }
        }
    }

    // IPC: toggle launcher from external scripts / hyprland binds
    IpcHandler {
        target: "launcher"
        function toggle(): void {
            GlobalStates.launcherOpen = !GlobalStates.launcherOpen
        }
    }
}
