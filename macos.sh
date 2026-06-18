#!/usr/bin/env bash
# =============================================================================
# macos.sh — macOS workstation setup
#
# Installs:
#   1. Homebrew (if not already installed)
#   2. Homebrew taps
#   3. Homebrew formulae grouped by category
#   4. Homebrew casks (GUI applications)
#   5. Post-install: colima with 8 GB RAM
#
# Usage:
#   bash macos.sh
#   bash <(curl -sL https://raw.githubusercontent.com/luisalcarasr/dotfiles/main/macos.sh)
#
# Adding packages:
#   - Formulae: append the package name to the relevant PACKAGES_* array below
#   - Casks:    append the cask name to the CASKS array below
#   - Taps:     append the tap name to the TAPS array below
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

# Returns 0 if the Homebrew formula is installed.
is_formula_installed() { brew list --formula "$1" &>/dev/null 2>&1; }

# Returns 0 if the Homebrew cask is installed.
is_cask_installed() { brew list --cask "$1" &>/dev/null 2>&1; }

# Returns 0 if the Homebrew tap is already added.
is_tap_added() { brew tap --list 2>/dev/null | grep -qx "$1"; }

# Installs a group of formulae, skipping already-installed ones.
# Collects missing formulae and installs them in a single brew call.
install_formula_group() {
  local group_name="$1"; shift
  local packages=("$@")
  local to_install=()

  log_info "Checking group: ${group_name}"

  for pkg in "${packages[@]}"; do
    if is_formula_installed "$pkg"; then
      log_skip "${pkg}"
    else
      log_info "Queued for install: ${pkg}"
      to_install+=("$pkg")
    fi
  done

  if [[ ${#to_install[@]} -gt 0 ]]; then
    brew install "${to_install[@]}"
    for pkg in "${to_install[@]}"; do
      log_ok "${pkg}"
    done
  else
    log_ok "All packages in '${group_name}' already installed."
  fi
}

# =============================================================================
# 1. HOMEBREW
# =============================================================================
log_section "🍺  Homebrew"

if command -v brew &>/dev/null; then
  log_skip "Homebrew already installed."
else
  log_info "Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  log_ok "Homebrew installed."

  # Add brew to PATH for the current session (Apple Silicon path)
  if [[ -f "/opt/homebrew/bin/brew" ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -f "/usr/local/bin/brew" ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  fi
fi

# =============================================================================
# 2. TAPS
# -----------------------------------------------------------------------------
# To add a tap: append it to the TAPS array below.
# =============================================================================
log_section "🚰  Homebrew Taps"

TAPS=(
  deskflow/tap       # Deskflow KVM — share keyboard and mouse across machines
  hashicorp/tap      # HashiCorp tools (Terraform, Vault, etc.)
  homebrew/services  # Manage background daemons with brew services
)

for tap in "${TAPS[@]%%  *}"; do
  # Strip inline comment if present
  tap_name="${tap%% #*}"
  tap_name="${tap_name%% *}"  # trim trailing whitespace
  if is_tap_added "$tap_name"; then
    log_skip "tap: ${tap_name}"
  else
    log_info "Adding tap: ${tap_name}"
    brew tap "$tap_name"
    log_ok "tap: ${tap_name}"
  fi
done

# =============================================================================
# 3. FORMULAE
# -----------------------------------------------------------------------------
# To add a package: append its name to the relevant array.
# Package names follow the exact Homebrew formula naming convention.
# =============================================================================
log_section "🛠️   Homebrew Formulae"

# Interactive shell, terminal multiplexer and navigation
PACKAGES_SHELL=(
  fish        # Primary shell with Tide prompt and fisher plugin manager
  tmux        # Terminal multiplexer with persistent sessions and panes
  zoxide      # Smart cd replacement that learns frequent directories
  fzf         # Interactive fuzzy finder for files, history and more
  fastfetch   # System info display on terminal open (neofetch alternative)
)

# Primary text editor and language servers
PACKAGES_EDITOR=(
  neovim        # Primary editor — LazyVim with LSP, treesitter, GitHub Dark theme
  rust-analyzer # Rust LSP server (autocompletion, diagnostics, refactoring)
)

# Modern CLI replacements and productivity tools
PACKAGES_CLI=(
  bat      # cat replacement with syntax highlighting and line numbers
  eza      # ls replacement with colors, icons and tree view
  fd       # find replacement — faster, respects .gitignore
  ripgrep  # Ultra-fast grep replacement (used by neovim Telescope)
  tree     # Directory structure visualization
  jq       # Command-line JSON processor and formatter
  glow     # Terminal Markdown renderer with colors
  pandoc   # Universal document converter (Markdown, HTML, PDF, DOCX)
  watch    # Runs a command periodically with updated output
  btop     # Interactive system monitor (CPU, RAM, disk, network)
  poppler  # PDF utilities (pdftotext, pdfinfo, etc.)
  imagemagick # Image processing — required by image.nvim for inline Jupyter plots
)

# Git TUI, GitLab CLI, security and dotfile management
PACKAGES_GIT=(
  lazygit   # Full Git TUI — visual commits, staging, rebase, conflict resolution
  glab      # Official GitLab CLI — MRs, issues, CI/CD pipelines from terminal
  gitleaks  # Repository secrets scanner — detects leaked API keys and tokens
  stow      # Symlink manager — core of the dotfiles system
  gnupg     # GPG encryption — commit signing and key management
)

# Container runtime and orchestration (Docker Desktop alternative)
PACKAGES_CONTAINERS=(
  colima           # Lightweight container runtime for macOS (replaces Docker Desktop)
  docker           # Container engine CLI — connects to colima daemon
  docker-compose   # Multi-container orchestration via docker-compose.yml
  docker-buildx    # Extended Docker build with multi-platform support
  qemu             # Machine emulator — dependency of colima/lima
  lazydocker       # Docker TUI — visual dashboard for containers, images and volumes
)

# Language runtimes and version/tool managers
PACKAGES_LANGS=(
  python@3.12   # Python 3.12 LTS runtime (supported until 2028)
  pipx          # Install Python CLI tools in isolated virtual environments
  openjdk@21    # Java 21 JDK LTS — runtime and compiler
  # Node.js is managed by nvm.fish (fish plugin) — not installed via Homebrew
)

# Networking and download utilities
PACKAGES_NETWORK=(
  curl   # URL data transfer — newer than macOS system curl, with HTTP/3 support
  wget   # HTTP/FTP downloader for recursive downloads
  axel   # Accelerated downloader with multiple simultaneous connections
  nmap   # Network scanner — host discovery, open ports, service detection
)

# Local development database
PACKAGES_DB=(
  postgresql@14   # PostgreSQL 14 — local relational database, managed via brew services
)

# System utilities
PACKAGES_UTILS=(
  unzip   # ZIP decompressor — more complete than the macOS system version
)

# Install all formula groups
declare -A FORMULA_GROUPS=(
  ["shell"]="${PACKAGES_SHELL[*]}"
  ["editor"]="${PACKAGES_EDITOR[*]}"
  ["cli"]="${PACKAGES_CLI[*]}"
  ["git"]="${PACKAGES_GIT[*]}"
  ["containers"]="${PACKAGES_CONTAINERS[*]}"
  ["languages"]="${PACKAGES_LANGS[*]}"
  ["network"]="${PACKAGES_NETWORK[*]}"
  ["database"]="${PACKAGES_DB[*]}"
  ["utils"]="${PACKAGES_UTILS[*]}"
)

# Process in a defined order (associative arrays are unordered in bash)
for group_name in shell editor cli git containers languages network database utils; do
  IFS=' ' read -r -a pkgs <<< "${FORMULA_GROUPS[$group_name]}"
  install_formula_group "$group_name" "${pkgs[@]}"
done

# =============================================================================
# 4. CASKS (GUI Applications)
# -----------------------------------------------------------------------------
# To add a cask: append its name to the CASKS array below.
# Find cask names at: https://formulae.brew.sh/cask/
# =============================================================================
log_section "🖥️   Homebrew Casks"

CASKS=(
  kitty    # Primary terminal emulator — GPU-accelerated, GitHub Dark, Operator Mono Lig
  ghostty  # Alternative GPU-accelerated terminal emulator
  mos      # Improves external mouse scrolling on macOS (smoothing + direction control)
  insomnia # REST and GraphQL API client — design, test and document endpoints
  gimp     # Professional open-source image editor
  quarto   # Scientific publishing system — required by jupytext quarto style + preview
)

for cask in "${CASKS[@]}"; do
  if is_cask_installed "$cask"; then
    log_skip "cask: ${cask}"
  else
    log_info "Installing cask: ${cask}"
    brew install --cask "$cask"
    log_ok "cask: ${cask}"
  fi
done

# =============================================================================
# 5. POST-INSTALL
# =============================================================================
log_section "🏁  Post-Install"

# Start colima with 8 GB RAM for comfortable container workloads
if command -v colima &>/dev/null; then
  if colima status 2>/dev/null | grep -q "running"; then
    log_skip "colima already running."
  else
    log_info "Starting colima (4 CPU, 8 GB RAM, 60 GB disk)..."
    colima start --cpu 4 --memory 8 --disk 60
    log_ok "colima started."
  fi
fi

# Neovim Python host for Jupyter (molten-nvim remote plugin). A dedicated venv
# lives inside the nvim config dir and is provisioned from requirements.txt.
# Idempotent: skips venv creation if it already exists, always syncs reqs.
NVIM_VENV="${HOME}/.config/nvim/.venv"
NVIM_REQS="${HOME}/.config/nvim/requirements.txt"
if command -v python3.12 &>/dev/null; then
  if [[ -d "$NVIM_VENV" ]]; then
    log_skip "Neovim Python venv already exists."
  else
    log_info "Creating Neovim Python venv (Jupyter host)..."
    python3.12 -m venv "$NVIM_VENV"
    "${NVIM_VENV}/bin/pip" install --quiet --upgrade pip
    log_ok "Neovim Python venv created."
  fi
  if [[ -f "$NVIM_REQS" ]]; then
    log_info "Installing Neovim Python requirements..."
    "${NVIM_VENV}/bin/pip" install --quiet -r "$NVIM_REQS"
    log_ok "Neovim Python requirements installed."
  fi
else
  log_skip "python3.12 not found; skipping Neovim Jupyter venv."
fi

echo ""
log_ok "════════════════════════════════════"
log_ok "  🍎 macOS setup complete!"
log_ok "════════════════════════════════════"
echo ""
echo -e "${_BOLD}🚀 Next steps:${_RESET}"
echo "  1. Set fish as your default shell:"
echo "       echo \$(which fish) | sudo tee -a /etc/shells"
echo "       chsh -s \$(which fish)"
echo "  2. Clone and deploy dotfiles:"
echo "       git clone git@github.com:luisalcarasr/dotfiles.git ~/.dotfiles"
echo "       cd ~/.dotfiles && stow fish nvim tmux kitty git btop opencode"
echo "  3. Start PostgreSQL (when needed):"
echo "       brew services start postgresql@14"
echo "  4. Jupyter in Neovim:"
echo "       - Run ':UpdateRemotePlugins' once in nvim after first launch"
echo "       - Register a kernel per project env: 'python -m ipykernel install --user'"
echo ""
