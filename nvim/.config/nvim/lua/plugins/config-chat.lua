-- Config help chat: a standalone, read-only opencode popup scoped to the
-- dotfiles repo. Each invocation starts a fresh session (history is still
-- saved and recoverable via <leader>as). Uses the `chat` agent (edit/bash
-- denied) so it can search and read ~/.dotfiles to answer config questions.
return {
  "folke/snacks.nvim",
  opts = {},
  keys = {
    {
      "<leader>ah",
      function()
        local dotfiles = vim.fn.expand("~/.dotfiles")
        require("snacks.terminal").open({ "opencode", dotfiles, "--agent", "chat" }, {
          cwd = dotfiles,
          interactive = true,
          auto_close = true,
          win = {
            position = "float",
            width = 0.85,
            height = 0.85,
            border = "rounded",
            title = " Config Chat (dotfiles · agent: chat) ",
            title_pos = "center",
          },
        })
      end,
      desc = "Config chat (opencode @ dotfiles)",
    },
  },
}
