# AGENTS.md

Personal dotfiles managed with **GNU Stow**. Primary platforms: Ubuntu and macOS Apple Silicon. Fedora KDE is **legacy** (kept working, lower priority). See `README.md` and `CONTRIBUTING.md`.

## Stow layout (read this first)
- Each top-level dir (`fish/`, `nvim/`, `kitty/`, `git/`, `opencode/`, `distrobox/`) is a **stow package**. Inside, paths mirror `$HOME` (e.g. `fish/.config/fish/config.fish` -> `~/.config/fish/config.fish`).
- Edit configs **inside the package dir**, never the symlinked `~/.config/...` target.
- `.stow-local-ignore` lists files that are NOT symlinked (README, AGENTS.md, LICENSE, setup scripts). Any new top-level file that is not a stow package MUST be added here, or `stow .` will symlink it into `$HOME`.

## Deploy commands
- Ubuntu / Fedora: `stow .` (stows everything).
- macOS: selective — `stow fish nvim kitty git opencode` (the `macos.sh` next-steps line also names `tmux` and `btop`, but those packages do not exist in the repo; only stow packages that exist).
- Re-link a single package: `stow <pkg>`. Remove: `stow -D <pkg>`. Preview conflicts: `stow -nv <pkg>`.

## Setup scripts
- `ubuntu.sh` (apt + snap), `macos.sh` (brew), and legacy `fedora.sh` (dnf + flatpak) are the source of truth for installed tooling.
- Add tools by appending to the relevant `PACKAGES_*` / `CASKS` / `SNAP_APPS` / `FLATPAK_APPS` / `TAPS` array — do not invent install steps elsewhere. Scripts are idempotent (skip already-installed).
- `set -euo pipefail`; keep them backwards-compatible and dependency-free (see CONTRIBUTING.md).
- Ubuntu uses **snap** for GUI apps, not Flatpak (Flatpak is Fedora-only). `ubuntu.sh` installs only dev-relevant GUI apps (Brave); gaming apps live in `fedora.sh` only.
- Ubuntu quirks (handled by `ubuntu.sh`): `bat`/`fd-find` install as `batcat`/`fdfind` and get shimmed to `bat`/`fd` in `~/.local/bin`; `eza` (gierens apt repo) and `lazygit` (GitHub release) are installed from upstream, not the default repos.

## Conventions
- Commits: Conventional Commits, imperative, lowercase, no trailing period, <=72 chars. Scope = stow package or script name (e.g. `fix(fish): ...`, `docs(readme): ...`).
- Shell style: clarity over cleverness; explicit loops over compact one-liners (CONTRIBUTING.md has the canonical example).
- Visual theme is GitHub Dark across tools; keep it consistent.

## Component notes
- `git/.local/bin/git-ai` — Python `git ai commit` helper; requires a running local **ollama** (default model `codellama`). Not a general dependency.
- `fish/.config/fish/functions/tide/`, `nvm.fish`, `fisher.fish`, `rj.fish` are **vendored plugins** (managed by fisher / `dotfiles_bootstrap.fish`). Do not hand-edit; they are regenerated.
- `fish/.config/fish/conf.d/` files load by numeric prefix order; `dotfiles_bootstrap.fish` installs fisher + tide/nvm/repojump on first interactive shell.
- nvim is LazyVim-based; `lazy-lock.json` is the plugin lockfile.

## Don't
- Don't add cross-platform/generalisation changes (zsh, Arch, openSUSE, etc.) — out of scope per CONTRIBUTING.md. Supported platforms are Ubuntu and macOS Apple Silicon (primary) and Fedora KDE (legacy) only.
- Don't commit `fish/.config/fish/fish_variables` machine state (gitignored).
