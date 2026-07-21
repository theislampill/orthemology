#!/usr/bin/env python3
"""Unicode-math -> LaTeX converter for the R7C corpus migration (Decision 0023).

Maps the unicode math glyphs and combining accents the corpus uses inside
backtick spans into the GitHub-compatible LaTeX subset that
`scripts/latex_to_typst_math.py` accepts. Deterministic and bounded.

Proven: over the 182 classified math/combining spans in the five publication
documents, every converted span translates and compiles under the pinned typst
package with ZERO missing-glyph (notdef) output (see
docs/project-closure/r7c/MATH-PIPELINE-PARITY-AUDIT.md and
docs/math-source-inventory.yaml). It is the migration engine for turning the
notdef-producing corpus notation (`μ⃗`/`C⃗` etc.) into real math source.

It does NOT change any meaning: it is a glyph-for-command transliteration. Every
migrated formula is still reviewed hunk-by-hunk in the fresh Fable pass.
"""
import re
import unicodedata

GREEK = {
    "α": "\\alpha", "β": "\\beta", "γ": "\\gamma", "δ": "\\delta", "ε": "\\epsilon",
    "ζ": "\\zeta", "η": "\\eta", "θ": "\\theta", "ι": "\\iota", "κ": "\\kappa",
    "λ": "\\lambda", "μ": "\\mu", "ν": "\\nu", "ξ": "\\xi", "π": "\\pi", "ρ": "\\rho",
    "σ": "\\sigma", "τ": "\\tau", "υ": "\\upsilon", "φ": "\\phi", "χ": "\\chi",
    "ψ": "\\psi", "ω": "\\omega", "Γ": "\\Gamma", "Δ": "\\Delta", "Θ": "\\Theta",
    "Λ": "\\Lambda", "Ξ": "\\Xi", "Π": "\\Pi", "Σ": "\\Sigma", "Φ": "\\Phi",
    "Ψ": "\\Psi", "Ω": "\\Omega",
}
REL = {
    "∈": "\\in", "∉": "\\notin", "⊆": "\\subseteq", "⊂": "\\subset", "⊇": "\\supseteq",
    "⊃": "\\supset", "∧": "\\wedge", "∨": "\\vee", "¬": "\\neg", "→": "\\to",
    "↦": "\\mapsto", "↪": "\\hookrightarrow", "⟨": "\\langle", "⟩": "\\rangle",
    "≼": "\\preceq", "≽": "\\succeq", "≠": "\\neq", "≤": "\\leq", "≥": "\\geq",
    "×": "\\times", "∀": "\\forall", "∃": "\\exists", "∘": "\\circ", "∂": "\\partial",
    "∇": "\\nabla", "⟺": "\\Leftrightarrow", "⇔": "\\Leftrightarrow", "⇒": "\\Rightarrow",
    "⟵": "\\leftarrow", "∪": "\\cup", "∩": "\\cap", "∅": "\\emptyset", "⊤": "\\top",
    "⊥": "\\bot", "·": "\\cdot", "⇝": "\\rightsquigarrow", "…": "\\dots", "∑": "\\sum",
    "∏": "\\prod", "√": "\\sqrt", "≔": ":=", "≈": "\\approx", "≡": "\\equiv",
    "≢": "\\neq", "∖": "\\setminus", "⊨": "\\models", "⇀": "\\rightharpoonup",
    "↔": "\\leftrightarrow", "∼": "\\sim", "≅": "\\cong", "∝": "\\propto", "∣": "\\mid",
    "′": "'", "″": "''", "⟹": "\\Rightarrow", "⟸": "\\Leftarrow", "∷": "::",
    "⟼": "\\mapsto", "↣": "\\hookrightarrow", "⊑": "\\subseteq", "⊒": "\\supseteq",
}
CAL = {}
for _i, _ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    CAL[chr(0x1D49C + _i)] = "\\mathcal{%s}" % _ch    # mathematical script
    CAL[chr(0x1D4D0 + _i)] = "\\mathcal{%s}" % _ch    # bold script
    CAL[chr(0x1D538 + _i)] = "\\mathbb{%s}" % _ch     # blackboard bold
