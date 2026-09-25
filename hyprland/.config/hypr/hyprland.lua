-- Hyprland Lua config
-- https://wiki.hypr.land/Configuring/Start/

---------------------
---- MY PROGRAMS ----
---------------------

local terminal = "kitty"
-- wofi as a toggle: pressing the launcher shortcut while wofi is open just
-- closes it, so only a single instance can ever exist.
local menu = "pkill -x wofi || wofi"
local browser = "flatpak run com.brave.Browser"
local mainMod = "SUPER"

local home = os.getenv("HOME")

------------------
---- MONITORS ----
------------------

hl.monitor({
	output = "desc:Dell Inc. DELL P2423D B0MQVP3",
	mode = "2560x1440@60",
	position = "0x0",
	scale = 1,
})

hl.monitor({
	output = "desc:GGF MG700 0000000000000",
	mode = "2560x1440@144",
	position = "2560x0",
	scale = 1,
	vrr = 1,
})

hl.monitor({
	output = "desc:Dell Inc. DELL P2423DE B87GXR3",
	mode = "2560x1440@60",
	position = "5120x0",
	scale = 1,
})

-------------------------------
---- ENVIRONMENT VARIABLES ----
-------------------------------

hl.env("XCURSOR_SIZE", "24")
hl.env("HYPRCURSOR_SIZE", "24")

-------------------------------
---- CURSOR FOLLOWS FOCUS ----
-------------------------------

-- Move the cursor to the center of the active window when focus changes
-- via keyboard (workspace / window navigation). Skip clicks and hover so
-- the cursor is not yanked away while using the mouse.
local FOCUS_REASON_FFM = 1
local FOCUS_REASON_CLICK = 16

hl.on("window.active", function(window, focusReason)
	if window == nil then
		return
	end
	if (focusReason & (FOCUS_REASON_FFM | FOCUS_REASON_CLICK)) ~= 0 then
		return
	end
	local at, size = window.at, window.size
	if at ~= nil and size ~= nil then
		hl.dispatch(hl.dsp.cursor.move({ x = at.x + size.x / 2, y = at.y + size.y / 2 }))
	end
end)

----------------------------
---- FOCUS HIGHLIGHT ----
----------------------------

-- Highlight the focused window while the SUPER key is held down: a thicker
-- border with a rotating gradient that follows keyboard navigation and
-- reverts to the default border as soon as SUPER is released. The gradient
-- runs between the accent color of the current wallpaper and its hue-opposite
-- (see scripts/accent.py); it is refreshed whenever the wallpaper changes.
-- Triggered by the key event (xkb keycodes 133/134 for Super_L/Super_R) with
-- a slow polling safety net; reads state only, so no keybind is consumed and
-- other shortcuts keep working.
local FOCUS_HIGHLIGHT_STEP = 150
local FOCUS_HIGHLIGHT_ANGLE_STEP = 30
local FOCUS_HIGHLIGHT_BORDER = 4
local FOCUS_HIGHLIGHT_POLL_MS = 500
local FOCUS_GRADIENT_A = "rgba(803457ee)"
local FOCUS_GRADIENT_B = "rgba(a1eb60ee)"
local ACCENT_SCRIPT = home .. "/.config/hypr/scripts/accent.py"
local ACTIVE_BORDER_DEFAULT = "rgba(5b8abfee)"
local BORDER_SIZE_DEFAULT = 4
local SUPER_KEYCODE_LEFT = 133
local SUPER_KEYCODE_RIGHT = 134

local highlightAddress = nil
local highlightRotateTimer = nil
local highlightPollTimer = nil
local highlightSuperDown = false

