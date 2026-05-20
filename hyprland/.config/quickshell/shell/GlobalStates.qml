pragma Singleton
pragma ComponentBehavior: Bound

import QtQuick
import Quickshell

Singleton {
    id: root

    // Launcher visibility
    property bool launcherOpen: false

    // Super key tracking (for release-to-open pattern)
    property bool superReleaseMightTrigger: false
}
