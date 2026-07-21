#!/usr/bin/env python3
"""Structural Markdown -> Typst converter (R3 PDF pipeline).

Parses Markdown with markdown-it-py (CommonMark + tables) into a token
stream and emits Typst markup. STRICT: any token type without an explicit
handler raises ConversionError — content is never silently dropped
(the R2 pipeline's silent line-skip defect is structurally impossible here).
"""
import os
import re
import sys

from markdown_it import MarkdownIt

# sibling import works regardless of caller (build_pdfs, validators, direct run)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from latex_to_typst_math import translate_inline, translate_display, MathConvertError


class ConversionError(Exception):
    pass


# R7B math pipeline (Decision 0023): canonical source carries mathematics in
# GitHub-compatible LaTeX ($...$, $$...$$, ```math fences). markdown-it-py does
# not tokenize `$`, so `$...$`/`$$...$$` are PROTECTED into placeholders before
# parsing and expanded to Typst math in the text renderer; ```math fences are
# handled as a block token. Backtick code is unchanged: identifiers/paths stay
# monospace `#raw`. See docs/project-closure/r7b/R7B-PDF-MATH-BASELINE.md.
_MATH = []  # per-convert store of (kind, latex); reset at the top of convert()
_PH_OPEN, _PH_CLOSE = "", ""
_PH_RE = re.compile(_PH_OPEN + r"(\d+)" + _PH_CLOSE)
# One ordered scanner: code regions (fenced blocks, then inline `code`) are
# passed through UNCHANGED so a literal `$...$` written to DESCRIBE the syntax is
# never protected (R7C fix for audit B3 — the gallery prose leaked placeholders).
# Only $$...$$ / $...$ OUTSIDE code become math placeholders.
_PROTECT_RE = re.compile(
    r"(?P<fence>```.*?```)"          # fenced code block (incl. ```math; the fence
    r"|(?P<code>`[^`]*`)"            #   token handler deals with those separately)
    r"|(?P<disp>\$\$.+?\$\$)"        # display math
    r"|(?P<inl>\$[^\$\n]+?\$)",      # inline math
    re.S)


def _protect_math(md_text):
    """Replace $$...$$ and $...$ (only outside code) with placeholder sentinels
    markdown-it passes through verbatim; record the LaTeX bodies in _MATH."""
    def sub(m):
        if m.lastgroup in ("fence", "code"):
            return m.group(0)  # code passes through unchanged
        kind = "display" if m.lastgroup == "disp" else "inline"
        body = m.group(0)[2:-2] if kind == "display" else m.group(0)[1:-1]
        _MATH.append((kind, body))
        return _PH_OPEN + str(len(_MATH) - 1) + _PH_CLOSE
    return _PROTECT_RE.sub(sub, md_text)


def _expand_math(text):
    """Expand math placeholders inside a text token; escape the rest as usual."""
    out, last = [], 0
    for m in _PH_RE.finditer(text):
        out.append(esc(text[last:m.start()]))
        kind, latex = _MATH[int(m.group(1))]
        try:
            if kind == "display":
                out.append("$ " + translate_display(latex) + " $")
            else:
                out.append("$" + translate_inline(latex) + "$")
        except MathConvertError as e:
            raise ConversionError("math translation failed for %r: %s" % (latex, e))
        last = m.end()
    out.append(esc(text[last:]))
    return "".join(out)


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
            out.append(_expand_math(t.content))
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
            # R6: pure comments (reference-key markers) are metadata, not content
            if re.fullmatch(r"<!--.*?-->", t.content, re.S):
                continue
            raise ConversionError("raw inline HTML not supported: %r" % t.content)
        else:
            raise ConversionError("unhandled inline token: %s" % t.type)
    return "".join(out)


def _typst_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def convert(md_text):
    global _MATH
    _MATH = []
    md_text = _protect_math(md_text)
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
            info = (getattr(t, "info", "") or "").strip()
            if info == "math":
                try:
                    out.append("\n$ " + translate_display(t.content.rstrip("\n")) + " $\n")
                except MathConvertError as e:
                    raise ConversionError("math fence translation failed: %s" % e)
            else:
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
            # R6: a PURE HTML comment is machine metadata (e.g. the companion
            # reference keys <!-- ref:KEY -->), not content — dropping it loses
            # nothing a reader sees. Anything else stays a hard error: the
            # strict no-silent-skip contract applies to CONTENT only.
            if re.fullmatch(r"\s*(<!--.*?-->\s*)+", t.content, re.S):
                i += 1
                continue
            raise ConversionError("raw HTML block not supported: %r" % t.content[:60])
        raise ConversionError("unhandled block token: %s" % ty)
    return "".join(out)