-- Read the accent triangle for the current wallpaper. accent.py prints
-- "BORDER GRAD_A GRAD_B": three triadic colors sharing the wallpaper accent
-- hue. Returns a table or nil on failure.
local function accentColors(wallpaper_path)
	if wallpaper_path == nil then
		return nil
	end
	local p = io.popen('python3 "' .. ACCENT_SCRIPT .. '" "' .. wallpaper_path .. '" 2>/dev/null')
	if not p then
		return nil
	end
	local out = p:read("*l")
	p:close()
	if out == nil then
		return nil
	end
	local border, grad_a, grad_b = out:match("(%x%x%x%x%x%x)%s+(%x%x%x%x%x%x)%s+(%x%x%x%x%x%x)")
	if border == nil then
		return nil
	end
	return { border = border, grad_a = grad_a, grad_b = grad_b }
end

local function highlightReset(address)
	if address == nil then
		return
	end
	pcall(function()
		hl.dispatch(
			hl.dsp.window.set_prop({ prop = "border_size", value = tostring(BORDER_SIZE_DEFAULT), window = address })
		)
		hl.dispatch(
			hl.dsp.window.set_prop({ prop = "active_border_color", value = ACTIVE_BORDER_DEFAULT, window = address })
		)
	end)
end

-- The setprop gradient parser drops the first space-separated token, so a
-- harmless separator keeps both gradient colors and the angle parseable.
local function highlightGradient(angleDeg)
	return table.concat({ "unused", FOCUS_GRADIENT_A, FOCUS_GRADIENT_B, angleDeg .. "deg" }, " ")
end

local function highlightStop()
	if highlightRotateTimer ~= nil then
		highlightRotateTimer:set_enabled(false)
		highlightRotateTimer = nil
	end
	highlightReset(highlightAddress)
	highlightAddress = nil
end

local function highlightStart(w)
	if w == nil or w.address == nil then
		return
	end

	if highlightAddress ~= nil then
		highlightStop()
	end

	local address = "address:" .. w.address
	highlightAddress = address
	local angle = 0

	hl.dispatch(
		hl.dsp.window.set_prop({ prop = "border_size", value = tostring(FOCUS_HIGHLIGHT_BORDER), window = address })
	)
	hl.dispatch(
		hl.dsp.window.set_prop({ prop = "active_border_color", value = highlightGradient(angle), window = address })
	)

	highlightRotateTimer = hl.timer(function()
		angle = (angle + FOCUS_HIGHLIGHT_ANGLE_STEP) % 360
		hl.dispatch(
			hl.dsp.window.set_prop({ prop = "active_border_color", value = highlightGradient(angle), window = address })
		)
	end, { timeout = FOCUS_HIGHLIGHT_STEP, type = "repeat" })
end

local function highlightIsSuperDown()
	return hl.is_key_down(SUPER_KEYCODE_LEFT) or hl.is_key_down(SUPER_KEYCODE_RIGHT)
end

local function highlightSetState(down)
	highlightSuperDown = down
	if down then
		highlightStart(hl.get_active_window())
	else
		highlightStop()
	end
end

-- input.keyboard.key args: xkb keycode, timestamp, state (0 released, 1
-- pressed, 2 repeated).
local function highlightOnKey(keycode, _, state)
	local isSuper = keycode == SUPER_KEYCODE_LEFT or keycode == SUPER_KEYCODE_RIGHT
	if not isSuper then
		return
	end
	if state == 1 and not highlightSuperDown then
		highlightSetState(true)
	elseif state == 0 and highlightSuperDown then
		highlightSetState(false)
	end
end

hl.on("input.keyboard.key", highlightOnKey)

-- Safety net: the key event drives press/release instantly, but a slow poll
-- re-synchronizes in case a release is swallowed by an input grab or config
-- reloaded while SUPER was already held.
highlightPollTimer = hl.timer(function()
	local down = highlightIsSuperDown()
	if down ~= highlightSuperDown then
		highlightSetState(down)
	end
end, { timeout = FOCUS_HIGHLIGHT_POLL_MS, type = "repeat" })

hl.on("window.active", function(window)
	if window ~= nil and highlightSuperDown then
		highlightStart(window)
	elseif window ~= nil then
		-- Newly focused window: apply the pastel accent border.
		highlightReset("address:" .. window.address)
	end
end)

