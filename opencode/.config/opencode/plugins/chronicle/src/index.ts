// ---------------------------------------------------------------------------
// Chronicle — OpenCode plugin
//
// Registers a `chronicle` tool the orchestrator can call on demand to retrieve
// context from past sessions in the current working directory (and its
// descendants). Never runs automatically — fully lazy.
// ---------------------------------------------------------------------------

import type { Plugin, PluginInput } from "@opencode-ai/plugin";
import { tool } from "@opencode-ai/plugin";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { join, dirname } from "path";
import { synthesize } from "./synthesizer.ts";
import type { ChronicleConfig } from "./synthesizer.ts";

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const CONFIG_PATH = join(__dirname, "..", "chronicle.json");

function loadConfig(): ChronicleConfig {
  const raw = readFileSync(CONFIG_PATH, "utf-8");
  return JSON.parse(raw) as ChronicleConfig;
}

const CONFIG = loadConfig();

// ---------------------------------------------------------------------------
// Subagent session tracking — do not inject hint into chronicle subagents
// ---------------------------------------------------------------------------

const chronicleSubagents = new Set<string>();

// ---------------------------------------------------------------------------
// System prompt hint — tells the orchestrator when to call chronicle
// ---------------------------------------------------------------------------

const CHRONICLE_HINT = `## Chronicle — Session History Tool

chronicle(query, limit?, since?, until?) retrieves context from past work sessions in the current directory and its subdirectories.

Call chronicle when the user:
- References previous work ("continue", "like last time", "last session", "where did we leave off")
- Asks what was done before ("what did we do with X?", "have we already done Y?")
- Mentions a specific date or time range ("on Monday", "last week", "June 17th", "yesterday", "3 days ago")
- Uses implicit continuity that requires historical context ("the plugin", "that bug", "the config we changed")
- Asks for a summary of past work in this project

Parameters:
- query (required): what to search for — topic, file name, feature name, or task description
- since (optional): start date filter — ISO "YYYY-MM-DD" or natural language ("yesterday", "last week", "N days ago", "june 17")
- until (optional): end date filter — same format as since
- limit (optional): override the default number of sessions to search (default: ${CONFIG.maxSessions})

chronicle searches only sessions run in the current directory or its subdirectories.
Do NOT call chronicle proactively — only call it when the user's message implies a need for historical context.\`;

// ---------------------------------------------------------------------------
// Plugin
// ---------------------------------------------------------------------------

const ChroniclePlugin: Plugin = async (ctx: PluginInput) => {
  if (!CONFIG.enabled) {
    return {};
  }

  const client = ctx.client;

  return {
    // -------------------------------------------------------------------------
    // Tool: chronicle
    // -------------------------------------------------------------------------
    tool: {
      chronicle: tool({
        description:
          "Retrieve context from past work sessions in the current directory and its subdirectories. " +
          "Call when the user references previous work, asks to continue something, or mentions a date. " +
          "Do NOT call proactively.",
        args: {
          query: tool.schema
            .string()
            .describe("What to search for in past sessions — topic, file, feature, or task description."),
          limit: tool.schema
            .number()
            .optional()
            .describe(`Max number of sessions to search. Default: ${CONFIG.maxSessions}.`),
          since: tool.schema
            .string()
            .optional()
            .describe('Start date filter. ISO format "YYYY-MM-DD" or natural language: "yesterday", "last week", "3 days ago", "june 17".'),
          until: tool.schema
            .string()
            .optional()
            .describe('End date filter. Same format as since.'),
        },

        async execute({ query, limit, since, until }): Promise<string> {
          // Resolve cwd from the current session
          let cwd: string;
          try {
            const sessions: any = await client.session.list({});
            const allSessions: any[] = sessions?.data ?? [];
            // The most recently created session that is not a subagent is the caller
            const orchestrator = allSessions
              .filter((s: any) => !s.parent_id && !s.parentID)
              .sort((a: any, b: any) => {
                const ta = a.time_updated ?? a.timeUpdated ?? 0;
                const tb = b.time_updated ?? b.timeUpdated ?? 0;
                return tb - ta;
              })[0];

            cwd = orchestrator?.directory ?? process.cwd();
          } catch {
            cwd = process.cwd();
          }

          try {
            const result = await synthesize(client, CONFIG, cwd, {
              query,
              limit,
              since,
              until,
            });
            return result;
          } catch (err: any) {
            return `[chronicle] Error: ${err?.message ?? "unknown error"}`;
          }
        },
      }),
    },

    // -------------------------------------------------------------------------
    // Track chronicle subagent sessions — skip hint injection for them
    // -------------------------------------------------------------------------
    "chat.message": async (input: any, _output: any) => {
      const sid: string | undefined = input?.sessionID;
      const agent: string | undefined = input?.agent;
      const parentID: string | undefined = input?.parentID;

      if (!sid) return;
      if (parentID || agent === "chronicle") {
        chronicleSubagents.add(sid);
      }
    },

    // -------------------------------------------------------------------------
    // Inject hint into orchestrator system prompt only
    // -------------------------------------------------------------------------
    "experimental.chat.system.transform": async (input: any, output: any) => {
      const sessionID: string | undefined = input?.sessionID;
      if (sessionID && chronicleSubagents.has(sessionID)) return;
      output.system.push(CHRONICLE_HINT);
    },
  };
};

export default ChroniclePlugin;
