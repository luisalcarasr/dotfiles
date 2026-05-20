#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Arch Linux Setup Script
# =============================================================================

# --- Colors for output -------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() { echo -e "${GREEN}[INFO]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

# =============================================================================
# Step 1: Network connectivity (Wi-Fi via iwctl if needed)
# =============================================================================

check_connectivity() {
  info "Checking internet connectivity..."
  if ping -c 3 -W 5 kernel.org &>/dev/null; then
    info "Internet connection is working."
    return 0
  else
    warn "No internet connection detected."
    return 1
  fi
}

setup_wifi() {
  info "Setting up Wi-Fi with iwctl..."

  # Check that iwd is available
  if ! command -v iwctl &>/dev/null; then
    error "iwctl not found. Make sure iwd is installed/running."
    exit 1
  fi

  # List available wireless devices
  info "Available wireless devices:"
  iwctl device list

  read -rp "Enter your wireless device name (e.g. wlan0): " WIFI_DEVICE

  # Scan for networks
  info "Scanning for networks on ${WIFI_DEVICE}..."
  iwctl station "${WIFI_DEVICE}" scan
  sleep 3

  # Show available networks
  info "Available networks:"
  iwctl station "${WIFI_DEVICE}" get-networks

  read -rp "Enter the SSID (network name) to connect: " WIFI_SSID

  # Connect to the network (iwctl will prompt for the passphrase)
  info "Connecting to '${WIFI_SSID}'..."
  iwctl station "${WIFI_DEVICE}" connect "${WIFI_SSID}"

  # Wait a moment for the connection to establish
  info "Waiting for connection to establish..."
  sleep 5

  # Verify connectivity after connecting
  if ping -c 3 -W 5 kernel.org &>/dev/null; then
    info "Successfully connected to '${WIFI_SSID}'!"
  else
    error "Connected to '${WIFI_SSID}' but still no internet. Check your network."
    exit 1
  fi
}

# --- Main: ensure we have internet ------------------------------------------
if ! check_connectivity; then
  setup_wifi
fi

info "Network is ready. Proceeding with setup..."

# =============================================================================
# Step 2: Disk partitioning
# Layout:
#   Partition 1 — EFI System Partition — 512 MiB
#   Partition 2 — Root (/)              — total disk - RAM
#   Partition 3 — Swap                  — equal to installed RAM
# =============================================================================

# Check sgdisk is available (pure CLI, non-interactive GPT partitioner)
if ! command -v sgdisk &>/dev/null; then
    error "sgdisk not found. Install gptfdisk to proceed."
    exit 1
fi

# Get installed RAM in MiB
RAM_MIB=$(awk '/MemTotal/ { printf "%d", $2 / 1024 }' /proc/meminfo)
info "Detected RAM: ${RAM_MIB} MiB"

# Detect internal disks (exclude USB/removable drives)
info "Detecting internal disks (excluding USB/removable)..."
INTERNAL_DISKS=()
for disk in /sys/block/sd* /sys/block/nvme* /sys/block/vd*; do
    [ -e "${disk}" ] || continue
    devname=$(basename "${disk}")

    # Skip removable devices (USB sticks, etc.)
    if [ "$(cat "${disk}/removable" 2>/dev/null)" = "1" ]; then
        continue
    fi

    # Skip USB-connected disks by checking the device path for "usb"
    devpath=$(realpath "${disk}" 2>/dev/null || echo "")
    if echo "${devpath}" | grep -qi "usb"; then
        continue
    fi

    INTERNAL_DISKS+=("/dev/${devname}")
done

if [ "${#INTERNAL_DISKS[@]}" -eq 0 ]; then
    error "No internal disks found."
    exit 1
fi

info "Internal disks found: ${INTERNAL_DISKS[*]}"

# Helper: get disk size in bytes for sorting
disk_size_bytes() {
    blockdev --getsize64 "$1"
}

# Helper: get partition prefix (nvme uses p1, sd/vd uses 1)
part_prefix() {
    if [[ "$1" == *nvme* ]]; then
        echo "${1}p"
    else
        echo "$1"
    fi
}

