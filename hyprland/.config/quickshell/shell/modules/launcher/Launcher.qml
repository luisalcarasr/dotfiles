pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Wayland
import Quickshell.Hyprland

// Spotlight-style launcher.
// Shows kitty (terminal) + installed Flatpak apps.
// Toggle with Super+Space or clicking "Activities".
Scope {
    id: launcherScope

    PanelWindow {
        id: panel

        visible: GlobalStates.launcherOpen

        WlrLayershell.namespace: "quickshell:launcher"
        WlrLayershell.layer: WlrLayer.Overlay
        WlrLayershell.keyboardFocus: GlobalStates.launcherOpen
            ? WlrKeyboardFocus.Exclusive
            : WlrKeyboardFocus.None

        // Full-screen transparent overlay
        anchors { top: true; bottom: true; left: true; right: true }
        color: "transparent"

        // Dismiss on click outside the card
        MouseArea {
            anchors.fill: parent
            onClicked: GlobalStates.launcherOpen = false
        }

        // ── Scrim ───────────────────────────────────────────────────────────
        Rectangle {
            anchors.fill: parent
            color: Appearance.scrim

            Behavior on opacity {
                NumberAnimation { duration: Appearance.anim.normal }
            }
        }

        // ── Launcher card ────────────────────────────────────────────────────
        Rectangle {
            id: card

            // Position: horizontally centered, sits just below the bar
            anchors {
                horizontalCenter: parent.horizontalCenter
                top:              parent.top
                topMargin:        Appearance.barHeight + 8
            }

            width:  560
            // Height grows with results, capped at 480px
            height: Math.min(
                searchField.height + resultsColumn.implicitHeight + 32,
                480
            )

            color:  Appearance.surface
            radius: Appearance.rounding.large

            // 1px accent border
            border.color: Appearance.accentMid
            border.width: 1

            // Subtle drop shadow via layer effect
            layer.enabled: true
            layer.effect: null  // shadow handled by Rectangle below

            // Stop clicks from propagating to the scrim dismissal
            MouseArea {
                anchors.fill: parent
                onClicked: {} // absorb
            }

            // ── Search field ─────────────────────────────────────────────────
            Rectangle {
                id: searchFieldBg
                anchors {
                    top:   parent.top
                    left:  parent.left
                    right: parent.right
                    margins: 12
                }
                height: 44
                color:  Appearance.surfaceHigh
                radius: Appearance.rounding.normal

                // Search icon
                Text {
                    id: searchIcon
                    anchors {
                        left:           parent.left
                        leftMargin:     12
                        verticalCenter: parent.verticalCenter
                    }
                    text:  "󰍉"
                    font {
                        family:    "JetBrainsMono Nerd Font"
                        pointSize: Appearance.font.size.large
                    }
                    color: Appearance.fgMuted
                }

                TextInput {
                    id: searchField
                    anchors {
                        left:           searchIcon.right
                        leftMargin:     8
                        right:          clearButton.left
                        rightMargin:    8
                        verticalCenter: parent.verticalCenter
                    }
                    font {
                        family:    Appearance.font.main
                        pointSize: Appearance.font.size.normal
                    }
                    color:            Appearance.fg
                    selectionColor:   Appearance.accentSubtle
                    selectedTextColor: Appearance.fg
                    clip:             true

                    // Placeholder
                    Text {
                        visible:  searchField.text === ""
                        text:     "Search apps…"
                        font:     searchField.font
                        color:    Appearance.fgDisabled
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    onTextChanged: launcherScope.filter(text)

                    Keys.onEscapePressed: GlobalStates.launcherOpen = false
                    Keys.onReturnPressed: launcherScope.activateFirst()
                    Keys.onEnterPressed:  launcherScope.activateFirst()
                    Keys.onDownPressed:   launcherScope.moveFocus(1)
                    Keys.onUpPressed:     launcherScope.moveFocus(-1)
                    Keys.onTabPressed:    launcherScope.moveFocus(1)
                }

                // Clear button
                Text {
                    id: clearButton
                    anchors {
                        right:          parent.right
                        rightMargin:    12
                        verticalCenter: parent.verticalCenter
                    }
                    visible: searchField.text !== ""
                    text:   "󰅖"
                    font {
                        family:    "JetBrainsMono Nerd Font"
                        pointSize: Appearance.font.size.normal
                    }
                    color: Appearance.fgMuted

                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: searchField.text = ""
                    }
                }
            }

            // ── Results list ──────────────────────────────────────────────────
            Flickable {
                id: resultsFlickable
                anchors {
                    top:     searchFieldBg.bottom
                    topMargin: 8
                    left:    parent.left
                    right:   parent.right
                    bottom:  parent.bottom
                    bottomMargin: 8
                }
                clip: true
                contentHeight: resultsColumn.implicitHeight

                Column {
                    id: resultsColumn
                    width: resultsFlickable.width
                    padding: 4
                    spacing: 2

                    Repeater {
                        model: launcherScope.filteredApps
                        delegate: LauncherItem {
                            required property var modelData
                            required property int index

                            width:    resultsColumn.width - resultsColumn.padding * 2
                            appEntry: modelData
                            focused:  launcherScope.focusedIndex === index

                            onActivated: launcherScope.launch(modelData)
                        }
                    }
                }
            }
        }

        // Focus the search field when the launcher opens
        onVisibleChanged: {
            if (visible) {
                searchField.text = ""
                searchField.forceActiveFocus()
                launcherScope.filter("")
                launcherScope.focusedIndex = 0
            }
        }
    }

    // ── App data & filtering ────────────────────────────────────────────────

    // All available entries (kitty + flatpak apps populated by Process)
    property var allApps:      []
    property var filteredApps: []
    property int focusedIndex: 0

    // Populate the app list on startup and when launcher opens
    Process {
        id: flatpakList
        // List installed flatpak apps: output "AppId\tName\tIcon"
        command: ["sh", "-c",
            "flatpak list --app --columns=application,name 2>/dev/null | awk -F'\\t' '{print $1\"\\t\"$2}'"]
        running: false
        stdout: StdioCollector {
            onStreamFinished: {
                const lines = text.trim().split("\n").filter(l => l.length > 0)
                let apps = [
                    // Always include kitty as first entry
                    { name: "Terminal", exec: "kitty", icon: "utilities-terminal", isFlatpak: false }
                ]
                for (const line of lines) {
                    const parts = line.split("\t")
                    if (parts.length < 2) continue
                    const appId = parts[0].trim()
                    const name  = parts[1].trim()
                    if (!name || !appId) continue
                    apps.push({
                        name:      name,
                        exec:      `flatpak run ${appId}`,
                        icon:      appId.toLowerCase(),
                        isFlatpak: true,
                        appId:     appId
                    })
                }
                launcherScope.allApps = apps
                launcherScope.filter(searchField.text)
            }
        }
    }

    // Refresh app list each time the launcher opens
    Connections {
        target: GlobalStates
        function onLauncherOpenChanged() {
            if (GlobalStates.launcherOpen) {
                flatpakList.running = true
            }
        }
    }

    // Filter helper — simple case-insensitive substring match
    function filter(query) {
        const q = query.trim().toLowerCase()
        if (q === "") {
            filteredApps = allApps
        } else {
            filteredApps = allApps.filter(app =>
                app.name.toLowerCase().includes(q)
            )
        }
        focusedIndex = 0
    }

    function moveFocus(delta) {
        const next = focusedIndex + delta
        focusedIndex = Math.max(0, Math.min(filteredApps.length - 1, next))
    }

    function activateFirst() {
        if (filteredApps.length > 0) {
            launch(filteredApps[focusedIndex] ?? filteredApps[0])
        }
    }

    function launch(app) {
        GlobalStates.launcherOpen = false
        Quickshell.execDetached(["sh", "-c", app.exec])
    }

    // ── Global shortcut ─────────────────────────────────────────────────────
    GlobalShortcut {
        name: "launcherToggle"
        description: "Toggle the app launcher"
        onPressed: GlobalStates.launcherOpen = !GlobalStates.launcherOpen
    }
}
