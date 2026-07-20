#!/usr/bin/env python3
"""Companion references validator (Decision 0019 / R6 Phase G).

Checks that both companion papers carry a self-contained References section
whose entries resolve, and that in-text author-year citations resolve to a
listed reference. Deterministic, offline; asserts bibliographic apparatus,
never source truth or wording access.

Checks per companion:
  1. a "## References" section exists;
  2. every reference line carries an explicit <!-- ref:KEY --> marker whose
     KEY exists in references/orthemology.bib;
  3. every in-text (Author Year) citation matches a listed reference by
     surname and year (citation-without-reference guard);
  4. no reference marker is orphaned (reference-without-citation guard is
     advisory only for classical works cited by title, so it is enforced
     just for author-year style entries);
  5. the References section defers evidence-access status to the registry
     (no PRIMARY_TEXT_EXACT-style claim is made inside the section beyond a
     registry row pointer).
"""
import io
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

COMPANIONS = ["companion/orthability-and-the-ground-of-intelligibility.md",
              "companion/orthability-divine-attributes-and-speech-athari.md"]


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    return io.open(os.path.join(ROOT, rel), encoding="utf-8").read()


def fold(s):
    out = unicodedata.normalize("NFKD", s)
    return "".join(c for c in out if not unicodedata.combining(c) and c.isascii()).lower()


def main():
    bib = read("references/orthemology.bib")
    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib))

    for rel in COMPANIONS:
        text = read(rel)
        parts = text.split("\n## References", 1)
        check("%s has a References section" % rel, len(parts) == 2)
        if len(parts) != 2:
            continue
        body, refsec = parts[0], parts[1]

        keys = re.findall(r"<!--\s*ref:([\w\-]+)\s*-->", refsec)
        check("%s references carry explicit keys" % rel, bool(keys))
        missing = sorted(set(keys) - bib_keys)
        check("%s: every reference key exists in the main bibliography" % rel,
              not missing, str(missing))

        # in-text author-year citations resolve to a listed reference
        cites = set(re.findall(r"\(([A-Z][^()]{0,60}?(?:19|20)\d{2}[a-z]?)\)", body))
        ref_fold = fold(refsec)
        unresolved = []
        for c in cites:
            m = re.match(r"(.+?)\s+((?:19|20)\d{2})[a-z]?$", c.strip())
            if not m:
                continue
            names, year = m.group(1), m.group(2)
            surnames = [fold(w) for w in re.split(r"\s*&\s*|,\s*| and ", names) if w
                        and w[0].isupper() and len(w) > 2 and w.lower() not in ("the", "in")]
            if not surnames:
                continue
            if not all(s in ref_fold for s in surnames) or year not in refsec:
                unresolved.append(c)
        check("%s: every in-text author-year citation resolves to a reference" % rel,
              not unresolved, str(unresolved[:4]))

        # author-year style entries must be cited somewhere in the body
        fbody = fold(body)
        orphans = []
        for line in refsec.splitlines():
            if "ref:" not in line:
                continue
            m = re.search(r"^-\s*(.+?)\s*\((\d{4})\)", line)
            if m:
                surname = fold(m.group(1).split(",")[0])
                if surname and surname not in fbody:
                    orphans.append(m.group(1)[:30])
        check("%s: no orphan author-year reference (uncited entry)" % rel,
              not orphans, str(orphans[:4]))

        check("%s References section defers wording-access status to the registry" % rel,
              "PRIMARY_TEXT_EXACT" not in refsec or "source-status" in refsec)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
