#!/usr/bin/env python3
"""Generate the complete offline R7 candidate-state overlay.

The frozen input is a timestamped observation, not a live GitHub query.  The
tracked output deliberately records ``head_at_observation`` rather than a
timeless branch head, because a tracked file cannot name the commit containing
itself as a convergent leaf-head invariant.
"""
import argparse
import copy
import io
import json
import os
import re
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_REL = "docs/project-closure/r7e-sol/CANDIDATE-TOPOLOGY-INPUT.yaml"
OUTPUT_REL = "docs/current-candidate-state.yaml"
INPUT_PATH = os.path.join(ROOT, *INPUT_REL.split("/"))
OUTPUT_PATH = os.path.join(ROOT, *OUTPUT_REL.split("/"))
TOPOLOGY_SCHEMA = os.path.join(ROOT, "schemas", "candidate-topology.schema.json")
OVERLAY_SCHEMA = os.path.join(ROOT, "schemas", "candidate-overlay.schema.json")
DECISIONS_PATH = os.path.join(ROOT, "docs", "decision-status.yaml")

REQUIRED_PRS = [8, 9, 10, 11, 12]
REQUIRED_MERGE_ORDER = [12, 11, 10, 9, 8]
REQUIRED_OBSERVED_AT = "2026-07-21T18:10:22Z"
REQUIRED_OBSERVATION_SOURCE = (
    "Frozen from docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json after "
    "the verified read-only GitHub PR observation and local Git object comparison."
)
REQUIRED_CANDIDATE_DOCUMENTS = {
    "applications": [
        "applications/daee-epistemics/",
        "applications/latent-state-orthing/",
        "applications/agentic-runtime/",
    ],
    "companions": ["companion/dynamic-orthing-noetic-learning-and-orthability.md"],
    "architecture": [
        "docs/architecture/ORTHEMOLOGY-LAYER-MAP.md",
        "docs/architecture/ORTHEMOLOGY-LAYER-MAP.yaml",
    ],
    "closure": [
        "docs/project-closure/r7/",
        "docs/project-closure/r7b/",
        "docs/project-closure/r7c/",
        "docs/project-closure/r7d/",
        "docs/project-closure/r7e/",
        "docs/project-closure/r7e-sol/",
    ],
}
REQUIRED_CANDIDATE_PDFS = [
    "artifacts/notation-gallery.pdf",
    "artifacts/dynamic-orthing-noetic-learning-orthability-draft.pdf",
]
REQUIRED_REVIEW_PROVENANCE = {
    "layer": "independent-review",
    "model": "gpt-5.6-sol",
    "statement": (
        "Controller-confirmed Sol review provenance; separate from the historical "
        "candidate implementation provenance."
    ),
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_TOPOLOGY = {
    8: {
        "revision": "R7",
        "base_branch": "main",
        "base_head_at_observation": "43fee0f519e2f6984fb143c1e621c83382e71ec7",
        "head_branch": "closure/r7-noetic-application-experiment-validity",
        "head_at_observation": "b0538601913c8234511a1f1131a58eb23a4a0dc4",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    9: {
        "revision": "R7B",
        "base_branch": "closure/r7-noetic-application-experiment-validity",
        "base_head_at_observation": "b0538601913c8234511a1f1131a58eb23a4a0dc4",
        "head_branch": "candidate/r7b-deep-noetic-latent-math",
        "head_at_observation": "86b8bbdddf35ac1e45748279bac05e5a2d4ed85e",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    10: {
        "revision": "R7C",
        "base_branch": "candidate/r7b-deep-noetic-latent-math",
        "base_head_at_observation": "86b8bbdddf35ac1e45748279bac05e5a2d4ed85e",
        "head_branch": "candidate/r7c-full-math-multitarget-noetic-dynamics",
        "head_at_observation": "3cce235f0e388ba78a093d43c879a2e73262938b",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    11: {
        "revision": "R7D",
        "base_branch": "candidate/r7c-full-math-multitarget-noetic-dynamics",
        "base_head_at_observation": "3cce235f0e388ba78a093d43c879a2e73262938b",
        "head_branch": "candidate/r7d-final-semantic-math-noetic-integration",
        "head_at_observation": "e34d2cd56057766f8f656a4ff3486eb34dad607e",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    12: {
        "revision": "R7E",
        "base_branch": "candidate/r7d-final-semantic-math-noetic-integration",
        "base_head_at_observation": "e34d2cd56057766f8f656a4ff3486eb34dad607e",
        "head_branch": "candidate/r7e-orthing-supplementation",
        "head_at_observation": "cbab14747835855d232448f648eefa1d4e36074e",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
}
EXPECTED_PROVENANCE = {
    8: {"layer": "owner-observed-model-substitution", "model": "Claude Opus 4.8"},
    9: {"layer": "surfaced-model-attestation", "model": "Claude Opus 4.8"},
    10: {"layer": "surfaced-model-attestation", "model": "Claude Opus 4.8"},
    11: {"layer": "surfaced-model-attestation", "model": "Claude Opus 4.8"},
    12: {"layer": "surfaced-model-attestation", "model": "Claude Opus 4.8"},
}
DECISION_PR_ALIASES = {
    "9-child (R7C grandchild)": 10,
    "10-child (R7D)": 11,
}


def _decision_pr(value):
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    return DECISION_PR_ALIASES.get(value)


def collect_issues(data, decisions):
    """Return semantic issues without reading files or mutating either argument."""
    issues = []
    rows = data.get("pull_requests", []) if isinstance(data, dict) else []
    seen = set()
    by_pr = {}

    for index, row in enumerate(rows):
        pr = row.get("pr") if isinstance(row, dict) else None
        if not isinstance(pr, int) or isinstance(pr, bool):
            issues.append("PR number must be an integer at pull_requests[%d]" % index)
            continue
        if pr in seen:
            issues.append("duplicate PR #%d" % pr)
        else:
            seen.add(pr)
            by_pr[pr] = row

    for pr in REQUIRED_PRS:
        if pr not in seen:
            issues.append("missing PR #%d" % pr)
    for pr in sorted(seen - set(REQUIRED_PRS)):
        issues.append("unexpected PR #%d" % pr)

    if data.get("observed_at_utc") != REQUIRED_OBSERVED_AT:
        issues.append("frozen observation is stale; expected %s" % REQUIRED_OBSERVED_AT)
    if data.get("observation_source") != REQUIRED_OBSERVATION_SOURCE:
        issues.append("observation_source drift from the frozen Task 1 boundary")
    if data.get("timeless_state") is not False:
        issues.append("frozen observation must declare timeless_state: false")
    if data.get("merge_order") != REQUIRED_MERGE_ORDER:
        issues.append("merge_order must be [12, 11, 10, 9, 8]")

    for pr, row in sorted(by_pr.items()):
        for field in ("base_head_at_observation", "head_at_observation"):
            value = row.get(field)
            if not isinstance(value, str) or not SHA40.fullmatch(value):
                issues.append("PR #%d %s must be 40-lowercase-hex" % (pr, field))
        provenance = row.get("provenance")
        if not isinstance(provenance, dict) or not provenance.get("layer"):
            issues.append("PR #%d provenance layer is missing" % pr)
        else:
            expected_provenance = EXPECTED_PROVENANCE.get(pr, {})
            for field in ("layer", "model"):
                if provenance.get(field) != expected_provenance.get(field):
                    issues.append(
                        "PR #%d provenance %s drift: expected %r, got %r"
                        % (pr, field, expected_provenance.get(field), provenance.get(field))
                    )

        expected = EXPECTED_TOPOLOGY.get(pr)
        if expected:
            for field, wanted in expected.items():
                if row.get(field) != wanted:
                    issues.append(
                        "PR #%d frozen %s drift: expected %r, got %r"
                        % (pr, field, wanted, row.get(field))
                    )

    documents = data.get("candidate_documents")
    if documents != REQUIRED_CANDIDATE_DOCUMENTS:
        issues.append("candidate document inventory must match the canonical inventory exactly")
    pdfs = data.get("candidate_pdfs")
    if pdfs != REQUIRED_CANDIDATE_PDFS:
        issues.append("candidate PDF inventory must match the canonical inventory exactly")
    inventory_paths = []
    if isinstance(documents, dict):
        for paths in documents.values():
            if isinstance(paths, list):
                inventory_paths.extend(path for path in paths if isinstance(path, str))
    if isinstance(pdfs, list):
        inventory_paths.extend(path for path in pdfs if isinstance(path, str))
    for path in inventory_paths:
        local_path = os.path.join(ROOT, *path.rstrip("/").split("/"))
        if not os.path.exists(local_path):
            issues.append("candidate artifact does not resolve locally: %s" % path)

    if data.get("review_provenance") != REQUIRED_REVIEW_PROVENANCE:
        issues.append("Sol review provenance drift from the controller-confirmed boundary")

    for previous, current in zip(REQUIRED_PRS, REQUIRED_PRS[1:]):
        parent = by_pr.get(previous)
        child = by_pr.get(current)
        if not parent or not child:
            continue
        if child.get("base_branch") != parent.get("head_branch"):
            issues.append(
                "PR #%d base_branch does not match PR #%d head_branch" % (current, previous)
            )
        if child.get("base_head_at_observation") != parent.get("head_at_observation"):
            issues.append(
                "PR #%d base head does not match PR #%d observed head" % (current, previous)
            )

    expected_allocations = {pr: set() for pr in REQUIRED_PRS}
    for did, decision in decisions.items():
        if "pr" not in decision:
            continue
        pr = _decision_pr(decision.get("pr"))
        if pr not in expected_allocations:
            issues.append("decision %s has an unrecognized candidate PR allocation" % did)
            continue
        expected_allocations[pr].add(str(did))
        if decision.get("status") != "proposed-candidate":
            issues.append("candidate self-promotion: decision %s is %r" % (did, decision.get("status")))

    declared_once = []
    for pr in REQUIRED_PRS:
        row = by_pr.get(pr, {})
        declared = row.get("candidate_decisions", [])
        declared_set = set(declared) if isinstance(declared, list) else set()
        declared_once.extend(declared if isinstance(declared, list) else [])
        if declared_set != expected_allocations[pr]:
            issues.append(
                "decision allocation drift for PR #%d: input=%s registry=%s"
                % (pr, sorted(declared_set), sorted(expected_allocations[pr]))
            )
    if len(declared_once) != len(set(declared_once)):
        issues.append("decision allocation drift: a candidate decision is assigned more than once")

    claims = data.get("status_claims", {})
    if claims.get("candidate_status") != "proposed-candidate":
        issues.append("candidate topology cannot self-promote its candidate_status")
    evidence = claims.get("evidence", {})
    any_terminal_claim = False
    for claim in ("merged", "independent_signoff", "ready_for_merge"):
        if claims.get(claim) is True:
            any_terminal_claim = True
            if not evidence.get(claim):
                issues.append("%s claim lacks evidence" % claim)
    if any_terminal_claim:
        issues.append("candidate topology cannot self-promote")

    return issues


def build_overlay(data):
    """Build the deterministic generated overlay from validated frozen input."""
    rows = []
    for source in data["pull_requests"]:
        rows.append({
            "pr": source["pr"],
            "revision": source["revision"],
            "branch": source["head_branch"],
            "base": source["base_branch"],
            "base_head_at_observation": source["base_head_at_observation"],
            "head_at_observation": source["head_at_observation"],
            "state": source["state"],
            "draft": source["draft"],
            "mergeable_at_observation": source["mergeable_at_observation"],
            "checks_at_observation": source["checks_at_observation"],
            "candidate_decisions": copy.deepcopy(source["candidate_decisions"]),
            "provenance": copy.deepcopy(source["provenance"]),
        })
    claims = copy.deepcopy(data["status_claims"])
    return {
        "schema": "orthemology-candidate-overlay-v2",
        "note": (
            "GENERATED from a frozen observation by scripts/generate_candidate_state.py; "
            "do not edit this file or read observed heads as timeless state."
        ),
        "generated_from": INPUT_REL,
        "label": "SOL INDEPENDENT REVIEW CANDIDATE — NO SIGNOFF OR MERGE READINESS",
        "observed_at_utc": data["observed_at_utc"],
        "observation_source": data["observation_source"],
        "timeless_state": False,
        "merged": False,
        "merged_base": copy.deepcopy(data["merged_base"]),
        "pr_chain": rows,
        "merge_order": copy.deepcopy(data["merge_order"]),
        "candidate_decisions": sorted(
            decision for row in rows for decision in row["candidate_decisions"]
        ),
        "candidate_documents": copy.deepcopy(data["candidate_documents"]),
        "candidate_pdfs": copy.deepcopy(data["candidate_pdfs"]),
        "provenance_layers": {
            row["revision"].lower(): copy.deepcopy(row["provenance"]) for row in rows
        },
        "review_provenance": copy.deepcopy(data["review_provenance"]),
        "status_claims": claims,
        "no_merge_status": {
            "merged": False,
            "independent_signoff": False,
            "ready_for_merge": False,
            "next_action": claims["next_action"],
        },
    }


def _schema_issues(instance, schema, name):
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.path))
    return ["%s schema: %s" % (name, error.message) for error in errors]


def _render(overlay):
    return yaml.safe_dump(overlay, sort_keys=False, allow_unicode=True, width=100)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    data = yaml.safe_load(io.open(INPUT_PATH, encoding="utf-8"))
    decisions = yaml.safe_load(io.open(DECISIONS_PATH, encoding="utf-8"))["decisions"]
    topology_schema = json.load(io.open(TOPOLOGY_SCHEMA, encoding="utf-8"))
    overlay_schema = json.load(io.open(OVERLAY_SCHEMA, encoding="utf-8"))
    issues = _schema_issues(data, topology_schema, "candidate topology")
    if not issues:
        issues.extend(collect_issues(data, decisions))
    if issues:
        for issue in issues:
            print("[FAIL] " + issue)
        print("TOTAL: %d failures" % len(issues))
        return 1

    overlay = build_overlay(data)
    issues = _schema_issues(overlay, overlay_schema, "candidate overlay")
    if issues:
        for issue in issues:
            print("[FAIL] " + issue)
        print("TOTAL: %d failures" % len(issues))
        return 1
    text = _render(overlay)

    if args.check:
        current = io.open(OUTPUT_PATH, encoding="utf-8").read() if os.path.exists(OUTPUT_PATH) else ""
        ok = current == text
        print("[%s] docs/current-candidate-state.yaml is current" % ("PASS" if ok else "FAIL"))
        print("TOTAL: %d failures" % (0 if ok else 1))
        return 0 if ok else 1

    io.open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n").write(text)
    print("wrote docs/current-candidate-state.yaml (%d observed PRs)" % len(overlay["pr_chain"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
