local function icon(name, kind)
    if kind == "pixmaps" then
        return "/usr/share/" .. kind .. "/" .. name .. ".svg"
    else
        return "/usr/share/icons/Adwaita/24x24/"
            .. kind
            .. "/"
            .. name
            .. "-symbolic.symbolic.png"
    end
end

return icon
