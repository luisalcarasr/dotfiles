-- Jupyter notebook support for Neovim (macOS Apple Silicon + kitty).
--
-- Stack:
--   * jupytext.nvim  - open .ipynb files as editable quarto/markdown text
--   * molten-nvim    - run code in a live Jupyter kernel, inline output
--   * image.nvim     - render plots inline via the kitty graphics protocol
--   * quarto-nvim    - cell orchestration (run cell/above/below), drives molten
--   * otter.nvim     - LSP (completion/hover/diagnostics) inside code cells
--
-- Requirements (provisioned by macos.sh): a Python venv at ~/.config/nvim/.venv
-- with pynvim/jupyter_client/jupytext/ipykernel/nbformat, `brew install
-- imagemagick`, and DYLD_FALLBACK_LIBRARY_PATH set in fish. The Python host is
-- wired in lua/config/options.lua. Run `:UpdateRemotePlugins` after install.
return {
  -- Inline image rendering (plots) through the kitty graphics protocol.
  {
    "3rd/image.nvim",
    -- build = false avoids the fragile `magick` luarock on Apple Silicon.
    build = false,
    opts = {
      backend = "kitty",
      processor = "magick_cli", -- shells out to ImageMagick; no luarock needed
      integrations = {
        markdown = {
          enabled = true,
          only_render_image_at_cursor = true,
          filetypes = { "markdown", "vimwiki", "quarto" },
        },
      },
      max_width = 100,
      max_height = 12,
      max_height_window_percentage = math.huge,
      max_width_window_percentage = math.huge,
      window_overlap_clear_enabled = true,
    },
  },

  -- Open .ipynb as plaintext (quarto) so quarto/otter/molten can operate on it.
  {
    "GCBallesteros/jupytext.nvim",
    lazy = false, -- must NOT be lazy or .ipynb opens as raw JSON
    opts = {
      style = "quarto",
      output_extension = "qmd",
      force_ft = "quarto",
    },
  },

  -- Live Jupyter kernel interaction (remote plugin).
  {
    "benlubas/molten-nvim",
    version = "^1.0.0",
    dependencies = { "3rd/image.nvim" },
    build = ":UpdateRemotePlugins",
    init = function()
      vim.g.molten_image_provider = "image.nvim"
      vim.g.molten_output_win_max_height = 20
      vim.g.molten_auto_open_output = false
      vim.g.molten_wrap_output = true
      vim.g.molten_virt_text_output = true
      vim.g.molten_virt_lines_off_by_1 = true
    end,
    keys = {
      { "<leader>ji", "<cmd>MoltenInit<cr>", desc = "Initialize kernel" },
      { "<leader>je", "<cmd>MoltenEvaluateOperator<cr>", desc = "Evaluate operator" },
      { "<leader>jl", "<cmd>MoltenEvaluateLine<cr>", desc = "Evaluate line" },
      { "<leader>jc", "<cmd>MoltenReevaluateCell<cr>", desc = "Re-evaluate cell" },
      { "<leader>je", ":<C-u>MoltenEvaluateVisual<cr>gv", mode = "v", desc = "Evaluate selection" },
      { "<leader>jd", "<cmd>MoltenDelete<cr>", desc = "Delete cell" },
      { "<leader>jo", "<cmd>MoltenShowOutput<cr>", desc = "Show output" },
      { "<leader>jh", "<cmd>MoltenHideOutput<cr>", desc = "Hide output" },
      { "<leader>jx", "<cmd>MoltenInterrupt<cr>", desc = "Interrupt kernel" },
      { "<leader>jr", "<cmd>MoltenRestart<cr>", desc = "Restart kernel" },
      { "<leader>jb", "<cmd>MoltenImportOutput<cr>", desc = "Import .ipynb output" },
      { "<leader>js", "<cmd>MoltenExportOutput<cr>", desc = "Export output to .ipynb" },
    },
  },

  -- Quarto literate-programming workflow + in-cell LSP via otter.
  {
    "quarto-dev/quarto-nvim",
    ft = { "quarto", "markdown" },
    dependencies = {
      "jmbuhr/otter.nvim",
      "nvim-treesitter/nvim-treesitter",
    },
    opts = {
      lspFeatures = {
        enabled = true,
        languages = { "python" },
        chunks = "all",
        diagnostics = { enabled = true, triggers = { "BufWritePost" } },
        completion = { enabled = true },
      },
      codeRunner = {
        enabled = true,
        default_method = "molten",
        ft_runners = { python = "molten" },
      },
    },
    keys = {
      { "<leader>jp", "<cmd>QuartoPreview<cr>", desc = "Quarto preview" },
      {
        "<leader>jR",
        function()
          require("quarto.runner").run_above()
        end,
        desc = "Run cells above",
        ft = { "quarto", "markdown" },
      },
      {
        "<leader>ja",
        function()
          require("quarto.runner").run_all()
        end,
        desc = "Run all cells",
        ft = { "quarto", "markdown" },
      },
    },
  },

  -- Ensure parsers needed by otter/quarto are installed.
  {
    "nvim-treesitter/nvim-treesitter",
    opts = function(_, opts)
      opts.ensure_installed = opts.ensure_installed or {}
      vim.list_extend(opts.ensure_installed, { "markdown", "markdown_inline", "python" })
    end,
  },
}
