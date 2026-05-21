#!/usr/bin/env bash
# =============================================================================
# fedora.sh — Fedora KDE workstation setup
#
# Installs:
#   1. RPM Fusion repositories (free + nonfree)
#   2. NVIDIA open driver (akmod-nvidia) — skipped if no NVIDIA GPU detected
#   3. DNF packages grouped by category
#   4. Flatpak + Flathub + GUI applications
#   5. NVIDIA Flatpak runtimes (GL 64-bit, GL32 32-bit, VAAPI)
#   6. System services
#
# Usage:
#   bash fedora.sh
#   bash <(curl -sL https://raw.githubusercontent.com/luisalcarasr/dotfiles/main/fedora.sh)
#
# Adding packages:
#   - DNF:     append the package name to the relevant PACKAGES_* array below
#   - Flatpak: append the Flatpak app ID to the FLATPAK_APPS array below
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

# Returns 0 if the RPM package is installed, 1 otherwise.
is_dnf_installed() { rpm -q "$1" &>/dev/null; }

# Returns 0 if the Flatpak app ID is installed, 1 otherwise.
is_flatpak_installed() {
  flatpak list --app --columns=application 2>/dev/null | grep -qx "$1"
}

# Installs a list of DNF packages, skipping already-installed ones.
# Collects missing packages and installs them in a single dnf call.
install_dnf_group() {
  local group_name="$1"; shift
  local packages=("$@")
  local to_install=()

  log_info "Checking group: ${group_name}"

  for pkg in "${packages[@]}"; do
    if is_dnf_installed "$pkg"; then
      log_skip "${pkg}"
    else
      log_info "Queued for install: ${pkg}"
      to_install+=("$pkg")
    fi
  done

  if [[ ${#to_install[@]} -gt 0 ]]; then
    sudo dnf install -y "${to_install[@]}"
    for pkg in "${to_install[@]}"; do
      log_ok "${pkg}"
    done
  else
    log_ok "All packages in '${group_name}' already installed."
  fi
}

# Installs a Flatpak app if not already present.
install_flatpak_app() {
  local app_id="$1"
  if is_flatpak_installed "$app_id"; then
    log_skip "flatpak: ${app_id}"
  else
    log_info "Installing flatpak: ${app_id}"
    flatpak install -y flathub "$app_id"
    log_ok "flatpak: ${app_id}"
  fi
}

# =============================================================================
# 1. RPM FUSION REPOSITORIES
# =============================================================================
log_section "📦  RPM Fusion"

FEDORA_VERSION=$(rpm -E %fedora)

RPM_FUSION_FREE="rpmfusion-free-release"
RPM_FUSION_NONFREE="rpmfusion-nonfree-release"

if is_dnf_installed "$RPM_FUSION_FREE"; then
  log_skip "${RPM_FUSION_FREE}"
else
  log_info "Enabling RPM Fusion Free..."
  sudo dnf install -y \
    "https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-${FEDORA_VERSION}.noarch.rpm"
  log_ok "${RPM_FUSION_FREE}"
fi

if is_dnf_installed "$RPM_FUSION_NONFREE"; then
  log_skip "${RPM_FUSION_NONFREE}"
else
  log_info "Enabling RPM Fusion Non-Free..."
  sudo dnf install -y \
    "https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-${FEDORA_VERSION}.noarch.rpm"
  log_ok "${RPM_FUSION_NONFREE}"
fi

# =============================================================================
# 2. NVIDIA OPEN DRIVER
# =============================================================================
log_section "🎮  NVIDIA Driver (open)"

if lspci 2>/dev/null | grep -qi "nvidia"; then
  log_info "NVIDIA GPU detected."

  # akmod-nvidia ships the open kernel module (requires Turing/RTX 20xx+).
  # xorg-x11-drv-nvidia-cuda provides CUDA and NVENC/NVDEC support.
  install_dnf_group "nvidia-driver" \
    akmod-nvidia \
    xorg-x11-drv-nvidia-cuda

  log_info "Waiting for kernel module to build (this may take a few minutes)..."
  sudo akmods --force
  sudo dracut --force
  log_ok "NVIDIA driver installed. A reboot is required before launching GPU applications."
else
  log_skip "No NVIDIA GPU detected — skipping driver installation."
fi

# =============================================================================
# 3. DNF PACKAGES
# -----------------------------------------------------------------------------
# To add a package: append its name to the relevant array.
# Package names follow the exact dnf/RPM naming convention.
# =============================================================================
log_section "🛠️   DNF Packages"

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
PACKAGES_CLI=(
  bat        # cat with syntax highlighting
  eza        # Modern ls with colors and icons
  fd-find    # find replacement (faster, gitignore-aware)
  ripgrep    # Ultra-fast grep (used by neovim Telescope)
  tree       # Directory structure visualizer
  jq         # Command-line JSON processor
  btop       # Interactive system monitor (CPU, RAM, disk, network)
  unzip      # ZIP extraction utility
)

# Git TUI
PACKAGES_GIT=(
  lazygit   # Full Git TUI — commits, staging, rebase, conflicts
)

# Daemonless containers and distro environments
PACKAGES_CONTAINERS=(
  podman      # Daemonless container engine (Docker-compatible CLI)
  distrobox   # Containerized terminal environments using podman
)

# Python runtime and isolated tool installer
PACKAGES_LANGS=(
  python3      # Python 3 runtime
  python3-pip  # Python package installer
  pipx         # Install Python CLI tools in isolated virtual environments
)

for group_var in \
  "system:${PACKAGES_SYSTEM[*]}" \
  "shell:${PACKAGES_SHELL[*]}" \
  "editor:${PACKAGES_EDITOR[*]}" \
  "cli:${PACKAGES_CLI[*]}" \
  "git:${PACKAGES_GIT[*]}" \
  "containers:${PACKAGES_CONTAINERS[*]}" \
  "languages:${PACKAGES_LANGS[*]}"; do
  group_name="${group_var%%:*}"
  IFS=' ' read -r -a pkgs <<< "${group_var#*:}"
  install_dnf_group "$group_name" "${pkgs[@]}"
done

# =============================================================================
# 4. FLATPAK + FLATHUB
# =============================================================================
log_section "📦  Flatpak + Flathub"

# Ensure flatpak is installed (may not be present on minimal installs)
if ! is_dnf_installed flatpak; then
  log_info "Installing flatpak..."
  sudo dnf install -y flatpak
  log_ok "flatpak"
else
  log_skip "flatpak"
fi

# Register the Flathub remote
if flatpak remotes 2>/dev/null | grep -q "^flathub"; then
  log_skip "flathub remote already configured"
else
  log_info "Adding Flathub remote..."
  flatpak remote-add --if-not-exists flathub \
    https://dl.flathub.org/repo/flathub.flatpakrepo
  log_ok "flathub remote"
fi

# 🎨 GTK theme for Flatpak apps (dark Adwaita look on KDE)
install_flatpak_app "org.gtk.Gtk3theme.adw-gtk3-dark"

# -----------------------------------------------------------------------------
# GUI Applications
# -----------------------------------------------------------------------------
# To add an app: append its Flatpak app ID to the array below.
# Find IDs at: https://flathub.org
# -----------------------------------------------------------------------------
FLATPAK_APPS=(
  com.brave.Browser            # Brave — privacy-focused Chromium browser
  com.valvesoftware.Steam      # Steam — gaming platform
  com.heroicgameslauncher.hgl  # Heroic — GOG and Epic Games launcher
  net.davidotek.pupgui2        # ProtonUp-Qt — manage Proton/Wine versions
)

for app in "${FLATPAK_APPS[@]%% #*}"; do
  install_flatpak_app "$app"
done

# -----------------------------------------------------------------------------
# Steam extras: gamescope compositor and MangoHud overlay
# -----------------------------------------------------------------------------
FLATPAK_STEAM_EXTRAS=(
  com.valvesoftware.Steam.Utility.gamescope             # Micro-compositor for Steam games
  org.freedesktop.Platform.VulkanLayer.MangoHud         # In-game performance overlay (64-bit)
  org.freedesktop.Platform.VulkanLayer.MangoHud//23.08  # MangoHud runtime 23.08
)

for app in "${FLATPAK_STEAM_EXTRAS[@]%% #*}"; do
  install_flatpak_app "$app"
done

# =============================================================================
# 5. NVIDIA FLATPAK RUNTIMES
# -----------------------------------------------------------------------------
# Steam Flatpak requires the NVIDIA GL and GL32 runtimes that exactly match
# the host driver version. Missing 32-bit runtime (GL32) will break DXVK
# and most Windows games via Proton.
# =============================================================================
log_section "🖥️   NVIDIA Flatpak Runtimes"

NVIDIA_VERSION=$(modinfo -F version nvidia 2>/dev/null || echo "")

if [[ -n "$NVIDIA_VERSION" ]]; then
  # Flatpak uses hyphens instead of dots in version strings (e.g. 550-90-07)
  NVIDIA_FLATPAK_VERSION="${NVIDIA_VERSION//./-}"

  log_info "Detected NVIDIA driver version: ${NVIDIA_VERSION}"

  NVIDIA_RUNTIMES=(
    # 64-bit OpenGL/Vulkan runtime — required by all Flatpak GPU apps
    "org.freedesktop.Platform.GL.nvidia-${NVIDIA_FLATPAK_VERSION}"
    # 32-bit OpenGL/Vulkan runtime — required by Steam, DXVK, Proton
    "org.freedesktop.Platform.GL32.nvidia-${NVIDIA_FLATPAK_VERSION}"
    # VAAPI hardware video acceleration (encode/decode)
    "org.freedesktop.Platform.VAAPI.nvidia"
  )

  for runtime in "${NVIDIA_RUNTIMES[@]}"; do
    install_flatpak_app "$runtime"
  done
else
  log_skip "No NVIDIA driver loaded — skipping NVIDIA Flatpak runtimes."
fi

# =============================================================================
# 6. SYSTEM SERVICES
# =============================================================================
log_section "⚙️   System Services"

SERVICES=(
  NetworkManager   # Network management daemon
  bluetooth        # Bluetooth stack
)

for svc in "${SERVICES[@]%% #*}"; do
  if systemctl is-enabled --quiet "$svc" 2>/dev/null; then
    log_skip "service already enabled: ${svc}"
  else
    log_info "Enabling service: ${svc}"
    sudo systemctl enable --now "$svc"
    log_ok "service enabled: ${svc}"
  fi
done

# =============================================================================
# 7. POST-INSTALL
# =============================================================================
log_section "🏁  Post-Install"

# GTK / desktop appearance (KDE respects these for GTK apps)
if command -v gsettings &>/dev/null; then
  log_info "Applying GTK settings..."
  gsettings set org.gnome.desktop.interface gtk-theme    "adw-gtk3-dark"
  gsettings set org.gnome.desktop.interface icon-theme   "Adwaita"
  gsettings set org.gnome.desktop.interface cursor-theme "Adwaita"
  gsettings set org.gnome.desktop.interface font-name    "Adwaita Sans 11"
  gsettings set org.gnome.desktop.interface color-scheme "prefer-dark"
  log_ok "GTK settings applied."
else
  log_skip "gsettings not found — skipping GTK theme configuration."
fi

echo ""
log_ok "════════════════════════════════════"
log_ok "  🐧 Fedora setup complete!"
log_ok "════════════════════════════════════"
echo ""
echo -e "${_BOLD}🚀 Next steps:${_RESET}"
echo "  1. Set fish as your default shell:"
echo "       echo \$(which fish) | sudo tee -a /etc/shells"
echo "       chsh -s \$(which fish)"
echo "  2. Clone and deploy dotfiles:"
echo "       git clone git@github.com:luisalcarasr/dotfiles.git ~/.dotfiles"
echo "       cd ~/.dotfiles && stow ."
if [[ -n "${NVIDIA_VERSION:-}" ]]; then
  echo "  3. Reboot to load the NVIDIA kernel module:"
  echo "       sudo reboot"
fi
echo ""
