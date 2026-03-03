"""Terminal.app theme generator."""

import os
import plistlib

from .helpers import ROOT, hex_to_rgb


def _nscolor_archive(r, g, b):
    """Create an NSKeyedArchiver-encoded NSColor (calibrated RGB, 0-1 floats)."""
    rgb_string = f"{r:.6f} {g:.6f} {b:.6f}".encode("ascii") + b"\x00"
    objects = [
        "$null",
        {
            "$class": plistlib.UID(2),
            "NSColorSpace": 1,
            "NSRGB": rgb_string,
        },
        {
            "$classes": ["NSColor", "NSObject"],
            "$classname": "NSColor",
        },
    ]
    archive = {
        "$archiver": "NSKeyedArchiver",
        "$objects": objects,
        "$top": {"root": plistlib.UID(1)},
        "$version": 100000,
    }
    return plistlib.dumps(archive, fmt=plistlib.FMT_BINARY)


def _hex_to_nscolor(hex_color):
    """Convert '#rrggbb' to NSKeyedArchiver binary data."""
    r, g, b = hex_to_rgb(hex_color)
    return _nscolor_archive(r / 255.0, g / 255.0, b / 255.0)


def generate_terminal_app(palette):
    for variant in ("light", "dark"):
        p = palette[variant]
        t = p["terminal"]
        ed = p["editor"]
        kw = p["syntax"]["keyword"]["color"]

        profile = {
            "name": f"Deligoez {variant.title()}",
            "type": "Window Settings",
            "ProfileCurrentVersion": 2.09,
            "ANSIBlackColor": _hex_to_nscolor(t["black"]),
            "ANSIRedColor": _hex_to_nscolor(t["red"]),
            "ANSIGreenColor": _hex_to_nscolor(t["green"]),
            "ANSIYellowColor": _hex_to_nscolor(t["yellow"]),
            "ANSIBlueColor": _hex_to_nscolor(t["blue"]),
            "ANSIMagentaColor": _hex_to_nscolor(t["magenta"]),
            "ANSICyanColor": _hex_to_nscolor(t["cyan"]),
            "ANSIWhiteColor": _hex_to_nscolor(t["white"]),
            "ANSIBrightBlackColor": _hex_to_nscolor(t["brightBlack"]),
            "ANSIBrightRedColor": _hex_to_nscolor(t["brightRed"]),
            "ANSIBrightGreenColor": _hex_to_nscolor(t["brightGreen"]),
            "ANSIBrightYellowColor": _hex_to_nscolor(t["brightYellow"]),
            "ANSIBrightBlueColor": _hex_to_nscolor(t["brightBlue"]),
            "ANSIBrightMagentaColor": _hex_to_nscolor(t["brightMagenta"]),
            "ANSIBrightCyanColor": _hex_to_nscolor(t["brightCyan"]),
            "ANSIBrightWhiteColor": _hex_to_nscolor(t["brightWhite"]),
            "BackgroundColor": _hex_to_nscolor(ed["background"]),
            "TextColor": _hex_to_nscolor(ed["foreground"]),
            "TextBoldColor": _hex_to_nscolor(ed["foreground"]),
            "CursorColor": _hex_to_nscolor(kw),
            "CursorTextColor": _hex_to_nscolor(ed["background"]),
            "SelectionColor": _hex_to_nscolor(ed["selection"]),
        }

        name = f"Deligoez {variant.title()}.terminal"
        path = os.path.join(ROOT, "terminal", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            plistlib.dump(profile, f, fmt=plistlib.FMT_XML)
        print(f"  Generated: {os.path.relpath(path, ROOT)}")
