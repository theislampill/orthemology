#!/usr/bin/env python3
"""Validate bounded waking/somnic schemas, fixtures, and outline profiles.

This is an offline conformance validator.  It is not a recurrence analyzer,
ledger emitter, scheduler, writeback engine, or collective runtime.
"""
import json
import hashlib
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
ACTIVATION_PATH = ROOT / "examples" / "somnus" / "activation-contract-fixtures.yaml"
RECORDS_PATH = ROOT / "examples" / "somnus" / "somnus-record-fixtures.yaml"
INVENTORY_PATH = ROOT / "applications" / "agentic-runtime" / "SOMNUS-CANDIDATE-INVENTORY.yaml"
ADOPTION_PATH = ROOT / "applications" / "agentic-runtime" / "HERMES-WRITEBACK-ADOPTION-PROFILE.yaml"
COLLECTIVE_PATH = ROOT / "applications" / "agentic-runtime" / "COLLECTIVE-SOMNUS-TRANSCLUSION-PROFILE.yaml"
DECISION_PATH = ROOT / "docs" / "decisions" / "0035-somnic-orthing-and-activation-contracts.md"
MANUSCRIPT_PATH = ROOT / "manuscript" / "orthemma-ortheme-systems-revised-draft.md"

SCHEMA_NAMES = {
    "contracts": "activation-contract.schema.json",
    "orthing_events": "orthing-event.schema.json",
    "meta_orthability_assessments": "meta-orthability-assessment.schema.json",
    "somnus_runs": "somnus-run.schema.json",
    "somnic_assessments": "somnic-assessment.schema.json",
    "recurrence_reports": "residual-recurrence-report.schema.json",
}
AUX_SCHEMA_NAMES = {
    "activation_bundle": "activation-contract-fixtures.schema.json",
    "records_bundle": "somnus-record-fixtures.schema.json",
    "claim_status": "somnus-claim-status.schema.json",
    "candidate_inventory": "somnus-candidate-inventory.schema.json",
    "adoption_profile": "hermes-writeback-adoption-profile.schema.json",
    "collective_profile": "collective-somnus-transclusion-profile.schema.json",
}
FIXTURE_CLASSES = {"positive", "negative-near-boundary", "indeterminate", "overlap"}
TRI_STATE = {"applicable", "inapplicable", "indeterminate"}


def _load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), None
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return None, "%s unavailable or malformed: %s" % (path.name, exc)


def _load_schemas():
    schemas = {}
    issues = []
    for name in list(SCHEMA_NAMES.values()) + list(AUX_SCHEMA_NAMES.values()):
        path = SCHEMA_DIR / name
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            schemas[name] = schema
        except (OSError, UnicodeError, ValueError) as exc:
            issues.append("schema %s unavailable or malformed: %s" % (name, exc))
        except Exception as exc:  # jsonschema reports schema contract failures here
            issues.append("schema %s does not compile: %s" % (name, exc))
    return schemas, issues


