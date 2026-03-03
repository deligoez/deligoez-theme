"""Ghostty theme generator."""

import os

from .helpers import ROOT, write_file


def generate_ghostty(palette):
    for variant in ("light", "dark"):
        p = palette[variant]
        t = p["terminal"]
        kw = p["syntax"]["keyword"]["color"]
        sel = p["editor"]["selection"]
        bg = p["editor"]["background"]
        fg = p["editor"]["foreground"]

        lines = [
            f"# Deligoez {variant.title()} \u2014 Ghostty theme",
            "# https://github.com/deligoez/deligoez-theme",
            "",
            f"background = {bg}",
            f"foreground = {fg}",
            f"cursor-color = {kw}",
            f"cursor-text = {bg}",
            f"selection-background = {sel}",
            f"selection-foreground = {fg}",
            "",
            "# Normal colors (0-7)",
            f"palette = 0={t['black']}",
            f"palette = 1={t['red']}",
            f"palette = 2={t['green']}",
            f"palette = 3={t['yellow']}",
            f"palette = 4={t['blue']}",
            f"palette = 5={t['magenta']}",
            f"palette = 6={t['cyan']}",
            f"palette = 7={t['white']}",
            "",
            "# Bright colors (8-15)",
            f"palette = 8={t['brightBlack']}",
            f"palette = 9={t['brightRed']}",
            f"palette = 10={t['brightGreen']}",
            f"palette = 11={t['brightYellow']}",
            f"palette = 12={t['brightBlue']}",
            f"palette = 13={t['brightMagenta']}",
            f"palette = 14={t['brightCyan']}",
            f"palette = 15={t['brightWhite']}",
        ]

        name = f"Deligoez {variant.title()}"
        write_file(os.path.join(ROOT, "ghostty", name), "\n".join(lines) + "\n")
