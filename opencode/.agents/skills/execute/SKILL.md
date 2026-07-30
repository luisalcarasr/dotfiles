---
name: execute
description: Executes the agreed session plan end-to-end, then verifies it — runs the test suite, reviews the CI config and runs locally the validations it can, links the change to a related repo issue/work item (GitHub via gh, GitLab via glab, auto-detected from the git remote) or creates a new one, adds a detailed comment, and updates the issue description and labels. Use when the user says "execute", "ejecuta el plan", "run the plan", or asks to implement and validate an agreed plan.
---

# Execute Skill

End-to-end workflow that takes the plan agreed in the current session, implements it, validates it, and keeps the repository's issue tracker in sync.

---

## Phase 0 — Preparation

1. **Confirm there is a plan.** If no plan was agreed in this session, ask the user to describe what should be done before proceeding.

2. **Build the task list.** Use `todowrite` to create a TODO for every step of the plan *plus* one TODO for each phase of this skill (Tests, CI local, Issue sync). Mark items `in_progress` / `completed` in real time — never batch completions.

3. **Detect the repo platform.** Run:

   ```bash
   git remote get-url origin
   ```

   | Remote contains       | Platform | CLI    |
   |-----------------------|----------|--------|
   | `github.com`          | GitHub   | `gh`   |
   | `gitlab.com` / any other GitLab host | GitLab | `glab` |

   Then verify authentication:

   - GitHub: `gh auth status`
   - GitLab: `glab auth status`

   If the CLI is not authenticated, warn the user and skip Phases 4–5 (but continue with Tests and CI).

4. **Capture the diff baseline.** Note which files are currently changed or staged (`git status`, `git diff --stat HEAD`). This is used later to scope the issue search.

---

## Phase 1 — Execute the Plan

- Implement all changes described in the session plan.
- Mark each plan TODO `in_progress` when you start it and `completed` when it is done.
- Do **not** commit or push unless the user explicitly asks. If a commit is needed, delegate to the `git` subagent.

---

## Phase 2 — Tests

1. **Detect the test runner.** Check in order:

   | Signal                                 | Runner command              |
   |----------------------------------------|-----------------------------|
   | `package.json` → `scripts.test`        | `npm test` / `pnpm test` / `yarn test` |
   | `pytest.ini` / `pyproject.toml [tool.pytest]` | `pytest`             |
   | `Cargo.toml`                           | `cargo test`                |
   | `Makefile` with `test` target          | `make test`                 |
   | `go.mod`                               | `go test ./...`             |

2. **Run the suite.** Do not mark this phase complete until tests pass.

3. **If tests fail:** fix the root cause, then re-run. Do not move on with a broken suite.

---

## Phase 3 — CI Local Validation

1. **Locate the CI config:**
   - GitHub: `.github/workflows/*.yml`
   - GitLab: `.gitlab-ci.yml`

2. **Read and extract steps.** For each job/stage, identify shell commands (lint, typecheck, format check, build, audit, etc.).

3. **Classify steps:**

   | Runnable locally                           | Skip (requires remote infra)              |
   |--------------------------------------------|-------------------------------------------|
   | `eslint`, `tsc`, `prettier --check`        | Deploy jobs, cloud auth, secret injection |
   | `pytest`, `cargo clippy`, `go vet`         | Docker build (if no daemon), test services |
   | `npm run build`, `pip install`, `make lint`| Matrix jobs requiring multiple OS/versions |

4. **Run the runnable steps.** Fix any failures before continuing.

5. **Report skipped steps** with a one-line reason each.

---

## Phase 4 — Issue / Work Item Sync

### 4a — Gather context

Collect keywords from:
- The plan summary
- `git diff --stat HEAD` (changed file names and paths)
- The commit message if one was written

### 4b — Search for a related issue

```bash
# GitHub
gh issue list --state open --limit 100 --json number,title,body,labels

# GitLab
glab issue list --state opened -P 100
```

Compare titles and descriptions against the collected keywords. An issue is "related" if it shares a clear semantic overlap (same feature, same bug, same module).

### 4c — If a related issue IS found

1. **Add a comment** with:
   - What was implemented (summary of the plan)
   - Files changed (`git diff --stat HEAD`)
   - Test result (pass/fail count if available)
   - CI local validations that ran and their outcome
   - CI steps that were skipped and why

   ```bash
   # GitHub
   gh issue comment <number> --body "..."

   # GitLab
   glab issue note <number> --message "..."
   ```

2. **Review the issue description.** If it is missing details, outdated, or incomplete relative to what was implemented, propose an update and — **after user confirmation** — apply it:

   ```bash
   # GitHub
   gh issue edit <number> --body "..."

   # GitLab
   glab issue update <number> --description "..."
   ```

3. **Validate labels.** Fetch the repo's label list:

   ```bash
   # GitHub
   gh label list

   # GitLab
   glab label list
   ```

   Check that the issue has at least one label that reflects the kind of work (e.g., `bug`, `feature`, `enhancement`, `refactor`, `ci`, `documentation`). If no appropriate label is applied, propose one and — **after user confirmation** — apply it:

   ```bash
   # GitHub
   gh issue edit <number> --add-label "<label>"

   # GitLab
   glab issue update <number> --label "<label>"
   ```

### 4d — If NO related issue is found

1. Review **all open issues** one more time to be sure none applies.

2. **Ask the user to confirm** before creating a new issue (show the proposed title and description first).

3. Create the issue with:
   - **Title:** one-line summary of the work done
   - **Description:** context, motivation, what was changed, files touched, test/CI status
   - **Label:** the most appropriate one from the repo's label list (or `enhancement` as default for GitHub)

   ```bash
   # GitHub
   gh issue create --title "..." --body "..." --label "..."

   # GitLab
   glab issue create --title "..." --description "..." --label "..."
   ```

---

## Phase 5 — Final Report

Output a concise summary to the user:

```
## Execution Summary

**Plan:** <one-line description>
**Tests:** ✅ passed / ❌ N failures
**CI local:** <list of steps run and their status> | Skipped: <list>
**Issue:** #<number> <title> — comment added / created
  URL: <link>
```

---

## Important Rules

- **Never commit or push** unless the user explicitly asks. Delegate all git operations to the `git` subagent.
- **Always confirm** before modifying an issue description, applying labels, or creating a new issue. These are writes to the remote repository.
- **Use `todowrite`** throughout. Keep exactly one TODO `in_progress` at any time.
- If a phase fails (tests won't pass, CI step errors that can't be fixed automatically), stop, report the problem, and ask the user for guidance — do not silently skip to the next phase.
- If the detected CLI (`gh`/`glab`) is not installed or not authenticated, skip all issue operations and clearly tell the user what would have happened.
