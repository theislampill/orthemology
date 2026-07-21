#!/usr/bin/env python3
"""Validate the generated, complete R7 candidate topology (Decision 0034).

This validator is deterministic and offline.  It validates the frozen PR
observation, rebuilds the candidate overlay in memory, and requires the tracked
overlay to equal that generated model.  It does not query GitHub or treat an
observed branch head as a timeless/self-referential commit claim.
"""
import io
import json
import os
import sys

import yaml
from jsonschema import Draft202012Validator

from generate_candidate_state import build_overlay, collect_issues

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_R6_SHA = "43fee0f519e2f6984fb143c1e621c83382e71ec7"
FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    path = os.path.join(ROOT, *rel.split("/"))
    return io.open(path, encoding="utf-8").read() if os.path.exists(path) else ""


def schema_errors(instance, rel):
    schema = json.loads(read(rel))
    return sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda error: list(error.path))


def main():
    registry = yaml.safe_load(read("docs/decision-status.yaml"))
    decisions = registry["decisions"]

    # Candidate decisions remain candidate and their source records say so.
    for did, row in sorted(decisions.items()):
        is_candidate = "pr" in row
        if is_candidate:
            check(
                "candidate decision %s is proposed-candidate (not adopted-merged)" % did,
                row.get("status") == "proposed-candidate",
                repr(row.get("status")),
            )
            decision_dir = os.path.join(ROOT, "docs", "decisions")
            filename = next((name for name in os.listdir(decision_dir) if name.startswith(did + "-")), None)
            body = read("docs/decisions/" + filename) if filename else ""
            check(
                "candidate decision %s file carries a CANDIDATE label" % did,
                "CANDIDATE" in body.upper(),
            )
        else:
            check(
                "merged decision %s is not proposed-candidate" % did,
                row.get("status") != "proposed-candidate",
                repr(row.get("status")),
            )

    for did, row in decisions.items():
        number = int(did)
        if number >= 20:
            check("decision %s (>=0020) is classified candidate (carries pr)" % did, "pr" in row)
        else:
            check("merged decision %s (<=0019) carries no pr field" % did, "pr" not in row)

    # Historical overlays remain historical evidence, never the current model.
    history = yaml.safe_load(read("docs/project-closure/HISTORICAL-STATUS-INDEX.yaml"))
    rules = history if isinstance(history, list) else history.get("rules", history.get("entries", []))
    bad = []
    for rule in rules if isinstance(rules, list) else []:
        prefix = str(rule.get("prefix", ""))
        status = str(rule.get("status", ""))
        if prefix.startswith("docs/project-closure/r7") and status in ("merged", "adopted", "adopted-merged"):
            bad.append("%s=%s" % (prefix, status))
    check("no R7 candidate closure artifact is marked merged/adopted", not bad, "; ".join(bad))

    input_text = read("docs/project-closure/r7e-sol/CANDIDATE-TOPOLOGY-INPUT.yaml")
    overlay_text = read("docs/current-candidate-state.yaml")
    check("frozen candidate-topology input exists", bool(input_text))
    check("generated candidate overlay exists", bool(overlay_text))
    data = yaml.safe_load(input_text) if input_text else {}
    overlay = yaml.safe_load(overlay_text) if overlay_text else {}

    input_schema_errors = schema_errors(data, "schemas/candidate-topology.schema.json")
    check(
        "frozen candidate topology validates against its schema",
        not input_schema_errors,
        "; ".join(error.message for error in input_schema_errors[:3]),
    )
    semantic_issues = [] if input_schema_errors else collect_issues(data, decisions)
    check(
        "frozen candidate topology passes complete semantic validation",
        not input_schema_errors and not semantic_issues,
        "; ".join(semantic_issues[:3]) if semantic_issues else "schema validation failed",
    )

    generated = build_overlay(data) if not input_schema_errors else {}
    overlay_schema_errors = schema_errors(overlay, "schemas/candidate-overlay.schema.json")
    check(
        "candidate overlay validates against its schema",
        not overlay_schema_errors,
        "; ".join(error.message for error in overlay_schema_errors[:3]),
    )
    check(
        "candidate overlay exactly matches the deterministic generated model",
        overlay == generated,
        "run scripts/generate_candidate_state.py",
    )

    if not overlay_schema_errors:
        check("candidate overlay declares merged: false", overlay.get("merged") is False)
        check(
            "candidate overlay merged-base sha is protected main R6",
            overlay.get("merged_base", {}).get("sha") == MAIN_R6_SHA,
        )
        check(
            "candidate overlay contains exact PR #8-#12 topology",
            [row.get("pr") for row in overlay.get("pr_chain", [])] == [8, 9, 10, 11, 12],
        )
        check(
            "candidate overlay uses head_at_observation and no timeless head field",
            all("head_at_observation" in row and "head" not in row for row in overlay.get("pr_chain", [])),
        )
        check("candidate overlay is explicitly non-timeless", overlay.get("timeless_state") is False)
        no_merge = overlay.get("no_merge_status", {})
        check(
            "candidate overlay declares merged/signoff/ready all false",
            no_merge.get("merged") is False
            and no_merge.get("independent_signoff") is False
            and no_merge.get("ready_for_merge") is False,
        )

    print("TOTAL: %d failures" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
