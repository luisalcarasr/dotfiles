pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import Quickshell

// A single row in the launcher results list.
Item {
    id: root

    required property var appEntry
    required property bool focused

    signal activated()

    implicitHeight: 48

    property bool hovered: mouseArea.containsMouse

    // Highlight background
    Rectangle {
        anchors {
            fill:           parent
            leftMargin:     4
            rightMargin:    4
            topMargin:      1
            bottomMargin:   1
        }
        radius: Appearance.rounding.normal
        color: root.focused
            ? Appearance.accentSubtle
            : root.hovered
                ? Qt.rgba(
                    Appearance.surfaceHigh.r,
                    Appearance.surfaceHigh.g,
                    Appearance.surfaceHigh.b,
                    0.6)
                : "transparent"

        Behavior on color {
            ColorAnimation { duration: Appearance.anim.fast }
        }

        // Left accent strip when focused
        Rectangle {
            visible:   root.focused
            anchors {
                left:         parent.left
                top:          parent.top
                bottom:       parent.bottom
                topMargin:    6
                bottomMargin: 6
                leftMargin:   0
            }
            width:  3
            radius: Appearance.rounding.full
            color:  Appearance.accent
        }
    }

    RowLayout {
        anchors {
            fill:           parent
            leftMargin:     20
            rightMargin:    16
            topMargin:      6
            bottomMargin:   6
        }
        spacing: 12

        // App icon — Adwaita icon theme
        Image {
            id: icon
            Layout.alignment: Qt.AlignVCenter
            width:  28
            height: 28
            source: Quickshell.iconPath(root.appEntry?.icon ?? "", "application-x-executable")
            mipmap: true
            fillMode: Image.PreserveAspectFit
        }

        // App name
        Text {
            Layout.fillWidth:  true
            Layout.alignment:  Qt.AlignVCenter
            text:  root.appEntry?.name ?? ""
            font {
                family:    Appearance.font.main
                pointSize: Appearance.font.size.normal
            }
            color:  root.focused ? Appearance.accent : Appearance.fg
            elide:  Text.ElideRight

            Behavior on color {
                ColorAnimation { duration: Appearance.anim.fast }
            }
        }

        // "Flatpak" badge
        Rectangle {
            visible: root.appEntry?.isFlatpak ?? false
            Layout.alignment: Qt.AlignVCenter
            implicitWidth:  badgeLabel.implicitWidth + 10
            implicitHeight: badgeLabel.implicitHeight + 4
            radius: Appearance.rounding.small
            color:  Appearance.withAlpha(Appearance.accent, 0.15)

            Text {
                id: badgeLabel
                anchors.centerIn: parent
                text: "Flatpak"
                font {
                    family:    Appearance.font.main
                    pointSize: Appearance.font.size.tiny
                    weight:    Font.Medium
                }
                color: Appearance.accentMid
            }
        }

        // "Enter" hint when focused
        Text {
            visible: root.focused
            Layout.alignment: Qt.AlignVCenter
            text: "↵"
            font {
                family:    Appearance.font.main
                pointSize: Appearance.font.size.small
            }
            color: Appearance.fgMuted
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape:  Qt.PointingHandCursor
        onClicked:    root.activated()
    }
}