-- A config reload recreates the Lua state, so tracked overrides are lost and
-- could leave a stale highlight behind. Reset every window's border whenever
-- the reload happens outside a held SUPER.
local function resetAllBorders()
	for _, win in ipairs(hl.get_windows() or {}) do
		if win ~= nil and win.address ~= nil then
			highlightReset("address:" .. win.address)
		end
	end
end

-- Refresh every accent-derived color from the current wallpaper: the
-- highlight gradient from two triadic partners and the default active border
-- from the third. Re-applies the default border so already-open windows pick
-- up the new border color.
local function updateAccent(wallpaper_path)
	local colors = accentColors(wallpaper_path)
	if colors == nil then
		return
	end
	FOCUS_GRADIENT_A = "rgba(" .. colors.grad_a .. "ee)"
	FOCUS_GRADIENT_B = "rgba(" .. colors.grad_b .. "ee)"
	ACTIVE_BORDER_DEFAULT = "rgba(" .. colors.border .. "ee)"
	resetAllBorders()
end

hl.on("config.reloaded", function()
	updateAccent(wallpaper.current(home .. "/Pictures/Wallpapers"))
	if not highlightIsSuperDown() then
		resetAllBorders()
	end
end)

--------------------------
---- AUTOSTART ----
--------------------------

-- Load wallpaper module
local wallpaper = require("scripts.wallpaper")

hl.on("hyprland.start", function()
	hl.exec_cmd("waybar")
	hl.exec_cmd("awww-daemon")
	hl.exec_cmd("mako")

	-- Set random wallpaper at start
	wallpaper.set_random(home .. "/Pictures/Wallpapers")
	hl.exec_cmd("hyprctl reload")
end)

-----------------------
---- LOOK AND FEEL ----
-----------------------

-- Derive the default active border from the current wallpaper accent so the
-- border matches the wallpaper even before the first SUPER hold.
local initialColors = accentColors(wallpaper.current(home .. "/Pictures/Wallpapers"))
if initialColors ~= nil then
	ACTIVE_BORDER_DEFAULT = "rgba(" .. initialColors.border .. "ee)"
end

hl.config({
	general = {
		gaps_in = 4,
		gaps_out = 8,
		border_size = 4,
		col = {
			active_border = ACTIVE_BORDER_DEFAULT,
			inactive_border = "rgba(21262d80)",
		},
		resize_on_border = false,
		allow_tearing = false,
		layout = "dwindle",
	},
	decoration = {
		rounding = 4,
		rounding_power = 4,
		active_opacity = 1.0,
		inactive_opacity = 1.0,
		shadow = {
			enabled = false,
			range = 4,
			render_power = 4,
			color = ACTIVE_BORDER_DEFAULT,
			color_inactive = "rgba(16161660)",
			offset = "0 0",
		},
		blur = {
			enabled = true,
			size = 8,
			passes = 3,
			vibrancy = 0.1696,
			noise = 0.0117,
			contrast = 0.8916,
			brightness = 0.8172,
			popups = true,
			popups_ignorealpha = 0.2,
		},
	},
	animations = {
		enabled = true,
	},
	dwindle = {
		preserve_split = true,
	},
	master = {
		new_status = "master",
	},
	misc = {
		force_default_wallpaper = -1,
		disable_hyprland_logo = true,
	},
	input = {
		kb_layout = "us",
		kb_variant = "",
		kb_model = "",
		kb_options = "",
		kb_rules = "",
		follow_mouse = 1,
		sensitivity = 0,
		touchpad = {
			natural_scroll = false,
		},
	},
	cursor = {
		hide_on_key_press = true,
		inactive_timeout = 2,
	},
})

---------------
---- CURVES ----
---------------

hl.curve("easeOutQuint", { type = "bezier", points = { { 0.23, 1 }, { 0.32, 1 } } })
hl.curve("easeInOutCubic", { type = "bezier", points = { { 0.65, 0.05 }, { 0.36, 1 } } })
hl.curve("linear", { type = "bezier", points = { { 0, 0 }, { 1, 1 } } })
hl.curve("almostLinear", { type = "bezier", points = { { 0.5, 0.5 }, { 0.75, 1 } } })
hl.curve("quick", { type = "bezier", points = { { 0.15, 0 }, { 0.1, 1 } } })

