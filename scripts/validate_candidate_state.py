#!/usr/bin/env python3
"""Candidate-state / pre-merge integrity validator (R7C, Decision 0026).

Deterministic, offline. Enforces the honest candidate/merged boundary so an Opus
candidate pass cannot present its own unreviewed work as merged:

  1. every candidate decision (one carrying a `pr:` field, i.e. 0020+) has status
     `proposed-candidate`, never `adopted-merged`;
  2. every candidate decision FILE carries the CANDIDATE label;
  3. the candidate overlay declares `merged: false`, `independent_signoff: false`,
     and the correct merged-base sha (main, R6);
  4. no candidate closure artifact (docs/project-closure/r7/|r7b/|r7c/) is
     classified merged/adopted in the historical-status index;
  5. the merged base lists only 0001-0019 (main has no 0020+).

Establishes no empirical or theological claim; an integrity gate only.
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
MAIN_R6_SHA = "43fee0f519e2f6984fb143c1e621c83382e71ec7"
FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def main():
    ds = yaml.safe_load(read("docs/decision-status.yaml"))
    decisions = ds["decisions"]

    # 1 + 2: candidate decisions are proposed-candidate and labeled
    for did, row in sorted(decisions.items()):
        is_candidate = "pr" in row
        if is_candidate:
            check("candidate decision %s is proposed-candidate (not adopted-merged)" % did,
                  row.get("status") == "proposed-candidate", repr(row.get("status")))
            ddir = os.path.join(ROOT, "docs", "decisions")
            fn = next((f for f in os.listdir(ddir) if f.startswith(did + "-")), None)
            btext = read("docs/decisions/" + fn) if fn else ""
            check("candidate decision %s file carries the CANDIDATE label" % did,
                  "OPUS CANDIDATE" in btext)
        else:
            # merged decisions must not be proposed-candidate
            check("merged decision %s is not proposed-candidate" % did,
                  row.get("status") != "proposed-candidate", repr(row.get("status")))

    # candidate range: every decision >= 0020 is candidate (carries pr); every
    # decision 0001-0019 is merged (no pr). Dynamic on the decision numbers present.
    for did, row in decisions.items():
        n = int(did)
        if n >= 20:
            check("decision %s (>=0020) is classified candidate (carries pr)" % did, "pr" in row)
        else:
            check("merged decision %s (<=0019) carries no pr field" % did, "pr" not in row)

    # 3: overlay integrity
    ov = yaml.safe_load(read("docs/project-closure/r7c/CANDIDATE-STATE.yaml"))
    check("overlay declares merged: false", ov.get("merged") is False)
    check("overlay declares no independent sign-off",
          ov.get("no_merge_status", {}).get("independent_signoff") is False)
    check("overlay merged-base sha is main R6", ov.get("merged_base", {}).get("sha") == MAIN_R6_SHA)
    check("overlay merged base lists only 0001-0019",
          ov.get("merged_base", {}).get("merged_decisions") == "0001-0019")

    # 4: closure artifacts are not marked merged/adopted in the historical index
    hist = yaml.safe_load(read("docs/project-closure/HISTORICAL-STATUS-INDEX.yaml"))
    rules = hist if isinstance(hist, list) else hist.get("rules", hist.get("entries", []))
    # the index is a top-level list in this repo; load robustly
    if isinstance(hist, dict) and "rules" not in hist and "entries" not in hist:
        # some indexes are a bare mapping/list; re-read as list
        rules = yaml.safe_load(read("docs/project-closure/HISTORICAL-STATUS-INDEX.yaml"))
    bad = []
    for r in (rules if isinstance(rules, list) else []):
        pref = str(r.get("prefix", ""))
        st = str(r.get("status", ""))
        if pref.startswith("docs/project-closure/r7") and st in ("merged", "adopted", "adopted-merged"):
            bad.append("%s=%s" % (pref, st))
    check("no R7/R7B/R7C closure artifact is marked merged/adopted", not bad, "; ".join(bad))

    # 6 (R7D, Decision 0029, audit B1/P1): the authoritative candidate overlay must
    # name the exact live PR-10 head and its candidate-decision set must NOT drift
    # from decision-status.yaml — so a STALE overlay (missing PR #10 / wrong head /
    # missing candidate decisions / omitted companion PDF) FAILS.
    PR10_HEAD = "3cce235f0e388ba78a093d43c879a2e73262938b"
    COMPANION_PDF = "artifacts/dynamic-orthing-noetic-learning-orthability-draft.pdf"
    ov2_text = read("docs/current-candidate-state.yaml")
    check("authoritative candidate overlay exists", bool(ov2_text))
    ov2 = yaml.safe_load(ov2_text) if ov2_text else {}
    check("candidate overlay declares merged: false", ov2.get("merged") is False)
    check("candidate overlay merged-base sha is main R6",
          ov2.get("merged_base", {}).get("sha") == MAIN_R6_SHA)
    chain = ov2.get("pr_chain", [])
    pr10 = next((p for p in chain if p.get("pr") == 10), None)
    check("candidate overlay names PR #10", pr10 is not None)
    check("candidate overlay names the exact live PR #10 head (not stale)",
          bool(pr10) and pr10.get("head") == PR10_HEAD, repr(pr10.get("head") if pr10 else None))
    # candidate-decision set == every decision carrying a `pr:` field (no drift)
    pr_decisions = {did for did, row in decisions.items() if "pr" in row}
    overlay_decisions = set(ov2.get("candidate_decisions", []))
    check("candidate overlay decision set matches decision-status (no drift)",
          overlay_decisions == pr_decisions,
          "overlay=%s status=%s" % (sorted(overlay_decisions), sorted(pr_decisions)))
    check("candidate overlay lists the companion PDF among candidate PDFs (B1)",
          COMPANION_PDF in ov2.get("candidate_pdfs", []))
    nms = ov2.get("no_merge_status", {})
    check("candidate overlay declares merged/signoff/ready all false",
          nms.get("merged") is False and nms.get("independent_signoff") is False
          and nms.get("ready_for_merge") is False)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
