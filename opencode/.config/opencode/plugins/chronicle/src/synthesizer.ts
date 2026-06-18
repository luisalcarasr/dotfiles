// ---------------------------------------------------------------------------
// Chronicle — synthesizer: runs haiku subagent to extract context
// ---------------------------------------------------------------------------

import { buildSynthesizerPrompt, buildMiniSynthesisPrompt } from "./prompt.ts";
import { buildTranscript, filterSessions, parseDate } from "./loader.ts";
import type { CompactionConfig } from "./loader.ts";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface ChronicleConfig {
  model: string;
  fallbackModel: string;
  maxSessions: number;
  enabled: boolean;
  compaction: CompactionConfig;
}

export interface ChronicleQuery {
  query: string;
  limit?: number;
  since?: string;
  until?: string;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function extractText(res: any): string {
  const parts: any[] = res?.data?.parts ?? [];
  return parts
    .filter((p: any) => p?.type === "text" && typeof p.text === "string")
    .map((p: any) => p.text)
    .join("\n")
    .trim();
}

/** Split "providerID/modelID" string into the object the SDK expects. */
function parseModel(model: string): { providerID: string; modelID: string } {
  const slashIdx = model.indexOf("/");
  if (slashIdx === -1) return { providerID: model, modelID: model };
  return {
    providerID: model.slice(0, slashIdx),
    modelID: model.slice(slashIdx + 1),
  };
}

async function callModel(
  client: any,
  model: string,
  prompt: string,
): Promise<string> {
  // session.create requires body: {}
  const created: any = await client.session.create({ body: {} });
  const sid: string | undefined = created?.data?.id;
  if (!sid) throw new Error("session.create returned no id");

  const res: any = await client.session.prompt({
    path: { id: sid },
    body: {
      model: parseModel(model),
      agent: "chronicle",
      parts: [{ type: "text", text: prompt }],
    },
  });

  return extractText(res);
}

async function callModelWithFallback(
  client: any,
  primary: string,
  fallback: string,
  prompt: string,
): Promise<string> {
  try {
    return await callModel(client, primary, prompt);
  } catch (err: any) {
    try {
      return await callModel(client, fallback, prompt);
    } catch (err2: any) {
      throw new Error(
        `Both models failed. Primary (${primary}): ${err?.message ?? "error"}. Fallback (${fallback}): ${err2?.message ?? "error"}`,
      );
    }
  }
}

// ---------------------------------------------------------------------------
// Capa 3: Mini-synthesis for oversized individual sessions
// ---------------------------------------------------------------------------

async function miniSynthesize(
  client: any,
  cfg: ChronicleConfig,
  rawTranscript: string,
  meta: { title: string; date: string; directory: string },
): Promise<string> {
  const prompt = buildMiniSynthesisPrompt(
    meta.title,
    meta.date,
    meta.directory,
    rawTranscript,
  );
  return callModelWithFallback(client, cfg.model, cfg.fallbackModel, prompt);
}

// ---------------------------------------------------------------------------
// Main synthesizer
// ---------------------------------------------------------------------------

export async function synthesize(
  client: any,
  cfg: ChronicleConfig,
  cwd: string,
  params: ChronicleQuery,
): Promise<string> {
  // 1. Load all sessions from the SDK
  const allSessionsRes: any = await client.session.list();
  const allSessions: any[] = allSessionsRes?.data ?? [];

  if (allSessions.length === 0) {
    return "No past sessions found.";
  }

  // 2. Parse date filters
  const sinceTs = params.since ? parseDate(params.since) : null;
  const untilTs = params.until ? parseDate(params.until) : null;

  // 3. Filter by directory (current + descendants) and date range
  const filtered = filterSessions(allSessions, cwd, sinceTs, untilTs);

  if (filtered.length === 0) {
    const dateHint = params.since ? ` since "${params.since}"` : "";
    return `No sessions found in ${cwd} or its subdirectories${dateHint}.`;
  }

  // 4. Sort newest first, take limit
  const limit = params.limit ?? cfg.maxSessions;
  const selected = filtered
    .sort((a: any, b: any) => {
      const ta = a.time_created ?? a.timeCreated ?? 0;
      const tb = b.time_created ?? b.timeCreated ?? 0;
      return tb - ta;
    })
    .slice(0, limit);

  // 5. Load messages + parts for each session via session.messages()
  //    Returns: { info: Message, parts: Part[] }[]
  const transcripts: string[] = [];

  for (const session of selected) {
    const sessionId: string = session.id;
    const meta = {
      id: sessionId,
      title: session.title ?? "(untitled)",
      directory: session.directory ?? cwd,
      timeCreated: session.time_created ?? session.timeCreated ?? 0,
    };

    // Use the correct SDK method: session.messages returns { info, parts }[]
    const messagesRes: any = await client.session.messages({
      path: { id: sessionId },
    }).catch(() => ({ data: [] }));

    const entries: any[] = messagesRes?.data ?? [];

    if (entries.length === 0) continue;

    // Adapt to the format buildTranscript expects:
    // messages: Message[], allParts: Map<messageId, Part[]>
    const messages: any[] = entries.map((e: any) => e.info ?? e);
    const allParts = new Map<string, any[]>();
    for (const entry of entries) {
      const msgId: string = (entry.info ?? entry)?.id;
      if (msgId) {
        allParts.set(msgId, entry.parts ?? []);
      }
    }

    // Capa 1 + 2: compact the transcript
    const { transcript, estimatedTokens } = buildTranscript(
      meta,
      messages,
      allParts,
      cfg.compaction,
    );

    // Capa 3: mini-synthesis if still too large
    if (
      cfg.compaction.miniSynthesisEnabled &&
      estimatedTokens > cfg.compaction.miniSynthesisThreshold
    ) {
      try {
        const miniSummary = await miniSynthesize(client, cfg, transcript, {
          title: meta.title,
          date: new Date(meta.timeCreated).toISOString().slice(0, 10),
          directory: meta.directory,
        });
        transcripts.push(
          `SESSION: ${meta.id} | Title: ${meta.title} | Date: ${new Date(meta.timeCreated).toISOString().slice(0, 10)} | Directory: ${meta.directory}\n\n[Pre-compacted summary]\n${miniSummary}`,
        );
      } catch {
        // If mini-synthesis fails, fall back to the already compacted transcript
        transcripts.push(transcript);
      }
    } else {
      transcripts.push(transcript);
    }
  }

  if (transcripts.length === 0) {
    return "Sessions were found but contained no readable content.";
  }

  // 6. Run global synthesizer subagent
  const synthPrompt = buildSynthesizerPrompt(params.query, cwd, transcripts);

  try {
    return await callModelWithFallback(client, cfg.model, cfg.fallbackModel, synthPrompt);
  } catch (err: any) {
    return `[chronicle] Synthesis failed: ${err?.message ?? "unknown error"}. Found ${transcripts.length} session(s) but could not summarize them.`;
  }
}