HOME_DISK=""

if [ "${#INTERNAL_DISKS[@]}" -eq 1 ]; then
    # --- Single disk: EFI + root + swap, no separate /home -------------------
    TARGET_DISK="${INTERNAL_DISKS[0]}"
    info "Only one internal disk detected: ${TARGET_DISK}"
else
    # --- Multiple disks: smallest → system, largest → /home ------------------
    info "Multiple internal disks detected:"

    # Sort disks by size (ascending) to pick smallest and largest
    SORTED_DISKS=($(
        for d in "${INTERNAL_DISKS[@]}"; do
            echo "$(disk_size_bytes "${d}") ${d}"
        done | sort -n | awk '{print $2}'
    ))

    TARGET_DISK="${SORTED_DISKS[0]}"                          # smallest
    HOME_DISK="${SORTED_DISKS[${#SORTED_DISKS[@]}-1]}"        # largest

    for d in "${SORTED_DISKS[@]}"; do
        size_hr=$(lsblk -dn -o SIZE "${d}" 2>/dev/null || echo "unknown")
        label=""
        [ "${d}" = "${TARGET_DISK}" ] && label=" ← system (EFI + root + swap)"
        [ "${d}" = "${HOME_DISK}" ]   && label=" ← /home"
        info "  ${d}  (${size_hr})${label}"
    done
fi

# Show current partition tables
info "Current partition table for ${TARGET_DISK}:"
sgdisk -p "${TARGET_DISK}"
if [ -n "${HOME_DISK}" ]; then
    info "Current partition table for ${HOME_DISK}:"
    sgdisk -p "${HOME_DISK}"
fi

# ---- Calculate partition sizes for the system disk --------------------------
DISK_SIZE_MIB=$(blockdev --getsize64 "${TARGET_DISK}" | awk '{ printf "%d", $1 / 1024 / 1024 }')
info "System disk size: ${DISK_SIZE_MIB} MiB"

EFI_SIZE_MIB=512
SWAP_SIZE_MIB="${RAM_MIB}"
ROOT_SIZE_MIB=$(( DISK_SIZE_MIB - EFI_SIZE_MIB - SWAP_SIZE_MIB ))

if [ "${ROOT_SIZE_MIB}" -le 0 ]; then
    error "System disk too small (${DISK_SIZE_MIB} MiB) for the layout (EFI=${EFI_SIZE_MIB} + swap=${SWAP_SIZE_MIB})."
    exit 1
fi

info "Partition plan for system disk (${TARGET_DISK}):"
info "  1) EFI  — ${EFI_SIZE_MIB} MiB"
info "  2) Root — ${ROOT_SIZE_MIB} MiB"
info "  3) Swap — ${SWAP_SIZE_MIB} MiB"

if [ -n "${HOME_DISK}" ]; then
    HOME_SIZE_HR=$(lsblk -dn -o SIZE "${HOME_DISK}" 2>/dev/null || echo "unknown")
    info "Partition plan for home disk (${HOME_DISK}):"
    info "  1) /home — ${HOME_SIZE_HR} (entire disk)"
fi

warn "⚠️  This will ERASE all data on ${TARGET_DISK}${HOME_DISK:+ and ${HOME_DISK}}!"
read -rp "Type YES to confirm: " CONFIRM
if [ "${CONFIRM}" != "YES" ]; then
    error "Aborted by user."
    exit 1
fi

# =============================================================================
# Partition the system disk (EFI + root + swap)
# =============================================================================
info "Partitioning system disk ${TARGET_DISK} with sgdisk..."
sgdisk --zap-all "${TARGET_DISK}"
sgdisk -n 1:0:+${EFI_SIZE_MIB}M -t 1:ef00 -c 1:"EFI"  "${TARGET_DISK}"
sgdisk -n 2:0:+${ROOT_SIZE_MIB}M -t 2:8300 -c 2:"root" "${TARGET_DISK}"
sgdisk -n 3:0:0                  -t 3:8200 -c 3:"swap"  "${TARGET_DISK}"

