pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import Quickshell

// Center clock — time + date, Cantarell, Light 1 on Dark 5.
Item {
    id: root

    implicitWidth:  row.implicitWidth + 16
    implicitHeight: parent?.height ?? Appearance.barHeight

    // Tick every second
    SystemClock {
        id: clock
        precision: SystemClock.Seconds
    }

    RowLayout {
        id: row
        anchors.centerIn: parent
        spacing: 6

        Text {
            id: timeText
            text: Qt.formatTime(clock.time, "HH:mm")
            font {
                family:    Appearance.font.main
                pointSize: Appearance.font.size.large
                weight:    Font.Medium
            }
            color: Appearance.fg
        }

        Text {
            text: "·"
            font {
                family:    Appearance.font.main
                pointSize: Appearance.font.size.small
            }
            color: Appearance.fgMuted
        }

        Text {
            id: dateText
            text: Qt.formatDate(clock.time, "ddd, MMM d")
            font {
                family:    Appearance.font.main
                pointSize: Appearance.font.size.small
            }
            color: Appearance.fgMuted
        }
    }
}