------------------
---- ANIMS ----
------------------

hl.animation({ leaf = "global", enabled = true, speed = 10, bezier = "default" })
hl.animation({ leaf = "border", enabled = true, speed = 5.39, bezier = "easeOutQuint" })
hl.animation({ leaf = "windows", enabled = true, speed = 4.79, bezier = "easeOutQuint" })
hl.animation({ leaf = "windowsIn", enabled = true, speed = 4.1, bezier = "easeOutQuint", style = "popin 87%" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 1.49, bezier = "linear", style = "popin 87%" })
hl.animation({ leaf = "fadeIn", enabled = true, speed = 1.73, bezier = "almostLinear" })
hl.animation({ leaf = "fadeOut", enabled = true, speed = 1.46, bezier = "almostLinear" })
hl.animation({ leaf = "fade", enabled = true, speed = 3.03, bezier = "quick" })
hl.animation({ leaf = "layers", enabled = true, speed = 3.81, bezier = "easeOutQuint" })
hl.animation({ leaf = "layersIn", enabled = true, speed = 4, bezier = "easeOutQuint", style = "fade" })
hl.animation({ leaf = "layersOut", enabled = true, speed = 1.5, bezier = "linear", style = "fade" })
hl.animation({ leaf = "fadeLayersIn", enabled = true, speed = 1.79, bezier = "almostLinear" })
hl.animation({ leaf = "fadeLayersOut", enabled = true, speed = 1.39, bezier = "almostLinear" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 1.94, bezier = "almostLinear", style = "fade" })
hl.animation({ leaf = "workspacesIn", enabled = true, speed = 1.21, bezier = "almostLinear", style = "fade" })
hl.animation({ leaf = "workspacesOut", enabled = true, speed = 1.94, bezier = "almostLinear", style = "fade" })
hl.animation({ leaf = "zoomFactor", enabled = true, speed = 7, bezier = "quick" })

-----------------
---- GESTURE ----
-----------------

hl.gesture({
	fingers = 3,
	direction = "horizontal",
	action = "workspace",
})

----------------
---- DEVICE ----
----------------

hl.device({
	name = "epic-mouse-v1",
	sensitivity = -0.5,
})

---------------------
---- WINDOW RULES ----
---------------------

hl.window_rule({
	name = "suppress-maximize-events",
	match = { class = ".*" },
	suppress_event = "maximize",
})

hl.window_rule({
	name = "fix-xwayland-drags",
	match = {
		class = "^$",
		title = "^$",
		xwayland = true,
		float = true,
		fullscreen = false,
		pin = false,
	},
	no_focus = true,
})

-- Blur the waybar layer
hl.layer_rule({
	name = "blur-waybar",
	match = { namespace = "waybar" },
	blur = true,
	blur_popups = true,
	ignore_alpha = 0.5,
})

-- Blur waybar tooltips
hl.layer_rule({
	name = "blur-tooltip",
	match = { namespace = "tooltip" },
	blur = true,
	ignore_alpha = 0.5,
})

-- Blur the wofi launcher
hl.layer_rule({
	name = "blur-wofi",
	match = { namespace = "wofi" },
	blur = true,
	ignore_alpha = 0.5,
})

-- Blur mako notifications
hl.layer_rule({
	name = "blur-mako",
	match = { namespace = "notifications" },
	blur = true,
	blur_popups = true,
	ignore_alpha = 0.5,
})

hl.window_rule({
	name = "tui-floating",
	match = { class = "^tui-floating$" },
	float = true,
	size = { 854, 480 },
	keep_aspect_ratio = true,
	border_size = 0,
	no_shadow = true,
})

---------------------
---- KEYBINDINGS ----
---------------------

