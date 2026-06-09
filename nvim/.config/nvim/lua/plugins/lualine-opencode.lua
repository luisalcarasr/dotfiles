-- Show the opencode agent status (idle / responding) in the statusline.
-- Non-invasive: extends LazyVim's lualine spec instead of replacing it.
return {
  "nvim-lualine/lualine.nvim",
  optional = true,
  opts = function(_, opts)
    opts.sections = opts.sections or {}
    opts.sections.lualine_x = opts.sections.lualine_x or {}
    table.insert(opts.sections.lualine_x, 1, {
      require("opencode").statusline,
      cond = function()
        return package.loaded["opencode"] ~= nil
      end,
    })
  end,
}
