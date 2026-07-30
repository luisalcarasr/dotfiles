---
name: conventional-commit
description: 'Prompt and workflow for generating conventional commit messages using a structured XML format. Guides users to create standardized, descriptive commit messages in line with the Conventional Commits specification, including instructions, examples, and validation.'
---

### Instructions

```xml
	<description>This file contains a prompt template for generating conventional commit messages. It provides instructions, examples, and formatting guidelines to help users write standardized, descriptive commit messages in accordance with the Conventional Commits specification.</description>
```

### Workflow

**Follow these steps:**

1. Run `git status` to review changed files.
2. Run `git diff` or `git diff --cached` to inspect changes.
3. Stage your changes with `git add <file>`.
4. **Detect the remote platform:**
   ```bash
   git remote get-url origin
   ```
   - Contains a GitLab host (e.g. `gitlab.com`) → GitLab project. Proceed to step 5.
   - Any other host → Non-GitLab. Skip step 5; omit `[#N]` from the subject.
5. **GitLab only — obtain the issue number:** delegate to the `gitlab` subagent to find or create the associated issue and get its number N. The subject **must** end with `[#N]`.
6. Construct your commit message using the following XML structure.
7. After generating your commit message, run the following command:

```bash
git commit -m "type(scope): description"          # non-GitLab
git commit -m "type(scope): description [#N]"     # GitLab
```

8. Just execute this prompt and the agent will handle the commit for you in the terminal.

### Commit Message Structure

```xml
<commit-message>
	<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert</type>
	<scope>()</scope>
	<description>A short, imperative summary of the change</description>
	<issue>#N (required for GitLab projects; omit for non-GitLab)</issue>
	<body>(optional: more detailed explanation)</body>
	<footer>(optional: e.g. BREAKING CHANGE: details, or issue references)</footer>
</commit-message>
```

> The `<issue>` value is appended to the subject line as `[#N]`: `type(scope): description [#N]`.

### Examples

Non-GitLab (no suffix):

```xml
<examples>
	<example>feat(parser): add ability to parse arrays</example>
	<example>fix(ui): correct button alignment</example>
	<example>docs: update README with usage instructions</example>
	<example>refactor: improve performance of data processing</example>
	<example>chore: update dependencies</example>
	<example>feat!: send email on registration (BREAKING CHANGE: email service required)</example>
</examples>
```

GitLab (subject ends with `[#N]`):

```xml
<examples>
	<example>feat(parser): add ability to parse arrays [#12]</example>
	<example>fix(ui): correct button alignment [#34]</example>
	<example>docs: update README with usage instructions [#7]</example>
	<example>refactor: improve performance of data processing [#21]</example>
	<example>chore: update dependencies [#55]</example>
	<example>feat!: send email on registration [#88] (BREAKING CHANGE: email service required)</example>
</examples>
```

### Validation

```xml
<validation>
	<type>Must be one of the allowed types. See <reference>https://www.conventionalcommits.org/en/v1.0.0/#specification</reference></type>
	<scope>Optional, but recommended for clarity.</scope>
	<description>Required. Use the imperative mood (e.g., "add", not "added").</description>
	<issue>Required for GitLab projects. Must be appended as [#N] at the end of the subject line. Obtain N via the gitlab subagent (find or create the associated issue). Omit entirely for non-GitLab remotes.</issue>
	<body>Optional. Use for additional context.</body>
	<footer>Use for breaking changes or issue references.</footer>
</validation>
```

### Final Step

```xml
<final-step>
	<cmd>git commit -m "type(scope): description"</cmd>
	<cmd-gitlab>git commit -m "type(scope): description [#N]"</cmd-gitlab>
	<note>Replace with your constructed message. Use the gitlab variant for GitLab projects (N = issue number obtained via the gitlab subagent). Include body and footer if needed.</note>
</final-step>
```
