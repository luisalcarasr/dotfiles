-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

local key = vim.keymap
local groups = require("which-key")

groups.register({
  ["<leader>"] = {
    t = { name = "terminal" }, -- Terminal
    h = { name = "clipboard history" }, -- Clipboard History
  },
})

-- Terminal

key.set("n", "<leader>tt", "<cmd>TermSelect<cr>", { desc = "Select terminal", silent = true, noremap = true })
key.set("n", "<leader>tr", "<cmd>ToggleTermSetName<cr>", { desc = "Rename terminal", silent = true, noremap = true })
key.set("n", "<leader>to", "<cmd>ToggleTerm<cr>", { desc = "Open terminal", silent = true, noremap = true })
key.set("t", "<c-t>", "<cmd>ToggleTerm<cr>", { desc = "Toggle terminal", silent = true, noremap = true })
key.set("n", "<c-t>", function()
  vim.cmd(vim.v.count .. "ToggleTerm")
end, { desc = "Toggle terminal", silent = true, noremap = true })

-- Clipboard History

key.set(
  "n",
  "<leader>hc",
  "<cmd>Telescope neoclip initial_mode=normal<cr>",
  { desc = "Clipboard history", silent = true, noremap = true }
)
