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
from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
ACTIVATION_PATH = ROOT / "examples" / "somnus" / "activation-contract-fixtures.yaml"
RECORDS_PATH = ROOT / "examples" / "somnus" / "somnus-record-fixtures.yaml"
HISTORY_PATH = ROOT / "examples" / "somnus" / "somnus-history-checkpoints.yaml"
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
    "somnic_episodes": "somnic-episode.schema.json",
    "somnic_assessments": "somnic-assessment.schema.json",
    "inter_somnic_relations": "inter-somnic-relation.schema.json",
    "recurrence_reports": "residual-recurrence-report.schema.json",
}
AUX_SCHEMA_NAMES = {
    "activation_bundle": "activation-contract-fixtures.schema.json",
    "records_bundle": "somnus-record-fixtures.schema.json",
    "history_checkpoints": "somnus-history-checkpoints.schema.json",
    "claim_status": "somnus-claim-status.schema.json",
    "candidate_inventory": "somnus-candidate-inventory.schema.json",
    "adoption_profile": "hermes-writeback-adoption-profile.schema.json",
    "collective_profile": "collective-somnus-transclusion-profile.schema.json",
}
FIXTURE_CLASSES = {"positive", "negative-near-boundary", "indeterminate", "overlap"}
TRI_STATE = {"applicable", "inapplicable", "indeterminate"}
PINNED_INDEPENDENCE_POLICY = {
    "rule_id": "independence-rule-v1",
    "rule_version": "1.0.0",
    "required_dimensions": [
        "session_count", "normalized_input_family_count", "actor_count",
        "source_family_count",
    ],
    "pass_label": "independent episodes",
    "fail_label": "distinct episodes",
    "immutable": True,
}
PINNED_INDEPENDENCE_POLICY_DIGEST = hashlib.sha256(
    json.dumps(
        PINNED_INDEPENDENCE_POLICY, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
).hexdigest()
EXPECTED_HISTORY_CHAIN = {
    "chain_id": "somnus-target-history",
    "chain_version": "1.0.0",
    "digest_algorithm": "sha256-canonical-json-v1",
    "authority_ref": "docs/decisions/0035-somnic-orthing-and-activation-contracts.md#history-checkpoint-chain",
    "immutable": True,
}
EXPECTED_VERSION_TRANSITION_AUTHORITY = {
    "authority_ref": "docs/decisions/0035-somnic-orthing-and-activation-contracts.md#activation-and-claimant-routing",
    "append_only": True,
    "accepted_versions": [
        {
            "artifact_kind": "activation_contract",
            "artifact_id": "database-schema-activation",
            "artifact_version": "1.0.0",
            "sequence": 1,
            "supersedes": None,
        },
        {
            "artifact_kind": "activation_contract",
            "artifact_id": "recurrence-meta-assessability",
            "artifact_version": "1.0.0",
            "sequence": 1,
            "supersedes": None,
        },
        {
            "artifact_kind": "activation_contract",
            "artifact_id": "theological-claimant-activation",
            "artifact_version": "1.0.0",
            "sequence": 1,
            "supersedes": None,
        },
        {
            "artifact_kind": "orthability_evaluator",
            "artifact_id": "property-boundary-evaluator",
            "artifact_version": "1.0.0",
            "sequence": 1,
            "supersedes": None,
        },
    ],
}
EXPECTED_REFERENCE_CORPUS_OWNER = (
    "docs/decisions/0035-somnic-orthing-and-activation-contracts.md#frontier-recurrence-and-retrospective-loci"
)
EXPECTED_AUTHORIZATION_RULES = {
    "independent-governance-rule@1": {
        "authorization_rule_ref": "independent-governance-rule@1",
        "rule_id": "independent-governance-rule",
        "rule_version": "1",
        "owner_ref": "docs/decisions/0035-somnic-orthing-and-activation-contracts.md#writeback-and-authorization-boundary",
        "ordering_scope": "proposal",
        "ordering_key": "decided_at",
        "simultaneous_decisions": "prohibited",
        "immutable": True,
    },
}
EXPECTED_RUN_OWNER_ROLES = {"analysis", "operation_contract"}
EXPECTED_CANDIDATE_EVENTS = {
    "orthability-check": {"orthability_assessed"},
    "orthing-ledger": {
        "occurrence_apprehended", "placement_committed", "residual_recorded",
        "orthing_closed", "orthing_abandoned",
    },
    "episode-residual-live": {"residual_recorded"},
    "residual-recurrence-somnic": {"somnus_assessment_emitted"},
    "metaorthemma-conflict": {"candidate_set_recorded", "route_selected"},
    "intervention-disposition": {"somnus_assessment_emitted"},
    "verdict-aware-patch-proposal": {"proposal_emitted"},
    "guarded-writeback-actuator": {"proposal_emitted"},
    "orthing-dream": {"somnus_assessment_emitted"},
    "somnus-export": {"none"},
    "somnus-import": {"none"},
    "metaortheme-transclusion": {"none"},
    "collective-somnus": {"none"},
    "somnus-council": {"none"},
    "transclusion-ledger": {"none"},
}
STANDARD_CANDIDATE_NON_CLAIMS = {
    "executable_skill": "not-implemented",
    "deployed_runtime": "not-implemented",
    "correctness": "not-established",
    "empirical_utility": "not-established",
}
PROHIBITED_CANDIDATE_OPERATIONS = {
    "schedule_runtime", "execute_mutation", "promote_governance",
    "close_governance_finding", "mutate_governance",
}
ORDERED_ACTUATOR_STAGES = [
    "proposal", "review", "approve_or_reject", "validation", "dry_run",
    "apply_or_revert",
]
EXPECTED_PREDECESSOR_CLASSIFICATION = {
    "relative_granularity": "coarser_or_more_implicit",
    "scope": [
        "source_interpretation", "proposal_generation", "destination_selection",
        "safe_writeback",
    ],
}
EXPECTED_GUARDED_ACTUATOR_OUTPUTS = {
    "application or rejection record", "revert provenance",
}
ALLOWED_CANDIDATE_OWNER_ROLES = {
    "agent-host routing owner", "durable-ledger owner", "runtime capture owner",
    "somnus operation owner after successor trigger", "conflict-detection owner",
    "intervention-governance owner", "proposal owner", "writeback runtime owner",
    "host/orchestrator owner", "transport owner", "import owner",
    "normative-adoption owner", "collective-assessment owner", "council owner",
    "transclusion-ledger owner", "external change-proposal custodian",
    "downstream guarded actuation service owner",
    "external bounded-record custody operator",
}
EXPECTED_CANDIDATE_SEMANTIC_DIGESTS = {
    "orthability-check": "cf242d6b54f20dd7ca776dce776fe172ca96baada846f5737dd8c929b9a892c9",
    "orthing-ledger": "e314f6dd4188c8481228e6a59c9a1144b082cbee76e08d9bf2d8731bdeda8575",
    "episode-residual-live": "682785d794617c1ee8c03dedcb321aaf44d8e362c9e93fef7799cc62b798ddab",
    "residual-recurrence-somnic": "364575d6b029447652b77d41ad72b502b897ecbdba125a80cc7c1f15c0b93f05",
    "metaorthemma-conflict": "a715f118f81c7c05490054aca1af361e6eab5e0d7ceb110f4a4fe51692f098ab",
    "intervention-disposition": "ea50fc7bfb34b7b9e94571bcc19a372e82e577676ee91452675bb164126d74cf",
    "verdict-aware-patch-proposal": "dcd6bfb2601b45d39de63ff241891be2e970d157539799e387fc4ebc0e570afc",
    "guarded-writeback-actuator": "e626342b1ea5a7da722fd01d326238815b15801f0b0c9bde24eef41944f0321e",
    "orthing-dream": "203272f6ab25c97f4632d766be0db11c650cc32de198431f72a505e551997e6c",
    "somnus-export": "08d7af255fc294ca6241f9364687e76ab7da37260a389f52dbfc586cd707299f",
    "somnus-import": "116183a002eabd25f65041a279a50c80c28c30cf4976291a464e152d5dca7c36",
    "metaortheme-transclusion": "97050e0300e0ba878428aadad0cad42764a0b7101ac96c53062516438e518ec3",
    "collective-somnus": "4cfdaa1168b60612a99eed9ac972428a2eaf01165c7ad585f40b344a04de8957",
    "somnus-council": "907513e41452df6b872c75a26faf3d2a2f05106e00f25f659f9dfe8904a43b41",
    "transclusion-ledger": "63883269de990dc4d6f2ab4121dca195eb19502c3580178016992445771381fe",
}
CANDIDATE_OWNER_ROLE_ALIASES = {
    "verdict-aware-patch-proposal": {
        "external change-proposal custodian": "proposal owner",
    },
    "guarded-writeback-actuator": {
        "downstream guarded actuation service owner": "writeback runtime owner",
    },
    "somnus-export": {
        "external bounded-record custody operator": "transport owner",
    },
}
EXPECTED_CANDIDATE_RESIDUALS = {
    "orthability-check": "retain inapplicable and indeterminate attempts",
    "orthing-ledger": "append interruption and incomplete-record residuals",
    "episode-residual-live": "preserve raw text and governed disposition",
    "residual-recurrence-somnic": "preserve dependence and counterexample uncertainty",
    "metaorthemma-conflict": "retain conflict and confidence effect",
    "intervention-disposition": "no-change and held residuals remain valid outcomes",
    "verdict-aware-patch-proposal": "rejection and failure do not rewrite assessment",
    "guarded-writeback-actuator": "failed application preserves histories",
    "orthing-dream": "closed outputs remain outside the frontier absent material delta",
    "somnus-export": "disclose redactions and non-claims",
    "somnus-import": "hold incompatible or insufficient packets",
    "metaortheme-transclusion": "retain source/local version distinction",
    "collective-somnus": "preserve unresolved conflict and scope limits",
    "somnus-council": "preserve plural closure",
    "transclusion-ledger": "record cycles, redactions, and incompatible versions",
}
ALLOWED_PREDECESSOR_CHARACTERIZATIONS = {
    "coarser-or-more-implicit orthing oriented toward source interpretation, proposal generation, destination selection, and safe writeback",
    "a coarser or more implicit orthing architecture focused on source interpretation, proposal generation, destination selection, and safe writeback",
    "a more implicit and coarser predecessor covering safe destination-bound proposal writeback",
}
DELTA_OWNER_ROLES = {
    "analysis_revision": "analysis",
    "contract_revision": "operation_contract",
    "selection_rule_revision": "selection_rule",
    "evaluator_revision": "evaluator",
    "metaortheme_revision": "metaortheme",
    "contradicting_evidence": "evidence",
    "later_outcome": "outcome",
    "assessment_conflict": "assessment",
    "expiry": "expiry",
    "governance_action": "governance",
}


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


def _canonical_digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _version_authority_issues(authority):
    """Validate fixed version rows as an explicitly sequenced registry, not a list."""
    issues = []
    if not isinstance(authority, dict):
        return ["activation version transition authority must be an object"]
    if authority.get("authority_ref") != EXPECTED_VERSION_TRANSITION_AUTHORITY["authority_ref"]:
        issues.append("activation version transition authority must retain its Decision 0035 owner")
    if authority.get("append_only") is not True:
        issues.append("activation version transition authority must remain append-only")
    rows = authority.get("accepted_versions")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        return issues + ["activation accepted versions must be typed records"]
    expected_rows = EXPECTED_VERSION_TRANSITION_AUTHORITY["accepted_versions"]
    key = lambda row: (row.get("artifact_kind"), row.get("artifact_id"), row.get("artifact_version"))
    actual_by_key = {}
    for row in rows:
        identity = key(row)
        if not all(isinstance(part, str) and part for part in identity):
            issues.append("activation accepted version has an incomplete typed identity")
            continue
        if identity in actual_by_key:
            issues.append("activation accepted versions duplicate %s@%s" % (identity[1], identity[2]))
        else:
            actual_by_key[identity] = row
    expected_by_key = {key(row): row for row in expected_rows}
    if actual_by_key != expected_by_key:
        issues.append(
            "activation contract and evaluator versions must resolve to the fixed append-only Decision 0035 transition authority"
        )
    chains = defaultdict(list)
    for identity, row in actual_by_key.items():
        sequence = row.get("sequence")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 1:
            issues.append("activation accepted version %s@%s requires a positive sequence" % (identity[1], identity[2]))
        chains[(identity[0], identity[1])].append(row)
    for chain_key, chain in chains.items():
        sequence_values = [
            row.get("sequence") for row in chain
            if isinstance(row.get("sequence"), int)
            and not isinstance(row.get("sequence"), bool)
        ]
        if len(sequence_values) != len(set(sequence_values)):
            issues.append("activation version chain %s/%s duplicates a sequence" % chain_key)
        ordered = sorted(
            (row for row in chain
             if isinstance(row.get("sequence"), int)
             and not isinstance(row.get("sequence"), bool)),
            key=lambda row: row["sequence"],
        )
        for index, row in enumerate(ordered):
            expected_supersedes = None if index == 0 else ordered[index - 1].get("artifact_version")
            if row.get("supersedes") != expected_supersedes:
                issues.append("activation version chain %s/%s has inconsistent supersession" % chain_key)
    return issues


def _candidate_semantic_digest(candidate):
    owner = candidate.get("downstream_owner")
    normalized_owner = dict(owner) if isinstance(owner, dict) else owner
    candidate_id = candidate.get("candidate_id")
    if isinstance(normalized_owner, dict):
        aliases = _string_lookup(CANDIDATE_OWNER_ROLE_ALIASES, candidate_id) or {}
        role = normalized_owner.get("owner_role")
        if isinstance(role, str):
            normalized_owner["owner_role"] = aliases.get(role, role)
    projection = {
        "layer": candidate.get("layer"),
        "inputs": sorted(_string_set(candidate.get("inputs"))),
        "outputs": sorted(_string_set(candidate.get("outputs"))),
        "dependencies": sorted(_string_set(candidate.get("dependencies"))),
        "downstream_owner": normalized_owner,
    }
    return _canonical_digest(projection)


def _heading_slug(value):
    value = re.sub(r"[`*_]", "", value.strip().lower())
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", value)).strip("-")


def _rendered_inline_text(token, parser=None):
    """Return the visible text represented by a CommonMark inline token."""
    parser = parser or MarkdownIt("commonmark")
    parts = []
    for child in token.children or []:
        if child.type in {"text", "text_special", "code_inline"}:
            parts.append(child.content)
        elif child.type == "image":
            image_inline = parser.parseInline(child.content)[0]
            parts.append(_rendered_inline_text(image_inline, parser))
        elif child.type in {"softbreak", "hardbreak"}:
            parts.append(" ")
    return "".join(parts)


def _markdown_heading_slugs(document):
    """Return slugs for document-owned top-level CommonMark headings."""
    headings = []
    parser = MarkdownIt("commonmark")
    tokens = parser.parse(document)
    for index, token in enumerate(tokens[:-1]):
        inline = tokens[index + 1]
        if (token.type == "heading_open"
                and token.level == 0
                and inline.type == "inline"):
            headings.append(_heading_slug(_rendered_inline_text(inline, parser)))
    return headings


def _decision_authority_issues(decision_text, authority_refs):
    if not isinstance(decision_text, str):
        return ["Decision authority references cannot resolve without Decision 0035"]
    heading_counts = Counter(_markdown_heading_slugs(decision_text))
    issues = []
    decision_path = "docs/decisions/0035-somnic-orthing-and-activation-contracts.md"
    for authority_ref in sorted(authority_refs, key=lambda value: str(value)):
        if not isinstance(authority_ref, str) or "#" not in authority_ref:
            issues.append("Decision authority reference %r is not a typed path fragment" % authority_ref)
            continue
        path, fragment = authority_ref.split("#", 1)
        if path != decision_path or heading_counts.get(fragment) != 1:
            issues.append("Decision authority reference %s must resolve to exactly one owned heading" % authority_ref)
    return issues


def _activation_contract_digest(contract):
    return _canonical_digest(contract)


def _activation_fixture_digest(outcome):
    projection = {
        key: value for key, value in outcome.items()
        if key not in {"occurrence", "observed_indicators", "observed_exclusions"}
    }
    projection["claimant_assessments"] = [
        {
            key: value for key, value in assessment.items()
            if key not in {"observed_indicators", "observed_exclusions"}
        }
        for assessment in outcome.get("claimant_assessments", [])
        if isinstance(assessment, dict)
    ]
    return _canonical_digest(projection)


def _normalized_words(value):
    if not isinstance(value, str):
        return set()
    return set(re.findall(r"[a-z]+", value.lower().replace("-", " ")))


def _activation_issues(document, schemas, store):
    issues = []
    issues += _schema_issues(
        "activation", document, schemas[AUX_SCHEMA_NAMES["activation_bundle"]], store
    )
    contracts = _objects(document, "contracts", issues, "activation")
    evaluators = _objects(document, "evaluators", issues, "activation")
    authoring_records = _objects(document, "authoring_records", issues, "activation")
    outcomes = _objects(document, "fixture_outcomes", issues, "activation")
    transition_authority = _mapping(
        document.get("version_transition_authority") if isinstance(document, dict) else None,
        "activation.version_transition_authority", issues,
    )
    issues += _version_authority_issues(transition_authority)
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
    authority_refs = {
        identity
        for row in transition_authority.get("accepted_versions", [])
        if isinstance(row, dict)
        for identity in [
            _string_tuple_key(
                row.get("artifact_kind"),
                row.get("artifact_id"),
                row.get("artifact_version"),
            )
        ]
        if identity is not None
    }
    if any(
        ("activation_contract", key[0], key[1]) not in authority_refs
        for key in contract_by_key
    ):
        issues.append("every activation contract version must resolve through the append-only transition authority")
    if any(
        ("orthability_evaluator", key[0], key[1]) not in authority_refs
        for key in evaluator_by_key
    ):
        issues.append("every evaluator version must resolve through the append-only transition authority")

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
            indicators = assessment.get("observed_indicators")
            if not isinstance(indicators, list):
                issues.append("fixture %s observed_indicators must be an array" % fixture_id)
                indicators = []
            if not _string_set(indicators) <= _string_set(contract.get("positive_indicators")):
                issues.append(
                    "fixture %s indicators must be owned by its exact activation contract/version"
                    % fixture_id
                )
            if not _string_set(exclusions) <= _string_set(contract.get("exclusion_indicators")):
                issues.append(
                    "fixture %s exclusions must be owned by its exact activation contract/version"
                    % fixture_id
                )
            result = assessment.get("result")
            if not isinstance(result, str) or result not in TRI_STATE:
                issues.append("fixture %s has result outside tri-state vocabulary" % fixture_id)
            elif result == "applicable" and (required != finding_sets["satisfied"] or controlling_exclusion):
                issues.append("fixture %s cannot infer applicability while required properties are absent, indeterminate, or excluded" % fixture_id)
            elif result == "inapplicable" and not (finding_sets["absent"] or controlling_exclusion):
                issues.append("fixture %s cannot be inapplicable when all required properties are satisfied and no exclusion controls" % fixture_id)
            elif result == "indeterminate" and not finding_sets["indeterminate"]:
                issues.append("fixture %s indeterminate result requires an indeterminate required property" % fixture_id)

        aggregate_findings = {
            field: set().union(*(
                _string_set(_mapping(
                    assessment.get("property_findings"),
                    "fixture %s property_findings" % fixture_id, issues,
                ).get(field))
                for assessment in assessments
            ))
            for field in ("satisfied", "absent", "indeterminate")
        }
        summary_findings = _mapping(
            outcome.get("property_findings"),
            "fixture %s top-level property_findings" % fixture_id, issues,
        )
        if any(_string_set(summary_findings.get(field)) != aggregate_findings[field]
               for field in aggregate_findings):
            issues.append(
                "fixture %s top-level property findings must equal the deterministic claimant union"
                % fixture_id
            )
        for field in ("observed_indicators", "observed_exclusions"):
            aggregate = set().union(*(
                _string_set(assessment.get(field)) for assessment in assessments
            ))
            if _string_set(outcome.get(field)) != aggregate:
                issues.append(
                    "fixture %s top-level %s must equal the deterministic claimant union"
                    % (fixture_id, field)
                )

        if fixture_class == "overlap":
            conflict = _mapping(outcome.get("conflict"), "overlap fixture %s conflict" % fixture_id, issues)
            named = conflict.get("claimant_contracts")
            if (not isinstance(named, list) or len(_string_set(named)) < 2
                    or _string_set(contract_keys_in_fixture) != _string_set(named)
                    or conflict.get("disposition") not in {"provisional_multi_claimant", "hold", "defer"}
                    or conflict.get("conflict_unresolved") is not True
                    or not conflict.get("authorization_rule_id")):
                issues.append("overlap fixture %s requires a structured conflict and disposition" % fixture_id)
        results = {
            assessment.get("result") for assessment in assessments
            if isinstance(assessment.get("result"), str)
        }
        class_matches = (
            (fixture_class == "positive" and results == {"applicable"})
            or (fixture_class == "negative-near-boundary" and results == {"inapplicable"})
            or (fixture_class == "indeterminate" and results == {"indeterminate"})
            or (fixture_class == "overlap"
                and len(assessments) >= 2
                and results == {"applicable"})
        )
        if not class_matches:
            issues.append(
                "fixture %s class must match its exact claimant-result semantics"
                % fixture_id
            )

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
            if isinstance(fixture_class, str) and fixture_id in refs
        }
        if represented != FIXTURE_CLASSES:
            issues.append("accepted contract %s requires per-contract positive, negative-near-boundary, indeterminate, and overlap assessments" % contract.get("contract_id"))
        exact_fixture_ids = {
            fixture_id for _, fixture_id, _ in assessments_by_contract.get(key, [])
        }
        if _string_set(refs) != exact_fixture_ids:
            issues.append(
                "accepted contract %s fixture set must equal the exact assessed fixtures"
                % contract.get("contract_id")
            )
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
                    or _string_set(record.get("fixture_ids")) != _string_set(refs)
                    or record.get("contract_body_digest")
                    != _activation_contract_digest(contract)
                    or record.get("fixture_semantic_digests") != {
                        fixture_id: _activation_fixture_digest(outcome_by_id[fixture_id])
                        for fixture_id in sorted(_string_set(refs))
                        if fixture_id in outcome_by_id
                    }):
                issues.append("accepted contract %s requires an exact immutable bootstrap authoring record" % contract.get("contract_id"))
    contract_refs = {"%s@%s" % key: row for key, row in contract_by_key.items()}
    for contract_ref, contract in contract_refs.items():
        supersedes = contract.get("supersedes")
        superseded_by = contract.get("superseded_by")
        if supersedes == contract_ref or superseded_by == contract_ref:
            issues.append("activation contract %s cannot supersede itself" % contract_ref)
        if isinstance(supersedes, str):
            predecessor = contract_refs.get(supersedes)
            if predecessor is None or predecessor.get("superseded_by") != contract_ref:
                issues.append("activation contract %s supersession must be reciprocal" % contract_ref)
        if isinstance(superseded_by, str):
            successor = contract_refs.get(superseded_by)
            if (successor is None or successor.get("supersedes") != contract_ref
                    or contract.get("status") == "accepted"):
                issues.append("activation contract %s successor state must be reciprocal and status-compatible" % contract_ref)
    for start in contract_refs:
        seen = set()
        current = start
        while isinstance(current, str) and current in contract_refs:
            if current in seen:
                issues.append("activation contract supersession graph must be acyclic")
                break
            seen.add(current)
            current = contract_refs[current].get("superseded_by")
    return issues


