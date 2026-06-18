#!/usr/bin/env bash
# =============================================================================
# ubuntu.sh — Ubuntu workstation setup
#
# Installs:
#   1. APT package index refresh
#   2. APT packages grouped by category
#   3. Third-party tools not in the default Ubuntu repos (eza, lazygit)
#   4. Snap GUI applications (Ubuntu does not use Flatpak here)
#   5. Post-install: binary name shims (batcat/fdfind)
#
# Usage:
#   bash ubuntu.sh
#   bash <(curl -sL https://raw.githubusercontent.com/luisalcarasr/dotfiles/main/ubuntu.sh)
#
# Adding packages:
#   - APT:  append the package name to the relevant PACKAGES_* array below
#   - Snap: append the snap name to the SNAP_APPS array below
#
# Notes on Ubuntu package quirks (different from Fedora):
#   - bat installs as `batcat`; we symlink it to `bat` in ~/.local/bin
#   - fd-find installs as `fdfind`; we symlink it to `fd` in ~/.local/bin
#   - eza and lazygit are not in the default repos — installed from upstream
# =============================================================================

set -euo pipefail

# -----------------------------------------------------------------------------
# Colors & logging helpers
# -----------------------------------------------------------------------------
_RED='\033[0;31m'
_GREEN='\033[0;32m'
_YELLOW='\033[1;33m'
_BLUE='\033[0;34m'
_BOLD='\033[1m'
_RESET='\033[0m'

log_info()    { echo -e "${_BLUE}${_BOLD}[INFO]${_RESET}  🔹 $*"; }
log_ok()      { echo -e "${_GREEN}${_BOLD}[OK]${_RESET}    ✅ $*"; }
log_skip()    { echo -e "${_YELLOW}${_BOLD}[SKIP]${_RESET}  ⏭️  $*"; }
log_error()   { echo -e "${_RED}${_BOLD}[ERR]${_RESET}   ❌ $*" >&2; }
log_section() { echo -e "\n${_BOLD}══════════════════════════════════════${_RESET}\n${_BOLD}  $*${_RESET}\n${_BOLD}══════════════════════════════════════${_RESET}"; }

# Returns 0 if the APT package is installed, 1 otherwise.
is_apt_installed() { dpkg-query -W -f='${Status}' "$1" 2>/dev/null | grep -q "ok installed"; }

# Returns 0 if a command exists in PATH.
has_command() { command -v "$1" &>/dev/null; }

# Returns 0 if the snap is installed, 1 otherwise.
is_snap_installed() {
  snap list "$1" &>/dev/null 2>&1
}

