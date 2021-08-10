import Xmobar
import Theme

colors = theme "onedark"
-- Example user-defined plugin

data HelloWorld = HelloWorld
    deriving (Read, Show)

instance Exec HelloWorld where
    alias HelloWorld = "hw"
    run   HelloWorld = return ("<fc=" ++ (colors "blue") ++ ">ARCH</fc>" ++ " <fc=" ++ (colors "fg") ++ ">LINUX</fc>")

data Separator = Separator
    deriving (Read, Show)

instance Exec Separator where
    alias Separator = "separator"
    run   Separator = return ("<fc=" ++ (colors "gray") ++ "><fn=1> | </fn></fc>")

data GPU = GPU
    deriving (Read, Show)

instance Exec GPU where
    alias GPU = "separator"
    run   GPU = return ("<fc=" ++ (colors "gray") ++ "><fn=1>|</fn></fc>")

-- Configuration, using predefined monitors as well as our HelloWorld
-- plugin:

config :: Config
config = defaultConfig {
  font = "xft:IBM Plex Sans-11"
  , additionalFonts = []
  , borderColor = colors "bg"
  , border = TopB
  , bgColor = colors "bg"
  , fgColor = colors "gray"
  , alpha = 255
  , position = Top
  , textOffset = -1
  , iconOffset = -1
  , lowerOnStart = True
  , pickBroadest = False
  , persistent = False
  , hideOnStart = False
  , iconRoot = "."
  , allDesktops = True
  , overrideRedirect = True
  , commands = [ Run $ Network "wlp2s0" ["-t", "NET: <fc=" ++ (colors "fg") ++ "><rx>KB/<tx>KB</fc>"] 10
               , Run $ Cpu ["-H","90","--high", colors "red", "-t", "CPU: <fc=" ++ (colors "fg") ++ "><total>%</fc>"] 10
               , Run $ Memory ["-t","RAM: <fc=" ++ (colors "fg") ++ "><usedratio>%</fc>"] 10
               , Run $ Swap ["-t","SWAP: <fc=" ++ (colors "fg") ++ "><usedratio>%</fc>"] 10
               , Run $ Com "nvidia" ["-g"] "gpu" 10
               , Run $ Com "nvidia" ["-v"] "vram" 10
               , Run $ Com "nvidia" ["-t"] "gtemp" 10
               , Run $ Com "intel" ["-t"] "temp" 10
               , Run $ Com "trayicons" ["panel"] "trayer" 10
               , Run $ Date "%H:%M" "date" 10
               , Run HelloWorld
               , Run Separator
               , Run UnsafeStdinReader
              ]
  , sepChar = "%"
  , alignSep = "}{"
  , template = ("    %hw% %separator% %UnsafeStdinReader% }\
                 \<fc=" ++ (colors "fg") ++ ">%date%</fc> { %wlp2s0% %separator% \
                 \%cpu% %separator% TEMP: <fc=" ++ (colors "fg") ++ ">%temp%</fc> %separator% %memory% %separator% %swap% %separator% \
                 \GPU: <fc=" ++ (colors "fg") ++ ">%gpu%</fc> %separator% TEMP: <fc=" ++ (colors "fg") ++ ">%gtemp%</fc> \
                 \%separator% VRAM: <fc=" ++ (colors "fg") ++ ">%vram%</fc> %separator% %trayer%  ")
}

main :: IO ()
main = xmobar config
