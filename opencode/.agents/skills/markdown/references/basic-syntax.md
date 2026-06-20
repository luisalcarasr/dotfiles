# Basic Markdown Syntax

Source: <https://www.markdownguide.org/basic-syntax/>

All elements below are part of the original Markdown design document and are
supported by virtually every Markdown processor.

---

## Headings

Use `#` signs. The number of `#` corresponds to the heading level (1–6).

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

**Alternate syntax** (h1 and h2 only): underline with `===` or `---`.

```markdown
Heading 1
=========

Heading 2
---------
```

**Best practices:**

- Always put a space between `#` and the heading text. (`# Heading`, not `#Heading`)
- Put a blank line before and after every heading.

---

## Paragraphs

Separate paragraphs with one or more blank lines. Do not indent with spaces or
tabs (unless inside a list).

```markdown
First paragraph.

Second paragraph.
```

---

## Line Breaks

To force a line break (`<br>`) inside a paragraph:

- Preferred: two or more trailing spaces, then Return.
- Also valid: trailing backslash `\` (supported by CommonMark, GFM, GLFM).
- Alternative: `<br>` HTML tag — works anywhere HTML is allowed.

```markdown
First line.  
Second line on a new line.

First line.\
Second line on a new line.

First line.<br>
Second line on a new line.
```

> Avoid relying on invisible trailing whitespace — use `<br>` or `\` for
> clarity.

---

## Emphasis

### Bold

Wrap with `**` (recommended) or `__`.

```markdown
**bold text**
__bold text__
Love**is**bold   ← mid-word: asterisks only
```

### Italic

Wrap with `*` (recommended) or `_`.

```markdown
*italic text*
_italic text_
A*cat*meow      ← mid-word: asterisks only
```

### Bold and italic

Wrap with `***` (recommended) or `___` / `__*` / `**_`.

```markdown
***bold and italic***
```

**Best practice:** Use asterisks for mid-word emphasis. Underscores inside
words are handled inconsistently across processors.

---

## Blockquotes

Prefix each line with `>`.

```markdown
> This is a blockquote.
```

### Multiple paragraphs

Add a `>` on the blank line between paragraphs.

```markdown
> Paragraph one.
>
> Paragraph two.
```

### Nested blockquotes

Use `>>` for the nested level.

```markdown
> Outer quote.
>
>> Nested quote.
```

### With other elements

Most Markdown elements work inside blockquotes.

```markdown
> #### Heading inside a quote
>
> - List item
>
> *Italic* and **bold** text.
```

**Best practice:** Put a blank line before and after blockquotes.

---

## Lists

### Ordered lists

Start each item with a number followed by a period. The list must begin with
`1.`; subsequent numbers need not be sequential — the processor auto-numbers.

```markdown
1. First item
2. Second item
3. Third item
```

**Best practice:** Use periods (`1.`), not parentheses (`1)`).

### Unordered lists

Use `-`, `*`, or `+` as markers. Do not mix markers in the same list.

```markdown
- First item
- Second item
- Third item
```

### Nested lists

Indent nested items by 4 spaces (or 1 tab).

```markdown
1. First item
2. Second item
   - Nested unordered item
   - Another nested item
3. Third item
```

### Adding other elements inside lists

Indent block-level content by 4 spaces (8 spaces for a code block inside a
list).

```markdown
- First item.
- Second item.

    A continuation paragraph inside the second item.

- Third item.
```

```markdown
1. Open the file.
2. Find the code block:

        <html>
          <head></head>
        </html>

3. Update the title.
```

---

## Code

### Inline code

Wrap with backticks.

```markdown
Use the `printf()` function.
```

### Escaping backticks

If the code itself contains backticks, wrap with double backticks.

```markdown
``Use `code` in your Markdown file.``
```

### Indented code blocks

Indent every line by at least 4 spaces or 1 tab.

```
    <html>
      <head></head>
    </html>
```

> Prefer fenced code blocks (see `extended-syntax.md`) — they are cleaner
> and support syntax highlighting.

---

## Horizontal Rules

Three or more asterisks, dashes, or underscores on their own line.

```markdown
---

***

___
```

All three render identically. **Best practice:** put blank lines before and
after to avoid accidental h2 parsing.

---

## Links

### Inline links

```markdown
[Duck Duck Go](https://duckduckgo.com)
[Duck Duck Go](https://duckduckgo.com "Optional tooltip")
```

### Auto-links

Wrap a URL or email in angle brackets.

```markdown
<https://www.markdownguide.org>
<fake@example.com>
```

### Reference-style links

Define the URL once and reference it by a label.

```markdown
[Duck Duck Go][duckduckgo]

[duckduckgo]: https://duckduckgo.com "Optional tooltip"
```

### Formatting links

```markdown
I love the **[EFF](https://eff.org)**.
This is the *[Markdown Guide](https://www.markdownguide.org)*.
See the section on [`code`](#code).
```

**Best practices:**

- URL-encode spaces: `%20` (e.g., `[page](https://example.com/my%20page)`).
- URL-encode parentheses: `%28` and `%29` when they appear inside URLs.

---

## Images

```markdown
![Alt text](https://example.com/image.png)
![Alt text](./image.png "Optional title")
```

### Clickable image (link wrapping an image)

```markdown
[![Alt text](./image.png "Title")](https://example.com)
```

---

## Escaping Characters

Prefix any special Markdown character with a backslash `\` to display it
literally.

| Character | Name            |
| --------- | --------------- |
| `\\`      | backslash       |
| `` \` ``  | backtick        |
| `\*`      | asterisk        |
| `\_`      | underscore      |
| `\{ \}`   | curly braces    |
| `\[ \]`   | brackets        |
| `\< \>`   | angle brackets  |
| `\( \)`   | parentheses     |
| `\#`      | pound sign      |
| `\+`      | plus sign       |
| `\-`      | minus sign      |
| `\.`      | dot             |
| `\!`      | exclamation mark|
| `\|`      | pipe            |

---

## HTML

Most processors allow raw HTML inline or as block-level elements.

```markdown
This **word** is bold. This <em>word</em> is italic.
```

**Best practices:**

- Separate block-level HTML (`<div>`, `<table>`, `<pre>`) from surrounding
  content with blank lines.
- Do not indent block HTML with tabs or spaces.
- Markdown syntax does not work inside block-level HTML tags.
- Not all processors allow HTML — confirm before relying on it.