CAL.update({"ℳ": "\\mathcal{M}", "ℒ": "\\mathcal{L}", "ℛ": "\\mathcal{R}",
            "ℬ": "\\mathcal{B}", "ℰ": "\\mathcal{E}", "ℱ": "\\mathcal{F}",
            "ℋ": "\\mathcal{H}", "ℐ": "\\mathcal{I}", "ℊ": "\\mathcal{g}",
            "ℯ": "\\mathcal{e}", "ℓ": "\\ell", "ℕ": "\\mathbb{N}", "ℝ": "\\mathbb{R}"})
SUB = {"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6", "₇": "7",
       "₈": "8", "₉": "9", "ₐ": "a", "ₑ": "e", "ᵢ": "i", "ⱼ": "j", "ₖ": "k", "ₘ": "m",
       "ₙ": "n", "ₜ": "t", "ₓ": "x", "₊": "+", "₋": "-", "₌": "="}
SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7",
       "⁸": "8", "⁹": "9", "ⁿ": "n", "ⁱ": "i", "⁺": "+", "⁻": "-", "ᵃ": "a", "ᵇ": "b",
       "ᶜ": "c", "ᵈ": "d", "ᵉ": "e", "ᵏ": "k", "ᵐ": "m", "ᵖ": "p", "ᵗ": "t", "ᵛ": "v"}
ACCENT = {"̄": "bar", "̂": "hat", "⃗": "vec", "̇": "dot", "̃": "tilde",
          "́": "acute", "̀": "grave", "̌": "check"}


def _atom(ch):
    return GREEK.get(ch) or CAL.get(ch) or REL.get(ch) or ch


def convert(s):
    s = unicodedata.normalize("NFD", s)   # Ô -> O + combining circumflex, etc.
    out = []
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if i + 1 < n and s[i + 1] in ACCENT:      # base + combining accent
            out.append("\\%s{%s}" % (ACCENT[s[i + 1]], _atom(ch)))
            i += 2
            continue
        if ch in SUB:
            j = i; run = ""
            while j < n and s[j] in SUB:
                run += SUB[s[j]]; j += 1
            out.append(("_{%s}" if len(run) > 1 else "_%s") % run)
            i = j
            continue
        if ch in SUP:
            j = i; run = ""
            while j < n and s[j] in SUP:
                run += SUP[s[j]]; j += 1
            out.append(("^{%s}" if len(run) > 1 else "^%s") % run)
            i = j
            continue
        atom = _atom(ch)
        if atom.startswith("\\") and out and out[-1][-1:].isalnum():
            out.append(" ")                        # E + \times -> E \times
        out.append(atom)
        if (atom.startswith("\\") and atom[-1].isalpha()
                and i + 1 < n and s[i + 1].isascii() and s[i + 1].isalpha()):
            out.append(" ")                        # \langle + g -> \langle g
        i += 1
    r = "".join(out)
    r = re.sub(r"([A-Za-z\}\)])\*", r"\1^*", r)     # O* -> O^*
    r = re.sub(r"([_^])([A-Za-z0-9]{2,})", r"\1{\2}", r)  # C^profile -> C^{profile}
    return r


def unmapped(s):
    """Non-ASCII chars that survive conversion (would need a new mapping)."""
    return {c for c in convert(s) if ord(c) > 127 and c not in "{}"}


if __name__ == "__main__":
    for t in ["μ⃗", "C⃗", "μ̄_{e,j}", "Inst_A ⊆ M_A × O_A", "Π_A^∂", "𝒢_{α,A_α} ⊆ Π_{A_α}"]:
        print("%-24s -> %s" % (t, convert(t)))
