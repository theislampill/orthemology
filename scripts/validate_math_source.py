#!/usr/bin/env python3
"""Mathematical-source validator (R7B, Decision 0023).

Deterministic, offline. Guards the math-source discipline the audit requires:

  1. render_map <-> registry bijection: every non-retired notation symbol has
     exactly one render_map entry and vice versa (no symbol goes un-rendered,
     no orphan render entry drifts in);
  2. every render_map `latex` translates through scripts/latex_to_typst_math.py
     with no MathConvertError (the strict subset actually covers the corpus);
  3. notation-gallery drift: every render_map `latex` appears verbatim in
     docs/notation-gallery.md, so the gallery renders every registered symbol;
  4. NO precomposed combining accent (U+0300-U+036F, U+20D7) inside publication
     math source ($...$, $$...$$, ```math) anywhere in the corpus — publication
     math must use \\hat / \\bar / \\vec (this is the exact source antipattern
     behind the reproduced notdef defect, R7B-PDF-MATH-BASELINE.md);
  5. the math-migration-status manifest covers every build_pdfs source document
     (nothing is silently omitted from the migration ledger).

This is a typography/consistency gate. It establishes no empirical or
theological claim, and it does not change any symbol's meaning (Decision 0005).
"""
import io
import os
import re
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from latex_to_typst_math import translate_inline, translate_display, MathConvertError

FAILS = []
GALLERY = "docs/notation-gallery.md"
# combining diacritics that must never appear in publication math source
COMBINING = re.compile(r"[̀-ͯ⃗]")
DISPLAY_RE = re.compile(r"\$\$(.+?)\$\$", re.S)
INLINE_RE = re.compile(r"\$([^\$\n]+?)\$")
CODE_FENCE_RE = re.compile(r"```(\w*)\n(.*?)```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def real_math_spans(text):
    """Extract genuine math spans, ignoring $ that appears inside code fences or
    inline `code` (e.g. prose describing the $...$ syntax). Returns (kind, body)
    with kind 'i' (inline) or 'd' (display/fence)."""
    spans = []

    def fence_sub(m):
        if m.group(1).strip() == "math":
            spans.append(("d", m.group(2)))
        return "\n"

    t = CODE_FENCE_RE.sub(fence_sub, text)
    t = INLINE_CODE_RE.sub(" ", t)
    for m in DISPLAY_RE.finditer(t):
        spans.append(("d", m.group(1)))
    t = DISPLAY_RE.sub(" ", t)
    for m in INLINE_RE.finditer(t):
        spans.append(("i", m.group(1)))
    return spans


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def main():
    reg = yaml.safe_load(read("docs/notation-registry.yaml"))
    symbols = [s["symbol"] for s in reg["symbols"]]
    rmap = reg.get("render_map", [])
    rm_syms = [e["registry_symbol"] for e in rmap]

    # 1. bijection
    missing = [s for s in symbols if s not in rm_syms]
    orphan = [s for s in rm_syms if s not in symbols]
    check("render_map covers every normative symbol", not missing, "missing: %s" % missing)
    check("render_map has no orphan (all map to a live symbol)", not orphan, "orphan: %s" % orphan)
    check("render_map has no duplicate registry_symbol",
          len(rm_syms) == len(set(rm_syms)),
          "dupes: %s" % [s for s in rm_syms if rm_syms.count(s) > 1])

    # 2. every latex translates
    gallery_text = read(GALLERY)
    for e in rmap:
        try:
            translate_inline(e["latex"])
            ok = True
            detail = ""
        except MathConvertError as ex:
            ok = False
            detail = str(ex)
        check("render_map latex translates: %s" % e["registry_symbol"], ok, detail)
        # 3. gallery drift
        check("gallery renders symbol %s" % e["registry_symbol"],
              ("$" + e["latex"] + "$") in gallery_text or e["latex"] in gallery_text,
              "latex not found verbatim in %s" % GALLERY)

    # 4. every math source span across the corpus (a) carries no precomposed
    #    combining accent and (b) translates cleanly through the strict subset —
    #    so no shipped math source can render broken or use the notdef antipattern.
    scan_roots = ["manuscript", "theory", "companion", "docs", "applications"]
    bad_accents = []
    bad_translate = []
    for r in scan_roots:
        base = os.path.join(ROOT, r)
        if not os.path.isdir(base):
            continue
        for dp, dirs, fns in os.walk(base):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
            for fn in fns:
                if not fn.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(dp, fn), ROOT).replace("\\", "/")
                text = io.open(os.path.join(dp, fn), encoding="utf-8").read()
                for kind, sp in real_math_spans(text):
                    if COMBINING.search(sp):
                        bad_accents.append("%s: %r" % (rel, sp[:40]))
                    try:
                        translate_inline(sp) if kind == "i" else translate_display(sp)
                    except MathConvertError as ex:
                        bad_translate.append("%s: %r -> %s" % (rel, sp[:30], ex))
    check("no precomposed combining accents in publication math source",
          not bad_accents, "; ".join(bad_accents[:5]))
    check("every math source span translates through the strict subset",
          not bad_translate, "; ".join(bad_translate[:5]))

    # 4b. (R7C, audit B5) no math-FORMULA or notdef-producing (U+20D7) span may sit
    #     in a backtick code span UNLESS it is a recorded, pending migration target
    #     in docs/math-source-inventory.yaml. This is the check that catches a
    #     formula left in code (tamper probe 1), which the corpus's own pending
    #     targets are allowlisted against by text.
    inv = yaml.safe_load(read("docs/math-source-inventory.yaml"))
    allow = set()
    for d in inv.get("documents", []):
        for t in d.get("targets", []):
            allow.add(t["text"])
    FORMULA = re.compile(r"[=∈⊆⊂⟺⇔→↦∧∨≼≠≤≥∀∃]|\{[^}]*\|[^}]*\}|⃗")
    INLINE_CODE = re.compile(r"`([^`]+)`")
    FENCE_STRIP = re.compile(r"```.*?```", re.S)  # remove ``` blocks so their backticks
    stray = []                                    # do not mis-pair the inline scanner
    for r in ("manuscript", "theory", "companion", "applications", "docs"):
        base = os.path.join(ROOT, r)
        if not os.path.isdir(base):
            continue
        for dp, dirs, fns in os.walk(base):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "project-closure", "archive")]
            for fn in fns:
                if not fn.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(dp, fn), ROOT).replace("\\", "/")
                if rel.endswith("math-source-inventory.yaml"):
                    continue
                body = FENCE_STRIP.sub("", io.open(os.path.join(dp, fn), encoding="utf-8").read())
                for m in INLINE_CODE.finditer(body):
                    span = m.group(1)
                    if FORMULA.search(span) and span not in allow:
                        stray.append("%s: `%s`" % (rel, span[:40]))
    check("no un-inventoried math-formula/notdef span left in a code span (B5/probe-1)",
          not stray, "; ".join(stray[:5]))

    # 5. migration manifest covers every build source doc
    mig = yaml.safe_load(read("docs/math-migration-status.yaml"))
    listed = set()
    for d in mig["documents"]:
        for s in d.get("sources", []):
            listed.add(s)
    # derive build sources from build_pdfs.py DOCS
    bp = read("scripts/build_pdfs.py")
    build_sources = set(re.findall(r'"([a-z0-9_\-]+/[A-Za-z0-9._\-/]+\.md)"', bp))
    uncovered = sorted(build_sources - listed)
    check("math-migration-status lists every build source document",
          not uncovered, "uncovered: %s" % uncovered)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
