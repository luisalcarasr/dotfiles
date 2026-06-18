import type { Plugin, PluginInput } from "@opencode-ai/plugin";
import { tool } from "@opencode-ai/plugin";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { join, dirname } from "path";

// ---------------------------------------------------------------------------
// Config paths — relative to this file, resolved at load time
// ---------------------------------------------------------------------------

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// switchboard.json lives in the opencode config dir (two levels up from src/)
// prompts/ lives alongside the plugin source
const CONFIG_DIR = join(__dirname, "..", "..", "..");

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface PresetTier {
  primary: string;
  fallback: string[];
}

interface TierMeta {
  description: string;
  steps: number;
  whenToUse: string[];
}

interface TiersConfig {
  activePreset: string;
  activeMode: string;
  tierCaps: Record<string, number>;
  tiers: Record<string, TierMeta>;
  presets: Record<string, Record<string, PresetTier>>;
  taskPatterns: Record<string, string>;
  modes: Record<string, { defaultTier: string; description: string; overrideRules?: string[] }>;
  rules: string[];
  defaultTier: string;
}

interface TierConfig {
  primary: string;
  fallback: string[];
  description: string;
  steps: number;
  whenToUse: string[];
  prompt: string;
}

// ---------------------------------------------------------------------------
// Loader — reads tiers.json and prompts/*.md at startup
// ---------------------------------------------------------------------------

function loadConfig(): { tiers: Record<string, TierConfig>; config: TiersConfig } {
  const raw = readFileSync(join(CONFIG_DIR, "switchboard.json"), "utf-8");
  const cfg: TiersConfig = JSON.parse(raw);

  const preset = cfg.presets[cfg.activePreset];
  if (!preset) {
    throw new Error(`[switchboard] unknown preset "${cfg.activePreset}" in switchboard.json`);
  }

  const tiers: Record<string, TierConfig> = {};

  for (const [name, meta] of Object.entries(cfg.tiers)) {
    const models = preset[name];
    if (!models) {
      throw new Error(`[switchboard] tier "${name}" missing in preset "${cfg.activePreset}"`);
    }

    const promptPath = join(__dirname, "..", "prompts", `${name}.md`);
    let prompt: string;
    try {
      prompt = readFileSync(promptPath, "utf-8").trim();
    } catch {
      throw new Error(`[switchboard] prompt file not found: ${promptPath}`);
    }

    tiers[name] = {
      primary: models.primary,
      fallback: models.fallback,
      description: meta.description,
      steps: meta.steps,
      whenToUse: meta.whenToUse,
      prompt,
    };
  }

  return { tiers, config: cfg };
}

const { tiers: TIERS, config: CFG } = loadConfig();

// Orchestrator model — read from the active preset's medium tier (primary)
const ORCHESTRATOR_MODEL = CFG.presets[CFG.activePreset]?.["medium"]?.primary ?? "unknown";

// ---------------------------------------------------------------------------
// Routing rules — injected into orchestrator system prompt every message
// ---------------------------------------------------------------------------

function buildDelegationProtocol(): string {
  const orchModel = ORCHESTRATOR_MODEL.split("/").pop();

  const routeLines = Object.entries(CFG.taskPatterns).map(
    ([tier, patterns]) => `${patterns} → delegate(tier="${tier}")`,
  );

  const modeNote = CFG.activeMode !== "normal"
    ? `\nACTIVE MODE: ${CFG.activeMode} — ${CFG.modes[CFG.activeMode]?.description ?? ""}`
    : "";

  const modeRules = CFG.activeMode !== "normal"
    ? (CFG.modes[CFG.activeMode]?.overrideRules ?? []).map((r, i) => `${i + 1}. ${r}`)
    : [];

  return [
    "## Delegation Protocol",
    "",
    `Orchestrator: ${orchModel}. You coordinate — subagents execute. Information-gathering IS execution: dispatch it, don't do it yourself.`,
    modeNote,
    "",
    "ROUTE (match the user request to the closest row, pick the fastest tier that fits):",
    ...routeLines,
    "",
    "RULES:",
    ...CFG.rules.map((r, i) => `${i + 1}. ${r}`),
    ...(modeRules.length > 0 ? ["", "MODE OVERRIDES:", ...modeRules] : []),
    "",
    "delegate(tier, prompt) runs the tier's primary model, falls back automatically on failure, and reports which model executed. Pass the subagent everything it needs in `prompt` — it does not see this conversation.",
  ]
    .filter((line) => line !== undefined)
    .join("\n");
}

