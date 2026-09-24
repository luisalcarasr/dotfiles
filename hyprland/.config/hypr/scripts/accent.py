#!/usr/bin/env python3
"""Build a triadic color triangle from a wallpaper's accent hue.

Prints "<BORDER> <GRAD_A> <GRAD_B>" (three hex RRGGBB, no "#"). The hue
extracted from the image seeds three colors spaced 120 degrees apart on the
color wheel: BORDER is the accent itself (soft, used for the default window
border) and the other two are its triadic partners at different values, so the
rotating highlight gradient sweeps between them.

Usage: accent.py [path-to-image]
If no path is given the script exits with a GitHub-blue fallback set so
callers always get usable colors.
"""

import colorsys
import os
import sys

from PIL import Image

FALLBACK_A = "58a6ff"


def hsv_to_hex(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return "%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def accent_hue_from_image(path):
    img = Image.open(path).convert("RGB")
    img.thumbnail((160, 160))

    hue_bins = {}
    sat_total = 0
    sat_count = 0
    data = img.tobytes()
    for i in range(0, len(data), 3):
        r, g, b = data[i], data[i + 1], data[i + 2]
        hue, sat, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        # skip greys, near-blacks and near-whites
        if sat < 0.25 or value < 0.18 or value > 0.92:
            continue
        bin_i = int(hue * 24) % 24
        hue_bins[bin_i] = hue_bins.get(bin_i, 0) + 1
        sat_total += sat
        sat_count += 1

    if not hue_bins:
        return None

    best_bin = max(hue_bins, key=hue_bins.get)
    hue = (best_bin + 0.5) / 24
    sat = min(0.95, max(0.5, sat_total / sat_count))
    return hue, sat


def color_triangle(path):
    accent = None
    if path:
        accent = accent_hue_from_image(path)
    if accent is None:
        accent = colorsys.rgb_to_hsv(
            int(FALLBACK_A[0:2], 16) / 255,
            int(FALLBACK_A[2:4], 16) / 255,
            int(FALLBACK_A[4:6], 16) / 255,
        )
    hue, sat = accent[0], accent[1]
    # the border accent must stay vivid: a pastel wallpaper can yield a dim
    # dominant hue that would read as "inactive" next to the grey borders
    border_sat = min(0.95, max(0.75, sat))
    border = hsv_to_hex(hue, border_sat, 0.68)
    grad_a = hsv_to_hex((hue + 1 / 3) % 1.0, sat * 0.9, 0.5)
    grad_b = hsv_to_hex((hue + 2 / 3) % 1.0, sat * 0.9, 0.92)
    return border, grad_a, grad_b


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if not path or not os.path.isfile(path):
        path = None
    border, grad_a, grad_b = color_triangle(path)
    print("%s %s %s" % (border, grad_a, grad_b))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        border, grad_a, grad_b = color_triangle(None)
        print("%s %s %s" % (border, grad_a, grad_b))