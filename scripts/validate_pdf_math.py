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


def validate_pdf_records(documents, text_by_artifact):
    """Return v2 migration-ledger PDF glyph issues without legacy key aliases."""
    issues = []
    for document in documents:
        name = document.get("artifact_id")
        if not name:
            issues.append("migration document missing artifact_id")
            continue
        text = text_by_artifact.get(name)
        if text is None:
            issues.append("%s artifact present" % name)
            continue
        notdef = text.count("\x00")
        replacement = text.count("�")
        expected = document.get("expected_notdef")
        if not isinstance(expected, int) or notdef != expected:
            issues.append(
                "%s notdef count == pinned (%r); observed %d"
                % (name, expected, notdef)
            )
        if replacement:
            issues.append(
                "%s has no U+FFFD replacement glyph; observed %d"
                % (name, replacement)
            )
        if document.get("full_math_source_migrated") is True and notdef:
            issues.append("%s migrated artifact must be notdef-free" % name)
    gallery = text_by_artifact.get("notation-gallery")
    if gallery is not None:
        for token in GALLERY_TOKENS:
            if token not in gallery:
                issues.append(
                    "notation-gallery PDF renders operator %r" % token
                )
    return issues


def main():
    mig = yaml.safe_load(io.open(os.path.join(ROOT, "docs/math-migration-status.yaml"),
                                 encoding="utf-8").read())
    text_by_artifact = {
        document.get("artifact_id"): pdf_text(document.get("artifact_id"))
        for document in mig["documents"]
        if document.get("artifact_id")
    }
    issues = validate_pdf_records(mig["documents"], text_by_artifact)
    for issue in issues:
        check(issue, False)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