def _records_issues(document, activation, history, schemas, store):
    issues = []
    issues += _schema_issues(
        "records", document, schemas[AUX_SCHEMA_NAMES["records_bundle"]], store
    )
    if isinstance(document, dict):
        issues += _schema_issues(
            "records.claim_status", document.get("claim_status"),
            schemas[AUX_SCHEMA_NAMES["claim_status"]], store,
        )
    issues += _schema_issues(
        "history checkpoints", history,
        schemas[AUX_SCHEMA_NAMES["history_checkpoints"]], store,
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
    somnic_episodes = collections["somnic_episodes"]
    assessments = collections["somnic_assessments"]
    inter_somnic_relations = collections["inter_somnic_relations"]
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
        "claimant_ids",
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
        "claimant_ids": "claimant",
    }
    for field, kind in fixture_kind.items():
        for identity_id in identity_sets[field]:
            if identity_kind_by_id.get(identity_id) != kind:
                issues.append("identity fixture %s must resolve as typed %s" % (identity_id, kind))

    provenance_rows = _objects(document, "provenance_records", issues, "records")
    provenance_by_id = _unique_index(
        provenance_rows, "provenance_record_id", "provenance registry", issues
    )
    lifecycle_rows = _objects(
        document, "lifecycle_associations", issues, "records"
    )
    lifecycle_by_occurrence = _unique_index(
        lifecycle_rows, "occurrence_id", "lifecycle association registry", issues
    )

    contract_authoring_rows = _objects(
        document, "contract_authoring_records", issues, "records"
    )
    contract_authoring_by_id = _unique_index(
        contract_authoring_rows, "authoring_record_id",
        "contract authoring registry", issues,
    )

    route_rows = _objects(document, "claimant_routing_cases", issues, "records")
    _unique_index(route_rows, "case_id", "claimant routing cases", issues)
    selected_route_pairs = {}
    selected_route_claimants = {}
    route_pair_owners = {}
    claim_attempt_owners = {}
    assessment_identity_owners = {}
    route_assessments_by_occurrence = defaultdict(dict)
    route_occurrences = set()
    for route in route_rows:
        occurrence_id = route.get("occurrence_id")
        if isinstance(occurrence_id, str):
            if occurrence_id in route_occurrences:
                issues.append(
                    "claimant routing occurrence %s must have exactly one routing case"
                    % occurrence_id
                )
            route_occurrences.add(occurrence_id)
            if _string_lookup(identity_kind_by_id, occurrence_id) != "occurrence":
                issues.append(
                    "claimant route %s occurrence must resolve through the global typed identity registry"
                    % route.get("case_id")
                )
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
                selected_route_claimants[occurrence_id] = selected.get("claimant_id")
        elif route.get("route_status") in {"deferred", "no_claim"}:
            if route.get("selected_claimant_id") is not None:
                issues.append(
                    "claimant route %s cannot select a claimant in deferred or no-claim state"
                    % route.get("case_id")
                )
        for row in route_assessments:
            if not isinstance(row, dict):
                continue
            if not _string_member(identity_sets["claim_attempt_ids"], row.get("claim_attempt_id")):
                issues.append("claimant route %s has unresolved claim attempt" % route.get("case_id"))
            if not _string_member(identity_sets["orthability_assessment_ids"], row.get("orthability_assessment_id")):
                issues.append("claimant route %s has unresolved orthability assessment" % route.get("case_id"))
            if _string_lookup(identity_kind_by_id, row.get("claimant_id")) != "claimant":
                issues.append(
                    "claimant route %s claimant must resolve through the global typed identity registry"
                    % route.get("case_id")
                )
            pair = _string_tuple_key(
                row.get("claim_attempt_id"), row.get("orthability_assessment_id")
            )
            if pair is not None and isinstance(occurrence_id, str):
                claimant_id = row.get("claimant_id")
                owner = (occurrence_id, claimant_id)
                prior_pair_owner = route_pair_owners.get(pair)
                if prior_pair_owner is not None and prior_pair_owner != owner:
                    issues.append(
                        "claimant route %s reassigns one assessment pair across occurrences or claimants"
                        % route.get("case_id")
                    )
                elif isinstance(claimant_id, str):
                    route_pair_owners[pair] = owner
                    route_assessments_by_occurrence[occurrence_id][pair] = claimant_id
                for identity_id, registry, label in (
                    (row.get("claim_attempt_id"), claim_attempt_owners, "claim attempt"),
                    (row.get("orthability_assessment_id"), assessment_identity_owners,
                     "orthability assessment"),
                ):
                    if not isinstance(identity_id, str):
                        continue
                    prior_owner = registry.get(identity_id)
                    if prior_owner is not None and prior_owner != owner:
                        issues.append(
                            "%s %s must have one occurrence and claimant owner"
                            % (label, identity_id)
                        )
                    else:
                        registry[identity_id] = owner
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
    source_record_rows = _objects(document, "source_records", issues, "records")
    source_record_by_id = _unique_index(
        source_record_rows, "source_record_id", "authoritative source records", issues
    )
    source_by_subject = {}
    for source in source_record_rows:
        source_id = source.get("source_record_id")
        subject_id = source.get("subject_id")
        prior = source_by_subject.get(subject_id) if isinstance(subject_id, str) else None
        if prior is not None:
            issues.append(
                "subject %s has conflicting authoritative source records %s and %s"
                % (subject_id, prior, source_id)
            )
        elif isinstance(subject_id, str):
            source_by_subject[subject_id] = source_id
        if subject_id not in subject_by_id:
            issues.append("source record %s has an unresolved subject owner" % source_id)
        for field, expected_kind in (
                ("subject_id", "orthing"), ("session_id", "session"),
                ("episode_id", "episode"), ("actor_id", "actor")):
            value = source.get(field)
            if _string_lookup(identity_kind_by_id, value) != expected_kind:
                issues.append(
                    "source record %s %s must resolve as a typed %s identity"
                    % (source_id, field, expected_kind)
                )
    for subject_id, subject in subject_by_id.items():
        subject_kind = subject.get("subject_kind")
        if isinstance(subject_kind, str) and subject_kind in {"waking_orthing", "counterexample"}:
            if identity_kind_by_id.get(subject_id) != "orthing":
                issues.append("subject %s must resolve as a globally typed orthing identity" % subject_id)
    for contract in activation_contract_rows:
        claimant_id = contract.get("claimant_id")
        claimant_ids = (
            {claimant_id} if isinstance(claimant_id, str) else set()
        ) | _string_set(contract.get("fallback_claimants"))
        if any(_string_lookup(identity_kind_by_id, claimant_id) != "claimant"
               for claimant_id in claimant_ids if isinstance(claimant_id, str)):
            issues.append(
                "activation contract %s claimant and fallbacks must resolve as typed claimant identities"
                % contract.get("contract_id")
            )
    delta_rows = _objects(document, "material_deltas", issues, "records")
    delta_by_id = _unique_index(delta_rows, "material_delta_id", "material delta registry", issues)
    event_by_id = _unique_index(events, "event_id", "orthing events", issues)

    event_groups = defaultdict(list)
    route_events_by_occurrence = defaultdict(list)
    for document_index, event in enumerate(events):
        event_id = event.get("event_id")
        lifecycle = _string_lookup(
            lifecycle_by_occurrence, event.get("occurrence_id")
        )
        if (lifecycle is None
                or any(event.get(field) != lifecycle.get(field) for field in (
                    "session_id", "episode_id", "occurrence_id", "orthing_id"
                ))):
            issues.append(
                "event %s must preserve its immutable lifecycle association"
                % event_id
            )
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
        claimant_id = event.get("claimant_id")
        if claimant_id is not None and _string_lookup(identity_kind_by_id, claimant_id) != "claimant":
            issues.append(
                "event %s claimant_id must resolve through the global typed identity registry"
                % event_id
            )
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
                not event.get("claim_attempt_id") or not event.get("orthability_assessment_id")
                or not event.get("claimant_id")):
            issues.append("event %s orthability assessment requires claimant identities" % event_id)
        event_type = event.get("event_type")
        if isinstance(event_type, str) and event_type in {
                "orthability_assessed", "route_selected", "placement_committed"}:
            occurrence_id = event.get("occurrence_id")
            selected_pair = _string_lookup(selected_route_pairs, occurrence_id)
            selected_claimant = _string_lookup(selected_route_claimants, occurrence_id)
            event_pair = (event.get("claim_attempt_id"), event.get("orthability_assessment_id"))
            if event_type == "orthability_assessed":
                expected_claimant = route_assessments_by_occurrence.get(
                    occurrence_id, {}
                ).get(event_pair)
                mismatch = expected_claimant is None or event.get("claimant_id") != expected_claimant
            else:
                mismatch = (selected_pair is None or event_pair != selected_pair
                            or event.get("claimant_id") != selected_claimant)
            if mismatch:
                issues.append(
                    "event %s assessment, route, and placement binding must match the exact selected claimant pair"
                    % event_id
                )
        if event.get("event_type") == "route_selected":
            selected_pair = _string_lookup(selected_route_pairs, event.get("occurrence_id"))
            event_pair = (event.get("claim_attempt_id"), event.get("orthability_assessment_id"))
            if selected_pair is None or event_pair != selected_pair:
                issues.append("event %s selected route must match the applicable claimant-routing record" % event_id)
            if isinstance(event.get("occurrence_id"), str):
                route_events_by_occurrence[event.get("occurrence_id")].append(event)
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
                event_type = row.get("event_type")
                if isinstance(event_type, str):
                    event_positions[event_type].append(position)
            if event_positions["route_selected"]:
                if (not event_positions["orthability_assessed"]
                        or min(event_positions["orthability_assessed"]) >= min(event_positions["route_selected"])):
                    issues.append("live orthing lifecycle %s must preserve capture then assessment then route order" % (group,))
            if event_positions["placement_committed"]:
                if (not event_positions["orthability_assessed"]
                        or not event_positions["route_selected"]
                        or min(event_positions["orthability_assessed"]) >= min(event_positions["route_selected"])
                        or min(event_positions["route_selected"]) >= min(event_positions["placement_committed"])):
                    issues.append(
                        "live orthing lifecycle %s must preserve capture, claimant assessment, route, then placement"
                        % (group,)
                    )
    for occurrence_id, selected_pair in selected_route_pairs.items():
        route_events = route_events_by_occurrence.get(occurrence_id, [])
        matching = [
            event for event in route_events
            if (event.get("claim_attempt_id"), event.get("orthability_assessment_id"))
            == selected_pair
        ]
        if len(route_events) != 1 or len(matching) != 1:
            issues.append(
                "selected claimant route %s requires exactly one matching route_selected event"
                % occurrence_id
            )
    if not live_lifecycle_seen:
        issues.append("records require an incremental capture-before-claimant-assessment lifecycle")

    run_by_id = _unique_index(runs, "somnus_run_id", "somnus runs", issues)
    corpus_rows = _objects(
        document, "reference_corpus_records", issues, "records"
    )
    corpus_by_revision = _unique_index(
        corpus_rows, "reference_corpus_revision", "reference corpus registry", issues
    )
    for corpus_revision, corpus in corpus_by_revision.items():
        if (corpus.get("owner_ref") != EXPECTED_REFERENCE_CORPUS_OWNER
                or corpus.get("immutable") is not True):
            issues.append(
                "reference corpus revision %s must resolve to the immutable Decision 0035 corpus owner"
                % corpus_revision
            )
    assessment_by_id = _unique_index(assessments, "assessment_id", "somnic assessments", issues)
    somnic_episode_by_id = _unique_index(
        somnic_episodes, "somnic_episode_id", "somnic episode registry", issues
    )
    inter_somnic_relation_by_id = _unique_index(
        inter_somnic_relations, "inter_somnic_relation_id",
        "inter-somnic relation registry", issues,
    )
    somnic_activity_rows = [
        activity
        for episode in somnic_episodes
        for activity in (
            episode.get("activity_events")
            if isinstance(episode.get("activity_events"), list) else []
        )
        if isinstance(activity, dict)
    ]
    somnic_activity_by_id = _unique_index(
        somnic_activity_rows, "activity_id", "somnic activity registry", issues
    )
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
    authorization_rule_rows = _objects(
        document, "authorization_rule_records", issues, "records"
    )
    authorization_rule_by_ref = _unique_index(
        authorization_rule_rows,
        "authorization_rule_ref",
        "authorization rule registry",
        issues,
    )
    if authorization_rule_by_ref != EXPECTED_AUTHORIZATION_RULES:
        issues.append(
            "authorization rule registry must equal the immutable typed Decision 0035 owner"
        )
    application_rows = _objects(document, "applications", issues, "records")
    application_by_id = _unique_index(application_rows, "application_id", "applications", issues)
    revert_provenance_rows = _objects(
        document, "revert_provenance_records", issues, "records"
    )
    revert_provenance_by_ref = _unique_index(
        revert_provenance_rows,
        "revert_provenance_ref",
        "revert provenance registry",
        issues,
    )
    revert_transition_rows = [
        row["revert_transition"] for row in application_rows
        if isinstance(row.get("revert_transition"), dict)
    ]
    revert_transition_by_id = _unique_index(
        revert_transition_rows,
        "revert_transition_id",
        "revert transition registry",
        issues,
    )
    successor_rows = _objects(document, "successor_states", issues, "records")
    successor_by_id = _unique_index(successor_rows, "successor_state_id", "successor states", issues)
    outcome_rows = _objects(document, "outcome_evaluations", issues, "records")
    outcome_by_id = _unique_index(outcome_rows, "outcome_evaluation_id", "outcome evaluations", issues)

    # Decision 0036 additive owners: the run is an orchestration envelope,
    # the episode is the semantic unit, and an assessment is a placement made
    # inside exactly one episode.  Recompute every classification from those
    # owners instead of trusting the fixture's declarative labels.
    episodes_by_run = defaultdict(set)
    assessments_by_episode = defaultdict(set)
    for episode_id, episode in somnic_episode_by_id.items():
        run_id = episode.get("somnus_run_id")
        if not _string_member(run_by_id, run_id):
            issues.append("somnic episode %s has unresolved somnus run" % episode_id)
        else:
            episodes_by_run[run_id].add(episode_id)
        if _string_lookup(identity_kind_by_id, episode.get("operator_id")) != "actor":
            issues.append("somnic episode %s operator must resolve as a typed actor" % episode_id)
        ledger_owner = _string_lookup(provenance_by_id, episode.get("ledger_id"))
        if ledger_owner is None or ledger_owner.get("immutable") is not True:
            issues.append(
                "somnic episode %s ledger must resolve through an immutable provenance owner"
                % episode_id
            )
        activity_ids = set()
        for activity in episode.get("activity_events", []):
            if not isinstance(activity, dict):
                continue
            activity_id = activity.get("activity_id")
            if isinstance(activity_id, str):
                activity_ids.add(activity_id)
            if (activity.get("somnic_episode_id") != episode_id
                    or activity.get("activity_scope") != "intra-somnic"):
                issues.append(
                    "somnic episode %s activity must remain intra-somnic to exactly that episode"
                    % episode_id
                )
        if len(activity_ids) != len(episode.get("activity_events", [])):
            issues.append("somnic episode %s has duplicate activity identity" % episode_id)
        if episode.get("source_state_mutated") is not False:
            issues.append("somnic episode %s cannot mutate a source episode" % episode_id)
        if episode.get("disposition") == "open":
            if episode.get("disposed_at") is not None:
                issues.append("open somnic episode %s cannot have a disposition time" % episode_id)
        elif episode.get("disposed_at") is None:
            issues.append("disposed somnic episode %s requires an explicit disposition time" % episode_id)
        if (episode_id == "SEP-R7E-RECONSTRUCTION"
                or "R7E" in _string_set(episode.get("subject_ids"))):
            if episode.get("telemetry_status") != "reconstructed-analogue-not-live":
                issues.append("R7E reconstruction cannot claim live telemetry")

    for run_id, run in run_by_id.items():
        declared_episode_ids = _string_set(run.get("somnic_episode_ids"))
        if declared_episode_ids != episodes_by_run.get(run_id, set()):
            issues.append(
                "somnus run %s episode membership must exactly match child episode owners"
                % run_id
            )
        if run.get("children_auto_completed") is not False:
            issues.append("run completion cannot auto-complete child episodes")
        if run.get("run_disposition") == "completed":
            undisposed = [
                episode_id for episode_id in declared_episode_ids
                if _string_lookup(somnic_episode_by_id, episode_id) is None
                or somnic_episode_by_id[episode_id].get("disposition") not in {
                    "closed", "partial", "held", "abandoned"
                }
            ]
            if undisposed:
                issues.append(
                    "completed somnus run %s has child episodes without explicit dispositions"
                    % run_id
                )

    for assessment_id, assessment in assessment_by_id.items():
        episode_id = assessment.get("somnic_episode_id")
        run_id = assessment.get("somnus_run_id")
        if episode_id == run_id:
            issues.append("episode identity must remain distinct from run identity")
        episode = _string_lookup(somnic_episode_by_id, episode_id)
        if episode is None:
            issues.append("somnic assessment %s has unresolved somnic episode" % assessment_id)
        else:
            assessments_by_episode[episode_id].add(assessment_id)
            if episode.get("somnus_run_id") != run_id:
                issues.append(
                    "somnic assessment %s run and episode ownership must agree"
                    % assessment_id
                )
        if assessment.get("auto_requeue") is not False:
            issues.append("somnic assessment %s cannot auto-requeue" % assessment_id)
        depth = assessment.get("assessment_depth")
        priors = _string_set(assessment.get("prior_assessment_ids"))
        prior_depths = [
            prior.get("assessment_depth")
            for prior_id in priors
            if (prior := _string_lookup(assessment_by_id, prior_id)) is not None
            and isinstance(prior.get("assessment_depth"), int)
        ]
        if ((priors and (len(prior_depths) != len(priors)
                         or depth != max(prior_depths) + 1))
                or (not priors and depth != 0)):
            issues.append(
                "somnic assessment %s depth must be derived from its assessment lineage"
                % assessment_id
            )
        if (assessment.get("closure_status") == "closed"
                and not priors
                and _string_set(assessment.get("frontier_trigger_ids"))):
            issues.append(
                "closed assessment %s cannot re-enter a frontier without a later trigger"
                % assessment_id
            )
    for episode_id, episode in somnic_episode_by_id.items():
        if _string_set(episode.get("assessment_ids")) != assessments_by_episode.get(
                episode_id, set()):
            issues.append(
                "somnic episode %s assessment membership must be exact and reciprocal"
                % episode_id
            )

    relation_identity_owners = {}
    relation_idempotency_owners = {}
    reopen_graph = defaultdict(set)
    relations_by_assessment = defaultdict(set)
    collective_sources_by_target = defaultdict(set)
    for relation_id, relation in inter_somnic_relation_by_id.items():
        source_id = relation.get("source_episode_id")
        target_id = relation.get("target_episode_id")
        asserting_id = relation.get("asserting_episode_id")
        source = _string_lookup(somnic_episode_by_id, source_id)
        target = _string_lookup(somnic_episode_by_id, target_id)
        if source_id == target_id:
            issues.append(
                "inter-somnic relation %s requires distinct source and target episodes"
                % relation_id
            )
        if source is None or target is None:
            issues.append("inter-somnic relation %s has unresolved episode identity" % relation_id)
            continue
        if asserting_id != target_id:
            issues.append(
                "inter-somnic relation %s must be asserted by its identified target episode"
                % relation_id
            )
        actual_run_relation = (
            "same-run" if source.get("somnus_run_id") == target.get("somnus_run_id")
            else "cross-run"
        )
        actual_operator_relation = (
            "same-operator" if source.get("operator_id") == target.get("operator_id")
            else "cross-operator"
        )
        if relation.get("run_relation") != actual_run_relation:
            issues.append("inter-somnic relation %s run relation is not derived from episode owners" % relation_id)
        if relation.get("operator_relation") != actual_operator_relation:
            issues.append("inter-somnic relation %s operator relation is not derived from episode owners" % relation_id)
        provenance = _mapping(
            relation.get("provenance"), "inter-somnic relation %s provenance" % relation_id,
            issues,
        )
        if (provenance.get("source_operator_id") != source.get("operator_id")
                or provenance.get("source_ledger_id") != source.get("ledger_id")
                or provenance.get("target_operator_id") != target.get("operator_id")
                or provenance.get("target_ledger_id") != target.get("ledger_id")):
            issues.append(
                "inter-somnic relation %s provenance must resolve exact episode operators and ledgers"
                % relation_id
            )
        for assessment_role in ("source_assessment_ids", "target_assessment_ids"):
            expected_episode = source_id if assessment_role.startswith("source") else target_id
            for assessment_id in _string_set(relation.get(assessment_role)):
                assessment = _string_lookup(assessment_by_id, assessment_id)
                if assessment is None or assessment.get("somnic_episode_id") != expected_episode:
                    issues.append(
                        "inter-somnic relation %s %s must resolve within its episode"
                        % (relation_id, assessment_role)
                    )
                else:
                    relations_by_assessment[assessment_id].add(relation_id)
        if relation.get("source_episode_state_preserved") is not True or relation.get(
                "source_assessment_state_preserved") is not True:
            issues.append(
                "inter-somnic relation %s must preserve source episode and assessment state"
                % relation_id
            )
        if relation.get("inherited_properties") != []:
            issues.append("inter-somnic relation %s cannot inherit source properties" % relation_id)
        expected_non_claims = {
            "does-not-transfer-applicability", "does-not-transfer-closure",
            "does-not-transfer-confidence", "does-not-transfer-authority",
            "does-not-transfer-evidence-time",
        }
        if _string_set(relation.get("non_claims")) != expected_non_claims:
            issues.append(
                "inter-somnic relation %s must preserve every authority non-inheritance boundary"
                % relation_id
            )
        if _string_set(relation.get("received_at_t2_evidence_ids")) & (
                _string_set(relation.get("source_t1_evidence_ids"))
                | _string_set(relation.get("target_t1_evidence_ids"))):
            issues.append("received t2 evidence cannot become target t1 evidence")
        received_t2_ids = _string_set(relation.get("received_at_t2_evidence_ids"))
        source_t1_ids = _string_set(relation.get("source_t1_evidence_ids"))
        target_t1_ids = _string_set(relation.get("target_t1_evidence_ids"))
        t1_timings = {"observed_at_t1", "used_at_t1", "indexed_unused_at_t1"}
        if (any(evidence_timing.get(evidence_id) != "discovered_after_t1"
                for evidence_id in received_t2_ids)
                or any(evidence_timing.get(evidence_id) not in t1_timings
                       for evidence_id in source_t1_ids | target_t1_ids)):
            issues.append(
                "relation evidence IDs must resolve through their exact timing owners"
            )
        semantic_relation = relation.get("semantic_relation")
        if semantic_relation != "reopens" and relation.get("reopens_source") is not False:
            issues.append("only a reopening relation can reopen its source")
        if semantic_relation == "compares-with":
            if relation.get("reopens_source") is not False or relation.get("material_delta_id") is not None:
                issues.append("comparison cannot reopen its source")
        elif semantic_relation == "reopens":
            reopen_graph[source_id].add(target_id)
            delta_id = relation.get("material_delta_id")
            source_assessment_ids = _string_set(relation.get("source_assessment_ids"))
            target_assessment_ids = _string_set(relation.get("target_assessment_ids"))
            target_lineage = set().union(*(
                _string_set(assessment_by_id[assessment_id].get("prior_assessment_ids"))
                for assessment_id in target_assessment_ids
                if assessment_id in assessment_by_id
            )) if target_assessment_ids else set()
            target_triggers = set().union(*(
                _string_set(assessment_by_id[assessment_id].get("frontier_trigger_ids"))
                for assessment_id in target_assessment_ids
                if assessment_id in assessment_by_id
            )) if target_assessment_ids else set()
            if (relation.get("reopens_source") is not True
                    or not _string_member(delta_by_id, delta_id)
                    or not source_assessment_ids
                    or not target_assessment_ids
                    or not source_assessment_ids.issubset(target_lineage)
                    or delta_id not in target_triggers):
                issues.append(
                    "reopening requires a new episode, material delta, and assessment lineage"
                )
        elif semantic_relation == "reassesses":
            source_assessment_ids = _string_set(relation.get("source_assessment_ids"))
            target_assessment_ids = _string_set(relation.get("target_assessment_ids"))
            target_predecessors = set().union(*(
                _string_set(assessment_by_id[assessment_id].get("prior_assessment_ids"))
                for assessment_id in target_assessment_ids
                if assessment_id in assessment_by_id
            )) if target_assessment_ids else set()
            target_depths = {
                assessment_by_id[assessment_id].get("assessment_depth")
                for assessment_id in target_assessment_ids
                if assessment_id in assessment_by_id
            }
            if (not source_assessment_ids
                    or not target_assessment_ids
                    or source_assessment_ids != target_predecessors
                    or target_depths != {relation.get("assessment_depth")}
                    or relation.get("auto_requeue") is not False):
                issues.append(
                    "reassessment must match target assessment lineage and depth"
                )
        if relation.get("information_path") == "direct-transclusion":
            local_meta = _string_lookup(
                meta_by_id, provenance.get("local_meta_orthability_assessment_id")
            )
            artifact_ref = provenance.get("received_artifact_ref")
            artifact = _string_lookup(subject_by_id, artifact_ref)
            if (relation.get("independence_claim") is not False
                    or provenance.get("received_artifact_ref") is None
                    or provenance.get("receipt_time") is None
                    or local_meta is None):
                issues.append(
                    "direct transclusion requires receipt provenance and local assessment without independence"
                )
            if (artifact is None
                    or artifact.get("subject_kind") != "transcluded_artifact"
                    or not _string_set(provenance.get("redactions"))
                    or _string_set(provenance.get("redactions"))
                    != _string_set(artifact.get("recorded_redactions"))):
                issues.append("transclusion must preserve its recorded redactions")
            if (local_meta is None
                    or local_meta.get("subject_kind") != "transcluded_artifact"
                    or _string_set(local_meta.get("subject_ids")) != {artifact_ref}
                    or _string_set(local_meta.get("receiving_somnic_episode_ids"))
                    != {target_id}):
                issues.append(
                    "local meta-orthability assessment must be bound to the receiving case"
                )
        elif relation.get("information_path") == "none-independent-discovery":
            if (provenance.get("received_artifact_ref") is not None
                    or provenance.get("receipt_time") is not None):
                issues.append(
                    "receipt-bearing relation cannot claim independent discovery"
                )
            if relation.get("independence_claim") is not True:
                issues.append(
                    "independent discovery requires the no-communication information path"
                )
        elif relation.get("independence_claim") is True:
            issues.append("communication-bearing relation cannot claim independence")
        if semantic_relation == "collective-synthesizes":
            collective_sources_by_target[target_id].add(source_id)
        identity_key = _string_tuple_key(
            asserting_id, source_id, target_id, semantic_relation,
            relation.get("information_path"), relation.get("operation_version"),
            relation.get("material_delta_id") or "<no-material-delta>",
        )
        if identity_key is not None:
            prior = relation_identity_owners.get(identity_key)
            if prior is not None and prior != relation_id:
                issues.append("inter-somnic relation semantic identity must be stable and unique")
            else:
                relation_identity_owners[identity_key] = relation_id
        idempotency_key = relation.get("idempotency_key")
        if isinstance(idempotency_key, str):
            prior = relation_idempotency_owners.get(idempotency_key)
            if prior is not None and prior != relation_id:
                issues.append("inter-somnic relation idempotency collision emits a duplicate")
            else:
                relation_idempotency_owners[idempotency_key] = relation_id

    for assessment_id, assessment in assessment_by_id.items():
        if _string_set(assessment.get("inter_somnic_relation_ids")) != relations_by_assessment.get(
                assessment_id, set()):
            issues.append(
                "somnic assessment %s inter-somnic relation membership must be exact and reciprocal"
                % assessment_id
            )
    for episode_id, episode in somnic_episode_by_id.items():
        collective = episode.get("collective_context")
        if not isinstance(collective, dict):
            continue
        source_ids = _string_set(collective.get("source_episode_ids"))
        if source_ids != collective_sources_by_target.get(episode_id, set()):
            issues.append(
                "collective episode %s source edges must be exact and inter-somnic"
                % episode_id
            )
        if (collective.get("dissent_preserved") is not True
                or any(
                    _string_lookup(somnic_episode_by_id, source_id) is None
                    or somnic_episode_by_id[source_id].get("disposition") != "closed"
                    for source_id in source_ids
                )):
            issues.append(
                "collective episode %s must preserve dissent and source episode closure"
                % episode_id
            )

    for start in list(reopen_graph):
        stack = [(start, set())]
        while stack:
            current, path = stack.pop()
            if current in path:
                issues.append("reopening relation graph must be acyclic")
                break
            stack.extend(
                (next_id, path | {current})
                for next_id in reopen_graph.get(current, set())
            )

    for revert_ref, revert_provenance in revert_provenance_by_ref.items():
        application = _string_lookup(
            application_by_id, revert_provenance.get("application_id")
        )
        authorization = _string_lookup(
            auth_by_id, revert_provenance.get("authorization_id")
        )
        source_revision = revert_provenance.get("source_revision")
        if (application is None
                or authorization is None
                or not isinstance(source_revision, str)
                or not source_revision.strip()
                or revert_provenance.get("immutable") is not True):
            issues.append(
                "revert provenance %s must resolve its application, authorization, source revision, and immutable owner"
                % revert_ref
            )
            continue
        if (application.get("authorization_id") != revert_provenance.get("authorization_id")
                or authorization.get("proposal_id") != application.get("proposal_id")
                or authorization.get("decision") != "authorized"):
            issues.append(
                "revert provenance %s must resolve the exact authorized application chain"
                % revert_ref
            )
            continue
        successor = _string_lookup(
            successor_by_id, application.get("successor_state_id")
        )
        if (application.get("status") not in {"applied", "reverted"}
                or successor is None
                or successor.get("status") != "materialized"
                or successor.get("application_id") != application.get("application_id")
                or successor.get("proposal_id") != application.get("proposal_id")):
            issues.append(
                "revert provenance %s must be owned by a materialized revert-capable application"
                % revert_ref
            )

    governed_sources_by_role = defaultdict(set)
    for run in runs:
        for owner in run.get("governing_input_owners", []):
            if (isinstance(owner, dict)
                    and isinstance(owner.get("owner_role"), str)
                    and isinstance(owner.get("source_ref"), str)):
                governed_sources_by_role[owner["owner_role"]].add(owner["source_ref"])
    for delta_id, delta in delta_by_id.items():
        expected_role = _string_lookup(DELTA_OWNER_ROLES, delta.get("delta_kind"))
        if (expected_role is None or delta.get("owner_role") != expected_role
                or delta.get("source_ref") not in governed_sources_by_role.get(
                    expected_role, set()
                )):
            issues.append(
                "material delta %s must resolve its kind, owner, and governed source"
                % delta_id
            )

    global_typed_registries = [
        ("lifecycle_identity", identity_by_id),
        ("capture_provenance", provenance_by_id),
        ("evidence", evidence_by_id),
        ("source_record", source_record_by_id),
        ("orthing_event", event_by_id),
        ("material_delta", delta_by_id),
        ("somnus_run", run_by_id),
        ("somnic_episode", somnic_episode_by_id),
        ("somnic_activity", somnic_activity_by_id),
        ("reference_corpus_revision", corpus_by_revision),
        ("somnic_assessment", assessment_by_id),
        ("inter_somnic_relation", inter_somnic_relation_by_id),
        ("meta_orthability_assessment", meta_by_id),
        ("recurrence_report", report_by_id),
        ("proposal", proposal_by_id),
        ("authorization", auth_by_id),
        ("application", application_by_id),
        ("revert_provenance", revert_provenance_by_ref),
        ("revert_transition", revert_transition_by_id),
        ("successor", successor_by_id),
        ("outcome", outcome_by_id),
    ]

    resolved_source_by_subject = {}
    for subject_id, subject in subject_by_id.items():
        source_ref = subject.get("source_record_ref")
        source = _string_lookup(source_record_by_id, source_ref)
        source_subject_id = source.get("subject_id") if source is not None else None
        source_time = source.get("occurred_at") if source is not None else None
        if source is None:
            event_source = _string_lookup(event_by_id, source_ref)
            if event_source is not None:
                source = event_source
                source_subject_id = event_source.get("orthing_id")
                source_time = event_source.get("occurred_at")
            else:
                assessment_source = _string_lookup(assessment_by_id, source_ref)
                if assessment_source is not None:
                    source = assessment_source
                    source_subject_id = assessment_source.get("assessment_id")
                    source_time = _mapping(
                        assessment_source.get("t2_configuration"),
                        "source assessment %s t2_configuration" % source_ref, issues,
                    ).get("assessed_at")
                else:
                    relation_source = _string_lookup(
                        inter_somnic_relation_by_id, source_ref
                    )
                    if relation_source is not None:
                        source = relation_source
                        relation_provenance = _mapping(
                            relation_source.get("provenance"),
                            "source relation %s provenance" % source_ref,
                            issues,
                        )
                        source_subject_id = relation_provenance.get(
                            "received_artifact_ref"
                        )
                        source_time = relation_provenance.get("receipt_time")
        if source is None or source_subject_id != subject_id or source_time != subject.get("t1_at"):
            issues.append(
                "subject %s source_record_ref must resolve to its exact authoritative source and t1"
                % subject_id
            )
        else:
            resolved_source_by_subject[subject_id] = source

    history_document = _mapping(history, "history checkpoints", issues)
    history_chain = _mapping(
        history_document.get("chain"), "history checkpoints.chain", issues
    )
    if history_chain != EXPECTED_HISTORY_CHAIN:
        issues.append(
            "history checkpoint chain identity, version, authority, and immutability are fixed"
        )
    history_checkpoint_rows = _objects(
        history_document, "checkpoints", issues, "history checkpoints"
    )
    history_checkpoint_by_id = _unique_index(
        history_checkpoint_rows, "checkpoint_id", "history checkpoints", issues
    )
    checkpoint_time_by_id = {}
    checkpoint_subject_by_id = {}
    checkpoints_by_subject = defaultdict(list)
    chain_projection = {
        "chain_id": history_chain.get("chain_id"),
        "chain_version": history_chain.get("chain_version"),
        "digest_algorithm": history_chain.get("digest_algorithm"),
    }
    for checkpoint_id, checkpoint in history_checkpoint_by_id.items():
        subject_id = checkpoint.get("subject_id")
        captured_through = _parse_time(
            checkpoint.get("captured_through"),
            "history checkpoint %s captured_through" % checkpoint_id, issues,
        )
        if captured_through is not None:
            checkpoint_time_by_id[checkpoint_id] = captured_through
        if isinstance(subject_id, str):
            checkpoint_subject_by_id[checkpoint_id] = subject_id
            checkpoints_by_subject[subject_id].append(checkpoint)
        subject = _string_lookup(subject_by_id, subject_id)
        source = _string_lookup(resolved_source_by_subject, subject_id)
        if subject is None or source is None:
            issues.append(
                "history checkpoint %s must resolve an authoritative subject and source"
                % checkpoint_id
            )
        subject_t1 = _parse_time(
            subject.get("t1_at") if subject is not None else None,
            "history checkpoint %s subject t1" % checkpoint_id,
            issues,
        )
        if captured_through and subject_t1 and captured_through < subject_t1:
            issues.append(
                "history checkpoint %s cannot predate its authoritative subject t1"
                % checkpoint_id
            )
        eligible_events = []
        for event in events:
            if event.get("orthing_id") != subject_id:
                continue
            occurred_at = _parse_time(
                event.get("occurred_at"),
                "history checkpoint %s event %s occurred_at"
                % (checkpoint_id, event.get("event_id")), issues,
            )
            if captured_through is not None and occurred_at is not None and occurred_at <= captured_through:
                eligible_events.append(event)
        eligible_events = sorted(
            eligible_events,
            key=lambda event: (
                event.get("sequence") if isinstance(event.get("sequence"), int) else 0,
                event.get("event_id") if isinstance(event.get("event_id"), str) else "",
            ),
        )
        expected_event_ids = {
            event.get("event_id") for event in eligible_events
            if isinstance(event.get("event_id"), str)
        }
        if _string_set(checkpoint.get("event_ids")) != expected_event_ids:
            issues.append(
                "history checkpoint %s must own the exact target events through its cutoff"
                % checkpoint_id
            )
        payload = {
            "chain": chain_projection,
            "subject": subject,
            "source_record": source,
            "event_history": eligible_events,
            "captured_through": checkpoint.get("captured_through"),
            "predecessor_checkpoint_digest": checkpoint.get(
                "predecessor_checkpoint_digest"
            ),
        }
        canonical = json.dumps(
            payload, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        expected_digest = hashlib.sha256(canonical).hexdigest()
        if checkpoint.get("checkpoint_digest") != expected_digest:
            issues.append(
                "history checkpoint %s digest must bind its authoritative subject, source, event cutoff, and predecessor"
                % checkpoint_id
            )

    for subject_id, checkpoints in checkpoints_by_subject.items():
        ordered = sorted(
            checkpoints,
            key=lambda checkpoint: (
                checkpoint_time_by_id.get(checkpoint.get("checkpoint_id"), datetime.min.replace(tzinfo=timezone.utc)),
                checkpoint.get("checkpoint_id") if isinstance(checkpoint.get("checkpoint_id"), str) else "",
            ),
        )
        predecessor = None
        prior_time = None
        for checkpoint in ordered:
            checkpoint_id = checkpoint.get("checkpoint_id")
            checkpoint_time = checkpoint_time_by_id.get(checkpoint_id)
            if prior_time is not None and checkpoint_time is not None and checkpoint_time <= prior_time:
                issues.append(
                    "history checkpoint chain for %s must advance strictly in time"
                    % subject_id
                )
            if checkpoint.get("predecessor_checkpoint_digest") != predecessor:
                issues.append(
                    "history checkpoint %s must extend the prior immutable checkpoint digest"
                    % checkpoint_id
                )
            predecessor = checkpoint.get("checkpoint_digest")
            prior_time = checkpoint_time

    for contract in activation_contract_rows:
        authorship = contract.get("authorship")
        if not isinstance(authorship, dict) or authorship.get("mode") != "normal":
            continue
        orthing_id = authorship.get("orthing_id")
        contract_ref = "%s@%s" % (
            contract.get("contract_id"), contract.get("contract_version")
        )
        matches = [
            row for row in contract_authoring_by_id.values()
            if row.get("orthing_id") == orthing_id
            and row.get("contract_id") == contract.get("contract_id")
            and row.get("contract_version") == contract.get("contract_version")
        ]
        authoring_time = matches[0].get("authored_at") if len(matches) == 1 else None
        event_matches = [
            event for event in events
            if event.get("orthing_id") == orthing_id
            and event.get("occurred_at") == authoring_time
            and _mapping(
                event.get("governing_versions"),
                "event %s governing_versions" % event.get("event_id"), issues,
            ).get("activation_contract") == contract_ref
        ]
        if (len(matches) != 1
                or _string_lookup(identity_kind_by_id, orthing_id) != "orthing"
                or not _string_member(subject_by_id, orthing_id)
                or matches[0].get("immutable") is not True
                or matches[0].get("fixture_suite") != contract.get("fixture_suite")
                or _string_set(matches[0].get("fixture_ids")) != _string_set(contract.get("fixture_outcomes"))
                or len(event_matches) != 1):
            issues.append(
                "normal activation-contract authorship must resolve one exact typed immutable authoring orthing record"
            )

    for meta in meta_assessments:
        meta_id = meta.get("meta_orthability_assessment_id")
        subject_ids = _string_set(meta.get("subject_ids"))
        if not subject_ids or any(subject_id not in subject_by_id for subject_id in subject_ids):
            issues.append("meta-orthability assessment %s has unresolved or empty subject scope" % meta_id)
        expected_kind = meta.get("subject_kind")
        if any(subject_by_id[subject_id].get("subject_kind") != expected_kind
               for subject_id in subject_ids if subject_id in subject_by_id):
            issues.append("meta-orthability assessment %s subject kind disagrees with its exact subject scope" % meta_id)
        if any(episode_id not in somnic_episode_by_id for episode_id in
               _string_set(meta.get("receiving_somnic_episode_ids"))):
            issues.append(
                "meta-orthability assessment %s has an unresolved receiving episode"
                % meta_id
            )
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
        indicators = _string_set(meta.get("observed_indicators"))
        if not indicators <= _string_set(contract.get("positive_indicators")):
            issues.append(
                "meta-orthability assessment %s indicators must be owned by its exact contract"
                % meta_id
            )
        if not exclusions <= _string_set(contract.get("exclusion_indicators")):
            issues.append(
                "meta-orthability assessment %s exclusions must be owned by its exact contract"
                % meta_id
            )
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
        if (assessment.get("closure_status") == "open"
                and not _string_set(assessment.get("prior_assessment_ids"))):
            issues.append(
                "open assessment %s requires an explicit append-only reopening predecessor"
                % aid
            )
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
                if _string_set(assessment_by_id[prior].get("target_orthing_ids")) != targets:
                    issues.append(
                        "assessment %s prior assessment %s must own the same exact target set"
                        % (aid, prior)
                    )
        if assessment.get("target_history_digest_mode") != "immutable-checkpoint-chain-sha256-v3":
            issues.append(
                "assessment %s target history digest must declare the immutable checkpoint-chain mode"
                % aid
            )
        checkpoint_ids = _string_set(assessment.get("target_history_checkpoint_ids"))
        checkpoints = [
            history_checkpoint_by_id[checkpoint_id]
            for checkpoint_id in checkpoint_ids
            if checkpoint_id in history_checkpoint_by_id
        ]
        checkpoint_subjects = {
            checkpoint.get("subject_id") for checkpoint in checkpoints
            if isinstance(checkpoint.get("subject_id"), str)
        }
        if (len(checkpoints) != len(checkpoint_ids)
                or checkpoint_subjects != targets
                or len(checkpoints) != len(targets)):
            issues.append(
                "assessment %s must resolve one authoritative history checkpoint for each exact target"
                % aid
            )
        checkpoint_payload = []
        for checkpoint in checkpoints:
            checkpoint_id = checkpoint.get("checkpoint_id")
            subject_id = checkpoint.get("subject_id")
            checkpoint_time = checkpoint_time_by_id.get(checkpoint_id)
            if assessed_at is not None and checkpoint_time is not None:
                if checkpoint_time > assessed_at:
                    issues.append(
                        "assessment %s cannot use a history checkpoint after its t2 cutoff"
                        % aid
                    )
                later_target_events = [
                    event for event in events
                    if event.get("orthing_id") == subject_id
                    and (event_time := _parse_time(
                        event.get("occurred_at"),
                        "assessment %s target event %s occurred_at"
                        % (aid, event.get("event_id")), issues,
                    )) is not None
                    and checkpoint_time < event_time <= assessed_at
                ]
                if later_target_events:
                    issues.append(
                        "assessment %s history checkpoint is stale at its t2 cutoff"
                        % aid
                    )
                eligible_for_target = [
                    candidate for candidate in checkpoints_by_subject.get(subject_id, [])
                    if (candidate_time := checkpoint_time_by_id.get(
                        candidate.get("checkpoint_id")
                    )) is not None
                    and candidate_time <= assessed_at
                ]
                if eligible_for_target:
                    latest = max(
                        eligible_for_target,
                        key=lambda candidate: checkpoint_time_by_id[candidate["checkpoint_id"]],
                    )
                    if latest.get("checkpoint_id") != checkpoint_id:
                        issues.append(
                            "assessment %s must select the latest eligible checkpoint for %s"
                            % (aid, subject_id)
                        )
            checkpoint_payload.append({
                "checkpoint_id": checkpoint_id,
                "subject_id": subject_id,
                "captured_through": checkpoint.get("captured_through"),
                "checkpoint_digest": checkpoint.get("checkpoint_digest"),
            })
        checkpoint_payload = sorted(
            checkpoint_payload,
            key=lambda row: (
                row.get("subject_id") if isinstance(row.get("subject_id"), str) else "",
                row.get("checkpoint_id") if isinstance(row.get("checkpoint_id"), str) else "",
            ),
        )
        canonical = json.dumps(
            checkpoint_payload, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        expected_digest = hashlib.sha256(canonical).hexdigest()
        if assessment.get("target_history_digest") != expected_digest:
            issues.append(
                "assessment %s target history digest must derive from its immutable checkpoint owners"
                % aid
            )
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
        if isinstance(disposition, str) and disposition in zero_proposal_dispositions and proposals:
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
        corpus = _string_lookup(
            corpus_by_revision, run.get("reference_corpus_revision")
        )
        if (corpus is None or corpus.get("immutable") is not True):
            issues.append(
                "run %s reference corpus revision requires an immutable owner"
                % rid
            )
        elif corpus.get("owner_ref") != EXPECTED_REFERENCE_CORPUS_OWNER:
            issues.append(
                "run %s reference corpus owner must resolve to the approved Decision 0035 authority"
                % rid
            )
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
        if not reopens <= closed_ids:
            issues.append(
                "run %s may reopen only subjects backed by actually closed assessments"
                % rid
            )
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
        governing_owner_rows = run.get("governing_input_owners")
        if not isinstance(governing_owner_rows, list):
            governing_owner_rows = []
        governing_owners = {
            row.get("owner_role"): row.get("source_ref")
            for row in governing_owner_rows
            if isinstance(row, dict)
            and isinstance(row.get("owner_role"), str)
            and isinstance(row.get("source_ref"), str)
        }
        governing_roles = [
            row.get("owner_role") for row in governing_owner_rows
            if isinstance(row, dict) and isinstance(row.get("owner_role"), str)
        ]
        if (set(governing_roles) != EXPECTED_RUN_OWNER_ROLES
                or len(governing_roles) != len(set(governing_roles))):
            issues.append(
                "run %s requires one exact analysis owner and one operation-contract owner"
                % rid
            )
        if set(governing_owners.values()) != _string_set(run.get("governing_versions")):
            issues.append(
                "run %s governing versions must equal its typed governing-input owners"
                % rid
            )
        for delta_id in deltas:
            delta = _string_lookup(delta_by_id, delta_id)
            if delta is None:
                continue
            recorded_at = _parse_time(
                delta.get("recorded_at"),
                "material delta %s recorded_at" % delta_id, issues,
            )
            delta_source = delta.get("source_ref")
            delta_kind = delta.get("delta_kind")
            owner_role = delta.get("owner_role")
            expected_owner_role = _string_lookup(DELTA_OWNER_ROLES, delta_kind)
            prior_times = [
                assessment_time_by_id.get(prior_id) for prior_id in reopens
                if assessment_time_by_id.get(prior_id) is not None
            ]
            prior_owner_refs = set()
            for prior_id in reopens:
                prior_assessment = _string_lookup(assessment_by_id, prior_id)
                prior_run = _string_lookup(
                    run_by_id,
                    prior_assessment.get("somnus_run_id")
                    if prior_assessment is not None else None,
                )
                if prior_run is not None:
                    for owner in prior_run.get("governing_input_owners", []):
                        if (isinstance(owner, dict)
                                and owner.get("owner_role") == owner_role
                                and isinstance(owner.get("source_ref"), str)):
                            prior_owner_refs.add(owner.get("source_ref"))
            if (started and recorded_at and recorded_at >= started) or (
                    expected_owner_role is None
                    or owner_role != expected_owner_role
                    or not isinstance(delta_source, str)
                    or _string_lookup(governing_owners, owner_role) != delta_source
                    or delta_source in prior_owner_refs
                    or (prior_times and recorded_at is not None
                        and recorded_at <= max(prior_times))
                    or _string_set(delta.get("applies_to_ids")) != reopens):
                issues.append(
                    "run %s material delta %s must strictly predate the run and resolve through its typed governing owner"
                    % (rid, delta_id)
                )
        if _string_set(run.get("used_comparator_ids")) != comparators:
            issues.append(
                "run %s declared comparators must equal its actual comparator-use set"
                % rid
            )
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

    for run in runs:
        rid = run.get("somnus_run_id")
        reopens = _string_set(run.get("reopens_subject_ids"))
        reopened_priors = set()
        for output_id in _string_set(run.get("output_ids")):
            output = _string_lookup(assessment_by_id, output_id)
            if output is not None:
                reopened_priors |= _string_set(output.get("prior_assessment_ids"))
        if reopened_priors != reopens:
            issues.append(
                "run %s reopened subjects must equal the exact prior assessments owned by its outputs"
                % rid
            )

    source_family_rows = _objects(document, "source_family_records", issues, "records")
    source_family_by_id = _unique_index(
        source_family_rows, "source_family_id", "source family registry", issues
    )
    for source_family_id, source_family in source_family_by_id.items():
        provenance = _string_lookup(
            provenance_by_id, source_family.get("provenance_ref")
        )
        if provenance is None or provenance.get("immutable") is not True:
            issues.append(
                "source family %s provenance_ref must resolve to an immutable provenance owner"
                % source_family_id
            )
    for source in source_record_rows:
        if not _string_member(source_family_by_id, source.get("source_family")):
            issues.append(
                "source record %s source_family must resolve through the authoritative source family registry"
                % source.get("source_record_id")
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
    global_typed_registries.extend((
        ("source_family", source_family_by_id),
        ("normalized_input_family", input_family_by_id),
        ("recurrence_support", support_record_by_id),
        ("opportunity", opportunity_by_id),
    ))
    global_id_kinds = defaultdict(list)
    for kind, registry in global_typed_registries:
        for record_id in registry:
            global_id_kinds[record_id].append(kind)
    for record_id, kinds in global_id_kinds.items():
        if len(kinds) != 1:
            issues.append(
                "global typed record ID %s collides across kinds %s"
                % (record_id, sorted(kinds))
            )
    for opportunity_id, opportunity in opportunity_by_id.items():
        if not _string_member(subject_by_id, opportunity.get("subject_id")):
            issues.append("recurrence opportunity %s has unresolved subject provenance" % opportunity_id)
    policy_rows = _objects(document, "independence_policies", issues, "records")
    policy_by_id = _unique_index(policy_rows, "rule_id", "independence policy registry", issues)

    for report in reports:
        report_id = report.get("recurrence_report_id")
        report_run = _string_lookup(run_by_id, report.get("somnus_run_id"))
        if report_run is None:
            issues.append("recurrence report %s has unresolved somnus run" % report_id)
            permitted_support_subjects = set()
        else:
            permitted_support_subjects = (
                _string_set(report_run.get("anchor_subject_ids"))
                | _string_set(report_run.get("historical_comparator_ids"))
            )
        support = report.get("supporting_occurrences") if isinstance(report.get("supporting_occurrences"), list) else []
        support = [row for row in support if isinstance(row, dict)]
        support_subjects = {
            row.get("orthing_id") for row in support
            if isinstance(row.get("orthing_id"), str)
        }
        if report_run is not None:
            declared_comparators = _string_set(
                report_run.get("historical_comparator_ids")
            )
            actual_comparators = support_subjects & declared_comparators
            if actual_comparators != declared_comparators:
                issues.append(
                    "recurrence report %s must use every declared historical comparator"
                    % report_id
                )
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
            orthing_id = row.get("orthing_id")
            if not isinstance(orthing_id, str) or orthing_id not in permitted_support_subjects:
                issues.append(
                    "recurrence report %s support must be drawn from its owning run anchor/comparator inputs"
                    % report_id
                )
            subject = _string_lookup(subject_by_id, orthing_id)
            source = _string_lookup(resolved_source_by_subject, orthing_id)
            authoritative_tuple = (
                subject.get("t1_at") if subject else None,
                source.get("episode_id") if source else None,
                source.get("session_id") if source else None,
                source.get("actor_id") if source else None,
                source.get("source_family") if source else None,
            )
            support_tuple = (
                row.get("occurred_at"), row.get("episode_id"), row.get("session_id"),
                row.get("actor_id"), row.get("source_family"),
            )
            if authoritative_tuple != support_tuple:
                issues.append(
                    "recurrence report %s support must equal its authoritative subject/source time, episode, session, actor, and source-family tuple"
                    % report_id
                )
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
        if any(
                _string_lookup(subject_by_id, ref).get("subject_kind") != "counterexample"
                for ref in counterexamples if _string_lookup(subject_by_id, ref) is not None):
            issues.append(
                "recurrence report %s counterexamples require typed counterexample subjects"
                % report_id
            )
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
        normalized_object = fingerprint.get("normalized_object")
        expected_input_family = (
            {normalized_object} if isinstance(normalized_object, str) else set()
        )
        if support_input_families != expected_input_family:
            issues.append("recurrence fingerprint normalized object must bind exactly to its support input family")
        threshold = report.get("threshold")
        denominator = report.get("opportunity_denominator")
        if (not isinstance(threshold, int) or threshold > len(unique_orthings)
                or threshold > len(unique_episodes)):
            issues.append("recurrence threshold requires distinct orthing and episode support")
        opportunity_ids = _string_set(report.get("opportunity_ids"))
        expected_opportunity_ids = {
            opportunity_id for opportunity_id, opportunity in opportunity_by_id.items()
            if opportunity.get("reference_corpus_revision")
            == (report_run.get("reference_corpus_revision") if report_run else None)
        }
        if opportunity_ids != expected_opportunity_ids:
            issues.append(
                "recurrence report %s must classify the complete pinned corpus opportunity population"
                % report_id
            )
        opportunities = [opportunity_by_id[ref] for ref in opportunity_ids if ref in opportunity_by_id]
        if len(opportunities) != len(opportunity_ids):
            issues.append("recurrence opportunity denominator has unresolved opportunity IDs")
        if not isinstance(denominator, int) or denominator != len(opportunity_ids):
            issues.append("recurrence opportunity denominator must equal its resolvable opportunity-ID set")
        opportunity_subjects = [
            row.get("subject_id") for row in opportunities
            if isinstance(row.get("subject_id"), str)
        ]
        if len(opportunity_subjects) != len(set(opportunity_subjects)):
            issues.append(
                "recurrence opportunity denominator requires one unique classification per subject"
            )
        support_opportunity_subjects = {
            row.get("subject_id") for row in opportunities if row.get("classification") == "support"
        }
        counterexample_opportunity_subjects = {
            row.get("subject_id") for row in opportunities if row.get("classification") == "counterexample"
        }
        if support_opportunity_subjects != unique_orthings or counterexample_opportunity_subjects != counterexamples:
            issues.append("recurrence opportunity records must back the exact support and counterexample subjects")
        if support_opportunity_subjects & counterexample_opportunity_subjects:
            issues.append("recurrence support and counterexample subject classes must be disjoint")
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
            observed_policy = {
                key: policy.get(key) for key in PINNED_INDEPENDENCE_POLICY
            }
            semantic_policy_matches = (
                all(observed_policy.get(key) == PINNED_INDEPENDENCE_POLICY[key]
                    for key in PINNED_INDEPENDENCE_POLICY
                    if key != "required_dimensions")
                and _string_set(observed_policy.get("required_dimensions"))
                == set(PINNED_INDEPENDENCE_POLICY["required_dimensions"])
            )
            observed_digest = _canonical_digest(observed_policy)
            if (not semantic_policy_matches
                    or policy.get("policy_digest") != observed_digest):
                issues.append(
                    "recurrence independence policy must equal the pinned immutable governing policy"
                )
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

    proposal_owners = defaultdict(list)
    for assessment in assessments:
        for proposal_id in _string_set(assessment.get("proposal_ids")):
            proposal_owners[proposal_id].append(assessment.get("assessment_id"))

    for proposal in proposal_rows:
        proposal_id = proposal.get("proposal_id")
        mode = proposal.get("provenance_mode")
        supporting_assessment_id = proposal.get("supporting_assessment_id")
        if mode == "somnus_grounded_proposal":
            if (not _string_member(assessment_by_id, supporting_assessment_id)
                    or proposal_owners.get(proposal_id, []) != [supporting_assessment_id]):
                issues.append(
                    "grounded proposal %s must be owned bidirectionally by exactly its supporting assessment"
                    % proposal_id
                )
        elif mode == "legacy_reflective_proposal" and supporting_assessment_id != "unavailable":
            issues.append("legacy proposal %s cannot launder a somnic assessment owner" % proposal_id)
        action = _mapping(proposal.get("proposed_action"), "proposal %s proposed_action" % proposal_id, issues)
        successor = _string_lookup(successor_by_id, action.get("successor_target_id"))
        owned_successors = [
            row for row in successor_by_id.values()
            if row.get("proposal_id") == proposal_id
        ]
        if successor is None:
            issues.append("proposal %s has unresolved successor target" % proposal_id)
        elif (successor.get("action_label") != action.get("action_label")
                or successor.get("proposal_id") != proposal_id):
            issues.append("proposal %s must own exactly its action-matched successor target" % proposal_id)
        if len(owned_successors) != 1 or (
                owned_successors
                and owned_successors[0].get("successor_state_id")
                != action.get("successor_target_id")):
            issues.append(
                "proposal %s must own one reciprocal successor and no extras"
                % proposal_id
            )
        proposed_at = _parse_time(
            proposal.get("proposed_at"), "proposal %s proposed_at" % proposal_id, issues
        )
        assessed_at = assessment_time_by_id.get(supporting_assessment_id)
        if mode == "somnus_grounded_proposal" and proposed_at and assessed_at and proposed_at <= assessed_at:
            issues.append(
                "grounded proposal %s must be created after its supporting assessment"
                % proposal_id
            )

    for auth in auth_rows:
        rule_ref = auth.get("authorization_rule_ref")
        if not _string_member(authorization_rule_by_ref, rule_ref):
            issues.append(
                "authorization %s must resolve through the immutable typed authorization rule registry"
                % auth.get("authorization_id")
            )
        if not _string_member(proposal_by_id, auth.get("proposal_id")):
            issues.append("authorization %s has unresolved proposal" % auth.get("authorization_id"))
        if auth.get("source") != "independent_governance":
            issues.append("proposal cannot self-authorize; authorization source must be independent governance")
        proposal = _string_lookup(proposal_by_id, auth.get("proposal_id"))
        if proposal is not None:
            if proposal.get("status") != "proposed" and auth.get("decision") == "authorized":
                issues.append(
                    "authorization %s cannot authorize a rejected or withdrawn proposal"
                    % auth.get("authorization_id")
                )
            proposed_at = _parse_time(
                proposal.get("proposed_at"), "proposal %s proposed_at" % proposal.get("proposal_id"), issues
            )
            decided_at = _parse_time(
                auth.get("decided_at"), "authorization %s decided_at" % auth.get("authorization_id"), issues
            )
            if proposed_at and decided_at and proposed_at >= decided_at:
                issues.append("authorization %s must occur after its proposal" % auth.get("authorization_id"))

    authorization_times = defaultdict(list)
    for auth in auth_rows:
        key = _string_tuple_key(auth.get("proposal_id"), auth.get("authorization_rule_ref"))
        decided_at = _parse_time(
            auth.get("decided_at"),
            "authorization %s decided_at" % auth.get("authorization_id"), issues,
        )
        if key is not None and decided_at is not None:
            authorization_times[(key, decided_at)].append(auth.get("authorization_id"))
    for (key, decided_at), authorization_ids in authorization_times.items():
        if len(authorization_ids) > 1:
            issues.append(
                "proposal %s authorization rule %s has a non-total effective order at %s"
                % (key[0], key[1], decided_at.isoformat())
            )

    outcome_application_ids = {
        row.get("application_id") for row in outcome_rows
        if isinstance(row.get("application_id"), str)
    }
    outcomes_by_application = defaultdict(list)
    for outcome in outcome_rows:
        if isinstance(outcome.get("application_id"), str):
            outcomes_by_application[outcome["application_id"]].append(outcome)
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
        elif authorization.get("decision") != "authorized":
            issues.append(
                "application attempt cannot exist under rejected authorization"
            )
        if proposal is not None and proposal.get("status") != "proposed":
            issues.append(
                "application attempt requires a non-rejected active proposal"
            )
        if application.get("status") == "applied":
            outcome_results = {
                outcome.get("result")
                for outcome in outcomes_by_application.get(application_id, [])
                if isinstance(outcome.get("result"), str)
            }
            if (application.get("outcome_evaluation_required") is not True
                    or len(outcomes_by_application.get(application_id, [])) != 1):
                issues.append("applied mutation requires later outcome evaluation")
            if outcome_results & {"ineffective", "harmful"}:
                issues.append(
                    "ineffective or harmful evaluated applications must transition to reverted"
                )
            if not _string_member(successor_by_id, application.get("successor_state_id")):
                issues.append("applied mutation requires a resolvable successor state")
            else:
                successor = successor_by_id[application.get("successor_state_id")]
                if (successor.get("status") != "materialized"
                        or successor.get("application_id") != application_id
                        or successor.get("proposal_id") != application.get("proposal_id")):
                    issues.append(
                        "applied mutation must own exactly one materialized successor for the same proposal"
                    )
                successor_time = _parse_time(
                    successor.get("created_at"),
                    "successor %s created_at" % successor.get("successor_state_id"), issues,
                )
                applied_time = _parse_time(
                    application.get("applied_at"), "application %s applied_at" % application_id, issues
                )
                if successor_time and applied_time and successor_time != applied_time:
                    issues.append("applied mutation and successor state must share the authoritative application time")
        elif application.get("status") == "failed":
            if (application.get("outcome_evaluation_required") is not False
                    or outcomes_by_application.get(application_id)):
                issues.append(
                    "failed application must not claim a required or effective outcome evaluation"
                )
            if application.get("successor_state_id") is not None:
                issues.append("failed mutation cannot claim a successor state")
        elif application.get("status") == "reverted":
            outcomes = outcomes_by_application.get(application_id, [])
            if (application.get("outcome_evaluation_required") is not True
                    or len(outcomes) != 1
                    or outcomes[0].get("result") not in {"ineffective", "harmful"}):
                issues.append(
                    "reverted application requires one ineffective or harmful outcome"
                )
            transition = _mapping(
                application.get("revert_transition"),
                "application %s revert_transition" % application_id,
                issues,
            )
            if (transition.get("application_id") != application_id
                    or transition.get("prior_successor_state_id")
                    != application.get("successor_state_id")
                    or transition.get("immutable") is not True):
                issues.append(
                    "reverted application must own an immutable transition from its materialized successor"
                )
            revert_provenance = _string_lookup(
                revert_provenance_by_ref,
                transition.get("revert_provenance_ref"),
            )
            if (revert_provenance is None
                    or revert_provenance.get("immutable") is not True
                    or revert_provenance.get("application_id") != application_id
                    or revert_provenance.get("authorization_id")
                    != application.get("authorization_id")):
                issues.append(
                    "reverted application must resolve revert provenance through its authorized immutable owner"
                )
            reverted_at = _parse_time(
                transition.get("reverted_at"),
                "application %s revert_transition.reverted_at" % application_id,
                issues,
            )
            applied_at = _parse_time(
                application.get("applied_at"),
                "application %s applied_at" % application_id,
                issues,
            )
            outcome_at = (
                _parse_time(
                    outcomes[0].get("evaluated_at"),
                    "application %s outcome evaluated_at" % application_id,
                    issues,
                )
                if len(outcomes) == 1 else None
            )
            if (reverted_at is not None
                    and ((applied_at is not None and reverted_at <= applied_at)
                         or (outcome_at is not None and reverted_at <= outcome_at))):
                issues.append(
                    "revert transition must occur after application and its harmful or ineffective outcome"
                )
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
            relevant = []
            for candidate in auth_rows:
                if (candidate.get("proposal_id") != application.get("proposal_id")
                        or candidate.get("authorization_rule_ref")
                        != authorization.get("authorization_rule_ref")):
                    continue
                candidate_time = _parse_time(
                    candidate.get("decided_at"),
                    "authorization %s decided_at" % candidate.get("authorization_id"),
                    issues,
                )
                if candidate_time and applied_at and candidate_time < applied_at:
                    relevant.append((candidate_time, candidate))
            effective = max(relevant, key=lambda pair: pair[0])[1] if relevant else None
            if (effective is None
                    or effective.get("authorization_id") != application.get("authorization_id")
                    or effective.get("decision") != "authorized"):
                issues.append(
                    "application %s must cite the latest effective authorization state"
                    % application_id
                )

    for successor_id, successor in successor_by_id.items():
        proposal = _string_lookup(proposal_by_id, successor.get("proposal_id"))
        if proposal is None:
            issues.append("successor %s has unresolved proposal owner" % successor_id)
        application_id = successor.get("application_id")
        successor_time = _parse_time(
            successor.get("created_at"),
            "successor %s created_at" % successor_id, issues,
        )
        proposed_at = _parse_time(
            proposal.get("proposed_at") if proposal is not None else None,
            "successor %s owning proposal time" % successor_id, issues,
        )
        if successor_time and proposed_at and successor_time < proposed_at:
            issues.append(
                "successor %s cannot predate its owning proposal"
                % successor_id
            )
        if successor.get("status") == "materialized":
            application = _string_lookup(application_by_id, application_id)
            if application is None or application.get("successor_state_id") != successor_id:
                issues.append(
                    "materialized successor %s must be owned bidirectionally by one application"
                    % successor_id
                )
        elif application_id is not None:
            issues.append(
                "proposed successor target %s cannot claim an application owner"
                % successor_id
            )

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
    required = {"candidate_id", "semantic_contract_version", "status", "execution", "inputs", "outputs", "dependencies", "event_emissions", "authority_limit", "authority_boundary", "residual_behavior", "downstream_owner", "non_claims", "non_claim_boundaries"}
    expected = {"orthability-check", "orthing-ledger", "episode-residual-live", "residual-recurrence-somnic", "metaorthemma-conflict", "intervention-disposition", "verdict-aware-patch-proposal", "guarded-writeback-actuator", "orthing-dream", "somnus-export", "somnus-import", "metaortheme-transclusion", "collective-somnus", "somnus-council", "transclusion-ledger"}
    candidate_by_id = _unique_index(
        candidates, "candidate_id", "inventory candidates", issues
    )
    if set(candidate_by_id) != expected:
        issues.append("inventory does not contain the exact bounded candidate set")
    for row in candidates:
        if not required <= set(row):
            issues.append("inventory candidate %s lacks its complete outline contract" % row.get("candidate_id"))
        if row.get("status") != "outline-only" or row.get("execution") != "not implemented":
            issues.append("inventory candidate %s must remain outline-only and undeployed" % row.get("candidate_id"))
        for field in ("inputs", "outputs", "dependencies"):
            if not _string_set(row.get(field)):
                issues.append("inventory candidate %s requires nonempty typed %s" % (row.get("candidate_id"), field))
        candidate_id = row.get("candidate_id")
        expected_semantic_digest = _string_lookup(
            EXPECTED_CANDIDATE_SEMANTIC_DIGESTS, candidate_id
        )
        if (row.get("semantic_contract_version") != "1.0.0"
                or expected_semantic_digest is None
                or _candidate_semantic_digest(row) != expected_semantic_digest):
            issues.append(
                "inventory candidate %s must preserve its candidate-specific versioned owner, layer, input, output, and dependency contract"
                % candidate_id
            )
        expected_events = (
            EXPECTED_CANDIDATE_EVENTS.get(candidate_id, set())
            if isinstance(candidate_id, str) else set()
        )
        if _string_set(row.get("event_emissions")) != expected_events:
            issues.append(
                "inventory candidate %s must preserve its exact typed event-emission contract"
                % candidate_id
            )
        non_claims = row.get("non_claims")
        boundaries = row.get("non_claim_boundaries")
        claim_status = document.get("claim_status")
        if (non_claims != STANDARD_CANDIDATE_NON_CLAIMS
                or boundaries != STANDARD_CANDIDATE_NON_CLAIMS
                or not isinstance(claim_status, dict)
                or _mapping(claim_status.get("runtime"), "inventory.claim_status.runtime", issues).get("status") != "not-implemented"):
            issues.append(
                "inventory candidate %s non-claims must equal its structured boundaries and runtime claim-status owner"
                % candidate_id
            )
        authority = _mapping(
            row.get("authority_boundary"),
            "inventory candidate %s authority_boundary" % row.get("candidate_id"), issues,
        )
        if any(authority.get(field) != "prohibited" for field in (
                "automatic_authorization", "automatic_execution",
                "automatic_writeback", "historical_rewrite")):
            issues.append("inventory candidate %s authority boundary must prohibit authorization, execution, writeback, and historical rewrite" % row.get("candidate_id"))
        authority_limit = _mapping(
            row.get("authority_limit"),
            "inventory candidate %s authority_limit" % row.get("candidate_id"), issues,
        )
        if (authority_limit.get("scope") != "bounded record or proposal production only"
                or authority_limit.get("operator_request_authorizes_mutation") is not False
                or _string_set(authority_limit.get("prohibited_operations"))
                != PROHIBITED_CANDIDATE_OPERATIONS):
            issues.append(
                "inventory candidate %s must preserve the exact structured prohibited-operation boundary"
                % row.get("candidate_id")
            )
        if authority.get("scope") != authority_limit.get("scope"):
            issues.append(
                "inventory candidate %s must declare one consistent authority scope"
                % row.get("candidate_id")
            )
        downstream_owner = _mapping(
            row.get("downstream_owner"),
            "inventory candidate %s downstream_owner" % row.get("candidate_id"), issues,
        )
        owner_role = downstream_owner.get("owner_role")
        if (downstream_owner.get("ownership_scope") != "external/downstream"
                or downstream_owner.get("local_runtime_ownership") != "prohibited"
                or not isinstance(owner_role, str)
                or owner_role not in ALLOWED_CANDIDATE_OWNER_ROLES):
            issues.append(
                "inventory candidate %s must bind an approved closed external/downstream owner role"
                % row.get("candidate_id")
            )
        expected_residual = _string_lookup(EXPECTED_CANDIDATE_RESIDUALS, candidate_id)
        if expected_residual is None or row.get("residual_behavior") != expected_residual:
            issues.append(
                "inventory candidate %s must preserve its closed structured residual disposition"
                % row.get("candidate_id")
            )
        if (candidate_id == "guarded-writeback-actuator"
                and _string_set(row.get("outputs"))
                != EXPECTED_GUARDED_ACTUATOR_OUTPUTS):
            issues.append(
                "guarded writeback actuator outputs must remain bounded records, not runtime actions"
            )
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
    if actuator.get("stages") != ORDERED_ACTUATOR_STAGES:
        issues.append("writeback actuator must preserve proposal, review, decision, validation, dry-run, and apply/revert stages")
    source = _mapping(document.get("source_verification"), "adoption.source_verification", issues)
    if (any(source.get(field) != "pending" for field in ("source_code", "license", "commit", "tests"))
            or source.get("implementation_claims") != "externally supplied and not repository-verified"):
        issues.append("Hermes implementation claims must remain pending source verification")
    predecessor = _mapping(
        document.get("predecessor_classification"),
        "adoption.predecessor_classification", issues,
    )
    if (predecessor.get("relative_granularity")
            != EXPECTED_PREDECESSOR_CLASSIFICATION["relative_granularity"]
            or _string_set(predecessor.get("scope"))
            != set(EXPECTED_PREDECESSOR_CLASSIFICATION["scope"])):
        issues.append(
            "Hermes predecessor classification must remain structured, neutral, and source-qualified"
        )
    characterization = document.get("predecessor_characterization")
    if characterization not in ALLOWED_PREDECESSOR_CHARACTERIZATIONS:
        issues.append(
            "Hermes predecessor characterization must use a closed neutral explanation bound to its structured scope"
        )
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
    if _string_set(subsumption.get("governing_targets")) != expected_governing:
        issues.append("writeback adoption profile must preserve the exact bounded governing target vocabulary")
    expected_outcomes = {"no_change", "investigation", "evidence_request", "preserve_residual", "one_proposal", "alternative_proposals"}
    expected_records = {"somnic_assessment", "intervention_disposition", "mutation_proposal", "mutation_authorization", "applied_mutation", "later_outcome_evaluation"}
    expected_times = {"t1_waking_orthing", "t2_somnic_assessment", "t3_proposal_and_authorization", "t4_application_and_successor_state", "t5_outcome_evaluation"}
    if _string_set(subsumption.get("outcomes")) != expected_outcomes:
        issues.append("writeback adoption profile must preserve the exact outcome vocabulary")
    if _string_set(document.get("record_separation")) != expected_records:
        issues.append("writeback adoption profile must preserve the exact record-separation vocabulary")
    if _string_set(document.get("temporal_roles")) != expected_times:
        issues.append("writeback adoption profile must preserve the exact t1-t5 vocabulary")
    expected_non_claims = {
        "source_implementation": "not-verified",
        "empirical_superiority": "not-established",
        "governed_learning": "not-established",
        "runtime_writeback": "not-implemented",
    }
    claim_status = document.get("claim_status")
    if (document.get("non_claims") != expected_non_claims
            or not isinstance(claim_status, dict)
            or _mapping(claim_status.get("runtime"), "adoption.claim_status.runtime", issues).get("status") != "not-implemented"
            or _mapping(claim_status.get("performance"), "adoption.claim_status.performance", issues).get("status") != "not-established"
            or _mapping(claim_status.get("learning"), "adoption.claim_status.learning", issues).get("status") != "not-established"):
        issues.append("writeback adoption non-claims must remain structured and projected from the claim-status owner")
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
            mode_id = row.get("mode_id")
            if not isinstance(mode_id, str) or mode_id not in expected_modes:
                continue
            expected = expected_modes[mode_id]
            observed = (row.get("name"), row.get("information_path"), row.get("coordination"))
            if observed != expected:
                issues.append("collective mode %s must preserve its exact normative contract" % mode_id)
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


def collect_issues(activation, records, history, inventory, adoption, collective,
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
        issues += _records_issues(records, activation, history, schemas, store)
    else:
        issues.append("somnus record fixture document must be an object")
    issues += _inventory_issues(inventory, schemas, store)
    issues += _adoption_issues(adoption, schemas, store)
    issues += _collective_issues(collective, schemas, store)
    decision_issues, claim_status = _decision_issues(decision_text)
    issues += decision_issues
    authority_refs = []
    if isinstance(activation, dict):
        transition_authority = activation.get("version_transition_authority")
        if isinstance(transition_authority, dict):
            authority_refs.append(transition_authority.get("authority_ref"))
    if isinstance(history, dict):
        history_chain = history.get("chain")
        if isinstance(history_chain, dict):
            authority_refs.append(history_chain.get("authority_ref"))
    if isinstance(records, dict):
        authority_refs.extend(
            row.get("owner_ref")
            for row in records.get("reference_corpus_records", [])
            if isinstance(row, dict)
        )
        authority_refs.extend(
            row.get("owner_ref")
            for row in records.get("authorization_rule_records", [])
            if isinstance(row, dict)
        )
    issues += _decision_authority_issues(decision_text, authority_refs)
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
    for path in (
            ACTIVATION_PATH, RECORDS_PATH, HISTORY_PATH, INVENTORY_PATH,
            ADOPTION_PATH, COLLECTIVE_PATH):
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
