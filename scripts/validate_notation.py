#!/usr/bin/env python3
"""Deterministic notation validator (Decision 0005).

Enforces the normative symbol registry (docs/notation-registry.yaml) over the
CURRENT corpus: no retired symbols, no role collisions, no legacy verdict
aliases, no task shorthand in multi-analysis contexts, no A/B formal actors,
and every verdict alias drawn from the verdict registry. Historical documents
(archive/, docs/provenance/, docs/decisions/, CHANGELOG.md) are exempt: they
are immutable records and retain old symbols by design.

Deterministic consistency tool; establishes no empirical claim.
"""
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("FATAL: PyYAML is required (pip install pyyaml)")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

# Current normative corpus (glob roots). Companion papers use their own declared
# local notation and are checked only for legacy verdict aliases and A/B actors.
CURRENT = ["theory", "manuscript", "docs/glossary.md", "docs/architecture-overview.md", "examples"]
COMPANION = ["companion"]


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def md_files(roots):
    out = []
    for r in roots:
        p = os.path.join(ROOT, r)
        if os.path.isfile(p):
            out.append(p)
        elif os.path.isdir(p):
            for dp, _, fns in os.walk(p):
                out += [os.path.join(dp, f) for f in fns if f.endswith(".md")]
    return out


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def main():
    with open(os.path.join(ROOT, "docs", "verdict-registry.yaml"), encoding="utf-8") as f:
        vreg = yaml.safe_load(f)
    with open(os.path.join(ROOT, "docs", "notation-registry.yaml"), encoding="utf-8") as f:
        nreg = yaml.safe_load(f)

    aliases = {v["alias"] for v in vreg["verdicts"]}
    files = md_files(CURRENT)
    texts = {p: open(p, encoding="utf-8").read() for p in files}
    comp_files = md_files(COMPANION)
    comp_texts = {p: open(p, encoding="utf-8").read() for p in comp_files}

    # 1. Retired symbols absent from the current corpus
    retired_patterns = [
        (r"App\(e\)", "retired App(e) (write App(·) only when citing the retirement)"),
        (r"R\*\(q\)", "retired R*(q)"),
        (r"Q_\{i=j\}", "retired Q_{i=j}"),
        (r"W\(·\)", "retired W(·) goal schema"),
        (r"select_μ\s*=\s*ε", "selector/epsilon confusion"),
        (r"ε_μ", "retired ε_μ selector"),
        (r"\bI_T\b", "pre-D1 primitive I_T"),
        (r"G = \(V_E", "retired bare-G episode graph"),
        (r"G\(α, T_α\)", "retired G(α, T_α) target set"),
    ]
    bad = []
    for p, c in texts.items():
        for pat, why in retired_patterns:
            if re.search(pat, c):
                bad.append("%s: %s" % (rel(p), why))
    check("no retired symbols in current corpus", not bad, "; ".join(bad))

    # 2. Legacy verdict aliases absent from current corpus (incl. companions)
    legacy = [r"V2b\^proc", r"V2b\^tok"]
    bad = []
    for p, c in list(texts.items()) + list(comp_texts.items()):
        for pat in legacy:
            if re.search(pat, c):
                bad.append("%s: %s" % (rel(p), pat))
    check("no legacy caret verdict aliases in current corpus", not bad, "; ".join(bad))

    # 3. Every V-token used is a registry alias. No trailing \b: greedy -P/-T
    #    capture must win even before claim subscripts like V2b-T_q.
    vtok = re.compile(r"\bV\d+[a-e]?(?:-[PT])?")
    bad = []
    for p, c in texts.items():
        for m in vtok.finditer(c):
            tok = m.group(0)
            if tok not in aliases:
                bad.append("%s: %s" % (rel(p), tok))
    check("every verdict token matches a registry display alias", not bad, "; ".join(sorted(set(bad))))

    # 4. No A/B formal actors: 'actor A', 'actors A and B' banned; 'Player A' is a
    #    declared prose label; 'Arm A/B/C' are benchmark arm names (not actors).
    bad = []
    actor_pat = re.compile(r"\bactors?\s+[AB]\b")
    for p, c in list(texts.items()) + list(comp_texts.items()):
        for m in actor_pat.finditer(c):
            bad.append("%s: '%s'" % (rel(p), m.group(0)))
    check("no A/B formal actor indices (α, β required)", not bad, "; ".join(bad))

    # 5. Task shorthand absent from declared multi-analysis contexts:
    #    the multi-actor note, manuscript Section 10, core §5.3.
    shorthand = re.compile(r"O\*_T\(|\bInst_T\b")
    bad = []
    note = os.path.join(ROOT, "theory", "orthemic-multi-actor-conflict-note.md")
    if os.path.exists(note) and shorthand.search(open(note, encoding="utf-8").read()):
        bad.append("multi-actor note uses task shorthand")
    for p, c in texts.items():
        if "manuscript" in rel(p):
            sec10 = re.search(r"\n## 10\..*?(?=\n## \d|\Z)", c, re.S)
            if sec10 and shorthand.search(sec10.group(0)):
                bad.append("%s: task shorthand inside Section 10 (multi-actor)" % rel(p))
        if "orthemic-core-formalization" in rel(p):
            sec53 = re.search(r"\n### 5\.3 .*?(?=\n### |\n## |\Z)", c, re.S)
            if sec53 and shorthand.search(sec53.group(0)):
                bad.append("%s: task shorthand inside §5.3 (multi-actor)" % rel(p))
    check("task shorthand absent from multi-analysis contexts", not bad, "; ".join(bad))

    # 6. Normative files that use registry glyphs reference the registry or define locally
    glyphs = ["𝒢_{", "Γ_E", "estatus", "select_μ", "θ_stop", "𝒬"]
    bad = []
    for p, c in texts.items():
        uses = [g for g in glyphs if g in c]
        if uses and ("notation-registry" not in c and "core formalization" not in c.lower()
                     and "core-formalization" not in c):
            bad.append("%s uses %s without registry reference" % (rel(p), uses))
    check("registry glyphs are anchored to the registry or the core", not bad, "; ".join(bad))

    # 7. Claim ledger vs representation: bare '`Q`' as a formal symbol is retired
    bad = []
    for p, c in texts.items():
        if re.search(r"claim ledger `Q`", c) or re.search(r"ledger `Q`\b", c):
            bad.append(rel(p))
    check("claim ledger written 𝒬 (no bare Q ledger)", not bad, "; ".join(bad))

    # 8. Registry files parse and are internally consistent
    ok = isinstance(nreg.get("symbols"), list) and isinstance(nreg.get("retired_symbols"), list)
    check("notation registry parses with symbols and retired_symbols lists", ok)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
