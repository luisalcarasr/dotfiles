# Extended Markdown Syntax

Source: <https://www.markdownguide.org/extended-syntax/>

Extended syntax is not universally supported. Always check `tool-support.md`
before using an element. When in doubt, use the HTML fallback if the processor
allows raw HTML.

---

## Tables

Supported by: GFM, GLFM, MultiMarkdown, Markdown Extra, many others.

Columns are separated by `|`. The second row (separator) uses `---` and sets
alignment with `:`.

```markdown
| Syntax    | Description |
| --------- | ----------- |
| Header    | Title       |
| Paragraph | Text        |
```

### Alignment

| Syntax | Effect          |
| ------ | --------------- |
| `:---` | Left-aligned    |
| `:---:`| Center-aligned  |
| `---:` | Right-aligned   |

```markdown
| Left   | Center | Right  |
| :----- | :----: | -----: |
| Cell 1 | Cell 2 | Cell 3 |
```

### Formatting inside cells

Inline elements work in cells: `**bold**`, `*italic*`, `` `code` ``, links.
Block elements (headings, blockquotes, lists, images, horizontal rules) do
**not** work directly. Use `<br>` for line breaks inside cells.

### Escaping a pipe character

Use the HTML entity `&#124;` to display a literal `|` inside a cell.

---

## Fenced Code Blocks

Supported by: GFM, GLFM, CommonMark, and most processors.

Three backticks or three tildes on lines before and after the block.

````markdown
```
Plain code, no language.
```
````

### Syntax highlighting

Add the language identifier after the opening fence.

````markdown
```python
def hello():
    print("Hello, world!")
```
````

````markdown
```json
{ "name": "Alice", "age": 30 }
```
````

Common language identifiers: `bash`, `sh`, `zsh`, `python`, `javascript`,
`typescript`, `json`, `yaml`, `toml`, `sql`, `html`, `css`, `rust`, `go`,
`lua`, `gdscript`, `diff`, `plaintext`.

> Always tag fenced blocks with a language when the language is known.

---

## Footnotes

Supported by: GFM (GitHub), GLFM (GitLab), MultiMarkdown, Markdown Extra.
**Not** in CommonMark baseline.

```markdown
Here is a sentence with a footnote.[^1]

[^1]: This is the footnote text.
```

Footnote identifiers can be numbers or words, but not spaces or tabs. They are
rendered sequentially regardless of the label used.

Multi-paragraph footnotes (indent with 4 spaces):

```markdown
[^long]: First paragraph of the footnote.

    Second paragraph, indented.

    `{ code here }`
```

Footnote definitions can go anywhere in the document (they always render at the
bottom).

---

## Heading IDs

Supported by: GFM, GLFM, MultiMarkdown, Markdown Extra.

### Custom heading IDs

```markdown
### My Section {#custom-id}
```

Renders as `<h3 id="custom-id">My Section</h3>`.

### Anchor links

```markdown
[Jump to section](#custom-id)
[Same-page link](#heading-ids)
[Other page](page.md#custom-id)
```

Note: GFM and GLFM auto-generate heading IDs from the heading text (lowercase,
spaces → hyphens, non-word characters removed), so custom IDs are usually
unnecessary on those platforms.

---

## Definition Lists

Supported by: MultiMarkdown, Markdown Extra, GLFM (since v17.7).
**Not** in GFM (GitHub) or CommonMark.

HTML fallback: `<dl>` / `<dt>` / `<dd>`.

```markdown
First Term
: This is the definition of the first term.

Second Term
: One definition of the second term.
: Another definition of the second term.
```

HTML fallback (use when the processor doesn't support native definition lists):

```html
<dl>
  <dt>First Term</dt>
  <dd>Definition of the first term.</dd>
</dl>
```

---

## Strikethrough

Supported by: GFM, GLFM, and most extended processors.

```markdown
~~The world is flat.~~ We now know it's round.
```

---

## Task Lists

Supported by: GFM, GLFM. Checkboxes are interactive on GitHub and GitLab.

```markdown
- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media
```

Nested tasks:

```markdown
- [x] Parent task
  - [x] Sub-task 1
  - [ ] Sub-task 2
```

GitLab also supports inapplicable tasks with `[~]`.

---

## Emoji

### Copy and paste

Paste the emoji directly — most processors display it inline.

```markdown
I went camping ⛺ last weekend.
```

### Shortcodes

Supported by: GFM (GitHub), GLFM (GitLab). Not in CommonMark baseline.

```markdown
Gone camping! :tent: Be back soon.
That is so funny! :joy:
```

A comprehensive shortcode list: <https://gist.github.com/rxaviers/7360908>

> Shortcode names vary by platform. Prefer direct emoji paste for portability.

---

## Highlight

Supported by: some extended processors (e.g., Markdown Extra, some static site
generators). **Not** in GFM or GLFM.

```markdown
I need to highlight ==these words==.
```

HTML fallback (works wherever HTML is allowed):

```markdown
I need to highlight <mark>these words</mark>.
```

---

## Subscript

Supported by: MultiMarkdown and some extended processors. **Not** in GFM or
GLFM natively.

```markdown
H~2~O
```

HTML fallback:

```markdown
H<sub>2</sub>O
```

> Test before using — some processors treat `~` as strikethrough trigger.

---

## Superscript

Supported by: MultiMarkdown and some extended processors. **Not** in GFM or
GLFM natively.

```markdown
X^2^
```

HTML fallback:

```markdown
X<sup>2</sup>
```

---

## Automatic URL Linking

Supported by: GFM, GLFM, and many extended processors.

Bare URLs are auto-linked without brackets.

```markdown
https://www.example.com
```

Renders as: [https://www.example.com](https://www.example.com)

### Disabling auto-linking

Wrap in backticks to prevent auto-linking.

```markdown
`https://www.example.com`
```

---

## HTML Fallbacks Summary

When an extended feature is not supported, use HTML:

| Feature         | Markdown (extended)  | HTML fallback                           |
| --------------- | -------------------- | --------------------------------------- |
| Highlight       | `==text==`           | `<mark>text</mark>`                     |
| Subscript       | `~text~`             | `<sub>text</sub>`                       |
| Superscript     | `^text^`             | `<sup>text</sup>`                       |
| Definition list | `term\n: def`        | `<dl><dt>...</dt><dd>...</dd></dl>`     |
| Line break      | trailing `\` or `  ` | `<br>`                                  |
| Colored text    | (not standard)       | `<span style="color:#f00">text</span>`  |
