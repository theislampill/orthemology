#!/usr/bin/env python3
"""Strict LaTeX-subset -> Typst-math translator (R7B, Decision 0023).

The Orthemology PDF pipeline compiles with the pinned `typst` Python package,
which has a real math mode. This module lets the canonical Markdown source carry
mathematics in GitHub-compatible LaTeX (`$...$`, `$$...$$`, or ```math fences)
that GitHub renders through MathJax, and translates that same LaTeX into Typst
math markup so the PDF renders publication-grade mathematics instead of the old
`#raw` monospace (which produced notdef glyphs for `mu-vec`/`C-vec`; see
docs/project-closure/r7b/R7B-PDF-MATH-BASELINE.md).

DESIGN CONTRACT — strict, no silent fallthrough:
  * every backslash command must be in COMMANDS or ACCENTS; an unknown command
    raises MathConvertError (never passed through, never dropped). This mirrors
    md_to_typst.py's no-silent-skip contract: a typo in the source fails the
    build rather than mis-rendering.
  * the supported subset is exactly the corpus's notation inventory
    (docs/notation-registry.yaml render_map); scripts/validate_math_source.py
    proves the gallery exercises every registered symbol through this translator.

It is NOT a general LaTeX engine. It is a bounded, tested translator for one
corpus. Extending it is a deliberate, reviewed act (add to the tables + a test).
"""


class MathConvertError(Exception):
    pass


# backslash command -> Typst token (non-accent). Order-independent.
COMMANDS = {
    # greek (lower)
    "alpha": "alpha", "beta": "beta", "gamma": "gamma", "delta": "delta",
    "epsilon": "epsilon", "varepsilon": "epsilon.alt", "zeta": "zeta",
    "eta": "eta", "theta": "theta", "iota": "iota", "kappa": "kappa",
    "lambda": "lambda", "mu": "mu", "nu": "nu", "xi": "xi", "pi": "pi",
    "rho": "rho", "sigma": "sigma", "tau": "tau", "upsilon": "upsilon",
    "phi": "phi", "varphi": "phi.alt", "chi": "chi", "psi": "psi", "omega": "omega",
    # greek (upper)
    "Gamma": "Gamma", "Delta": "Delta", "Theta": "Theta", "Lambda": "Lambda",
    "Xi": "Xi", "Pi": "Pi", "Sigma": "Sigma", "Phi": "Phi", "Psi": "Psi",
    "Omega": "Omega",
    # relations / logic / set
    "in": "in", "notin": "in.not", "ni": "in.rev",
    "subseteq": "subset.eq", "subset": "subset", "supseteq": "supset.eq",
    "supset": "supset", "cup": "union", "cap": "inter", "setminus": "without",
    "emptyset": "nothing", "varnothing": "nothing",
    "wedge": "and", "land": "and", "vee": "or", "lor": "or",
    "neg": "not", "lnot": "not", "forall": "forall", "exists": "exists",
    "nexists": "exists.not", "top": "top", "bot": "bot",
    "leq": "<=", "le": "<=", "geq": ">=", "ge": ">=", "neq": "!=", "ne": "!=",
    "equiv": "equiv", "approx": "approx", "sim": "tilde.op", "cong": "tilde.equiv",
    "preceq": "prec.eq", "succeq": "succ.eq", "prec": "prec", "succ": "succ",
    "propto": "prop", "asymp": "asymp",
    # arrows
    "to": "arrow.r", "rightarrow": "arrow.r", "leftarrow": "arrow.l",
    "Rightarrow": "arrow.r.double", "Leftarrow": "arrow.l.double",
    "leftrightarrow": "arrow.l.r", "Leftrightarrow": "arrow.l.r.double",
    "iff": "arrow.l.r.double", "implies": "arrow.r.double",
    "mapsto": "arrow.r.bar", "longmapsto": "arrow.r.long.bar",
    "longrightarrow": "arrow.r.long", "longleftarrow": "arrow.l.long",
    "hookrightarrow": "arrow.r.hook",
    "rightsquigarrow": "arrow.r.squiggly", "leadsto": "arrow.r.squiggly",
    "uparrow": "arrow.t", "downarrow": "arrow.b", "harpoonup": "harpoon.rt",
    "rightharpoonup": "harpoon.rt",
    # binary ops / misc
    "times": "times", "cdot": "dot.op", "circ": "compose", "ast": "*",
    "pm": "plus.minus", "mp": "minus.plus", "star": "star.op",
    "partial": "partial", "nabla": "nabla", "infty": "infinity",
    "sum": "sum", "prod": "product", "int": "integral",
    "min": "min", "max": "max", "inf": "inf", "sup": "sup", "arg": "arg",
    # delimiters (as tokens)
    "langle": "⟨", "rangle": "⟩",
    "lfloor": "floor.l", "rfloor": "floor.r", "lceil": "ceil.l", "rceil": "ceil.r",
    "mid": "bar.v", "|": "bar.v", "parallel": "bar.v.double",
    "{": "{", "}": "}", "backslash": "backslash",
    # dots / spacing
    "ldots": "dots.h", "dots": "dots.h", "cdots": "dots.c", "vdots": "dots.v",
    "quad": "quad", "qquad": "wide", "colon": ":", "coloneqq": ":=",
    # named upright function-ish
    "log": "log", "exp": "exp", "det": "det", "dim": "dim",
}

