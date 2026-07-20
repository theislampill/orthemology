#!/usr/bin/env python3
"""Validate references/source-status.yaml and its agreement with paper prose
(Decision 0013). Offline: validates the frozen records, never the internet.

WHAT THIS VALIDATOR ESTABLISHES (and what it does not): it checks RECORD SHAPE
and INTERNAL AGREEMENT — required fields, declared vocabulary, status/evidence-
access consistency, membership in a declared claim family, and agreement with
paper prose. It does NOT verify that a source is true, that a quotation was
actually read, that a page locus is right, or that a DOI resolves. A green run
is evidence about the records, never about the world.

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

    # R4 independent review: the registry's scope is declared and enforced.
    # Decision 0013's original "authoritative for every load-bearing claim"
    # overstated the coverage; the honest contract is that the registry is
    # authoritative for the families it declares, and every row belongs to one.
    families = reg.get("covered_claim_families") or {}
    check("registry declares its covered claim families", bool(families))
    check("registry declares what it does NOT cover", bool(reg.get("not_covered")))
    prefixes = {f["prefix"] for f in families.values()}
    orphan_rows = sorted(r["id"] for r in rows
                         if r["id"].split("-")[0] not in prefixes)
    check("every row belongs to a declared claim family",
          not orphan_rows, "rows outside any declared family: %s" % orphan_rows)
    unused = sorted(p for p in prefixes
                    if not any(r["id"].split("-")[0] == p for r in rows))
    check("every declared claim family has at least one row",
          not unused, "declared but empty: %s" % unused)
    header = read("references/source-status.yaml")
    check("registry header does not claim coverage of every load-bearing claim",
          "authoritative for\n# every load-bearing claim" not in header
          and "Authoritative for\n# every load-bearing claim" not in header)
    check("registry header states the validator does not verify source truth",
          "does\n# NOT verify that a source is true" in header
          or "NOT verify that a source is true" in header)

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

    # R4 independent review (audit §9.2, final bullet): every inline
    # [via compilation] label must AGREE with the machine registry. The R4
    # candidate had ATH-3 at PRIMARY_TEXT_EXACT / wording_directly_checked while
    # the companion labelled that same Majmūʿ al-Fatāwā locus [via compilation];
    # one citation cannot have two evidence accesses. Any row whose source is
    # cited inside a [via compilation]-labelled passage may not claim exact
    # primary wording.
    def fold(s):
        """ASCII-fold: the registry writes Majmu' al-Fatawa where the prose writes
        Majmūʿ al-Fatāwā. Without folding, the two surfaces can contradict each
        other and no substring check would ever notice."""
        import unicodedata
        out = unicodedata.normalize("NFKD", str(s))
        return "".join(c for c in out if not unicodedata.combining(c)
                       and c.isascii()).lower()

    compiled_passages = [fold(ln) for ln in athari.splitlines()
                         if "[via compilation]" in ln]
    WORK_TOKENS = ("majmu", "khalq af", "tabaqat", "sawaiq", "sharh",
                   "tuhfat", "wasitiyya", "lum")
    for r in rows:
        if r["status"] != "PRIMARY_TEXT_EXACT":
            continue
        src = fold(r.get("source", ""))
        toks = [t for t in WORK_TOKENS if t in src]
        hit = [t for t in toks if any(t in p for p in compiled_passages)]
        check("row %s claims exact primary wording for a source the companion does "
              "NOT label [via compilation]" % r["id"], not hit,
              "the companion cites %s inside a [via compilation] passage while this row "
              "claims PRIMARY_TEXT_EXACT — one citation cannot have two evidence accesses"
              % (hit[0] if hit else ""))
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
