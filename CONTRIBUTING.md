# Contributing

This is a personal dotfiles repository. It is public because sharing configurations openly is useful to the community, and because I enjoy seeing how others set up their environments. However, it is **not designed to be a universal solution** — it is built around one specific, opinionated setup: Ubuntu and macOS Apple Silicon as primary, with Fedora KDE kept as legacy, and a fixed set of tools, fonts, and workflows that suit me personally.

Before opening a pull request, please read this document in full.

---

## What this repository is (and is not)

These dotfiles are tailored to my exact machines, preferences, and habits. Configs reference specific fonts, paths, shell plugins, and tools that may not exist on your system. There is no abstraction layer, no plugin system, and no intention to become one.

**This means:**

- A change that works perfectly on your machine may be intentionally absent here because it does not fit my workflow.
- Generalisation patches (e.g. "add support for zsh", "make it work on Arch/openSUSE") will almost certainly be declined — not because they are bad ideas, but because they are out of scope.
- Aesthetic changes driven purely by personal preference will also be declined.

---

## Contributions that may be accepted

The bar is intentional narrowness, not quality. High-quality contributions that fall outside the scope of this repo will still be declined. With that said, the following are genuinely welcome:

- **Bug fixes** that affect the primary platforms (Ubuntu, macOS Apple Silicon) and reproduce reliably. Fedora KDE is legacy — fixes are welcome but lower priority.
- **Factual corrections** to `README.md`, `CONTRIBUTING.md`, or inline script comments.
- **Script improvements** to `ubuntu.sh`, `macos.sh`, or `fedora.sh` that are clearly correct, backwards-compatible, and do not introduce new dependencies.
- **Fixes for broken symlinks or stow conflicts** that affect the standard deployment (`stow .`).

If you are unsure whether your contribution is in scope, open an issue and ask before writing any code.

---

## How to contribute

### 1. Fork and branch

Fork the repository and create a branch with a descriptive name:

```
fix/fish-path-scanner-hidden-dirs
docs/update-stow-package-table
```

### 2. Write clear, readable code

This repository values **clarity over cleverness**. Code should be easy to read at a glance, even if a more compact or optimised version exists. Prefer explicit over implicit. Add a comment when the intent is not immediately obvious.

```bash
# Good: intent is clear
for pkg in "${PACKAGES_CLI[@]}"; do
    sudo dnf install -y "$pkg"
done

# Avoid: clever but opaque
sudo dnf install -y "${PACKAGES_CLI[@]}"
```

Both work. The first is preferred here.

### 3. Use Conventional Commits

All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification:

```
type(scope): short imperative description
```

**Allowed types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

**Scope** is optional but encouraged. Use the stow package name or script name as scope:

```
fix(fish): correct path expansion for nested bin dirs
docs(readme): update macOS package table
chore(fedora.sh): add missing flatpak remote check
```

Rules:
- Subject line is imperative mood, lowercase after the type, no period at end
- Maximum 72 characters on the subject line
- Use the body to explain *what changed and why*, not *how*

### 4. Describe your pull request thoroughly

A good PR description answers:

1. **What** does this change do?
2. **Why** is it needed? What problem does it solve or what error does it fix?
3. **Which platform** was it tested on? (Ubuntu, macOS Apple Silicon, Fedora KDE, or a combination)
4. **Are there any side effects** or caveats to be aware of?

Pull requests with vague descriptions will be asked to provide more detail before review.

---

## Questions

If you have a question — about how something works, why a particular choice was made, or how to adapt something for your own setup — **open an issue**. I am genuinely happy to answer. Questions are one of the most valuable forms of engagement a public repository can receive, and I will do my best to respond clearly and promptly.

There is no such thing as a question too simple to ask here.

---

## License

By contributing, you agree that your changes will be distributed under the same license as this repository. See [`LICENSE`](./LICENSE).
