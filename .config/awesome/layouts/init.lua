local awful = require("awful")

local vertical = function(p, context, layout_config)
    local wa = p.workarea
    local cls = p.clients

    local height = wa.height / #cls
    local y = wa.y

    for _, c in ipairs(cls) do
        local g = {
            x = wa.x + p.useless_gap,
            y = y + p.useless_gap,
            width = wa.width - p.useless_gap * 2,
            height = height - p.useless_gap * 2,
        }
        c:geometry(g)
        y = y + g.height + p.useless_gap * 2
    end
end

local layout = {
    auto = {
        name = awful.layout.suit.tile.name,
        skip_gap = awful.layout.suit.tile.skip_gap,
        arrange = function(p, context, layout_config)
            local wa = p.workarea
            if wa.height > wa.width then
                vertical(p, context, layout_config)
            else
                awful.layout.suit.tile.arrange(p, context, layout_config)
            end
        end,
    },
}

-- Table of layouts to cover with awful.layout.inc, order matters.
awful.layout.layouts = {
    layout.auto,
    -- awful.layout.suit.tile,
    -- awful.layout.suit.tile.left,
    -- awful.layout.suit.tile.bottom,
    -- awful.layout.suit.tile.top,
    -- awful.layout.suit.floating,
    -- awful.layout.suit.fair,
    -- awful.layout.suit.fair.horizontal,
    -- awful.layout.suit.spiral,
    -- awful.layout.suit.spiral.dwindle,
    -- awful.layout.suit.max,
    -- awful.layout.suit.max.fullscreen,
    -- awful.layout.suit.magnifier,
    -- awful.layout.suit.corner.nw,
    -- awful.layout.suit.corner.ne,
    -- awful.layout.suit.corner.sw,
    -- awful.layout.suit.corner.se,
}
