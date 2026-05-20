#!/usr/bin/env bash
# setup.sh — Install QuickShell + dependencies for the hyprland shell config.
# Target: Arch Linux with yay (AUR helper).
# Run as your normal user (sudo will be invoked when needed).

set -euo pipefail

# ── Helpers ─────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

info()    { echo -e "${GREEN}[setup]${NC} $*"; }
warn()    { echo -e "${YELLOW}[warn]${NC}  $*"; }
error()   { echo -e "${RED}[error]${NC} $*"; exit 1; }
confirm() {
    read -rp "$1 [y/N] " ans
    [[ "${ans,,}" == "y" ]]
}

# ── Preflight checks ─────────────────────────────────────────────────────────
[[ "$(uname -s)" == "Linux" ]] || error "This script is for Linux (Arch) only."

command -v pacman &>/dev/null || error "pacman not found — are you on Arch Linux?"
command -v yay    &>/dev/null || warn "yay not found — AUR packages will be skipped."

info "Starting setup for QuickShell + Hyprland shell"
echo

# ── 1. Official repo packages ────────────────────────────────────────────────
info "Installing pacman packages…"

PACMAN_PKGS=(
    # Wayland / Hyprland ecosystem
    hyprland
    hyprlock
    hypridle
    hyprsunset
    hyprpicker
    xdg-desktop-portal-hyprland
    xdg-desktop-portal-gtk

    # Wayland utilities
    wl-clipboard
    grim
    slurp

    # Audio
    pipewire
    pipewire-pulse
    wireplumber

    # Network
    networkmanager

    # System utilities
    upower
    brightnessctl
    playerctl
    flatpak
    jq
    curl
    bc

    # QuickShell — official Extra repo (no AUR needed)
    quickshell

    # Fonts — Adwaita (GNOME 50+ system font, ships Adwaita Sans + Adwaita Mono)
    adwaita-fonts
    # Nerd font for bar icons (battery, network, volume glyphs)
    ttf-jetbrains-mono-nerd

    # GTK / icon theme
    adwaita-icon-theme
    gnome-themes-extra

    # Notification daemon (lightweight, no panel needed)
    mako

    # Terminal
    kitty

    # Shell
    fish
)

sudo pacman -S --needed --noconfirm "${PACMAN_PKGS[@]}"

echo

# ── 2. AUR packages (via yay) ────────────────────────────────────────────────
# Currently no AUR packages are required — quickshell is in the official Extra repo.
# This section is kept for future optional additions.
if command -v yay &>/dev/null; then
    info "yay available — no AUR packages required for this config."
fi

echo

# ── 3. Flatpak setup ─────────────────────────────────────────────────────────
info "Ensuring Flathub remote is configured…"
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo || true

echo

# ── 4. Enable system services ────────────────────────────────────────────────
info "Enabling NetworkManager service…"
sudo systemctl enable --now NetworkManager || warn "NetworkManager already running or failed."

info "Enabling Bluetooth service…"
sudo systemctl enable --now bluetooth || warn "bluetooth already running or failed."

echo

# ── 5. Stow the config ───────────────────────────────────────────────────────
DOTFILES_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HYPRLAND_DIR="$DOTFILES_ROOT/hyprland"

if command -v stow &>/dev/null; then
    info "Symlinking config with GNU Stow…"
    stow --dir="$DOTFILES_ROOT" --target="$HOME" hyprland
else
    warn "GNU Stow not found. Copying config files manually…"
    mkdir -p "$HOME/.config"
    cp -rv "$HYPRLAND_DIR/.config/"* "$HOME/.config/"
fi

echo

# ── 6. Create QuickShell config state directory ───────────────────────────────
info "Creating QuickShell state directory…"
mkdir -p "$HOME/.config/quickshell/shell"

echo

# ── 7. Set Adwaita GTK theme ─────────────────────────────────────────────────
info "Applying Adwaita Dark GTK theme…"
if command -v gsettings &>/dev/null; then
    gsettings set org.gnome.desktop.interface gtk-theme      "Adwaita-dark" 2>/dev/null || true
    gsettings set org.gnome.desktop.interface icon-theme     "Adwaita"      2>/dev/null || true
    gsettings set org.gnome.desktop.interface cursor-theme   "Adwaita"      2>/dev/null || true
    gsettings set org.gnome.desktop.interface font-name      "Adwaita Sans 11" 2>/dev/null || true
    gsettings set org.gnome.desktop.interface color-scheme   "prefer-dark"  2>/dev/null || true
else
    warn "gsettings not available; set GTK theme manually in ~/.config/gtk-3.0/settings.ini"
    mkdir -p "$HOME/.config/gtk-3.0"
    cat > "$HOME/.config/gtk-3.0/settings.ini" <<EOF
[Settings]
gtk-theme-name=Adwaita-dark
gtk-icon-theme-name=Adwaita
gtk-cursor-theme-name=Adwaita
gtk-font-name=Adwaita Sans 11
gtk-application-prefer-dark-theme=1
EOF
    mkdir -p "$HOME/.config/gtk-4.0"
    cat > "$HOME/.config/gtk-4.0/settings.ini" <<EOF
[Settings]
gtk-theme-name=Adwaita-dark
gtk-icon-theme-name=Adwaita
gtk-cursor-theme-name=Adwaita
gtk-font-name=Adwaita Sans 11
gtk-application-prefer-dark-theme=1
EOF
fi

echo

# ── 8. Summary ───────────────────────────────────────────────────────────────
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
info "Setup complete!"
echo
echo "  Quickshell starts automatically via hyprland.conf exec-once."
echo "  Keybinds:"
echo "    Super + Space    → toggle launcher"
echo "    Super + Return   → kitty terminal"
echo "    Super + Q        → close window"
echo
echo "  Change accent color at runtime:"
echo "    Edit ~/.config/quickshell/shell/config.json"
echo "    and set \"accentKey\" to one of:"
echo "    blue green yellow orange red purple brown"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
