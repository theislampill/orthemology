#!/usr/bin/env python3
"""Qurʾān locus validator (R3 §6.1). Offline and deterministic.

Checks: (1) every locus in references/quran-loci.yaml is well-formed and
in-range for its sūrah (using the registry's recorded āyah counts);
(2) every sūrah:āyah citation found in current papers and sourcing ledgers
appears in the registry (corpus→registry consistency); (3) the known-defective
bare '20:11' citation no longer occurs in current papers/ledgers (the correct
form is 20:11-12 or 20:12); (4) every registry locus declares usage
direct|inference and a verification date exists.

Live verification against the text happened in the R3 research pass and is
recorded in the registry; CI verifies the records, not the internet.
"""
import os
import re
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

SCAN = [
    "companion/orthability-divine-attributes-and-speech-athari.md",
    "companion/orthability-and-the-ground-of-intelligibility.md",
    "companion/CONCRETE-AND-SOUND-REASON.md",
    "companion/sourcing/COMPANION-SOURCING-LEDGER.md",
    "docs/sourcing/SOURCING-LEDGER.md",
    "docs/sourcing/R3-SOURCING-LEDGER.md",
    "companion/sourcing/R3-COMPANION-SOURCING-LEDGER.md",
]

CITE = re.compile(r"\((\d{1,3}):(\d{1,3})(?:[-–](\d{1,3}))?\)")


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def main():
    reg = yaml.safe_load(open(os.path.join(ROOT, "references", "quran-loci.yaml"), encoding="utf-8"))
    counts = reg["surah_ayah_counts"]
    check("registry records a verification date", bool(reg.get("verified")))

    covered = set()
    for loc in reg["loci"]:
        ref = loc["ref"]
        m = re.fullmatch(r"(\d+):(\d+)(?:-(\d+))?", ref)
        check("locus %s well-formed" % ref, bool(m))
        if not m:
            continue
        s, a1 = int(m.group(1)), int(m.group(2))
        a2 = int(m.group(3)) if m.group(3) else a1
        check("locus %s sūrah known" % ref, s in counts)
        if s in counts:
            check("locus %s in range (sūrah has %d āyāt)" % (ref, counts[s]),
                  1 <= a1 <= a2 <= counts[s])
        check("locus %s declares usage" % ref, loc.get("usage") in ("direct", "inference"))
        for a in range(a1, a2 + 1):
            covered.add((s, a))

    for rel in SCAN:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        cited = set()
        for m in CITE.finditer(text):
            s, a1 = int(m.group(1)), int(m.group(2))
            a2 = int(m.group(3)) if m.group(3) else a1
            if s not in counts:
                continue  # non-Quranic numeric parenthetical (page refs etc.)
            for a in range(a1, a2 + 1):
                cited.add((s, a))
        missing = sorted(cited - covered)
        check("%s: every cited āyah is in the registry" % rel, not missing, str(missing[:8]))
        # the known defect: a bare 20:11 citation not extended to 20:12
        bad2011 = re.search(r"\(20:11\)", text)
        check("%s: no bare (20:11) citation" % rel, not bad2011)
    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
