#!/usr/bin/env python3
"""Unit tests for the R7B math pipeline (Decision 0023): the strict LaTeX-subset
-> Typst-math translator and the md_to_typst wiring. Runnable: `python
tests/test_math_pipeline.py`. Deterministic, offline."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from latex_to_typst_math import translate_inline, translate_display, MathConvertError
import md_to_typst

FAILS = []


def eq(name, got, want):
    ok = got == want
    print("[%s] %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        print("      got : %r\n      want: %r" % (got, want))
        FAILS.append(name)


def ok(name, cond, detail=""):
    print("[%s] %s%s" % ("PASS" if cond else "FAIL", name, "" if cond else " — " + detail))
    if not cond:
        FAILS.append(name)


# --- translation exactness (meaning preservation is the whole point) ----------
eq("O-star", translate_inline(r"O^*(m; A)"), "O^*(m; A)")
eq("Inst subscript", translate_inline(r"\operatorname{Inst}_A"), 'op("Inst")_A')
eq("hat + subscript group", translate_inline(r"\hat p_{A,\alpha,t}"),
   "hat(p)_(A,alpha ,t)")
eq("bar mu", translate_inline(r"\bar\mu_{e,j}"), "macron(mu)_(e,j)")
eq("vec mu", translate_inline(r"\vec\mu"), "arrow(mu)")
eq("Pi partial", translate_inline(r"\Pi_A^\partial"), "Pi _A^(partial)")
eq("calligraphic", translate_inline(r"\mathcal{Q}_e"), "cal(Q)_e")
eq("angle brackets literal", translate_inline(r"\langle a, b \rangle"), "⟨ a, b ⟩")
eq("labeled arrow", translate_inline(r"m_t \xrightarrow{a_t} m"),
   "m_t arrow.r.long^(a_t) m")
eq("underbrace with label", translate_inline(r"\underbrace{x}_{y}"),
   "underbrace(x, y)")
eq("operatorname underscore", translate_inline(r"\operatorname{hand\_in}"),
   'op("hand_in")')

# --- strict contract: unknown commands raise, never pass through --------------
for bad in [r"\frobnicate", r"\sqrt{x}", r"\begin{matrix}a\end{matrix}"]:
    try:
        translate_inline(bad)
        ok("strict: rejects %s" % bad, False, "did not raise")
    except MathConvertError:
        ok("strict: rejects %s" % bad, True)

# unbalanced braces raise
for bad in [r"\hat{p", r"a}b"]:
    try:
        translate_inline(bad)
        ok("strict: rejects unbalanced %r" % bad, False, "did not raise")
    except MathConvertError:
        ok("strict: rejects unbalanced %r" % bad, True)

# --- display / aligned --------------------------------------------------------
d = translate_display(r"\begin{aligned} a &\to b \\ c &\to d \end{aligned}")
ok("aligned has two rows", d.count("&") == 2 and "\\" in d, repr(d))

# --- md_to_typst wiring: $...$ inline, ```math fence, backticks unchanged ------
out = md_to_typst.convert("Belief $\\hat p$ is not $O^*(m;A)$.")
ok("inline $...$ -> typst math", "$hat(p)$" in out and "$O^*(m;A)$" in out, out)

out2 = md_to_typst.convert("```math\n\\vec\\mu = (\\mu_1; \\preceq)\n```\n")
ok("```math fence -> display", "$ arrow(mu)" in out2, out2)

out3 = md_to_typst.convert("Identifier `Inst_A` stays code.")
ok("backtick identifier stays #raw", '#raw("Inst_A")' in out3, out3)

# a math translation failure inside convert() surfaces as ConversionError
try:
    md_to_typst.convert("bad $\\nope$ math")
    ok("convert surfaces math errors", False, "did not raise")
except md_to_typst.ConversionError:
    ok("convert surfaces math errors", True)

print("TOTAL: %d failures" % len(FAILS))
sys.exit(1 if FAILS else 0)
