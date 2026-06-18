// ---------------------------------------------------------------------------
// Chronicle — synthesizer subagent prompt
// ---------------------------------------------------------------------------

export function buildSynthesizerPrompt(
  query: string,
  cwd: string,
  transcripts: string[],
): string {
  const sessionBlocks = transcripts
    .map((t, i) => `### Session ${i + 1}\n\n${t}`)
    .join("\n\n---\n\n");

  return `You are a session history analyst. Your task is to extract relevant context from past work sessions and present it in a structured, useful format.

## Context

Working directory: ${cwd}
Query: "${query}"

## Instructions

Read the session transcripts below and extract information relevant to the query.
For each session that contains relevant information, output a structured summary.
If a session is not relevant to the query, skip it entirely.
Detect the primary language used in the sessions and respond in that same language.

## Output Format

For each relevant session, use this exact structure:

### <session title> — <date>
**Directory:** <directory>
**What was done:** <2-4 bullet points of concrete actions taken>
**Key decisions:** <decisions made, technologies chosen, approaches agreed on — omit if none>
**Pending / state:** <what was left incomplete or in progress — omit if nothing pending>
**Relevant lines:** <brief pointer to where in the transcript the most relevant content is, e.g. "user request at start, implementation in middle third, summary at end">

After all sessions, add a final section:

## Overall Context
<3-6 sentences synthesizing the state of the work across all sessions, what has been accomplished, and what the current situation is — focused on what would help someone continue the work>

## Rules

- Be concise. Bullet points over prose.
- Only include sessions with content relevant to the query.
- If no sessions are relevant, say so clearly in one sentence.
- Do not invent or assume information not present in the transcripts.
- Do not include internal tool call details (grep outputs, file reads) unless they contain a key decision or result.

## Session Transcripts

${sessionBlocks}`;
}

export function buildMiniSynthesisPrompt(
  sessionTitle: string,
  sessionDate: string,
  sessionDirectory: string,
  transcript: string,
): string {
  return `You are a session summarizer. Compress the following work session transcript into a concise summary (max 400 words).

Session: ${sessionTitle}
Date: ${sessionDate}
Directory: ${sessionDirectory}

## Output Format

**What was done:** <3-6 bullet points>
**Key decisions:** <bullet points, or "None" if absent>
**Pending / state:** <what was left incomplete, or "Completed" if finished>
**Key files touched:** <list of files modified/created/deleted, or "None">

Be factual. Only include information explicitly present in the transcript.
Detect the language of the transcript and respond in that same language.

## Transcript

${transcript}`;
}
