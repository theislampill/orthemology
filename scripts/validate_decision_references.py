#!/usr/bin/env python3
"""Semantic decision-reference validator (R7D, Decision 0029, audit B5/B38).

Deterministic, offline. Syntactic existence of a `Decision NNNN` reference is not
semantic correctness: the R7C companion attributed the analysis-relative primitives
`Inst_A` / `O*(m; A)` to Decision 0005 (symbol normalization) when they belong to
Decision 0001 (analysis-relative ground truth). This gate binds specific concepts to
their governing decision via an explicit registry and fails when a document cites the
wrong one in the same sentence/line.

The registry is explicit because the mapping cannot be inferred automatically: it is
maintained here, reviewed like any other normative surface.

Establishes no empirical or theological claim; a citation-integrity gate only.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

# concept -> (regex that matches a mention of the concept, correct decision id,
#             set of WRONG decision ids that must never appear in the same line)
REGISTRY = [
    # analysis-relative ground truth primitives belong to 0001, NOT 0005 (symbol norm)
    ("Inst_A / O*(m;A) analysis-relative primitive",
     re.compile(r"\\operatorname\{Inst\}_A|\bInst_A\b|O\^?\*\(m;?\s*A\)|O\^\{?\\?\*\}?\(m"),
     "0001", {"0005"}),
    # symbol normalization is 0005, not 0004 (verdict registry)
    ("symbol/notation normalization",
     re.compile(r"symbol[- ]table normalization|notation normalization|symbol normalization", re.I),
     "0005", {"0004"}),
]

# documents whose decision references are load-bearing normative prose
DOCS = [
    "companion/dynamic-orthing-noetic-learning-and-orthability.md",
    "companion/orthability-and-the-ground-of-intelligibility.md",
    "companion/orthability-divine-attributes-and-speech-athari.md",
    "manuscript/orthemma-ortheme-systems-revised-draft.md",
    "theory/orthemic-core-formalization.md",
]

DEC = re.compile(r"Decision[s]?\s+(\d{4})")


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def main():
    checked = 0
    for rel in DOCS:
        text = read(rel)
        if not text:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            cited = set(DEC.findall(line))
            if not cited:
                continue
            for concept, crx, correct, wrong in REGISTRY:
                if crx.search(line):
                    checked += 1
                    bad = cited & wrong
                    # a wrong decision id in the same line as the concept, with the
                    # correct one absent, is a semantic miscite
                    miscite = bool(bad) and correct not in cited
                    check("%s L%d: %s cites the correct decision (%s), not %s"
                          % (rel, lineno, concept, correct, sorted(wrong)),
                          not miscite, "cited %s" % sorted(cited))
    check("at least one concept-bearing decision reference was audited", checked >= 1)
    print("TOTAL: %d failures (%d concept-references audited)" % (len(FAILS), checked))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
