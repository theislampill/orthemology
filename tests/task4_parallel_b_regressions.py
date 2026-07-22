#!/usr/bin/env python3
"""Fresh Task 4 history-domain probe through the production validator main().

The program emits JSON Lines only. Each case runs against temporary YAML copies
and leaves the tracked repository tree untouched.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_somnic_orthing.py"
PINNED_PYTHON = ROOT.parent / "venv-lock" / "Scripts" / "python.exe"
PATHS = {
    "activation": ROOT / "examples" / "somnus" / "activation-contract-fixtures.yaml",
    "records": ROOT / "examples" / "somnus" / "somnus-record-fixtures.yaml",
    "history": ROOT / "examples" / "somnus" / "somnus-history-checkpoints.yaml",
    "inventory": ROOT / "applications" / "agentic-runtime" / "SOMNUS-CANDIDATE-INVENTORY.yaml",
    "adoption": ROOT / "applications" / "agentic-runtime" / "HERMES-WRITEBACK-ADOPTION-PROFILE.yaml",
    "collective": ROOT / "applications" / "agentic-runtime" / "COLLECTIVE-SOMNUS-TRANSCLUSION-PROFILE.yaml",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def item(rows, key, value):
    return next(row for row in rows if row[key] == value)


def production_exit(documents):
    """Invoke scripts/validate_somnic_orthing.py main() in pinned Python."""
    path_attrs = {
        "activation": "ACTIVATION_PATH",
        "records": "RECORDS_PATH",
        "history": "HISTORY_PATH",
        "inventory": "INVENTORY_PATH",
        "adoption": "ADOPTION_PATH",
        "collective": "COLLECTIVE_PATH",
    }
    with tempfile.TemporaryDirectory(prefix="task4-history-probe-") as temp_dir:
        temp = Path(temp_dir)
        for name, attr in path_attrs.items():
            path = temp / f"{name}.yaml"
            path.write_text(
                yaml.safe_dump(documents[name], sort_keys=False), encoding="utf-8"
            )
            path_attrs[name] = (attr, path)
        runner = """
