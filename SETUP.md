# Setup Instructions

This document contains setup instructions for different operating systems.

## macOS

Setup instructions for a new macOS workstation. The environment is terminal-centric, oriented towards fullstack development (TypeScript, Python, Rust, Java) with a consistent **GitHub Dark** visual theme across all tools.

### Homebrew

Install [Homebrew](https://brew.sh/) if not already installed:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Taps

```sh
brew tap deskflow/tap       # Deskflow KVM (share keyboard/mouse across machines)
brew tap hashicorp/tap      # HashiCorp tools (Terraform, Vault, etc.)
brew tap homebrew/services  # Manage background services (start/stop daemons)
```

#### Shell and Terminal Environment

| Package | Purpose |
|---|---|
| **fish** | Primary shell. Uses Tide prompt, fisher plugin manager, nvm.fish for Node.js, and repojump for repo navigation. Configures aliases for eza, git, nvim and python. |
| **tmux** | Terminal multiplexer. Persistent sessions and panes. Configured with prefix `Ctrl+a`, vim navigation (hjkl), and mouse support. |
| **zoxide** | Smart `cd` replacement. Learns frequently visited directories, allows fuzzy jumping. Aliased as `cd` in fish. |
| **fzf** | Interactive fuzzy finder. Integrates with fish and neovim for searching files, history, and more. |
| **fastfetch** | System info display on terminal open (OS, hardware, uptime). Modern neofetch alternative. |

```sh
brew install fish tmux zoxide fzf fastfetch
```

#### Code Editor

| Package | Purpose |
|---|---|
| **neovim** | Primary editor. LazyVim-based with extras: ESLint, Prettier, Python, TypeScript, Rust, JSON, Markdown, Tailwind. Plugins: toggleterm (floating terminal), neoclip (clipboard history), blamer (inline git blame), zen-mode, scrollbar with gitsigns. GitHub Dark theme. |
| **rust-analyzer** | Rust LSP server. Provides autocompletion, diagnostics, and refactoring in neovim. |

```sh
brew install neovim rust-analyzer
```

#### CLI Productivity Tools

| Package | Purpose |
|---|---|
| **bat** | `cat` replacement with syntax highlighting, line numbers, and paging. |
| **eza** | `ls` replacement with colors, icons, and tree view. Aliased as `ls`, `ll`, `la` in fish. |
| **fd** | `find` replacement. Faster, respects `.gitignore`, simple syntax. |
| **ripgrep** | Ultra-fast `grep` replacement. Used internally by neovim Telescope for project-wide search. |
| **tree** | Directory structure visualization in tree form. |
| **jq** | Command-line JSON processor and formatter. Essential for working with APIs and config files. |
| **glow** | Terminal Markdown renderer with styles and colors. |
| **pandoc** | Universal document converter (Markdown, HTML, PDF, DOCX, LaTeX, etc.). |
| **watch** | Runs a command periodically, displaying updated output. Useful for monitoring. |
| **btop** | Interactive system monitor (CPU, RAM, disk, network). Configured with vim keys and braille graphs. |
| **poppler** | PDF processing library. Provides utilities like `pdftotext`, `pdfinfo`. |

```sh
brew install bat eza fd ripgrep tree jq glow pandoc watch btop poppler
```

#### Git and Version Control

| Package | Purpose |
|---|---|
| **lazygit** | Full Git TUI. Visual commits, partial staging, interactive rebase, conflict resolution in terminal. |
| **glab** | Official GitLab CLI. Manage merge requests, issues, CI/CD pipelines and releases from terminal. |
| **gitleaks** | Repository secrets scanner. Detects accidentally committed API keys, tokens and passwords. |
| **stow** | Symlink manager. Core of the dotfiles system: each repo directory is a "package" that stow links into `$HOME` preserving directory structure. |
| **gnupg** | GPG encryption suite. Commit signing, cryptographic key management, file encryption. |

```sh
brew install lazygit glab gitleaks stow gnupg
```

#### Containers and Virtualization

| Package | Purpose |
|---|---|
| **colima** | Container runtime for macOS. Lightweight Docker Desktop alternative, runs a Linux VM with containerd/docker. |
| **docker** | Container engine CLI. Connects to colima daemon to build and run containers. |
| **docker-compose** | Multi-container orchestration via `docker-compose.yml`. Aliased as `compose` in fish. |
| **docker-buildx** | Extended Docker build plugin. Supports multi-platform builds (ARM/x86) and advanced caching. |
| **qemu** | Machine emulator and virtualizer. Dependency of colima/lima for running the Linux VM on macOS. |
| **lazydocker** | Docker TUI. Visual dashboard for containers, images, volumes and logs. |

```sh
brew install colima docker docker-compose docker-buildx qemu lazydocker
```

#### Languages and Runtimes

| Package | Purpose |
|---|---|
| **python@3.10** | Python 3.10 runtime. |
| **pipx** | Installs Python CLI tools in isolated virtual environments. Avoids polluting the system Python. |
| **openjdk@21** | Java 21 JDK (LTS). Runtime and compiler for Java applications. |
| Node.js | Managed by **nvm.fish** (fish plugin), not Homebrew. Defaults to LTS version. |

```sh
brew install python@3.10 pipx openjdk@21
```

#### Networking

| Package | Purpose |
|---|---|
| **curl** | URL data transfer. Homebrew version is more recent than the system one, with HTTP/3 support. |
| **wget** | HTTP/FTP downloader. Useful for recursive downloads and mirrors. |
| **axel** | Accelerated downloader with multiple simultaneous connections. |
| **nmap** | Network scanner and security auditing. Host discovery, open ports, service detection. |

```sh
brew install curl wget axel nmap
```

#### Database

| Package | Purpose |
|---|---|
| **postgresql@14** | Relational database system for local development. Managed as a service via `brew services`. |

```sh
brew install postgresql@14
```

#### System Utilities

| Package | Purpose |
|---|---|
| **unzip** | ZIP file decompressor. Homebrew version more complete than the system one. |

```sh
brew install unzip
```

#### Casks (GUI Applications)

| Cask | Purpose |
|---|---|
| **kitty** | Primary terminal emulator. GPU-accelerated, configured with GitHub Dark theme, Operator Mono Lig font on macOS, smart layouts (auto grid/vertical). |
| **ghostty** | Alternative GPU-accelerated terminal emulator. Installed without custom dotfiles configuration. |
| **mos** | macOS utility that improves external mouse scrolling (smoothing, independent direction inversion from trackpad). |
| **insomnia** | GUI client for REST and GraphQL API testing. Design, test and document endpoints. |
| **gimp** | Professional open-source image editor. Graphics manipulation, design and retouching. |

```sh
brew install --cask kitty ghostty mos insomnia gimp
```

### Dotfiles

Clone the repository and deploy configurations with stow:

```sh
git clone git@github.com:luisalcarasr/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
stow .
```

Alternatively, deploy only macOS-relevant packages:

```sh
stow fish nvim tmux kitty git btop opencode
```

#### Stow Packages (macOS-relevant)

| Package | Target | Contents |
|---|---|---|
| `fish` | `~/.config/fish/` | Shell config, plugins (fisher, tide, nvm, repojump), aliases, dynamic PATH builder, automatic bootstrap. |
| `nvim` | `~/.config/nvim/` | LazyVim config, plugins, keymaps, GitHub Dark theme. |
| `tmux` | `~/.tmux.conf` | Prefix, keybindings, vim navigation. |
| `kitty` | `~/.config/kitty/` | Theme, macOS-specific font (Operator Mono Lig 16pt), smart layout kitten, OS-conditional config. |
| `git` | `~/.gitconfig` | User identity, defaults, custom `git-ai` command (AI commit messages via ollama/codellama). |
| `btop` | `~/.config/btop/` | Vim keys, braille graphs, transparent background. |
| `opencode` | `~/.config/opencode/` | AI provider configuration, model definitions, custom agents and commands. |

The remaining stow packages (awesome, qtile, hyprland, picom, mako, rofi, gtk, xorg, fonts, distrobox, heroic) are **Linux-only** and do not apply on macOS.

### Post-Installation

**Set fish as default shell:**

```sh
echo $(which fish) | sudo tee -a /etc/shells
chsh -s $(which fish)
```

**First fish session** automatically bootstraps fisher and installs all plugins (tide, nvm.fish, repojump) via `conf.d/dotfiles_bootstrap.fish`. Tide will prompt for initial configuration.

**Start PostgreSQL:**

```sh
brew services start postgresql@14
```

**Start Docker (via colima):**

```sh
colima start
```

---

## Arch Linux + [AwesomeWM](https://awesomewm.org/)

Setup instructions for Arch Linux.

### Required Software

**Arch Official Repository**

```sh
sudo pacstrap /mnt awesome axel base base-devel bluez bluez-utils btop cpupower docker efibootmgr exa firefox fish git gnome-keyring grub hyprland intel-ucode kitty lazygit sddm linux linux-firmware linux-headers fastfetch neovim networkmanager nvidia openssh pacman-contrib pipewire-alsa pipewire-jack pipewire-pulse ripgrep wofi steam stow ttf-ibm-plex ttf-ibmplex-mono-nerd unzip waybar
```

**Arch User Repository**

```fish
# An AUR Helper Written in Go
git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
makepkg -si
cd ..
rm -rf yay-bin

# Dependencies
yay -Sy ttf-symbola-free spotify notion-app slack-desktop protonup-rs
```

### Dotfiles

```fish
git clone git@github.com:luisalcarasr/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
stow .
```

## Troubleshooting and Enhancements

### Disabling mouse acceleration (X11)

To completely disable any sort of acceleration/deceleration, create the following file:

```fish
vi /etc/X11/xorg.conf.d/50-mouse-acceleration.conf
```

```conf
Section "InputClass"
	Identifier "My Mouse"
	MatchIsPointer "yes"
	Option "AccelerationProfile" "-1"
	Option "AccelerationScheme" "none"
	Option "AccelSpeed" "-1"
EndSection
```

## References

- https://www.atlassian.com/git/tutorials/dotfiles
- https://wiki.archlinux.org/title/xorg
- https://wiki.archlinux.org/title/lightdm
