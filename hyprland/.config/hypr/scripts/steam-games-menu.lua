local home = os.getenv("HOME")
local steam_dir = home .. "/.local/share/Steam/steamapps"

local blacklist = {
    "Proton",
    "Steam Linux Runtime",
    "Steamworks Common Redistributables",
    "SteamVR",
}

local function notify(msg, urgency)
    urgency = urgency or "normal"
    os.execute('notify-send "Steam Games" "' .. msg:gsub('"', '\\"') .. '" -u ' .. urgency)
end

local handle = io.popen('ls -1 "' .. steam_dir .. '/appmanifest_*.acf" 2>/dev/null')
if not handle then
    notify("Steam directory not found", "critical")
    return
end

local games = {}
for manifest in handle:lines() do
    local appid = manifest:match("appmanifest_(%d+).acf$")
    local f = io.open(manifest, "r")
    if f then
        local content = f:read("*all")
        f:close()
        local name = content:match('"name"%s+"([^"]+)"')
        if name and appid then
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
local tmp = "/tmp/steam-menu-" .. os.time()
local f = io.open(tmp, "w")
f:write(input)
f:close()

local ph = io.popen("sort < " .. tmp .. " | hyprlauncher --dmenu --prompt 'Launch Game'", "r")
local selected = ph:read("*l")
ph:close()
os.remove(tmp)

if selected and #selected > 0 then
    local appid = games[selected]
    if appid then
        notify(selected)
        local steam_sh = home .. "/.local/share/Steam/steam.sh"
        local f = io.open(steam_sh, "r")
        if f then
            f:close()
            os.execute('nohup "' .. steam_sh .. '" "steam://rungameid/' .. appid .. '" > /dev/null 2>&1 &')
        else
            os.execute('nohup xdg-open "steam://rungameid/' .. appid .. '" > /dev/null 2>&1 &')
        end
    end
end