PREFIX=$(part_prefix "${TARGET_DISK}")
PART_EFI="${PREFIX}1"
PART_ROOT="${PREFIX}2"
PART_SWAP="${PREFIX}3"

# Format system partitions
info "Formatting EFI partition (${PART_EFI}) as FAT32..."
mkfs.fat -F 32 "${PART_EFI}"

info "Formatting root partition (${PART_ROOT}) as ext4..."
mkfs.ext4 -F "${PART_ROOT}"

info "Setting up swap partition (${PART_SWAP})..."
mkswap "${PART_SWAP}"
swapon "${PART_SWAP}"

# Mount system partitions
info "Mounting system partitions..."
mount "${PART_ROOT}" /mnt
mkdir -p /mnt/boot
mount "${PART_EFI}" /mnt/boot

# =============================================================================
# Partition the home disk (if a second disk exists)
# =============================================================================
if [ -n "${HOME_DISK}" ]; then
    info "Partitioning home disk ${HOME_DISK} with sgdisk..."
    sgdisk --zap-all "${HOME_DISK}"
    sgdisk -n 1:0:0 -t 1:8300 -c 1:"home" "${HOME_DISK}"

    HOME_PREFIX=$(part_prefix "${HOME_DISK}")
    PART_HOME="${HOME_PREFIX}1"

    info "Formatting home partition (${PART_HOME}) as ext4..."
    mkfs.ext4 -F "${PART_HOME}"

    info "Mounting /home..."
    mkdir -p /mnt/home
    mount "${PART_HOME}" /mnt/home
fi

info "Partitioning complete!"
lsblk "${TARGET_DISK}"
[ -n "${HOME_DISK}" ] && lsblk "${HOME_DISK}"

# =============================================================================
# Step 3: Install packages with pacstrap
# =============================================================================

info "Installing base system and packages with pacstrap..."

pacstrap -K /mnt \
    base \
    base-devel \
    linux \
    linux-firmware \
    linux-headers \
    intel-ucode \
    grub \
    efibootmgr \
    networkmanager \
    bluez \
    bluez-utils \
    pipewire-alsa \
    pipewire-jack \
    pipewire-pulse \
    nvidia-open \
    hyprland \
    wofi \
    sddm \
    kitty \
    flatpak \
    fish \
    neovim \
    git \
    lazygit \
    stow \
    openssh \
    gnome-keyring \
    podman \
    distrobox \
    btop \
    fastfetch \
    ripgrep \
    eza \
    axel \
    unzip \
    cpupower \
    pacman-contrib \
    adwaita-fonts \
    ttf-adwaitamono-nerd \
    adw-gtk-theme \
    xdg-desktop-portal-gtk \
    xdg-user-dirs \
    quickshell \
    less

info "pacstrap complete!"

# =============================================================================
# Step 4: Generate fstab
# =============================================================================

info "Generating fstab..."
genfstab -U /mnt >> /mnt/etc/fstab
info "Generated /mnt/etc/fstab:"
cat /mnt/etc/fstab

# =============================================================================
# Step 5: Time (3.3)
# =============================================================================

info "Configuring timezone..."
read -rp "Enter your timezone (e.g. America/Mexico_City): " TIMEZONE

if [ ! -f "/mnt/usr/share/zoneinfo/${TIMEZONE}" ]; then
    error "Invalid timezone: ${TIMEZONE}"
    info "Available timezones:"
    arch-chroot /mnt ls /usr/share/zoneinfo/
    exit 1
fi

arch-chroot /mnt ln -sf "/usr/share/zoneinfo/${TIMEZONE}" /etc/localtime
arch-chroot /mnt hwclock --systohc
info "Timezone set to ${TIMEZONE} and hardware clock synced."

# =============================================================================
# Step 6: Localization (3.4)
# =============================================================================

info "Configuring localization..."