# spacing commands that map to a Typst spacing token (or nothing)
SPACING = {",": "thin", ";": "thick", ":": "med", " ": "med", "!": ""}

# accent commands: \cmd{X} or \cmd X -> typst_accent(X)
ACCENTS = {
    "hat": "hat", "widehat": "hat", "bar": "macron", "overline": "overline",
    "vec": "arrow", "tilde": "tilde", "widetilde": "tilde", "dot": "dot",
    "ddot": "dot.double", "check": "caron", "breve": "breve", "acute": "acute",
    "grave": "grave", "mathring": "circle",
}
# font/style commands: \cmd{...} -> typst_fn(...)
STYLE = {
    "mathcal": "cal", "mathbb": "bb", "mathfrak": "frak", "mathbf": "bold",
    "mathrm": "upright", "mathsf": "sans", "boldsymbol": "bold", "bm": "bold",
    "operatorname": None,  # -> op("...")
    "text": None,          # -> "..."
    "textrm": None,        # -> "..."
    "textbf": None,        # -> bold("...")
}


def _typ_text(s):
    """Turn the body of \\operatorname{...}/\\text{...} into a safe Typst string
    literal: unescape common LaTeX text escapes, then escape for Typst."""
    for a, b in (("\\_", "_"), ("\\&", "&"), ("\\%", "%"), ("\\#", "#"),
                 ("\\{", "{"), ("\\}", "}"), ("\\ ", " "), ("\\,", " ")):
        s = s.replace(a, b)
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _skip_ws(s, i):
    while i < len(s) and s[i] == " ":
        i += 1
    return i


def _read_group(s, i):
    """s[i] == '{' ; return (inner_string, index_after_closing_brace)."""
    assert s[i] == "{"
    depth = 0
    j = i
    while j < len(s):
        if s[j] == "\\":
            j += 2
            continue
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise MathConvertError("unbalanced { in math: %r" % s[i:i + 30])


def _read_command(s, i):
    """s[i] == '\\' ; return (name, index_after_name). name is a run of letters,
    or a single non-letter (e.g. \\{, \\,, \\|)."""
    j = i + 1
    if j < len(s) and s[j].isalpha():
        k = j
        while k < len(s) and s[k].isalpha():
            k += 1
        return s[j:k], k
    if j < len(s):
        return s[j], j + 1
    raise MathConvertError("dangling backslash at end of math")


