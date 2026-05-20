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

The remaining stow packages (awesome, hyprland, picom, rofi, gtk, xorg, fonts, distrobox, heroic) are **Linux-only** and do not apply on macOS.

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

## Arch Linux + [Hyprland](https://hyprland.org/)

Setup instructions for Arch Linux. Boot the live ISO and run:

```sh
bash <(curl -sL https://raw.githubusercontent.com/luisalcarasr/dotfiles/main/arch-linux-setup.sh)
```

or with wget:

```sh
bash <(wget -qO- https://raw.githubusercontent.com/luisalcarasr/dotfiles/main/arch-linux-setup.sh)
```

### Dotfiles

```fish
git clone git@github.com:luisalcarasr/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
stow .
```

### Packages

Explicitly installed packages (`pacman -Qe`):

#### System

| Package | Purpose |
|---|---|
| **base** | Core Arch Linux system group |
| **base-devel** | Build tools (gcc, make, etc.) |
| **linux** | Linux kernel |
| **linux-headers** | Kernel headers for module compilation |
| **linux-firmware** | Firmware for hardware devices |
| **intel-ucode** | Intel CPU microcode updates |
| **grub** | Bootloader |
| **efibootmgr** | EFI boot entry manager |
| **cpupower** | CPU frequency scaling and management |

#### Display & GPU

| Package | Purpose |
|---|---|
| **hyprland** | Wayland compositor (primary WM) |
| **nvidia-open** | Open-source NVIDIA GPU driver |
| **sddm** | Display manager (login screen) |
| **wofi** | Application launcher |

#### Audio

| Package | Purpose |
|---|---|
| **pipewire-alsa** | ALSA compatibility layer for PipeWire |
| **pipewire-jack** | JACK compatibility layer for PipeWire |
| **pipewire-pulse** | PulseAudio compatibility layer for PipeWire |

#### Bluetooth

| Package | Purpose |
|---|---|
| **bluez** | Bluetooth protocol stack |
| **bluez-utils** | Bluetooth CLI utilities (bluetoothctl) |

#### Networking

| Package | Purpose |
|---|---|
| **networkmanager** | Network management daemon |
| **openssh** | SSH client and server |
| **axel** | Accelerated downloader (multi-connection) |

#### Shell & Terminal

| Package | Purpose |
|---|---|
| **fish** | Primary shell (interactive and scripting) |
| **kitty** | GPU-accelerated terminal emulator |
| **quickshell** | Quick shell launcher |
| **whisker-shell-git** | Modern shell menu (AUR/git) |
| **less** | Terminal pager |

#### Editor

| Package | Purpose |
|---|---|
| **neovim** | Primary text editor |

#### Development & CLI Tools

| Package | Purpose |
|---|---|
| **git** | Version control system |
| **lazygit** | TUI for Git operations |
| **stow** | Symlink manager (dotfile deployment) |
| **fastfetch** | System info display |
| **eza** | Modern `ls` replacement |
| **btop** | Interactive system monitor |
| **ripgrep** | Fast text search (used by neovim) |
| **unzip** | ZIP extraction utility |
| **pacman-contrib** | Pacman contrib scripts (checkupdates, etc.) |

#### Fonts & Themes

| Package | Purpose |
|---|---|
| **adw-gtk-theme** | Libadwaita GTK theme |
| **adwaita-fonts** | Adwaita font family |
| **ttf-adwaitamono-nerd** | Adwaita Mono Nerd Font (nerdfont patched) |

#### Containers

| Package | Purpose |
|---|---|
| **podman** | Daemonless container engine |
| **distrobox** | Containerized terminal environments |

#### Desktop & GUI

| Package | Purpose |
|---|---|
| **flatpak** | Application sandboxing framework |
| **xdg-desktop-portal-gtk** | GTK portal backend |
| **xdg-user-dirs** | Standard XDG user directories |
| **gnome-keyring** | Credential and secret storage |
| **curseforge** | Minecraft mod manager |

#### AUR Packages

| Package | Purpose |
|---|---|
| **yay-bin** | AUR helper (pre-compiled binary) |
| **opencode** | AI coding agent |

```fish
sudo pacman -S --needed - < packages.txt
```

### Post-install

Enable services:

```fish
sudo systemctl enable --now NetworkManager bluetooth
```

Flatpak:

```fish
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install -y flathub org.gtk.Gtk3theme.adw-gtk3-dark
```

Apply GTK settings:

```fish
gsettings set org.gnome.desktop.interface gtk-theme    "adw-gtk3-dark"
gsettings set org.gnome.desktop.interface icon-theme   "Adwaita"
gsettings set org.gnome.desktop.interface cursor-theme "Adwaita"
gsettings set org.gnome.desktop.interface font-name    "Adwaita Sans 11"
gsettings set org.gnome.desktop.interface color-scheme "prefer-dark"
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
