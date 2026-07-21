#!/usr/bin/env python3
"""Validate bounded waking/somnic schemas, fixtures, and outline profiles.

This is an offline conformance validator.  It is not a recurrence analyzer,
ledger emitter, scheduler, writeback engine, or collective runtime.
"""
import json
import re
import sys
from collections import Counter, defaultdict
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

SCHEMA_NAMES = {
    "contracts": "activation-contract.schema.json",
    "orthing_events": "orthing-event.schema.json",
    "meta_orthability_assessments": "meta-orthability-assessment.schema.json",
    "somnus_runs": "somnus-run.schema.json",
    "somnic_assessments": "somnic-assessment.schema.json",
    "recurrence_reports": "residual-recurrence-report.schema.json",
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
    for name in SCHEMA_NAMES.values():
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


def _activation_issues(document, schemas, store):
    issues = []
    contracts = _objects(document, "contracts", issues, "activation")
    evaluators = _objects(document, "evaluators", issues, "activation")
    outcomes = _objects(document, "fixture_outcomes", issues, "activation")
    for index, contract in enumerate(contracts):
        issues += _schema_issues("activation.contracts[%d]" % index, contract,
                                 schemas[SCHEMA_NAMES["contracts"]], store)
    classes = {row.get("fixture_class") for row in outcomes}
    if classes != FIXTURE_CLASSES:
        issues.append("fixture outcomes must cover positive, negative-near-boundary, indeterminate, and overlap")
    outcome_by_id = _by(outcomes, "fixture_id")
    contract_by_key = {(row.get("contract_id"), row.get("contract_version")): row for row in contracts}
    for contract in contracts:
        if contract.get("status") == "accepted":
            refs = contract.get("fixture_outcomes")
            if not isinstance(refs, list) or not refs:
                issues.append("accepted contract %s requires fixture outcomes" % contract.get("contract_id"))
            elif any(ref not in outcome_by_id for ref in refs):
                issues.append("accepted contract %s has unresolved fixture outcomes" % contract.get("contract_id"))
    for evaluator in evaluators:
        if set(evaluator.get("result_vocabulary", [])) != TRI_STATE:
            issues.append("orthability evaluator %s must preserve the tri-state vocabulary" % evaluator.get("evaluator_id"))
    for outcome in outcomes:
        findings = outcome.get("property_findings")
        if not isinstance(findings, dict):
            issues.append("fixture %s lacks structured property findings" % outcome.get("fixture_id"))
            continue
        assessments = outcome.get("claimant_assessments")
        if not isinstance(assessments, list) or not assessments:
            issues.append("fixture %s lacks claimant assessments" % outcome.get("fixture_id"))
            continue
        for assessment in assessments:
            if not isinstance(assessment, dict):
                issues.append("fixture %s has malformed claimant assessment" % outcome.get("fixture_id"))
                continue
            for field in ("activation_contract_id", "activation_contract_version", "evaluator_id", "evaluator_version"):
                if not assessment.get(field):
                    issues.append("fixture %s claimant assessment missing contract/evaluator version field %s" % (outcome.get("fixture_id"), field))
            contract = contract_by_key.get((assessment.get("activation_contract_id"), assessment.get("activation_contract_version")))
            if contract is None:
                issues.append("fixture %s references unknown activation contract/version" % outcome.get("fixture_id"))
                continue
            result = assessment.get("result")
            if result not in TRI_STATE:
                issues.append("fixture %s has result outside tri-state vocabulary" % outcome.get("fixture_id"))
            if result == "applicable":
                satisfied = set(findings.get("satisfied", []))
                absent = set(findings.get("absent", []))
                indeterminate = set(findings.get("indeterminate", []))
                required = set(contract.get("required_properties", []))
                if not required <= satisfied or required & (absent | indeterminate):
                    issues.append("fixture %s cannot infer applicability from indicators while required properties are absent or indeterminate" % outcome.get("fixture_id"))
        if outcome.get("fixture_id") == "ACT-MIXED-LEXICAL-001":
            if any(row.get("result") != "indeterminate" for row in assessments if isinstance(row, dict)):
                issues.append("mixed lexical fixture must remain indeterminate when required properties are absent")
    return issues


def _records_issues(document, schemas, store):
    issues = []
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

    evidence_rows = _objects(document, "evidence_records", issues, "records")
    evidence_timing = {row.get("evidence_id"): row.get("timing") for row in evidence_rows}
    for event in events:
        identity_values = [event.get(name) for name in ("session_id", "episode_id", "occurrence_id", "claim_attempt_id", "orthability_assessment_id", "orthing_id") if event.get(name) is not None]
        if len(identity_values) != len(set(identity_values)):
            issues.append("event %s collapses distinct identity levels" % event.get("event_id"))
        if event.get("source_case") == "R7E" and event.get("capture_mode") != "retrospective_reconstruction":
            issues.append("R7E retrospective reconstruction cannot be relabeled as live capture")
        issues += _evidence_timing_issues(event.get("event_id"), event.get("evidence_timing"), evidence_timing)

    assessment_by_id = _by(assessments, "assessment_id")
    proposal_rows = _objects(document, "proposals", issues, "records")
    proposal_by_id = _by(proposal_rows, "proposal_id")
    for assessment in assessments:
        aid = assessment.get("assessment_id")
        if assessment.get("target_history_mutated") is not False or assessment.get("explicit_non_mutation") is not True:
            issues.append("assessment %s violates the append-only target history rule" % aid)
        if not assessment.get("target_orthing_ids"):
            issues.append("assessment %s lacks target orthing identity" % aid)
        if assessment.get("retroactive_conformity_rewrite") is not False:
            issues.append("assessment %s rewrites historical conformity" % aid)
        issues += _evidence_timing_issues(aid, assessment.get("evidence_timing"), evidence_timing)
        proposals = assessment.get("proposal_ids")
        disposition = assessment.get("intervention_disposition")
        if disposition == "no_change" and proposals:
            issues.append("assessment %s no-change outcome cannot be forced into a proposal" % aid)
        if disposition == "alternative_proposals" and (not isinstance(proposals, list) or len(proposals) < 2):
            issues.append("assessment %s alternative proposal disposition requires at least two proposals" % aid)
        if disposition == "proposal" and (not isinstance(proposals, list) or len(proposals) != 1):
            issues.append("assessment %s proposal disposition requires exactly one proposal" % aid)
        for proposal_id in proposals or []:
            if proposal_id not in proposal_by_id:
                issues.append("assessment %s references unknown proposal %s" % (aid, proposal_id))

    closed_ids = {row.get("assessment_id") for row in assessments if row.get("closure_status") == "closed"}
    signatures = defaultdict(list)
    for run in runs:
        rid = run.get("somnus_run_id")
        reopens = set(run.get("reopens_subject_ids", []))
        deltas = run.get("material_delta_ids", [])
        if reopens and not deltas:
            issues.append("run %s reopens a subject without a material delta" % rid)
        for subject in set(run.get("anchor_subject_ids", [])) & closed_ids:
            if subject not in reopens or not deltas:
                issues.append("run %s automatically requeues closed assessment %s without material delta" % (rid, subject))
        if set(run.get("historical_comparator_ids", [])) & reopens:
            issues.append("run %s reopens a historical comparator merely to use it" % rid)
        signature = (
            run.get("operation_id"), run.get("operation_version"),
            tuple(sorted(run.get("anchor_subject_ids", []))), run.get("reference_corpus_revision"),
            tuple(sorted(run.get("governing_versions", []))), tuple(sorted(deltas)),
            run.get("idempotency_key"),
        )
        signatures[signature].append(run)
    for rows in signatures.values():
        if len(rows) > 1:
            outputs = {tuple(sorted(row.get("output_ids", []))) for row in rows}
            if len(outputs) > 1:
                issues.append("idempotency collision emits non-equivalent duplicate outputs")

    for report in reports:
        support = report.get("supporting_occurrences", [])
        unique_orthings = {row.get("orthing_id") for row in support if isinstance(row, dict)}
        unique_episodes = {row.get("episode_id") for row in support if isinstance(row, dict)}
        dims = report.get("dependence_dimensions", {})
        if dims.get("episode_count") != len(unique_episodes) or len(unique_orthings) != len(support):
            issues.append("recurrence support must count distinct episodes and orthings, not copies")
        independence = report.get("independence_assessment", {})
        if independence.get("passed") is False and independence.get("label") != "distinct episodes":
            issues.append("recurrence without a passed independence rule must say distinct episodes")
        if report.get("systemic_defect_proven") is not False or report.get("threshold_effect") != "review_trigger_only":
            issues.append("recurrence threshold is a review trigger, not proof of a systemic defect")
        if report.get("emitted_actions"):
            issues.append("v0 recurrence cannot emit automatic patch, promotion, closure, or mutation actions")
        if report.get("causal_diagnosis") != "not-established" or report.get("proposed_intervention") != "not-produced-by-v0":
            issues.append("v0 must keep recurrence equality separate from causal diagnosis and intervention")

    for proposal in proposal_rows:
        mode = proposal.get("provenance_mode")
        if mode not in {"legacy_reflective_proposal", "somnus_grounded_proposal"}:
            issues.append("proposal %s has invalid provenance mode" % proposal.get("proposal_id"))
        if mode == "somnus_grounded_proposal" and proposal.get("supporting_assessment_id") not in assessment_by_id:
            issues.append("grounded proposal %s lacks supporting assessment" % proposal.get("proposal_id"))

    auth_rows = _objects(document, "authorizations", issues, "records")
    auth_by_id = _by(auth_rows, "authorization_id")
    for auth in auth_rows:
        if auth.get("source") == "provisional_placement" and auth.get("authorized") is not False:
            issues.append("provisional placement cannot supply its own mutation authorization")

    application_rows = _objects(document, "applications", issues, "records")
    outcome_rows = _objects(document, "outcome_evaluations", issues, "records")
    outcome_application_ids = {row.get("application_id") for row in outcome_rows}
    for application in application_rows:
        if application.get("assessment_history_mutated") is not False or application.get("proposal_history_mutated") is not False:
            issues.append("application failure or success cannot rewrite assessment/proposal history")
        if application.get("status") == "applied" and application.get("outcome_evaluation_required") is not True:
            issues.append("applied mutation requires later outcome evaluation")
        if application.get("status") == "applied" and application.get("application_id") not in outcome_application_ids:
            issues.append("applied mutation lacks a later outcome evaluation record")
        auth_id = application.get("authorization_id")
        if auth_id not in auth_by_id:
            issues.append("application authorization reference must resolve")
            continue
        authorization = auth_by_id[auth_id]
        if authorization.get("proposal_id") != application.get("proposal_id"):
            issues.append("application authorization must govern the same proposal")
        if authorization.get("authorized") is False and application.get("status") == "applied":
            issues.append("application cannot apply under rejected authorization")

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
    t1_fields = ("observed_at_t1", "used_at_t1", "indexed_unused_at_t1")
    t1_ids = set().union(*(set(timing.get(field, [])) for field in t1_fields))
    later = set(timing.get("discovered_after_t1", []))
    if t1_ids & later:
        issues.append("%s evidence timing puts one item at both t1 and t2" % record_id)
    if any(registry.get(evidence_id) == "discovered_after_t1" for evidence_id in t1_ids):
        issues.append("%s evidence timing relabels later-discovered evidence as t1" % record_id)
    if any(registry.get(evidence_id) != "discovered_after_t1" for evidence_id in later):
        issues.append("%s evidence timing mislabels a t1 item as discovered after t1" % record_id)
    return issues


def _inventory_issues(document):
    issues = []
    candidates = _objects(document, "candidates", issues, "inventory")
    if not isinstance(document, dict) or document.get("status") != "outline-only" or document.get("execution") != "not implemented":
        issues.append("inventory must be outline-only and not implemented")
    required = {"candidate_id", "status", "execution", "inputs", "outputs", "dependencies", "event_emissions", "authority_limit", "residual_behavior", "downstream_owner", "non_claims"}
    expected = {"orthability-check", "orthing-ledger", "episode-residual-live", "residual-recurrence-somnic", "metaorthemma-conflict", "intervention-disposition", "verdict-aware-patch-proposal", "guarded-writeback-actuator", "orthing-dream", "somnus-export", "somnus-import", "metaortheme-transclusion", "collective-somnus", "somnus-council", "transclusion-ledger"}
    if {row.get("candidate_id") for row in candidates} != expected:
        issues.append("inventory does not contain the exact bounded candidate set")
    for row in candidates:
        if not required <= set(row):
            issues.append("inventory candidate %s lacks its complete outline contract" % row.get("candidate_id"))
        if row.get("status") != "outline-only" or row.get("execution") != "not implemented":
            issues.append("inventory candidate %s must remain outline-only and undeployed" % row.get("candidate_id"))
    return issues


def _adoption_issues(document):
    if not isinstance(document, dict):
        return ["adoption profile must be an object"]
    issues = []
    if document.get("status") != "outline-only" or document.get("execution") != "not implemented in orthemology":
        issues.append("writeback adoption profile must remain outline-only and not implemented")
    subsumption = document.get("subsumption", {})
    if subsumption.get("ordinary_reflective_writeback_question_is_first_class") is not True:
        issues.append("Somnus must subsume the ordinary reflective-writeback question")
    actuator = document.get("actuator", {})
    if actuator.get("role") != "first-class downstream actuator" or actuator.get("ontology_center") is not False or actuator.get("unrelated_accessory") is not False:
        issues.append("writeback must be a first-class downstream actuator, not the ontology center or unrelated accessory")
    source = document.get("source_verification", {})
    if any(source.get(field) != "pending" for field in ("source_code", "license", "commit", "tests")):
        issues.append("Hermes implementation claims must remain pending source verification")
    for field in ("automatic_proposal", "automatic authorization", "automatic application", "automatic writeback"):
        if document.get(field) != "prohibited":
            issues.append("%s must be prohibited" % field)
    return issues


def _collective_issues(document):
    if not isinstance(document, dict):
        return ["collective profile must be an object"]
    issues = []
    modes = document.get("modes")
    if not isinstance(modes, list) or [row.get("mode_id") for row in modes if isinstance(row, dict)] != ["C1", "C2", "C3"]:
        issues.append("collective mode contract must preserve distinct C1, C2, and C3 modes")
    if document.get("shared_types_supply_transport") is not False:
        issues.append("shared types do not supply a transport channel")
    if (document.get("event_instances") or {}).get("actor_ledger_version_indexed") is not True:
        issues.append("collective event instances must remain actor, ledger, and version indexed")
    if document.get("source_applicability_auto_propagates") is not False:
        issues.append("source applicability cannot auto-propagate to a recipient")
    if document.get("receipt_can_govern_or_execute") is not False:
        issues.append("receipt cannot directly govern or execute")
    semantic = (document.get("transclusion") or {}).get("semantic_character")
    if semantic != "structurally encoded and semantically reconstructible within declared limits":
        issues.append("transclusion semantic boundary must reject non-semantic or lossless identity claims")
    if document.get("multi_operator_count_implies") != []:
        issues.append("multi-operator count implies neither independence, tawatur, truth, nor authorization")
    if (document.get("source_envelope") or {}).get("immutable") is not True:
        issues.append("source envelope must remain immutable")
    if (document.get("collective_closure") or {}).get("preserves_dissent") is not True:
        issues.append("bounded collective closure must preserve dissent")
    if (document.get("privacy") or {}).get("redacted_projection_may_claim_complete") is not False:
        issues.append("redacted projection cannot be labeled complete")
    exact = {"implemented in orthemology": "no", "automatic adoption": "prohibited", "automatic execution": "prohibited", "automatic writeback": "prohibited"}
    for field, value in exact.items():
        if document.get(field) != value:
            issues.append("collective automatic boundary %s must be %s" % (field, value))
    return issues


def _decision_issues(text):
    if not isinstance(text, str):
        return ["Decision 0035 is unreadable"]
    match = re.search(r"<!-- decision-candidate-boundary:start -->\s*```yaml\s*(.*?)\s*```\s*<!-- decision-candidate-boundary:end -->", text, re.S)
    if not match:
        return ["Decision 0035 lacks a structured candidate boundary"]
    try:
        boundary = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return ["Decision 0035 candidate boundary is malformed: %s" % exc]
    expected = {"decision": "0035", "status": "proposed-candidate", "pr": 12, "scope": "runtime-neutral-somnic-contracts-only", "independent_signoff": False, "ready_for_merge": False, "merged": False}
    return ["Decision 0035 candidate boundary changes %s" % key for key, value in expected.items() if not isinstance(boundary, dict) or boundary.get(key) != value]


def collect_issues(activation, records, inventory, adoption, collective, decision_text, schemas):
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
        issues += _records_issues(records, schemas, store)
    else:
        issues.append("somnus record fixture document must be an object")
    issues += _inventory_issues(inventory)
    issues += _adoption_issues(adoption)
    issues += _collective_issues(collective)
    issues += _decision_issues(decision_text)
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
    schemas, schema_load_issues = _load_schemas()
    issues = preload_issues + schema_load_issues
    if len(schemas) == len(SCHEMA_NAMES):
        issues += collect_issues(*inputs, decision_text, schemas)
    for issue in issues:
        print("[FAIL] %s" % issue)
    if not issues:
        print("[PASS] bounded waking/somnic contracts, fixtures, and outline profiles")
    print("TOTAL: %d failures" % len(issues))
    raise SystemExit(1 if issues else 0)


if __name__ == "__main__":
    main()
