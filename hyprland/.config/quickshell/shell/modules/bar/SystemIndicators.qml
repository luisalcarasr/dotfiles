pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Services.UPower

// Right-side system indicators: battery, network icon, volume icon.
// Plain icon indicators — no popup panel (per design: only bar + launcher).
RowLayout {
    id: root
    spacing: 4
    layoutDirection: Qt.RightToLeft

    // ── Battery ──────────────────────────────────────────────────────────────
    Loader {
        active: UPower.displayDevice?.isPresent ?? false
        sourceComponent: RowLayout {
            spacing: 3
            layoutDirection: Qt.RightToLeft

            Text {
                text: {
                    const pct = Math.round((UPower.displayDevice?.percentage ?? 0) * 100)
                    return `${pct}%`
                }
                font {
                    family:    Appearance.font.main
                    pointSize: Appearance.font.size.small
                }
                color: {
                    const pct = (UPower.displayDevice?.percentage ?? 1)
                    if (pct < 0.10) return Appearance.error
                    if (pct < 0.25) return Appearance.warning
                    return Appearance.fgMuted
                }
            }

            Text {
                text: {
                    const pct = UPower.displayDevice?.percentage ?? 1
                    const charging = UPower.displayDevice?.state === 1 // Charging
                    if (charging) return "󰂄" // nerd font: battery charging
                    if (pct < 0.10) return "󰁺"
                    if (pct < 0.25) return "󰁼"
                    if (pct < 0.50) return "󰁾"
                    if (pct < 0.75) return "󰂀"
                    return "󰁹"
                }
                font {
                    family:    "JetBrainsMono Nerd Font"
                    pointSize: Appearance.font.size.large
                }
                color: {
                    const pct = (UPower.displayDevice?.percentage ?? 1)
                    if (pct < 0.10) return Appearance.error
                    if (pct < 0.25) return Appearance.warning
                    return Appearance.fgMuted
                }
            }
        }
    }

    // ── Separator ─────────────────────────────────────────────────────────────
    Rectangle {
        width:  1
        height: 14
        color:  Appearance.border
    }

    // ── Clock — already in center, nothing here ───────────────────────────────
    // ── Network indicator (icon only) ────────────────────────────────────────
    Text {
        id: networkIcon
        // We use a nerd font glyph: wired=󰈀  wifi=󰤨  disconnected=󰤭
        // Quickshell does not yet expose NetworkManager directly; use a
        // Process to check connectivity once on startup and refresh every 30s.
        property string status: "unknown"
        text: {
            switch (networkIcon.status) {
                case "wifi":        return "󰤨"
                case "ethernet":    return "󰈀"
                case "limited":     return "󰤫"
                case "none":        return "󰤭"
                default:            return "󰤭"
            }
        }
        font {
            family:    "JetBrainsMono Nerd Font"
            pointSize: Appearance.font.size.large
        }
        color: networkIcon.status === "none" ? Appearance.fgDisabled : Appearance.fgMuted

        Process {
            id: netProc
            command: ["sh", "-c",
                "nmcli -t -f TYPE,STATE dev 2>/dev/null | grep -qE 'ethernet:connected' && echo ethernet || " +
                "nmcli -t -f TYPE,STATE dev 2>/dev/null | grep -qE 'wifi:connected' && echo wifi || " +
                "nmcli networking connectivity 2>/dev/null | grep -q limited && echo limited || echo none"]
            running: false
            stdout: StdioCollector {
                onStreamFinished: {
                    const result = text.trim()
                    networkIcon.status = result
                }
            }
        }

        Timer {
            interval: 30000
            repeat:   true
            running:  true
            triggeredOnStart: true
            onTriggered: netProc.running = true
        }
    }

    // ── Volume indicator (icon only) ─────────────────────────────────────────
    Text {
        id: volIcon
        property int volume: 100
        property bool muted: false

        text: {
            if (muted || volume === 0) return "󰝟"
            if (volume < 33)           return "󰕿"
            if (volume < 66)           return "󰖀"
            return "󰕾"
        }
        font {
            family:    "JetBrainsMono Nerd Font"
            pointSize: Appearance.font.size.large
        }
        color: muted ? Appearance.fgDisabled : Appearance.fgMuted

        Process {
            id: volProc
            command: ["sh", "-c",
                "wpctl get-volume @DEFAULT_AUDIO_SINK@ 2>/dev/null | awk '{print $2, ($3==\"[MUTED]\"?\"1\":\"0\")}'"]
            running: false
            stdout: StdioCollector {
                onStreamFinished: {
                    const parts = text.trim().split(" ")
                    if (parts.length >= 1) {
                        volIcon.volume = Math.round(parseFloat(parts[0]) * 100)
                    }
                    volIcon.muted = (parts[1] === "1")
                }
            }
        }

        Timer {
            interval: 5000
            repeat:   true
            running:  true
            triggeredOnStart: true
            onTriggered: volProc.running = true
        }
    }
}
