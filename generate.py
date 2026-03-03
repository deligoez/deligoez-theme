#!/usr/bin/env python3
"""
Theme generator for Deligoez theme.
Reads palette.json and generates Ghostty, Zed, and PHPStorm theme files.

Usage: python3 generate.py
"""

import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


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


def write_file(path, content):
    """Write content to file, creating directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="\n") as f:
        f.write(content)
    print(f"  Generated: {os.path.relpath(path, ROOT)}")


# ---------------------------------------------------------------------------
# Ghostty generator
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Zed generator
# ---------------------------------------------------------------------------

def _zed_syntax_entry(color, font_style=None, font_weight=None):
    return {
        "color": color,
        "font_style": font_style,
        "font_weight": font_weight,
    }


def generate_zed(palette):
    themes = []
    for variant in ("light", "dark"):
        p = palette[variant]
        syn = p["syntax"]
        t = p["terminal"]
        ed = p["editor"]
        st = p["status"]

        bg = ed["background"]
        fg = ed["foreground"]

        if variant == "light":
            themes.append(_zed_light_theme(p, syn, t, ed, st, bg, fg))
        else:
            themes.append(_zed_dark_theme(p, syn, t, ed, st, bg, fg))

    output = {
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": "Deligoez",
        "author": "deligoez",
        "themes": themes,
    }

    content = json.dumps(output, indent=2, ensure_ascii=False)
    write_file(os.path.join(ROOT, "zed", "deligoez.json"), content)


def _hex8(color):
    """Ensure color has alpha. '#rrggbb' -> '#rrggbbff', pass through '#rrggbbaa'."""
    c = color.lstrip("#")
    if len(c) == 6:
        return f"#{c}ff"
    return f"#{c}"


def _zed_light_theme(p, syn, t, ed, st, bg, fg):
    # Hand-tuned grays for light theme UI chrome
    GRAY_APP = "#f5f5f5"     # app background, status bar
    GRAY_SURFACE = "#f0f0f0" # surfaces, panels, tab bar
    GRAY_HOVER = "#e8e8e8"   # element hover, wrap guide, indent guide
    GRAY_BORDER_V = "#e3e3e3" # border variant
    GRAY_BORDER = "#d0d0d0"  # main border
    GRAY_INDENT_A = "#c0c0c0" # indent guide active
    GRAY_BORDER_D = "#e0e0e0" # border disabled
    GRAY_PLACEHOLDER = "#999999" # placeholder, dim foreground
    GRAY_MUTED = "#666666"   # muted text/icons
    GRAY_DISABLED = "#aaaaaa" # disabled text/icons

    sel = ed["selection"]

    style = {}

    # App chrome
    style["background"] = _hex8(GRAY_APP)
    style["text"] = _hex8(fg)
    style["text.muted"] = _hex8(GRAY_MUTED)
    style["text.placeholder"] = _hex8(GRAY_PLACEHOLDER)
    style["text.disabled"] = _hex8(GRAY_DISABLED)
    style["text.accent"] = _hex8(syn["function"]["color"])
    style["border"] = _hex8(GRAY_BORDER)
    style["border.variant"] = _hex8(GRAY_BORDER_V)
    style["border.focused"] = _hex8(syn["function"]["color"])
    style["border.selected"] = _hex8(sel)
    style["border.transparent"] = "#00000000"
    style["border.disabled"] = _hex8(GRAY_BORDER_D)

    # Surfaces
    style["elevated_surface.background"] = _hex8(GRAY_SURFACE)
    style["surface.background"] = _hex8(GRAY_SURFACE)
    style["panel.background"] = _hex8(GRAY_SURFACE)
    style["panel.focused_border"] = None
    style["pane.focused_border"] = None

    # Elements
    style["element.background"] = _hex8(GRAY_SURFACE)
    style["element.hover"] = _hex8(GRAY_HOVER)
    style["element.active"] = _hex8(sel)
    style["element.selected"] = _hex8(sel)
    style["element.disabled"] = _hex8(GRAY_SURFACE)
    style["ghost_element.background"] = "#00000000"
    style["ghost_element.hover"] = _hex8(GRAY_HOVER)
    style["ghost_element.active"] = _hex8(sel)
    style["ghost_element.selected"] = _hex8(sel)
    style["ghost_element.disabled"] = _hex8(GRAY_SURFACE)

    style["drop_target.background"] = with_alpha(sel, "80")

    # Icons
    style["icon"] = _hex8(fg)
    style["icon.muted"] = _hex8(GRAY_MUTED)
    style["icon.disabled"] = _hex8(GRAY_DISABLED)
    style["icon.placeholder"] = _hex8(GRAY_MUTED)
    style["icon.accent"] = _hex8(syn["function"]["color"])

    # Tab bar
    style["tab_bar.background"] = _hex8(GRAY_SURFACE)
    style["tab.active_background"] = _hex8(bg)
    style["tab.inactive_background"] = _hex8(GRAY_SURFACE)

    # Status/title bar
    style["status_bar.background"] = _hex8(GRAY_APP)
    style["title_bar.background"] = _hex8(GRAY_APP)
    style["title_bar.inactive_background"] = _hex8(GRAY_SURFACE)
    style["toolbar.background"] = _hex8(bg)

    # Scrollbar
    style["scrollbar.thumb.background"] = with_alpha(fg, "1a")
    style["scrollbar.thumb.hover_background"] = with_alpha(fg, "33")
    style["scrollbar.thumb.border"] = "#00000000"
    style["scrollbar.track.background"] = "#00000000"
    style["scrollbar.track.border"] = _hex8(GRAY_SURFACE)

    # Editor
    style["editor.background"] = _hex8(bg)
    style["editor.foreground"] = _hex8(fg)
    style["editor.gutter.background"] = _hex8(bg)
    style["editor.subheader.background"] = _hex8(GRAY_SURFACE)
    style["editor.active_line.background"] = "#00000000"
    style["editor.highlighted_line.background"] = _hex8(GRAY_SURFACE)
    style["editor.line_number"] = _hex8(ed["lineNumber"])
    style["editor.active_line_number"] = _hex8(fg)
    style["editor.invisible"] = _hex8(GRAY_BORDER)
    style["editor.wrap_guide"] = _hex8(GRAY_HOVER)
    style["editor.active_wrap_guide"] = _hex8(GRAY_BORDER)
    style["editor.indent_guide"] = _hex8(GRAY_HOVER)
    style["editor.indent_guide_active"] = _hex8(GRAY_INDENT_A)
    style["editor.document_highlight.read_background"] = _hex8(p["ui"]["identifierUnderCaret"])
    style["editor.document_highlight.write_background"] = with_alpha(sel, "66")

    style["search.match_background"] = with_alpha(p["ui"]["searchResult"], "55")

    # Links
    style["link_text.hover"] = _hex8(syn["link"]["color"])

    # Terminal
    style["terminal.background"] = _hex8(bg)
    style["terminal.foreground"] = _hex8(fg)
    style["terminal.bright_foreground"] = _hex8(t["black"] if t["black"] != bg else "#000000")
    style["terminal.dim_foreground"] = _hex8(GRAY_PLACEHOLDER)

    _terminal_colors = [
        ("black", t["black"]), ("red", t["red"]), ("green", t["green"]),
        ("yellow", t["yellow"]), ("blue", t["blue"]), ("magenta", t["magenta"]),
        ("cyan", t["cyan"]), ("white", t["white"]),
    ]
    _bright_map = {
        "black": t["brightBlack"], "red": t["brightRed"],
        "green": t["brightGreen"], "yellow": t["brightYellow"],
        "blue": t["brightBlue"], "magenta": t["brightMagenta"],
        "cyan": t["brightCyan"], "white": t["brightWhite"],
    }
    # Dim colors: darken normal colors toward background
    _dim_map_light = {
        "black": "#333333", "red": "#990000", "green": "#4a8045",
        "yellow": "#a09000", "blue": "#0f2560", "magenta": "#a0407a",
        "cyan": "#208090", "white": "#999999",
    }
    for name, color in _terminal_colors:
        style[f"terminal.ansi.{name}"] = _hex8(color)
        style[f"terminal.ansi.bright_{name}"] = _hex8(_bright_map[name])
        style[f"terminal.ansi.dim_{name}"] = _hex8(_dim_map_light[name])

    # Status colors
    style["error"] = _hex8(st["error"])
    style["error.background"] = _hex8(p["ui"]["breakpoint"])
    style["error.border"] = with_alpha(st["error"], "33")
    style["warning"] = _hex8(st["warning"])
    style["warning.background"] = "#fff3e0ff"
    style["warning.border"] = with_alpha(st["warning"], "33")
    style["success"] = _hex8(st["success"])
    style["success.background"] = _hex8(p["diff"]["inserted"])
    style["success.border"] = with_alpha(st["success"], "33")
    style["info"] = _hex8(st["info"])
    style["info.background"] = _hex8(sel)
    style["info.border"] = with_alpha(st["info"], "33")
    style["hint"] = _hex8(st["hint"])
    style["hint.background"] = "#f0ebf5ff"
    style["hint.border"] = with_alpha(st["hint"], "33")

    # Conflict / created / deleted / modified / renamed
    style["conflict"] = _hex8(st["warning"])
    style["conflict.background"] = "#fff3e0ff"
    style["conflict.border"] = with_alpha(st["warning"], "33")
    style["created"] = _hex8(st["success"])
    style["created.background"] = _hex8(p["diff"]["inserted"])
    style["created.border"] = with_alpha(st["success"], "33")
    style["deleted"] = _hex8(st["error"])
    style["deleted.background"] = "#ffdadaff"
    style["deleted.border"] = with_alpha(st["error"], "33")
    style["modified"] = _hex8(st["info"])
    style["modified.background"] = _hex8(p["diff"]["modified"])
    style["modified.border"] = with_alpha(st["info"], "33")
    style["renamed"] = _hex8(st["hint"])
    style["renamed.background"] = "#f0ebf5ff"
    style["renamed.border"] = with_alpha(st["hint"], "33")

    # Hidden / ignored / unreachable / predictive
    style["hidden"] = _hex8(GRAY_PLACEHOLDER)
    style["hidden.background"] = _hex8(GRAY_APP)
    style["hidden.border"] = _hex8(GRAY_BORDER_D)
    style["ignored"] = _hex8(GRAY_PLACEHOLDER)
    style["ignored.background"] = _hex8(GRAY_APP)
    style["ignored.border"] = _hex8(GRAY_BORDER_D)
    style["unreachable"] = _hex8(GRAY_MUTED)
    style["unreachable.background"] = _hex8(GRAY_APP)
    style["unreachable.border"] = _hex8(GRAY_BORDER_D)
    style["predictive"] = _hex8(ed["lineNumber"])
    style["predictive.background"] = _hex8(GRAY_APP)
    style["predictive.border"] = _hex8(GRAY_BORDER_D)

    # Players
    player_colors = [
        syn["keyword"]["color"], syn["function"]["color"],
        syn["interface"]["color"], syn["tag"]["color"],
        syn["constant"]["color"], syn["operator"]["color"],
        st["warning"], syn["class"]["color"],
    ]
    players = []
    for i, c in enumerate(player_colors):
        entry = {"cursor": _hex8(c), "background": _hex8(c)}
        if i == 0:
            entry["selection"] = _hex8(sel)
        else:
            entry["selection"] = with_alpha(c, "3d")
        players.append(entry)
    style["players"] = players

    # Syntax
    style["syntax"] = _zed_light_syntax(syn, fg)

    return {
        "name": "Deligoez Light",
        "appearance": "light",
        "style": style,
    }


def _zed_light_syntax(syn, fg):
    s = {}
    s["attribute"] = _zed_syntax_entry(_hex8(syn["interface"]["color"]))
    s["boolean"] = _zed_syntax_entry(_hex8(syn["keyword"]["color"]), font_style="italic")
    s["comment"] = _zed_syntax_entry(_hex8(syn["comment"]["color"]), font_style="italic")
    s["comment.doc"] = _zed_syntax_entry(_hex8(syn["commentDoc"]["color"]), font_style="italic")
    s["constant"] = _zed_syntax_entry(_hex8(syn["constant"]["color"]))
    s["constructor"] = _zed_syntax_entry(_hex8(syn["class"]["color"]))
    s["embedded"] = _zed_syntax_entry(_hex8(fg))
    s["emphasis"] = _zed_syntax_entry(_hex8(fg), font_style="italic")
    s["emphasis.strong"] = _zed_syntax_entry(_hex8(fg), font_weight=700)
    s["enum"] = _zed_syntax_entry(_hex8(syn["interface"]["color"]))
    s["function"] = _zed_syntax_entry(_hex8(syn["function"]["color"]))
    s["hint"] = _zed_syntax_entry(_hex8(syn["commentDocTag"]["color"]))
    s["keyword"] = _zed_syntax_entry(_hex8(syn["keyword"]["color"]), font_style="italic")
    s["label"] = _zed_syntax_entry(_hex8(syn["commentDocTag"]["color"]))
    s["link_text"] = _zed_syntax_entry(_hex8(syn["link"]["color"]), font_style="italic")
    s["link_uri"] = _zed_syntax_entry(_hex8(syn["link"]["color"]))
    s["namespace"] = _zed_syntax_entry(_hex8(syn["class"]["color"]))
    s["number"] = _zed_syntax_entry(_hex8(syn["number"]["color"]))
    s["operator"] = _zed_syntax_entry(_hex8(syn["operator"]["color"]), font_weight=700)
    s["predictive"] = _zed_syntax_entry(_hex8("#a7a7a7"), font_style="italic")
    s["preproc"] = _zed_syntax_entry(_hex8(syn["phpTag"]["color"]))
    s["primary"] = _zed_syntax_entry(_hex8(fg))
    s["property"] = _zed_syntax_entry(_hex8(syn["class"]["color"]))
    s["punctuation"] = _zed_syntax_entry(_hex8(fg))
    s["punctuation.bracket"] = _zed_syntax_entry(_hex8(fg))
    s["punctuation.delimiter"] = _zed_syntax_entry(_hex8(fg))
    s["punctuation.list_marker"] = _zed_syntax_entry(_hex8(syn["operator"]["color"]))
    s["punctuation.markup"] = _zed_syntax_entry(_hex8(syn["operator"]["color"]))
    s["punctuation.special"] = _zed_syntax_entry(_hex8(syn["phpTag"]["color"]))
    s["selector"] = _zed_syntax_entry(_hex8(syn["tag"]["color"]))
    s["selector.pseudo"] = _zed_syntax_entry(_hex8(syn["interface"]["color"]))
    s["string"] = _zed_syntax_entry(_hex8(syn["string"]["color"]))
    s["string.escape"] = _zed_syntax_entry(_hex8(syn["attributeValue"]["color"]))
    s["string.regex"] = _zed_syntax_entry(_hex8(syn["regex"]["color"]))
    s["string.special"] = _zed_syntax_entry(_hex8(syn["stringSpecial"]["color"]))
    s["string.special.symbol"] = _zed_syntax_entry(_hex8(syn["symbol"]["color"]))
    s["tag"] = _zed_syntax_entry(_hex8(syn["tag"]["color"]))
    s["text.literal"] = _zed_syntax_entry(_hex8(syn["string"]["color"]))
    s["title"] = _zed_syntax_entry(_hex8(syn["class"]["color"]), font_weight=700)
    s["type"] = _zed_syntax_entry(_hex8(syn["class"]["color"]))
    s["variable"] = _zed_syntax_entry(_hex8(fg))
    s["variable.special"] = _zed_syntax_entry(_hex8(syn["variableSpecial"]["color"]))
    s["variant"] = _zed_syntax_entry(_hex8(syn["interface"]["color"]))
    return s


def _zed_dark_theme(p, syn, t, ed, st, bg, fg):
    # Dark grays: lerp between bg (#1a1a1f) and fg (#d4d4d8)
    # We use specific computed values to match the current file exactly
    app_bg = "#161619"     # slightly darker than editor bg
    surface = "#1e1e22"    # 1 step up
    elevated = "#242428"   # 2 steps up
    element_hover = "#2a2a2f"
    border_var = "#2a2a30"
    active = "#303036"
    border_main = "#35353b"
    indent_active = "#45454d"
    invisible = "#3a3a42"

    sel = ed["selection"]

    style = {}

    # App chrome
    style["background"] = _hex8(app_bg)
    style["text"] = _hex8(fg)
    style["text.muted"] = "#9898a0ff"
    style["text.placeholder"] = "#6b6b73ff"
    style["text.disabled"] = "#55555dff"
    style["text.accent"] = _hex8(syn["function"]["color"])
    style["border"] = _hex8(border_main)
    style["border.variant"] = _hex8(border_var)
    style["border.focused"] = _hex8(syn["function"]["color"])
    style["border.selected"] = _hex8(active)
    style["border.transparent"] = "#00000000"
    style["border.disabled"] = _hex8(border_var)

    # Surfaces
    style["elevated_surface.background"] = _hex8(elevated)
    style["surface.background"] = _hex8(surface)
    style["panel.background"] = _hex8(surface)
    style["panel.focused_border"] = None
    style["pane.focused_border"] = None

    # Elements
    style["element.background"] = _hex8(surface)
    style["element.hover"] = _hex8(element_hover)
    style["element.active"] = _hex8(active)
    style["element.selected"] = _hex8(active)
    style["element.disabled"] = _hex8(surface)
    style["ghost_element.background"] = "#00000000"
    style["ghost_element.hover"] = _hex8(element_hover)
    style["ghost_element.active"] = _hex8(active)
    style["ghost_element.selected"] = _hex8(active)
    style["ghost_element.disabled"] = _hex8(surface)

    style["drop_target.background"] = with_alpha(syn["function"]["color"], "40")

    # Icons
    style["icon"] = _hex8(fg)
    style["icon.muted"] = "#9898a0ff"
    style["icon.disabled"] = "#55555dff"
    style["icon.placeholder"] = "#9898a0ff"
    style["icon.accent"] = _hex8(syn["function"]["color"])

    # Tab bar
    style["tab_bar.background"] = _hex8(surface)
    style["tab.active_background"] = _hex8(bg)
    style["tab.inactive_background"] = _hex8(surface)

    # Status/title bar
    style["status_bar.background"] = _hex8(app_bg)
    style["title_bar.background"] = _hex8(app_bg)
    style["title_bar.inactive_background"] = _hex8(surface)
    style["toolbar.background"] = _hex8(bg)

    # Scrollbar
    style["scrollbar.thumb.background"] = with_alpha(fg, "1a")
    style["scrollbar.thumb.hover_background"] = with_alpha(fg, "33")
    style["scrollbar.thumb.border"] = "#00000000"
    style["scrollbar.track.background"] = "#00000000"
    style["scrollbar.track.border"] = _hex8(surface)

    # Editor
    style["editor.background"] = _hex8(bg)
    style["editor.foreground"] = _hex8(fg)
    style["editor.gutter.background"] = _hex8(bg)
    style["editor.subheader.background"] = _hex8(surface)
    style["editor.active_line.background"] = "#00000000"
    style["editor.highlighted_line.background"] = _hex8(surface)
    style["editor.line_number"] = _hex8(ed["lineNumber"])
    style["editor.active_line_number"] = _hex8(fg)
    style["editor.invisible"] = _hex8(invisible)
    style["editor.wrap_guide"] = _hex8(border_var)
    style["editor.active_wrap_guide"] = _hex8(border_main)
    style["editor.indent_guide"] = _hex8(border_var)
    style["editor.indent_guide_active"] = _hex8(indent_active)
    style["editor.document_highlight.read_background"] = _hex8(p["ui"]["identifierUnderCaret"])
    style["editor.document_highlight.write_background"] = with_alpha(syn["function"]["color"], "26")

    style["search.match_background"] = p["ui"]["searchResult"] + ("" if len(p["ui"]["searchResult"]) > 7 else "")

    # Links
    style["link_text.hover"] = _hex8(syn["link"]["color"])

    # Terminal
    style["terminal.background"] = _hex8(bg)
    style["terminal.foreground"] = _hex8(fg)
    style["terminal.bright_foreground"] = _hex8(t["brightWhite"])
    style["terminal.dim_foreground"] = "#777777ff"

    _terminal_colors = [
        ("black", t["black"]), ("red", t["red"]), ("green", t["green"]),
        ("yellow", t["yellow"]), ("blue", t["blue"]), ("magenta", t["magenta"]),
        ("cyan", t["cyan"]), ("white", t["white"]),
    ]
    _bright_map = {
        "black": t["brightBlack"], "red": t["brightRed"],
        "green": t["brightGreen"], "yellow": t["brightYellow"],
        "blue": t["brightBlue"], "magenta": t["brightMagenta"],
        "cyan": t["brightCyan"], "white": t["brightWhite"],
    }
    _dim_map_dark = {
        "black": "#333333", "red": "#ff9585", "green": "#90ba8c",
        "yellow": "#dad080", "blue": "#738bbe", "magenta": "#d588b3",
        "cyan": "#7dbbc7", "white": "#999999",
    }
    for name, color in _terminal_colors:
        style[f"terminal.ansi.{name}"] = _hex8(color)
        style[f"terminal.ansi.bright_{name}"] = _hex8(_bright_map[name])
        style[f"terminal.ansi.dim_{name}"] = _hex8(_dim_map_dark[name])

    # Status colors
    style["error"] = _hex8(st["error"])
    style["error.background"] = "#320001ff"
    style["error.border"] = with_alpha(st["error"], "33")
    style["warning"] = _hex8(st["warning"])
    style["warning.background"] = "#290d00ff"
    style["warning.border"] = with_alpha(st["warning"], "33")
    style["success"] = _hex8(st["success"])
    style["success.background"] = "#071b06ff"
    style["success.border"] = with_alpha(st["success"], "33")
    style["info"] = _hex8(st["info"])
    style["info.background"] = "#001928ff"
    style["info.border"] = with_alpha(st["info"], "33")
    style["hint"] = _hex8(st["hint"])
    style["hint.background"] = "#1a1127ff"
    style["hint.border"] = with_alpha(st["hint"], "33")

    style["conflict"] = _hex8(st["warning"])
    style["conflict.background"] = "#290d00ff"
    style["conflict.border"] = with_alpha(st["warning"], "33")
    style["created"] = _hex8(st["success"])
    style["created.background"] = "#071b06ff"
    style["created.border"] = with_alpha(st["success"], "33")
    style["deleted"] = _hex8(st["error"])
    style["deleted.background"] = "#320001ff"
    style["deleted.border"] = with_alpha(st["error"], "33")
    style["modified"] = _hex8(st["info"])
    style["modified.background"] = "#001928ff"
    style["modified.border"] = with_alpha(st["info"], "33")
    style["renamed"] = _hex8(st["hint"])
    style["renamed.background"] = "#1a1127ff"
    style["renamed.border"] = with_alpha(st["hint"], "33")

    style["hidden"] = "#6b6b73ff"
    style["hidden.background"] = _hex8(app_bg)
    style["hidden.border"] = _hex8(border_var)
    style["ignored"] = "#6b6b73ff"
    style["ignored.background"] = _hex8(app_bg)
    style["ignored.border"] = _hex8(border_main)
    style["unreachable"] = "#9898a0ff"
    style["unreachable.background"] = _hex8(app_bg)
    style["unreachable.border"] = _hex8(border_main)
    style["predictive"] = "#6b6b73ff"
    style["predictive.background"] = _hex8(app_bg)
    style["predictive.border"] = _hex8(border_var)

    # Players
    player_colors = [
        syn["keyword"]["color"], syn["function"]["color"],
        syn["interface"]["color"], syn["tag"]["color"],
        syn["constant"]["color"], syn["operator"]["color"],
        st["warning"], syn["class"]["color"],
    ]
    players = []
    for c in player_colors:
        players.append({
            "cursor": _hex8(c),
            "background": _hex8(c),
            "selection": with_alpha(c, "33"),
        })
    style["players"] = players

    # Syntax
    style["syntax"] = _zed_dark_syntax(syn, fg)

    return {
        "name": "Deligoez Dark",
        "appearance": "dark",
        "style": style,
    }


def _zed_dark_syntax(syn, fg):
    s = {}
    s["attribute"] = _zed_syntax_entry(_hex8(syn["interface"]["color"]))
    s["boolean"] = _zed_syntax_entry(_hex8(syn["keyword"]["color"]), font_style="italic")
    s["comment"] = _zed_syntax_entry(_hex8(syn["comment"]["color"]), font_style="italic")
    s["comment.doc"] = _zed_syntax_entry(_hex8(syn["commentDoc"]["color"]), font_style="italic")
    s["constant"] = _zed_syntax_entry(_hex8(syn["constant"]["color"]))
    s["constructor"] = _zed_syntax_entry(_hex8(syn["class"]["color"]))
    s["embedded"] = _zed_syntax_entry(_hex8(fg))
    s["emphasis"] = _zed_syntax_entry(_hex8(fg), font_style="italic")
    s["emphasis.strong"] = _zed_syntax_entry(_hex8(fg), font_weight=700)
    s["enum"] = _zed_syntax_entry(_hex8(syn["interface"]["color"]))
    s["function"] = _zed_syntax_entry(_hex8(syn["function"]["color"]))
    s["hint"] = _zed_syntax_entry("#adb6bdff")
    s["keyword"] = _zed_syntax_entry(_hex8(syn["keyword"]["color"]), font_style="italic")
    s["label"] = _zed_syntax_entry("#adb6bdff")
    s["link_text"] = _zed_syntax_entry(_hex8(syn["link"]["color"]), font_style="italic")
    s["link_uri"] = _zed_syntax_entry(_hex8(syn["link"]["color"]))
    s["namespace"] = _zed_syntax_entry(_hex8(syn["class"]["color"]))
    s["number"] = _zed_syntax_entry(_hex8(syn["number"]["color"]))
    s["operator"] = _zed_syntax_entry(_hex8(syn["operator"]["color"]), font_weight=700)
    s["predictive"] = _zed_syntax_entry("#6b6b73ff", font_style="italic")
    s["preproc"] = _zed_syntax_entry(_hex8(syn["phpTag"]["color"]))
    s["primary"] = _zed_syntax_entry(_hex8(fg))
    s["property"] = _zed_syntax_entry(_hex8(syn["class"]["color"]))
    s["punctuation"] = _zed_syntax_entry(_hex8(fg))
    s["punctuation.bracket"] = _zed_syntax_entry(_hex8(fg))
    s["punctuation.delimiter"] = _zed_syntax_entry(_hex8(fg))
    s["punctuation.list_marker"] = _zed_syntax_entry(_hex8(syn["operator"]["color"]))
    s["punctuation.markup"] = _zed_syntax_entry(_hex8(syn["operator"]["color"]))
    s["punctuation.special"] = _zed_syntax_entry(_hex8(syn["phpTag"]["color"]))
    s["selector"] = _zed_syntax_entry(_hex8(syn["tag"]["color"]))
    s["selector.pseudo"] = _zed_syntax_entry(_hex8(syn["interface"]["color"]))
    s["string"] = _zed_syntax_entry(_hex8(syn["string"]["color"]))
    s["string.escape"] = _zed_syntax_entry(_hex8(syn["attributeValue"]["color"]))
    s["string.regex"] = _zed_syntax_entry(_hex8(syn["regex"]["color"]))
    s["string.special"] = _zed_syntax_entry(_hex8(syn["stringSpecial"]["color"]))
    s["string.special.symbol"] = _zed_syntax_entry(_hex8(syn["symbol"]["color"]))
    s["tag"] = _zed_syntax_entry(_hex8(syn["tag"]["color"]))
    s["text.literal"] = _zed_syntax_entry(_hex8(syn["string"]["color"]))
    s["title"] = _zed_syntax_entry(_hex8(syn["class"]["color"]), font_weight=700)
    s["type"] = _zed_syntax_entry(_hex8(syn["class"]["color"]))
    s["variable"] = _zed_syntax_entry(_hex8(fg))
    s["variable.special"] = _zed_syntax_entry(_hex8(syn["variableSpecial"]["color"]))
    s["variant"] = _zed_syntax_entry(_hex8(syn["interface"]["color"]))
    return s


# ---------------------------------------------------------------------------
# PHPStorm generator
# ---------------------------------------------------------------------------

def _ps_opt(name, value):
    """Single <option name="X" value="Y" /> line."""
    return f'        <option name="{name}" value="{value}" />'


def _ps_attr_empty(name):
    """Attribute with empty value."""
    return f'    <option name="{name}">\n      <value />\n    </option>'


def _ps_attr(name, *, fg=None, bg=None, font_type=None, effect_color=None, effect_type=None, error_stripe=None):
    """Build an attribute entry."""
    opts = []
    if fg is not None:
        opts.append(f'        <option name="FOREGROUND" value="{phpstorm_hex(fg)}" />')
    if bg is not None:
        opts.append(f'        <option name="BACKGROUND" value="{phpstorm_hex(bg)}" />')
    if font_type is not None:
        opts.append(f'        <option name="FONT_TYPE" value="{font_type}" />')
    if effect_color is not None:
        opts.append(f'        <option name="EFFECT_COLOR" value="{phpstorm_hex(effect_color)}" />')
    if error_stripe is not None:
        opts.append(f'        <option name="ERROR_STRIPE_COLOR" value="{phpstorm_hex(error_stripe)}" />')
    if effect_type is not None:
        opts.append(f'        <option name="EFFECT_TYPE" value="{effect_type}" />')

    if not opts:
        return _ps_attr_empty(name)

    inner = "\n".join(opts)
    return f'    <option name="{name}">\n      <value>\n{inner}\n      </value>\n    </option>'


def generate_phpstorm(palette):
    for variant in ("light", "dark"):
        p = palette[variant]
        syn = p["syntax"]
        ed = p["editor"]
        ui = p["ui"]
        diff = p["diff"]
        t = p["terminal"]
        st = p["status"]
        rb = p["rainbow"]
        sass = p["sass"]

        parent = "Default" if variant == "light" else "Darcula"
        scheme_name = f"deligoez-{variant}"

        lines = []
        lines.append(f'<scheme name="{scheme_name}" version="142" parent_scheme="{parent}">')
        lines.append('  <option name="FONT_SCALE" value="1.0" />')
        lines.append('  <metaInfo>')
        lines.append('    <property name="created">2022-02-10T18:38:05</property>')
        lines.append('    <property name="ide">PhpStorm</property>')
        lines.append('    <property name="ideVersion">2021.3.2.0.0</property>')
        lines.append('    <property name="modified">2022-02-10T18:38:12</property>')
        lines.append(f'    <property name="originalScheme">{scheme_name}</property>')
        lines.append('  </metaInfo>')
        lines.append('  <option name="CONSOLE_FONT_NAME" value="MonoLisa" />')
        lines.append('  <option name="CONSOLE_FONT_SIZE" value="17" />')
        lines.append('  <option name="CONSOLE_LIGATURES" value="true" />')
        lines.append('  <option name="CONSOLE_LINE_SPACING" value="1.7" />')

        # --- colors block ---
        lines.append('  <colors>')
        if variant == "light":
            _gen_light_colors(lines, p)
        else:
            _gen_dark_colors(lines, p)
        lines.append('  </colors>')

        # --- attributes block ---
        lines.append('  <attributes>')
        if variant == "light":
            _gen_light_pre_mn_attrs(lines, p)
        else:
            _gen_dark_pre_mn_attrs(lines, p)

        # Insert MARKDOWN_NAVIGATOR template
        mn_path = os.path.join(ROOT, "phpstorm", "templates", f"markdown-navigator-{variant}.xml")
        with open(mn_path) as f:
            lines.append(f.read().rstrip("\n"))

        # Post-MN attributes
        if variant == "light":
            _gen_light_post_mn_attrs(lines, p)
        else:
            _gen_dark_post_mn_attrs(lines, p)

        lines.append('  </attributes>')
        lines.append('</scheme>')

        path = os.path.join(ROOT, "phpstorm", f"deligoez-{variant}.icls")
        write_file(path, "\n".join(lines))


def _color_opt(name, value):
    """Color option line. value is already phpstorm-formatted."""
    return f'    <option name="{name}" value="{value}" />'


def _gen_light_colors(lines, p):
    lines.append(_color_opt("CARET_ROW_COLOR", ""))
    lines.append(_color_opt("CODE_LENS_BORDER_COLOR", "e8e8e8"))
    lines.append(_color_opt("CONSOLE_BACKGROUND_KEY", "ffffff"))
    lines.append(_color_opt("GUTTER_BACKGROUND", "ffffff"))
    lines.append(_color_opt("INDENT_GUIDE", "e8e8e8"))
    lines.append(_color_opt("LINE_NUMBERS_COLOR", "e5e5e5"))
    lines.append(_color_opt("MATCHED_BRACES_INDENT_GUIDE_COLOR", "e8e8e8"))
    lines.append(_color_opt("METHOD_SEPARATORS_COLOR", "e8e8e8"))
    lines.append(_color_opt("RIGHT_MARGIN_COLOR", "e8e8e8"))
    lines.append(_color_opt("SELECTED_INDENT_GUIDE", "c8c8c8"))
    lines.append(_color_opt("SELECTION_BACKGROUND", phpstorm_hex(p["editor"]["selection"])))
    lines.append(_color_opt("SELECTION_FOREGROUND", ""))
    lines.append(_color_opt("SOFT_WRAP_SIGN_COLOR", "c8c8c8"))
    lines.append(_color_opt("TEARLINE_COLOR", "e3e3e3"))
    lines.append(_color_opt("VISUAL_INDENT_GUIDE", "e8e8e8"))


def _gen_dark_colors(lines, p):
    lines.append(_color_opt("CARET_COLOR", phpstorm_hex("#ce5391")))
    lines.append(_color_opt("CARET_ROW_COLOR", ""))
    lines.append(_color_opt("CONSOLE_BACKGROUND_KEY", phpstorm_hex(p["editor"]["background"])))
    lines.append(_color_opt("DOCUMENTATION_COLOR", "1e1e22"))
    lines.append(_color_opt("GUTTER_BACKGROUND", phpstorm_hex(p["editor"]["background"])))
    lines.append(_color_opt("CODE_LENS_BORDER_COLOR", "222227"))
    lines.append(_color_opt("INDENT_GUIDE", "222227"))
    lines.append(_color_opt("MATCHED_BRACES_INDENT_GUIDE_COLOR", "222227"))
    lines.append(_color_opt("LINE_NUMBERS_COLOR", phpstorm_hex(p["editor"]["lineNumber"])))
    lines.append(_color_opt("LINE_NUMBER_ON_CARET_ROW_COLOR", phpstorm_hex(p["editor"]["foreground"])))
    lines.append(_color_opt("METHOD_SEPARATORS_COLOR", "222227"))
    lines.append(_color_opt("NOTIFICATION_BACKGROUND", "1e1e22"))
    lines.append(_color_opt("RIGHT_MARGIN_COLOR", "222227"))
    lines.append(_color_opt("SELECTED_INDENT_GUIDE", "35353b"))
    lines.append(_color_opt("SELECTION_BACKGROUND", phpstorm_hex(p["editor"]["selection"])))
    lines.append(_color_opt("SELECTION_FOREGROUND", ""))
    lines.append(_color_opt("ScrollBar.Mac.thumbColor", ""))
    lines.append(_color_opt("SOFT_WRAP_SIGN_COLOR", "35353b"))
    lines.append(_color_opt("TEARLINE_COLOR", "222227"))
    lines.append(_color_opt("VISUAL_INDENT_GUIDE", "222227"))


def _gen_light_pre_mn_attrs(lines, p):
    syn = p["syntax"]
    ui = p["ui"]
    diff = p["diff"]
    t = p["terminal"]

    lines.append(_ps_attr_empty("APACHE_CONFIG.ARG_LEXEM"))
    lines.append(_ps_attr("APACHE_CONFIG.COMMENT", fg=syn["commentDoc"]["color"]))
    lines.append(_ps_attr_empty("APACHE_CONFIG.IDENTIFIER"))
    lines.append(_ps_attr("BREAKPOINT_ATTRIBUTES", bg=ui["breakpoint"]))
    lines.append(_ps_attr("COFFEESCRIPT.FUNCTION_BINDING", fg="#000080", font_type="1"))
    lines.append(_ps_attr("CONSOLE_BLUE_OUTPUT", fg=t["brightBlue"]))
    lines.append(_ps_attr("CONSOLE_GREEN_BRIGHT_OUTPUT", fg=t["brightGreen"]))
    lines.append(_ps_attr("CONSOLE_NORMAL_OUTPUT", fg="#7d9496"))
    lines.append(_ps_attr("CONSOLE_RANGE_TO_EXECUTE", bg="#e5fafc"))
    lines.append(_ps_attr("CONSOLE_YELLOW_OUTPUT", fg=t["brightYellow"]))
    lines.append(_ps_attr("CSS.COMMENT", fg=syn["commentDoc"]["color"], font_type="2"))
    lines.append(_ps_attr("CSS.FUNCTION", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("CSS.IDENT", fg="#445588", font_type="1"))
    lines.append(_ps_attr("CSS.IMPORTANT", font_type="1"))
    lines.append(_ps_attr("CSS.KEYWORD", fg="#000080", effect_type="1"))
    lines.append(_ps_attr("CSS.NUMBER", fg=syn["number"]["color"]))
    lines.append(_ps_attr("CSS.PROPERTY_NAME", font_type="1"))
    lines.append(_ps_attr("CSS.PROPERTY_VALUE", font_type="1"))
    lines.append(_ps_attr("CSS.STRING", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("CSS.TAG_NAME", fg="#000080"))
    lines.append(_ps_attr("CSS.URL", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("DEFAULT_ATTRIBUTE", fg="#0000ff"))
    lines.append(_ps_attr_empty("DEFAULT_BRACES"))
    lines.append(_ps_attr("DEFAULT_CLASS_NAME", fg="#000000"))
    lines.append(_ps_attr("DEFAULT_CONSTANT", fg=syn["symbol"]["color"], font_type="2"))
    lines.append(_ps_attr("DEFAULT_DOC_COMMENT_TAG", effect_color="#808080", effect_type="1"))
    lines.append(_ps_attr("DEFAULT_DOC_COMMENT_TAG_VALUE", fg="#3d3d3d", font_type="2"))
    lines.append(_ps_attr("DEFAULT_ENTITY", fg="#0000ff"))
    lines.append(_ps_attr("DEFAULT_INSTANCE_FIELD", fg=syn["symbol"]["color"]))
    lines.append(_ps_attr("DEFAULT_KEYWORD", fg="#000080"))
    lines.append(_ps_attr("DEFAULT_LABEL", effect_color="#808080", effect_type="1"))
    lines.append(_ps_attr("DEFAULT_OPERATION_SIGN", font_type="1"))
    lines.append(_ps_attr("DEFAULT_STRING", fg=syn["string"]["color"]))
    lines.append(_ps_attr("DEFAULT_VALID_STRING_ESCAPE", fg="#000080"))
    lines.append(_ps_attr("DIFF_DELETED", bg=diff["deleted"], error_stripe="#cbcbcb"))
    lines.append(_ps_attr("DIFF_INSERTED", bg=diff["inserted"], error_stripe="#baeeba"))
    lines.append(_ps_attr("DIFF_MODIFIED", bg=diff["modified"], error_stripe="#bccff9"))
    lines.append(_ps_attr("EXECUTIONPOINT_ATTRIBUTES", fg="#ffffff", bg="#0000ff"))
    lines.append(_ps_attr("FOLDED_TEXT_ATTRIBUTES", fg=ui["foldedText"], bg="#f6f6f6", effect_type="1"))
    lines.append(_ps_attr("FOLLOWED_HYPERLINK_ATTRIBUTES", fg="#0000ff", bg="#e9e9e9", font_type="2", effect_color="#0000ff", effect_type="1"))
    lines.append(_ps_attr("GENERIC_SERVER_ERROR_OR_WARNING", effect_color="#f49810", error_stripe="#f49810", effect_type="2"))
    lines.append(_ps_attr("HTML_ATTRIBUTE_NAME", fg=syn["attribute"]["color"]))
    lines.append(_ps_attr("HTML_ATTRIBUTE_VALUE", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr_empty("HTML_CODE"))
    lines.append(_ps_attr("HTML_COMMENT", fg=syn["commentDoc"]["color"], font_type="2"))
    lines.append(_ps_attr("HTML_ENTITY_REFERENCE", font_type="1"))
    lines.append(_ps_attr("HTML_TAG", fg=p["editor"]["foreground"]))
    lines.append(_ps_attr("HTML_TAG_NAME", fg=syn["tag"]["color"]))
    lines.append(_ps_attr("HYPERLINK_ATTRIBUTES", fg="#0000ff", font_type="2", effect_color="#0000ff", effect_type="1"))
    lines.append(_ps_attr("IDENTIFIER_UNDER_CARET_ATTRIBUTES", bg=ui["identifierUnderCaret"], error_stripe="#ccccff"))
    lines.append(_ps_attr("INDENT_RAINBOW_COLOR_1", bg="#ffffe8"))
    lines.append(_ps_attr("INDENT_RAINBOW_COLOR_2", bg="#f0fff0"))
    lines.append(_ps_attr("INDENT_RAINBOW_COLOR_3", bg="#fff0ff"))
    lines.append(_ps_attr("INDENT_RAINBOW_COLOR_4", bg="#eafdfd"))
    lines.append(_ps_attr("INDENT_RAINBOW_ERROR", bg="#d9bcbc"))
    lines.append(_ps_attr("INFO_ATTRIBUTES", effect_color="#b5beca", error_stripe="#ffffcc", effect_type="5"))
    lines.append(_ps_attr("INLINE_PARAMETER_HINT", fg="#d0d0d0"))
    lines.append(_ps_attr("INLINE_PARAMETER_HINT_CURRENT", fg="#9b9b9b", bg="#c0defb"))
    lines.append(_ps_attr_empty("JS.BADCHARACTER"))
    lines.append(_ps_attr("JS.BLOCK_COMMENT", fg="#969896", font_type="2"))
    lines.append(_ps_attr("JS.DOC_COMMENT", fg="#969896"))
    lines.append(_ps_attr_empty("JS.DOC_MARKUP"))
    lines.append(_ps_attr("JS.DOC_TAG", effect_type="1"))
    lines.append(_ps_attr_empty("JS.GLOBAL_FUNCTION"))
    lines.append(_ps_attr("JS.GLOBAL_VARIABLE", fg=syn["predefined"]["color"]))
    lines.append(_ps_attr("JS.INSTANCE_MEMBER_FUNCTION", fg=syn["interface"]["color"]))
    lines.append(_ps_attr_empty("JS.INSTANCE_MEMBER_VARIABLE"))
    lines.append(_ps_attr("JS.INVALID_STRING_ESCAPE", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("JS.KEYWORD", fg=syn["operator"]["color"]))
    lines.append(_ps_attr("JS.LINE_COMMENT", fg="#969896", font_type="2"))
    lines.append(_ps_attr_empty("JS.LOCAL_VARIABLE"))
    lines.append(_ps_attr("JS.NUMBER", fg=syn["number"]["color"]))
    lines.append(_ps_attr("JS.OPERATION_SIGN", fg=syn["operator"]["color"]))
    lines.append(_ps_attr("JS.PARAMETER", effect_type="1"))
    lines.append(_ps_attr("JS.REGEXP", fg=syn["regex"]["color"]))
    lines.append(_ps_attr_empty("JS.STATIC_MEMBER_FUNCTION"))
    lines.append(_ps_attr_empty("JS.STATIC_MEMBER_VARIABLE"))
    lines.append(_ps_attr("JS.STRING", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("JS.VALID_STRING_ESCAPE", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW", font_type="1"))
    lines.append(_ps_attr_empty("KOTLIN_LABEL"))
    lines.append(_ps_attr("LESS_IMPORTANT", fg=syn["operator"]["color"]))
    lines.append(_ps_attr_empty("LESS_PROPERTY_NAME"))
    lines.append(_ps_attr_empty("LESS_PROPERTY_VALUE"))
    lines.append(_ps_attr("LOG_ERROR_OUTPUT", fg="#ff0000"))
    lines.append(_ps_attr("LOG_WARNING_OUTPUT", fg="#ffa500"))
    lines.append(_ps_attr("LUA_KEYWORD", fg="#000080"))
    lines.append(_ps_attr("LUA_LONGSTRING", fg="#008000"))
    lines.append(_ps_attr("LUA_NUMBER", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("LUA_STRING", fg="#008000"))
    lines.append(_ps_attr("MAGIC_MEMBER_ACCESS", fg=syn["constant"]["color"]))


def _gen_dark_pre_mn_attrs(lines, p):
    syn = p["syntax"]
    ui = p["ui"]
    diff = p["diff"]
    t = p["terminal"]

    lines.append(_ps_attr_empty("APACHE_CONFIG.ARG_LEXEM"))
    lines.append(_ps_attr("APACHE_CONFIG.COMMENT", fg=syn["comment"]["color"]))
    lines.append(_ps_attr_empty("APACHE_CONFIG.IDENTIFIER"))
    lines.append(_ps_attr("BREAKPOINT_ATTRIBUTES", bg="#140707"))
    lines.append(_ps_attr("COFFEESCRIPT.FUNCTION_BINDING", fg="#5a83db", font_type="1"))
    lines.append(_ps_attr("CONSOLE_BLUE_OUTPUT", fg=t["brightBlue"]))
    lines.append(_ps_attr("CONSOLE_GREEN_BRIGHT_OUTPUT", fg=t["brightGreen"]))
    lines.append(_ps_attr("CONSOLE_NORMAL_OUTPUT", fg="#bfd2d3"))
    lines.append(_ps_attr("CONSOLE_RANGE_TO_EXECUTE", bg="#000101"))
    lines.append(_ps_attr("CONSOLE_YELLOW_OUTPUT", fg=t["brightYellow"]))
    lines.append(_ps_attr("CSS.COMMENT", fg=syn["comment"]["color"], font_type="2"))
    lines.append(_ps_attr("CSS.FUNCTION", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("CSS.IDENT", fg="#afc0eb", font_type="1"))
    lines.append(_ps_attr("CSS.IMPORTANT", font_type="1"))
    lines.append(_ps_attr("CSS.KEYWORD", fg="#5a83db", effect_type="1"))
    lines.append(_ps_attr("CSS.NUMBER", fg=syn["number"]["color"]))
    lines.append(_ps_attr("CSS.PROPERTY_NAME", font_type="1"))
    lines.append(_ps_attr("CSS.PROPERTY_VALUE", font_type="1"))
    lines.append(_ps_attr("CSS.STRING", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("CSS.TAG_NAME", fg="#5a83db"))
    lines.append(_ps_attr("CSS.URL", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("DEFAULT_ATTRIBUTE", fg=syn["link"]["color"]))
    lines.append(_ps_attr_empty("DEFAULT_BRACES"))
    lines.append(_ps_attr("DEFAULT_CLASS_NAME", fg="#717171"))
    lines.append(_ps_attr("DEFAULT_CONSTANT", fg=syn["symbol"]["color"], font_type="2"))
    lines.append(_ps_attr("DEFAULT_DOC_COMMENT_TAG", effect_color="#aeaeae", effect_type="1"))
    lines.append(_ps_attr("DEFAULT_DOC_COMMENT_TAG_VALUE", fg="#a1a1a1", font_type="2"))
    lines.append(_ps_attr("DEFAULT_ENTITY", fg=syn["link"]["color"]))
    lines.append(_ps_attr("DEFAULT_INSTANCE_FIELD", fg=syn["symbol"]["color"]))
    lines.append(_ps_attr("DEFAULT_KEYWORD", fg="#5a83db"))
    lines.append(_ps_attr("DEFAULT_LABEL", effect_color="#aeaeae", effect_type="1"))
    lines.append(_ps_attr("DEFAULT_OPERATION_SIGN", font_type="1"))
    lines.append(_ps_attr("DEFAULT_STRING", fg=syn["string"]["color"]))
    lines.append(_ps_attr("DEFAULT_VALID_STRING_ESCAPE", fg="#5a83db"))
    lines.append(_ps_attr("DIFF_DELETED", bg="#0c0c0c", error_stripe="#aeaeae"))
    lines.append(_ps_attr("DIFF_INSERTED", bg="#010601", error_stripe="#9ab79a"))
    lines.append(_ps_attr("DIFF_MODIFIED", bg="#070a12", error_stripe="#a3aec6"))
    lines.append(_ps_attr("EXECUTIONPOINT_ATTRIBUTES", fg="#cecece", bg="#5377c4"))
    lines.append(_ps_attr("FOLDED_TEXT_ATTRIBUTES", fg="#a7b0b8", bg="#010101", effect_type="1"))
    lines.append(_ps_attr("FOLLOWED_HYPERLINK_ATTRIBUTES", fg=syn["link"]["color"], bg="#030303", font_type="2", effect_color="#3a74ff", effect_type="1"))
    lines.append(_ps_attr("GENERIC_SERVER_ERROR_OR_WARNING", effect_color="#df9f59", error_stripe="#d8a268", effect_type="2"))
    lines.append(_ps_attr("HTML_ATTRIBUTE_NAME", fg=syn["attribute"]["color"]))
    lines.append(_ps_attr("HTML_ATTRIBUTE_VALUE", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr_empty("HTML_CODE"))
    lines.append(_ps_attr("HTML_COMMENT", fg=syn["comment"]["color"], font_type="2"))
    lines.append(_ps_attr("HTML_ENTITY_REFERENCE", font_type="1"))
    lines.append(_ps_attr("HTML_TAG", fg="#959595"))
    lines.append(_ps_attr("HTML_TAG_NAME", fg=syn["tag"]["color"]))
    lines.append(_ps_attr("HYPERLINK_ATTRIBUTES", fg=syn["link"]["color"], font_type="2", effect_color="#3a74ff", effect_type="1"))
    lines.append(_ps_attr("IDENTIFIER_UNDER_CARET_ATTRIBUTES", bg="#020202", error_stripe="#aaabc8"))
    lines.append(_ps_attr("INDENT_RAINBOW_COLOR_1", bg="#1f1f18"))
    lines.append(_ps_attr("INDENT_RAINBOW_COLOR_2", bg="#181f18"))
    lines.append(_ps_attr("INDENT_RAINBOW_COLOR_3", bg="#1f181f"))
    lines.append(_ps_attr("INDENT_RAINBOW_COLOR_4", bg="#181e1e"))
    lines.append(_ps_attr("INDENT_RAINBOW_ERROR", bg="#2d1e1e"))
    lines.append(_ps_attr("INFO_ATTRIBUTES", effect_color="#a8aeb7", error_stripe="#b0b094", effect_type="5"))
    lines.append(_ps_attr("INLINE_PARAMETER_HINT", fg="#cecece"))
    lines.append(_ps_attr("INLINE_PARAMETER_HINT_CURRENT", fg="#bababa", bg="#040a12"))
    lines.append(_ps_attr_empty("JS.BADCHARACTER"))
    lines.append(_ps_attr("JS.BLOCK_COMMENT", fg=syn["comment"]["color"], font_type="2"))
    lines.append(_ps_attr("JS.DOC_COMMENT", fg=syn["commentDoc"]["color"]))
    lines.append(_ps_attr_empty("JS.DOC_MARKUP"))
    lines.append(_ps_attr("JS.DOC_TAG", effect_type="1"))
    lines.append(_ps_attr_empty("JS.GLOBAL_FUNCTION"))
    lines.append(_ps_attr("JS.GLOBAL_VARIABLE", fg="#7bc2e6"))
    lines.append(_ps_attr("JS.INSTANCE_MEMBER_FUNCTION", fg=syn["interface"]["color"]))
    lines.append(_ps_attr_empty("JS.INSTANCE_MEMBER_VARIABLE"))
    lines.append(_ps_attr("JS.INVALID_STRING_ESCAPE", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("JS.KEYWORD", fg=syn["operator"]["color"]))
    lines.append(_ps_attr("JS.LINE_COMMENT", fg=syn["comment"]["color"], font_type="2"))
    lines.append(_ps_attr_empty("JS.LOCAL_VARIABLE"))
    lines.append(_ps_attr("JS.NUMBER", fg=syn["number"]["color"]))
    lines.append(_ps_attr("JS.OPERATION_SIGN", fg=syn["operator"]["color"]))
    lines.append(_ps_attr("JS.PARAMETER", effect_type="1"))
    lines.append(_ps_attr("JS.REGEXP", fg=syn["regex"]["color"]))
    lines.append(_ps_attr_empty("JS.STATIC_MEMBER_FUNCTION"))
    lines.append(_ps_attr_empty("JS.STATIC_MEMBER_VARIABLE"))
    lines.append(_ps_attr("JS.STRING", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("JS.VALID_STRING_ESCAPE", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW", font_type="1"))
    lines.append(_ps_attr_empty("KOTLIN_LABEL"))
    lines.append(_ps_attr("LESS_IMPORTANT", fg=syn["operator"]["color"]))
    lines.append(_ps_attr_empty("LESS_PROPERTY_NAME"))
    lines.append(_ps_attr_empty("LESS_PROPERTY_VALUE"))
    lines.append(_ps_attr("LOG_ERROR_OUTPUT", fg=t["brightRed"]))
    lines.append(_ps_attr("LOG_WARNING_OUTPUT", fg="#ffbf6a"))
    lines.append(_ps_attr("LUA_KEYWORD", fg="#5a83db"))
    lines.append(_ps_attr("LUA_LONGSTRING", fg="#70b96b"))
    lines.append(_ps_attr("LUA_NUMBER", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("LUA_STRING", fg="#70b96b"))
    lines.append(_ps_attr("MAGIC_MEMBER_ACCESS", fg=syn["constant"]["color"]))


def _gen_light_post_mn_attrs(lines, p):
    syn = p["syntax"]
    ui = p["ui"]
    rb = p["rainbow"]
    sass = p["sass"]

    lines.append(_ps_attr("MATCHED_BRACE_ATTRIBUTES", bg=ui["matchedBrace"], font_type="1"))
    lines.append(_ps_attr("NOT_USED_ELEMENT_ATTRIBUTES", effect_color="#b5beca", effect_type="5"))
    lines.append(_ps_attr("PHP_CLASS", fg=syn["class"]["color"]))
    lines.append(_ps_attr("PHP_COMMENT", fg=syn["comment"]["color"], font_type="2"))
    lines.append(_ps_attr("PHP_CONSTANT", fg=syn["constant"]["color"]))
    lines.append(_ps_attr("PHP_DOC_COMMENT_ID", fg=syn["commentDoc"]["color"], font_type="2"))
    lines.append(_ps_attr("PHP_DOC_IDENTIFIER", fg="#808080", effect_type="1"))
    lines.append(_ps_attr("PHP_DOC_PARAMETER", fg="#808080"))
    lines.append(_ps_attr("PHP_DOC_TAG", fg=syn["commentDocTag"]["color"], font_type="3", effect_type="1"))
    lines.append(_ps_attr("PHP_ESCAPE_SEQUENCE", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("PHP_EXEC_COMMAND_ID", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("PHP_FUNCTION", fg=syn["function"]["color"]))
    lines.append(_ps_attr("PHP_HEREDOC_CONTENT", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("PHP_HEREDOC_ID", effect_type="1"))
    lines.append(_ps_attr("PHP_IDENTIFIER", fg=syn["variableSpecial"]["color"], effect_type="1"))
    lines.append(_ps_attr("PHP_INSTANCE_FIELD", fg=syn["property"]["color"]))
    lines.append(_ps_attr("PHP_INSTANCE_METHOD", fg=syn["instanceMethod"]["color"]))
    lines.append(_ps_attr("PHP_INTERFACE", fg=syn["interface"]["color"]))
    lines.append(_ps_attr("PHP_KEYWORD", fg=syn["keyword"]["color"], font_type="2"))
    lines.append(_ps_attr("PHP_MARKUP_ID", fg="#1b42fb", font_type="2"))
    lines.append(_ps_attr("PHP_NUMBER", fg=syn["number"]["color"]))
    lines.append(_ps_attr("PHP_OPERATION_SIGN", fg=syn["operator"]["color"], font_type="1"))
    lines.append(_ps_attr("PHP_PARAMETER", fg=syn["parameter"]["color"]))
    lines.append(_ps_attr("PHP_PREDEFINED SYMBOL", fg=syn["predefined"]["color"]))
    lines.append(_ps_attr("PHP_SCRIPTING_BACKGROUND", fg=p["editor"]["foreground"]))
    lines.append(_ps_attr("PHP_STATIC_METHOD", fg=syn["parameter"]["color"]))
    lines.append(_ps_attr("PHP_STRING", fg=syn["string"]["color"]))
    lines.append(_ps_attr("PHP_TAG", fg=syn["phpTag"]["color"]))
    lines.append(_ps_attr("PHP_VAR", fg=syn["variable"]["color"]))
    lines.append(_ps_attr("PHP_THIS_VAR", fg=syn["variableSpecial"]["color"], font_type="2"))
    lines.append(_ps_attr("PHP_VAR_VAR", fg=syn["variableSpecial"]["color"]))
    lines.append(_ps_attr("PHP_FUNCTION_CALL", fg=syn["function"]["color"]))
    lines.append(_ps_attr("PHP_NAMED_ARGUMENT", fg=syn["commentDocTag"]["color"], font_type="2"))
    lines.append(_ps_attr("PHP_ATTRIBUTE", fg=syn["interface"]["color"]))
    lines.append(_ps_attr("PHP_ENUM", fg=syn["interface"]["color"]))
    lines.append(_ps_attr("PHP_ENUM_CASE", fg=syn["constant"]["color"]))
    lines.append(_ps_attr("PHP_READONLY", fg=syn["keyword"]["color"], font_type="2"))
    lines.append(_ps_attr("RAINBOW_COLOR0", fg=rb["color0"]))
    lines.append(_ps_attr("RAINBOW_COLOR1", fg=rb["color1"]))
    lines.append(_ps_attr("RAINBOW_COLOR2", fg=rb["color2"]))
    lines.append(_ps_attr("RAINBOW_COLOR3", fg=rb["color3"]))
    lines.append(_ps_attr("RAINBOW_COLOR4", fg=rb["color4"]))
    lines.append(_ps_attr("SASS_IDENTIFIER", fg=sass["identifier"]))
    lines.append(_ps_attr("SASS_VARIABLE", fg=sass["variable"]))
    lines.append(_ps_attr("TEXT", fg=p["editor"]["foreground"], bg=p["editor"]["background"]))
    lines.append(_ps_attr("TEXT_SEARCH_RESULT_ATTRIBUTES", bg=ui["searchResult"], error_stripe="#00ff00"))
    lines.append(_ps_attr("TODO_DEFAULT_ATTRIBUTES", fg=ui["todo"], font_type="3", error_stripe=ui["todo"]))
    lines.append(_ps_attr("TWIG_KEYWORD", fg="#000080"))
    lines.append(_ps_attr("TYPO", effect_color="#88e99f", effect_type="4"))
    lines.append(_ps_attr("WARNING_ATTRIBUTES", effect_type="1"))
    lines.append(_ps_attr("WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES", bg=ui["identifierUnderCaret"], error_stripe="#ffcdff"))
    lines.append(_ps_attr("XML_ATTRIBUTE_NAME", fg=syn["attribute"]["color"]))
    lines.append(_ps_attr("XML_ATTRIBUTE_VALUE", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("XML_NS_PREFIX", fg=syn["attribute"]["color"]))
    lines.append(_ps_attr_empty("XML_PROLOGUE"))
    lines.append(_ps_attr_empty("XML_TAG"))
    lines.append(_ps_attr("XML_TAG_NAME", fg=syn["tag"]["color"]))
    lines.append(_ps_attr("YAML_COMMENT", fg=syn["commentDoc"]["color"]))
    lines.append(_ps_attr("YAML_SCALAR_DSTRING", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("YAML_SCALAR_KEY", fg=syn["tag"]["color"]))
    lines.append(_ps_attr_empty("YAML_SCALAR_LIST"))
    lines.append(_ps_attr("YAML_SCALAR_STRING", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("YAML_SCALAR_VALUE", font_type="1"))
    lines.append(_ps_attr("YAML_SIGN", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("YAML_TEXT", fg=syn["predefined"]["color"]))


def _gen_dark_post_mn_attrs(lines, p):
    syn = p["syntax"]
    ui = p["ui"]
    rb = p["rainbow"]
    sass = p["sass"]

    lines.append(_ps_attr("MATCHED_BRACE_ATTRIBUTES", bg="#101f1b", font_type="1"))
    lines.append(_ps_attr("NOT_USED_ELEMENT_ATTRIBUTES", effect_color="#a8aeb7", effect_type="5"))
    lines.append(_ps_attr("PHP_CLASS", fg=syn["class"]["color"]))
    lines.append(_ps_attr("PHP_COMMENT", fg=syn["comment"]["color"], font_type="2"))
    lines.append(_ps_attr("PHP_CONSTANT", fg=syn["constant"]["color"]))
    lines.append(_ps_attr("PHP_DOC_COMMENT_ID", fg=syn["commentDoc"]["color"], font_type="2"))
    lines.append(_ps_attr("PHP_DOC_IDENTIFIER", fg="#808080", effect_type="1"))
    lines.append(_ps_attr("PHP_DOC_PARAMETER", fg="#808080"))
    lines.append(_ps_attr("PHP_DOC_TAG", fg=syn["commentDocTag"]["color"], font_type="3", effect_type="1"))
    lines.append(_ps_attr("PHP_ESCAPE_SEQUENCE", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("PHP_EXEC_COMMAND_ID", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("PHP_FUNCTION", fg=syn["function"]["color"]))
    lines.append(_ps_attr("PHP_HEREDOC_CONTENT", fg=syn["stringSpecial"]["color"]))
    lines.append(_ps_attr("PHP_HEREDOC_ID", effect_type="1"))
    lines.append(_ps_attr("PHP_IDENTIFIER", fg=syn["variableSpecial"]["color"], effect_type="1"))
    lines.append(_ps_attr("PHP_INSTANCE_FIELD", fg=syn["property"]["color"]))
    lines.append(_ps_attr("PHP_INSTANCE_METHOD", fg=syn["instanceMethod"]["color"]))
    lines.append(_ps_attr("PHP_INTERFACE", fg=syn["interface"]["color"]))
    lines.append(_ps_attr("PHP_KEYWORD", fg=syn["keyword"]["color"], font_type="2"))
    lines.append(_ps_attr("PHP_MARKUP_ID", fg="#6296ff", font_type="2"))
    lines.append(_ps_attr("PHP_NUMBER", fg=syn["number"]["color"]))
    lines.append(_ps_attr("PHP_OPERATION_SIGN", fg=syn["operator"]["color"], font_type="1"))
    lines.append(_ps_attr("PHP_PARAMETER", fg="#717171"))
    lines.append(_ps_attr("PHP_PREDEFINED SYMBOL", fg="#7bc2e6"))
    lines.append(_ps_attr("PHP_SCRIPTING_BACKGROUND", fg=p["editor"]["foreground"], bg=p["editor"]["background"]))
    lines.append(_ps_attr("PHP_STATIC_METHOD", fg="#717171"))
    lines.append(_ps_attr("PHP_STRING", fg=syn["string"]["color"]))
    lines.append(_ps_attr("PHP_TAG", fg=syn["phpTag"]["color"]))
    lines.append(_ps_attr("PHP_VAR", fg=syn["variable"]["color"]))
    lines.append(_ps_attr("PHP_THIS_VAR", fg=syn["variableSpecial"]["color"], font_type="2"))
    lines.append(_ps_attr("PHP_VAR_VAR", fg=syn["variableSpecial"]["color"]))
    lines.append(_ps_attr("PHP_FUNCTION_CALL", fg=syn["function"]["color"]))
    lines.append(_ps_attr("PHP_NAMED_ARGUMENT", fg="#adb6bd", font_type="2"))
    lines.append(_ps_attr("PHP_ATTRIBUTE", fg=syn["interface"]["color"]))
    lines.append(_ps_attr("PHP_ENUM", fg=syn["interface"]["color"]))
    lines.append(_ps_attr("PHP_ENUM_CASE", fg=syn["constant"]["color"]))
    lines.append(_ps_attr("PHP_READONLY", fg=syn["keyword"]["color"], font_type="2"))
    lines.append(_ps_attr("RAINBOW_COLOR0", fg=rb["color0"]))
    lines.append(_ps_attr("RAINBOW_COLOR1", fg=rb["color1"]))
    lines.append(_ps_attr("RAINBOW_COLOR2", fg=rb["color2"]))
    lines.append(_ps_attr("RAINBOW_COLOR3", fg=rb["color3"]))
    lines.append(_ps_attr("RAINBOW_COLOR4", fg=rb["color4"]))
    lines.append(_ps_attr("SASS_IDENTIFIER", fg=sass["identifier"]))
    lines.append(_ps_attr("SASS_VARIABLE", fg=sass["variable"]))
    lines.append(_ps_attr("TEXT", fg=p["editor"]["foreground"], bg=p["editor"]["background"]))
    lines.append(_ps_attr("TEXT_SEARCH_RESULT_ATTRIBUTES", bg="#020100", error_stripe="#62c95c"))
    lines.append(_ps_attr("TODO_DEFAULT_ATTRIBUTES", fg=ui["todo"], font_type="3", error_stripe="#5388ff"))
    lines.append(_ps_attr("TWIG_KEYWORD", fg="#5a83db"))
    lines.append(_ps_attr("TYPO", effect_color="#80c08e", effect_type="4"))
    lines.append(_ps_attr("WARNING_ATTRIBUTES", effect_type="1"))
    lines.append(_ps_attr("WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES", bg="#020202", error_stripe="#c0a3c0"))
    lines.append(_ps_attr("XML_ATTRIBUTE_NAME", fg=syn["attribute"]["color"]))
    lines.append(_ps_attr("XML_ATTRIBUTE_VALUE", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("XML_NS_PREFIX", fg=syn["attribute"]["color"]))
    lines.append(_ps_attr_empty("XML_PROLOGUE"))
    lines.append(_ps_attr_empty("XML_TAG"))
    lines.append(_ps_attr("XML_TAG_NAME", fg=syn["tag"]["color"]))
    lines.append(_ps_attr("YAML_COMMENT", fg=syn["comment"]["color"]))
    lines.append(_ps_attr("YAML_SCALAR_DSTRING", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("YAML_SCALAR_KEY", fg=syn["tag"]["color"]))
    lines.append(_ps_attr_empty("YAML_SCALAR_LIST"))
    lines.append(_ps_attr("YAML_SCALAR_STRING", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("YAML_SCALAR_VALUE", font_type="1"))
    lines.append(_ps_attr("YAML_SIGN", fg=syn["attributeValue"]["color"]))
    lines.append(_ps_attr("YAML_TEXT", fg="#7bc2e6"))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    palette = load_palette()
    print("Generating themes from palette.json...")
    generate_ghostty(palette)
    generate_zed(palette)
    generate_phpstorm(palette)
    print("Done!")


if __name__ == "__main__":
    main()
