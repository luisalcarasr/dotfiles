-- Inline AI suggestions (ghost text) backed by the F5AI OpenAI-compatible
-- endpoint. The API key is read from the F5AI_API_KEY environment variable.
return {
  "milanglacier/minuet-ai.nvim",
  event = "InsertEnter",
  opts = {
    provider = "openai_compatible",
    request_timeout = 20,
    provider_options = {
      openai_compatible = {
        api_key = "F5AI_API_KEY",
        end_point = "https://f5ai.pd.f5net.com/openai/v1/chat/completions",
        model = "gpt-5.4-mini",
        name = "F5AI",
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
