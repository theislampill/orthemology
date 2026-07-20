#!/usr/bin/env python3
"""Structural Markdown -> Typst converter (R3 PDF pipeline).

Parses Markdown with markdown-it-py (CommonMark + tables) into a token
stream and emits Typst markup. STRICT: any token type without an explicit
handler raises ConversionError — content is never silently dropped
(the R2 pipeline's silent line-skip defect is structurally impossible here).
"""
from markdown_it import MarkdownIt


class ConversionError(Exception):
    pass


# characters with markup meaning in Typst text context
_ESC = "\\#$*_`@<>[]~"


def esc(text):
    out = []
    for ch in text:
        if ch in _ESC:
            out.append("\\" + ch)
        else:
            out.append(ch)
    return "".join(out)


def _inline(tokens):
    """Render an inline token's children."""
    out = []
    for t in tokens:
        if t.type == "text":
            out.append(esc(t.content))
        elif t.type == "code_inline":
            out.append("#raw(" + _typst_str(t.content) + ")")
        elif t.type == "strong_open":
            out.append("#strong[")
        elif t.type == "strong_close":
            out.append("]")
        elif t.type == "em_open":
            out.append("#emph[")
        elif t.type == "em_close":
            out.append("]")
        elif t.type == "link_open":
            href = t.attrGet("href") or ""
            if href.startswith("http://") or href.startswith("https://"):
                out.append("#link(" + _typst_str(href) + ")[")
            else:
                # internal repository link: no in-PDF target exists; the link
                # TEXT is rendered emphasized (in this corpus the text is the
                # path or the document title) — a documented rendering rule,
                # recorded in R3-PDF-VISUAL-QA.md, not a silent skip
                out.append("#emph[")
        elif t.type == "link_close":
            out.append("]")
        elif t.type == "softbreak":
            out.append(" ")
        elif t.type == "hardbreak":
            out.append(" \\\n")
        elif t.type == "s_open":
            out.append("#strike[")
        elif t.type == "s_close":
            out.append("]")
        elif t.type == "image":
            raise ConversionError("images are not supported in this corpus")
        elif t.type == "html_inline":
            raise ConversionError("raw inline HTML not supported: %r" % t.content)
        else:
            raise ConversionError("unhandled inline token: %s" % t.type)
    return "".join(out)


def _typst_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def convert(md_text):
    md = MarkdownIt("commonmark").enable("table").enable("strikethrough")
    tokens = md.parse(md_text)
    out = []
    i = 0
    list_stack = []
    table = None

    while i < len(tokens):
        t = tokens[i]
        ty = t.type
        if ty == "heading_open":
            level = int(t.tag[1])
            inline = tokens[i + 1]
            out.append("\n" + "=" * level + " " + _inline(inline.children) + "\n")
            i += 3
            continue
        if ty == "paragraph_open":
            inline = tokens[i + 1]
            body = _inline(inline.children)
            if list_stack:
                out.append(body + "\n")
            else:
                out.append("\n" + body + "\n")
            i += 3
            continue
        if ty == "blockquote_open":
            out.append("\n#quote(block: true)[\n")
            i += 1
            continue
        if ty == "blockquote_close":
            out.append("]\n")
            i += 1
            continue
        if ty in ("bullet_list_open", "ordered_list_open"):
            list_stack.append("-" if ty == "bullet_list_open" else "+")
            i += 1
            continue
        if ty in ("bullet_list_close", "ordered_list_close"):
            list_stack.pop()
            out.append("\n" if not list_stack else "")
            i += 1
            continue
        if ty == "list_item_open":
            out.append("\n" + "  " * (len(list_stack) - 1) + list_stack[-1] + " ")
            i += 1
            continue
        if ty == "list_item_close":
            i += 1
            continue
        if ty == "fence" or ty == "code_block":
            out.append("\n#raw(block: true, " + _typst_str(t.content.rstrip("\n")) + ")\n")
            i += 1
            continue
        if ty == "hr":
            out.append("\n#line(length: 100%, stroke: 0.5pt + gray)\n")
            i += 1
            continue
        if ty == "table_open":
            table = {"rows": [], "header": []}
            i += 1
            continue
        if ty in ("thead_open", "tbody_open", "tr_open"):
            if ty == "tr_open":
                table["current"] = []
            i += 1
            continue
        if ty in ("th_open", "td_open"):
            inline = tokens[i + 1]
            cell = _inline(inline.children) if inline.type == "inline" else ""
            table["current"].append((ty == "th_open", cell))
            i += 3
            continue
        if ty == "tr_close":
            row = table.pop("current")
            if row and row[0][0]:
                table["header"] = [c for _, c in row]
            else:
                table["rows"].append([c for _, c in row])
            i += 1
            continue
        if ty in ("thead_close", "tbody_close"):
            i += 1
            continue
        if ty == "table_close":
            ncol = max([len(table["header"])] + [len(r) for r in table["rows"]] or [1])
            cells = []
            for c in table["header"]:
                cells.append("[#strong[" + c + "]]")
            for r in table["rows"]:
                r = r + [""] * (ncol - len(r))
                for c in r:
                    cells.append("[" + c + "]")
            out.append(
                "\n#block(breakable: true)[#table(columns: %d, inset: 4.5pt, "
                "stroke: 0.4pt + gray.darken(30%%), %s)]\n" % (ncol, ", ".join(cells)))
            table = None
            i += 1
            continue
        if ty == "html_block":
            raise ConversionError("raw HTML block not supported: %r" % t.content[:60])
        raise ConversionError("unhandled block token: %s" % ty)
    return "".join(out)