import importlib.util
import sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('task4_history_subprocess', sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
for assignment in sys.argv[2:]:
    name, value = assignment.split('=', 1)
    setattr(module, name, Path(value))
module.main()
"""
        assignments = [
            f"{attr}={path}" for attr, path in path_attrs.values()
        ]
        completed = subprocess.run(
            [str(PINNED_PYTHON), "-c", runner, str(SCRIPT), *assignments],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        output = completed.stdout + completed.stderr
        exit_code = 99 if "Traceback (most recent call last)" in output else completed.returncode
        return exit_code, output


def checkpoint_digest(records, history, checkpoint):
    subject = item(records["subject_records"], "subject_id", checkpoint["subject_id"])
    source_ref = subject["source_record_ref"]
    sources = {row["source_record_id"]: row for row in records["source_records"]}
    events = {row["event_id"]: row for row in records["orthing_events"]}
    assessments = {
        row["assessment_id"]: row for row in records["somnic_assessments"]
    }
    source = sources.get(source_ref) or events.get(source_ref) or assessments.get(source_ref)
    cutoff = checkpoint["captured_through"]
    cutoff_key = cutoff.replace("Z", "+00:00")
    eligible = [
        row
        for row in records["orthing_events"]
        if row.get("orthing_id") == checkpoint["subject_id"]
        and row["occurred_at"].replace("Z", "+00:00") <= cutoff_key
    ]
    eligible.sort(key=lambda row: (row.get("sequence", 0), row.get("event_id", "")))
    checkpoint["event_ids"] = sorted(row["event_id"] for row in eligible)
    chain = history["chain"]
    payload = {
        "chain": {
            "chain_id": chain["chain_id"],
            "chain_version": chain["chain_version"],
            "digest_algorithm": chain["digest_algorithm"],
        },
        "subject": subject,
        "source_record": source,
        "event_history": eligible,
        "captured_through": checkpoint["captured_through"],
        "predecessor_checkpoint_digest": checkpoint["predecessor_checkpoint_digest"],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def recompute_subject_chain(records, history, subject_id):
    checkpoints = [
        row for row in history["checkpoints"] if row["subject_id"] == subject_id
    ]
    checkpoints.sort(key=lambda row: (row["captured_through"], row["checkpoint_id"]))
    predecessor = None
    for checkpoint in checkpoints:
        checkpoint["predecessor_checkpoint_digest"] = predecessor
        checkpoint["checkpoint_digest"] = checkpoint_digest(records, history, checkpoint)
        predecessor = checkpoint["checkpoint_digest"]


def recompute_all_chains(records, history):
    for subject_id in sorted({row["subject_id"] for row in history["checkpoints"]}):
        recompute_subject_chain(records, history, subject_id)


def recompute_assessment_digest(records, history, assessment_id):
    assessment = item(records["somnic_assessments"], "assessment_id", assessment_id)
    by_id = {row["checkpoint_id"]: row for row in history["checkpoints"]}
    payload = [
        {
            "checkpoint_id": by_id[checkpoint_id]["checkpoint_id"],
            "subject_id": by_id[checkpoint_id]["subject_id"],
            "captured_through": by_id[checkpoint_id]["captured_through"],
            "checkpoint_digest": by_id[checkpoint_id]["checkpoint_digest"],
        }
        for checkpoint_id in set(assessment["target_history_checkpoint_ids"])
    ]
    payload.sort(key=lambda row: (row["subject_id"], row["checkpoint_id"]))
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    assessment["target_history_digest"] = hashlib.sha256(encoded).hexdigest()


def recompute_all_assessment_digests(records, history):
    for assessment in records["somnic_assessments"]:
        recompute_assessment_digest(records, history, assessment["assessment_id"])


def clone(baseline):
    return copy.deepcopy(baseline)


def build_cases(baseline):
    cases = []

    def invalid(case_id, name, mutate):
        cases.append((case_id, "invalid", name, 1, mutate))

    def control(case_id, name, mutate):
        cases.append((case_id, "control", name, 0, mutate))

    def i01(doc):
        assessment = item(doc["records"]["somnic_assessments"], "assessment_id", "SA-REOPENED-001")
        assessment["target_history_checkpoint_ids"] = ["CP-ORTH-OLD-001-T2"]
        recompute_assessment_digest(doc["records"], doc["history"], "SA-REOPENED-001")

    invalid("I01", "reopened-assessment-selects-stale-predecessor-checkpoint", i01)

    def i02(doc):
        assessment = item(doc["records"]["somnic_assessments"], "assessment_id", "SA-REOPENED-001")
        assessment["target_history_checkpoint_ids"] = [
            "CP-ORTH-OLD-001-T2", "CP-ORTH-OLD-001-REOPEN-T2"
        ]
        recompute_assessment_digest(doc["records"], doc["history"], "SA-REOPENED-001")

    invalid("I02", "assessment-uses-two-checkpoints-for-one-target", i02)

    def i03(doc):
        checkpoint = item(doc["history"]["checkpoints"], "checkpoint_id", "CP-ORTH-NO-CHANGE-001-T2")
        checkpoint["captured_through"] = "2026-07-20T11:59:59Z"
        recompute_subject_chain(doc["records"], doc["history"], "ORTH-NO-CHANGE-001")
        recompute_assessment_digest(doc["records"], doc["history"], "SA-NO-CHANGE-001")

    invalid("I03", "checkpoint-cutoff-predates-authoritative-target-t1", i03)

    def i04(doc):
        doc["history"]["chain"]["chain_version"] = "99.0.0-unowned"
        recompute_all_chains(doc["records"], doc["history"])
        recompute_all_assessment_digests(doc["records"], doc["history"])

    invalid("I04", "unowned-history-chain-version-replaces-entire-chain", i04)

    def i05(doc):
        original = item(doc["history"]["checkpoints"], "checkpoint_id", "CP-ORTH-NO-CHANGE-001-T2")
        fork = copy.deepcopy(original)
        fork.update(
            checkpoint_id="CP-ORTH-NO-CHANGE-001-FORK",
            captured_through="2026-07-21T19:00:02Z",
            predecessor_checkpoint_digest=None,
        )
        fork["checkpoint_digest"] = checkpoint_digest(doc["records"], doc["history"], fork)
        doc["history"]["checkpoints"].append(fork)

    invalid("I05", "same-subject-checkpoint-fork-starts-second-root", i05)

    def i06(doc):
        assessment = item(doc["records"]["somnic_assessments"], "assessment_id", "SA-NO-CHANGE-001")
        assessment["target_history_checkpoint_ids"] = ["CP-ORTH-ALTERNATIVES-001-T2"]
        recompute_assessment_digest(doc["records"], doc["history"], "SA-NO-CHANGE-001")

    invalid("I06", "assessment-selects-checkpoint-owned-by-different-target", i06)

    def i07(doc):
        checkpoint = item(doc["history"]["checkpoints"], "checkpoint_id", "CP-ORTH-NO-CHANGE-001-T2")
        checkpoint["captured_through"] = "2026-07-21T19:00:02Z"
        recompute_subject_chain(doc["records"], doc["history"], "ORTH-NO-CHANGE-001")
        recompute_assessment_digest(doc["records"], doc["history"], "SA-NO-CHANGE-001")

    invalid("I07", "assessment-selects-checkpoint-after-exact-t2-cutoff", i07)

    def i08(doc):
        item(doc["records"]["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["closure_status"] = "open"

    invalid("I08", "closed-assessment-reopened-in-place-without-successor", i08)

    def i09(doc):
        item(doc["records"]["material_deltas"], "material_delta_id", "DELTA-CONTRACT-0.1.1")["recorded_at"] = "2026-07-21T18:00:00Z"

    invalid("I09", "reopening-delta-predates-prior-assessment-cutoff", i09)

    def i10(doc):
        run = item(doc["records"]["somnus_runs"], "somnus_run_id", "RUN-REOPEN-001")
        run["governing_versions"] = ["analysis-retro@1", "recurrence-contract@0.1.0"]
        item(run["governing_input_owners"], "owner_role", "operation_contract")["source_ref"] = "recurrence-contract@0.1.0"
        item(doc["records"]["material_deltas"], "material_delta_id", "DELTA-CONTRACT-0.1.1")["source_ref"] = "recurrence-contract@0.1.0"

    invalid("I10", "contract-revision-delta-reuses-prior-governing-version", i10)

    def i11(doc):
        run = item(doc["records"]["somnus_runs"], "somnus_run_id", "RUN-REOPEN-001")
        run["governing_input_owners"].insert(
            0,
            {"owner_role": "analysis", "source_ref": "recurrence-contract@0.1.1"},
        )

    invalid("I11", "governing-input-declares-contradictory-duplicate-owner-role", i11)

    def i12(doc):
        item(doc["records"]["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")["reference_corpus_revision"] = "LEDGER-REV-NOT-REGISTERED"

    invalid("I12", "reference-corpus-revision-has-no-authoritative-owner", i12)

    def i13(doc):
        item(doc["records"]["somnus_runs"], "somnus_run_id", "RUN-NEXT-001")["historical_comparator_ids"].append("ORTH-SUCCESS-001")

    invalid("I13", "reportless-run-declares-additional-unused-comparator", i13)

    def i14(doc):
        for event in doc["records"]["orthing_events"]:
            if event.get("orthing_id") == "ORTH-002":
                event["session_id"] = "SESSION-R7E-RECONSTRUCTION"

    invalid("I14", "episode-occurrence-orthing-lifecycle-reassigned-to-unrelated-session", i14)

    def i15(doc):
        report = item(doc["records"]["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["opportunity_ids"].remove("OPP-OTHER-004")
        report["opportunity_denominator"] -= 1

    invalid("I15", "opportunity-denominator-omits-eligible-other-opportunity", i15)

    def i16(doc):
        report = item(doc["records"]["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["counterexample_ids"] = ["ORTH-NEW-002"]
        item(doc["records"]["opportunity_records"], "opportunity_id", "OPP-COUNTEREXAMPLE-001")["classification"] = "other"
        replacement = item(doc["records"]["opportunity_records"], "opportunity_id", "OPP-OTHER-001")
        replacement.update(subject_id="ORTH-NEW-002", classification="counterexample")

    invalid("I16", "waking-orthing-promoted-to-counterexample-without-counterexample-owner", i16)

    def i17(doc):
        checkpoint = {
            "checkpoint_id": "CP-UNKNOWN-SUBJECT-T2",
            "subject_id": "ORTH-NOT-IN-SUBJECT-REGISTRY",
            "captured_through": "2026-07-21T19:00:01Z",
            "event_ids": [],
            "predecessor_checkpoint_digest": None,
            "checkpoint_digest": "",
            "immutable": True,
        }
        chain = doc["history"]["chain"]
        payload = {
            "chain": {
                "chain_id": chain["chain_id"],
                "chain_version": chain["chain_version"],
                "digest_algorithm": chain["digest_algorithm"],
            },
            "subject": None,
            "source_record": None,
            "event_history": [],
            "captured_through": checkpoint["captured_through"],
            "predecessor_checkpoint_digest": None,
        }
        checkpoint["checkpoint_digest"] = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        doc["history"]["checkpoints"].append(checkpoint)

    invalid("I17", "checkpoint-chain-accepts-unresolved-subject-and-source", i17)

    control("C01", "canonical-baseline", lambda doc: None)

    def c02(doc):
        doc["history"]["checkpoints"] = list(reversed(doc["history"]["checkpoints"]))

    control("C02", "history-checkpoint-document-order-reversed", c02)

    def c03(doc):
        old = "CP-ORTH-NO-CHANGE-001-T2"
        new = "CP-ORTH-NO-CHANGE-RENAMED"
        item(doc["history"]["checkpoints"], "checkpoint_id", old)["checkpoint_id"] = new
        assessment = item(doc["records"]["somnic_assessments"], "assessment_id", "SA-NO-CHANGE-001")
        assessment["target_history_checkpoint_ids"] = [new]
        recompute_assessment_digest(doc["records"], doc["history"], "SA-NO-CHANGE-001")

    control("C03", "consistent-checkpoint-id-rename", c03)

    def c04(doc):
        assessment = item(doc["records"]["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")
        assessment["target_history_checkpoint_ids"] = list(reversed(assessment["target_history_checkpoint_ids"]))

    control("C04", "assessment-checkpoint-reference-order-reversed", c04)

    def c05(doc):
        report = item(doc["records"]["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["supporting_occurrences"] = list(reversed(report["supporting_occurrences"]))

    control("C05", "recurrence-support-order-reversed", c05)

    def c06(doc):
        report = item(doc["records"]["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["opportunity_ids"] = list(reversed(report["opportunity_ids"]))

    control("C06", "opportunity-id-order-reversed", c06)

    def c07(doc):
        policy = item(doc["records"]["independence_policies"], "rule_id", "independence-rule-v1")
        policy["required_dimensions"] = list(reversed(policy["required_dimensions"]))
        payload = {key: policy[key] for key in (
            "rule_id", "rule_version", "required_dimensions", "pass_label",
            "fail_label", "immutable"
        )}
        policy["policy_digest"] = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        report = item(doc["records"]["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["independence_assessment"]["required_dimensions"] = list(policy["required_dimensions"])

    control("C07", "independence-required-dimension-order-reversed", c07)

    def c08(doc):
        old = "DELTA-CONTRACT-0.1.1"
        new = "DELTA-CONTRACT-REVISION-A"
        item(doc["records"]["material_deltas"], "material_delta_id", old)["material_delta_id"] = new
        run = item(doc["records"]["somnus_runs"], "somnus_run_id", "RUN-REOPEN-001")
        run["material_delta_ids"] = [new]

    control("C08", "consistent-material-delta-id-rename", c08)

    return cases


def main():
    baseline = {name: load_yaml(path) for name, path in PATHS.items()}
    results = []
    for case_id, case_kind, name, expected_exit, mutate in build_cases(baseline):
        documents = clone(baseline)
        mutate(documents)
        actual_exit, output = production_exit(documents)
        traceback = actual_exit == 99 or "TRACEBACK" in output
        passed = actual_exit == expected_exit and not traceback
        diagnostic = next(
            (line for line in output.splitlines() if line.startswith("FAIL:")),
            output.strip().splitlines()[0] if output.strip() else "",
        )
        result = {
            "type": "case", "case_id": case_id, "case_kind": case_kind,
            "name": name, "expected_exit": expected_exit,
            "actual_exit": actual_exit, "traceback": traceback,
            "expectation_met": passed, "diagnostic": diagnostic,
        }
        results.append(result)
        print(json.dumps(result, sort_keys=True))

    invalids = [row for row in results if row["case_kind"] == "invalid"]
    controls = [row for row in results if row["case_kind"] == "control"]
    summary = {
        "type": "summary",
        "invalid_total": len(invalids),
        "invalid_rejected": sum(row["actual_exit"] == 1 and not row["traceback"] for row in invalids),
        "invalid_false_passes": sum(row["actual_exit"] == 0 for row in invalids),
        "invalid_tracebacks": sum(row["traceback"] for row in invalids),
        "control_total": len(controls),
        "controls_accepted": sum(row["actual_exit"] == 0 for row in controls),
        "controls_rejected": sum(row["actual_exit"] != 0 and not row["traceback"] for row in controls),
        "control_tracebacks": sum(row["traceback"] for row in controls),
        "approval_blocked": any(not row["expectation_met"] for row in results),
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
