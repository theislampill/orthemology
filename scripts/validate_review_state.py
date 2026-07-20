#!/usr/bin/env python3
"""Review-state / historical-supersession validator (Decision 0016, R5).

Guards the class the R4 post-merge audit found: a completed review and merge
whose review-state surfaces still said "candidate pending independent review",
with every validator green — a false current-state claim surviving CI because
no check owned those surfaces. Deterministic, offline.

Checks:
  1. authored.review_state exists with the full field set; status from a
     closed vocabulary; no commit hash inside the block (Decision 0014);
  2. the sign-off, merge-verification, and historical-index paths resolve;
  3. every CURRENT surface (STATUS, README, the five primary headers, the PDF
     status lines in build_pdfs.py) carries the authored header_wording;
  4. no current surface carries a banned stale phrase;
  5. a decision whose registry status is adopted may say "requiring
     independent review" only alongside a dated "review discharged" notice;
  6. every file under docs/project-closure/ is classified by the historical
     index (path overrides first, then prefix rules); the sign-off is
     classified current-signoff; the merge-verification record is current;
     the pre-merge fresh-review state JSON is a historical snapshot;
  7. the superseded R4 owner-actions snapshot carries its discharge banner;
  8. the merged-state record is either explicitly PROVISIONAL, or — once
     provisional is false — complete (no PENDING placeholders, all r5_merge
     fields non-null).
"""
import io
import json
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

BANNED_CURRENT = [
    "candidate revision pending independent review",
    "REQUIRES INDEPENDENT REVIEW",
    "not independently signed off",
]

REVIEW_STATE_VOCAB = {"fresh-session-review-completed"}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def main():
    state = yaml.safe_load(read("docs/current-state.yaml"))
    a = state["authored"]

    # 1. review_state contract
    rs = a.get("review_state") or {}
    required = ["status", "scope", "current_signoff", "current_merge_verification",
                "historical_status_index", "empirical_validation",
                "terminology_adoption", "header_wording"]
    missing = [k for k in required if not str(rs.get(k, "")).strip()]
    check("review_state block carries the full field set", not missing, str(missing))
    check("review_state.status is in the closed vocabulary",
          rs.get("status") in REVIEW_STATE_VOCAB, repr(rs.get("status")))
    check("review_state.scope states it is not external peer review",
          "not external" in str(rs.get("scope", "")))
    blob = yaml.safe_dump(rs)
    check("review_state contains no commit hash (Decision 0014: no HEAD in a "
          "tracked equality contract)", not re.search(r"\b[0-9a-f]{40}\b", blob))

    # 2. paths resolve
    for key in ("current_signoff", "current_merge_verification", "historical_status_index"):
        rel = str(rs.get(key, ""))
        check("review_state.%s path resolves" % key,
              rel and os.path.exists(os.path.join(ROOT, rel)), rel)

    # 3-4. current surfaces: required wording present, banned phrases absent
    wording = str(rs.get("header_wording", ""))
    primaries = list(a.get("primary_documents", {}).values())
    surfaces = ["STATUS.md", "README.md"] + primaries
    for rel in surfaces:
        text = read(rel)
        head = "\n".join(text.split("\n")[:16]) if rel in primaries else text
        check("%s carries the authored review-state wording" % rel,
              wording in head, "missing: %r" % wording)
    for rel in ["VERSION", "STATUS.md", "README.md"] + primaries:
        text = read(rel)
        for phrase in BANNED_CURRENT:
            check("%s free of stale phrase %r" % (rel, phrase), phrase not in text)

    # PDF status page: the STATUS_LINES literal in build_pdfs.py
    bp = read("scripts/build_pdfs.py")
    m = re.search(r"STATUS_LINES\s*=\s*\[(.*?)\]", bp, re.S)
    lines = " ".join(re.findall(r'"([^"]*)"', m.group(1))) if m else ""
    check("PDF status lines carry the review-state wording",
          "fresh-session repository review completed" in lines
          and "not external human peer review" in lines, lines[:120])
    for phrase in BANNED_CURRENT:
        check("PDF status lines free of stale phrase %r" % phrase, phrase not in lines)

    # 5. decision headers vs registry
    reg = yaml.safe_load(read("docs/decision-status.yaml"))
    for did, row in sorted(reg["decisions"].items()):
        if row.get("status", "").startswith("adopted"):
            fns = [f for f in os.listdir(os.path.join(ROOT, "docs", "decisions"))
                   if f.startswith(did)]
            if not fns:
                continue
            t = read("docs/decisions/" + fns[0])
            if "requiring independent review" in t:
                check("decision %s pairs its historical candidate wording with a "
                      "review-discharged notice" % did, "review discharged" in t)

    # 6. historical index coverage + classifications
    idx = yaml.safe_load(read("docs/project-closure/HISTORICAL-STATUS-INDEX.yaml"))
    path_rules = {r["path"]: r for r in idx["rules"] if "path" in r}
    prefix_rules = [r for r in idx["rules"] if "prefix" in r]

    def classify(rel):
        if rel in path_rules:
            return path_rules[rel]["status"]
        for r in prefix_rules:
            if rel.startswith(r["prefix"]):
                return r["status"]
        return None

    unmatched = []
    croot = os.path.join(ROOT, "docs", "project-closure")
    for base, _dirs, fns in os.walk(croot):
        for fn in fns:
            rel = os.path.relpath(os.path.join(base, fn), ROOT).replace("\\", "/")
            if classify(rel) is None:
                unmatched.append(rel)
    check("every project-closure artifact is classified by the historical index",
          not unmatched, str(unmatched[:5]))
    check("declared statuses come from the index's own vocabulary",
          all(r["status"] in idx["statuses"] for r in idx["rules"]))
    check("the current sign-off is classified current-signoff",
          classify(str(rs.get("current_signoff"))) == "current-signoff")
    check("the merge-verification record is classified current",
          classify(str(rs.get("current_merge_verification"))) == "current")
    check("the pre-merge fresh-review state JSON is a historical snapshot",
          classify("docs/project-closure/r4-fresh-fable-review/AUTONOMOUS-REVIEW-STATE.json")
          == "historical-snapshot")

    # 7. discharged owner action
    t = read("docs/project-closure/r4/R4-UNAVOIDABLE-OWNER-ACTIONS.md")
    check("R4 owner-actions snapshot carries the item-7 discharge banner",
          "HISTORICAL SNAPSHOT" in t and "discharged" in t)

    # 8. merged-state record honesty
    ms = json.loads(read("docs/project-closure/r5/FINAL-MERGED-STATE.json") or "{}")
    mv = read(str(rs.get("current_merge_verification")))
    if ms.get("provisional") is True:
        check("provisional merged-state record is labeled PROVISIONAL in the md",
              "PROVISIONAL" in mv)
    else:
        check("finalized merge-verification md contains no PENDING placeholder",
              "PENDING" not in mv)
        r5m = ms.get("r5_merge") or {}
        empty = [k for k, v in r5m.items() if v in (None, "")]
        check("finalized merged-state record has no empty r5_merge field",
              not empty, str(empty))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