-- Launch programs
hl.bind(mainMod .. " + RETURN", hl.dsp.exec_cmd(terminal), { description = "Open terminal" })
hl.bind(mainMod .. " + BACKSLASH", hl.dsp.exec_cmd(browser), { description = "Open browser" })
hl.bind(mainMod .. " + SPACE", hl.dsp.exec_cmd(menu), { description = "Open launcher (wofi)" })

-- Close wofi when it stops being the focused window: any click on another
-- window or keyboard focus change dismisses the launcher. The open/active
-- wofi never matches the branch, so it cannot close itself.
hl.on("window.active", function(window)
	if window == nil or (window.class or ""):lower() == "wofi" then
		return
	end
	os.execute("pkill -x wofi")
end)
hl.bind(
	mainMod .. " + G",
	hl.dsp.exec_cmd("lua " .. home .. "/.config/hypr/scripts/steam-games-menu.lua"),
	{ description = "Steam games menu" }
)
hl.bind(mainMod .. " + N", hl.dsp.exec_cmd("makoctl mode -t dnd"), { description = "Toggle Do Not Disturb" })

-- Window management
hl.bind(mainMod .. " + Q", hl.dsp.window.close(), { description = "Close window" })
hl.bind(mainMod .. " + V", hl.dsp.window.float({ action = "toggle" }), { description = "Toggle floating window" })
hl.bind(mainMod .. " + P", hl.dsp.window.pseudo(), { description = "Toggle pseudo-tiling" })
hl.bind(
	mainMod .. " + F",
	hl.dsp.window.fullscreen_state({ internal = 2, client = 2, action = "toggle" }),
	{ description = "Fullscreen" }
)
hl.bind(
	mainMod .. " + SHIFT + F",
	hl.dsp.window.fullscreen_state({ internal = 0, client = 2, action = "toggle" }),
	{ description = "Fake Fullscreen" }
)

-- Power actions (all around SUPER + Escape)
hl.bind(mainMod .. " + SHIFT + Escape", hl.dsp.exit(), { description = "Log out" })
hl.bind(mainMod .. " + CTRL + Escape", hl.dsp.exec_cmd("systemctl reboot"), { description = "Reboot" })
hl.bind(mainMod .. " + ALT + Escape", hl.dsp.exec_cmd("systemctl poweroff"), { description = "Power off" })

-- Reload config
hl.bind(mainMod .. " + R", hl.dsp.exec_cmd("hyprctl reload"), { description = "Reload config" })

-- Move focus
hl.bind(mainMod .. " + H", hl.dsp.focus({ direction = "l" }), { description = "Focus left" })
hl.bind(mainMod .. " + L", hl.dsp.focus({ direction = "r" }), { description = "Focus right" })
hl.bind(mainMod .. " + K", hl.dsp.focus({ direction = "u" }), { description = "Focus up" })
hl.bind(mainMod .. " + J", hl.dsp.focus({ direction = "d" }), { description = "Focus down" })

-- Move window
hl.bind(mainMod .. " + SHIFT + H", hl.dsp.window.move({ direction = "l" }), { description = "Move window left" })
hl.bind(mainMod .. " + SHIFT + L", hl.dsp.window.move({ direction = "r" }), { description = "Move window right" })
hl.bind(mainMod .. " + SHIFT + K", hl.dsp.window.move({ direction = "u" }), { description = "Move window up" })
hl.bind(mainMod .. " + SHIFT + J", hl.dsp.window.move({ direction = "d" }), { description = "Move window down" })

-- Resize window
hl.bind(mainMod .. " + ALT + H", hl.dsp.window.resize({ x = -20, y = 0 }), { description = "Shrink window" })
hl.bind(mainMod .. " + ALT + L", hl.dsp.window.resize({ x = 20, y = 0 }), { description = "Grow window" })
hl.bind(mainMod .. " + ALT + K", hl.dsp.window.resize({ x = 0, y = -20 }), { description = "Lower window" })
hl.bind(mainMod .. " + ALT + J", hl.dsp.window.resize({ x = 0, y = 20 }), { description = "Raise window" })

