#!/usr/bin/env python3
"""Fresh Task 4 domain-C strictness probe.

The probe runs the real production validator through temporary copies of every
YAML input. It emits one JSON object per line and makes no tracked-tree writes.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_somnic_orthing.py"
PATHS = {
    "activation": ROOT / "examples" / "somnus" / "activation-contract-fixtures.yaml",
    "records": ROOT / "examples" / "somnus" / "somnus-record-fixtures.yaml",
    "history": ROOT / "examples" / "somnus" / "somnus-history-checkpoints.yaml",
    "inventory": ROOT / "applications" / "agentic-runtime" / "SOMNUS-CANDIDATE-INVENTORY.yaml",
    "adoption": ROOT / "applications" / "agentic-runtime" / "HERMES-WRITEBACK-ADOPTION-PROFILE.yaml",
    "collective": ROOT / "applications" / "agentic-runtime" / "COLLECTIVE-SOMNUS-TRANSCLUSION-PROFILE.yaml",
}
DECISION = ROOT / "docs" / "decisions" / "0035-somnic-orthing-and-activation-contracts.md"
MANUSCRIPT = ROOT / "manuscript" / "orthemma-ortheme-systems-revised-draft.md"


def item(rows, key, value):
    return next(row for row in rows if row.get(key) == value)


def load_module():
    spec = importlib.util.spec_from_file_location("task4_parallel_c_production", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not import production validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_base():
    return {
        label: yaml.safe_load(path.read_text(encoding="utf-8"))
        for label, path in PATHS.items()
    }


def production_exit(documents):
    module = load_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        attr_by_label = {
            "activation": "ACTIVATION_PATH",
            "records": "RECORDS_PATH",
            "history": "HISTORY_PATH",
            "inventory": "INVENTORY_PATH",
            "adoption": "ADOPTION_PATH",
            "collective": "COLLECTIVE_PATH",
        }
        for label, attr in attr_by_label.items():
            path = temp / (label + ".yaml")
            path.write_text(
                yaml.safe_dump(documents[label], sort_keys=False), encoding="utf-8"
            )
            setattr(module, attr, path)
        decision_path = temp / "decision.md"
        manuscript_path = temp / "manuscript.md"
        decision_path.write_text(DECISION.read_text(encoding="utf-8"), encoding="utf-8")
        manuscript_path.write_text(
            MANUSCRIPT.read_text(encoding="utf-8"), encoding="utf-8"
        )
        module.DECISION_PATH = decision_path
        module.MANUSCRIPT_PATH = manuscript_path
        output = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                module.main()
            except SystemExit as exc:
                code = int(exc.code or 0)
            except Exception as exc:
                code = 99
                output.write("TRACEBACK: %s: %s" % (type(exc).__name__, exc))
        return code, output.getvalue()


def checkpoint_payload(documents, checkpoint):
    records = documents["records"]
    subjects = {row["subject_id"]: row for row in records["subject_records"]}
    sources = {row["source_record_id"]: row for row in records["source_records"]}
    events = {row["event_id"]: row for row in records["orthing_events"]}
    assessments = {
        row["assessment_id"]: row for row in records["somnic_assessments"]
    }
    subject = subjects.get(checkpoint["subject_id"])
    source = None
    if subject is not None:
        ref = subject["source_record_ref"]
        source = sources.get(ref) or events.get(ref) or assessments.get(ref)
    cutoff = checkpoint["captured_through"]
    eligible = sorted(
        [
            event
            for event in records["orthing_events"]
            if event.get("orthing_id") == checkpoint["subject_id"]
            and event.get("occurred_at") <= cutoff
        ],
        key=lambda event: (event.get("sequence", 0), event.get("event_id", "")),
    )
    chain = documents["history"]["chain"]
    return {
        "chain": {
            "chain_id": chain["chain_id"],
            "chain_version": chain["chain_version"],
            "digest_algorithm": chain["digest_algorithm"],
        },
        "subject": subject,
        "source_record": source,
        "event_history": eligible,
        "captured_through": cutoff,
        "predecessor_checkpoint_digest": checkpoint["predecessor_checkpoint_digest"],
    }


def recompute_checkpoint(documents, checkpoint_id):
    checkpoint = item(
        documents["history"]["checkpoints"], "checkpoint_id", checkpoint_id
    )
    payload = checkpoint_payload(documents, checkpoint)
    checkpoint["event_ids"] = [row["event_id"] for row in payload["event_history"]]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    checkpoint["checkpoint_digest"] = hashlib.sha256(encoded).hexdigest()


def recompute_assessment_digest(documents, assessment_id):
    assessment = item(
        documents["records"]["somnic_assessments"], "assessment_id", assessment_id
    )
    checkpoints = {
        row["checkpoint_id"]: row for row in documents["history"]["checkpoints"]
    }
    payload = [
        {
            "checkpoint_id": checkpoints[checkpoint_id]["checkpoint_id"],
            "subject_id": checkpoints[checkpoint_id]["subject_id"],
            "captured_through": checkpoints[checkpoint_id]["captured_through"],
            "checkpoint_digest": checkpoints[checkpoint_id]["checkpoint_digest"],
        }
        for checkpoint_id in assessment["target_history_checkpoint_ids"]
    ]
    payload.sort(key=lambda row: (row["subject_id"], row["checkpoint_id"]))
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    assessment["target_history_digest"] = hashlib.sha256(encoded).hexdigest()


def fresh(base):
    return copy.deepcopy(base)


def build_cases(base):
    cases = []

    def invalid(case_id, name, boundary, mutate):
        cases.append((case_id, name, "invalid", 1, boundary, mutate))

    def control(case_id, name, boundary, mutate):
        cases.append((case_id, name, "valid-control", 0, boundary, mutate))

    invalid("I01", "malformed-history-document-null", "history top-level schema", lambda d: d.__setitem__("history", None))

    def i02(d):
        d["history"]["checkpoints"][0]["event_ids"] = [{"nested": ["EV-WAKE-001"]}]
    invalid("I02", "malformed-checkpoint-event-ids-nested-map-list", "history checkpoint event_ids", i02)

    def i03(d):
        item(d["records"]["somnic_assessments"], "assessment_id", "SA-NO-CHANGE-001")["target_history_checkpoint_ids"] = {"nested": ["CP-ORTH-NO-CHANGE-001-T2"]}
    invalid("I03", "malformed-assessment-checkpoint-ids-map", "somnic assessment checkpoint owners", i03)

    def i04(d):
        item(d["records"]["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")["governing_input_owners"][0]["source_ref"] = ["analysis-retro@1"]
    invalid("I04", "malformed-run-owner-source-list", "somnus run governing_input_owners", i04)

    def i05(d):
        item(d["records"]["material_deltas"], "material_delta_id", "DELTA-CONTRACT-0.1.1")["owner_role"] = None
    invalid("I05", "malformed-delta-owner-null", "material delta typed owner", i05)

    def i06(d):
        item(d["records"]["orthing_events"], "event_id", "EV-WAKE-002-ASSESS")["claimant_id"] = ["claimant-f"]
    invalid("I06", "malformed-event-claimant-list", "orthing event claimant owner", i06)

    def i07(d):
        candidate = item(d["inventory"]["candidates"], "candidate_id", "orthing-dream")
        candidate["authority_limit"]["prohibited_operations"] = [
            "schedule_runtime", "execute_mutation", {"nested": "promote_governance"},
            "close_governance_finding", "mutate_governance",
        ]
    invalid("I07", "malformed-inventory-prohibition-nested-map", "candidate prohibited operations", i07)

    def i08(d):
        item(d["inventory"]["candidates"], "candidate_id", "guarded-writeback-actuator")["downstream_owner"] = "external downstream owner"
    invalid("I08", "malformed-inventory-owner-scalar", "candidate structured downstream owner", i08)

    def i09(d):
        d["adoption"]["predecessor_classification"]["scope"] = {"nested": ["safe_writeback"]}
    invalid("I09", "malformed-adoption-predecessor-scope-map", "adoption predecessor classification", i09)

    def i10(d):
        d["adoption"]["actuator"]["stages"][3] = None
    invalid("I10", "malformed-adoption-stage-null", "ordered actuator stages", i10)

    def i11(d):
        positive = item(d["activation"]["fixture_outcomes"], "fixture_id", "ACT-POS-001")
        negative = item(d["activation"]["fixture_outcomes"], "fixture_id", "ACT-NEG-001")
        positive["fixture_class"], negative["fixture_class"] = negative["fixture_class"], positive["fixture_class"]
    invalid("I11", "activation-positive-negative-classes-swapped", "fixture class to semantic result parity", i11)

    def i12(d):
        gate = item(d["records"]["meta_orthability_assessments"], "meta_orthability_assessment_id", "MOA-001")
        gate["observed_indicators"] = ["unowned-retrospective-indicator"]
        gate["observed_exclusions"] = ["unowned-retrospective-exclusion"]
    invalid("I12", "meta-gate-unowned-indicator-and-exclusion", "meta gate exact activation-contract vocabulary", i12)

    def i13(d):
        route = item(d["records"]["claimant_routing_cases"], "case_id", "ROUTE-PLACEMENT-002")
        route["claimant_assessments"][0].update(
            claim_attempt_id="CA-002", orthability_assessment_id="OA-002",
            claimant_id="claimant-d",
        )
        route["selected_claimant_id"] = "claimant-d"
        for event_id in ("EV-WAKE-002-ASSESS", "EV-WAKE-002-ROUTE", "EV-WAKE-002"):
            item(d["records"]["orthing_events"], "event_id", event_id).update(
                claim_attempt_id="CA-002", orthability_assessment_id="OA-002",
                claimant_id="claimant-d",
            )
    invalid("I13", "same-claim-pair-owned-by-two-occurrences", "global claim-attempt and assessment ownership", i13)

    def i14(d):
        checkpoint = item(d["history"]["checkpoints"], "checkpoint_id", "CP-ORTH-NO-CHANGE-001-T2")
        checkpoint["captured_through"] = "2026-07-19T12:00:00Z"
        recompute_checkpoint(d, checkpoint["checkpoint_id"])
        recompute_assessment_digest(d, "SA-NO-CHANGE-001")
    invalid("I14", "checkpoint-cutoff-predates-authoritative-subject", "checkpoint cutoff to subject chronology", i14)

    def i15(d):
        assessment = item(d["records"]["somnic_assessments"], "assessment_id", "SA-REOPENED-001")
        assessment["target_history_checkpoint_ids"] = ["CP-ORTH-OLD-001-T2", "CP-ORTH-OLD-001-REOPEN-T2"]
        recompute_assessment_digest(d, "SA-REOPENED-001")
    invalid("I15", "assessment-binds-two-checkpoints-for-one-target", "one current checkpoint per exact target", i15)

    def i16(d):
        checkpoint = {
            "checkpoint_id": "CP-UNRESOLVED-SUBJECT-001",
            "subject_id": "ORTH-UNRESOLVED-001",
            "captured_through": "2026-07-21T19:00:01Z",
            "event_ids": [],
            "predecessor_checkpoint_digest": None,
            "checkpoint_digest": "0" * 64,
            "immutable": True,
        }
        d["history"]["checkpoints"].append(checkpoint)
        recompute_checkpoint(d, checkpoint["checkpoint_id"])
    invalid("I16", "orphan-checkpoint-hashes-null-authorities", "checkpoint subject and source resolution", i16)

    def i17(d):
        run = item(d["records"]["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        run["governing_input_owners"][0]["owner_role"] = "selection_rule"
        run["governing_input_owners"][1]["owner_role"] = "evaluator"
    invalid("I17", "run-governing-refs-relabelled-as-wrong-owner-roles", "run governing owner semantics", i17)

    def i18(d):
        d["records"]["material_deltas"].append({
            "material_delta_id": "DELTA-ORPHAN-CONTRADICTION-001",
            "delta_kind": "contract_revision",
            "owner_role": "analysis",
            "recorded_at": "2026-07-20T10:00:00Z",
            "source_ref": "unresolved-analysis-ref@9",
        })
    invalid("I18", "unused-delta-has-kind-owner-contradiction", "material delta registry parity", i18)

    def i19(d):
        owner = item(d["inventory"]["candidates"], "candidate_id", "guarded-writeback-actuator")["downstream_owner"]
        owner["owner_role"] = "orthemology built-in deployed writeback runtime"
    invalid("I19", "owner-label-contradicts-external-prohibited-structure", "candidate ownership meaning", i19)

    def i20(d):
        candidate = item(d["inventory"]["candidates"], "candidate_id", "orthing-dream")
        candidate["authority_boundary"]["scope"] = "unbounded local scheduling and governance mutation"
    invalid("I20", "authority-scopes-contradict-each-other", "candidate authority scope parity", i20)

    def i21(d):
        d["adoption"]["predecessor_characterization"] = "a non-reasoning toy with no interpretation or safe writeback stages"
    invalid("I21", "predecessor-prose-contradicts-structured-classification", "adoption explanatory to structured parity", i21)

    def i22(d):
        candidate = item(d["inventory"]["candidates"], "candidate_id", "guarded-writeback-actuator")
        candidate["outputs"] = ["automatic live mutation, governance promotion, and closure"]
    invalid("I22", "candidate-output-claims-prohibited-runtime-actions", "candidate outputs to authority parity", i22)

    def i23(d):
        contract = item(d["activation"]["contracts"], "contract_id", "theological-claimant-activation")
        contract["positive_indicators"].append("weather-token")
    invalid("I23", "accepted-contract-boundary-mutates-without-version-or-authorship-change", "bootstrap authoring content binding", i23)

    def i24(d):
        d["history"]["checkpoints"][0]["unknown_nested_key"] = "must not fall through"
    invalid("I24", "checkpoint-unknown-nested-property", "history checkpoint additionalProperties", i24)

    def i25(d):
        run = item(d["records"]["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        run["governing_input_owners"][0]["unknown_nested_key"] = True
    invalid("I25", "run-owner-unknown-nested-property", "somnus run owner additionalProperties", i25)

    def i26(d):
        owner = item(d["inventory"]["candidates"], "candidate_id", "guarded-writeback-actuator")["downstream_owner"]
        owner["unknown_nested_key"] = "must not fall through"
    invalid("I26", "candidate-owner-unknown-nested-property", "candidate owner additionalProperties", i26)

    def i27(d):
        d["adoption"]["predecessor_classification"]["unknown_nested_key"] = False
    invalid("I27", "predecessor-classification-unknown-nested-property", "adoption predecessor additionalProperties", i27)

    def i28(d):
        item(d["records"]["orthing_events"], "event_id", "EV-WAKE-002-ASSESS")["unknown_nested_key"] = None
    invalid("I28", "orthing-event-unknown-nested-property", "orthing event additionalProperties", i28)

    def i29(d):
        item(d["records"]["somnic_assessments"], "assessment_id", "SA-NO-CHANGE-001")["unknown_nested_key"] = []
    invalid("I29", "somnic-assessment-unknown-nested-property", "somnic assessment additionalProperties", i29)

    def i30(d):
        item(d["records"]["material_deltas"], "material_delta_id", "DELTA-CONTRACT-0.1.1")["unknown_nested_key"] = {}
    invalid("I30", "material-delta-unknown-nested-property", "material delta additionalProperties", i30)

    control("C01", "baseline", "all canonical boundaries", lambda d: None)

    def c02(d):
        d["history"]["checkpoints"] = list(reversed(d["history"]["checkpoints"]))
    control("C02", "checkpoint-document-order-permutation", "checkpoint collection order", c02)

    def c03(d):
        old = "CP-ORTH-NO-CHANGE-001-T2"
        new = "CP-ORTH-NO-CHANGE-RENAMED"
        item(d["history"]["checkpoints"], "checkpoint_id", old)["checkpoint_id"] = new
        assessment = item(d["records"]["somnic_assessments"], "assessment_id", "SA-NO-CHANGE-001")
        assessment["target_history_checkpoint_ids"] = [new]
        recompute_assessment_digest(d, "SA-NO-CHANGE-001")
    control("C03", "consistent-checkpoint-id-renaming", "arbitrary checkpoint identifiers", c03)

    def c04(d):
        for run in d["records"]["somnus_runs"]:
            run["governing_input_owners"] = list(reversed(run["governing_input_owners"]))
    control("C04", "governing-owner-row-order-permutation", "run owner collection order", c04)

    def c05(d):
        owner = item(d["inventory"]["candidates"], "candidate_id", "guarded-writeback-actuator")["downstream_owner"]
        owner["owner_role"] = "downstream guarded actuation service owner"
    control("C05", "neutral-downstream-owner-role-rewording", "arbitrary explanatory owner role", c05)

    def c06(d):
        for candidate in d["inventory"]["candidates"]:
            candidate["authority_limit"]["prohibited_operations"] = list(
                reversed(candidate["authority_limit"]["prohibited_operations"])
            )
    control("C06", "prohibited-operation-order-permutation", "unordered prohibition set", c06)

    def c07(d):
        d["adoption"]["predecessor_characterization"] = "a more implicit and coarser predecessor covering safe destination-bound proposal writeback"
    control("C07", "neutral-predecessor-explanation-rewording", "free explanatory prose", c07)

    def c08(d):
        fixture = item(d["activation"]["fixture_outcomes"], "fixture_id", "ACT-POS-001")
        fixture["occurrence"] = "Compare explicit claims made by two theological accounts about divine unity."
    control("C08", "activation-occurrence-rewording", "arbitrary fixture text", c08)

    def c09(d):
        events = d["records"]["orthing_events"]
        selected = item(events, "event_id", "EV-WAKE-001-ASSESS")
        selected["sequence"] = 3
        selected["occurred_at"] = "2026-07-20T10:01:00Z"
        route = item(events, "event_id", "EV-WAKE-001-ROUTE")
        route["sequence"] = 4
        extra = copy.deepcopy(selected)
        extra.update(
            event_id="EV-WAKE-001-ASSESS-RESIDUAL",
            sequence=2,
            occurred_at="2026-07-20T10:00:30Z",
            claim_attempt_id="CA-001",
            orthability_assessment_id="OA-001",
            claimant_id="claimant-c",
        )
        events.append(extra)
        recompute_checkpoint(d, "CP-ORTH-001-T2")
        recompute_assessment_digest(d, "SA-EVIDENCE-TIMING-001")
    control("C09", "additional-nonselected-claimant-assessment-event", "plural claimant audit history before route selection", c09)

    def c10(d):
        d["activation"]["fixture_outcomes"] = list(reversed(d["activation"]["fixture_outcomes"]))
    control("C10", "activation-fixture-order-permutation", "fixture collection order", c10)

    return cases


def classify(code, output):
    if code == 0:
        return "accepted"
    if code == 1 and "TRACEBACK" not in output:
        return "bounded-rejection"
    return "traceback"


def diagnostic_excerpt(output):
    lines = [line for line in output.splitlines() if line]
    return " | ".join(lines[:4])[:1000]


def main():
    base = load_base()
    cases = build_cases(base)
    results = []
    for case_id, name, kind, expected, boundary, mutate in cases:
        documents = fresh(base)
        mutate(documents)
        code, output = production_exit(documents)
        actual_class = classify(code, output)
        passed = code == expected and actual_class != "traceback"
        row = {
            "record_type": "case",
            "case_id": case_id,
            "name": name,
            "kind": kind,
            "boundary": boundary,
            "expected_exit": expected,
            "actual_exit": code,
            "actual_class": actual_class,
            "expectation_met": passed,
            "diagnostic": diagnostic_excerpt(output),
        }
        results.append(row)
        print(json.dumps(row, sort_keys=True))
    invalids = [row for row in results if row["kind"] == "invalid"]
    controls = [row for row in results if row["kind"] == "valid-control"]
    summary = {
        "record_type": "summary",
        "invalid_total": len(invalids),
        "invalid_bounded_rejections": sum(row["actual_class"] == "bounded-rejection" for row in invalids),
        "invalid_false_passes": sum(row["actual_class"] == "accepted" for row in invalids),
        "invalid_tracebacks": sum(row["actual_class"] == "traceback" for row in invalids),
        "control_total": len(controls),
        "control_acceptances": sum(row["actual_class"] == "accepted" for row in controls),
        "control_rejections": sum(row["actual_class"] != "accepted" for row in controls),
        "all_expectations_met": all(row["expectation_met"] for row in results),
    }
    print(json.dumps(summary, sort_keys=True))
    raise SystemExit(0)


if __name__ == "__main__":
    main()