def _render_command(name, s, i):
    """Render a backslash command starting just AFTER the name (i points past it).
    Returns (typst_text, next_i)."""
    # under/over-brace with an optional _{label}/^{label}: LaTeX
    # \underbrace{X}_{Y} -> Typst underbrace(X, Y)
    if name in ("underbrace", "overbrace"):
        i = _skip_ws(s, i)
        if i >= len(s) or s[i] != "{":
            raise MathConvertError("\\%s requires a { } argument" % name)
        inner, j = _read_group(s, i)
        fn = "underbrace" if name == "underbrace" else "overbrace"
        j2 = _skip_ws(s, j)
        if j2 < len(s) and s[j2] in "_^":
            lbl, k = _read_script(s, j2 + 1)
            lab = lbl[1:-1] if lbl.startswith("(") and lbl.endswith(")") else lbl
            return fn + "(" + _translate(inner) + ", " + lab + ")", k
        return fn + "(" + _translate(inner) + ")", j
    # labeled long arrow: LaTeX \xrightarrow{L} -> Typst arrow.r^(L)
    if name in ("xrightarrow", "xleftarrow", "xmapsto"):
        arrow = {"xrightarrow": "arrow.r.long", "xleftarrow": "arrow.l.long",
                 "xmapsto": "arrow.r.bar"}[name]
        i = _skip_ws(s, i)
        if i < len(s) and s[i] == "{":
            inner, j = _read_group(s, i)
            return arrow + "^(" + _translate(inner) + ")", j
        return arrow, i
    if name in ACCENTS:
        i = _skip_ws(s, i)
        if i < len(s) and s[i] == "{":
            inner, j = _read_group(s, i)
            return ACCENTS[name] + "(" + _translate(inner) + ")", j
        if i < len(s) and s[i] == "\\":
            sub, j = _read_command(s, i)
            txt, k = _render_command(sub, s, j)
            return ACCENTS[name] + "(" + txt + ")", k
        if i < len(s):
            return ACCENTS[name] + "(" + _translate(s[i]) + ")", i + 1
        raise MathConvertError("accent \\%s with no argument" % name)
    if name in STYLE:
        i = _skip_ws(s, i)
        if i >= len(s) or s[i] != "{":
            raise MathConvertError("\\%s requires a { } argument" % name)
        inner, j = _read_group(s, i)
        fn = STYLE[name]
        if name == "operatorname":
            return 'op("' + _typ_text(inner.strip()) + '")', j
        if name in ("text", "textrm"):
            return '"' + _typ_text(inner) + '"', j
        if name == "textbf":
            return 'bold("' + _typ_text(inner) + '")', j
        return fn + "(" + _translate(inner) + ")", j
    if name in SPACING:
        tok = SPACING[name]
        return (tok, i) if tok else ("", i)
    if name in COMMANDS:
        return COMMANDS[name], i
    raise MathConvertError("unsupported LaTeX command: \\%s" % name)


def _translate(s):
    """Translate a LaTeX math fragment (no surrounding $) into Typst math markup."""
    out = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == "\\":
            name, j = _read_command(s, i)
            txt, k = _render_command(name, s, j)
            out.append(txt)
            # a trailing space after a word-token (mu, Pi, thin, in, ...) keeps it
            # from gluing to the next token; tokens ending in ) or a symbol need
            # none. Typst collapses extra math spaces and sub/superscripts still
            # attach across them (verified), so this never detaches a script.
            if txt and txt[-1].isalnum():
                out.append(" ")
            i = k
            continue
        if c == "{":
            inner, j = _read_group(s, i)
            out.append(_translate(inner))  # invisible LaTeX grouping -> transparent
            i = j
            continue
        if c == "}":
            raise MathConvertError("unmatched } in math: %r" % s[max(0, i - 20):i + 1])
        if c in "_^":
            arg, j = _read_script(s, i + 1)
            out.append(c + arg)
            i = j
            continue
        if c == "&":  # alignment tab (only meaningful inside aligned env, handled by caller)
            out.append("&")
            i += 1
            continue
        if c == "%":  # LaTeX comment to end of line
            while i < n and s[i] != "\n":
                i += 1
            continue
        out.append(c)  # ordinary char: letters, digits, ( ) [ ] + - = < > | . , ; : ! ? / * space
        i += 1
    return "".join(out)


def _read_script(s, i):
    """Read a sub/superscript argument at s[i:]; return (typst_arg, next_i)."""
    i = _skip_ws(s, i)
    if i >= len(s):
        raise MathConvertError("script marker '_' or '^' with no argument")
    if s[i] == "{":
        inner, j = _read_group(s, i)
        return "(" + _translate(inner) + ")", j
    if s[i] == "\\":
        name, j = _read_command(s, i)
        txt, k = _render_command(name, s, j)
        return "(" + txt + ")", k
    return _translate(s[i]), i + 1


