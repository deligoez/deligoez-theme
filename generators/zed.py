"""Zed theme generator."""

import json
import os

from .helpers import ROOT, with_alpha, hex8, write_file


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
    style["background"] = hex8(GRAY_APP)
    style["text"] = hex8(fg)
    style["text.muted"] = hex8(GRAY_MUTED)
    style["text.placeholder"] = hex8(GRAY_PLACEHOLDER)
    style["text.disabled"] = hex8(GRAY_DISABLED)
    style["text.accent"] = hex8(syn["function"]["color"])
    style["border"] = hex8(GRAY_BORDER)
    style["border.variant"] = hex8(GRAY_BORDER_V)
    style["border.focused"] = hex8(syn["function"]["color"])
    style["border.selected"] = hex8(sel)
    style["border.transparent"] = "#00000000"
    style["border.disabled"] = hex8(GRAY_BORDER_D)

    # Surfaces
    style["elevated_surface.background"] = hex8(GRAY_SURFACE)
    style["surface.background"] = hex8(GRAY_SURFACE)
    style["panel.background"] = hex8(GRAY_SURFACE)
    style["panel.focused_border"] = None
    style["pane.focused_border"] = None

    # Elements
    style["element.background"] = hex8(GRAY_SURFACE)
    style["element.hover"] = hex8(GRAY_HOVER)
    style["element.active"] = hex8(sel)
    style["element.selected"] = hex8(sel)
    style["element.disabled"] = hex8(GRAY_SURFACE)
    style["ghost_element.background"] = "#00000000"
    style["ghost_element.hover"] = hex8(GRAY_HOVER)
    style["ghost_element.active"] = hex8(sel)
    style["ghost_element.selected"] = hex8(sel)
    style["ghost_element.disabled"] = hex8(GRAY_SURFACE)

    style["drop_target.background"] = with_alpha(sel, "80")

    # Icons
    style["icon"] = hex8(fg)
    style["icon.muted"] = hex8(GRAY_MUTED)
    style["icon.disabled"] = hex8(GRAY_DISABLED)
    style["icon.placeholder"] = hex8(GRAY_MUTED)
    style["icon.accent"] = hex8(syn["function"]["color"])

    # Tab bar
    style["tab_bar.background"] = hex8(GRAY_SURFACE)
    style["tab.active_background"] = hex8(bg)
    style["tab.inactive_background"] = hex8(GRAY_SURFACE)

    # Status/title bar
    style["status_bar.background"] = hex8(GRAY_APP)
    style["title_bar.background"] = hex8(GRAY_APP)
    style["title_bar.inactive_background"] = hex8(GRAY_SURFACE)
    style["toolbar.background"] = hex8(bg)

    # Scrollbar
    style["scrollbar.thumb.background"] = with_alpha(fg, "1a")
    style["scrollbar.thumb.hover_background"] = with_alpha(fg, "33")
    style["scrollbar.thumb.border"] = "#00000000"
    style["scrollbar.track.background"] = "#00000000"
    style["scrollbar.track.border"] = hex8(GRAY_SURFACE)

    # Editor
    style["editor.background"] = hex8(bg)
    style["editor.foreground"] = hex8(fg)
    style["editor.gutter.background"] = hex8(bg)
    style["editor.subheader.background"] = hex8(GRAY_SURFACE)
    style["editor.active_line.background"] = "#00000000"
    style["editor.highlighted_line.background"] = hex8(GRAY_SURFACE)
    style["editor.line_number"] = hex8(ed["lineNumber"])
    style["editor.active_line_number"] = hex8(fg)
    style["editor.invisible"] = hex8(GRAY_BORDER)
    style["editor.wrap_guide"] = hex8(GRAY_HOVER)
    style["editor.active_wrap_guide"] = hex8(GRAY_BORDER)
    style["editor.indent_guide"] = hex8(GRAY_HOVER)
    style["editor.indent_guide_active"] = hex8(GRAY_INDENT_A)
    style["editor.document_highlight.read_background"] = hex8(p["ui"]["identifierUnderCaret"])
    style["editor.document_highlight.write_background"] = with_alpha(sel, "66")

    style["search.match_background"] = with_alpha(p["ui"]["searchResult"], "55")

    # Links
    style["link_text.hover"] = hex8(syn["link"]["color"])

    # Terminal
    style["terminal.background"] = hex8(bg)
    style["terminal.foreground"] = hex8(fg)
    style["terminal.bright_foreground"] = hex8(t["black"] if t["black"] != bg else "#000000")
    style["terminal.dim_foreground"] = hex8(GRAY_PLACEHOLDER)

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
        style[f"terminal.ansi.{name}"] = hex8(color)
        style[f"terminal.ansi.bright_{name}"] = hex8(_bright_map[name])
        style[f"terminal.ansi.dim_{name}"] = hex8(_dim_map_light[name])

    # Status colors
    style["error"] = hex8(st["error"])
    style["error.background"] = hex8(p["ui"]["breakpoint"])
    style["error.border"] = with_alpha(st["error"], "33")
    style["warning"] = hex8(st["warning"])
    style["warning.background"] = "#fff3e0ff"
    style["warning.border"] = with_alpha(st["warning"], "33")
    style["success"] = hex8(st["success"])
    style["success.background"] = hex8(p["diff"]["inserted"])
    style["success.border"] = with_alpha(st["success"], "33")
    style["info"] = hex8(st["info"])
    style["info.background"] = hex8(sel)
    style["info.border"] = with_alpha(st["info"], "33")
    style["hint"] = hex8(st["hint"])
    style["hint.background"] = "#f0ebf5ff"
    style["hint.border"] = with_alpha(st["hint"], "33")

    # Conflict / created / deleted / modified / renamed
    style["conflict"] = hex8(st["warning"])
    style["conflict.background"] = "#fff3e0ff"
    style["conflict.border"] = with_alpha(st["warning"], "33")
    style["created"] = hex8(st["success"])
    style["created.background"] = hex8(p["diff"]["inserted"])
    style["created.border"] = with_alpha(st["success"], "33")
    style["deleted"] = hex8(st["error"])
    style["deleted.background"] = "#ffdadaff"
    style["deleted.border"] = with_alpha(st["error"], "33")
    style["modified"] = hex8(st["info"])
    style["modified.background"] = hex8(p["diff"]["modified"])
    style["modified.border"] = with_alpha(st["info"], "33")
    style["renamed"] = hex8(st["hint"])
    style["renamed.background"] = "#f0ebf5ff"
    style["renamed.border"] = with_alpha(st["hint"], "33")

    # Hidden / ignored / unreachable / predictive
    style["hidden"] = hex8(GRAY_PLACEHOLDER)
    style["hidden.background"] = hex8(GRAY_APP)
    style["hidden.border"] = hex8(GRAY_BORDER_D)
    style["ignored"] = hex8(GRAY_PLACEHOLDER)
    style["ignored.background"] = hex8(GRAY_APP)
    style["ignored.border"] = hex8(GRAY_BORDER_D)
    style["unreachable"] = hex8(GRAY_MUTED)
    style["unreachable.background"] = hex8(GRAY_APP)
    style["unreachable.border"] = hex8(GRAY_BORDER_D)
    style["predictive"] = hex8(ed["lineNumber"])
    style["predictive.background"] = hex8(GRAY_APP)
    style["predictive.border"] = hex8(GRAY_BORDER_D)

    # Players
    player_colors = [
        syn["keyword"]["color"], syn["function"]["color"],
        syn["interface"]["color"], syn["tag"]["color"],
        syn["constant"]["color"], syn["operator"]["color"],
        st["warning"], syn["class"]["color"],
    ]
    players = []
    for i, c in enumerate(player_colors):
        entry = {"cursor": hex8(c), "background": hex8(c)}
        if i == 0:
            entry["selection"] = hex8(sel)
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
    s["attribute"] = _zed_syntax_entry(hex8(syn["interface"]["color"]))
    s["boolean"] = _zed_syntax_entry(hex8(syn["keyword"]["color"]), font_style="italic")
    s["comment"] = _zed_syntax_entry(hex8(syn["comment"]["color"]), font_style="italic")
    s["comment.doc"] = _zed_syntax_entry(hex8(syn["commentDoc"]["color"]), font_style="italic")
    s["constant"] = _zed_syntax_entry(hex8(syn["constant"]["color"]))
    s["constructor"] = _zed_syntax_entry(hex8(syn["class"]["color"]))
    s["embedded"] = _zed_syntax_entry(hex8(fg))
    s["emphasis"] = _zed_syntax_entry(hex8(fg), font_style="italic")
    s["emphasis.strong"] = _zed_syntax_entry(hex8(fg), font_weight=700)
    s["enum"] = _zed_syntax_entry(hex8(syn["interface"]["color"]))
    s["function"] = _zed_syntax_entry(hex8(syn["function"]["color"]))
    s["hint"] = _zed_syntax_entry(hex8(syn["commentDocTag"]["color"]))
    s["keyword"] = _zed_syntax_entry(hex8(syn["keyword"]["color"]), font_style="italic")
    s["label"] = _zed_syntax_entry(hex8(syn["commentDocTag"]["color"]))
    s["link_text"] = _zed_syntax_entry(hex8(syn["link"]["color"]), font_style="italic")
    s["link_uri"] = _zed_syntax_entry(hex8(syn["link"]["color"]))
    s["namespace"] = _zed_syntax_entry(hex8(syn["class"]["color"]))
    s["number"] = _zed_syntax_entry(hex8(syn["number"]["color"]))
    s["operator"] = _zed_syntax_entry(hex8(syn["operator"]["color"]), font_weight=700)
    s["predictive"] = _zed_syntax_entry(hex8("#a7a7a7"), font_style="italic")
    s["preproc"] = _zed_syntax_entry(hex8(syn["phpTag"]["color"]))
    s["primary"] = _zed_syntax_entry(hex8(fg))
    s["property"] = _zed_syntax_entry(hex8(syn["class"]["color"]))
    s["punctuation"] = _zed_syntax_entry(hex8(fg))
    s["punctuation.bracket"] = _zed_syntax_entry(hex8(fg))
    s["punctuation.delimiter"] = _zed_syntax_entry(hex8(fg))
    s["punctuation.list_marker"] = _zed_syntax_entry(hex8(syn["operator"]["color"]))
    s["punctuation.markup"] = _zed_syntax_entry(hex8(syn["operator"]["color"]))
    s["punctuation.special"] = _zed_syntax_entry(hex8(syn["phpTag"]["color"]))
    s["selector"] = _zed_syntax_entry(hex8(syn["tag"]["color"]))
    s["selector.pseudo"] = _zed_syntax_entry(hex8(syn["interface"]["color"]))
    s["string"] = _zed_syntax_entry(hex8(syn["string"]["color"]))
    s["string.escape"] = _zed_syntax_entry(hex8(syn["attributeValue"]["color"]))
    s["string.regex"] = _zed_syntax_entry(hex8(syn["regex"]["color"]))
    s["string.special"] = _zed_syntax_entry(hex8(syn["stringSpecial"]["color"]))
    s["string.special.symbol"] = _zed_syntax_entry(hex8(syn["symbol"]["color"]))
    s["tag"] = _zed_syntax_entry(hex8(syn["tag"]["color"]))
    s["text.literal"] = _zed_syntax_entry(hex8(syn["string"]["color"]))
    s["title"] = _zed_syntax_entry(hex8(syn["class"]["color"]), font_weight=700)
    s["type"] = _zed_syntax_entry(hex8(syn["class"]["color"]))
    s["variable"] = _zed_syntax_entry(hex8(fg))
    s["variable.special"] = _zed_syntax_entry(hex8(syn["variableSpecial"]["color"]))
    s["variant"] = _zed_syntax_entry(hex8(syn["interface"]["color"]))
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
    style["background"] = hex8(app_bg)
    style["text"] = hex8(fg)
    style["text.muted"] = "#9898a0ff"
    style["text.placeholder"] = "#6b6b73ff"
    style["text.disabled"] = "#55555dff"
    style["text.accent"] = hex8(syn["function"]["color"])
    style["border"] = hex8(border_main)
    style["border.variant"] = hex8(border_var)
    style["border.focused"] = hex8(syn["function"]["color"])
    style["border.selected"] = hex8(active)
    style["border.transparent"] = "#00000000"
    style["border.disabled"] = hex8(border_var)

    # Surfaces
    style["elevated_surface.background"] = hex8(elevated)
    style["surface.background"] = hex8(surface)
    style["panel.background"] = hex8(surface)
    style["panel.focused_border"] = None
    style["pane.focused_border"] = None

    # Elements
    style["element.background"] = hex8(surface)
    style["element.hover"] = hex8(element_hover)
    style["element.active"] = hex8(active)
    style["element.selected"] = hex8(active)
    style["element.disabled"] = hex8(surface)
    style["ghost_element.background"] = "#00000000"
    style["ghost_element.hover"] = hex8(element_hover)
    style["ghost_element.active"] = hex8(active)
    style["ghost_element.selected"] = hex8(active)
    style["ghost_element.disabled"] = hex8(surface)

    style["drop_target.background"] = with_alpha(syn["function"]["color"], "40")

    # Icons
    style["icon"] = hex8(fg)
    style["icon.muted"] = "#9898a0ff"
    style["icon.disabled"] = "#55555dff"
    style["icon.placeholder"] = "#9898a0ff"
    style["icon.accent"] = hex8(syn["function"]["color"])

    # Tab bar
    style["tab_bar.background"] = hex8(surface)
    style["tab.active_background"] = hex8(bg)
    style["tab.inactive_background"] = hex8(surface)

    # Status/title bar
    style["status_bar.background"] = hex8(app_bg)
    style["title_bar.background"] = hex8(app_bg)
    style["title_bar.inactive_background"] = hex8(surface)
    style["toolbar.background"] = hex8(bg)

    # Scrollbar
    style["scrollbar.thumb.background"] = with_alpha(fg, "1a")
    style["scrollbar.thumb.hover_background"] = with_alpha(fg, "33")
    style["scrollbar.thumb.border"] = "#00000000"
    style["scrollbar.track.background"] = "#00000000"
    style["scrollbar.track.border"] = hex8(surface)

    # Editor
    style["editor.background"] = hex8(bg)
    style["editor.foreground"] = hex8(fg)
    style["editor.gutter.background"] = hex8(bg)
    style["editor.subheader.background"] = hex8(surface)
    style["editor.active_line.background"] = "#00000000"
    style["editor.highlighted_line.background"] = hex8(surface)
    style["editor.line_number"] = hex8(ed["lineNumber"])
    style["editor.active_line_number"] = hex8(fg)
    style["editor.invisible"] = hex8(invisible)
    style["editor.wrap_guide"] = hex8(border_var)
    style["editor.active_wrap_guide"] = hex8(border_main)
    style["editor.indent_guide"] = hex8(border_var)
    style["editor.indent_guide_active"] = hex8(indent_active)
    style["editor.document_highlight.read_background"] = hex8(p["ui"]["identifierUnderCaret"])
    style["editor.document_highlight.write_background"] = with_alpha(syn["function"]["color"], "26")

    style["search.match_background"] = p["ui"]["searchResult"] + ("" if len(p["ui"]["searchResult"]) > 7 else "")

    # Links
    style["link_text.hover"] = hex8(syn["link"]["color"])

    # Terminal
    style["terminal.background"] = hex8(bg)
    style["terminal.foreground"] = hex8(fg)
    style["terminal.bright_foreground"] = hex8(t["brightWhite"])
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
        style[f"terminal.ansi.{name}"] = hex8(color)
        style[f"terminal.ansi.bright_{name}"] = hex8(_bright_map[name])
        style[f"terminal.ansi.dim_{name}"] = hex8(_dim_map_dark[name])

    # Status colors
    style["error"] = hex8(st["error"])
    style["error.background"] = "#320001ff"
    style["error.border"] = with_alpha(st["error"], "33")
    style["warning"] = hex8(st["warning"])
    style["warning.background"] = "#290d00ff"
    style["warning.border"] = with_alpha(st["warning"], "33")
    style["success"] = hex8(st["success"])
    style["success.background"] = "#071b06ff"
    style["success.border"] = with_alpha(st["success"], "33")
    style["info"] = hex8(st["info"])
    style["info.background"] = "#001928ff"
    style["info.border"] = with_alpha(st["info"], "33")
    style["hint"] = hex8(st["hint"])
    style["hint.background"] = "#1a1127ff"
    style["hint.border"] = with_alpha(st["hint"], "33")

    style["conflict"] = hex8(st["warning"])
    style["conflict.background"] = "#290d00ff"
    style["conflict.border"] = with_alpha(st["warning"], "33")
    style["created"] = hex8(st["success"])
    style["created.background"] = "#071b06ff"
    style["created.border"] = with_alpha(st["success"], "33")
    style["deleted"] = hex8(st["error"])
    style["deleted.background"] = "#320001ff"
    style["deleted.border"] = with_alpha(st["error"], "33")
    style["modified"] = hex8(st["info"])
    style["modified.background"] = "#001928ff"
    style["modified.border"] = with_alpha(st["info"], "33")
    style["renamed"] = hex8(st["hint"])
    style["renamed.background"] = "#1a1127ff"
    style["renamed.border"] = with_alpha(st["hint"], "33")

    style["hidden"] = "#6b6b73ff"
    style["hidden.background"] = hex8(app_bg)
    style["hidden.border"] = hex8(border_var)
    style["ignored"] = "#6b6b73ff"
    style["ignored.background"] = hex8(app_bg)
    style["ignored.border"] = hex8(border_main)
    style["unreachable"] = "#9898a0ff"
    style["unreachable.background"] = hex8(app_bg)
    style["unreachable.border"] = hex8(border_main)
    style["predictive"] = "#6b6b73ff"
    style["predictive.background"] = hex8(app_bg)
    style["predictive.border"] = hex8(border_var)

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
            "cursor": hex8(c),
            "background": hex8(c),
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
    s["attribute"] = _zed_syntax_entry(hex8(syn["interface"]["color"]))
    s["boolean"] = _zed_syntax_entry(hex8(syn["keyword"]["color"]), font_style="italic")
    s["comment"] = _zed_syntax_entry(hex8(syn["comment"]["color"]), font_style="italic")
    s["comment.doc"] = _zed_syntax_entry(hex8(syn["commentDoc"]["color"]), font_style="italic")
    s["constant"] = _zed_syntax_entry(hex8(syn["constant"]["color"]))
    s["constructor"] = _zed_syntax_entry(hex8(syn["class"]["color"]))
    s["embedded"] = _zed_syntax_entry(hex8(fg))
    s["emphasis"] = _zed_syntax_entry(hex8(fg), font_style="italic")
    s["emphasis.strong"] = _zed_syntax_entry(hex8(fg), font_weight=700)
    s["enum"] = _zed_syntax_entry(hex8(syn["interface"]["color"]))
    s["function"] = _zed_syntax_entry(hex8(syn["function"]["color"]))
    s["hint"] = _zed_syntax_entry("#adb6bdff")
    s["keyword"] = _zed_syntax_entry(hex8(syn["keyword"]["color"]), font_style="italic")
    s["label"] = _zed_syntax_entry("#adb6bdff")
    s["link_text"] = _zed_syntax_entry(hex8(syn["link"]["color"]), font_style="italic")
    s["link_uri"] = _zed_syntax_entry(hex8(syn["link"]["color"]))
    s["namespace"] = _zed_syntax_entry(hex8(syn["class"]["color"]))
    s["number"] = _zed_syntax_entry(hex8(syn["number"]["color"]))
    s["operator"] = _zed_syntax_entry(hex8(syn["operator"]["color"]), font_weight=700)
    s["predictive"] = _zed_syntax_entry("#6b6b73ff", font_style="italic")
    s["preproc"] = _zed_syntax_entry(hex8(syn["phpTag"]["color"]))
    s["primary"] = _zed_syntax_entry(hex8(fg))
    s["property"] = _zed_syntax_entry(hex8(syn["class"]["color"]))
    s["punctuation"] = _zed_syntax_entry(hex8(fg))
    s["punctuation.bracket"] = _zed_syntax_entry(hex8(fg))
    s["punctuation.delimiter"] = _zed_syntax_entry(hex8(fg))
    s["punctuation.list_marker"] = _zed_syntax_entry(hex8(syn["operator"]["color"]))
    s["punctuation.markup"] = _zed_syntax_entry(hex8(syn["operator"]["color"]))
    s["punctuation.special"] = _zed_syntax_entry(hex8(syn["phpTag"]["color"]))
    s["selector"] = _zed_syntax_entry(hex8(syn["tag"]["color"]))
    s["selector.pseudo"] = _zed_syntax_entry(hex8(syn["interface"]["color"]))
    s["string"] = _zed_syntax_entry(hex8(syn["string"]["color"]))
    s["string.escape"] = _zed_syntax_entry(hex8(syn["attributeValue"]["color"]))
    s["string.regex"] = _zed_syntax_entry(hex8(syn["regex"]["color"]))
    s["string.special"] = _zed_syntax_entry(hex8(syn["stringSpecial"]["color"]))
    s["string.special.symbol"] = _zed_syntax_entry(hex8(syn["symbol"]["color"]))
    s["tag"] = _zed_syntax_entry(hex8(syn["tag"]["color"]))
    s["text.literal"] = _zed_syntax_entry(hex8(syn["string"]["color"]))
    s["title"] = _zed_syntax_entry(hex8(syn["class"]["color"]), font_weight=700)
    s["type"] = _zed_syntax_entry(hex8(syn["class"]["color"]))
    s["variable"] = _zed_syntax_entry(hex8(fg))
    s["variable.special"] = _zed_syntax_entry(hex8(syn["variableSpecial"]["color"]))
    s["variant"] = _zed_syntax_entry(hex8(syn["interface"]["color"]))
    return s
