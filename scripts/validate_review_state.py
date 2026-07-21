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

R7D_BASE = "e34d2cd56057766f8f656a4ff3486eb34dad607e"
R7E_HEAD_AT_OBSERVATION = "cbab14747835855d232448f648eefa1d4e36074e"
R7E_SOL_FINDING_IDS = {
    "R7E-SOL-F%03d" % n for n in range(1, 16)
}
R7E_PATHS = {
    "applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md",
    "artifacts/dynamic-orthing-noetic-learning-orthability-draft.pdf",
    "artifacts/dynamic-orthing-noetic-learning-orthability-draft.sources.json",
    "companion/DYNAMIC-ORTHABILITY-ARGUMENT-MAP.yaml",
    "companion/dynamic-orthing-noetic-learning-and-orthability.md",
    "docs/current-state.yaml",
    "docs/project-closure/HISTORICAL-STATUS-INDEX.yaml",
    "docs/project-closure/r7e/AUTONOMOUS-R7E-STATE.json",
    "docs/project-closure/r7e/ORTHING-CANDIDATE-BACKLOG.md",
    "docs/provenance/RELEASE-MANIFEST.sha256",
}


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
                      "review-discharged notice" % did,
                      "review discharged" in t or "review-discharged" in t)

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

    # 6a. R7E Sol independent-review control plane (Decision 0034). These
    # records are current-candidate evidence only: never sign-off or merge
    # readiness. Exact SHAs are timestamped observations, not HEAD contracts.
    check("R7E-Sol control-plane prefix is current-candidate",
          classify("docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json")
          == "current-candidate")

    sol = json.loads(read(
        "docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json") or "{}")
    obs = sol.get("r7e_observation") or {}
    check("R7E-Sol state records the exact R7D base observation",
          obs.get("base") == R7D_BASE, repr(obs.get("base")))
    check("R7E-Sol state records the exact R7E head-at-observation",
          obs.get("head_at_observation") == R7E_HEAD_AT_OBSERVATION,
          repr(obs.get("head_at_observation")))
    gate = sol.get("model_gate") or {}
    check("R7E-Sol state records the controller-confirmed gpt-5.6-sol gate",
          gate.get("required") == "gpt-5.6-sol"
          and gate.get("selected") == "gpt-5.6-sol"
          and gate.get("evidence") == "controller-confirmed-agent-model-selection"
          and gate.get("environment_variable_observation") is False)
    baseline = sol.get("baseline") or {}
    check("R7E-Sol baseline accounts for 53 direct plus three unchanged UTF-8 reruns",
          baseline.get("logical_validations") == 56
          and baseline.get("passing") == 56
          and baseline.get("direct_passes") == 53
          and baseline.get("utf8_unchanged_reruns") == 3
          and baseline.get("validator_logic_failures") == 0)
    pdf = baseline.get("pdf_rebuild") or {}
    check("R7E-Sol baseline records six byte-identical PDF rebuilds",
          pdf.get("artifacts") == 6 and pdf.get("byte_identical") == 6)
    check("R7E-Sol state refuses sign-off, readiness, and merge claims",
          sol.get("independent_signoff") is False
          and sol.get("ready_for_merge") is False
          and sol.get("merged") is False)

    matrix = yaml.safe_load(read(
        "docs/project-closure/r7e-sol/R7E-INDEPENDENT-FINDING-MATRIX.yaml")) or {}
    findings = matrix.get("findings") or []
    finding_ids = [row.get("id") for row in findings]
    check("R7E-Sol finding matrix has the complete unique finding-ID set",
          set(finding_ids) == R7E_SOL_FINDING_IDS
          and len(finding_ids) == len(set(finding_ids)), repr(finding_ids))
    allowed_findings = {"reproduced", "refuted", "partially-reproduced", "unverified"}
    allowed_terminal = {"open", "resolved", "deferred", "blocked"}
    malformed_findings = [
        str(row.get("id")) for row in findings
        if row.get("disposition") not in allowed_findings
        or not row.get("evidence")
        or not str(row.get("severity", "")).strip()
        or not isinstance(row.get("repair_task"), int)
        or row.get("terminal_status") not in allowed_terminal
    ]
    check("every R7E-Sol finding has disposition, evidence, severity, repair task, and terminal status",
          not malformed_findings, repr(malformed_findings))

    hunk_text = read("docs/project-closure/r7e-sol/R7E-HUNK-DISPOSITION.md")
    hunk_rows = re.findall(
        r"^\|\s*`([^`]+)`\s*\|\s*`?(keep|revise|drop|provenance-only)`?\s*\|",
        hunk_text, re.M)
    hunk_paths = [path for path, _disposition in hunk_rows]
    check("all ten R7E paths have exactly one allowed hunk disposition",
          set(hunk_paths) == R7E_PATHS and len(hunk_paths) == len(R7E_PATHS),
          repr(hunk_paths))
    check("R7E PDF and release manifest are provenance-only",
          ("artifacts/dynamic-orthing-noetic-learning-orthability-draft.pdf",
           "provenance-only") in hunk_rows
          and ("docs/provenance/RELEASE-MANIFEST.sha256", "provenance-only")
          in hunk_rows)

    d34 = (reg.get("decisions") or {}).get("0034") or {}
    check("Decision 0034 is proposed-candidate on PR 12",
          d34.get("status") == "proposed-candidate" and d34.get("pr") == 12)
    d34_text = read("docs/decisions/0034-r7e-sol-independent-repair-contract.md")
    check("Decision 0034 carries the Sol candidate and no-self-promotion boundary",
          "SOL CANDIDATE" in d34_text
          and "Status:** proposed-candidate" in d34_text
          and "cannot self-promote" in d34_text)

    # 7. discharged owner action
    t = read("docs/project-closure/r4/R4-UNAVOIDABLE-OWNER-ACTIONS.md")
    check("R4 owner-actions snapshot carries the item-7 discharge banner",
          "HISTORICAL SNAPSHOT" in t and "discharged" in t)

    # 8. merged-state record honesty
    ms_path = str(rs.get("current_merge_verification", "")).replace(
        "FINAL-MERGED-VERIFICATION.md", "FINAL-MERGED-STATE.json")
    ms = json.loads(read(ms_path) or "{}")
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
