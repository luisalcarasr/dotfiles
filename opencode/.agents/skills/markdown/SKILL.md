---
name: markdown
description: Write and format content in Markdown following the markdownguide.org standard (basic + extended syntax). Use when authoring or editing any Markdown — README.md, docs, code comments, changelogs, GitHub/GitLab issues, pull/merge requests, wiki pages, snippets, or chat messages. Prefer rich (extended) syntax wherever the target tool supports it, and degrade to basic syntax otherwise.
---

# Markdown Writing

Author clean, portable Markdown. Default to **extended syntax** (tables, fenced
code blocks, task lists, footnotes, etc.) on every tool that supports it, and
fall back to **basic syntax** only when the target renderer is limited.

The full element-by-element reference lives in `references/`:

- `references/basic-syntax.md` — original Markdown elements (headings,
  emphasis, lists, links, images, code, blockquotes, escaping, HTML).
- `references/extended-syntax.md` — tables, fenced code blocks + syntax
  highlighting, footnotes, heading IDs, definition lists, strikethrough, task
  lists, emoji, highlight, sub/superscript, automatic URL linking.
- `references/tool-support.md` — which features are safe per renderer
  (CommonMark, GitHub GFM, GitLab GLFM) and the GitLab-vs-GitHub answer.

Read the relevant reference file before writing anything non-trivial.

## Core principle: rich first, degrade on purpose

1. Identify the target renderer (GitHub, GitLab, a CommonMark processor, a
   plain `.md` in the repo, etc.). See `references/tool-support.md`.
2. Use the richest syntax that renderer supports: tables over ASCII art,
   fenced code blocks with a language over indented blocks, task lists over
   bullet dashes, footnotes over inline parentheticals.
3. If you cannot confirm support for an extended element (highlight,
   sub/superscript, definition lists), use the HTML fallback (`<mark>`,
   `<sub>`, `<sup>`, `<dl>`) or fall back to basic syntax.

## Golden compatibility rules

Apply these universally — they hold across virtually every processor:

- **Emphasis:** use asterisks (`*`, `**`, `***`), not underscores, especially
  mid-word (`Love**is**bold`). Processors disagree on underscores inside words.
- **Headings:** always put a space after `#` (`# Heading`, never `#Heading`),
  and a blank line before and after the heading.
- **Blank lines:** surround blockquotes, horizontal rules, headings, tables,
  and block-level HTML with blank lines.
- **Ordered lists:** delimit with periods (`1.`), not parentheses (`1)`).
- **Unordered lists:** pick one marker (`-`, `*`, or `+`) and stay consistent;
  never mix markers in the same list.
- **Line breaks:** prefer a trailing `<br>` or a trailing backslash `\`
  (CommonMark/GFM/GLFM). Avoid invisible trailing whitespace.
- **Nested content in lists:** indent 4 spaces; code blocks inside lists
  indent 8 spaces.
- **URLs with spaces or parens:** URL-encode (`%20`, `%28`, `%29`).
- **Code fences:** always tag the language for syntax highlighting
  (```` ```python ````), and match opening/closing fence lengths.

## Target → syntax decision

| Target                           | Use                                                                        |
| -------------------------------- | -------------------------------------------------------------------------- |
| `README.md` / repo docs          | GFM: tables, fenced+highlighted code, task lists, footnotes, admonitions   |
| GitHub issues / PRs / comments   | Full GFM + alerts (`> [!NOTE]`), task lists, `@user` / `#123` references   |
| GitLab issues / MRs / wiki       | GLFM: GFM + alerts, Mermaid/PlantUML, math, `#123`/`@user`/`!MR`, diffs   |
| Unknown / generic CommonMark     | Basic syntax + portable extended (tables, fenced code)                     |
| Plain `.txt` / no renderer       | Basic syntax only; avoid HTML fallbacks                                    |

## Quick element map

**Basic** (→ `references/basic-syntax.md`): headings, paragraphs, line breaks,
bold/italic/bold-italic, blockquotes, ordered/unordered lists, inline code,
indented code blocks, horizontal rules, links (inline/reference/auto), images,
character escaping, raw HTML.

**Extended** (→ `references/extended-syntax.md`): tables (+ alignment), fenced
code blocks (+ syntax highlighting), footnotes, custom heading IDs + anchors,
definition lists, strikethrough (`~~`), task lists (`- [ ]` / `- [x]`),
emoji (paste or `:shortcode:`), highlight (`==` / `<mark>`), subscript
(`~` / `<sub>`), superscript (`^` / `<sup>`), automatic URL linking.

## Don't

- Don't hand-build alignment with spaces when a table works.
- Don't leave fenced code blocks untagged when the language is known.
- Don't use underscores for mid-word emphasis.
- Don't assume highlight, sub/superscript, or definition lists render
  everywhere — confirm in `references/tool-support.md` or use the HTML fallback.
- Don't use GitLab-only syntax (Mermaid, `!123`, `~label`) on GitHub, or
  GitHub alert syntax assuming it renders identically everywhere.

## Source standard

- Basic syntax: <https://www.markdownguide.org/basic-syntax/>
- Extended syntax: <https://www.markdownguide.org/extended-syntax/>
