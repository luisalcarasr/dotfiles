#!/usr/bin/env python3
"""Extract an accent color from an image, adjusted for window border contrast.

Prints a single lowercase RRGGBB hex color: the vivid (fully saturated) accent
of the wallpaper, bright (full value) when the wallpaper is dark or mid-bright
so the border separates dark windows from the background, and a darker tint of
the same hue for genuinely bright wallpapers where a light border would wash
out.

Exits 1 (and prints nothing) when the image cannot be read or no suitable
color is found, so callers can fall back to their default border colors.
"""

import sys

from PIL import Image

MIN_COUNT = 2
MAX_SIZE = 256
SAT_MIN = 0.15
VALUE_MIN = 0.15
VALUE_MAX = 0.95
LIGHT_VALUE = 1.0
DARK_VALUE = 0.22
BG_LIGHT_THRESHOLD = 165


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


def from_hsv(hue, saturation, value):
    i = int(hue / 60) % 6
    f = hue / 60 - int(hue / 60)
    p = value * (1 - saturation)
    q = value * (1 - f * saturation)
    t = value * (1 - (1 - f) * saturation)
    if i == 0:
        r, g, b = value, t, p
    elif i == 1:
        r, g, b = q, value, p
    elif i == 2:
        r, g, b = p, value, t
    elif i == 3:
        r, g, b = p, q, value
    elif i == 4:
        r, g, b = t, p, value
    else:
        r, g, b = value, p, q
    return int(r * 255 + 0.5), int(g * 255 + 0.5), int(b * 255 + 0.5)


def luma(r, g, b):
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def mean_luma(image):
    data = image.tobytes()
    total = 0.0
    count = len(data) // 3
    for i in range(0, len(data), 3):
        total += luma(data[i], data[i + 1], data[i + 2])
    return total / count if count else 0.0


def accent_hex(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        background = Image.new("RGBA", img.size, (0, 0, 0, 255))
        img = Image.alpha_composite(background, img).convert("RGB")
        img.thumbnail((MAX_SIZE, MAX_SIZE))

    bg_luma = mean_luma(img)

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

    _, r, g, b = best
    hue, _, _ = to_hsv(r, g, b)
    light = from_hsv(hue, 1.0, LIGHT_VALUE)
    dark = from_hsv(hue, 1.0, DARK_VALUE)

    if bg_luma >= BG_LIGHT_THRESHOLD:
        primary = dark
    else:
        primary = light

    return "{:02x}{:02x}{:02x}".format(*primary)


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        result = accent_hex(argv[1])
    except Exception:
        result = None
    if result is None:
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))