# Installs a list of APT packages, skipping already-installed ones.
# Collects missing packages and installs them in a single apt call.
install_apt_group() {
  local group_name="$1"; shift
  local packages=("$@")
  local to_install=()

  log_info "Checking group: ${group_name}"

  for pkg in "${packages[@]}"; do
    if is_apt_installed "$pkg"; then
      log_skip "${pkg}"
    else
      log_info "Queued for install: ${pkg}"
      to_install+=("$pkg")
    fi
  done

  if [[ ${#to_install[@]} -gt 0 ]]; then
    sudo apt-get install -y "${to_install[@]}"
    for pkg in "${to_install[@]}"; do
      log_ok "${pkg}"
    done
  else
    log_ok "All packages in '${group_name}' already installed."
  fi
}

# Installs a snap if not already present.
# A trailing " --classic" or " --edge" etc. in the entry is passed to snap.
install_snap_app() {
  local entry="$1"
  local name="${entry%% *}"
  local extra_flags=""
  if [[ "$entry" != "$name" ]]; then
    extra_flags="${entry#"$name" }"
  fi

  if is_snap_installed "$name"; then
    log_skip "snap: ${name}"
  else
    log_info "Installing snap: ${name}"
    # shellcheck disable=SC2086
    sudo snap install "$name" $extra_flags
    log_ok "snap: ${name}"
  fi
}

# =============================================================================
# 1. APT INDEX
# =============================================================================
log_section "📦  APT Index"

log_info "Refreshing package index..."
sudo apt-get update -y
log_ok "Package index refreshed."

# =============================================================================
# 2. APT PACKAGES
# -----------------------------------------------------------------------------
# To add a package: append its name to the relevant array.
# Package names follow the exact apt/dpkg naming convention.
# =============================================================================
log_section "🛠️   APT Packages"

# Base tools and dotfile management
PACKAGES_SYSTEM=(
  stow   # Symlink manager — core of the dotfiles system
  git    # Version control
  curl   # URL data transfer
  wget   # HTTP/FTP downloader
)

# Interactive shell, navigation and system info
PACKAGES_SHELL=(
  fish        # Primary shell
  zoxide      # Smart cd replacement (learns frequent dirs)
  fzf         # Interactive fuzzy finder
  fastfetch   # System info display (neofetch alternative)
)

# Primary text editor
PACKAGES_EDITOR=(
  neovim   # LazyVim-based editor with LSP, treesitter, GitHub Dark theme
)

# Modern CLI replacements and monitors
# NOTE: bat -> batcat, fd-find -> fdfind on Ubuntu (shimmed in post-install).
#       eza is not packaged in the default repos (installed separately below).
PACKAGES_CLI=(
  bat        # cat with syntax highlighting (binary: batcat)
  fd-find    # find replacement (binary: fdfind)
  ripgrep    # Ultra-fast grep (used by neovim Telescope)
  tree       # Directory structure visualizer
  jq         # Command-line JSON processor
  btop       # Interactive system monitor (CPU, RAM, disk, network)
  unzip      # ZIP extraction utility
)

# Daemonless containers and distro environments
PACKAGES_CONTAINERS=(
  podman      # Daemonless container engine (Docker-compatible CLI)
  distrobox   # Containerized terminal environments using podman
)

# Python runtime and isolated tool installer
PACKAGES_LANGS=(
  python3       # Python 3 runtime
  python3-pip   # Python package installer
  pipx          # Install Python CLI tools in isolated virtual environments
)

for group_var in \
  "system:${PACKAGES_SYSTEM[*]}" \
  "shell:${PACKAGES_SHELL[*]}" \
  "editor:${PACKAGES_EDITOR[*]}" \
  "cli:${PACKAGES_CLI[*]}" \
  "containers:${PACKAGES_CONTAINERS[*]}" \
  "languages:${PACKAGES_LANGS[*]}"; do
  group_name="${group_var%%:*}"
  IFS=' ' read -r -a pkgs <<< "${group_var#*:}"
  install_apt_group "$group_name" "${pkgs[@]}"
done

# =============================================================================
# 3. THIRD-PARTY TOOLS (not in default Ubuntu repos)
# -----------------------------------------------------------------------------
# eza and lazygit are not packaged by Ubuntu. They are installed from their
# official sources. Each block is idempotent (skips if already present).
# =============================================================================
log_section "🌍  Third-party Tools"

# eza — modern ls — from the official gierens.de apt repository
if has_command eza; then
  log_skip "eza"
else
  log_info "Adding eza apt repository..."
  sudo mkdir -p /etc/apt/keyrings
  wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc \
    | sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg
  echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" \
    | sudo tee /etc/apt/sources.list.d/gierens.list >/dev/null
  sudo chmod 644 /etc/apt/keyrings/gierens.gpg /etc/apt/sources.list.d/gierens.list
  sudo apt-get update -y
  sudo apt-get install -y eza
  log_ok "eza"
fi

# lazygit — Git TUI — from the latest GitHub release tarball
if has_command lazygit; then
  log_skip "lazygit"
else
  log_info "Installing lazygit from GitHub releases..."
  LAZYGIT_VERSION=$(curl -fsSL "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" \
    | grep -Po '"tag_name": *"v\K[^"]*')
  curl -fsSLo /tmp/lazygit.tar.gz \
    "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_${LAZYGIT_VERSION}_Linux_x86_64.tar.gz"
  tar -xf /tmp/lazygit.tar.gz -C /tmp lazygit
  sudo install /tmp/lazygit /usr/local/bin
  rm -f /tmp/lazygit /tmp/lazygit.tar.gz
  log_ok "lazygit ${LAZYGIT_VERSION}"
fi

# =============================================================================
# 4. SNAP (GUI Applications)
# -----------------------------------------------------------------------------
# Ubuntu uses snap for GUI apps (Flatpak is intentionally not used here).
# snapd ships with Ubuntu Desktop by default; install it just in case.
#
# To add an app: append its snap name to the SNAP_APPS array below.
#   - Add " --classic" after the name for snaps that need classic confinement.
# Find snaps at: https://snapcraft.io
# =============================================================================
log_section "📦  Snap"

# Ensure snapd is installed (present by default on Ubuntu Desktop)
if is_apt_installed snapd; then
  log_skip "snapd"
else
  log_info "Installing snapd..."
  sudo apt-get install -y snapd
  log_ok "snapd"
fi

SNAP_APPS=(
  "brave"   # Brave — privacy-focused Chromium browser
)

for entry in "${SNAP_APPS[@]}"; do
  # Strip inline comment, keep name and any flags (e.g. "code --classic")
  entry="${entry%% #*}"
  entry="${entry%"${entry##*[![:space:]]}"}"  # trim trailing whitespace
  install_snap_app "$entry"
done

# =============================================================================
# 5. POST-INSTALL
# -----------------------------------------------------------------------------
# Ubuntu ships bat as `batcat` and fd-find as `fdfind` to avoid name clashes.
# The dotfiles (and neovim plugins) expect `bat` and `fd`, so create shims in
# ~/.local/bin, which fish adds to PATH via paths_scanner.fish.
# =============================================================================
log_section "🏁  Post-Install"

mkdir -p "$HOME/.local/bin"

if has_command batcat && ! has_command bat; then
  ln -sf "$(command -v batcat)" "$HOME/.local/bin/bat"
  log_ok "shim: bat -> batcat"
else
  log_skip "bat shim not needed"
fi

if has_command fdfind && ! has_command fd; then
  ln -sf "$(command -v fdfind)" "$HOME/.local/bin/fd"
  log_ok "shim: fd -> fdfind"
else
  log_skip "fd shim not needed"
fi

echo ""
log_ok "════════════════════════════════════"
log_ok "  🐧 Ubuntu setup complete!"
log_ok "════════════════════════════════════"
echo ""
echo -e "${_BOLD}🚀 Next steps:${_RESET}"
echo "  1. Set fish as your default shell:"
echo "       echo \$(which fish) | sudo tee -a /etc/shells"
echo "       chsh -s \$(which fish)"
echo "  2. Clone and deploy dotfiles:"
echo "       git clone git@github.com:luisalcarasr/dotfiles.git ~/.dotfiles"
echo "       cd ~/.dotfiles && stow ."
echo ""
