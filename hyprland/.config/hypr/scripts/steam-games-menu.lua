local home = os.getenv("HOME")
local steam_dir = home .. "/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps"

local blacklist = {
    "Proton",
    "Steam Linux Runtime",
    "Steam Runtime",
    "Steamworks Common Redistributables",
    "SteamVR",
}

local function notify(msg, urgency)
    urgency = urgency or "normal"
    os.execute('notify-send "Steam Games" "' .. msg:gsub('"', '\\"') .. '" -u ' .. urgency)
end

local handle = io.popen('ls -1 "' .. steam_dir .. '" 2>/dev/null')
if not handle then
    notify("Steam directory not found", "critical")
    return
end

local games = {}
for entry in handle:lines() do
    local appid = entry:match("^appmanifest_(%d+)%.acf$")
    if appid then
        local manifest = steam_dir .. "/" .. entry
        local f = io.open(manifest, "r")
        if f then
            local content = f:read("*all")
            f:close()
            local name = content:match('"name"%s+"([^"]+)"')
            if name then
                local skip = false
                for _, b in ipairs(blacklist) do
                    if name:find(b, 1, true) then
                        skip = true
                        break
                    end
                end
                if not skip then
                    games[name] = appid
                end
            end
        end
    end
end
handle:close()

if next(games) == nil then
    notify("No games found")
    return
end

local sorted = {}
for name, _ in pairs(games) do
    table.insert(sorted, name)
end
table.sort(sorted)

local input = table.concat(sorted, "\n")
local ph = io.popen("printf '%s' '" .. input:gsub("'", "'\\''") .. "' | wofi --dmenu --prompt 'Launch Game'", "r")
local selected = ph:read("*l")
ph:close()

if selected and #selected > 0 then
    local appid = games[selected]
    if appid then
        notify(selected)
        os.execute('nohup flatpak run com.valvesoftware.Steam steam://rungameid/' .. appid .. ' > /dev/null 2>&1 &')
    end
end
