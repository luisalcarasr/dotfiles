pragma Singleton
pragma ComponentBehavior: Bound

import QtQuick
import Quickshell

// GNOME HIG color system.
// Background: Dark 5 (#000000), surfaces step up through the Dark scale.
// Foreground: Light 1 (#ffffff).
// Accent: configurable, one of the GNOME HIG shade-5 colors (default Blue 5).
Singleton {
    id: root

    // ── GNOME HIG full palette ──────────────────────────────────────────────

    readonly property QtObject gnome: QtObject {
        // Blue
        readonly property color blue1: "#99c1f1"
        readonly property color blue2: "#62a0ea"
        readonly property color blue3: "#3584e4"
        readonly property color blue4: "#1c71d8"
        readonly property color blue5: "#1a5fb4"
        // Green
        readonly property color green1: "#8ff0a4"
        readonly property color green2: "#57e389"
        readonly property color green3: "#33d17a"
        readonly property color green4: "#2ec27e"
        readonly property color green5: "#26a269"
        // Yellow
        readonly property color yellow1: "#f9f06b"
        readonly property color yellow2: "#f8e45c"
        readonly property color yellow3: "#f6d32d"
        readonly property color yellow4: "#f5c211"
        readonly property color yellow5: "#e5a50a"
        // Orange
        readonly property color orange1: "#ffbe6f"
        readonly property color orange2: "#ffa348"
        readonly property color orange3: "#ff7800"
        readonly property color orange4: "#e66100"
        readonly property color orange5: "#c64600"
        // Red
        readonly property color red1: "#f66151"
        readonly property color red2: "#ed333b"
        readonly property color red3: "#e01b24"
        readonly property color red4: "#c01c28"
        readonly property color red5: "#a51d2d"
        // Purple
        readonly property color purple1: "#dc8add"
        readonly property color purple2: "#c061cb"
        readonly property color purple3: "#9141ac"
        readonly property color purple4: "#813d9c"
        readonly property color purple5: "#613583"
        // Brown
        readonly property color brown1: "#cdab8f"
        readonly property color brown2: "#b5835a"
        readonly property color brown3: "#986a44"
        readonly property color brown4: "#865e3c"
        readonly property color brown5: "#63452c"
        // Light (neutral highlights)
        readonly property color light1: "#ffffff"
        readonly property color light2: "#f6f5f4"
        readonly property color light3: "#deddda"
        readonly property color light4: "#c0bfbc"
        readonly property color light5: "#9a9996"
        // Dark (neutral surfaces)
        readonly property color dark1: "#77767b"
        readonly property color dark2: "#5e5c64"
        readonly property color dark3: "#3d3846"
        readonly property color dark4: "#241f31"
        readonly property color dark5: "#000000"
    }

    // ── Semantic tokens ─────────────────────────────────────────────────────

    // Accent — driven by Config.accentColor
    readonly property color accent:          Config.accentColor
    // Shade-1 equivalent per accent family (for hover/active states)
    readonly property color accentLight: {
        switch (Config.accentKey) {
            case "blue":   return gnome.blue1
            case "green":  return gnome.green1
            case "yellow": return gnome.yellow1
            case "orange": return gnome.orange1
            case "red":    return gnome.red1
            case "purple": return gnome.purple1
            case "brown":  return gnome.brown1
            default:       return gnome.blue1
        }
    }
    // Shade-3 for mid-tone uses (borders, selection highlights)
    readonly property color accentMid: {
        switch (Config.accentKey) {
            case "blue":   return gnome.blue3
            case "green":  return gnome.green3
            case "yellow": return gnome.yellow3
            case "orange": return gnome.orange3
            case "red":    return gnome.red3
            case "purple": return gnome.purple3
            case "brown":  return gnome.brown3
            default:       return gnome.blue3
        }
    }

    // Base surfaces — Dark scale stepping up for elevation
    readonly property color bg:            gnome.dark5   // #000000  bar background
    readonly property color surface:       gnome.dark4   // #241f31  panel / popup base
    readonly property color surfaceHigh:   gnome.dark3   // #3d3846  elevated card
    readonly property color surfaceHigher: gnome.dark2   // #5e5c64  highest elevation
    readonly property color border:        gnome.dark1   // #77767b  subtle borders

    // Foreground
    readonly property color fg:            gnome.light1  // #ffffff  primary text
    readonly property color fgMuted:       gnome.light4  // #c0bfbc  secondary / hint text
    readonly property color fgDisabled:    gnome.light5  // #9a9996  disabled text

    // Semantic utility colors
    readonly property color success:       gnome.green4
    readonly property color warning:       gnome.yellow4
    readonly property color error:         gnome.red3
    readonly property color errorMuted:    gnome.red5

    // Interactive state helpers
    // Mix two colors — pure QML: interpolate each channel
    function mix(a, b, t) {
        // t=1 → full a, t=0 → full b
        return Qt.rgba(
            a.r * t + b.r * (1 - t),
            a.g * t + b.g * (1 - t),
            a.b * t + b.b * (1 - t),
            a.a * t + b.a * (1 - t)
        )
    }

    function withAlpha(c, alpha) {
        return Qt.rgba(c.r, c.g, c.b, alpha)
    }

    // Hover: accent mixed with surface at 80%
    readonly property color accentHover:  mix(accent, surfaceHigh, 0.75)
    // Active / pressed
    readonly property color accentActive: mix(accent, surfaceHigh, 0.55)
    // Subtle tint on surfaces (for selected items)
    readonly property color accentSubtle: withAlpha(accent, 0.15)

    // Scrim / overlay
    readonly property color scrim: withAlpha(gnome.dark5, 0.55)

    // ── Typography ──────────────────────────────────────────────────────────
    readonly property QtObject font: QtObject {
        // Adwaita Sans — GNOME 50+ system UI font (package: adwaita-fonts)
        readonly property string main:      "Adwaita Sans"
        // Adwaita Mono — companion monospace face, same package
        readonly property string monospace: "Adwaita Mono"

        readonly property QtObject size: QtObject {
            readonly property int tiny:    10
            readonly property int small:   12
            readonly property int normal:  13
            readonly property int large:   15
            readonly property int title:   16
        }
    }

    // ── Adwaita icon theme name (for Quickshell.iconPath) ──────────────────
    readonly property string iconTheme: "Adwaita"

    // ── Rounding ────────────────────────────────────────────────────────────
    readonly property QtObject rounding: QtObject {
        readonly property int none:    0
        readonly property int small:   4
        readonly property int normal:  6
        readonly property int large:   12
        readonly property int full:    9999
    }

    // ── Animation durations (ms) ─────────────────────────────────────────────
    readonly property QtObject anim: QtObject {
        readonly property int fast:    150
        readonly property int normal:  200
        readonly property int slow:    300
    }
}