def _schema_issues(label, value, schema, store):
    try:
        errors = sorted(
            Draft202012Validator(schema).iter_errors(value),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
    except Exception as exc:
        return ["%s schema resolution failed: %s" % (label, exc)]
    result = []
    for error in errors:
        locus = ".".join(str(part) for part in error.absolute_path) or "<root>"
        result.append("%s schema %s: %s" % (label, locus, error.message))
    return result


def _objects(document, key, issues, label):
    if not isinstance(document, dict):
        issues.append("%s must be an object" % label)
        return []
    rows = document.get(key)
    if not isinstance(rows, list):
        issues.append("%s.%s must be an array" % (label, key))
        return []
    if any(not isinstance(row, dict) for row in rows):
        issues.append("%s.%s contains a non-object record" % (label, key))
    return [row for row in rows if isinstance(row, dict)]


def _by(rows, key):
    return {row.get(key): row for row in rows if isinstance(row.get(key), str)}


def _mapping(value, label, issues):
    if isinstance(value, dict):
        return value
    issues.append("%s must be an object" % label)
    return {}


def _string_set(value):
    """Return only schema-valid string members for semantic set operations.

    JSON Schema remains the diagnostic owner for malformed containers or
    members.  Semantic validation must not hash attacker-controlled nested
    lists or mappings after that schema failure has already been recorded.
    """
    if not isinstance(value, list):
        return set()
    return {member for member in value if isinstance(member, str)}


def _string_tuple_key(*values):
    """Return a hashable semantic key only when every component is a string."""
    return tuple(values) if all(isinstance(value, str) for value in values) else None


def _string_lookup(index, key):
    """Look up only schema-valid string IDs in a registry."""
    return index.get(key) if isinstance(key, str) else None


def _string_member(index, key):
    """Test registry membership without hashing malformed nested values."""
    return isinstance(key, str) and key in index


def _unique_index(rows, key, label, issues):
    index = {}
    for row in rows:
        value = row.get(key)
        if not isinstance(value, str) or not value:
            issues.append("%s record lacks %s" % (label, key))
        elif value in index:
            issues.append("%s duplicates %s %s" % (label, key, value))
        else:
            index[value] = row
    return index


def _parse_time(value, label, issues):
    if not isinstance(value, str):
        issues.append("%s must be an ISO date-time" % label)
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        issues.append("%s must be an ISO date-time" % label)
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _activation_issues(document, schemas, store):
    issues = []
    issues += _schema_issues(
        "activation", document, schemas[AUX_SCHEMA_NAMES["activation_bundle"]], store
    )
    contracts = _objects(document, "contracts", issues, "activation")
    evaluators = _objects(document, "evaluators", issues, "activation")
    authoring_records = _objects(document, "authoring_records", issues, "activation")
    outcomes = _objects(document, "fixture_outcomes", issues, "activation")
    for index, contract in enumerate(contracts):
        issues += _schema_issues("activation.contracts[%d]" % index, contract,
                                 schemas[SCHEMA_NAMES["contracts"]], store)
    if {row.get("fixture_class") for row in outcomes if isinstance(row.get("fixture_class"), str)} != FIXTURE_CLASSES:
        issues.append("fixture outcomes must cover positive, negative-near-boundary, indeterminate, and overlap")
    outcome_by_id = _unique_index(outcomes, "fixture_id", "activation outcomes", issues)
    authoring_by_id = _unique_index(
        authoring_records, "provenance_record_id", "activation authoring records", issues
    )
    contract_by_key = {}
    for contract in contracts:
        key = _string_tuple_key(contract.get("contract_id"), contract.get("contract_version"))
        if key is None:
            continue
        if key in contract_by_key:
            issues.append("activation contracts duplicate %s@%s" % key)
        contract_by_key[key] = contract
    evaluator_by_key = {}
    for evaluator in evaluators:
        key = _string_tuple_key(evaluator.get("evaluator_id"), evaluator.get("evaluator_version"))
        if key is None:
            continue
        if key in evaluator_by_key:
            issues.append("activation evaluators duplicate %s@%s" % key)
        evaluator_by_key[key] = evaluator
        if _string_set(evaluator.get("result_vocabulary")) != TRI_STATE:
            issues.append("orthability evaluator %s must preserve the tri-state vocabulary" % evaluator.get("evaluator_id"))

    assessments_by_contract = defaultdict(list)
    for outcome in outcomes:
        fixture_id = outcome.get("fixture_id")
        fixture_class = outcome.get("fixture_class")
        assessments = outcome.get("claimant_assessments")
        if not isinstance(assessments, list) or not assessments or any(not isinstance(row, dict) for row in assessments):
            issues.append("fixture %s lacks structured claimant assessments" % fixture_id)
            continue
        contract_keys_in_fixture = []
        for assessment in assessments:
            for field in ("activation_contract_id", "activation_contract_version", "evaluator_id", "evaluator_version"):
                if not isinstance(assessment.get(field), str) or not assessment.get(field):
                    issues.append("fixture %s claimant assessment missing contract/evaluator version field %s" % (fixture_id, field))
            key = _string_tuple_key(assessment.get("activation_contract_id"), assessment.get("activation_contract_version"))
            contract = contract_by_key.get(key)
            if contract is None:
                issues.append("fixture %s references unknown activation contract/version" % fixture_id)
                continue
            evaluator_key = _string_tuple_key(
                assessment.get("evaluator_id"), assessment.get("evaluator_version")
            )
            if evaluator_key is None or evaluator_key not in evaluator_by_key:
                issues.append("fixture %s references unknown evaluator/version" % fixture_id)
            if assessment.get("claimant_id") != contract.get("claimant_id"):
                issues.append("fixture %s claimant does not match its activation contract" % fixture_id)
            contract_keys_in_fixture.append("%s@%s" % key)
            assessments_by_contract[key].append((fixture_class, fixture_id, assessment))

            findings = _mapping(assessment.get("property_findings"), "fixture %s property_findings" % fixture_id, issues)
            finding_sets = {}
            for field in ("satisfied", "absent", "indeterminate"):
                values = findings.get(field)
                if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
                    issues.append("fixture %s property_findings.%s must be an array of IDs" % (fixture_id, field))
                    values = []
                finding_sets[field] = _string_set(values)
            if any(finding_sets[left] & finding_sets[right] for left, right in (("satisfied", "absent"), ("satisfied", "indeterminate"), ("absent", "indeterminate"))):
                issues.append("fixture %s property findings must be mutually exclusive" % fixture_id)
            required = _string_set(contract.get("required_properties"))
            if set().union(*finding_sets.values()) != required:
                issues.append("fixture %s must disposition every required property for its contract" % fixture_id)
            exclusions = assessment.get("observed_exclusions")
            if not isinstance(exclusions, list):
                issues.append("fixture %s observed_exclusions must be an array" % fixture_id)
                exclusions = []
            controlling_exclusion = bool(_string_set(exclusions) & _string_set(contract.get("exclusion_indicators")))
            result = assessment.get("result")
            if result not in TRI_STATE:
                issues.append("fixture %s has result outside tri-state vocabulary" % fixture_id)
            elif result == "applicable" and (required != finding_sets["satisfied"] or controlling_exclusion):
                issues.append("fixture %s cannot infer applicability while required properties are absent, indeterminate, or excluded" % fixture_id)
            elif result == "inapplicable" and not (finding_sets["absent"] or controlling_exclusion):
                issues.append("fixture %s cannot be inapplicable when all required properties are satisfied and no exclusion controls" % fixture_id)
            elif result == "indeterminate" and not finding_sets["indeterminate"]:
                issues.append("fixture %s indeterminate result requires an indeterminate required property" % fixture_id)

        if fixture_class == "overlap":
            conflict = _mapping(outcome.get("conflict"), "overlap fixture %s conflict" % fixture_id, issues)
            named = conflict.get("claimant_contracts")
            if (not isinstance(named, list) or len(_string_set(named)) < 2
                    or not _string_set(contract_keys_in_fixture) <= _string_set(named)
                    or conflict.get("disposition") not in {"provisional_multi_claimant", "hold", "defer"}
                    or conflict.get("conflict_unresolved") is not True
                    or not conflict.get("authorization_rule_id")):
                issues.append("overlap fixture %s requires a structured conflict and disposition" % fixture_id)

    for key, contract in contract_by_key.items():
        if contract.get("status") != "accepted":
            continue
        refs = contract.get("fixture_outcomes")
        if not isinstance(refs, list) or not refs:
            issues.append("accepted contract %s requires fixture outcomes" % contract.get("contract_id"))
            continue
        if len(_string_set(refs)) != len(refs) or any(ref not in outcome_by_id for ref in _string_set(refs)):
            issues.append("accepted contract %s has unresolved fixture outcomes" % contract.get("contract_id"))
            continue
        represented = {
            fixture_class for fixture_class, fixture_id, _ in assessments_by_contract.get(key, [])
            if fixture_id in refs
        }
        if represented != FIXTURE_CLASSES:
            issues.append("accepted contract %s requires per-contract positive, negative-near-boundary, indeterminate, and overlap assessments" % contract.get("contract_id"))
        authorship = _mapping(
            contract.get("authorship"),
            "activation contract %s authorship" % contract.get("contract_id"), issues,
        )
        if authorship.get("mode") == "bootstrap_provenance":
            record = _string_lookup(authoring_by_id, authorship.get("provenance_record_id"))
            expected_ref = "%s@%s" % key
            if (record is None or record.get("capture_mode") != "bootstrap_provenance"
                    or record.get("immutable") is not True
                    or record.get("selected_contract_ref") != expected_ref
                    or _string_set(record.get("fixture_ids")) != _string_set(refs)):
                issues.append("accepted contract %s requires an exact immutable bootstrap authoring record" % contract.get("contract_id"))
    return issues


def _records_issues(document, activation, schemas, store):
    issues = []
    issues += _schema_issues(
        "records", document, schemas[AUX_SCHEMA_NAMES["records_bundle"]], store
    )
    if isinstance(document, dict):
        issues += _schema_issues(
            "records.claim_status", document.get("claim_status"),
            schemas[AUX_SCHEMA_NAMES["claim_status"]], store,
        )
    collections = {}
    for key in SCHEMA_NAMES:
        if key == "contracts":
            continue
        collections[key] = _objects(document, key, issues, "records")
        schema = schemas[SCHEMA_NAMES[key]]
        for index, row in enumerate(collections[key]):
            issues += _schema_issues("records.%s[%d]" % (key, index), row, schema, store)
    events = collections["orthing_events"]
    runs = collections["somnus_runs"]
    assessments = collections["somnic_assessments"]
    reports = collections["recurrence_reports"]
    meta_assessments = collections["meta_orthability_assessments"]

    activation_contract_rows = _objects(activation, "contracts", issues, "activation")
    activation_evaluator_rows = _objects(activation, "evaluators", issues, "activation")
    activation_contract_by_key = {
        key: row for row in activation_contract_rows
        if (key := _string_tuple_key(row.get("contract_id"), row.get("contract_version"))) is not None
    }
    activation_evaluator_by_key = {
        key: row for row in activation_evaluator_rows
        if (key := _string_tuple_key(row.get("evaluator_id"), row.get("evaluator_version"))) is not None
    }

    identity = _mapping(document.get("identity_fixture"), "records.identity_fixture", issues)
    identity_fields = (
        "session_ids", "occurrence_ids", "episode_ids", "orthing_ids",
        "claim_attempt_ids", "orthability_assessment_ids",
    )
    identity_sets = {}
    for field in identity_fields:
        values = identity.get(field)
        if not isinstance(values, list) or not values or any(not isinstance(value, str) for value in values):
            issues.append("records.identity_fixture.%s must be a nonempty ID array" % field)
            values = []
        identity_sets[field] = _string_set(values)
    for index, left in enumerate(identity_fields):
        for right in identity_fields[index + 1:]:
            if identity_sets[left] & identity_sets[right]:
                issues.append("global identity levels %s and %s must remain distinct" % (left, right))

    identity_rows = _objects(document, "identity_registry", issues, "records")
    identity_by_id = _unique_index(identity_rows, "identity_id", "typed identity registry", issues)
    identity_kind_by_id = {key: row.get("identity_kind") for key, row in identity_by_id.items()}
    fixture_kind = {
        "session_ids": "session", "episode_ids": "episode",
        "occurrence_ids": "occurrence", "orthing_ids": "orthing",
        "claim_attempt_ids": "claim_attempt",
        "orthability_assessment_ids": "orthability_assessment",
    }
    for field, kind in fixture_kind.items():
        for identity_id in identity_sets[field]:
            if identity_kind_by_id.get(identity_id) != kind:
                issues.append("identity fixture %s must resolve as typed %s" % (identity_id, kind))

    provenance_rows = _objects(document, "provenance_records", issues, "records")
    provenance_by_id = _unique_index(
        provenance_rows, "provenance_record_id", "provenance registry", issues
    )

    route_rows = _objects(document, "claimant_routing_cases", issues, "records")
    selected_route_pairs = {}
    for route in route_rows:
        route_assessments = route.get("claimant_assessments")
        if not isinstance(route_assessments, list):
            continue
        by_claimant = {
            row.get("claimant_id"): row for row in route_assessments
            if isinstance(row, dict) and isinstance(row.get("claimant_id"), str)
        }
        selected = _string_lookup(by_claimant, route.get("selected_claimant_id"))
        if route.get("route_status") == "selected" and (
                selected is None or selected.get("result") != "applicable"):
            issues.append("claimant route %s may select only an applicable claimant" % route.get("case_id"))
        elif route.get("route_status") == "selected" and selected is not None:
            occurrence_id = route.get("occurrence_id")
            if isinstance(occurrence_id, str):
                selected_route_pairs[occurrence_id] = (
                    selected.get("claim_attempt_id"), selected.get("orthability_assessment_id")
                )
        for row in route_assessments:
            if not isinstance(row, dict):
                continue
            if not _string_member(identity_sets["claim_attempt_ids"], row.get("claim_attempt_id")):
                issues.append("claimant route %s has unresolved claim attempt" % route.get("case_id"))
            if not _string_member(identity_sets["orthability_assessment_ids"], row.get("orthability_assessment_id")):
                issues.append("claimant route %s has unresolved orthability assessment" % route.get("case_id"))
        residuals = _string_set(route.get("retained_residual_claimants"))
        inapplicable = _string_set(route.get("retained_inapplicable_claimants"))
        expected_residuals = {key for key, row in by_claimant.items() if row.get("result") == "indeterminate"}
        expected_inapplicable = {key for key, row in by_claimant.items() if row.get("result") == "inapplicable"}
        if residuals != expected_residuals or inapplicable != expected_inapplicable:
            issues.append("claimant route %s must retain indeterminate and inapplicable attempts" % route.get("case_id"))

    evidence_rows = _objects(document, "evidence_records", issues, "records")
    evidence_by_id = _unique_index(evidence_rows, "evidence_id", "evidence registry", issues)
    evidence_timing = {key: row.get("timing") for key, row in evidence_by_id.items()}
    subject_rows = _objects(document, "subject_records", issues, "records")
    subject_by_id = _unique_index(subject_rows, "subject_id", "subject registry", issues)
    for subject_id, subject in subject_by_id.items():
        if subject.get("subject_kind") in {"waking_orthing", "counterexample"}:
            if identity_kind_by_id.get(subject_id) != "orthing":
                issues.append("subject %s must resolve as a globally typed orthing identity" % subject_id)
    for contract in activation_contract_rows:
        authorship = contract.get("authorship")
        if isinstance(authorship, dict) and authorship.get("mode") == "normal":
            orthing_id = authorship.get("orthing_id")
            if (not _string_member(subject_by_id, orthing_id)
                    or _string_lookup(identity_kind_by_id, orthing_id) != "orthing"):
                issues.append("normal activation-contract authorship must resolve to a typed authoring orthing")
    delta_rows = _objects(document, "material_deltas", issues, "records")
    delta_by_id = _unique_index(delta_rows, "material_delta_id", "material delta registry", issues)
    event_by_id = _unique_index(events, "event_id", "orthing events", issues)

    event_groups = defaultdict(list)
    for document_index, event in enumerate(events):
        event_id = event.get("event_id")
        identities = [
            event.get(name) for name in (
                "session_id", "episode_id", "occurrence_id", "claim_attempt_id",
                "orthability_assessment_id", "orthing_id",
            ) if event.get(name) is not None
        ]
        string_identities = [identity for identity in identities if isinstance(identity, str)]
        if len(string_identities) == len(identities) and len(identities) != len(set(string_identities)):
            issues.append("event %s collapses distinct identity levels" % event_id)
        event_identity_fields = {
            "session_id": "session", "episode_id": "episode",
            "occurrence_id": "occurrence", "orthing_id": "orthing",
            "actor_id": "actor",
        }
        for field, kind in event_identity_fields.items():
            if _string_lookup(identity_kind_by_id, event.get(field)) != kind:
                issues.append("event %s %s must resolve through the global typed identity registry" % (event_id, field))
        for field, kind in (
                ("claim_attempt_id", "claim_attempt"),
                ("orthability_assessment_id", "orthability_assessment")):
            value = event.get(field)
            if value is not None and _string_lookup(identity_kind_by_id, value) != kind:
                issues.append("event %s %s must resolve through the global typed identity registry" % (event_id, field))
        provenance = _string_lookup(provenance_by_id, event.get("provenance_record_id"))
        if (provenance is None or provenance.get("immutable") is not True
                or provenance.get("capture_mode") != event.get("capture_mode")
                or provenance.get("source_revision") != event.get("source_revision")):
            issues.append("event %s capture classification must resolve to an exact immutable provenance record" % event_id)
        if provenance is not None and provenance.get("source_case") == "R7E" and provenance.get("capture_mode") != "retrospective_reconstruction":
            issues.append("R7E retrospective reconstruction cannot be relabeled as live capture")
        if event.get("claim_attempt_id") is not None and not _string_member(identity_sets["claim_attempt_ids"], event.get("claim_attempt_id")):
            issues.append("event %s has unresolved claim attempt identity" % event_id)
        if event.get("orthability_assessment_id") is not None and not _string_member(identity_sets["orthability_assessment_ids"], event.get("orthability_assessment_id")):
            issues.append("event %s has unresolved orthability assessment identity" % event_id)
        if event.get("event_type") == "occurrence_apprehended" and (
                event.get("claim_attempt_id") is not None
                or event.get("orthability_assessment_id") is not None):
            issues.append("event %s must capture the occurrence before claimant evaluation" % event_id)
        if event.get("event_type") == "orthability_assessed" and (
                not event.get("claim_attempt_id") or not event.get("orthability_assessment_id")):
            issues.append("event %s orthability assessment requires claimant identities" % event_id)
        if event.get("event_type") == "route_selected":
            selected_pair = _string_lookup(selected_route_pairs, event.get("occurrence_id"))
            event_pair = (event.get("claim_attempt_id"), event.get("orthability_assessment_id"))
            if selected_pair is None or event_pair != selected_pair:
                issues.append("event %s selected route must match the applicable claimant-routing record" % event_id)
        issues += _evidence_timing_issues(event_id, event.get("evidence_timing"), evidence_timing)
        group_key = _string_tuple_key(
            event.get("session_id"), event.get("episode_id"),
            event.get("occurrence_id"), event.get("orthing_id"),
        )
        if group_key is not None:
            event_groups[group_key].append((document_index, event))

    live_lifecycle_seen = False
    for group, rows in event_groups.items():
        sequence_values = [row.get("sequence") for _, row in rows]
        if any(not isinstance(value, int) for value in sequence_values) or len(sequence_values) != len(set(sequence_values)):
            issues.append("orthing event lifecycle %s requires unique integer sequence values" % (group,))
        ordered = sorted(rows, key=lambda pair: pair[1].get("sequence") if isinstance(pair[1].get("sequence"), int) else 0)
        parsed_times = [_parse_time(row.get("occurred_at"), "event %s occurred_at" % row.get("event_id"), issues) for _, row in ordered]
        if any(left and right and left >= right for left, right in zip(parsed_times, parsed_times[1:])):
            issues.append("orthing event lifecycle %s must be strictly chronological" % (group,))
        live = [row for _, row in ordered if row.get("capture_mode") == "live_capture"]
        if live:
            if not live or live[0].get("event_type") != "occurrence_apprehended":
                issues.append("live orthing lifecycle %s must begin with occurrence capture" % (group,))
            if any(row.get("event_type") == "orthability_assessed" for row in live):
                live_lifecycle_seen = True
            event_positions = defaultdict(list)
            for position, row in enumerate(live):
                event_positions[row.get("event_type")].append(position)
            if event_positions["route_selected"]:
                if (not event_positions["orthability_assessed"]
                        or min(event_positions["orthability_assessed"]) >= min(event_positions["route_selected"])):
                    issues.append("live orthing lifecycle %s must preserve capture then assessment then route order" % (group,))
    if not live_lifecycle_seen:
        issues.append("records require an incremental capture-before-claimant-assessment lifecycle")

    run_by_id = _unique_index(runs, "somnus_run_id", "somnus runs", issues)
    assessment_by_id = _unique_index(assessments, "assessment_id", "somnic assessments", issues)
    report_by_id = _unique_index(reports, "recurrence_report_id", "recurrence reports", issues)
    meta_by_id = _unique_index(meta_assessments, "meta_orthability_assessment_id", "meta-orthability assessments", issues)
    cross_kind_output_ids = set(assessment_by_id) & set(report_by_id)
    if cross_kind_output_ids:
        issues.append("somnic assessment and recurrence-report output IDs must be globally unique across kinds: %s" % sorted(cross_kind_output_ids))
    output_by_id = dict(assessment_by_id)
    output_by_id.update(report_by_id)

    proposal_rows = _objects(document, "proposals", issues, "records")
    proposal_by_id = _unique_index(proposal_rows, "proposal_id", "proposals", issues)
    auth_rows = _objects(document, "authorizations", issues, "records")
    auth_by_id = _unique_index(auth_rows, "authorization_id", "authorizations", issues)
    application_rows = _objects(document, "applications", issues, "records")
    application_by_id = _unique_index(application_rows, "application_id", "applications", issues)
    successor_rows = _objects(document, "successor_states", issues, "records")
    successor_by_id = _unique_index(successor_rows, "successor_state_id", "successor states", issues)
    outcome_rows = _objects(document, "outcome_evaluations", issues, "records")
    outcome_by_id = _unique_index(outcome_rows, "outcome_evaluation_id", "outcome evaluations", issues)

    for meta in meta_assessments:
        meta_id = meta.get("meta_orthability_assessment_id")
        subject_ids = _string_set(meta.get("subject_ids"))
        if not subject_ids or any(subject_id not in subject_by_id for subject_id in subject_ids):
            issues.append("meta-orthability assessment %s has unresolved or empty subject scope" % meta_id)
        expected_kind = meta.get("subject_kind")
        if any(subject_by_id[subject_id].get("subject_kind") != expected_kind
               for subject_id in subject_ids if subject_id in subject_by_id):
            issues.append("meta-orthability assessment %s subject kind disagrees with its exact subject scope" % meta_id)
        if meta.get("result") == "applicable_assessable" and meta.get("assessable") is not True:
            issues.append("meta-orthability assessment %s has incoherent assessability" % meta.get("meta_orthability_assessment_id"))
        if meta.get("result") != "applicable_assessable" and meta.get("assessable") is not False:
            issues.append("meta-orthability assessment %s has incoherent non-assessability" % meta.get("meta_orthability_assessment_id"))
        contract_key = _string_tuple_key(
            meta.get("activation_contract_id"), meta.get("activation_contract_version")
        )
        evaluator_key = _string_tuple_key(
            meta.get("orthability_evaluator_id"), meta.get("orthability_evaluator_version")
        )
        contract = activation_contract_by_key.get(contract_key)
        if contract is None or contract.get("status") != "accepted":
            issues.append("meta-orthability assessment %s must resolve an exact accepted activation contract/version" % meta_id)
            continue
        if evaluator_key not in activation_evaluator_by_key:
            issues.append("meta-orthability assessment %s must resolve an exact evaluator/version" % meta_id)
        property_sets = {
            field: _string_set(meta.get(field))
            for field in ("satisfied_properties", "absent_properties", "indeterminate_properties")
        }
        if any(property_sets[left] & property_sets[right] for left, right in (
                ("satisfied_properties", "absent_properties"),
                ("satisfied_properties", "indeterminate_properties"),
                ("absent_properties", "indeterminate_properties"))):
            issues.append("meta-orthability assessment %s property partitions must be mutually exclusive" % meta_id)
        required = _string_set(contract.get("required_properties"))
        if set().union(*property_sets.values()) != required:
            issues.append("meta-orthability assessment %s must disposition the exact required property set" % meta_id)
        exclusions = _string_set(meta.get("observed_exclusions"))
        controlling_exclusion = bool(exclusions & _string_set(contract.get("exclusion_indicators")))
        evidence_ids = _string_set(meta.get("evidence_state_ids"))
        if any(evidence_id not in evidence_by_id for evidence_id in evidence_ids):
            issues.append("meta-orthability assessment %s has unresolved evidence state" % meta_id)
        result = meta.get("result")
        non_reason = meta.get("non_assessment_reason")
        if result == "applicable_assessable":
            if (property_sets["satisfied_properties"] != required
                    or property_sets["absent_properties"]
                    or property_sets["indeterminate_properties"]
                    or controlling_exclusion or not evidence_ids or non_reason is not None):
                issues.append("meta-orthability assessment %s applicable result contradicts properties, exclusions, evidence, or non-assessment reason" % meta_id)
        elif result == "inapplicable":
            if (not property_sets["absent_properties"] and not controlling_exclusion) or not non_reason:
                issues.append("meta-orthability assessment %s inapplicable result requires absence/exclusion and a non-assessment reason" % meta_id)
        elif result == "indeterminate":
            if not property_sets["indeterminate_properties"] or not non_reason:
                issues.append("meta-orthability assessment %s indeterminate result requires indeterminate properties and a non-assessment reason" % meta_id)
        elif result == "record_insufficient":
            if evidence_ids or not non_reason:
                issues.append("meta-orthability assessment %s record-insufficient result requires missing evidence and a reason" % meta_id)

    zero_proposal_dispositions = {"no_change", "investigation", "evidence_request", "preserve_residual"}
    assessment_time_by_id = {}
    prior_graph = defaultdict(set)
    for assessment in assessments:
        aid = assessment.get("assessment_id")
        if assessment.get("target_history_mutated") is not False or assessment.get("explicit_non_mutation") is not True:
            issues.append("assessment %s violates the append-only target history rule" % aid)
        if assessment.get("retroactive_conformity_rewrite") is not False:
            issues.append("assessment %s rewrites historical conformity" % aid)
        targets = _string_set(assessment.get("target_orthing_ids"))
        if not targets:
            issues.append("assessment %s lacks target orthing identity" % aid)
        unresolved_targets = [target for target in targets if target not in subject_by_id]
        if unresolved_targets:
            issues.append("assessment %s has unresolved target subjects %s" % (aid, unresolved_targets))
        t2 = _mapping(assessment.get("t2_configuration"), "assessment %s t2_configuration" % aid, issues)
        assessed_at = _parse_time(t2.get("assessed_at"), "assessment %s assessed_at" % aid, issues)
        if isinstance(aid, str) and assessed_at is not None:
            assessment_time_by_id[aid] = assessed_at
        for target in targets:
            subject = _string_lookup(subject_by_id, target)
            if subject:
                t1 = _parse_time(subject.get("t1_at"), "subject %s t1_at" % target, issues)
                if t1 and assessed_at and assessed_at <= t1:
                    issues.append("assessment %s t2 must be later than target %s t1" % (aid, target))
        if not _string_member(run_by_id, assessment.get("somnus_run_id")):
            issues.append("assessment %s has unresolved somnus run" % aid)
        gate = _string_lookup(meta_by_id, assessment.get("meta_orthability_assessment_id"))
        if gate is None:
            issues.append("assessment %s has unresolved meta-orthability assessment" % aid)
        else:
            if gate.get("result") != "applicable_assessable" or gate.get("assessable") is not True:
                issues.append("assessment %s requires an applicable and assessable meta-orthability gate" % aid)
            if _string_set(gate.get("subject_ids")) != targets:
                issues.append("assessment %s meta-orthability gate must exactly scope its target subject set" % aid)
        for prior in _string_set(assessment.get("prior_assessment_ids")):
            if prior not in assessment_by_id:
                issues.append("assessment %s has unresolved prior assessment" % aid)
            elif isinstance(aid, str):
                prior_graph[aid].add(prior)
        if assessment.get("target_history_digest_mode") != "derived-subject-record-sha256-v1":
            issues.append("assessment %s target history digest must declare the derived verification mode" % aid)
        if targets and not unresolved_targets:
            payload = [subject_by_id[target] for target in sorted(targets)]
            canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
            expected_digest = hashlib.sha256(canonical).hexdigest()
            if assessment.get("target_history_digest") != expected_digest:
                issues.append("assessment %s target history digest must be derived from its authoritative subject records" % aid)
        issues += _evidence_timing_issues(aid, assessment.get("evidence_timing"), evidence_timing)
        proposals = _string_set(assessment.get("proposal_ids"))
        disposition = assessment.get("intervention_disposition")
        assessment_result = assessment.get("assessment_result")
        if assessment_result == "no_change" and disposition != "no_change":
            issues.append("assessment %s no-change result requires a no-change disposition" % aid)
        if assessment_result == "no_change" and proposals:
            issues.append("assessment %s no-change result cannot carry a mutation proposal" % aid)
        if assessment_result == "unassessable" and disposition not in {
                "investigation", "evidence_request", "preserve_residual"}:
            issues.append("assessment %s unassessable result cannot produce a mutation disposition" % aid)
        if disposition in zero_proposal_dispositions and proposals:
            issues.append("assessment %s %s disposition cannot carry a proposal" % (aid, disposition.replace("_", "-")))
        if disposition == "alternative_proposals" and len(proposals) < 2:
            issues.append("assessment %s alternative proposal disposition requires at least two proposals" % aid)
        if disposition == "proposal" and len(proposals) != 1:
            issues.append("assessment %s proposal disposition requires exactly one proposal" % aid)
        for proposal_id in proposals:
            proposal = _string_lookup(proposal_by_id, proposal_id)
            if proposal is None:
                issues.append("assessment %s references unknown proposal %s" % (aid, proposal_id))
            elif proposal.get("supporting_assessment_id") != aid:
                issues.append("assessment %s proposal %s points to a different assessment" % (aid, proposal_id))
        chain_specs = (
            ("authorization_refs", auth_by_id),
            ("application_refs", application_by_id),
            ("outcome_evaluation_refs", outcome_by_id),
        )
        for field, registry in chain_specs:
            refs = _string_set(assessment.get(field))
            if any(ref not in registry for ref in refs):
                issues.append("assessment %s has unresolved %s" % (aid, field))

    for assessment_id, priors in prior_graph.items():
        for prior_id in priors:
            current_time = assessment_time_by_id.get(assessment_id)
            prior_time = assessment_time_by_id.get(prior_id)
            if prior_id == assessment_id or (
                    current_time is not None and prior_time is not None and prior_time >= current_time):
                issues.append("assessment %s prior-assessment graph must be acyclic and strictly time-ordered" % assessment_id)
    visit_state = {}
    def visit_prior(node):
        state = visit_state.get(node, 0)
        if state == 1:
            return True
        if state == 2:
            return False
        visit_state[node] = 1
        if any(visit_prior(prior) for prior in prior_graph.get(node, ())):
            return True
        visit_state[node] = 2
        return False
    if any(visit_prior(node) for node in prior_graph):
        issues.append("prior-assessment references must form an acyclic graph")

    closed_ids = {
        row.get("assessment_id") for row in assessments
        if row.get("closure_status") == "closed" and isinstance(row.get("assessment_id"), str)
    }
    idempotency_bindings = {}
    declared_output_owners = defaultdict(list)
    for run in runs:
        rid = run.get("somnus_run_id")
        anchors = _string_set(run.get("anchor_subject_ids"))
        comparators = _string_set(run.get("historical_comparator_ids"))
        if anchors & comparators:
            issues.append("run %s anchor frontier and historical comparators must be disjoint" % rid)
        for ref in anchors | comparators:
            if ref not in subject_by_id:
                issues.append("run %s has unresolved anchor/comparator %s" % (rid, ref))
        reopens = _string_set(run.get("reopens_subject_ids"))
        deltas = _string_set(run.get("material_delta_ids"))
        if any(delta not in delta_by_id for delta in deltas):
            issues.append("run %s has unresolved material delta" % rid)
        if reopens and not deltas:
            issues.append("run %s reopens a subject without a material delta" % rid)
        for subject in anchors & closed_ids:
            if subject not in reopens or not deltas:
                issues.append("run %s automatically requeues closed assessment %s without material delta" % (rid, subject))
        if comparators & reopens:
            issues.append("run %s reopens a historical comparator merely to use it" % rid)
        expected_comparators_reopened = bool(comparators & reopens)
        if run.get("historical_comparators_reopened") is not expected_comparators_reopened:
            issues.append("run %s historical-comparator reopened assertion must be recomputed" % rid)
        if not reopens <= anchors:
            issues.append("run %s reopened subjects must enter the anchor frontier" % rid)
        started = _parse_time(run.get("started_at"), "run %s started_at" % rid, issues)
        completed = _parse_time(run.get("completed_at"), "run %s completed_at" % rid, issues)
        if started and completed and started >= completed:
            issues.append("run %s must complete after it starts" % rid)
        outputs = sorted(_string_set(run.get("output_ids")))
        if any(output not in output_by_id for output in outputs):
            issues.append("run %s has unresolved output IDs" % rid)
        for output in outputs:
            declared_output_owners[output].append(rid)
            output_record = output_by_id.get(output)
            if output_record is not None and output_record.get("somnus_run_id") != rid:
                issues.append("run %s output %s belongs to a different run" % (rid, output))
            output_time = None
            if output in assessment_by_id:
                output_time = _parse_time(
                    _mapping(output_record.get("t2_configuration"), "output %s t2_configuration" % output, issues).get("assessed_at"),
                    "output %s assessed_at" % output, issues,
                )
            elif output in report_by_id:
                output_time = _parse_time(output_record.get("emitted_at"), "output %s emitted_at" % output, issues)
            if started and completed and output_time and not (started <= output_time <= completed):
                issues.append("run %s output %s timestamp must fall within its owning run interval" % (rid, output))
        signature = {
            "operation_id": run.get("operation_id"),
            "operation_version": run.get("operation_version"),
            "anchors": sorted(anchors),
            "reference_corpus_revision": run.get("reference_corpus_revision"),
            "comparators": sorted(comparators),
            "selection_rule": run.get("selection_rule"),
            "governing_versions": sorted(_string_set(run.get("governing_versions"))),
            "material_deltas": sorted(deltas),
            "reopens": sorted(reopens),
        }
        canonical_input = json.dumps(signature, sort_keys=True, separators=(",", ":"))
        canonical_output = json.dumps(sorted(outputs), separators=(",", ":"))
        key = run.get("idempotency_key")
        if isinstance(key, str):
            prior = idempotency_bindings.get(key)
            if prior and prior[0] != canonical_input:
                issues.append("idempotency key %s is reused for different canonical input" % key)
            elif prior and prior[1] != canonical_output:
                issues.append("idempotency collision emits non-equivalent duplicate outputs")
            else:
                idempotency_bindings[key] = (canonical_input, canonical_output)

    for output_id, output_record in output_by_id.items():
        expected_run = output_record.get("somnus_run_id")
        owners = declared_output_owners.get(output_id, [])
        if owners != [expected_run]:
            issues.append(
                "output %s must be declared exactly once by its owning somnus run %s"
                % (output_id, expected_run)
            )

    source_family_rows = _objects(document, "source_family_records", issues, "records")
    source_family_by_id = _unique_index(
        source_family_rows, "source_family_id", "source family registry", issues
    )
    input_family_rows = _objects(document, "input_family_records", issues, "records")
    input_family_by_id = _unique_index(
        input_family_rows, "normalized_input_family_id", "input family registry", issues
    )
    support_record_rows = _objects(document, "recurrence_support_records", issues, "records")
    support_record_by_id = _unique_index(
        support_record_rows, "support_record_id", "recurrence support registry", issues
    )
    opportunity_rows = _objects(document, "opportunity_records", issues, "records")
    opportunity_by_id = _unique_index(
        opportunity_rows, "opportunity_id", "recurrence opportunity registry", issues
    )
    for opportunity_id, opportunity in opportunity_by_id.items():
        if not _string_member(subject_by_id, opportunity.get("subject_id")):
            issues.append("recurrence opportunity %s has unresolved subject provenance" % opportunity_id)
    policy_rows = _objects(document, "independence_policies", issues, "records")
    policy_by_id = _unique_index(policy_rows, "rule_id", "independence policy registry", issues)

    for report in reports:
        report_id = report.get("recurrence_report_id")
        if not _string_member(run_by_id, report.get("somnus_run_id")):
            issues.append("recurrence report %s has unresolved somnus run" % report_id)
        support = report.get("supporting_occurrences") if isinstance(report.get("supporting_occurrences"), list) else []
        support = [row for row in support if isinstance(row, dict)]
        for row in support:
            support_record = _string_lookup(support_record_by_id, row.get("support_record_id"))
            if support_record is None or support_record != row:
                issues.append("recurrence report %s support must resolve exactly to authoritative provenance records" % report_id)
            typed_dimensions = {
                "orthing_id": "orthing", "episode_id": "episode",
                "session_id": "session", "actor_id": "actor",
            }
            for field, kind in typed_dimensions.items():
                if _string_lookup(identity_kind_by_id, row.get(field)) != kind:
                    issues.append("recurrence report %s support %s must resolve as typed %s" % (report_id, field, kind))
            if not _string_member(source_family_by_id, row.get("source_family")):
                issues.append("recurrence report %s support has unresolved source-family provenance" % report_id)
            if not _string_member(input_family_by_id, row.get("normalized_input_family")):
                issues.append("recurrence report %s support has unresolved normalized-input provenance" % report_id)
        fields = {
            "episode_count": "episode_id", "session_count": "session_id",
            "normalized_input_family_count": "normalized_input_family",
            "actor_count": "actor_id", "source_family_count": "source_family",
        }
        recomputed = {
            dimension: len({row.get(field) for row in support if isinstance(row.get(field), str)})
            for dimension, field in fields.items()
        }
        unique_orthings = {row.get("orthing_id") for row in support if isinstance(row.get("orthing_id"), str)}
        unique_episodes = {row.get("episode_id") for row in support if isinstance(row.get("episode_id"), str)}
        if len(unique_orthings) != len(support):
            issues.append("recurrence support must count distinct episodes and orthings, not copies")
        if any(orthing not in subject_by_id for orthing in unique_orthings):
            issues.append("recurrence report %s has unresolved supporting orthing" % report_id)
        dims = _mapping(report.get("dependence_dimensions"), "recurrence report %s dependence_dimensions" % report_id, issues)
        for dimension, count in recomputed.items():
            if dims.get(dimension) != count:
                issues.append("recurrence report %s dependence %s must be recomputed from support" % (report_id, dimension))
        counterexamples = _string_set(report.get("counterexample_ids"))
        if any(ref not in subject_by_id for ref in counterexamples):
            issues.append("recurrence report %s has unresolved counterexample" % report_id)
        if dims.get("success_counterexample_count") != len(counterexamples):
            issues.append("recurrence report %s counterexample count must be recomputed" % report_id)
        times = [_parse_time(row.get("occurred_at"), "recurrence support occurred_at", issues) for row in support]
        valid_times = [value for value in times if value]
        if valid_times:
            span = max(valid_times) - min(valid_times)
            expected_span = "P%dD" % span.days if span.seconds == 0 else "PT%dS" % int(span.total_seconds())
            if dims.get("time_span") != expected_span:
                issues.append("recurrence report %s time span must be recomputed" % report_id)
        fingerprint = _mapping(report.get("fingerprint"), "recurrence report %s fingerprint" % report_id, issues)
        fingerprint_sources = _string_set(fingerprint.get("source_orthing_ids"))
        if fingerprint_sources != unique_orthings:
            issues.append("recurrence fingerprint sources must exactly match supporting orthings")
        support_input_families = {
            row.get("normalized_input_family") for row in support
            if isinstance(row.get("normalized_input_family"), str)
        }
        if support_input_families != {fingerprint.get("normalized_object")}:
            issues.append("recurrence fingerprint normalized object must bind exactly to its support input family")
        threshold = report.get("threshold")
        denominator = report.get("opportunity_denominator")
        if (not isinstance(threshold, int) or threshold > len(unique_orthings)
                or threshold > len(unique_episodes)):
            issues.append("recurrence threshold requires distinct orthing and episode support")
        opportunity_ids = _string_set(report.get("opportunity_ids"))
        opportunities = [opportunity_by_id[ref] for ref in opportunity_ids if ref in opportunity_by_id]
        if len(opportunities) != len(opportunity_ids):
            issues.append("recurrence opportunity denominator has unresolved opportunity IDs")
        if not isinstance(denominator, int) or denominator != len(opportunity_ids):
            issues.append("recurrence opportunity denominator must equal its resolvable opportunity-ID set")
        support_opportunity_subjects = {
            row.get("subject_id") for row in opportunities if row.get("classification") == "support"
        }
        counterexample_opportunity_subjects = {
            row.get("subject_id") for row in opportunities if row.get("classification") == "counterexample"
        }
        if support_opportunity_subjects != unique_orthings or counterexample_opportunity_subjects != counterexamples:
            issues.append("recurrence opportunity records must back the exact support and counterexample subjects")
        independence = _mapping(report.get("independence_assessment"), "recurrence report %s independence_assessment" % report_id, issues)
        evaluated = _mapping(independence.get("evaluated_dimensions"), "recurrence report %s evaluated independence dimensions" % report_id, issues)
        expected_evaluated = {
            dimension: recomputed[dimension] == len(support)
            for dimension in ("session_count", "normalized_input_family_count", "actor_count", "source_family_count")
        }
        if evaluated != expected_evaluated:
            issues.append("recurrence independence dimensions must be recomputed from support")
        required_dimensions = _string_set(independence.get("required_dimensions"))
        policy = _string_lookup(policy_by_id, independence.get("rule_id"))
        if policy is None:
            issues.append("recurrence independence assessment must resolve a declared fixed policy")
            policy_dimensions = set()
        else:
            policy_dimensions = _string_set(policy.get("required_dimensions"))
            if required_dimensions != policy_dimensions:
                issues.append("recurrence independence dimensions cannot weaken the declared policy")
        expected_pass = bool(policy_dimensions) and all(expected_evaluated.get(name) is True for name in policy_dimensions)
        if independence.get("passed") is not expected_pass:
            issues.append("recurrence independence result must evaluate its declared structured rule")
        expected_label = (
            policy.get("pass_label") if expected_pass else policy.get("fail_label")
        ) if policy is not None else ("independent episodes" if expected_pass else "distinct episodes")
        if independence.get("label") != expected_label:
            issues.append("recurrence independence label must match the evaluated rule")
        if report.get("systemic_defect_proven") is not False or report.get("threshold_effect") != "review_trigger_only":
            issues.append("recurrence threshold is a review trigger, not proof of a systemic defect")
        if report.get("emitted_actions"):
            issues.append("v0 recurrence cannot emit automatic patch, promotion, closure, or mutation actions")
        if report.get("causal_diagnosis") != "not-established" or report.get("proposed_intervention") != "not-produced-by-v0":
            issues.append("v0 must keep recurrence equality separate from causal diagnosis and intervention")

    for proposal in proposal_rows:
        proposal_id = proposal.get("proposal_id")
        mode = proposal.get("provenance_mode")
        if mode == "somnus_grounded_proposal" and not _string_member(assessment_by_id, proposal.get("supporting_assessment_id")):
            issues.append("grounded proposal %s lacks supporting assessment" % proposal_id)
        action = _mapping(proposal.get("proposed_action"), "proposal %s proposed_action" % proposal_id, issues)
        successor = _string_lookup(successor_by_id, action.get("successor_target_id"))
        if successor is None:
            issues.append("proposal %s has unresolved successor target" % proposal_id)
        elif successor.get("action_label") != action.get("action_label"):
            issues.append("proposal %s action must match its successor-state action" % proposal_id)
        _parse_time(proposal.get("proposed_at"), "proposal %s proposed_at" % proposal_id, issues)

    for auth in auth_rows:
        if not _string_member(proposal_by_id, auth.get("proposal_id")):
            issues.append("authorization %s has unresolved proposal" % auth.get("authorization_id"))
        if auth.get("source") != "independent_governance":
            issues.append("proposal cannot self-authorize; authorization source must be independent governance")
        proposal = _string_lookup(proposal_by_id, auth.get("proposal_id"))
        if proposal is not None:
            proposed_at = _parse_time(
                proposal.get("proposed_at"), "proposal %s proposed_at" % proposal.get("proposal_id"), issues
            )
            decided_at = _parse_time(
                auth.get("decided_at"), "authorization %s decided_at" % auth.get("authorization_id"), issues
            )
            if proposed_at and decided_at and proposed_at >= decided_at:
                issues.append("authorization %s must occur after its proposal" % auth.get("authorization_id"))

    outcome_application_ids = {
        row.get("application_id") for row in outcome_rows
        if isinstance(row.get("application_id"), str)
    }
    for application in application_rows:
        application_id = application.get("application_id")
        if application.get("assessment_history_mutated") is not False or application.get("proposal_history_mutated") is not False:
            issues.append("application failure or success cannot rewrite assessment/proposal history")
        proposal = _string_lookup(proposal_by_id, application.get("proposal_id"))
        authorization = _string_lookup(auth_by_id, application.get("authorization_id"))
        if proposal is None:
            issues.append("application %s proposal reference must resolve" % application_id)
        if authorization is None:
            issues.append("application %s authorization reference must resolve" % application_id)
        elif authorization.get("proposal_id") != application.get("proposal_id"):
            issues.append("application authorization must govern the same proposal")
        elif application.get("status") == "applied" and authorization.get("decision") != "authorized":
            issues.append("application cannot apply under rejected authorization")
        if application.get("status") == "applied":
            if proposal is not None and proposal.get("status") != "proposed":
                issues.append("applied mutation requires a non-rejected active proposal")
            if application.get("outcome_evaluation_required") is not True or application_id not in outcome_application_ids:
                issues.append("applied mutation requires later outcome evaluation")
            if not _string_member(successor_by_id, application.get("successor_state_id")):
                issues.append("applied mutation requires a resolvable successor state")
            else:
                successor = successor_by_id[application.get("successor_state_id")]
                successor_time = _parse_time(
                    successor.get("created_at"),
                    "successor %s created_at" % successor.get("successor_state_id"), issues,
                )
                applied_time = _parse_time(
                    application.get("applied_at"), "application %s applied_at" % application_id, issues
                )
                if successor_time and applied_time and successor_time != applied_time:
                    issues.append("applied mutation and successor state must share the authoritative application time")
        elif application.get("successor_state_id") is not None:
            issues.append("non-applied mutation cannot claim a successor state")
        if authorization is not None:
            authorized_at = _parse_time(
                authorization.get("decided_at"),
                "authorization %s decided_at" % authorization.get("authorization_id"), issues,
            )
            applied_at = _parse_time(
                application.get("applied_at"),
                "application %s applied_at" % application_id, issues,
            )
            if authorized_at and applied_at and authorized_at >= applied_at:
                issues.append("application %s must occur after its authoritative authorization time" % application_id)

    for outcome in outcome_rows:
        application = _string_lookup(application_by_id, outcome.get("application_id"))
        if application is None:
            issues.append("outcome evaluation %s has unresolved application" % outcome.get("outcome_evaluation_id"))
        else:
            applied_at = _parse_time(
                application.get("applied_at"),
                "application %s applied_at" % application.get("application_id"), issues,
            )
            evaluated_at = _parse_time(
                outcome.get("evaluated_at"),
                "outcome %s evaluated_at" % outcome.get("outcome_evaluation_id"), issues,
            )
            if applied_at and evaluated_at and applied_at >= evaluated_at:
                issues.append("outcome %s must occur after its authoritative application time" % outcome.get("outcome_evaluation_id"))

    for assessment in assessments:
        aid = assessment.get("assessment_id")
        proposal_ids = _string_set(assessment.get("proposal_ids"))
        auth_refs = _string_set(assessment.get("authorization_refs"))
        app_refs = _string_set(assessment.get("application_refs"))
        outcome_refs = _string_set(assessment.get("outcome_evaluation_refs"))
        linked_auth = {
            key for key, row in auth_by_id.items()
            if isinstance(row.get("proposal_id"), str) and row.get("proposal_id") in proposal_ids
        }
        linked_apps = {
            key for key, row in application_by_id.items()
            if isinstance(row.get("proposal_id"), str) and row.get("proposal_id") in proposal_ids
        }
        linked_outcomes = {
            key for key, row in outcome_by_id.items()
            if isinstance(row.get("application_id"), str) and row.get("application_id") in linked_apps
        }
        if auth_refs != linked_auth or app_refs != linked_apps or outcome_refs != linked_outcomes:
            issues.append("assessment %s must carry its complete proposal/authorization/application/outcome reference chain" % aid)

    timeline = document.get("writeback_timeline")
    if not isinstance(timeline, list) or len(timeline) != 5:
        issues.append("writeback timeline requires distinct ordered t1-t5 records")
    else:
        expected_roles = ["t1", "t2", "t3", "t4", "t5"]
        if [row.get("time_role") for row in timeline if isinstance(row, dict)] != expected_roles:
            issues.append("writeback timeline requires distinct ordered t1-t5 records")
        timeline_times = [
            _parse_time(row.get("occurred_at"), "writeback timeline %s" % row.get("time_role"), issues)
            for row in timeline if isinstance(row, dict)
        ]
        if len(timeline_times) != 5 or any(left and right and left >= right for left, right in zip(timeline_times, timeline_times[1:])):
            issues.append("writeback timeline times must be strictly ordered t1-t5")
        registries = [subject_by_id, assessment_by_id, None, None, outcome_by_id]
        timeline_refs = []
        for index, row in enumerate(timeline):
            if not isinstance(row, dict):
                timeline_refs.append(set())
                continue
            refs = _string_set(row.get("record_ids"))
            timeline_refs.append(refs)
            if index == 2:
                valid = set(proposal_by_id) | set(auth_by_id)
            elif index == 3:
                valid = set(application_by_id) | set(successor_by_id)
            else:
                valid = set(registries[index]) if registries[index] is not None else set()
            if not refs or any(ref not in valid for ref in refs):
                issues.append("writeback timeline %s has unresolved record references" % row.get("time_role"))

        if len(timeline_refs) == 5:
            t1_refs, t2_refs, t3_refs, t4_refs, t5_refs = timeline_refs
            if len(t2_refs) != 1:
                issues.append("writeback timeline t2 must identify exactly one governing somnic assessment")
            else:
                assessment_id = next(iter(t2_refs))
                assessment = assessment_by_id.get(assessment_id)
                if assessment is not None:
                    expected_t1 = _string_set(assessment.get("target_orthing_ids"))
                    expected_proposals = _string_set(assessment.get("proposal_ids"))
                    expected_auths = _string_set(assessment.get("authorization_refs"))
                    expected_apps = _string_set(assessment.get("application_refs"))
                    expected_outcomes = _string_set(assessment.get("outcome_evaluation_refs"))
                    expected_successors = {
                        application_by_id[app_id].get("successor_state_id")
                        for app_id in expected_apps
                        if app_id in application_by_id
                        and isinstance(application_by_id[app_id].get("successor_state_id"), str)
                    }
                    if t1_refs != expected_t1:
                        issues.append("writeback timeline t1 must name the exact subjects of its t2 assessment")
                    if t3_refs != expected_proposals | expected_auths:
                        issues.append("writeback timeline t3 must name the assessment's exact proposal and authorization chain")
                    if t4_refs != expected_apps | expected_successors:
                        issues.append("writeback timeline t4 must name the exact applications and produced successors")
                    if t5_refs != expected_outcomes:
                        issues.append("writeback timeline t5 must name the exact later outcomes for that application chain")
                    authoritative_times = []
                    t1_times = [
                        _parse_time(subject_by_id[ref].get("t1_at"), "subject %s t1_at" % ref, issues)
                        for ref in expected_t1 if ref in subject_by_id
                    ]
                    authoritative_times.append(max((value for value in t1_times if value), default=None))
                    authoritative_times.append(_parse_time(
                        _mapping(assessment.get("t2_configuration"), "assessment %s t2_configuration" % assessment_id, issues).get("assessed_at"),
                        "assessment %s assessed_at" % assessment_id, issues,
                    ))
                    t3_times = []
                    for ref in expected_proposals:
                        if ref in proposal_by_id:
                            t3_times.append(_parse_time(proposal_by_id[ref].get("proposed_at"), "proposal %s proposed_at" % ref, issues))
                    for ref in expected_auths:
                        if ref in auth_by_id:
                            t3_times.append(_parse_time(auth_by_id[ref].get("decided_at"), "authorization %s decided_at" % ref, issues))
                    authoritative_times.append(max((value for value in t3_times if value), default=None))
                    t4_times = []
                    for ref in expected_apps:
                        if ref in application_by_id:
                            t4_times.append(_parse_time(application_by_id[ref].get("applied_at"), "application %s applied_at" % ref, issues))
                    for ref in expected_successors:
                        if ref in successor_by_id:
                            t4_times.append(_parse_time(successor_by_id[ref].get("created_at"), "successor %s created_at" % ref, issues))
                    authoritative_times.append(max((value for value in t4_times if value), default=None))
                    t5_times = [
                        _parse_time(outcome_by_id[ref].get("evaluated_at"), "outcome %s evaluated_at" % ref, issues)
                        for ref in expected_outcomes if ref in outcome_by_id
                    ]
                    authoritative_times.append(max((value for value in t5_times if value), default=None))
                    if len(timeline_times) == 5:
                        for role, displayed, authoritative in zip(expected_roles, timeline_times, authoritative_times):
                            if displayed and authoritative and displayed != authoritative:
                                issues.append("writeback timeline %s must equal its authoritative record time" % role)

    if document.get("runtime_status") != "fixture_only_no_runtime":
        issues.append("records must state explicit fixture-only non-runtime status")
    if document.get("reference_operation_status") != "specified_and_validated_not_implemented":
        issues.append("reference recurrence operation is specified/validated, not implemented")
    if not document.get("successor_trigger"):
        issues.append("missing exact downstream successor trigger")
    return issues


def _evidence_timing_issues(record_id, timing, registry):
    if not isinstance(timing, dict):
        return ["%s lacks four-way evidence timing" % record_id]
    issues = []
    fields = ("observed_at_t1", "used_at_t1", "indexed_unused_at_t1", "discovered_after_t1")
    categories = {}
    for field in fields:
        values = timing.get(field)
        if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
            issues.append("%s evidence timing %s must be an ID array" % (record_id, field))
            values = []
        categories[field] = set(values)
        for evidence_id in values:
            if evidence_id not in registry:
                issues.append("%s evidence timing references unknown evidence %s" % (record_id, evidence_id))
            elif registry[evidence_id] != field:
                issues.append("%s evidence timing contradicts registry for %s" % (record_id, evidence_id))
    for index, left in enumerate(fields):
        for right in fields[index + 1:]:
            if categories[left] & categories[right]:
                issues.append("%s evidence timing categories %s and %s must be mutually exclusive" % (record_id, left, right))
    return issues


def _inventory_issues(document, schemas, store):
    issues = []
    candidates = _objects(document, "candidates", issues, "inventory")
    issues += _schema_issues(
        "inventory", document, schemas[AUX_SCHEMA_NAMES["candidate_inventory"]], store
    )
    if not isinstance(document, dict) or document.get("status") != "outline-only" or document.get("execution") != "not implemented":
        issues.append("inventory must be outline-only and not implemented")
    if isinstance(document, dict):
        issues += _schema_issues(
            "inventory.claim_status", document.get("claim_status"),
            schemas[AUX_SCHEMA_NAMES["claim_status"]], store,
        )
    required = {"candidate_id", "status", "execution", "inputs", "outputs", "dependencies", "event_emissions", "authority_limit", "authority_boundary", "residual_behavior", "downstream_owner", "non_claims", "non_claim_boundaries"}
    expected = {"orthability-check", "orthing-ledger", "episode-residual-live", "residual-recurrence-somnic", "metaorthemma-conflict", "intervention-disposition", "verdict-aware-patch-proposal", "guarded-writeback-actuator", "orthing-dream", "somnus-export", "somnus-import", "metaortheme-transclusion", "collective-somnus", "somnus-council", "transclusion-ledger"}
    if {row.get("candidate_id") for row in candidates if isinstance(row.get("candidate_id"), str)} != expected:
        issues.append("inventory does not contain the exact bounded candidate set")
    for row in candidates:
        if not required <= set(row):
            issues.append("inventory candidate %s lacks its complete outline contract" % row.get("candidate_id"))
        if row.get("status") != "outline-only" or row.get("execution") != "not implemented":
            issues.append("inventory candidate %s must remain outline-only and undeployed" % row.get("candidate_id"))
        for field in ("inputs", "outputs", "dependencies"):
            if not _string_set(row.get(field)):
                issues.append("inventory candidate %s requires nonempty typed %s" % (row.get("candidate_id"), field))
        authority = _mapping(
            row.get("authority_boundary"),
            "inventory candidate %s authority_boundary" % row.get("candidate_id"), issues,
        )
        if any(authority.get(field) != "prohibited" for field in (
                "automatic_authorization", "automatic_execution",
                "automatic_writeback", "historical_rewrite")):
            issues.append("inventory candidate %s authority boundary must prohibit authorization, execution, writeback, and historical rewrite" % row.get("candidate_id"))
        authority_text = row.get("authority_limit")
        if (isinstance(authority_text, str) and "automatic" in authority_text.lower()
                and any(token in authority_text.lower() for token in ("authorized", "allowed", "permitted"))):
            issues.append("inventory candidate %s prose contradicts its structured authority boundary" % row.get("candidate_id"))
    return issues


def _adoption_issues(document, schemas, store):
    if not isinstance(document, dict):
        return ["adoption profile must be an object"]
    issues = _schema_issues(
        "adoption", document, schemas[AUX_SCHEMA_NAMES["adoption_profile"]], store
    )
    issues += _schema_issues(
        "adoption.claim_status", document.get("claim_status"),
        schemas[AUX_SCHEMA_NAMES["claim_status"]], store,
    )
    if document.get("status") != "outline-only" or document.get("execution") != "not implemented in orthemology":
        issues.append("writeback adoption profile must remain outline-only and not implemented")
    subsumption = _mapping(document.get("subsumption"), "adoption.subsumption", issues)
    if subsumption.get("ordinary_reflective_writeback_question_is_first_class") is not True:
        issues.append("Somnus must subsume the ordinary reflective-writeback question")
    actuator = _mapping(document.get("actuator"), "adoption.actuator", issues)
    if actuator.get("role") != "first-class downstream actuator" or actuator.get("ontology_center") is not False or actuator.get("unrelated_accessory") is not False:
        issues.append("writeback must be a first-class downstream actuator, not the ontology center or unrelated accessory")
    source = _mapping(document.get("source_verification"), "adoption.source_verification", issues)
    if any(source.get(field) != "pending" for field in ("source_code", "license", "commit", "tests")):
        issues.append("Hermes implementation claims must remain pending source verification")
    for field in ("automatic_proposal", "automatic authorization", "automatic application", "automatic writeback"):
        if document.get(field) != "prohibited":
            issues.append("%s must be prohibited" % field)
    expected_ordinary = {"memory", "user_state", "fact", "skill"}
    expected_governing = {
        "activation_contract", "orthability_evaluator", "selector", "metaortheme",
        "metaorthemma_binding_rule", "evidence_requirement", "closure_rule",
        "residual_rule", "fixture", "provenance", "documentation",
    }
    if _string_set(subsumption.get("ordinary_targets")) != expected_ordinary:
        issues.append("writeback adoption profile must preserve the complete ordinary target vocabulary")
    if not expected_governing <= _string_set(subsumption.get("governing_targets")):
        issues.append("writeback adoption profile must preserve the complete governing target vocabulary")
    expected_outcomes = {"no_change", "investigation", "evidence_request", "preserve_residual", "one_proposal", "alternative_proposals"}
    expected_records = {"somnic_assessment", "intervention_disposition", "mutation_proposal", "mutation_authorization", "applied_mutation", "later_outcome_evaluation"}
    expected_times = {"t1_waking_orthing", "t2_somnic_assessment", "t3_proposal_and_authorization", "t4_application_and_successor_state", "t5_outcome_evaluation"}
    if _string_set(subsumption.get("outcomes")) != expected_outcomes:
        issues.append("writeback adoption profile must preserve the exact outcome vocabulary")
    if _string_set(document.get("record_separation")) != expected_records:
        issues.append("writeback adoption profile must preserve the exact record-separation vocabulary")
    if _string_set(document.get("temporal_roles")) != expected_times:
        issues.append("writeback adoption profile must preserve the exact t1-t5 vocabulary")
    return issues


def _collective_issues(document, schemas, store):
    if not isinstance(document, dict):
        return ["collective profile must be an object"]
    issues = _schema_issues(
        "collective", document, schemas[AUX_SCHEMA_NAMES["collective_profile"]], store
    )
    issues += _schema_issues(
        "collective.claim_status", document.get("claim_status"),
        schemas[AUX_SCHEMA_NAMES["claim_status"]], store,
    )
    modes = document.get("modes")
    expected_modes = {
        "C1": ("independent-type-convergent-orthing", "none-during-discovery", "none-required"),
        "C2": ("federated-transclusive-orthing", "provenance-preserving-transclusion", "recipient-locally-re-orths"),
        "C3": ("coordinated-council-orthing", "intentionally-shared-evidence-and-assessments", "bounded-deliberation"),
    }
    if not isinstance(modes, list) or [row.get("mode_id") for row in modes if isinstance(row, dict)] != ["C1", "C2", "C3"]:
        issues.append("collective mode contract must preserve distinct C1, C2, and C3 modes")
    else:
        for row in modes:
            expected = expected_modes[row["mode_id"]]
            observed = (row.get("name"), row.get("information_path"), row.get("coordination"))
            if observed != expected:
                issues.append("collective mode %s must preserve its exact normative contract" % row["mode_id"])
    if document.get("shared_types_supply_transport") is not False:
        issues.append("shared types do not supply a transport channel")
    event_instances = _mapping(document.get("event_instances"), "collective.event_instances", issues)
    if event_instances.get("actor_ledger_version_indexed") is not True:
        issues.append("collective event instances must remain actor, ledger, and version indexed")
    if document.get("source_applicability_auto_propagates") is not False:
        issues.append("source applicability cannot auto-propagate to a recipient")
    if document.get("receipt_can_govern_or_execute") is not False:
        issues.append("receipt cannot directly govern or execute")
    transclusion = _mapping(document.get("transclusion"), "collective.transclusion", issues)
    semantic = transclusion.get("semantic_character")
    if semantic != "structurally encoded and semantically reconstructible within declared limits":
        issues.append("transclusion semantic boundary must reject non-semantic or lossless identity claims")
    if document.get("multi_operator_count_implies") != []:
        issues.append("multi-operator count implies neither independence, tawatur, truth, nor authorization")
    required_dependence = {"operator_count", "model_family_count", "contract_version_count", "source_family_count", "input_family_count", "institutional_origin_count", "coordination_path", "time_span", "counterexample_count"}
    if _string_set(document.get("dependence_dimensions")) != required_dependence:
        issues.append("collective recurrence must preserve the exact declared dependence dimensions")
    source_envelope = _mapping(document.get("source_envelope"), "collective.source_envelope", issues)
    if source_envelope.get("immutable") is not True:
        issues.append("source envelope must remain immutable")
    required_source_identity = {"source_actor_id", "source_ledger_id", "source_occurrence_ids", "source_orthing_ids", "source_assessment_ids", "source_versions"}
    if _string_set(source_envelope.get("required_identity")) != required_source_identity:
        issues.append("source envelope must preserve complete source actor, ledger, occurrence, orthing, assessment, and version identity")
    required_disclosure = {"redactions", "permitted_use", "intended_recipient", "expiry_or_review_trigger", "residuals", "non_claims"}
    if _string_set(source_envelope.get("disclosure")) != required_disclosure:
        issues.append("source envelope must preserve the exact bounded disclosure vocabulary")
    receiving = _mapping(document.get("receiving_assessment"), "collective.receiving_assessment", issues)
    if any(receiving.get(field) is not True for field in (
            "append_only", "source_and_local_versions_separate",
            "local_meta_orthability_required", "local_authorization_required")):
        issues.append("receiving assessment must append locally and preserve local meta-orthability and authorization gates")
    closure = _mapping(document.get("collective_closure"), "collective.collective_closure", issues)
    if closure.get("preserves_dissent") is not True or closure.get("bounded_scope") is not True:
        issues.append("bounded collective closure must preserve dissent")
    required_closure = {"shared_placement", "bounded_agreement_with_dissent", "several_local_placements", "unresolved_conflict", "insufficient_shared_evidence", "domain_scope_split", "hold_partial_recurse"}
    if _string_set(closure.get("permitted")) != required_closure:
        issues.append("bounded collective closure must preserve the exact plural disposition vocabulary")
    privacy = _mapping(document.get("privacy"), "collective.privacy", issues)
    if privacy.get("redacted_projection_may_claim_complete") is not False:
        issues.append("redacted projection cannot be labeled complete")
    required_privacy = {"minimum_necessary_disclosure", "selective_projection", "redaction", "consent_authorization", "purpose_limitation", "retention_limits", "recipient_scope", "future_access_retirement"}
    if _string_set(privacy.get("controls")) != required_privacy:
        issues.append("collective privacy profile must preserve all disclosure controls")
    security = _mapping(document.get("security"), "collective.security", issues)
    required_threats = {"instruction_injection", "malicious_dsl_ir", "poisoned_represented_standard", "authority_laundering", "sybil_multiplication", "collusion", "common_source_dependence", "schema_version_drift", "semantic_decoding_drift", "stale_contract", "privacy_leakage", "transclusion_cycle", "recursive_assessment_storm", "receipt_triggered_execution", "consensus_as_truth", "provenance_loss"}
    required_controls = {"bounded_cycle_depth", "immutable_source_reference", "integrity_check", "version_compatibility", "fail_closed_parsing", "separate_execution_authorization", "local_hold_override", "audit_trail"}
    if _string_set(security.get("threats")) != required_threats or _string_set(security.get("controls")) != required_controls:
        issues.append("collective security profile must preserve injection, poisoning, Sybil, dependence, integrity, privacy, and cycle safeguards")
    required_bearers = {"normative_metaortheme_type", "represented_standard_at_actor_time", "case_bound_metaorthemma", "execution_trace", "transclusion_envelope"}
    if _string_set(document.get("bearer_separation")) != required_bearers:
        issues.append("collective profile must preserve normative, represented, case-bound, execution, and envelope bearers")
    required_levels = {"evidential_artifact", "normative_standard", "operational_dsl_ir"}
    levels = transclusion.get("levels") if isinstance(transclusion.get("levels"), list) else []
    if {row.get("level") for row in levels if isinstance(row, dict) and isinstance(row.get("level"), str)} != required_levels:
        issues.append("collective transclusion must preserve evidential, normative, and operational levels")
    expected_level_effects = {
        "evidential_artifact": ("available_evidence_or_comparator", "governing_or_executable"),
        "normative_standard": ("local_meta_orthability_candidate", "locally_governing_without_version_acceptance_and_authorization"),
        "operational_dsl_ir": ("inspectable_capability_candidate", "execution_from_parse_success"),
    }
    for level in levels:
        if (not isinstance(level, dict) or not isinstance(level.get("level"), str)
                or level.get("level") not in expected_level_effects):
            continue
        if (level.get("permitted_effect"), level.get("prohibited_effect")) != expected_level_effects[level["level"]]:
            issues.append("collective transclusion level %s must preserve its exact permitted and prohibited effects" % level["level"])
    required_gates = {"schema_compatibility", "source_authenticity", "semantic_reconstruction", "domain_applicability", "contract_owner_validity", "local_authorization", "execution_capability", "post_execution_witness"}
    if _string_set(transclusion.get("gates")) != required_gates:
        issues.append("collective transclusion must preserve all local import and execution gates")
    boundaries = _mapping(document.get("semantic_boundaries"), "collective.semantic_boundaries", issues)
    if any(boundaries.get(field) is not False for field in (
            "nar_or_field_witness_similarity_proves_identity",
            "source_execution_closure_proves_recipient_uptake",
            "exported_record_is_direct_soul_access",
            "multi_operator_recurrence_proves_independence",
            "multi_operator_recurrence_proves_tawatur",
            "multi_operator_recurrence_proves_truth",
            "multi_operator_recurrence_supplies_authorization")):
        issues.append("collective testimony, semantic identity, uptake, truth, authorization, and no-soul boundaries must remain false")
    exact = {"implemented in orthemology": "no", "automatic adoption": "prohibited", "automatic execution": "prohibited", "automatic writeback": "prohibited"}
    for field, value in exact.items():
        if document.get(field) != value:
            issues.append("collective automatic boundary %s must be %s" % (field, value))
    non_claims = _mapping(document.get("non_claims"), "collective.non_claims", issues)
    expected_non_claims = {
        "runtime": "not-implemented", "collective_execution": "not-implemented",
        "automatic_writeback": "not-implemented", "semantic_identity": "not-established",
        "local_applicability": "not-established", "authorization": "not-established",
        "recipient_uptake": "not-established",
    }
    if non_claims != expected_non_claims:
        issues.append("collective non-claims must remain structured and consistent with the claim-status owner")
    claim_status = document.get("claim_status") if isinstance(document.get("claim_status"), dict) else {}
    if (isinstance(claim_status.get("runtime"), dict)
            and non_claims.get("runtime") != claim_status["runtime"].get("status")):
        issues.append("collective runtime non-claim contradicts the claim-status owner")
    if (isinstance(claim_status.get("collective_execution"), dict)
            and non_claims.get("collective_execution") != claim_status["collective_execution"].get("status")):
        issues.append("collective execution non-claim contradicts the claim-status owner")
    return issues


def _decision_issues(text):
    if not isinstance(text, str):
        return ["Decision 0035 is unreadable"], None
    match = re.search(r"<!-- decision-candidate-boundary:start -->\s*```yaml\s*(.*?)\s*```\s*<!-- decision-candidate-boundary:end -->", text, re.S)
    if not match:
        return ["Decision 0035 lacks a structured candidate boundary"], None
    try:
        boundary = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return ["Decision 0035 candidate boundary is malformed: %s" % exc], None
    expected = {"decision": "0035", "status": "proposed-candidate", "pr": 12, "scope": "runtime-neutral-somnic-contracts-only", "independent_signoff": False, "ready_for_merge": False, "merged": False}
    issues = ["Decision 0035 candidate boundary changes %s" % key for key, value in expected.items() if not isinstance(boundary, dict) or boundary.get(key) != value]
    claim_matches = re.findall(r"<!-- somnus-claim-status:start -->\s*```yaml\s*(.*?)\s*```\s*<!-- somnus-claim-status:end -->", text, re.S)
    if len(claim_matches) != 1:
        issues.append("Decision 0035 requires exactly one structured Somnus claim-status owner")
        return issues, None
    try:
        claim_status = yaml.safe_load(claim_matches[0])
    except yaml.YAMLError as exc:
        issues.append("Decision 0035 claim-status owner is malformed: %s" % exc)
        claim_status = None
    return issues, claim_status


def _manuscript_issues(text, claim_status):
    if not isinstance(text, str):
        return ["manuscript Somnus claim-status projection is unreadable"]
    matches = re.findall(r"<!-- somnus-claim-status-projection:start -->\s*```yaml\s*(.*?)\s*```\s*<!-- somnus-claim-status-projection:end -->", text, re.S)
    if len(matches) != 1:
        return ["manuscript requires exactly one structured Somnus claim-status projection"]
    try:
        projection = yaml.safe_load(matches[0])
    except yaml.YAMLError as exc:
        return ["manuscript Somnus claim-status projection is malformed: %s" % exc]
    issues = []
    if not isinstance(projection, dict) or projection.get("claim_status_ref") != "docs/decisions/0035-somnic-orthing-and-activation-contracts.md#somnus-claim-status":
        issues.append("manuscript Somnus claim-status projection must resolve to Decision 0035")
        return issues
    if isinstance(claim_status, dict):
        for field, record in claim_status.items():
            if field == "claim_status_id" or not isinstance(record, dict):
                continue
            if projection.get(field) != record.get("status"):
                issues.append("manuscript Somnus claim-status projection disagrees on %s" % field)
    return issues


def collect_issues(activation, records, inventory, adoption, collective,
                   decision_text, manuscript_text, schemas):
    store = {}
    for name, schema in schemas.items():
        store[name] = schema
        store[schema.get("$id", name)] = schema
    issues = []
    if isinstance(activation, dict):
        issues += _activation_issues(activation, schemas, store)
    else:
        issues.append("activation fixture document must be an object")
    if isinstance(records, dict):
        issues += _records_issues(records, activation, schemas, store)
    else:
        issues.append("somnus record fixture document must be an object")
    issues += _inventory_issues(inventory, schemas, store)
    issues += _adoption_issues(adoption, schemas, store)
    issues += _collective_issues(collective, schemas, store)
    decision_issues, claim_status = _decision_issues(decision_text)
    issues += decision_issues
    if claim_status is not None:
        issues += _schema_issues(
            "Decision 0035 claim_status", claim_status,
            schemas[AUX_SCHEMA_NAMES["claim_status"]], store,
        )
        for label, document in (
                ("records", records), ("inventory", inventory),
                ("adoption", adoption), ("collective", collective)):
            if isinstance(document, dict) and document.get("claim_status") != claim_status:
                issues.append("%s claim-status projection disagrees with Decision 0035 owner" % label)
    issues += _manuscript_issues(manuscript_text, claim_status)
    return issues


def main():
    inputs = []
    preload_issues = []
    for path in (ACTIVATION_PATH, RECORDS_PATH, INVENTORY_PATH, ADOPTION_PATH, COLLECTIVE_PATH):
        value, issue = _load_yaml(path)
        inputs.append(value)
        if issue:
            preload_issues.append(issue)
    try:
        decision_text = DECISION_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        decision_text = ""
        preload_issues.append("Decision 0035 unavailable: %s" % exc)
    try:
        manuscript_text = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        manuscript_text = ""
        preload_issues.append("manuscript unavailable: %s" % exc)
    schemas, schema_load_issues = _load_schemas()
    issues = preload_issues + schema_load_issues
    if len(schemas) == len(SCHEMA_NAMES) + len(AUX_SCHEMA_NAMES):
        issues += collect_issues(*inputs, decision_text, manuscript_text, schemas)
    for issue in issues:
        print("[FAIL] %s" % issue)
    if not issues:
        print("[PASS] bounded waking/somnic contracts, fixtures, and outline profiles")
    print("TOTAL: %d failures" % len(issues))
    raise SystemExit(1 if issues else 0)


if __name__ == "__main__":
    main()
