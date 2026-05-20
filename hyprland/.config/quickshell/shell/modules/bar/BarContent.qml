pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Hyprland
import Quickshell.Services.UPower

// The visual content of the top bar.
// Layout mirrors GNOME Shell:
//   [Activities | Workspaces]   [Clock]   [SystemTray | Status]
Item {
    id: root

    // Bar background — solid Dark 5 with a 1px bottom border in Dark 2
    Rectangle {
        anchors.fill: parent
        color: Appearance.bg

        // Subtle separator at the bottom edge
        Rectangle {
            anchors {
                bottom: parent.bottom
                left:   parent.left
                right:  parent.right
            }
            height: 1
            color:  Appearance.border
        }
    }

    // ── Left section ─────────────────────────────────────────────────────────
    RowLayout {
        id: leftSection
        anchors {
            left:           parent.left
            top:            parent.top
            bottom:         parent.bottom
            leftMargin:     8
        }
        spacing: 2

        // Activities button — opens the launcher
        ActivitiesButton {}
    }

    // ── Center section — clock ────────────────────────────────────────────────
    BarClock {
        anchors.centerIn: parent
    }

    // ── Right section — system tray + indicators ──────────────────────────────
    RowLayout {
        id: rightSection
        anchors {
            right:        parent.right
            top:          parent.top
            bottom:       parent.bottom
            rightMargin:  8
        }
        spacing: 6
        layoutDirection: Qt.RightToLeft

        SystemIndicators {}
    }
}
