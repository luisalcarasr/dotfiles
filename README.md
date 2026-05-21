# 🏠 Dotfiles

Personal workstation configuration managed with [GNU Stow](https://www.gnu.org/software/stow/). Targets **Fedora KDE** (primary) and **macOS** (secondary), providing a reproducible, terminal-centric development environment with a consistent GitHub Dark visual theme across all tools.

## 🚀 Quick Start

### 🐧 Fedora

```bash
bash <(curl -sL https://raw.githubusercontent.com/luisalcarasr/dotfiles/main/fedora.sh)
```

### 🍎 macOS

```bash
bash <(curl -sL https://raw.githubusercontent.com/luisalcarasr/dotfiles/main/macos.sh)
```

### 🔗 Dotfiles

Install `stow` first:

| OS      | Command                   |
|---------|---------------------------|
| Fedora  | `sudo dnf install stow`   |
| macOS   | `brew install stow`       |
| Ubuntu  | `sudo apt install stow`   |

Then clone and deploy:

```bash
git clone git@github.com:luisalcarasr/dotfiles.git ~/.dotfiles && cd ~/.dotfiles && stow .
```

## 📦 Packages

### 🐧 Fedora

| Group        | Packages                                                  | Description                                    |
|--------------|-----------------------------------------------------------|------------------------------------------------|
| 🔧 system    | stow, git, curl, wget                                     | Base tools and dotfile symlink management      |
| 🐚 shell     | fish, zoxide, fzf, fastfetch                              | Primary shell, smart navigation, system info   |
| 📝 editor    | neovim                                                    | LazyVim-based editor with LSP and GitHub Dark  |
| ⚡ cli       | bat, eza, fd-find, ripgrep, tree, jq, btop, unzip         | Modern CLI replacements and system monitor     |
| 🌿 git       | lazygit                                                   | Full-featured Git TUI                          |
| 🐋 containers | podman, distrobox                                        | Daemonless containers and distro environments  |
| 🐍 languages | python3, python3-pip, pipx                                | Python runtime and isolated tool installer     |
| 📱 flatpak   | Brave, Steam, Heroic, ProtonUp-Qt                         | GUI apps via Flathub                           |

### 🍎 macOS

| Group         | Packages                                                                     | Description                                       |
|---------------|------------------------------------------------------------------------------|---------------------------------------------------|
| 🐚 shell      | fish, tmux, zoxide, fzf, fastfetch                                           | Shell, multiplexer, smart navigation              |
| 📝 editor     | neovim, rust-analyzer                                                        | Primary editor and Rust LSP server                |
| ⚡ cli        | bat, eza, fd, ripgrep, tree, jq, glow, pandoc, watch, btop, poppler          | Modern CLI tools and document utilities           |
| 🌿 git        | lazygit, glab, gitleaks, stow, gnupg                                         | Git TUI, GitLab CLI, secrets scanner, GPG         |
| 🐋 containers | colima, docker, docker-compose, docker-buildx, qemu, lazydocker              | Docker Desktop alternative with TUI              |
| 🐍 languages  | python@3.12, pipx, openjdk@21                                                | Python 3.12 LTS, isolated tools, Java 21 JDK     |
| 🌐 network    | curl, wget, axel, nmap                                                       | Networking, downloaders and port scanner          |
| 🗄️ database   | postgresql@14                                                                | Local relational database via brew services       |
| 🔩 utils      | unzip                                                                        | System utilities                                  |
| 🖥️ casks      | kitty, ghostty, mos, insomnia, gimp                                          | GPU terminal, API client, image editor            |

## 🗂️ Stow Packages

| Package      | Target                  | Contents                                                |
|--------------|-------------------------|---------------------------------------------------------|
| 🐚 fish      | `~/.config/fish/`       | Shell config, plugins (tide, nvm, repojump), aliases    |
| 📝 nvim      | `~/.config/nvim/`       | LazyVim config, plugins, keymaps, GitHub Dark theme     |
| 🐱 kitty     | `~/.config/kitty/`      | Terminal theme, OS-specific font and keybindings        |
| 🌿 git       | `~/`                    | `.gitconfig` and `git-ai` AI commit command             |
| 🤖 opencode  | `~/.config/opencode/`   | AI provider config, custom agents and slash commands    |
| 🐋 distrobox | `~/.config/distrobox/`  | Container desktop entry suppression (Linux only)        |

## 🔗 References

- [GNU Stow](https://www.gnu.org/software/stow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Flathub](https://flathub.org/)
- [RPM Fusion](https://rpmfusion.org/)
