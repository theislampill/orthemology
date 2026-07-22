#!/usr/bin/env python3
"""Validate the bounded, evidence-qualified R7E LLM witness and crosswalk."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "llm-mediated-orthing-witness.schema.json"
WITNESS_PATH = ROOT / "docs" / "project-closure" / "r7e-sol" / "R7E-LLM-MEDIATED-ORTHING-WITNESS.yaml"
CROSSWALK_PATH = ROOT / "docs" / "project-closure" / "r7e-sol" / "R7E-SOMNIC-CASE-CROSSWALK.yaml"
NARRATIVE_PATH = ROOT / "docs" / "project-closure" / "r7e-sol" / "R7E-LLM-MEDIATED-ORTHING-WITNESS.md"
TASK4_FIXTURES_PATH = ROOT / "examples" / "somnus" / "somnus-record-fixtures.yaml"

EVIDENCE_STATES = {
    "repository-verified",
    "attachment-observed",
    "implementing-run-attributed",
    "missing",
    "unresolved",
}
ILLUSTRATION_ROLES = {
    "documented-historical-fact",
    "retrospective-reconstruction",
    "schema-conformant-illustrative-mapping",
    "unsupported-live-runtime-claim",
}
IDENTITY_KINDS = {"turn", "session", "episode", "occurrence", "orthing", "reconstruction_event"}
OBJECT_KINDS = {
    "orthemmata",
    "declared-analysis",
    "executor-subagent-roles",
    "governing-types",
    "case-bound-applications",
    "sources",
    "candidate-findings-profiles",
    "routes",
    "integrated-actions",
    "residual-backlog",
    "successor-state",
    "higher-order-audit",
}
CLAIM_BOUNDARIES = {
    "correctness": "not-established",
    "empirical_validation": "not-established",
    "terminology_benefit_or_adoption": "not-established",
    "exact_internal_model_ontology": "not-established",
    "cross_model_or_domain_generalization": "not-established",
    "live_append_only_capture": "not-observed",
    "claimant_contract_enforcement": "not-observed",
    "recurrence_detection": "not-observed",
    "idempotent_frontier_processing": "not-observed",
    "full_somnus_writeback_chain": "not-implemented",
    "nightly_autonomy": "not-implemented",
    "runtime_deployment": "not-implemented",
}
EXPECTED_SOURCE_STATES = {
    "docs/project-closure/r7e/AUTONOMOUS-R7E-STATE.json": "repository-verified",
    "docs/project-closure/r7e-sol/R7E-INPUT-PROVENANCE.json": "repository-verified",
    "docs/project-closure/r7e-sol/R7E-INDEPENDENT-FINDING-MATRIX.yaml": "repository-verified",
    "workflow journal": "missing",
    "per-agent reports": "missing",
    "full candidate drafts": "missing",
    "eight repository rejection bullets": "repository-verified",
    "eight reported rejection records": "missing",
    "supplied R7E attachments": "attachment-observed",
    "R7E implementing-run aggregate statistics": "implementing-run-attributed",
}
# The retained Task 5 source registry is descriptive evidence, not an authority
# registry. None of its current members owns original R7E identity, original t1
# history, or authoritative target history. A future owner requires a reviewed
# contract change rather than promotion based only on evidence state.
SOURCE_AUTHORITY_SCOPES = {source_ref: frozenset() for source_ref in EXPECTED_SOURCE_STATES}
EXPECTED_OBJECT_ROLES = {
    "orthemmata": "retrospective-reconstruction",
    "declared-analysis": "schema-conformant-illustrative-mapping",
    "executor-subagent-roles": "documented-historical-fact",
    "governing-types": "schema-conformant-illustrative-mapping",
    "case-bound-applications": "unsupported-live-runtime-claim",
    "sources": "documented-historical-fact",
    "candidate-findings-profiles": "retrospective-reconstruction",
    "routes": "retrospective-reconstruction",
    "integrated-actions": "documented-historical-fact",
    "residual-backlog": "documented-historical-fact",
    "successor-state": "documented-historical-fact",
    "higher-order-audit": "retrospective-reconstruction",
}
AUTHORITY_ID = re.compile(r"[A-Z0-9]+(?:-[A-Z0-9]+)*\Z")
PROMOTED_CLAIM = re.compile(
    r"(?:"
    r"\bauthoritative(?:ly)?\b[^.\n]{0,120}\b(?:identit(?:y|ies)|correctness|runtime|Somnus)\b"
    r"|\bverified\b[^.\n]{0,120}\b(?:deploy(?:ed|ment)?|runtime|correctness|Somnus)\b"
    r"|\b(?:proves?|proved|establishes|established|demonstrates?|demonstrated|validates?|validated)\b"
    r"[^.\n]{0,120}\b(?:correctness|comparative utility|empirical validation|terminology (?:benefit|adoption)|"
    r"internal model ontology|generalization|recurrence|frontier|writeback|autonomy|runtime|Somnus|original .{0,30}identit(?:y|ies))\b"
    r")",
    re.IGNORECASE,
)
TEMPORAL_RELATION_PROMOTION = re.compile(
    r"(?:\b(?:temporal separation|different times?|time difference)\b[^.\n]{0,100}\b(?:alone|solely|sufficient)\b"
    r"[^.\n]{0,100}\b(?:establish(?:es|ed)?|prove(?:s|d)?|constitute(?:s|d)?)\b"
    r"|\b(?:establish(?:es|ed)?|prove(?:s|d)?|constitute(?:s|d)?)\b[^.\n]{0,100}"
    r"\b(?:solely|only)\b[^.\n]{0,40}\b(?:time|temporal)\b)",
    re.IGNORECASE,
)


def _schema_issues(witness: object) -> list[str]:
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, ValueError) as exc:
        return ["witness schema unavailable or malformed: %s" % exc]
    errors = sorted(
        Draft202012Validator(schema).iter_errors(witness),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    issues = []
    for error in errors:
        locus = ".".join(str(part) for part in error.absolute_path) or "<root>"
        message = error.message
        if locus.endswith("state"):
            message = "evidence state outside the exact Task 5 vocabulary: %s" % message
        elif locus.startswith("claim_boundaries"):
            key = locus.rsplit(".", 1)[-1].replace("_", " ")
            message = "%s claim boundary: %s" % (key, message)
        elif locus.startswith("proof_protocol_placement"):
            message = "proof protocol requires a separate reviewed follow-up: %s" % message
        issues.append("witness schema %s: %s" % (locus, message))
    return issues


def _objects(value: object, label: str, issues: list[str]) -> list[dict]:
    if not isinstance(value, list):
        issues.append("%s must be an array" % label)
        return []
    rows = [row for row in value if isinstance(row, dict)]
    if len(rows) != len(value):
        issues.append("%s contains a non-object row" % label)
    return rows


def _refs(value: object) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {item for item in value if isinstance(item, str)}


def _has_source_authority(evidence_by_id: dict, ref: str, scope: str) -> bool:
    row = evidence_by_id.get(ref)
    if not isinstance(row, dict) or row.get("state") != "repository-verified":
        return False
    source_ref = row.get("source_ref")
    return isinstance(source_ref, str) and scope in SOURCE_AUTHORITY_SCOPES.get(source_ref, frozenset())


def _task4_r7e_events(issues: list[str]) -> dict[str, dict]:
    try:
        fixtures = yaml.safe_load(TASK4_FIXTURES_PATH.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        issues.append("retained Task 4 event owner is unavailable: %s" % exc)
        return {}
    if not isinstance(fixtures, dict):
        issues.append("retained Task 4 event owner must be structured")
        return {}
    provenance = {
        row.get("provenance_record_id"): row
        for row in fixtures.get("provenance_records", [])
        if isinstance(row, dict) and isinstance(row.get("provenance_record_id"), str)
    }
    retained = {}
    for event in fixtures.get("orthing_events", []):
        if not isinstance(event, dict) or not isinstance(event.get("event_id"), str):
            continue
        owner = provenance.get(event.get("provenance_record_id"))
        if (
            event.get("capture_mode") == "retrospective_reconstruction"
            and event.get("source_case") == "R7E"
            and isinstance(owner, dict)
            and owner.get("capture_mode") == "retrospective_reconstruction"
            and owner.get("source_case") == "R7E"
        ):
            retained[event["event_id"]] = event
    return retained


def _witness_issues(witness: dict) -> list[str]:
    issues: list[str] = []
    evidence = _objects(witness.get("evidence_registry"), "evidence registry", issues)
    evidence_ids = [row.get("evidence_id") for row in evidence]
    if len(evidence_ids) != len(set(map(str, evidence_ids))):
        issues.append("evidence registry has duplicate IDs")
    source_refs = [row.get("source_ref") for row in evidence]
    missing_sources = set(EXPECTED_SOURCE_STATES) - set(source_refs)
    if missing_sources or len(source_refs) != len(set(map(str, source_refs))):
        issues.append("evidence inventory is incomplete, renamed, or duplicates a source")
    evidence_by_id = {row.get("evidence_id"): row for row in evidence}
    registered = {key for key in evidence_by_id if isinstance(key, str)}

    for row in evidence:
        state = row.get("state")
        if state not in EVIDENCE_STATES:
            issues.append("evidence state outside the exact Task 5 vocabulary")
        source_ref = row.get("source_ref")
        expected = EXPECTED_SOURCE_STATES.get(source_ref)
        if expected and state != expected:
            if expected == "missing":
                issues.append("missing source %s cannot be promoted to %s" % (source_ref, state))
            elif expected == "implementing-run-attributed":
                issues.append("attributed statistic cannot be promoted to repository fact")
            else:
                issues.append("source %s must retain evidence state %s" % (source_ref, expected))
        claim_boundary = row.get("claim_boundary")
        if isinstance(claim_boundary, str) and PROMOTED_CLAIM.search(claim_boundary):
            issues.append("structured evidence claim exceeds its typed source purpose")

    objects = _objects(witness.get("witness_objects"), "witness objects", issues)
    object_ids = [row.get("object_id") for row in objects]
    if len(object_ids) != len(set(map(str, object_ids))):
        issues.append("duplicate witness object ID")
    kinds = [row.get("object_kind") for row in objects]
    if set(kinds) != OBJECT_KINDS or len(kinds) != len(set(kinds)):
        issues.append("witness object kinds are incomplete or duplicated")
    roles = {row.get("illustration_role") for row in objects}
    if roles != ILLUSTRATION_ROLES:
        issues.append("illustration roles must preserve historical fact, reconstruction, illustrative mapping, and unsupported runtime separately")
    for row in objects:
        kind = row.get("object_kind")
        if EXPECTED_OBJECT_ROLES.get(kind) != row.get("illustration_role"):
            issues.append("illustration role disagrees with object kind %s" % kind)
        description = row.get("description")
        if isinstance(description, str) and PROMOTED_CLAIM.search(description):
            issues.append("structured witness claim exceeds its illustration and evidence boundary")
        row_refs = _refs(row.get("evidence_refs"))
        if row.get("illustration_role") == "documented-historical-fact" and not any(
            evidence_by_id.get(ref, {}).get("state") == "repository-verified" for ref in row_refs
        ):
            issues.append("documented historical fact requires repository-verified supporting evidence")
        if row.get("illustration_role") == "unsupported-live-runtime-claim" and any(
            evidence_by_id.get(ref, {}).get("state") not in {"missing", "unresolved"} for ref in row_refs
        ):
            issues.append("unsupported live runtime illustration cannot be promoted by available evidence")

    referenced: set[str] = set()
    analysis = witness.get("declared_analysis")
    if isinstance(analysis, dict):
        referenced |= _refs(analysis.get("evidence_refs"))
    for row in objects:
        referenced |= _refs(row.get("evidence_refs"))
    audit = witness.get("higher_order_audit")
    if isinstance(audit, dict):
        referenced |= _refs(audit.get("original_t1_evidence_refs"))
        referenced |= _refs(audit.get("later_evidence_refs"))
    for ref in sorted(referenced - registered):
        issues.append("dangling evidence reference %s" % ref)

    history = witness.get("original_history")
    authoritative: set[str] = set()
    if isinstance(history, dict):
        authoritative = _refs(history.get("authoritative_identity_evidence_refs"))
        cardinality = history.get("episode_cardinality")
        identity_authorized = bool(authoritative) and all(
            _has_source_authority(evidence_by_id, ref, "original-identity") for ref in authoritative
        )
        if authoritative and not identity_authorized:
            issues.append("original identity authority must resolve through a typed owner")
        if cardinality != "underdetermined" and not identity_authorized:
            issues.append("original episode cardinality cannot be resolved without typed identity authority")
        if history.get("original_t1_checkpoint_status") != "missing" or history.get("original_t1_evidence_status") != "not-observed":
            issues.append("original t1 history cannot be promoted without a typed checkpoint owner")
        if history.get("capture_mode") != "retrospective_reconstruction":
            issues.append("R7E retrospective reconstruction cannot be relabeled as live capture or another mode")

    identities = _objects(witness.get("identity_records"), "identity records", issues)
    identity_kinds = [row.get("identity_kind") for row in identities]
    if set(identity_kinds) != IDENTITY_KINDS or len(identity_kinds) != len(set(identity_kinds)):
        issues.append("identity records must cover each distinct identity level exactly once")
    resolved_ids: dict[str, str] = {}
    for row in identities:
        identifier = row.get("identifier")
        kind = row.get("identity_kind")
        if kind in {"turn", "session", "episode", "occurrence", "orthing"} and (
            isinstance(identifier, str) or row.get("status") == "repository-verified"
        ):
            if not authoritative or not all(
                _has_source_authority(evidence_by_id, ref, "original-identity") for ref in authoritative
            ):
                issues.append("original identity %s cannot be resolved without typed identity authority" % kind)
        if isinstance(identifier, str):
            prior = resolved_ids.get(identifier)
            if prior and prior != kind:
                issues.append("turn, session, episode, occurrence, and orthing identity levels must remain distinct")
            resolved_ids[identifier] = str(kind)

    retained_events = _task4_r7e_events(issues)
    reconstruction = next((row for row in identities if row.get("identity_kind") == "reconstruction_event"), None)
    if not isinstance(reconstruction, dict) or reconstruction.get("status") != "reconstruction-only" or reconstruction.get("identifier") not in retained_events:
        issues.append("reconstruction event must resolve through the retained Task 4 event owner")

    if isinstance(audit, dict):
        if audit.get("subject_witness_id") != witness.get("witness_id"):
            issues.append("higher-order audit must identify its exact witness subject")
        audit_authority = audit.get("audit_authority_id")
        implementing_authority = audit.get("implementing_authority_id")
        canonical_authorities = all(
            isinstance(value, str) and AUTHORITY_ID.fullmatch(value) is not None
            for value in (audit_authority, implementing_authority)
        )
        if not canonical_authorities:
            issues.append("canonical authority IDs must be trimmed uppercase identifiers")
        normalized_audit = audit_authority.strip().casefold() if isinstance(audit_authority, str) else ""
        normalized_implementing = implementing_authority.strip().casefold() if isinstance(implementing_authority, str) else ""
        if audit.get("self_certifying") is not False or normalized_audit == normalized_implementing:
            issues.append("higher-order audit cannot self-certify the implementing witness")
        original_t1 = _refs(audit.get("original_t1_evidence_refs"))
        later = _refs(audit.get("later_evidence_refs"))
        if original_t1 & later or any("SOL" in ref for ref in original_t1):
            issues.append("later evidence cannot be inserted into the original t1 evidence state")
        if original_t1 and not all(_has_source_authority(evidence_by_id, ref, "original-t1-history") for ref in original_t1):
            issues.append("original t1 evidence must resolve through a typed history owner")
        expected_target_boundary = (
            "unresolved", "missing", "not-observed", "record-insufficient", "not-established"
        )
        observed_target_boundary = (
            audit.get("authoritative_target_identity_status"),
            audit.get("target_history_checkpoint_status"),
            audit.get("target_history_digest_status"),
            audit.get("meta_orthability_disposition"),
            audit.get("somnic_conformance"),
        )
        if observed_target_boundary != expected_target_boundary:
            issues.append("target-history authority is absent; the R7E review must remain record-insufficient")
        unresolved_target = audit.get("authoritative_target_identity_status") != "repository-verified"
        missing_checkpoints = audit.get("target_history_checkpoint_status") != "repository-verified"
        missing_digest = audit.get("target_history_digest_status") != "repository-verified"
        if (unresolved_target or missing_checkpoints or missing_digest) and audit.get("meta_orthability_disposition") != "record-insufficient":
            issues.append("record-insufficient meta-orthability disposition is required for unavailable target history")
        if (unresolved_target or missing_checkpoints or missing_digest) and audit.get("somnic_conformance") != "not-established":
            issues.append("somnic conformance cannot be established without authoritative target identity, checkpoints, and digest")

    boundaries = witness.get("claim_boundaries")
    if isinstance(boundaries, dict):
        for key, expected in CLAIM_BOUNDARIES.items():
            if boundaries.get(key) != expected:
                issues.append("%s claim boundary must remain %s" % (key.replace("_", " "), expected))

    proof = witness.get("proof_protocol_placement")
    if isinstance(proof, dict) and (
        proof.get("status") != "requires-separately-numbered-reviewed-follow-up"
        or proof.get("implemented") is not False
        or proof.get("normative_owner_created") is not False
    ):
        issues.append("proof, grant, and receipt semantics require a separate reviewed follow-up")
    return issues


def _crosswalk_issues(witness: dict, crosswalk: object) -> list[str]:
    if not isinstance(crosswalk, dict):
        return ["somnic case crosswalk must be an object"]
    issues = []
    expected_keys = {"schema", "status", "witness_ref", "source_case", "original_history", "later_review", "relation_disposition", "illustration_roles", "evidence_refs"}
    if set(crosswalk) != expected_keys:
        issues.append("somnic case crosswalk fields are incomplete or expanded")
    if crosswalk.get("schema") != "orthemology-r7e-somnic-case-crosswalk-v1" or crosswalk.get("status") != "current-candidate":
        issues.append("somnic case crosswalk schema or status is invalid")
    if crosswalk.get("witness_ref") != witness.get("witness_id") or crosswalk.get("source_case") != "R7E":
        issues.append("somnic case crosswalk must resolve the exact R7E witness")

    history = crosswalk.get("original_history")
    witness_history = witness.get("original_history")
    if not isinstance(history, dict) or not isinstance(witness_history, dict):
        issues.append("somnic case crosswalk original history must be structured")
    else:
        expected = {
            "episode_cardinality": witness_history.get("episode_cardinality"),
            "target_identity_status": "unresolved",
            "t1_checkpoint_status": witness_history.get("original_t1_checkpoint_status"),
            "t1_evidence_partition_status": witness_history.get("original_t1_evidence_status"),
            "capture_mode": witness_history.get("capture_mode"),
        }
        if history != expected:
            issues.append("crosswalk must preserve underdetermined original identity and t1 boundaries")

    audit = witness.get("higher_order_audit")
    later = crosswalk.get("later_review")
    if not isinstance(audit, dict) or not isinstance(later, dict):
        issues.append("later review crosswalk must be structured")
    else:
        expected_later = {
            "audit_ref": audit.get("audit_id"),
            "assessment_kind": audit.get("assessment_kind"),
            "meta_orthability_disposition": audit.get("meta_orthability_disposition"),
            "somnic_conformance": audit.get("somnic_conformance"),
        }
        if later != expected_later:
            issues.append("later review crosswalk must preserve retrospective assessment and meta-orthability boundaries")

    relation = crosswalk.get("relation_disposition")
    if not isinstance(relation, dict):
        issues.append("relation disposition must be structured")
    elif relation.get("inter_somnic_relation") != "not-established" or relation.get("temporal_separation_is_sufficient") is not False:
        issues.append("temporal separation alone cannot establish an inter-somnic relation")
    else:
        reason = relation.get("reason")
        if not isinstance(reason, str) or not reason.strip() or TEMPORAL_RELATION_PROMOTION.search(reason):
            issues.append("relation reason contradicts the not-established temporal disposition")
    roles = crosswalk.get("illustration_roles")
    if not isinstance(roles, list) or set(roles) != ILLUSTRATION_ROLES or len(roles) != len(ILLUSTRATION_ROLES):
        issues.append("crosswalk illustration roles are incomplete or duplicated")

    registered = {
        row.get("evidence_id")
        for row in witness.get("evidence_registry", [])
        if isinstance(row, dict) and isinstance(row.get("evidence_id"), str)
    }
    for ref in sorted(_refs(crosswalk.get("evidence_refs")) - registered):
        issues.append("crosswalk has dangling evidence reference %s" % ref)
    return issues


def _narrative_issues(witness: dict, narrative: object) -> list[str]:
    if not isinstance(narrative, str):
        return ["witness narrative must be UTF-8 text"]
    issues = []
    required = [str(witness.get("witness_id", "")), "record-insufficient meta-orthability", "not deployed Somnus", "does not establish comparative utility"]
    for phrase in required:
        if phrase and phrase not in narrative:
            issues.append("witness narrative omits required boundary: %s" % phrase)
    unsafe = re.compile(
        r"\b(?:proves?|establishes|demonstrates|validates|implements|deploys)\b[^.\n]{0,100}\b(?:correctness|comparative utility|empirical validation|terminology benefit|terminology adoption|internal model ontology|generalization|recurrence|frontier|writeback|autonomy|runtime|Somnus)\b",
        re.IGNORECASE,
    )
    if unsafe.search(narrative):
        issues.append("witness narrative contains an unqualified promoted claim")
    return issues


def collect_issues(witness: object, crosswalk: object, narrative: object) -> list[str]:
    issues = _schema_issues(witness)
    if not isinstance(witness, dict):
        issues.append("LLM-mediated witness must be an object")
        return issues + _crosswalk_issues({}, crosswalk) + _narrative_issues({}, narrative)
    issues.extend(_witness_issues(witness))
    issues.extend(_crosswalk_issues(witness, crosswalk))
    issues.extend(_narrative_issues(witness, narrative))
    return issues


def _load_yaml(path: Path) -> tuple[object, list[str]]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), []
    except (OSError, yaml.YAMLError) as exc:
        return {}, ["cannot read %s: %s" % (path.name, exc)]


def main() -> None:
    issues: list[str] = []
    witness, load_issues = _load_yaml(WITNESS_PATH)
    issues.extend(load_issues)
    crosswalk, load_issues = _load_yaml(CROSSWALK_PATH)
    issues.extend(load_issues)
    try:
        narrative = NARRATIVE_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        narrative = ""
        issues.append("cannot read witness narrative: %s" % exc)
    try:
        issues.extend(collect_issues(witness, crosswalk, narrative))
    except Exception as exc:  # fail closed at the CLI boundary
        issues.append("malformed witness input: %s: %s" % (type(exc).__name__, exc))
    for issue in issues:
        print("[FAIL] %s" % issue)
    if not issues:
        print("[PASS] bounded R7E LLM-mediated orthing witness")
    print("TOTAL: %d failures" % len(issues))
    raise SystemExit(1 if issues else 0)


if __name__ == "__main__":
    main()
