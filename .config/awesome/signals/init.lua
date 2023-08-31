-- Standard awesome library
local gears = require("gears")
local awful = require("awful")
require("awful.autofocus")
-- Widget and layout library
local wibox = require("wibox")
-- Theme handling library
local beautiful = require("beautiful")
-- Notification library
local naughty = require("naughty")
local menubar = require("menubar")
local hotkeys_popup = require("awful.hotkeys_popup")
local xresources = require("beautiful.xresources")
local dpi = xresources.apply_dpi
-- Signal function to execute when a new client appears.
client.connect_signal("manage", function(c)
    -- Set the windows at the slave,
    -- i.e. put it at the end of others instead of setting it master.
    if not awesome.startup then
        awful.client.setslave(c)
    end

    if
        awesome.startup
        and not c.size_hints.user_position
        and not c.size_hints.program_position
    then
        -- Prevent clients from being unreachable after screen count changes.
        awful.placement.no_offscreen(c)
    end
end)

-- Enable sloppy focus, so that focus follows mouse.
client.connect_signal("mouse::enter", function(c)
    c:emit_signal("request::activate", "mouse_enter", { raise = false })
end)

client.connect_signal("focus", function(c)
    c.border_color = beautiful.border_focus
end)
client.connect_signal("unfocus", function(c)
    c.border_color = beautiful.border_normal
end)

client.connect_signal("mouse::leave", function(c)
    if c.fullscreen then
        local cg = c:geometry() -- get window size
        local mg = mouse.coords() -- get current mouse position

        -- quick and dirty calculate for mouse position correction
        local newx = mg.x <= cg.x and cg.x
            or mg.x >= (cg.x + cg.width) and cg.x + cg.width
            or mg.x
        local newy = mg.y <= cg.y and cg.y
            or mg.y >= (cg.y + cg.height) and cg.y + cg.height
            or mg.y

        -- set mouse to new position
        mouse.coords({ x = newx, y = newy })
    end
end)
