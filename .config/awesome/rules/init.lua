-- Standard awesome library
local awful = require("awful")
require("awful.autofocus")
local beautiful = require("beautiful")

awful.rules.rules = {
    -- All clients will match this rule.
    {
        rule = {},
        properties = {
            border_width = beautiful.border_width,
            border_color = beautiful.border_normal,
            focus = awful.client.focus.filter,
            raise = true,
            keys = clientkeys,
            buttons = clientbuttons,
            screen = awful.screen.preferred,
            placement = awful.placement.centered,
        },
    }, -- Floating clients.
    {
        rule_any = {
            instance = {
                "DTA", -- Firefox addon DownThemAll.
                "copyq", -- Includes session name in class.
                "pinentry",
            },
            class = {
                "Arandr",
                "Blueman-manager",
                "Gpick",
                "Kruler",
                "MessageWin", -- kalarm.
                "Sxiv",
                "Tor Browser", -- Needs a fixed window size to avoid fingerprinting by screen size.
                "Wpa_gui",
                "veromix",
                "xtightvncviewer",
            },

            -- Note that the name property shown in xprop might be set slightly after creation of the client
            -- and the name shown there might not match defined rules here.
            name = {
                "Event Tester", -- xev.
            },
            role = {
                "AlarmWindow", -- Thunderbird's calendar.
                "ConfigManager", -- Thunderbird's about:config.
                "pop-up", -- e.g. Google Chrome's (detached) Developer Tools.
            },
        },
        properties = { floating = true },
    }, -- Add titlebars to normal clients and dialogs
    {
        rule_any = { type = { "normal", "dialog" } },
        properties = { titlebars_enabled = true },
    }, -- Always center floating clients
    -- Set Firefox to always map on the tag named "2" on screen 1.
    -- { rule = { class = "Firefox" },
    --   properties = { screen = 1, tag = "2" } },
    -- Spawn floating clients centered
    -- Force fullscreen
    {
        rule = {
            fullscreen = true,
        },
        properties = {
            floating = true,
            ontop = true,
            fullscreen = true,
        },
    },
    {
        rule = {
            fullscreen = true,
        },
        callback = function(c)
            c.screen = screen[1]
            local g = c:geometry()
            local x = g.x + g.width / 2
            local y = g.y + g.height / 2
            mouse.coords({ x = x, y = y })
            c:emit_signal("request::activate", "mouse_enter", { raise = false })
        end,
    },
    -- Set apps on proper screen.
    {
        properties = {
            screen = 2,
            tag = "1",
        },
        rule_any = {
            class = {
                "Slack",
                "discord",
                "Microsoft-edge",
            },
        },
    },
    {
        properties = {
            screen = 2,
            tag = "3",
        },
        rule_any = {
            class = {
                "Spotify",
                "steam",
            },
        },
    },
}
-- }}}
