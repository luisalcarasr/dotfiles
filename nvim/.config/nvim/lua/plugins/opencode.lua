-- Detect when nvim is used as a pager / git editor (stdin) so we can skip auto-open.
vim.api.nvim_create_autocmd("StdinReadPre", {
  callback = function()
    vim.g.opencode_read_from_stdin = true
  end,
})

return {
  {
    "nickjvandyke/opencode.nvim",
    version = "*",
    dependencies = {
      {
        "folke/snacks.nvim",
        optional = true,
        opts = {
          input = {}, -- Enhances ask()
          picker = {
            actions = {
              opencode_send = function(...) return require("opencode").snacks_picker_send(...) end,
            },
            win = {
              input = {
                keys = {
                  ["<a-a>"] = { "opencode_send", mode = { "n", "i" } },
                },
              },
            },
          },
        },
      },
    },
    config = function()
      local opencode_cmd = "opencode --port"
      ---@type snacks.terminal.Opts
      local term_opts = {
        win = {
          position = "float",
          border = "rounded",
          width = 0.85,
          height = 0.85,
          enter = true, -- popup: enter on open (quake-style)
        },
      }

      ---@type opencode.Opts
      vim.g.opencode_opts = {
        server = {
          start = function()
            require("snacks.terminal").open(opencode_cmd, term_opts)
          end,
        },
      }

      vim.o.autoread = true -- required for buffer reload after edits

      -- === Core ===
      -- Inline prompt (primary workflow)
      vim.keymap.set({ "n", "x" }, "<leader>ai", function()
        require("opencode").ask("@this: ")
      end, { desc = "Ask opencode (inline)" })

      -- Prompts/commands/server palette
      vim.keymap.set({ "n", "x" }, "<leader>ap", function()
        require("opencode").select()
      end, { desc = "Opencode palette" })

      -- Cycle agent mode (build / plan / ask from opencode.json)
      vim.keymap.set("n", "<leader>am", function()
        require("opencode").command("agent.cycle")
      end, { desc = "Cycle agent/mode" })

      -- === Session control ===
      vim.keymap.set("n", "<leader>as", function()
        require("opencode").command("session.select")
      end, { desc = "Select session (cwd)" })

      vim.keymap.set("n", "<leader>an", function()
        require("opencode").command("session.new")
      end, { desc = "New session" })

      vim.keymap.set("n", "<leader>ax", function()
        require("opencode").command("session.interrupt")
      end, { desc = "Interrupt agent" })

      vim.keymap.set("n", "<leader>au", function()
        require("opencode").command("session.undo")
      end, { desc = "Undo agent action" })

      vim.keymap.set("n", "<leader>ar", function()
        require("opencode").command("session.redo")
      end, { desc = "Redo agent action" })

      vim.keymap.set("n", "<leader>aC", function()
        require("opencode").command("session.compact")
      end, { desc = "Compact session" })

      -- === Built-in prompts (on @this / @diagnostics) ===
      vim.keymap.set({ "n", "x" }, "<leader>ae", function()
        require("opencode").prompt("Explain @this and its context")
      end, { desc = "Explain @this" })

      vim.keymap.set({ "n", "x" }, "<leader>af", function()
        require("opencode").prompt("Fix @diagnostics")
      end, { desc = "Fix diagnostics" })

      vim.keymap.set({ "n", "x" }, "<leader>aR", function()
        require("opencode").prompt("Review @this for correctness and readability")
      end, { desc = "Review @this" })

      vim.keymap.set({ "n", "x" }, "<leader>ao", function()
        require("opencode").prompt("Optimize @this for performance and readability")
      end, { desc = "Optimize @this" })

      vim.keymap.set({ "n", "x" }, "<leader>ad", function()
        require("opencode").prompt("Add comments documenting @this")
      end, { desc = "Document @this" })

      vim.keymap.set({ "n", "x" }, "<leader>at", function()
        require("opencode").prompt("Add tests for @this")
      end, { desc = "Add tests for @this" })

      -- === Server ===
      -- Toggle the opencode popup (no <leader> in terminal mode = no input delay)
      vim.keymap.set({ "n", "t" }, "<C-.>", function()
        require("snacks.terminal").toggle(opencode_cmd, term_opts)
      end, { desc = "Toggle opencode popup" })

      -- === Operator + dot-repeat to add ranges ===
      vim.keymap.set({ "n", "x" }, "go", function()
        return require("opencode").operator("@this ")
      end, { desc = "Add range to opencode", expr = true })
      vim.keymap.set("n", "goo", function()
        return require("opencode").operator("@this ") .. "_"
      end, { desc = "Add line to opencode", expr = true })

      -- === Scroll the panel ===
      vim.keymap.set("n", "<S-C-u>", function()
        require("opencode").command("session.half.page.up")
      end, { desc = "Scroll opencode up" })
      vim.keymap.set("n", "<S-C-d>", function()
        require("opencode").command("session.half.page.down")
      end, { desc = "Scroll opencode down" })

      -- Auto-open the opencode popup on startup (only when nvim is opened with no args)
      vim.api.nvim_create_autocmd("User", {
        pattern = "VeryLazy",
        callback = function()
          local no_file_args = vim.fn.argc() == 0
          local no_stdin = not vim.g.opencode_read_from_stdin
          if no_file_args and no_stdin then
            require("snacks.terminal").open(opencode_cmd, term_opts)
          end
        end,
      })
    end,
  },
}