// ---------------------------------------------------------------------------
// Subagent session tracking — prevents protocol injection into subagents
// ---------------------------------------------------------------------------

const subagentSessions = new Set<string>();

// ---------------------------------------------------------------------------
// Delegation helpers
// ---------------------------------------------------------------------------

const modelName = (m: string): string => m.split("/").pop() ?? m;

function extractText(res: any): string {
  const parts: any[] = res?.data?.parts ?? [];
  return parts
    .filter((p) => p?.type === "text" && typeof p.text === "string")
    .map((p) => p.text)
    .join("\n")
    .trim();
}

async function runModel(
  client: any,
  model: string,
  tier: string,
  prompt: string,
): Promise<string> {
  const created: any = await client.session.create({});
  const sid: string | undefined = created?.data?.id;
  if (!sid) throw new Error("session.create returned no id");

  const res: any = await client.session.prompt({
    path: { id: sid },
    body: {
      model,
      agent: tier,
      parts: [{ type: "text", text: prompt }],
    },
  });
  return extractText(res);
}

// ---------------------------------------------------------------------------
// Plugin — single delegate tool, zero commands, zero mutable config
// ---------------------------------------------------------------------------

const SwitchboardPlugin: Plugin = async (ctx: PluginInput) => {
  const client = ctx.client;

  const tierList = Object.keys(TIERS).join(", ");

  return {
    tool: {
      delegate: tool({
        description:
          `Delegate a task to a tier subagent. Runs the tier's primary model; on failure, automatically falls back through the tier's model chain. Always reports which model executed. The subagent does NOT see this conversation — pass everything it needs in \`prompt\`. Tiers: ${tierList}.`,
        args: {
          tier: tool.schema
            .string()
            .describe(`One of: ${tierList}`),
          prompt: tool.schema
            .string()
            .describe("The complete, self-contained task for the subagent."),
        },
        async execute({ tier, prompt }): Promise<string> {
          const cfg = TIERS[tier];
          if (!cfg) {
            return `[✗ unknown tier "${tier}" — valid: ${tierList}]`;
          }

          const chain = [cfg.primary, ...cfg.fallback];
          const failures: string[] = [];

          for (let i = 0; i < chain.length; i++) {
            const model = chain[i]!;
            try {
              const text = await runModel(client, model, tier, prompt);
              const header =
                i === 0
                  ? `[✓ @${tier} → ${modelName(model)}]`
                  : `[✗ @${tier} primary failed: ${failures.join("; ")}]\n[✓ @${tier} → ${modelName(model)} (fallback #${i})]`;
              return `${header}\n\n${text}`;
            } catch (err: any) {
              failures.push(`${modelName(model)}: ${err?.message ?? "error"}`);
            }
          }

          return `[✗ @${tier} — all ${chain.length} models exhausted]\n${failures.map((f) => `  - ${f}`).join("\n")}`;
        },
      }),
    },

    // Register all tier agents at load time
    config: async (opencodeConfig: any) => {
      opencodeConfig.agent ??= {};

      for (const [name, tier] of Object.entries(TIERS)) {
        opencodeConfig.agent[name] = {
          model: tier.primary,
          mode: "subagent",
          description: tier.description,
          maxSteps: tier.steps,
          prompt: tier.prompt,
        };
      }
    },

    // Track subagent sessions — protocol must NOT be injected into them
    "chat.message": async (input: any, _output: any) => {
      const sid: string | undefined = input?.sessionID;
      const parentID: string | undefined = input?.parentID;
      const agent: string | undefined = input?.agent;
      const tierNames = Object.keys(TIERS);

      if (!sid) return;
      if (parentID || (agent && tierNames.includes(agent))) {
        subagentSessions.add(sid);
      }
    },

    // Inject delegation protocol into orchestrator system prompt only
    "experimental.chat.system.transform": async (input: any, output: any) => {
      const sessionID: string | undefined = input?.sessionID;
      if (sessionID && subagentSessions.has(sessionID)) return;
      output.system.push(buildDelegationProtocol());
    },
  };
};

export default SwitchboardPlugin;
