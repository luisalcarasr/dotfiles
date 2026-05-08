return {
  "projekt0n/github-nvim-theme",
  lazy = false,
  priority = 1000,
  config = function()
    require("github-theme").setup({
      options = {
        transparent = false,
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
}
