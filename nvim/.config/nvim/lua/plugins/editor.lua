return {
  {
    "petertriho/nvim-scrollbar",
    dependencies = {
      { "lewis6991/gitsigns.nvim" },
      { "kevinhwang91/nvim-hlslens", opts = {} },
    },
    opts = {
      hide_if_all_visible = true,
      handlers = {
        gitsigns = true,
      },
    },
  },
  {
    "AckslD/nvim-neoclip.lua",
    dependencies = {
      {
        "kkharji/sqlite.lua",
        module = "sqlite",
      },
    },
    opts = {},
  },
}
