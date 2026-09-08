-- Wallpaper selector for Hyprland
-- Random at startup, sequential cycling on demand

local M = {}

--- List all files in the wallpaper directory
-- @param wallpaper_dir Path to the directory containing wallpapers
-- @return table List of full paths, or empty table on failure
local function list_wallpapers(wallpaper_dir)
  local p = io.popen('ls -1 "' .. wallpaper_dir .. '" 2>/dev/null')
  if not p then
    return {}
  end

  local files = {}
  for f in p:lines() do
    table.insert(files, wallpaper_dir .. "/" .. f)
  end
  p:close()

  return files
end

--- Persist the current sequential index to a state file
local function save_index(index)
  local state_dir = os.getenv("XDG_CACHE_HOME") or (os.getenv("HOME") .. "/.cache")
  os.execute('mkdir -p "' .. state_dir .. '"')
  local f = io.open(state_dir .. "/wallpaper-next", "w")
  if f then
    f:write(tostring(index))
    f:close()
  end
end

--- Load the last sequential index from the state file
local function load_index()
  local state_dir = os.getenv("XDG_CACHE_HOME") or (os.getenv("HOME") .. "/.cache")
  local f = io.open(state_dir .. "/wallpaper-next", "r")
  if not f then
    return 0
  end
  local index = tonumber(f:read("*l")) or 0
  f:close()
  return index
end

--- Set a given wallpaper on all monitors
local function set_wallpaper(bg)
  hl.exec_cmd('awww img "' .. bg .. '"')
end

--- Set a random wallpaper from the specified directory on all monitors
-- @param wallpaper_dir Path to the directory containing wallpapers
-- @return boolean True if successful, false otherwise
function M.set_random(wallpaper_dir)
  local files = list_wallpapers(wallpaper_dir)
  if #files == 0 then
    print("Warning: no wallpapers found in " .. wallpaper_dir)
    return false
  end

  math.randomseed(os.time())
  set_wallpaper(files[math.random(#files)])

  return true
end

--- Cycle to the next wallpaper sequentially across sessions
-- @param wallpaper_dir Path to the directory containing wallpapers
-- @return boolean True if successful, false otherwise
function M.set_next(wallpaper_dir)
  local files = list_wallpapers(wallpaper_dir)
  if #files == 0 then
    print("Warning: no wallpapers found in " .. wallpaper_dir)
    return false
  end

  local index = load_index() % #files + 1
  set_wallpaper(files[index])
  save_index(index)

  return true
end

return M
