-- Random wallpaper selector for Hyprland
-- Sets a random wallpaper from a directory on all monitors

local M = {}

--- Set a random wallpaper from the specified directory on all monitors
-- @param wallpaper_dir Path to the directory containing wallpapers
-- @return boolean True if successful, false otherwise
function M.set_random(wallpaper_dir)
  if not wallpaper_dir then
    print("Error: wallpaper directory not specified")
    return false
  end

  -- List all files in the wallpaper directory
  local p = io.popen('ls -1 "' .. wallpaper_dir .. '" 2>/dev/null')
  if not p then
    print("Error: could not list wallpapers in " .. wallpaper_dir)
    return false
  end

  local files = {}
  for f in p:lines() do
    table.insert(files, wallpaper_dir .. "/" .. f)
  end
  p:close()

  if #files == 0 then
    print("Warning: no wallpapers found in " .. wallpaper_dir)
    return false
  end

  -- Select a random wallpaper
  math.randomseed(os.time())
  local bg = files[math.random(#files)]

  -- Set wallpaper with awww on all monitors
  hl.exec_cmd('awww img "' .. bg .. '"')

  return true
end

return M
