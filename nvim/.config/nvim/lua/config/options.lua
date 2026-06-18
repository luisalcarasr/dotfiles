-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

-- Python host for the molten-nvim remote plugin. Uses a dedicated venv inside
-- the nvim config dir (~/.config/nvim/.venv), provisioned from requirements.txt
-- by macos.sh. Falls back to the default host if the venv is absent.
local nvim_venv = vim.fn.stdpath("config") .. "/.venv"
local nvim_python = nvim_venv .. "/bin/python"
if vim.fn.executable(nvim_python) == 1 then
  vim.g.python3_host_prog = nvim_python
  -- Put the venv's bin on PATH so CLI tools shelled out by plugins are found:
  -- jupytext.nvim invokes bare `jupytext`, molten needs `jupyter`, etc.
  vim.env.PATH = nvim_venv .. "/bin:" .. vim.env.PATH
end
