// ---------------------------------------------------------------------------
// Chronicle — session loader and compactor
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface CompactionConfig {
  maxTokensPerSession: number;
  windowRatio: { start: number; end: number };
  maxToolOutputChars: number;
  maxMessagesPerSession: number;
  miniSynthesisThreshold: number;
  miniSynthesisEnabled: boolean;
}

export interface SessionMeta {
  id: string;
  title: string;
  directory: string;
  timeCreated: number;
}

export interface LoadedSession {
  meta: SessionMeta;
  transcript: string;
  estimatedTokens: number;
}

// ---------------------------------------------------------------------------
// Date parsing — no external dependencies
// ---------------------------------------------------------------------------

export function parseDate(input: string): number | null {
  const s = input.trim().toLowerCase();
  const now = Date.now();
  const day = 86_400_000;

  if (s === "today") return new Date().setHours(0, 0, 0, 0);
  if (s === "yesterday") return now - day;
  if (s === "last week" || s === "a week ago") return now - 7 * day;
  if (s === "last month" || s === "a month ago") return now - 30 * day;

  const daysAgo = s.match(/^(\d+)\s+days?\s+ago$/);
  if (daysAgo) return now - parseInt(daysAgo[1]!, 10) * day;

  const weeksAgo = s.match(/^(\d+)\s+weeks?\s+ago$/);
  if (weeksAgo) return now - parseInt(weeksAgo[1]!, 10) * 7 * day;

  // ISO date: YYYY-MM-DD
  const iso = s.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (iso) {
    const d = new Date(s);
    return isNaN(d.getTime()) ? null : d.getTime();
  }

  // Month name + day: "june 17", "jun 17", "17 june"
  const monthNames: Record<string, number> = {
    jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5,
    jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11,
    january: 0, february: 1, march: 2, april: 3, june: 5,
    july: 6, august: 7, september: 8, october: 9, november: 10, december: 11,
  };

  const monthDay = s.match(/^([a-z]+)\s+(\d{1,2})$/);
  if (monthDay) {
    const month = monthNames[monthDay[1]!];
    if (month !== undefined) {
      const year = new Date().getFullYear();
      return new Date(year, month, parseInt(monthDay[2]!, 10)).getTime();
    }
  }

  const dayMonth = s.match(/^(\d{1,2})\s+([a-z]+)$/);
  if (dayMonth) {
    const month = monthNames[dayMonth[2]!];
    if (month !== undefined) {
      const year = new Date().getFullYear();
      return new Date(year, month, parseInt(dayMonth[1]!, 10)).getTime();
    }
  }

  return null;
}

// ---------------------------------------------------------------------------
// Token estimator — cheap approximation (no tokenizer dependency)
// ---------------------------------------------------------------------------

function estimateTokens(text: string): number {
  return Math.ceil(text.length / 4);
}

// ---------------------------------------------------------------------------
// Part types to skip entirely
// ---------------------------------------------------------------------------

const SKIP_PART_TYPES = new Set([
  "step-start",
  "step-finish",
  "snapshot",
  "file",
]);

// Tool names whose output we aggressively truncate
const HEAVY_TOOL_NAMES = new Set([
  "read",
  "grep",
  "glob",
  "bash",
  "ls",
]);

// ---------------------------------------------------------------------------
// Capa 1: Filter and flatten parts from a message's data
// ---------------------------------------------------------------------------

