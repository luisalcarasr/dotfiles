#!/usr/bin/env python3
"""Extract an accent color from an image for Hyprland window borders.

Prints a lowercase RRGGBB hex color to stdout. Exits 1 (and prints nothing)
when the image cannot be read or no suitable color is found, so callers can
fall back to their default border colors.
"""

import sys

from PIL import Image

MIN_COUNT = 2
MAX_SIZE = 256
SAT_MIN = 0.15
VALUE_MIN = 0.15
VALUE_MAX = 0.95


def to_hsv(r, g, b):
    rn, gn, bn = r / 255.0, g / 255.0, b / 255.0
    cmax = max(rn, gn, bn)
    cmin = min(rn, gn, bn)
    delta = cmax - cmin
    value = cmax
    saturation = 0 if delta == 0 else delta / cmax
    if delta == 0:
        hue = 0.0
    elif cmax == rn:
        hue = 60 * (((gn - bn) / delta) % 6)
    elif cmax == gn:
        hue = 60 * (((bn - rn) / delta) + 2)
    else:
        hue = 60 * (((rn - gn) / delta) + 4)
    return hue, saturation, value


def accent_hex(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        background = Image.new("RGBA", img.size, (0, 0, 0, 255))
        img = Image.alpha_composite(background, img).convert("RGB")
        img.thumbnail((MAX_SIZE, MAX_SIZE))

    hist = {}
    pixel_bytes = img.tobytes()
    for i in range(0, len(pixel_bytes), 3):
        r, g, b = pixel_bytes[i], pixel_bytes[i + 1], pixel_bytes[i + 2]
        key = (r & 0xF8, g & 0xF8, b & 0xF8)
        hist[key] = hist.get(key, 0) + 1

    best = None
    for (r, g, b), count in hist.items():
        if count < MIN_COUNT:
            continue
        hue, sat, val = to_hsv(r, g, b)
        if sat < SAT_MIN or val < VALUE_MIN or val > VALUE_MAX:
            continue
        score = sat
        if best is None or score > best[0]:
            best = (score, r, g, b)

    if best is None:
        return None
    return "{:02x}{:02x}{:02x}".format(best[1], best[2], best[3])


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        hex_color = accent_hex(argv[1])
    except Exception:
        hex_color = None
    if hex_color is None:
        return 1
    print(hex_color)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))