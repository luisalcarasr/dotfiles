---------------------------
-- Adwaita-like awesome theme --
---------------------------

local dpi = require("beautiful.xresources").apply_dpi

local gfs = require("gears.filesystem")
-- local themes_path = gfs.get_configuration_dir() .. "themes/"
local themes_path = gfs.get_themes_dir()

local theme = {}

theme.font = "IBM Plex Sans Bold 11"

theme.bg_normal = "#000000"
theme.bg_focus = "#222222"
theme.bg_urgent = "#ff0000"
theme.bg_minimize = "#444444"
theme.bg_systray = theme.bg_normal

theme.fg_normal = "#ffffff"
theme.fg_focus = "#ffffff"
theme.fg_urgent = "#ffffff"
theme.fg_minimize = "#ffffff"

theme.useless_gap = dpi(4)
theme.border_width = dpi(1)
theme.border_normal = "#000000"
theme.border_focus = "#41a7fc"
theme.border_marked = "#535d6c"

theme.systray_icon_spacing = dpi(6)

theme.wallpaper = "/usr/share/backgrounds/gnome/symbolic-d.webp"

theme.layout_fairh = themes_path .. "default/layouts/fairhw.png"
theme.layout_fairv = themes_path .. "default/layouts/fairvw.png"
theme.layout_floating = themes_path .. "default/layouts/floatingw.png"
theme.layout_magnifier = themes_path .. "default/layouts/magnifierw.png"
theme.layout_max = themes_path .. "default/layouts/maxw.png"
theme.layout_fullscreen = themes_path .. "default/layouts/fullscreenw.png"
theme.layout_tilebottom = themes_path .. "default/layouts/tilebottomw.png"
theme.layout_tileleft = themes_path .. "default/layouts/tileleftw.png"
theme.layout_tile = themes_path .. "default/layouts/tilew.png"
theme.layout_tiletop = themes_path .. "default/layouts/tiletopw.png"
theme.layout_spiral = themes_path .. "default/layouts/spiralw.png"
theme.layout_dwindle = themes_path .. "default/layouts/dwindlew.png"
theme.layout_cornernw = themes_path .. "default/layouts/cornernww.png"
theme.layout_cornerne = themes_path .. "default/layouts/cornernew.png"
theme.layout_cornersw = themes_path .. "default/layouts/cornersww.png"
theme.layout_cornerse = themes_path .. "default/layouts/cornersew.png"

theme.awesome_icon = "/usr/share/pixmaps/archlinux-logo.svg"

theme.icon_theme = nil

theme.notification_width = dpi(256 * 1.5)
theme.notification_icon_size = dpi(64)
theme.notification_font = "IBM Plex Sans 11"

return theme
