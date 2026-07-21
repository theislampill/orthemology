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
from datetime import datetime, timezone

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
R7E_TOPOLOGY_AT_OBSERVATION = [
    {
        "pr": 8,
        "base_branch": "main",
        "base_head": "43fee0f519e2f6984fb143c1e621c83382e71ec7",
        "head_branch": "closure/r7-noetic-application-experiment-validity",
        "head_at_observation": "b0538601913c8234511a1f1131a58eb23a4a0dc4",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    {
        "pr": 9,
        "base_branch": "closure/r7-noetic-application-experiment-validity",
        "base_head": "b0538601913c8234511a1f1131a58eb23a4a0dc4",
        "head_branch": "candidate/r7b-deep-noetic-latent-math",
        "head_at_observation": "86b8bbdddf35ac1e45748279bac05e5a2d4ed85e",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    {
        "pr": 10,
        "base_branch": "candidate/r7b-deep-noetic-latent-math",
        "base_head": "86b8bbdddf35ac1e45748279bac05e5a2d4ed85e",
        "head_branch": "candidate/r7c-full-math-multitarget-noetic-dynamics",
        "head_at_observation": "3cce235f0e388ba78a093d43c879a2e73262938b",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    {
        "pr": 11,
        "base_branch": "candidate/r7c-full-math-multitarget-noetic-dynamics",
        "base_head": "3cce235f0e388ba78a093d43c879a2e73262938b",
        "head_branch": "candidate/r7d-final-semantic-math-noetic-integration",
        "head_at_observation": "e34d2cd56057766f8f656a4ff3486eb34dad607e",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    {
        "pr": 12,
        "base_branch": "candidate/r7d-final-semantic-math-noetic-integration",
        "base_head": "e34d2cd56057766f8f656a4ff3486eb34dad607e",
        "head_branch": "candidate/r7e-orthing-supplementation",
        "head_at_observation": "cbab14747835855d232448f648eefa1d4e36074e",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
]
R7E_CONTROL_PLANE = {
    "reproduction": "docs/project-closure/r7e-sol/R7E-SOL-READONLY-REPRODUCTION.md",
    "finding_matrix": "docs/project-closure/r7e-sol/R7E-INDEPENDENT-FINDING-MATRIX.yaml",
    "hunk_disposition": "docs/project-closure/r7e-sol/R7E-HUNK-DISPOSITION.md",
    "decision": "docs/decisions/0034-r7e-sol-independent-repair-contract.md",
}
R7E_REPRODUCTION_LINK_TARGETS = {
    "AUTONOMOUS-R7E-SOL-STATE.json",
    "R7E-INDEPENDENT-FINDING-MATRIX.yaml",
    "R7E-HUNK-DISPOSITION.md",
    "../../decisions/0034-r7e-sol-independent-repair-contract.md",
}
R7E_FINDING_ADJUDICATIONS = {
    "R7E-SOL-F001": ("reproduced", "blocker", 2, "open"),
    "R7E-SOL-F002": ("reproduced", "blocker", 3, "open"),
    "R7E-SOL-F003": ("reproduced", "blocker", 3, "open"),
    "R7E-SOL-F004": ("reproduced", "high", 7, "open"),
    "R7E-SOL-F005": ("reproduced", "blocker", 2, "open"),
    "R7E-SOL-F006": ("reproduced", "blocker", 8, "open"),
    "R7E-SOL-F007": ("reproduced", "blocker", 5, "open"),
    "R7E-SOL-F008": ("partially-reproduced", "high", 5, "open"),
    "R7E-SOL-F009": ("reproduced", "high", 7, "open"),
    "R7E-SOL-F010": ("reproduced", "high", 6, "open"),
    "R7E-SOL-F011": ("partially-reproduced", "high", 8, "open"),
    "R7E-SOL-F012": ("reproduced", "blocker", 8, "open"),
    "R7E-SOL-F013": ("reproduced", "blocker", 8, "open"),
    "R7E-SOL-F014": ("reproduced", "blocker", 10, "open"),
    "R7E-SOL-F015": ("refuted", "historical-high", 12, "resolved"),
}
R7E_F001_EVIDENCE = [
    "docs/current-candidate-state.yaml stops at a placeholder R7D child and does not name exact PR 11 or PR 12 observations",
    "scripts/validate_candidate_state.py passes the stale natural state",
]
R7E_F011_EVIDENCE = [
    "cbab14747835855d232448f648eefa1d4e36074e:companion/dynamic-orthing-noetic-learning-and-orthability.md:113 and :235 use Pi as the reachability policy/action-sequence argument, while cbab14747835855d232448f648eefa1d4e36074e:docs/notation-registry.yaml:24-26 fixes Pi_A as the complete-profile space; the glyph/role reuse is a notation collision",
    "cbab14747835855d232448f648eefa1d4e36074e:companion/dynamic-orthing-noetic-learning-and-orthability.md:237-238 says correction tracks an objective gradient even though :125-127 disclaims a literal scalar gradient; the objective-gradient formulation overstates the typed contract",
]
R7E_DECISION_BOUNDARY = {
    "schema": "orthemology-decision-candidate-boundary-v1",
    "decision": "0034",
    "status": "proposed-candidate",
    "pr": 12,
    "scope": "review-state-accounting-only",
    "preserves_decisions": ["0001-0022"],
    "reopens": [],
    "independent_signoff": False,
    "ready_for_merge": False,
    "merged": False,
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


def valid_utc_timestamp(value):
    if not isinstance(value, str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def decision_candidate_boundary(text):
    match = re.search(
        r"<!-- decision-candidate-boundary:start -->\s*```yaml\s*(.*?)\s*```\s*"
        r"<!-- decision-candidate-boundary:end -->",
        text,
        re.S,
    )
    return yaml.safe_load(match.group(1)) if match else {}


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
    check("R7E-Sol state records a valid UTC observation timestamp",
          valid_utc_timestamp(sol.get("observed_at_utc")),
          repr(sol.get("observed_at_utc")))
    obs = sol.get("r7e_observation") or {}
    check("R7E-Sol state records the exact R7D base observation",
          obs.get("base") == R7D_BASE, repr(obs.get("base")))
    check("R7E-Sol state records the exact R7E head-at-observation",
          obs.get("head_at_observation") == R7E_HEAD_AT_OBSERVATION,
          repr(obs.get("head_at_observation")))
    check("R7E-Sol state marks the R7E observation as non-timeless",
          obs.get("timeless_state") is False,
          repr(obs.get("timeless_state")))
    check("R7E-Sol state records the exact PR 8-12 topology observation",
          sol.get("topology_at_observation") == R7E_TOPOLOGY_AT_OBSERVATION,
          repr(sol.get("topology_at_observation")))
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
    control_plane = sol.get("control_plane") or {}
    check("R7E-Sol state records the exact control-plane links",
          control_plane == R7E_CONTROL_PLANE, repr(control_plane))
    check("every R7E-Sol state control-plane link resolves",
          all(bool(read(path)) for path in R7E_CONTROL_PLANE.values()))
    reproduction = read(R7E_CONTROL_PLANE["reproduction"])
    reproduction_links = set(re.findall(r"\]\(([^)]+)\)", reproduction))
    check("R7E-Sol reproduction links every control-plane artifact",
          R7E_REPRODUCTION_LINK_TARGETS <= reproduction_links,
          repr(sorted(reproduction_links)))

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
    actual_adjudications = {
        str(row.get("id")): (
            row.get("disposition"),
            row.get("severity"),
            row.get("repair_task"),
            row.get("terminal_status"),
        )
        for row in findings
    }
    check("R7E-Sol finding adjudications exactly match the Task 1 boundary",
          actual_adjudications == R7E_FINDING_ADJUDICATIONS,
          repr(actual_adjudications))
    findings_by_id = {str(row.get("id")): row for row in findings}
    check("R7E-Sol F001 retains exact review evidence",
          findings_by_id.get("R7E-SOL-F001", {}).get("evidence")
          == R7E_F001_EVIDENCE,
          repr(findings_by_id.get("R7E-SOL-F001", {}).get("evidence")))
    check("R7E-Sol F011 uses only exact current-source evidence",
          findings_by_id.get("R7E-SOL-F011", {}).get("evidence")
          == R7E_F011_EVIDENCE,
          repr(findings_by_id.get("R7E-SOL-F011", {}).get("evidence")))
    resolved_findings = {
        fid for fid, values in actual_adjudications.items()
        if values[3] == "resolved"
    }
    check("R7E-Sol F001-F014 remain open and F015 alone is resolved",
          resolved_findings == {"R7E-SOL-F015"}
          and all(actual_adjudications.get(
              "R7E-SOL-F%03d" % n, (None,) * 4)[3] == "open"
              for n in range(1, 15)),
          repr(sorted(resolved_findings)))

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
    d34_boundary = decision_candidate_boundary(d34_text)
    check("Decision 0034 carries the exact structured candidate boundary",
          d34_boundary == R7E_DECISION_BOUNDARY, repr(d34_boundary))

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
