import System.IO
import XMonad
import qualified XMonad.StackSet as W
import XMonad.Actions.WorkspaceNames
import XMonad.Actions.CopyWindow (kill1)
import XMonad.Actions.WithAll (killAll)
import XMonad.Actions.Promote
import XMonad.Layout.Gaps
import XMonad.Layout.Spacing
import XMonad.Layout.LayoutModifier
import XMonad.Layout.ResizableTile
import XMonad.Config.Desktop
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.SetWMName
import XMonad.Hooks.WorkspaceHistory
import XMonad.Util.Run
import XMonad.Util.SpawnOnce
import XMonad.Util.EZConfig (additionalKeysP)
import Theme

color = theme "onedark"

myWorkspaces = ["DEV", "WWW", "DESIGN", "MEDIA", "MISC", "SOCIAL", "GAMES", "TERM", "VBOX"]

mySpacing:: Integer -> l a -> XMonad.Layout.LayoutModifier.ModifiedLayout Spacing l a
mySpacing i = spacingRaw False (Border i i i i) True (Border i i i i) True

myStartupHook = do
          spawnOnce "nitrogen --restore &"
          spawnOnce "picom &"
          spawnOnce "trayer --edge top --align right --widthtype request --padding 8 --SetDockType true --SetPartialStrut true --expand true --monitor 1 --transparent true --alpha 0 --tint 0x292d3e --height 18 &"
          setWMName "LG3D"

myKeys :: [(String, X ())]

myKeys =
  [ ("M-<Return>", spawn "alacritty")
  -- , ("M-m", spawn "spotify")
  , ("M-t", spawn "teams")
  , ("M-g", spawn "steam")
  , ("M-d", spawn "discord")
  , ("M-i i", spawn "firefox")
  , ("M-i p", spawn "firefox -private")
  , ("M-i f", spawn "firefox figma.com")
  , ("M-i y", spawn "firefox youtube.com")
  , ("M-n", spawn "firefox localhost:4000")
  , ("M-<Space>", spawn "rofi -show run")
  , ("M-S p", spawn "shutdown -h now")
  , ("M-S r", spawn "reboot")

  -- KB_GROUP Windows navigation
  , ("M-m", windows W.focusMaster)  -- Move focus to the master window
  , ("M-j", windows W.focusDown)    -- Move focus to the next window
  , ("M-k", windows W.focusUp)      -- Move focus to the prev window
  , ("M-S-m", windows W.swapMaster) -- Swap the focused window and the master window
  , ("M-S-j", windows W.swapDown)   -- Swap focused window with next window
  , ("M-S-k", windows W.swapUp)     -- Swap focused window with prev window
  , ("M-<Backspace>", promote)      -- Moves focused window to master, others maintain order

    -- KB_GROUP Window resizing
  , ("M-h", sendMessage Shrink)                   -- Shrink horiz window width
  , ("M-l", sendMessage Expand)                   -- Expand horiz window width
  , ("M-M1-j", sendMessage MirrorShrink)          -- Shrink vert window width
  , ("M-M1-k", sendMessage MirrorExpand)          -- Expand vert window width

  , ("M-<Tab>", sendMessage NextLayout)

  -- KB_GROUP Kill windows
  , ("M-c", kill1)     -- Kill the currently focused client
  , ("M-S-c", killAll)   -- Kill all windows on current workspace
  ]

main = do
  xmproc <- spawnPipe "$HOME/.xmonad/xmobar"
  xmonad $ defaultConfig {
    manageHook = manageDocks,
    terminal = "alacritty",
    modMask = mod4Mask,
    workspaces = myWorkspaces,
    borderWidth = 2,
    startupHook = myStartupHook,
    normalBorderColor  = color "fg",
    focusedBorderColor = color "blue",
    layoutHook = mySpacing 8 $ avoidStruts $ layoutHook def,
    handleEventHook = docksEventHook,
    logHook = workspaceHistoryHook <+> dynamicLogWithPP xmobarPP {
        ppOutput = hPutStrLn xmproc,
        ppCurrent = xmobarColor (color "purple") "" . wrap (" <box type=Bottom width=2 color=" ++ (color "purple") ++ ">") "</box> "
      , ppVisible = xmobarColor (color "purple") "" . wrap " " " "
      , ppHidden = xmobarColor (color "fg") "" . wrap (" <box type=Bottom width=2 color=" ++ (color "fg") ++ ">") "</box> "
      , ppHiddenNoWindows = xmobarColor (color "gray") "" . wrap " " " "
      , ppTitle = xmobarColor (color "fg") "" . shorten 60
      , ppSep = ("<fc=" ++ (color "gray") ++ "> <fn=1>|</fn> </fc>")
      , ppUrgent = xmobarColor (color "red") "" . wrap " !" "! "
      , ppOrder  = \(ws:l:t:ex) -> [ws]
      -- , ppOrder  = \(ws:l:t:ex) -> [ws,l]++ex++[t]
    }
  } `additionalKeysP` myKeys
