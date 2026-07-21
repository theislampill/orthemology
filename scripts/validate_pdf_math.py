#!/usr/bin/env python3
"""PDF mathematical-glyph regression gate (R7B, Decision 0023).

Deterministic, offline. Reads the committed artifacts and the math-migration
ledger (docs/math-migration-status.yaml) and enforces:

  1. every rendered PDF's missing-glyph (notdef / NUL) count EQUALS the value
     pinned in the ledger — expected_notdef (0) for migrated documents,
     known_notdef for not-yet-migrated corpus documents. This turns the
     reproduced notdef defect (R7B-PDF-MATH-BASELINE.md) into a tracked
     quantity: it cannot silently grow, and it cannot be silently declared
     fixed (a migration to migrated:true must drop the pinned value to 0 in the
     same commit);
  2. no U+FFFD replacement character in any rendered PDF;
  3. equation-loss / gallery-drift guard: the notation-gallery PDF text layer
     contains the rendered operator names that prove the showcase equations
     actually rendered (not dropped) — Inst, MetaTok, StrictlySoundReasoning,
     TokenAdequate.

It establishes no empirical or theological claim; it is a rendering gate.
"""
import io
import os
import sys

try:
    import yaml
    from pypdf import PdfReader
except ImportError as e:
    print("FATAL: requires pyyaml + pypdf:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "artifacts")
FAILS = []
GALLERY_TOKENS = ["Inst", "MetaTok", "StrictlySoundReasoning", "TokenAdequate"]


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def pdf_text(name):
    p = os.path.join(ART, name + ".pdf")
    if not os.path.exists(p):
        return None
    r = PdfReader(p)
    return "\n".join(pg.extract_text() or "" for pg in r.pages)


def main():
    mig = yaml.safe_load(io.open(os.path.join(ROOT, "docs/math-migration-status.yaml"),
                                 encoding="utf-8").read())
    for d in mig["documents"]:
        name = d["pdf"]
        txt = pdf_text(name)
        if txt is None:
            check("%s artifact present" % name, False)
            continue
        notdef = txt.count("\x00")
        fffd = txt.count("�")
        expected = d["expected_notdef"] if d.get("migrated") else d["known_notdef"]
        check("%s notdef count == pinned (%d)" % (name, expected),
              notdef == expected,
              "observed %d notdef vs pinned %d — update the source migration or the ledger, never silently"
              % (notdef, expected))
        check("%s has no U+FFFD replacement glyph" % name, fffd == 0,
              "%d replacement chars" % fffd)
        if d.get("migrated"):
            check("%s (migrated) is notdef-free" % name, notdef == 0,
                  "a migrated document must render every glyph")

    gtxt = pdf_text("notation-gallery") or ""
    for tok in GALLERY_TOKENS:
        check("notation-gallery PDF renders operator %r (no equation loss)" % tok,
              tok in gtxt)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
