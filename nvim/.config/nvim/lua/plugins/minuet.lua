-- Inline AI suggestions (ghost text) backed by a local Ollama
-- OpenAI-compatible endpoint (no API key required).
return {
  "milanglacier/minuet-ai.nvim",
  event = "InsertEnter",
  opts = {
    provider = "openai_compatible",
    request_timeout = 20,
    provider_options = {
      openai_compatible = {
        api_key = "ollama",
        end_point = "http://localhost:11434/v1/chat/completions",
        model = "codellama",
        name = "Ollama",
      },
    },
    virtualtext = {
      auto_trigger_ft = { "*" },
      keymap = {
        accept = "<C-g>",
        accept_line = "<C-l>",
        next = "<C-]>",
        prev = "<C-p>",
        dismiss = "<C-e>",
      },
    },
  },
}