"""Shared color utilities and file I/O for all generators."""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_palette():
    with open(os.path.join(ROOT, "palette.json")) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------

def hex_to_rgb(h):
    """'#rrggbb' -> (r, g, b) ints."""
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rgb_to_hex(r, g, b):
    """(r, g, b) ints -> '#rrggbb'."""
    return f"#{r:02x}{g:02x}{b:02x}"


def lerp_color(c1, c2, t):
    """Linearly interpolate between two hex colors."""
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return rgb_to_hex(r, g, b)


def with_alpha(hex6, alpha_hex):
    """'#rrggbb' + 'aa' -> '#rrggbbaa'."""
    return hex6 + alpha_hex


def phpstorm_hex(color):
    """Convert '#rrggbb' to PHPStorm format: strip '#' and leading zeros.
    '#009999' -> '9999', '#000000' -> '0', '#ffffff' -> 'ffffff'."""
    h = color.lstrip("#")
    # Strip leading zeros but keep at least one character
    stripped = h.lstrip("0") or "0"
    return stripped


def hex8(color):
    """Ensure color has alpha. '#rrggbb' -> '#rrggbbff', pass through '#rrggbbaa'."""
    c = color.lstrip("#")
    if len(c) == 6:
        return f"#{c}ff"
    return f"#{c}"


def write_file(path, content):
    """Write content to file, creating directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="\n") as f:
        f.write(content)
    print(f"  Generated: {os.path.relpath(path, ROOT)}")
