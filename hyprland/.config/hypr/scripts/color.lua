-- Color helpers for wallpaper-derived decoration colors
-- Darken a RRGGBB hex color toward black, keeping its hue for a subtle tint.

--- Darken a 6-digit RRGGBB hex color by a factor applied to each channel.
-- @param hex 6-digit hex string without '#'
-- @param factor Per-channel multiplier (0-1); e.g. 0.22 for a dark accent tint
-- @return Darkened 6-digit lowercase hex string
local function darken(hex, factor)
  local r = tonumber(hex:sub(1, 2), 16)
  local g = tonumber(hex:sub(3, 4), 16)
  local b = tonumber(hex:sub(5, 6), 16)
  local function channel(v)
    return string.format("%02x", math.min(255, math.floor(v * factor + 0.5)))
  end
  return channel(r) .. channel(g) .. channel(b)
end

--- Dark accent tint used for the window shadow that separates windows from the
-- wallpaper while keeping the wallpaper accent hue.
-- @param hex 6-digit hex string without '#'
-- @return Darkened 6-digit lowercase hex string
local function shadow_hex(hex)
  return darken(hex, 0.22)
end

return {
  darken = darken,
  shadow_hex = shadow_hex,
}