# Uncomment en_US.UTF-8 and es_MX.UTF-8 in locale.gen
sed -i 's/^#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /mnt/etc/locale.gen
sed -i 's/^#es_MX.UTF-8 UTF-8/es_MX.UTF-8 UTF-8/' /mnt/etc/locale.gen

arch-chroot /mnt locale-gen

echo "LANG=en_US.UTF-8" > /mnt/etc/locale.conf

info "Localization configured (en_US.UTF-8 + es_MX.UTF-8)."

# =============================================================================
# Step 7: Network configuration (3.5)
# =============================================================================

info "Configuring network..."
read -rp "Enter hostname for this machine: " HOSTNAME

echo "${HOSTNAME}" > /mnt/etc/hostname

info "Hostname set to '${HOSTNAME}'."

# =============================================================================
# Step 8: Initramfs (3.6)
# =============================================================================

info "Regenerating initramfs..."
arch-chroot /mnt mkinitcpio -P
info "Initramfs generated."

# =============================================================================
# Step 9: Root password (3.7)
# =============================================================================

info "Set the root password:"
arch-chroot /mnt passwd

# =============================================================================
# Step 10: Install Flatpak apps
# =============================================================================

info "Installing Flatpak apps inside chroot..."

arch-chroot /mnt flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
arch-chroot /mnt flatpak install -y flathub \
    org.mozilla.firefox \
    com.valvesoftware.Steam

info "Flatpak apps installed!"

# =============================================================================
# Step 11: Create regular user
# =============================================================================

info "Creating a regular user..."

read -rp "Full name: " USER_FULLNAME
read -rp "Username: " USERNAME

# Create user with home directory, own group, fish shell and full name
arch-chroot /mnt useradd -m -U -G wheel -s /usr/bin/fish -c "${USER_FULLNAME}" "${USERNAME}"

# Set password
info "Set password for ${USERNAME}:"
arch-chroot /mnt passwd "${USERNAME}"

info "User '${USERNAME}' created (group: ${USERNAME}, shell: fish)."

# =============================================================================
# Step 12: Enable services and configure cpupower
# =============================================================================

info "Enabling system services..."

arch-chroot /mnt systemctl enable NetworkManager
arch-chroot /mnt systemctl enable bluetooth
arch-chroot /mnt systemctl enable sshd
arch-chroot /mnt systemctl enable sddm
arch-chroot /mnt systemctl enable cpupower

# PipeWire runs as user service, enable for the new user
arch-chroot /mnt systemctl --global enable pipewire pipewire-pulse wireplumber

# Set cpupower governor to performance
sed -i "s/^#governor=.*/governor='performance'/" /mnt/etc/default/cpupower
info "cpupower governor set to performance."

info "All services enabled."

# =============================================================================
# Step 13: Install GRUB bootloader
# =============================================================================

info "Installing GRUB bootloader (EFI x86_64, removable)..."

arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot --removable
arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg

info "GRUB installed and configured."

# =============================================================================
# Step 14: Install AUR packages via yay
# =============================================================================

info "Creating temporary user for AUR build..."
arch-chroot /mnt useradd -m -G wheel tempuser
echo "tempuser ALL=(ALL) NOPASSWD: ALL" >> /mnt/etc/sudoers

# Install yay-bin (pre-compiled, no build needed)
info "Installing yay-bin from AUR..."
arch-chroot /mnt su - tempuser -c "
    git clone --depth 1 https://aur.archlinux.org/yay-bin.git /tmp/yay-bin
    cd /tmp/yay-bin
    makepkg -si --noconfirm
    rm -rf /tmp/yay-bin
"

# Install AUR packages
info "Installing AUR packages via yay..."
arch-chroot /mnt su - tempuser -c "
    yay -S --noconfirm \
        opencode \
        whisker-shell-git \
        curseforge
"

# Clean up temp user
info "Cleaning up temporary user..."
arch-chroot /mnt userdel -r tempuser
sed -i '/^tempuser/d' /mnt/etc/sudoers

info "AUR packages installed!"
