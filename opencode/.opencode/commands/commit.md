---
description: Analyze changes and create a commit
---
Prepare a git commit for the current repository.

Requirements:
- Read `CONTRIBUTING.md` if it exists and follow any commit message guidance found there.
- Inspect recent commit history with `git log --oneline -20` and infer the repository's commit message style.
- If there is no clear style from `CONTRIBUTING.md` or the commit history, use a short, semantic, single-line Conventional Commit message.
- Inspect the current worktree with `git status --short`.
- Inspect staged and unstaged changes with `git diff --stat`, `git diff`, `git diff --cached --stat`, and `git diff --cached`.
- Do not include files that likely contain secrets, credentials, tokens, private keys, or local environment values. Warn me if such files appear in the changes.
- Do not revert or modify unrelated user changes.
- Draft the commit message based on the actual changes, focusing on why the change exists.
- Show the proposed commit message and a concise summary of files to be committed.
- Ask for confirmation before running `git add` or `git commit`.
- After confirmation, stage only relevant files and create the commit.
- Run `git status --short` after the commit and report the result.

If arguments are provided, treat them as extra instructions from me:

`$ARGUMENTS`