function compactMessageData(
  data: any,
  parts: any[],
  maxToolOutputChars: number,
): string {
  const role: string = data?.role ?? "unknown";
  const lines: string[] = [];

  for (const part of parts) {
    const partData = part?.data ? (typeof part.data === "string" ? JSON.parse(part.data) : part.data) : part;
    const type: string = partData?.type ?? "";

    if (SKIP_PART_TYPES.has(type)) continue;

    if (type === "text") {
      const text: string = partData.text ?? "";
      if (text.trim()) {
        lines.push(`[${role}] ${text.trim()}`);
      }
      continue;
    }

    if (type === "tool-invocation") {
      const toolName: string = partData.toolInvocation?.toolName ?? partData.toolName ?? "tool";
      const args = partData.toolInvocation?.args ?? partData.args ?? {};
      const state: string = partData.toolInvocation?.state ?? partData.state ?? "";

      if (state === "result") {
        const result = partData.toolInvocation?.result ?? partData.result ?? "";
        const resultStr = typeof result === "string" ? result : JSON.stringify(result);

        if (HEAVY_TOOL_NAMES.has(toolName) && resultStr.length > maxToolOutputChars) {
          const truncated = resultStr.slice(0, maxToolOutputChars);
          lines.push(`[tool:${toolName}] args=${JSON.stringify(args)} → ${truncated} [truncated: ${resultStr.length} chars]`);
        } else {
          lines.push(`[tool:${toolName}] args=${JSON.stringify(args)} → ${resultStr.slice(0, maxToolOutputChars * 2)}`);
        }
      } else {
        // Call without result yet — just note the invocation
        lines.push(`[tool:${toolName}] args=${JSON.stringify(args)}`);
      }
      continue;
    }

    // Write/edit tool results: only show filenames
    if (type === "tool-result") {
      const toolName: string = partData.toolName ?? "tool";
      if (toolName === "write" || toolName === "edit") {
        const filePath = partData.args?.filePath ?? partData.result?.filePath ?? "(unknown file)";
        lines.push(`[tool:${toolName}] modified: ${filePath}`);
      }
      continue;
    }
  }

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Capa 2: Sliding window on message array
// ---------------------------------------------------------------------------

function applyWindow(
  messages: string[],
  maxTokens: number,
  ratio: { start: number; end: number },
): string {
  const full = messages.join("\n");
  if (estimateTokens(full) <= maxTokens) return full;

  const startCount = Math.max(1, Math.floor(messages.length * ratio.start));
  const endCount = Math.max(1, Math.floor(messages.length * ratio.end));
  const omitted = messages.length - startCount - endCount;

  if (omitted <= 0) return full;

  const startPart = messages.slice(0, startCount).join("\n");
  const endPart = messages.slice(messages.length - endCount).join("\n");

  return `${startPart}\n\n[... ${omitted} messages omitted for compaction ...]\n\n${endPart}`;
}

// ---------------------------------------------------------------------------
// Build a plain-text transcript from a session's messages and parts
// ---------------------------------------------------------------------------

export function buildTranscript(
  meta: SessionMeta,
  messages: any[],
  allParts: Map<string, any[]>,
  cfg: CompactionConfig,
): { transcript: string; estimatedTokens: number } {
  const header = [
    `SESSION: ${meta.id}`,
    `Title: ${meta.title}`,
    `Date: ${new Date(meta.timeCreated).toISOString().slice(0, 10)}`,
    `Directory: ${meta.directory}`,
  ].join(" | ");

  // Limit messages to maxMessagesPerSession (keep most recent)
  const capped = messages.slice(-cfg.maxMessagesPerSession);

  const messageLines: string[] = [];

  for (const msg of capped) {
    const data = typeof msg.data === "string" ? JSON.parse(msg.data) : msg.data;
    const parts = allParts.get(msg.id) ?? [];

    // Skip subagent messages (they have an agent field pointing to a tier)
    const agent: string | undefined = data?.agent;
    if (agent && agent !== "plan" && agent !== "code" && agent !== "auto") {
      const text = parts
        .map((p: any) => {
          const pd = typeof p.data === "string" ? JSON.parse(p.data) : p.data;
          return pd?.type === "text" ? pd.text?.trim() : null;
        })
        .filter(Boolean)
        .join(" ")
        .slice(0, 120);
      messageLines.push(`[@${agent}] → ${text || "(no text output)"}`);
      continue;
    }

    const compact = compactMessageData(data, parts, cfg.maxToolOutputChars);
    if (compact.trim()) messageLines.push(compact);
  }

  // Capa 2: sliding window
  const body = applyWindow(messageLines, cfg.maxTokensPerSession, cfg.windowRatio);
  const transcript = `${header}\n\n${body}`;

  return { transcript, estimatedTokens: estimateTokens(transcript) };
}

// ---------------------------------------------------------------------------
// Filter sessions by directory and optional date range
// ---------------------------------------------------------------------------

export function filterSessions(
  sessions: any[],
  cwd: string,
  since: number | null,
  until: number | null,
): any[] {
  return sessions.filter((s: any) => {
    const dir: string = s.directory ?? "";
    const inScope = dir === cwd || dir.startsWith(cwd + "/");
    if (!inScope) return false;

    // Exclude subagent sessions
    if (s.parent_id || s.parentID) return false;

    const created: number = s.time_created ?? s.timeCreated ?? 0;
    if (since !== null && created < since) return false;
    if (until !== null && created > until) return false;

    return true;
  });
}