-- Workspaces
for i = 1, 10 do
	local key = i % 10
	hl.bind(
		mainMod .. " + " .. key,
		hl.dsp.exec_cmd(home .. "/.config/hypr/scripts/workspace-nav.py goto " .. i),
		{ description = "Go to workspace " .. i }
	)
	hl.bind(
		mainMod .. " + SHIFT + " .. key,
		hl.dsp.window.move({ workspace = i }),
		{ description = "Send window to workspace " .. i }
	)
end

-- Navigate workspaces (only those with windows, swap across monitors)
hl.bind(
	mainMod .. " + right",
	hl.dsp.exec_cmd(home .. "/.config/hypr/scripts/workspace-nav.py next"),
	{ description = "Next workspace" }
)
hl.bind(
	mainMod .. " + left",
	hl.dsp.exec_cmd(home .. "/.config/hypr/scripts/workspace-nav.py prev"),
	{ description = "Previous workspace" }
)

-- Special workspace
hl.bind(mainMod .. " + S", hl.dsp.workspace.toggle_special("magic"), { description = "Toggle scratchpad" })
hl.bind(
	mainMod .. " + SHIFT + S",
	hl.dsp.window.move({ workspace = "special:magic" }),
	{ description = "Send window to scratchpad" }
)

-- Mouse scroll workspaces
hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }), { description = "Next workspace (scroll)" })
hl.bind(mainMod .. " + mouse_up", hl.dsp.focus({ workspace = "e-1" }), { description = "Previous workspace (scroll)" })

-- Mouse drag/resize
hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag(), { mouse = true, description = "Drag window" })
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true, description = "Resize window" })

-- Multimedia keys
hl.bind(
	"XF86AudioRaiseVolume",
	hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"),
	{ locked = true, repeating = true, description = "Increase volume" }
)
hl.bind(
	"XF86AudioLowerVolume",
	hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),
	{ locked = true, repeating = true, description = "Decrease volume" }
)
hl.bind(
	"XF86AudioMute",
	hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"),
	{ locked = true, repeating = true, description = "Mute audio" }
)
hl.bind(
	"XF86AudioMicMute",
	hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"),
	{ locked = true, repeating = true, description = "Mute mic" }
)
hl.bind(
	mainMod .. " + PLUS",
	hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"),
	{ locked = true, repeating = true, description = "Increase volume" }
)
hl.bind(
	mainMod .. " + MINUS",
	hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),
	{ locked = true, repeating = true, description = "Decrease volume" }
)
hl.bind(
	"XF86MonBrightnessUp",
	hl.dsp.exec_cmd("brightnessctl set 5%+"),
	{ locked = true, repeating = true, description = "Brightness up" }
)
hl.bind(
	"XF86MonBrightnessDown",
	hl.dsp.exec_cmd("brightnessctl set 5%-"),
	{ locked = true, repeating = true, description = "Brightness down" }
)

-- Playerctl
hl.bind("XF86AudioNext", hl.dsp.exec_cmd("playerctl next"), { locked = true, description = "Next track" })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true, description = "Play/Pause" })
hl.bind("XF86AudioPlay", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true, description = "Play/Pause" })
hl.bind("XF86AudioPrev", hl.dsp.exec_cmd("playerctl previous"), { locked = true, description = "Previous track" })

-- Random wallpaper at startup (sequential with KEY + W)
hl.bind(mainMod .. " + W", function()
	wallpaper.set_next(home .. "/Pictures/Wallpapers")
	hl.exec_cmd("hyprctl reload")
end, { description = "Change wallpaper" })

-- Toggle secondary monitors (keep only DP-3 active)
hl.bind(
	mainMod .. " + X",
	hl.dsp.exec_cmd(home .. "/.config/hypr/scripts/toggle-secondary-monitors.sh"),
	{ description = "Toggle secondary monitors" }
)

-- Show keybindings (SUPER + ?)
hl.bind(
	mainMod .. " + SHIFT + slash",
	hl.dsp.exec_cmd(home .. "/.config/hypr/scripts/show-binds.py"),
	{ description = "Show keybindings (SUPER + ?)" }
)
