---
description: Sync F5 Inc provider models in opencode.json with the live API catalog
agent: build
---

Synchronize the `provider.f5ai.models` section in `~/.config/opencode/opencode.json` with the live F5 Inc API catalog. Do this **without asking for confirmation** — apply all changes and report a summary at the end.

## Steps

### 1. Fetch the live catalog

Run the following shell command and parse the JSON response:

!`curl -s -H "Authorization: Bearer $F5AI_API_KEY" https://f5ai.pd.f5net.com/openai/v1/models`

If `F5AI_API_KEY` is not set or the request fails (non-200, empty body, or malformed JSON), **abort immediately** and report the error. Do not modify any file.

### 2. Read the current config

Read `~/.config/opencode/opencode.json`. Extract:

- `provider.f5ai.models` — the current model registry (object keyed by model id).
- `agent` — the agent-to-model assignments, to detect orphans after deletion.

### 3. Compute the diff

Build two sets:

- **To add**: model ids present in the API response but absent from `provider.f5ai.models`.
- **To remove**: model ids present in `provider.f5ai.models` but absent from the API response.

### 4. Generate display names for new models

For each model id to add, derive a human-readable `name` using this rule:

- Split the id on `-`, `.`, and `_`.
- Capitalise each segment.
- Examples:
  - `gemini-2.5-flash` → `"Gemini 2.5 Flash"`
  - `gpt-5-nano` → `"GPT 5 Nano"` (keep "GPT" all-caps)
  - `claude-sonnet-4-6` → `"Claude Sonnet 4.6"` (restore `.` between version digits)
  - `DeepSeek-V4-Flash` → `"DeepSeek V4 Flash"` (preserve original casing if the id uses it)
  - `Kimi-K2.5` → `"Kimi K2.5"`
  - `dall-e-3` → `"DALL-E 3"` (keep known abbreviations)
  - `o3-mini` → `"O3 Mini"`

Apply the same capitalisation conventions used by existing entries in `provider.f5ai.models`.

### 5. Detect and reasign orphaned agents

After computing the removal list, check every value in the `agent` section. If an agent's `model` field contains a `f5ai/<id>` where `<id>` is in the removal list, automatically reasign it to the closest available successor:

- Prefer a model from the same family and tier (e.g. if `claude-opus-4-6` is removed, try the next `claude-opus-*` version).
- If no successor exists in the same family, fall back to the current default model (`model` at root level).
- Record every reasignment for the final report.

### 6. Apply all changes atomically

Edit `~/.config/opencode/opencode.json` in a single operation:

- Add new model entries to `provider.f5ai.models`, preserving the existing multi-line JSON style (each model on its own `"id": { "name": "..." }` block, indented with 8 spaces).
- Remove obsolete model entries from `provider.f5ai.models`.
- Update any orphaned agent `model` fields with the reasigned value.

Do not touch any other section of the file.

### 7. Verify

1. Run `python3 -m json.tool ~/.config/opencode/opencode.json > /dev/null` and confirm it exits with 0. If JSON is invalid, restore the original file and report the error.
2. Re-run the diff (step 3) against the updated file and confirm both sets are empty.

### 8. Report

Print a concise summary:

```
✅ Sync complete
  Added   (N): model-id-1, model-id-2, ...
  Removed (N): model-id-3, ...
  Agents reasigned (N): agent-name: old-model → new-model, ...
  No changes (if nothing changed)
```

If arguments are provided, treat them as extra instructions:

`$ARGUMENTS`
