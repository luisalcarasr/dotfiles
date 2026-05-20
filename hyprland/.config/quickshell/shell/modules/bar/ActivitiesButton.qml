pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Hyprland

// "Activities" button on the left of the bar.
// Click → toggle launcher. Shows the current active app name when idle.
Item {
    id: root

    implicitWidth:  label.implicitWidth + 24
    implicitHeight: parent?.height ?? Appearance.barHeight

    // Hover state
    property bool hovered: mouseArea.containsMouse
    property bool pressed: mouseArea.pressed

    Rectangle {
        anchors.fill:    parent
        anchors.margins: 3
        radius:          Appearance.rounding.normal
        color: root.pressed
            ? Appearance.accentActive
            : root.hovered
                ? Appearance.accentHover
                : "transparent"

        Behavior on color {
            ColorAnimation { duration: Appearance.anim.fast }
        }
    }

    Text {
        id: label
        anchors.centerIn: parent
        text: "Activities"
        font {
            family:    Appearance.font.main
            pointSize: Appearance.font.size.normal
            weight:    Font.Medium
        }
        color: Appearance.fg
    }

    MouseArea {
        id: mouseArea
        anchors.fill:  parent
        hoverEnabled:  true
        cursorShape:   Qt.PointingHandCursor

        onClicked: {
            GlobalStates.launcherOpen = !GlobalStates.launcherOpen
        }
    }
}
