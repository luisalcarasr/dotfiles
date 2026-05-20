//@ pragma UseQApplication
//@ pragma Env QT_QUICK_CONTROLS_STYLE=Basic
//@ pragma Env QT_QUICK_FLICKABLE_WHEEL_DECELERATION=10000

import QtQuick
import Quickshell
import "modules/common"
import "modules/bar"
import "modules/launcher"

ShellRoot {
    // Load the persistent config first
    Config { id: config }
    Appearance { id: appearance }
    GlobalStates { id: globalStates }

    // Top bar — one instance per monitor
    Bar {}

    // Spotlight launcher — single floating overlay
    Launcher {}
}
