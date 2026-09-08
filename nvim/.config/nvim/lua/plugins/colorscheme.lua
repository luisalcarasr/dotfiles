return {
  "projekt0n/github-nvim-theme",
  lazy = false,
  priority = 1000,
  config = function()
    require("github-theme").setup({
      options = {
        transparent = true,
        hide_end_of_buffer = true,
        hide_nc_statusline = true,
        darken = {
          floats = false,
          sidebars = {
            enable = true,
            list = {},
          },
        },
      },
    })
    vim.cmd("colorscheme github_dark_default")
  end,
  -- Keep every window group transparent so the terminal opacity + blur shine
  -- through (kitty does background_blur + background_opacity).
  init = function()
    local transparent_groups = {
      "Normal",
      "NormalFloat",
      "NormalNC",
      "SignColumn",
      "SignColumnNC",
      "LineNr",
      "CursorLineNr",
      "FoldColumn",
      "StatusLine",
      "StatusLineNC",
      "TabLine",
      "TabLineFill",
      "TabLineSel",
      "WinSeparator",
      "FloatBorder",
      "FloatTitle",
      "FloatFooter",
      "Pmenu",
      "PmenuSel",
      "PmenuSbar",
      "PmenuThumb",
      "CursorLine",
      "CursorLineSign",
      "CursorLineNr",
      "MsgsSeparator",
    }
    vim.api.nvim_create_autocmd("ColorScheme", {
      callback = function()
        for _, group in ipairs(transparent_groups) do
          local ok, hl = pcall(vim.api.nvim_get_hl, 0, { name = group })
          if ok and hl then
            vim.api.nvim_set_hl(0, group, vim.tbl_extend("force", hl, { bg = "none" }))
          end
        end
      end,
    })
  end,
}