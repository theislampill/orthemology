#!/usr/bin/env python3
"""Public/private evidence-boundary validator (Decision 0017, R5).

Publication-facing prose (manuscript/, theory/, companion/) may not lean on
the private design-history records as evidence. This validator fails when the
private-evidence vocabulary reappears there, and when the standing
no-public-dataset statements go missing. Deterministic, offline.

Scope note: STATUS.md/README.md carry the boundary *statement* ("private,
not auditable, no claim rests on them") — that is the honesty surface, not a
violation, and it is governed by the review-state contract instead.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

BANNED = [
    "casebook",
    "branch 11",
    "transcript-verified",
    "real and recurrent",
    "observational support",
    "observational record",
    "33-case",
    "33 cases",
    "fifty governed stops",
    "internal longitudinal",
]

TREES = ["manuscript", "theory", "companion"]

REQUIRED_MANUSCRIPT = [
    "No public observational dataset",
    "non-evidential design provenance",
    "None currently supplied",
]


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def main():
    offenders = []
    for tree in TREES:
        for base, _dirs, fns in os.walk(os.path.join(ROOT, tree)):
            for fn in fns:
                if not fn.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(base, fn), ROOT).replace("\\", "/")
                text = io.open(os.path.join(base, fn), encoding="utf-8").read().lower()
                for tok in BANNED:
                    if tok in text:
                        offenders.append("%s: %r" % (rel, tok))
    check("publication-facing prose free of private-evidence vocabulary",
          not offenders, "; ".join(offenders[:6]))

    ms_rel = "manuscript/orthemma-ortheme-systems-revised-draft.md"
    ms = io.open(os.path.join(ROOT, ms_rel), encoding="utf-8").read()
    for phrase in REQUIRED_MANUSCRIPT:
        check("manuscript carries the standing statement %r" % phrase, phrase in ms)

    # the availability section itself must carry the no-dataset statement —
    # a copy elsewhere (e.g. the abstract) must not be able to stand in for it
    # (found by adversarial pass G-B3)
    avail = ms.split("## 17. Data and Materials Availability", 1)
    avail_text = avail[1].split("\n## ", 1)[0] if len(avail) == 2 else ""
    check("availability section itself states no public observational dataset",
          "No public observational dataset" in avail_text)
    check("availability section states the private records are non-evidential",
          "no claim in this paper rests on them" in avail_text
          or "non-evidential" in avail_text)

    check("manuscript labels the launch-pipeline example synthetic and non-evidential",
          "Synthetic composite" in ms and "not evidence" in ms)
    check("manuscript frames the residual as an integration proposal, not impossibility",
          "integration proposal" in ms and "has no object on which a joint verdict" not in ms)
    check("no current prose calls fixtures a consistency proof",
          "Consistency shown by construction" not in ms
          and "formal coherence established analytically" not in
          io.open(os.path.join(ROOT, "theory", "orthemic-core-formalization.md"),
                  encoding="utf-8").read())

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
