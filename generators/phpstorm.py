"""PHPStorm theme generator."""

import os

from .helpers import ROOT, phpstorm_hex, write_file


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
