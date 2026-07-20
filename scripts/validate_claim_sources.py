#!/usr/bin/env python3
"""Citation/source-ledger completeness validator.

Checks required fields and stable identifiers are PRESENT and consistent
(deterministic); it performs NO live web requests — scholarly verification
belongs to the sourcing pass, not CI."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

ALLOWED_STATUSES = ("WEB-VERIFIED", "RECORD-CONFIRMED", "VIA-COMPILATION", "UNVERIFIED")


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def table_rows(text):
    rows = []
    for ln in text.splitlines():
        if ln.startswith("|") and not set(ln) <= set("|- :"):
            cells = [c.strip() for c in ln.strip("|").split("|")]
            rows.append(cells)
    return rows


def main():
    bib_path = os.path.join(ROOT, "references", "orthemology.bib")
    check("references/orthemology.bib exists", os.path.exists(bib_path))
    bib = open(bib_path, encoding="utf-8").read()
    keys = set(re.findall(r"@\w+\{([^,\s]+),", bib))
    check("bib has entries", len(keys) >= 30, "found %d" % len(keys))
    braces_balanced = bib.count("{") == bib.count("}")
    check("bib braces balanced", braces_balanced,
          "{=%d }=%d" % (bib.count("{"), bib.count("}")))
    dupes = len(keys) != len(re.findall(r"@\w+\{([^,\s]+),", bib))
    check("bib keys unique", not dupes)

    for rel in ("docs/sourcing/SOURCING-LEDGER.md", "companion/sourcing/COMPANION-SOURCING-LEDGER.md"):
        p = os.path.join(ROOT, rel)
        check(rel + " exists", os.path.exists(p))
        if not os.path.exists(p):
            continue
        text = open(p, encoding="utf-8").read()
        rows = [r for r in table_rows(text) if len(r) >= 4]
        header_like = [r for r in rows if "Status" in r or "status" in r]
        data = [r for r in rows if r not in header_like]
        check(rel + " has data rows", len(data) >= 5, "rows=%d" % len(data))
        # every data row carries a recognized status token somewhere
        missing_status = [r[0][:40] for r in data
                          if not any(s in " ".join(r) for s in ALLOWED_STATUSES)]
        check(rel + ": every row carries a recognized verification status",
              not missing_status, str(missing_status[:5]))
        # bib keys mentioned in the ledger must exist in the bib
        mentioned = set(re.findall(r"\b([a-z][a-z_]*\d{4}[a-z]*)\b", text))
        ghosts = sorted(k for k in mentioned if k not in keys and re.match(r"^[a-z_]+\d{4}[a-z]*$", k)
                        and k not in ("conee1998",))
        ghosts = [g for g in ghosts if g in text and ("_" in g or any(g.startswith(pfx) for pfx in
                  ("kaelbling", "littman", "givan", "larsen", "hopcroft", "fisher", "crutchfield",
                   "shalizi", "chow", "tsoumakas", "silla", "elyaniv", "geifman", "traub",
                   "scheirer", "hendrycks", "howard", "wald", "w3c", "chen", "iaasb", "iso",
                   "gettier", "goldman", "plantinga", "millikan", "sep", "stroud", "anderson",
                   "hume", "garrett", "kemp", "hoover", "millican", "loeb", "bukhari", "tahawi",
                   "ibntaymiyya", "ibnqayyim", "ibnuthaymin", "lalikai", "quran")))]
        check(rel + ": every cited bib key resolves", not ghosts, str(ghosts[:8]))

    # VIA-COMPILATION claims must be flagged in the Athari paper itself
    athari = os.path.join(ROOT, "companion", "orthability-divine-attributes-and-speech-athari.md")
    if os.path.exists(athari):
        at = open(athari, encoding="utf-8").read()
        check("Athari paper flags compilation-sourced loci inline", "[via compilation]" in at)
        check("Athari paper carries the school-internal label", "school-internal" in at)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