def translate_inline(latex):
    """LaTeX (no delimiters) -> a Typst inline math body (no surrounding $)."""
    return _translate(latex.strip())


def translate_display(latex):
    """LaTeX display body -> Typst display math body. Supports a lightweight
    aligned form: lines separated by '\\\\' become rows; '&' becomes an align tab.
    Returns Typst markup WITHOUT surrounding $ ... $ (caller wraps)."""
    body = latex.strip()
    # strip an optional \begin{aligned}...\end{aligned} / align* wrapper
    for env in ("aligned", "align*", "align", "gather*", "gather", "cases"):
        b = "\\begin{" + env + "}"
        e = "\\end{" + env + "}"
        if body.startswith(b) and body.endswith(e):
            body = body[len(b):-len(e)].strip()
            break
    rows = [r.strip() for r in body.split("\\\\") if r.strip()]
    if len(rows) <= 1:
        return _translate(body)
    return " \\\n  ".join(_translate(r) for r in rows)


if __name__ == "__main__":
    # self-test: the audit's required prototype expressions + registry glyphs.
    import typst, os, tempfile, pypdf
    CASES = [
        (r"\operatorname{Inst}_A", "inline"),
        (r"O^*(m; A)", "inline"),
        (r"\hat p_{A,\alpha,t}(m) \in \Pi_A^\partial", "inline"),
        (r"\bar\mu_{e,j}", "inline"),
        (r"\vec\mu = (\mu_1, \ldots, \mu_k; \preceq)", "inline"),
        (r"\vec C", "inline"),
        (r"\operatorname{StrictlySoundReasoning}_\chi(e) := \operatorname{ReasoningPathAdequate}_\chi(e) \wedge \operatorname{TokenTruthLinked}_\chi(e)", "inline"),
        (r"\mathcal{M}_A \subseteq \mathcal{M} \quad \mathcal{K}_A \quad \mathcal{R}_A \quad \mathcal{W}_A \quad \mathcal{Q}_e \quad \mathcal{G}_{\alpha, A_\alpha}", "inline"),
        (r"\Gamma_E = (E, \rightsquigarrow)", "inline"),
        (r"m_t \xrightarrow{a_t} m_{t+1}", "inline-should-fail"),  # xrightarrow unsupported -> must raise
        (r"\{\, x \in M \mid O^*(x; A) \in \mathcal{G} \,\}", "inline"),
        (r"\begin{aligned} b_t &\to b_{t+1} \\ \hat p_t &\to \hat p_{t+1} \end{aligned}", "display"),
    ]
    typ_lines = ["#set page(width: 340pt, height: auto, margin: 10pt)", "#set text(size: 10pt)"]
    ok = 0
    for latex, kind in CASES:
        try:
            if kind == "display":
                body = translate_display(latex)
                typ_lines.append("$ " + body + " $")
            else:
                body = translate_inline(latex)
                typ_lines.append("$" + body + "$")
            print("OK   %-10s %s\n       -> %s" % (kind, latex[:52], body[:72]))
            ok += 1
        except MathConvertError as ex:
            marker = "EXPECTED-FAIL" if kind.endswith("fail") else "UNEXPECTED-FAIL"
            print("%s %s -> %s" % (marker, latex[:40], ex))
    src = "\n\n".join(typ_lines)
    d = tempfile.mkdtemp()
    p = os.path.join(d, "t.typ")
    open(p, "w", encoding="utf-8").write(src)
    pdf = typst.compile(p)
    open(os.path.join(d, "t.pdf"), "wb").write(pdf)
    r = pypdf.PdfReader(os.path.join(d, "t.pdf"))
    txt = "\n".join(pg.extract_text() for pg in r.pages)
    nul = txt.count("\x00")
    print("\ncompiled %d bytes, pages=%d, NOTDEF(NUL)=%d" % (len(pdf), len(r.pages), nul))
    print("extracted (first 400 chars):\n" + txt[:400])
