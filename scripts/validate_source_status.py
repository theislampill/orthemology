#!/usr/bin/env python3
"""Validate references/source-status.yaml and its agreement with paper prose
(Decision 0013). Offline: validates the frozen records, never the internet.

Checks:
  1. every row carries the full required field set (no silent omissions);
  2. every status is in the declared vocabulary;
  3. PRIMARY_TEXT_EXACT requires wording_directly_checked: true — the status
     cannot be claimed without the wording having been checked;
  4. any row with page_edition_dependent: true must NOT claim an exact page
     as verified (guards the R2/R3 confusion between work-level and page-level
     verification);
  5. UNVERIFIED_REMOVE_OR_DOWNSCOPE rows must be marked non-load-bearing;
  6. no load-bearing row rests solely on COMPILATION_MEDIATED;
  7. the Atharī paper carries no blanket source-status claim (the R3 front
     matter said all classical loci were [via compilation] and that printed
     editions were not opened — replaced by per-claim rows here);
  8. the corrected attribution chain is present and the withdrawn one absent:
     Doko & Turner 2023 must be cited for the concrete/ideal application, and
     the Evans page locus must never be asserted as directly verified;
  9. El-Tobgui's three records are distinct;
 10. every research residual referenced by a row exists in docs/current-state.yaml.
"""
import io
import os
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

REQUIRED = ["id", "locus", "claim_level", "claim", "source", "source_type", "doi",
            "locus_exact", "status", "verification_date", "wording_directly_checked",
            "page_edition_dependent", "school_flag", "support", "notes"]


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def main():
    reg = yaml.safe_load(read("references/source-status.yaml"))
    vocab = set(reg["status_vocabulary"])
    rows = reg["claims"]
    check("registry non-empty", len(rows) >= 10, str(len(rows)))

    ids = [r["id"] for r in rows]
    check("row ids unique", len(ids) == len(set(ids)))

    for r in rows:
        missing = [f for f in REQUIRED if f not in r]
        check("row %s carries every required field" % r.get("id"), not missing, str(missing))
        check("row %s status in vocabulary" % r["id"], r["status"] in vocab, r["status"])
        if r["status"] == "PRIMARY_TEXT_EXACT":
            check("row %s PRIMARY_TEXT_EXACT implies wording directly checked" % r["id"],
                  r.get("wording_directly_checked") is True)
        if r.get("page_edition_dependent") is True:
            txt = (str(r.get("locus_exact", "")) + " " + str(r.get("notes", ""))).lower()
            claims_exact_page = ("verified page" in txt or "page verified" in txt)
            check("row %s does not claim a verified exact page while edition-dependent" % r["id"],
                  not claims_exact_page)
        if r["status"] == "UNVERIFIED_REMOVE_OR_DOWNSCOPE":
            check("row %s unverified => marked non-load-bearing" % r["id"],
                  "not load-bearing" in str(r.get("support", "")).lower()
                  or "non-load-bearing" in str(r.get("support", "")).lower())
        if r["status"] == "COMPILATION_MEDIATED":
            check("row %s compilation-mediated => not load-bearing alone" % r["id"],
                  "not load-bearing" in str(r.get("support", "")).lower()
                  or "non-load-bearing" in str(r.get("support", "")).lower()
                  or "pending" in str(r.get("notes", "")).lower())

    athari = read("companion/orthability-divine-attributes-and-speech-athari.md")
    check("Atharī paper carries no blanket 'printed editions were not independently opened' claim",
          "printed editions were not independently opened" not in athari)
    check("Atharī paper points at the source-status registry",
          "source-status.yaml" in athari or "source-status registry" in athari.lower())

    joined = " ".join(str(r) for r in rows)
    check("Doko & Turner 2023 present as the verified application", "Doko" in joined and "2023" in joined)
    check("Doko credited in companion prose", "Doko" in read("companion/CONCRETE-AND-SOUND-REASON.md"))
    evans = [r for r in rows if "Evans" in str(r.get("source", ""))]
    check("Evans row exists", bool(evans))
    if evans:
        e = evans[0]
        check("Evans page locus not asserted as directly verified",
              e.get("wording_directly_checked") is False and e["status"] != "PRIMARY_TEXT_EXACT")
    elt = {r["id"] for r in rows if r["id"].startswith("ELT-")}
    check("El-Tobgui dissertation, monograph, and tawatur article are distinct rows",
          {"ELT-1", "ELT-2", "ELT-3"} <= elt, str(sorted(elt)))

    state = yaml.safe_load(read("docs/current-state.yaml"))
    rr_ids = {rr["id"] for rr in state["authored"]["research_residuals_with_triggers"]}
    for r in rows:
        for token in str(r.get("notes", "")).split():
            t = token.strip(".,;)")
            if t.startswith("RR-"):
                check("row %s references an existing research residual %s" % (r["id"], t), t in rr_ids)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
