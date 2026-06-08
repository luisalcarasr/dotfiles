return {
  {
    "olimorris/codecompanion.nvim",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "nvim-treesitter/nvim-treesitter",
    },
    cmd = {
      "CodeCompanion",
      "CodeCompanionChat",
      "CodeCompanionActions",
      "CodeCompanionCmd",
    },
    keys = {
      { "<C-a>", "<cmd>CodeCompanionActions<cr>", mode = { "n", "v" }, desc = "CodeCompanion actions" },
      { "<leader>aa", "<cmd>CodeCompanionChat Toggle<cr>", mode = { "n", "v" }, desc = "Toggle CodeCompanion chat" },
      { "<leader>ai", "<cmd>CodeCompanion<cr>", mode = { "n", "v" }, desc = "Inline CodeCompanion prompt" },
      { "ga", "<cmd>CodeCompanionChat Add<cr>", mode = "v", desc = "Add selection to CodeCompanion chat" },
    },
    opts = {
      adapters = {
        http = {
          f5ai = function()
            return require("codecompanion.adapters").extend("openai_compatible", {
              name = "f5ai",
              formatted_name = "F5 AI",
              env = {
                url = "https://f5ai.pd.f5net.com",
                api_key = "F5AI_API_KEY",
                chat_url = "/openai/v1/chat/completions",
                models_endpoint = "/openai/v1/models",
              },
              schema = {
                model = {
                  default = "claude-opus-4-8",
                },
              },
            })
          end,
        },
      },
      strategies = {
        chat = {
          adapter = "f5ai",
        },
        inline = {
          adapter = "f5ai",
        },
        cmd = {
          adapter = "f5ai",
        },
      },
    },
  },
}
