{ config, pkgs, ... }:

{
  imports = [ ./hardware-configuration.nix ];

  system.stateVersion = "24.11";
  networking.hostName = "msi";
  networking.networkmanager.enable = true;

  boot.kernelPackages = pkgs.linuxPackages_latest;
  boot.kernelParams = [ "nvidia_drm.modeset=1" ];
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  services.xserver.enable = true;
  services.xserver.videoDrivers = [ "nvidia" ];
  hardware.nvidia = {
    open = true;
    package = config.boot.kernelPackages.nvidiaPackages.latest;
    modesetting.enable = true;
    powerManagement.enable = true;
    nvidiaSettings = true;
  };
  hardware.graphics.enable = true;
  hardware.graphics.enable32Bit = true;

  programs.hyprland.enable = true;
  environment.sessionVariables.NIXOS_OZONE_WL = "1";

  security.rtkit.enable = true;
  hardware.pulseaudio.enable = false;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
    jack.enable = true;
    wireplumber.enable = true;
  };

  hardware.bluetooth.enable = true;
  services.blueman.enable = true;

  environment.systemPackages = with pkgs; [
    fish zoxide fzf fastfetch eza bat fd ripgrep tree jq btop
    neovim
    git lazygit stow
    waybar hyprpaper hyprlauncher wofi dolphin kitty playerctl brightnessctl
    curl wget unzip
    podman distrobox
    python3 pipx
    steam
    bluetui
    nerd-fonts.jetbrains-mono
  ];

  networking.firewall.enable = true;

  users.users.luis = {
    isNormalUser = true;
    extraGroups = [ "wheel" "networkmanager" "audio" "video" ];
    shell = pkgs.fish;
  };

  programs.fish.enable = true;
}
