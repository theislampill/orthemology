#!/usr/bin/env python3
"""Fresh Task 4 ownership and chronology probes through production main()."""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_somnic_orthing.py"
ACTIVATION = ROOT / "examples" / "somnus" / "activation-contract-fixtures.yaml"
RECORDS = ROOT / "examples" / "somnus" / "somnus-record-fixtures.yaml"
HISTORY = ROOT / "examples" / "somnus" / "somnus-history-checkpoints.yaml"
INVENTORY = ROOT / "applications" / "agentic-runtime" / "SOMNUS-CANDIDATE-INVENTORY.yaml"
ADOPTION = ROOT / "applications" / "agentic-runtime" / "HERMES-WRITEBACK-ADOPTION-PROFILE.yaml"
COLLECTIVE = ROOT / "applications" / "agentic-runtime" / "COLLECTIVE-SOMNUS-TRANSCLUSION-PROFILE.yaml"
DECISION = ROOT / "docs" / "decisions" / "0035-somnic-orthing-and-activation-contracts.md"


def item(rows, key, value):
    return next(row for row in rows if row[key] == value)


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_module():
    spec = importlib.util.spec_from_file_location("task4_parallel_a_probe", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not import production validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def production_exit(documents):
    """Invoke the production validator with every YAML input on a temp path."""
    module = load_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        paths = {
            "ACTIVATION_PATH": (temp / "activation.yaml", documents["activation"]),
            "RECORDS_PATH": (temp / "records.yaml", documents["records"]),
            "HISTORY_PATH": (temp / "history.yaml", documents["history"]),
            "INVENTORY_PATH": (temp / "inventory.yaml", documents["inventory"]),
            "ADOPTION_PATH": (temp / "adoption.yaml", documents["adoption"]),
            "COLLECTIVE_PATH": (temp / "collective.yaml", documents["collective"]),
        }
        for attr, (path, value) in paths.items():
            path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
            setattr(module, attr, path)
        decision_path = temp / "decision.md"
        decision_path.write_text(documents["decision"], encoding="utf-8")
        module.DECISION_PATH = decision_path
        output = io.StringIO()
        exit_code = 0
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                module.main()
            except SystemExit as exc:
                exit_code = int(exc.code or 0)
            except Exception as exc:  # A traceback is contract failure evidence.
                exit_code = 99
                output.write("TRACEBACK: %s: %s" % (type(exc).__name__, exc))
        return exit_code, output.getvalue()


def fresh(baseline):
    return copy.deepcopy(baseline)


def rewrite_property(values, old, new):
    return [new if value == old else value for value in values]


def invalid_cases(baseline):
    cases = []

    docs = fresh(baseline)
    contract = docs["activation"]["contracts"][0]
    old_property = "worldview-bearing-task"
    new_property = "worldview-sensitive-task"
    contract["required_properties"] = rewrite_property(
        contract["required_properties"], old_property, new_property
    )
    for outcome in docs["activation"]["fixture_outcomes"]:
        changed = False
        for assessment in outcome["claimant_assessments"]:
            if (
                assessment["activation_contract_id"] == contract["contract_id"]
                and assessment["activation_contract_version"] == contract["contract_version"]
            ):
                changed = True
                for field in ("satisfied", "absent", "indeterminate"):
                    assessment["property_findings"][field] = rewrite_property(
                        assessment["property_findings"][field], old_property, new_property
                    )
        if changed:
            for field in ("satisfied", "absent", "indeterminate"):
                outcome["property_findings"][field] = rewrite_property(
                    outcome["property_findings"][field], old_property, new_property
                )
    cases.append((
        "I01",
        "accepted-contract-same-version-body-rewritten-without-authorship-content-binding",
        docs,
        "authorship-content",
    ))

    docs = fresh(baseline)
    contract = docs["activation"]["contracts"][0]
    foreign_fixture = "ACT-DB-POS-001"
    contract["fixture_outcomes"].append(foreign_fixture)
    authoring = item(
        docs["activation"]["authoring_records"],
        "provenance_record_id",
        contract["authorship"]["provenance_record_id"],
    )
    authoring["fixture_ids"].append(foreign_fixture)
    cases.append((
        "I02",
        "accepted-contract-and-authoring-record-claim-unassessed-foreign-fixture",
        docs,
        "fixture-ownership",
    ))

    docs = fresh(baseline)
    contract = docs["activation"]["contracts"][0]
    contract["superseded_by"] = "%s@%s" % (
        contract["contract_id"], contract["contract_version"]
    )
    cases.append((
        "I03",
        "accepted-contract-self-supersedes",
        docs,
        "activation-version-state",
    ))

    docs = fresh(baseline)
    route = item(
        docs["records"]["claimant_routing_cases"], "case_id", "ROUTE-PLACEMENT-002"
    )
    route["claimant_assessments"][0].update(
        claim_attempt_id="CA-002",
        orthability_assessment_id="OA-002",
        claimant_id="claimant-d",
    )
    route["selected_claimant_id"] = "claimant-d"
    for event in docs["records"]["orthing_events"]:
        if event.get("occurrence_id") == "OCC-002" and event.get("event_type") in {
            "orthability_assessed", "route_selected", "placement_committed"
        }:
            event.update(
                claim_attempt_id="CA-002",
                orthability_assessment_id="OA-002",
                claimant_id="claimant-d",
            )
    cases.append((
        "I04",
        "one-claimant-assessment-pair-replayed-across-two-occurrences",
        docs,
        "routing-ownership",
    ))

    docs = fresh(baseline)
    docs["records"]["identity_fixture"]["claim_attempt_ids"].append("CA-NOCLAIM-001")
    docs["records"]["identity_fixture"]["orthability_assessment_ids"].append(
        "OA-NOCLAIM-001"
    )
    docs["records"]["identity_fixture"]["claimant_ids"].append(
        "claimant-no-claim-001"
    )
    docs["records"]["identity_registry"].extend([
        {"identity_id": "CA-NOCLAIM-001", "identity_kind": "claim_attempt"},
        {
            "identity_id": "OA-NOCLAIM-001",
            "identity_kind": "orthability_assessment",
        },
        {"identity_id": "claimant-no-claim-001", "identity_kind": "claimant"},
    ])
    docs["records"]["claimant_routing_cases"].append({
        "case_id": "ROUTE-NOCLAIM-CONTRADICTION-001",
        "occurrence_id": "OCC-R7E-SURVIVING-TRACE",
        "claimant_assessments": [{
            "claim_attempt_id": "CA-NOCLAIM-001",
            "orthability_assessment_id": "OA-NOCLAIM-001",
            "claimant_id": "claimant-no-claim-001",
            "result": "inapplicable",
        }],
        "selected_claimant_id": "claimant-no-claim-001",
        "route_status": "no_claim",
        "retained_residual_claimants": [],
        "retained_inapplicable_claimants": ["claimant-no-claim-001"],
    })
    cases.append((
        "I05",
        "no-claim-route-simultaneously-declares-a-selected-claimant",
        docs,
        "route-state",
    ))

    docs = fresh(baseline)
    docs["records"]["successor_states"].append({
        "successor_state_id": "SUCCESSOR-ORPHAN-ALTERNATE-001",
        "proposal_id": "PROP-CONTRACT-001",
        "application_id": None,
        "status": "proposed_target",
        "identity_key": "unowned-alternate-target",
        "version": "proposed-v2",
        "action_label": "unowned-alternate-action",
        "created_at": "2026-07-21T19:02:45Z",
    })
    cases.append((
        "I06",
        "proposal-owns-an-extra-successor-not-named-by-its-proposed-action",
        docs,
        "successor-ownership",
    ))

    docs = fresh(baseline)
    docs["records"]["authorizations"].append({
        "authorization_id": "AUTH-LATE-REJECT-001",
        "proposal_id": "PROP-CONTRACT-001",
        "source": "independent_governance",
        "decision": "rejected",
        "authorization_rule_ref": "independent-governance-rule@1",
        "decided_at": "2026-07-21T19:04:00Z",
        "reason": "later rejection under the same governing rule",
    })
    assessment = item(
        docs["records"]["somnic_assessments"],
        "assessment_id",
        "SA-CORRECT-DEFECTIVE-001",
    )
    assessment["authorization_refs"].append("AUTH-LATE-REJECT-001")
    timeline_t3 = item(docs["records"]["writeback_timeline"], "time_role", "t3")
    timeline_t3["record_ids"].append("AUTH-LATE-REJECT-001")
    timeline_t3["occurred_at"] = "2026-07-21T19:04:00Z"
    cases.append((
        "I07",
        "later-rejection-under-same-rule-does-not-stop-earlier-authorized-application",
        docs,
        "authorization-state-chronology",
    ))

    docs = fresh(baseline)
    failed = item(docs["records"]["applications"], "application_id", "APP-FAILED-001")
    failed["outcome_evaluation_required"] = True
    cases.append((
        "I08",
        "failed-application-declares-required-outcome-but-has-none",
        docs,
        "application-outcome-contract",
    ))

    docs = fresh(baseline)
    docs["records"]["outcome_evaluations"].append({
        "outcome_evaluation_id": "OUTCOME-FAILED-EFFECTIVE-001",
        "application_id": "APP-FAILED-001",
        "time_role": "t5",
        "evaluated_at": "2026-07-21T19:05:00Z",
        "result": "effective",
        "verdict_record_ref": "schemas/verdict-record.schema.json",
        "self_validating": False,
    })
    assessment = item(
        docs["records"]["somnic_assessments"],
        "assessment_id",
        "SA-ALTERNATIVES-001",
    )
    assessment["outcome_evaluation_refs"].append("OUTCOME-FAILED-EFFECTIVE-001")
    cases.append((
        "I09",
        "failed-application-receives-effective-outcome",
        docs,
        "application-outcome-state",
    ))

    return cases


def valid_controls(baseline):
    cases = [("C01", "canonical-baseline", fresh(baseline), "baseline")]

    docs = fresh(baseline)
    assessment = item(
        docs["records"]["somnic_assessments"],
        "assessment_id",
        "SA-ALTERNATIVES-001",
    )
    assessment["proposal_ids"] = list(reversed(assessment["proposal_ids"]))
    cases.append((
        "C02",
        "alternative-proposal-set-order-is-nonsemantic",
        docs,
        "proposal-cardinality-control",
    ))

    docs = fresh(baseline)
    item(docs["records"]["proposals"], "proposal_id", "PROP-SKILL-001")[
        "status"
    ] = "withdrawn"
    cases.append((
        "C03",
        "unapplied-unauthed-proposal-may-be-withdrawn-without-history-rewrite",
        docs,
        "withdrawn-state-control",
    ))

    docs = fresh(baseline)
    candidate = item(
        docs["inventory"]["candidates"],
        "candidate_id",
        "verdict-aware-patch-proposal",
    )
    candidate["downstream_owner"]["owner_role"] = "external change-proposal custodian"
    cases.append((
        "C04",
        "external-proposal-owner-role-allows-neutral-equivalent-wording",
        docs,
        "ownership-wording-control",
    ))

    return cases


def classify(kind, exit_code, output):
    traceback = exit_code == 99 or "TRACEBACK" in output
    if traceback:
        return "traceback"
    if kind == "invalid":
        return "bounded_rejection" if exit_code == 1 else "false_pass"
    return "accepted" if exit_code == 0 else "valid_control_rejection"


def main():
    baseline = {
        "activation": load_yaml(ACTIVATION),
        "records": load_yaml(RECORDS),
        "history": load_yaml(HISTORY),
        "inventory": load_yaml(INVENTORY),
        "adoption": load_yaml(ADOPTION),
        "collective": load_yaml(COLLECTIVE),
        "decision": DECISION.read_text(encoding="utf-8"),
    }
    results = []
    all_cases = [
        *(('invalid', case) for case in invalid_cases(baseline)),
        *(('control', case) for case in valid_controls(baseline)),
    ]
    for kind, (case_id, name, documents, domain) in all_cases:
        expected = 1 if kind == "invalid" else 0
        exit_code, output = production_exit(documents)
        diagnostic_class = classify(kind, exit_code, output)
        result = {
            "case_id": case_id,
            "kind": kind,
            "name": name,
            "domain": domain,
            "expected_exit": expected,
            "actual_exit": exit_code,
            "diagnostic_class": diagnostic_class,
            "expectation_met": exit_code == expected and "TRACEBACK" not in output,
            "diagnostic_excerpt": " | ".join(
                line.strip() for line in output.splitlines()[:3] if line.strip()
            )[:500],
        }
        results.append(result)
        print(json.dumps(result, sort_keys=True))

    summary = {
        "type": "summary",
        "invalid_total": sum(row[0] == "invalid" for row in all_cases),
        "invalid_rejected": sum(
            row["kind"] == "invalid" and row["diagnostic_class"] == "bounded_rejection"
            for row in results
        ),
        "false_passes": sum(row["diagnostic_class"] == "false_pass" for row in results),
        "tracebacks": sum(row["diagnostic_class"] == "traceback" for row in results),
        "control_total": sum(row[0] == "control" for row in all_cases),
        "controls_accepted": sum(
            row["kind"] == "control" and row["diagnostic_class"] == "accepted"
            for row in results
        ),
        "valid_control_rejections": sum(
            row["diagnostic_class"] == "valid_control_rejection" for row in results
        ),
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
