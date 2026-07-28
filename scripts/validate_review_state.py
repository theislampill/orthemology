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
  3. every CURRENT surface (STATUS, README, the five primary headers, and
     their generated publication-LaTeX owners) carries the authored
     header_wording;
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
import hashlib
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
    "clean_clone_verification": "docs/project-closure/r7e-sol/R7E-SOL-CLEAN-CLONE-VERIFICATION.md",
    "finding_matrix": "docs/project-closure/r7e-sol/R7E-INDEPENDENT-FINDING-MATRIX.yaml",
    "hunk_disposition": "docs/project-closure/r7e-sol/R7E-HUNK-DISPOSITION.md",
    "decision": "docs/decisions/0034-r7e-sol-independent-repair-contract.md",
}
R7E_REPRODUCTION_LINK_TARGETS = {
    "AUTONOMOUS-R7E-SOL-STATE.json",
    "R7E-SOL-CLEAN-CLONE-VERIFICATION.md",
    "R7E-INDEPENDENT-FINDING-MATRIX.yaml",
    "R7E-HUNK-DISPOSITION.md",
    "../../decisions/0034-r7e-sol-independent-repair-contract.md",
}
R7E_FINDING_ADJUDICATIONS = {
    "R7E-SOL-F001": ("reproduced", "blocker", 2, "resolved"),
    "R7E-SOL-F002": ("reproduced", "blocker", 3, "resolved"),
    "R7E-SOL-F003": ("reproduced", "blocker", 3, "resolved"),
    "R7E-SOL-F004": ("reproduced", "high", 7, "resolved"),
    "R7E-SOL-F005": ("reproduced", "blocker", 2, "resolved"),
    "R7E-SOL-F006": ("reproduced", "blocker", 8, "resolved"),
    "R7E-SOL-F007": ("reproduced", "blocker", 5, "resolved"),
    "R7E-SOL-F008": ("partially-reproduced", "high", 5, "resolved"),
    "R7E-SOL-F009": ("reproduced", "high", 7, "resolved"),
    "R7E-SOL-F010": ("reproduced", "high", 6, "resolved"),
    "R7E-SOL-F011": ("partially-reproduced", "high", 8, "resolved"),
    "R7E-SOL-F012": ("reproduced", "blocker", 8, "resolved"),
    "R7E-SOL-F013": ("reproduced", "blocker", 8, "resolved"),
    "R7E-SOL-F014": ("reproduced", "blocker", 10, "resolved"),
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
R7E_TASK15_REVIEWED_COMMIT = "b22d4351f4d3a76bc3f16b41704a470b4abb1aa5"
R7E_TASK16_MAIN_MERGE = "8db1630ab715b0931907c627be97b32399d6f4fc"
R7E_TASK16_MERGED_RECORD = (
    "docs/project-closure/r7e-sol/R7E-SOL-MERGED-MAIN-VERIFICATION.md")
R7E_TASK16_MERGED_RECORD_SHA256 = (
    "d75cf18da8f6ac68fa3b5f00038a360f9dc87de056494efcf459fb7da6a1e7a3")
R7E_TASK16_MERGES = [
    "e12cfbbf880b52c38f4064bb7ec6e4393705e319",
    "4d09fed5f2d2106fd5ecd9a79b1d13e6b9af32fc",
    "f4a4804101202c056a31f3d30f2ef931e1dcca2d",
    "2867f3510c343fea8c7fd6c37b8ad38ce5de83a6",
    "17f6783d5d5a39a90dee7b10573ef6bc3732ae5e",
    R7E_TASK16_MAIN_MERGE,
]
R7E_TASK16_RUNS = [
    30317000439, 30317471209, 30317917503, 30317919628,
    30318432384, 30318434266, 30318923898, 30318925662,
    30319389233, 30319391979, 30319878639, 30319880488,
    30320348878,
]
R7E_TASK16_PUBLIC_SURFACES = [
    "README.md",
    "STATUS.md",
    "TODO.md",
    "docs/current-state.yaml",
    "docs/project-closure/HISTORICAL-STATUS-INDEX.yaml",
    "docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json",
    "docs/project-closure/r7e-sol/R7E-HUNK-DISPOSITION.md",
    R7E_TASK16_MERGED_RECORD,
]
R7E_PROHIBITED_TERMS = [
    "ani" + "me",
    "Ghost" + " in the Shell",
    "Stand" + " Alone Complex",
    "Tachi" + "koma",
    "Fuchi" + "koma",
]
R7E_PROHIBITED_ACRONYM = "S" + "A" + "C"
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


def read_bytes(rel):
    p = os.path.join(ROOT, rel)
    return open(p, "rb").read() if os.path.exists(p) else b""


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


def task16_record_claim_issues(text):
    """Return narrow public-record promotion or self-attestation defects."""
    issues = []
    sentences = re.split(r"(?<=[.!?])(?:\s+|$)", text)
    record_subject = (
        r"\b(?:this|the)\s+(?:tracked\s+|merged-main\s+|verification\s+)?record\b")
    attestation_verb = (
        r"\b(?:verif(?:y|ies|ied)|validat(?:e|es|ed)|attest(?:s|ed)?|"
        r"certif(?:y|ies|ied)|authenticat(?:e|es|ed)|prove(?:s|d)?)\b")
    forbidden_object = (
        r"\b(?:itself|its\s+own\s+(?:commit|merge|contents?|validity|integrity)|"
        r"(?:its\s+)?containing(?:\s+follow-up)?\s+(?:commit|merge))\b")
    ar6_positive = (
        r"\b(?:approved|adopted|accepted|established|integrated|"
        r"repository-ready|promoted)\b")
    ar6_object = r"\b(?:theorem|proof|claim|result|work|repository\s+theory)\b"

    for sentence in sentences:
        if (
            re.search(record_subject, sentence, flags=re.IGNORECASE)
            and re.search(attestation_verb, sentence, flags=re.IGNORECASE)
            and re.search(forbidden_object, sentence, flags=re.IGNORECASE)
        ):
            issues.append("record claims self or containing-merge attestation")

        lowered = sentence.lower()
        has_ar6_promotion_shape = (
            "ar6" in lowered
            and "interrupt" in lowered
            and re.search(ar6_positive, sentence, flags=re.IGNORECASE)
            and re.search(ar6_object, sentence, flags=re.IGNORECASE)
        )
        negated = (
            "not_applied_not_approved" in lowered
            or re.search(
                r"\b(?:no|not|never)\b.{0,100}" + ar6_positive,
                sentence, flags=re.IGNORECASE)
        )
        if has_ar6_promotion_shape and not negated:
            issues.append("interrupted AR6 result is promoted")
    return issues


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

    # Generated publication sources, not a builder-owned status literal, are
    # the current PDF text owners. Require every primary document to map to an
    # artifact whose generated LaTeX preserves the authored review wording.
    profile = yaml.safe_load(read("docs/publication-profile.yaml"))
    artifact_by_source = {
        source: artifact.get("artifact_id")
        for artifact in profile.get("artifacts", [])
        for source in artifact.get("sources", [])
    }
    generated_status_text = []
    missing_generated_status = []
    for rel in primaries:
        artifact_id = artifact_by_source.get(rel)
        generated_rel = (
            "publication/latex/%s/main.tex" % artifact_id
            if artifact_id
            else ""
        )
        text = read(generated_rel) if generated_rel else ""
        generated_status_text.append(text)
        if wording not in text:
            missing_generated_status.append(rel)
    lines = "\n".join(generated_status_text)
    check("generated PDF sources carry the review-state wording",
          not missing_generated_status, repr(missing_generated_status))
    for phrase in BANNED_CURRENT:
        check("generated PDF sources free of stale phrase %r" % phrase,
              phrase not in lines)

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

    # 6a. R7E Sol independent-review and merged-main control plane (Decision
    # 0034). Historical topology remains a timestamped observation; the final
    # merge record follows the non-self-referential protected-follow-up pattern.
    check("R7E-Sol control-plane prefix is current after protected integration",
          classify("docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json")
          == "current")
    integrated_prefixes = [
        "docs/project-closure/r7e/",
        "docs/project-closure/r7d/",
        "docs/project-closure/r7c/",
        "docs/project-closure/r7b/",
        "docs/project-closure/r7/",
    ]
    check("integrated candidate-era closure records are historical snapshots",
          all(classify(prefix + "AUTONOMOUS-STATE") == "historical-snapshot"
              for prefix in integrated_prefixes))
    stale_integrated_notes = [
        rule for rule in idx["rules"]
        if rule.get("prefix") in integrated_prefixes
        and (
            rule.get("status") != "historical-snapshot"
            or "protected-main" not in str(rule.get("note", "")).lower()
            or "unmerged" in str(rule.get("note", "")).lower()
            or "never merged" in str(rule.get("note", "")).lower()
        )
    ]
    check("integrated candidate-era classifications contain no false live topology",
          not stale_integrated_notes, repr(stale_integrated_notes))

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
    check("R7E-Sol state records completed integration without follow-up self-attestation",
          sol.get("independent_signoff") is True
          and sol.get("ready_for_merge") is False
          and sol.get("merged") is True)
    task15 = sol.get("task15_verification") or {}
    check("R7E-Sol Task 15 binds the approved exact remote candidate",
          task15.get("candidate_commit")
          == "ad57371b8ef88c313f9b92c43c7618500337e0ed"
          and task15.get("remote_head")
          == "ad57371b8ef88c313f9b92c43c7618500337e0ed"
          and task15.get("independent_review_verdict") == "APPROVED")
    check("R7E-Sol Task 15 binds exact-SHA CI and clean-clone validation",
          task15.get("github_actions_run") == 30313374447
          and task15.get("github_actions_conclusion") == "SUCCESS"
          and task15.get("workflow_command_count") == 71
          and task15.get("supplemental_command_count") == 8
          and task15.get("clean_clone_head")
          == "ad57371b8ef88c313f9b92c43c7618500337e0ed"
          and task15.get("clean_clone_status_porcelain") == "")
    check("R7E-Sol Task 15 accounts for deterministic all-page PDF QA",
          task15.get("pdf_artifacts") == 6
          and task15.get("pdf_pages") == 61
          and task15.get("raster_passes") == 2
          and task15.get("raster_hash_lists_identical") is True
          and task15.get("visually_inspected_pages") == 61
          and task15.get("prohibited_semantic_hits") == 0)
    task16 = sol.get("task16_verification") or {}
    task16_record = read(R7E_TASK16_MERGED_RECORD)
    task16_record_sha256 = hashlib.sha256(
        read_bytes(R7E_TASK16_MERGED_RECORD)).hexdigest()
    check("R7E-Sol Task 16 merged-main record matches the immutable byte contract",
          task16_record_sha256 == R7E_TASK16_MERGED_RECORD_SHA256,
          task16_record_sha256)
    check("R7E-Sol Task 16 binds the reviewed candidate and protected-main merge",
          task16.get("reviewed_commit") == R7E_TASK15_REVIEWED_COMMIT
          and task16.get("main_merge_commit") == R7E_TASK16_MAIN_MERGE
          and task16.get("merge_commits") == R7E_TASK16_MERGES
          and R7E_TASK15_REVIEWED_COMMIT in task16_record
          and R7E_TASK16_MAIN_MERGE in task16_record)
    cascade_labels = ["PR #13", "PR #12", "PR #11", "PR #10", "PR #9", "PR #8"]
    check("R7E-Sol Task 16 record binds every intermediate merge to its PR",
          all(re.search(
              r"\|\s*" + re.escape(label) + r"[^|]*\|\s*`"
              + re.escape(commit) + r"`\s*\|",
              task16_record)
              for label, commit in zip(cascade_labels, R7E_TASK16_MERGES)))
    check("R7E-Sol Task 16 binds all successful exact-SHA runs",
          task16.get("github_actions_runs") == R7E_TASK16_RUNS
          and task16.get("github_actions_conclusion") == "SUCCESS"
          and all(str(run) in task16_record for run in R7E_TASK16_RUNS))
    check("R7E-Sol Task 16 records the complete fresh-main proof",
          task16.get("workflow_command_count") == 71
          and task16.get("supplemental_command_count") == 8
          and task16.get("pdf_pages") == 61
          and task16.get("visually_inspected_pages") == 61
          and task16.get("visual_defects") == 0
          and task16.get("tracked_paths") == 707
          and task16.get("release_manifest_entries") == 706
          and task16.get("prohibited_semantic_hits") == 0
          and task16.get("ar6_records") == 1329
          and task16.get("ar6_unclassified_counters") == 0)
    check("R7E-Sol Task 16 preserves the non-self-referential follow-up boundary",
          task16.get("followup_record_self_hashed") is False
          and task16.get("followup_protected_readback") == "pending"
          and "never self-hashed" in task16_record
          and "protected readback" in task16_record
          and not re.search(
              r"containing.{0,100}\b[0-9a-f]{40}\b",
              task16_record, flags=re.IGNORECASE | re.DOTALL))
    record_claim_issues = task16_record_claim_issues(task16_record)
    check("R7E-Sol Task 16 record rejects promotion and self-attestation claims",
          not record_claim_issues, repr(record_claim_issues))
    check("R7E-Sol Task 16 preserves AR6 interruption and non-application",
          task16.get("ar6_status") == "INTERRUPTED_IN_PROGRESS"
          and task16.get("ar6_integration_status") == "NOT_APPLIED_NOT_APPROVED")
    prohibited_hits = []
    for path in R7E_TASK16_PUBLIC_SURFACES:
        text = read(path)
        for term in R7E_PROHIBITED_TERMS:
            if re.search(re.escape(term), text, flags=re.IGNORECASE):
                prohibited_hits.append(path + ":" + term)
        if re.search(
                r"(?<![A-Za-z0-9])" + R7E_PROHIBITED_ACRONYM
                + r"(?![A-Za-z0-9])", text):
            prohibited_hits.append(path + ":prohibited-acronym")
    check("R7E-Sol Task 16 public surfaces use neutral terminology",
          not prohibited_hits, repr(prohibited_hits))
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
    check("R7E-Sol finding adjudications exactly match the Task 15 boundary",
          actual_adjudications == R7E_FINDING_ADJUDICATIONS,
          repr(actual_adjudications))
    findings_by_id = {str(row.get("id")): row for row in findings}
    check("R7E-Sol F001 retains exact review evidence before resolution evidence",
          findings_by_id.get("R7E-SOL-F001", {}).get("evidence", [])[:2]
          == R7E_F001_EVIDENCE,
          repr(findings_by_id.get("R7E-SOL-F001", {}).get("evidence")))
    check("R7E-Sol F011 retains exact source evidence before resolution evidence",
          findings_by_id.get("R7E-SOL-F011", {}).get("evidence", [])[:2]
          == R7E_F011_EVIDENCE,
          repr(findings_by_id.get("R7E-SOL-F011", {}).get("evidence")))
    resolved_findings = {
        fid for fid, values in actual_adjudications.items()
        if values[3] == "resolved"
    }
    check("all fifteen R7E-Sol findings are terminally resolved",
          resolved_findings == R7E_SOL_FINDING_IDS,
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
    check("preserved R7E provenance inputs are kept byte-identical",
          ("docs/project-closure/r7e/AUTONOMOUS-R7E-STATE.json", "keep")
          in hunk_rows
          and ("docs/project-closure/r7e/ORTHING-CANDIDATE-BACKLOG.md", "keep")
          in hunk_rows)
    check("R7E hunk disposition records Task 16 integration and follow-up boundary",
          "TASK 16 PROTECTED CASCADE AND FRESH-MAIN PROOF COMPLETE" in hunk_text
          and "FOLLOW-UP PROTECTED READBACK PENDING" in hunk_text)
    check("R7E hunk disposition contains no stale Task 16 future tense",
          "must be regenerated after each Task 16 merge" not in hunk_text
          and "Task 16 must regenerate it last" not in hunk_text
          and "Correctly classifies R7E as current-candidate" not in hunk_text)

    todo = read("TODO.md")
    stale_tasks = []
    for task_number in range(1, 11):
        match = re.search(
            r"^### Task %d\b(?P<body>.*?)(?=^### Task \d+\b|\Z)"
            % task_number, todo, flags=re.MULTILINE | re.DOTALL)
        body = match.group("body") if match else ""
        if (
            not body
            or "integrated to protected `main`" not in body
            or "not merged to `main`" in body
            or "inherits Tasks 15–16 integration gates" in body
        ):
            stale_tasks.append(task_number)
    check("TODO Tasks 1-10 record completed protected-main integration",
          not stale_tasks, repr(stale_tasks))
    task16_match = re.search(
        r"^### Task 16\b(?P<body>.*?)(?=^### Task \d+\b|\Z)",
        todo, flags=re.MULTILINE | re.DOTALL)
    task16_body = task16_match.group("body") if task16_match else ""
    check("TODO Task 16 remains completed through protected-main verification",
          bool(task16_body)
          and "Status: completed through protected-main merge and fresh-main verification"
          in task16_body
          and "unfinished; protected cascade pending" not in task16_body)
    readme = read("README.md")
    check("README records current protected-main truth without adoption promotion",
          R7E_TASK16_MAIN_MERGE in readme
          and "R7E-SOL-MERGED-MAIN-VERIFICATION.md" in readme
          and "Decisions 0020–0036 are `proposed-candidate` in the unmerged PR chain"
          not in readme
          and "No PR is merged" not in readme
          and "Git integration does not establish" in readme)
    status_text = read("STATUS.md")
    check("STATUS points to current merged-main verification without adoption promotion",
          "docs/project-closure/r7e-sol/R7E-SOL-MERGED-MAIN-VERIFICATION.md"
          in status_text
          and "Git integration is **not** theory or terminology adoption"
          in status_text)

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
    mv_path = str(rs.get("current_merge_verification", ""))
    mv = read(mv_path)
    if mv_path.endswith("R7E-SOL-MERGED-MAIN-VERIFICATION.md"):
        check("R7E-Sol merged-main record names the earlier protected merge",
              R7E_TASK16_MAIN_MERGE in mv)
        check("R7E-Sol merged-main record is explicitly non-self-referential",
              "never self-hashed" in mv
              and "containing follow-up commit and merge live" in mv
              and "ordinary Git history" in mv)
    else:
        ms_path = mv_path.replace(
            "FINAL-MERGED-VERIFICATION.md", "FINAL-MERGED-STATE.json")
        ms = json.loads(read(ms_path) or "{}")
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
