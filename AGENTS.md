# AGENTS.md

Agent instructions for the `~/.dotfiles` repository.

## What this repo is

GNU Stow-based dotfiles for **Fedora KDE** (primary) and **macOS** (secondary). Each top-level directory is a stow package that maps 1:1 onto `$HOME`. There is no build system, no tests, and no CI — the source of truth is the files themselves.

## Stow packages and their targets

| Directory   | Stow target          | Notes                                       |
|-------------|----------------------|---------------------------------------------|
| `fish/`     | `~/.config/fish/`    | Shell config — see bootstrap quirk below    |
| `nvim/`     | `~/.config/nvim/`    | LazyVim; Lua only, no compiled artifacts    |
| `kitty/`    | `~/.config/kitty/`   | Includes `macos.conf` and `linux.conf`; kitty loads the right one via `${KITTY_OS}.conf` |
| `git/`      | `~/`                 | `.gitconfig` + `git-ai` fish script at `.local/bin/git-ai` |
| `opencode/` | `~/.config/opencode/` + `~/.agents/` | AI config, agents, commands, skills |
| `distrobox/`| `~/.config/distrobox/` | Linux only; suppresses container `.desktop` entries |

Files excluded from stow (never symlinked into `$HOME`): see `.stow-local-ignore`. Always add new root-level scripts there.

## Deploy commands

```bash
stow .                              # deploy all packages
stow fish nvim kitty git opencode   # macOS subset
stow -D <package>                   # remove a package
```

**Do not run `stow` from inside a package subdirectory** — always from repo root.

## Setup scripts

- `fedora.sh` — Fedora KDE full setup (RPM Fusion, NVIDIA open driver, DNF packages, Flatpak/Flathub apps, NVIDIA GL/GL32/VAAPI Flatpak runtimes, system services). Idempotent; runs as normal user, uses `sudo` internally.
- `macos.sh` — macOS setup (Homebrew, taps, formulae by category, casks, colima). Idempotent.

**Adding packages:** append to the relevant `PACKAGES_*` array in the script. One line per package, no other changes needed.

Both scripts use `set -euo pipefail` — they abort on first error.

## Fish shell bootstrap quirk

`fish/.config/fish/conf.d/dotfiles_bootstrap.fish` auto-installs fisher and plugins on first interactive shell via a universal variable flag (`__dotfiles_bootstrapped`). Plugins: `jorgebucaran/nvm.fish`, `IlanCosman/tide`, `luisalcarasr/repojump`. This only runs once per machine. Node.js is managed by `nvm.fish` — never install it via a system package manager.

`paths_scanner.fish` scans `~/.*` hidden dirs (up to 4 levels) for `bin/` folders and prepends them to `$PATH`. This is how `~/.local/bin/git-ai` gets on the path.

## Commit style

Conventional Commits — inferred from history and enforced by `opencode/commands/commit.md`:

```
type(scope): short imperative description
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`. Scope is optional but used (e.g. `feat(fish):`, `fix(nvim):`, `chore(opencode):`). No period at end. Max 72 chars on subject line.

The `/commit` slash command in OpenCode automates this: inspects staged diff, detects secrets, asks for confirmation, then commits.

## `git-ai` command

`git ai commit` — generates a Conventional Commit message from the staged diff using `ollama run codellama` locally. Requires ollama running with the `codellama` model pulled.

## OpenCode config location

`opencode/.config/opencode/opencode.json` — provider is **F5 AI** (internal OpenAI-compatible gateway). Requires `F5AI_API_KEY` env var. Do not commit or expose this key. The `default_agent` is `plan` (read-only by default; switches to `build` for edits).

Custom agents: `opencode/.config/opencode/agents/` — `chat.md` (read-only), `browse.md` (Firefox DevTools subagent).

Skills live in `opencode/.agents/skills/` and are tracked in `.skill-lock.json`.

## Neovim

LazyVim base with extras: `eslint`, `prettier`, `python`, `typescript`, `json`, `rust`, `markdown`, `tailwind`, `mini-hipatterns`, `mini-animate`. Custom plugins in `nvim/.config/nvim/lua/plugins/`. No compiled output — everything is plain Lua loaded at startup. `lazy-lock.json` pins plugin versions; update intentionally with `:Lazy update`.

Opencode integration via `opencode.nvim`: `<C-a>` ask, `<C-x>` select action, `<C-.>` toggle. `+`/`-` replace `<C-a>`/`<C-x>` for increment/decrement since those are remapped.

## Platform notes

- macOS: Apple Silicon (`/opt/homebrew`) — `paths_scanner.fish` adds brew to PATH. Container runtime is colima (not Docker Desktop).
- Fedora KDE: container runtime is podman + distrobox. `distrobox/` package suppresses auto-generated `.desktop` entries.
- Kitty loads `macos.conf` or `linux.conf` automatically via `${KITTY_OS}.conf` — edit the right file for OS-specific font or keybinding changes.
- The Linux-specific font is **AdwaitaMono Nerd Font**; macOS uses **Operator Mono Lig**.
