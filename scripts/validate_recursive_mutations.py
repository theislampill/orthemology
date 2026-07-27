#!/usr/bin/env python3
"""Recursive, path-aware mutation testing for the R4 semantic contract (R4 7.5).

The R3 engine applied three TOP-LEVEL operators (drop-required, bad-enum,
extra-field). The read-only audit's finding B7 was that "208 mutants, 0
survivors" therefore said much less than it sounded like: nothing nested,
nothing referential, nothing cardinality-bearing, nothing cross-record was ever
mutated.

This engine walks every positive example part RECURSIVELY, resolving the
effective schema at each node (through $ref, allOf and the applicable if/then
and anyOf/oneOf branches) so that it knows, at every path, which fields are
required, which arrays are sets, and which values are references. It then
applies eighteen operator families. A mutant is KILLED if it is rejected at a
declared layer:

  schema   — the hardened JSON Schema rejects the mutated part; or
  semantic — validate_cross_record_semantics.collect_issues flags the mutated
             bundle (the unmutated bundles are all issue-free, so any issue is
             attributable to the mutation).

Everything is deterministic: mutants are enumerated in sorted path order, never
sampled. There is no randomness and no seed.

A SURVIVOR is a mutant both layers accept. Survivors are failures unless they
are declared, with a reason, in tests/schema-mutations/mutation-spec.json under
"justified_equivalents" — i.e. unless the mutation provably does not change what
the record claims. The report always prints every operator family with its own
counts; "N mutants killed" alone is exactly the kind of summary this engine
exists to replace.
"""
import argparse
import copy
import hashlib
import json
import os
import pathlib
import subprocess
import sys

import yaml

try:
    from scripts.task14_probe_registry import load_registry
    from scripts.task14_direct_probes import execute_direct_probe
except ModuleNotFoundError:
    from task14_probe_registry import load_registry
    from task14_direct_probes import execute_direct_probe
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from validate_cross_record_semantics import collect_issues, aggregate  # noqa: E402

FAMILIES = [
    ("1", "delete-nested-required",
     "delete each required field at EVERY depth, not only the top level"),
    ("2", "empty-required-string",
     "blank each required string ('' is not a declaration)"),
    ("3", "empty-required-array-or-map",
     "empty each required array or map that the contract requires to be nonempty"),
    ("4", "duplicate-unique-member",
     "duplicate a member of an array-as-set, and collide two ids that must differ"),
    ("5", "unknown-reference-id",
     "repoint each resolvable reference (claim, token, evidence, episode) at nothing"),
    ("6", "analysis-version-mismatch",
     "desynchronise an analysis version between records that must share it"),
    ("7", "occurrence-version-mismatch",
     "desynchronise an occurrence version between records that must share it"),
    ("8", "delete-disposition-conditional-field",
     "delete the field a residual's own disposition makes mandatory"),
    ("9", "claim-dependency-cycle",
     "make a claim depend on itself, directly or through another claim"),
    ("10", "remove-required-verdict-status",
     "delete the status of a verdict the required path demands"),
    ("11", "contradict-pathway-summary",
     "state a pathway or reasoning-path summary the statuses do not support"),
    ("12", "na-without-reason",
     "strip the reason from a not-applicable status, anywhere in the record"),
    ("13", "plural-metaorthemma-type",
     "give one token several of_type entries (unimplemented many-to-many MetaInst)"),
    ("14", "empty-metaorthemma-binding",
     "empty the binding map (a token with no material binding)"),
    ("15", "postdate-reliability-declaration",
     "declare a RelSpec at or after the result it is used to assess"),
    ("16", "violate-perturbation-invariant",
     "vary a field the PerturbSpec declares invariant"),
    ("17", "collapse-candidate-set-into-partial-profile",
     "collapse a candidate SET of complete profiles into one partial profile (B1)"),
    ("18", "collapse-claim-path-into-episode-path",
     "overwrite a claim's reasoning adequacy with the episode-level pathway state (B2)"),
    ("19", "inheritance-self-or-ghost",
     "make an analysis inherit from itself, or from a parent that resolves nowhere (D1)"),
    ("20", "cross-episode-token-collision",
     "rename an embedded token to another episode's token id (global identity, D3)"),
    ("21", "token-scope-cross-ledger-leak",
     "point a token's claim scope at a claim owned by ANOTHER episode's ledger (D4)"),
    ("22", "ghost-metaortheme-reference",
     "repoint a governing-configuration mu_ref or a token of_type at an undeclared edition (D5)"),
    ("23", "precedence-self-or-cycle",
     "add a precedence self-edge, or close a 2-cycle over declared governing types (D5)"),
    ("24", "mixed-offset-time-reversal",
     "postdate a RelSpec past the outcome using a UTC offset that string-compares earlier, "
     "or make it timezone-naive (D7)"),
    ("25", "invert-token-validity",
     "set a token's expiry before its effective_from (D7)"),
    ("26", "silent-external-reference",
     "strip or unresolve an audit-ready record's external_refs, or desynchronise its "
     "analysis from the bundle (D6)"),
    ("27", "omit-claim-reasoning-verdict",
     "drop one entry from a claim's recorded req_reason projection (omission attack, D8)"),
]

MUTANT_MARK = "MUTANT-NO-SUCH-ID"
TASK14_PLAN = (
    "docs/superpowers/plans/2026-07-21-r7e-sol-independent-repair.md"
)
TASK14_LEDGER = (
    "docs/project-closure/r7e-sol/AR6_TO_TASKS_10_16_IMPACT_LEDGER.yaml"
)
TASK14_REPORT = (
    "docs/project-closure/r7e-sol/R7E-SOL-ADVERSARIAL-REPORT.md"
)
TASK14_PROBE = "scripts/run_task14_probe.py"
TASK14_OBSERVATION_SCHEMA = "orthemology-task14-observation-v1"


def _task14_plan_names(root):
    plan = pathlib.Path(root) / TASK14_PLAN
    prefix = "**Step 1:** Make every mandatory attack durable:"
    lines = plan.read_text(encoding="utf-8").splitlines()
    matching = [line for line in lines if line.startswith(prefix)]
    if len(matching) != 1:
        raise ValueError("authoritative plan must contain one Task 14 Step 1 inventory")
    names = matching[0].split("durable: ", 1)[1].rstrip(".").split("; ")
    names[-1] = names[-1].removeprefix("and ")
    return names


def load_task14_ar6_rows(root):
    ledger_path = pathlib.Path(root) / TASK14_LEDGER
    ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
    entries = ledger.get("entries", []) if isinstance(ledger, dict) else []
    return [
        row for row in entries
        if isinstance(row, dict) and row.get("closest_tracked_task") == "Task 14"
    ]


def load_task14_probe_registry(root):
    """Load the independently digest-anchored 77-variant registry."""
    return load_registry(pathlib.Path(root))


def expected_task14_observation(binding, role, root):
    """Return every identity field a direct observation must match exactly."""
    if role not in {"control", "mutation"}:
        raise ValueError("Task 14 observation role is invalid")
    entry_point = pathlib.Path(root) / binding.validator_entry_point
    return {
        "attack_id": binding.attack_id,
        "variant_id": binding.variant_id,
        "mutation_id": binding.mutation_id,
        "role": role,
        "evidence_selector": getattr(binding, role + "_evidence_selector"),
        "validator_owner": binding.validator_owner,
        "validator_entry_point": binding.validator_entry_point,
        "validator_sha256": hashlib.sha256(entry_point.read_bytes()).hexdigest(),
    }


def task14_observation_id(expected, outcome, input_sha256):
    canonical = json.dumps(
        {
            **expected,
            "observed_validator_outcome": outcome,
            "input_sha256": input_sha256,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def audit_task14_spec(spec, root):
    """Return deterministic issues in the authoritative Task 14 inventory."""
    issues = []
    attacks = spec.get("mandatory_attacks")
    if not isinstance(attacks, list):
        return ["mandatory_attacks must be a list"]
    try:
        plan_names = _task14_plan_names(root)
    except (OSError, ValueError) as exc:
        return [str(exc)]
    observed_names = [
        row.get("name") if isinstance(row, dict) else None for row in attacks
    ]
    if observed_names != plan_names:
        issues.append("plan attack inventory differs from the authoritative Step 1 order")

    try:
        registry = load_task14_probe_registry(root)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return ["Task 14 closed probe registry mismatch: %s" % exc]

    attack_ids = []
    mutation_ids = []
    variant_ids = []
    for index, row in enumerate(attacks, 1):
        expected_id = "R7E-T14-A%02d" % index
        if not isinstance(row, dict):
            issues.append("%s must be an object" % expected_id)
            continue
        attack_id = row.get("attack_id")
        attack_ids.append(attack_id)
        if attack_id != expected_id:
            issues.append("attack %d ID must be %s" % (index, expected_id))
        if "coverage_kind" in row or "coverage" in row or "command" in row:
            issues.append(
                "%s must not use an arbitrary coverage label or shared command"
                % expected_id
            )
        for field in ("invariant", "owner"):
            value = row.get(field)
            if not isinstance(value, str) or not value.strip():
                issues.append("%s has no %s" % (expected_id, field))
        variants = row.get("variants")
        if not isinstance(variants, list) or not variants:
            issues.append("%s has no explicit control/mutation variants" % expected_id)
            continue
        for variant_index, variant in enumerate(variants, 1):
            expected_variant_id = "%s-V%02d" % (expected_id, variant_index)
            expected_mutation_id = "%s-M%02d" % (expected_id, variant_index)
            if not isinstance(variant, dict):
                issues.append("%s variant %d must be an object" % (expected_id, variant_index))
                continue
            variant_id = variant.get("variant_id")
            mutation_id = variant.get("mutation_id")
            variant_ids.append(variant_id)
            mutation_ids.append(mutation_id)
            if variant_id != expected_variant_id or mutation_id != expected_mutation_id:
                issues.append("%s variant command identity mismatch" % expected_id)
            if variant.get("validator_owner") != row.get("owner"):
                issues.append(
                    "%s %s validator owner differs from attack owner"
                    % (expected_id, variant_id)
                )
            binding = registry.get((expected_id, expected_variant_id))
            if binding is None:
                issues.append(
                    "%s %s has no closed probe-registry binding"
                    % (expected_id, expected_variant_id)
                )
            else:
                expected_registry_fields = {
                    "mutation_id": binding.mutation_id,
                    "validator_owner": binding.validator_owner,
                    "validator_entry_point": binding.validator_entry_point,
                    "control_evidence_selector": binding.control_evidence_selector,
                    "mutation_evidence_selector": binding.mutation_evidence_selector,
                }
                for field, expected_value in expected_registry_fields.items():
                    if variant.get(field) != expected_value:
                        issues.append(
                            "%s %s %s differs from the closed probe registry"
                            % (expected_id, expected_variant_id, field)
                        )
                if row.get("owner") != binding.owner:
                    issues.append(
                        "%s owner differs from the closed probe registry" % expected_id
                    )
            for field in (
                "neutral_concept",
                "validator_entry_point",
                "control_evidence_selector",
                "mutation_evidence_selector",
            ):
                value = variant.get(field)
                if not isinstance(value, str) or not value.strip():
                    issues.append("%s %s has no %s" % (expected_id, variant_id, field))
            if (
                variant.get("control_evidence_selector")
                == variant.get("mutation_evidence_selector")
            ):
                issues.append(
                    "%s %s reuses one selector for control and mutation"
                    % (expected_id, variant_id)
                )
            for role in ("control", "mutation"):
                expected_selector = "direct-probe:%s:%s" % (
                    expected_variant_id,
                    role,
                )
                if variant.get(role + "_evidence_selector") != expected_selector:
                    issues.append(
                        "%s %s %s selector is not the exact direct-probe identity"
                        % (expected_id, expected_variant_id, role)
                    )
            entry_point = variant.get("validator_entry_point")
            if (
                isinstance(entry_point, str)
                and entry_point
                and not (pathlib.Path(root) / entry_point).is_file()
            ):
                issues.append("%s %s production validator is missing" % (expected_id, variant_id))
            for role in ("control", "mutation"):
                command = variant.get(role + "_command")
                if command is None:
                    issues.append("%s %s has no %s command" % (expected_id, variant_id, role))
                    continue
                expected_command = [
                    "python",
                    TASK14_PROBE,
                    "--attack-id",
                    expected_id,
                    "--variant-id",
                    expected_variant_id,
                    "--role",
                    role,
                ]
                if command != expected_command:
                    issues.append(
                        "%s %s %s command must invoke the production observation probe; "
                        "variant command identity mismatch"
                        % (expected_id, variant_id, role)
                    )

    for value in sorted({value for value in attack_ids if attack_ids.count(value) > 1}):
        issues.append("duplicate attack ID %s" % value)
    for value in sorted({value for value in variant_ids if variant_ids.count(value) > 1}):
        issues.append("duplicate variant ID %s" % value)
    for value in sorted(
        {value for value in mutation_ids if mutation_ids.count(value) > 1}
    ):
        issues.append("duplicate mutation ID %s" % value)

    try:
        ledger_rows = load_task14_ar6_rows(root)
    except (OSError, yaml.YAMLError) as exc:
        issues.append("Task 14 AR6 ledger cannot be loaded: %s" % exc)
        ledger_rows = []
    expected_ar6 = {
        row.get("artifact_id") for row in ledger_rows if row.get("artifact_id")
    }
    declared_ar6 = spec.get("task14_ar6_artifact_ids")
    if not isinstance(declared_ar6, list) or set(declared_ar6) != expected_ar6:
        issues.append("Task 14 AR6 artifact inventory differs from the impact ledger")
    if isinstance(declared_ar6, list) and len(declared_ar6) != len(set(declared_ar6)):
        issues.append("Task 14 AR6 artifact inventory contains duplicates")
    allowed_dispositions = {
        "INTERRUPTED_UNVERIFIED_RESEARCH",
        "COUNTERMODEL_OR_NEGATIVE_EVIDENCE",
    }
    for row in ledger_rows:
        if row.get("required_disposition") not in allowed_dispositions:
            issues.append(
                "%s has a non-adversarial Task 14 disposition"
                % row.get("artifact_id", "unknown AR6 artifact")
            )
        if row.get("normative_flow_status") != "NO_AUTOMATIC_NORMATIVE_FLOW":
            issues.append(
                "%s is not bounded away from automatic normative flow"
                % row.get("artifact_id", "unknown AR6 artifact")
            )
    mappings = spec.get("task14_ar6_mappings")
    if not isinstance(mappings, list):
        issues.append("Task 14 AR6 impact mappings must be a list")
        mappings = []
    mapping_ids = [
        row.get("artifact_id") for row in mappings if isinstance(row, dict)
    ]
    if set(mapping_ids) != expected_ar6 or len(mapping_ids) != len(set(mapping_ids)):
        issues.append("Task 14 AR6 impact mappings do not cover each ledger row exactly once")
    attack_variant_pairs = {
        (attack.get("attack_id"), variant.get("variant_id"))
        for attack in attacks
        if isinstance(attack, dict)
        for variant in attack.get("variants", [])
        if isinstance(variant, dict)
    }
    ledger_by_id = {
        row.get("artifact_id"): row for row in ledger_rows if row.get("artifact_id")
    }
    for mapping in mappings:
        if not isinstance(mapping, dict):
            issues.append("Task 14 AR6 impact mapping must be an object")
            continue
        artifact_id = mapping.get("artifact_id", "unknown AR6 artifact")
        ledger_row = ledger_by_id.get(artifact_id)
        status = mapping.get("reproduction_status")
        if not isinstance(mapping.get("neutral_concept"), str) or not mapping[
            "neutral_concept"
        ].strip():
            issues.append("%s AR6 mapping lacks a neutral concept" % artifact_id)
        if status == "REPRODUCED_AGAINST_INTEGRATED_TREE":
            pair = (mapping.get("attack_id"), mapping.get("variant_id"))
            if (
                pair not in attack_variant_pairs
                or mapping.get("normative_flow") != "NEGATIVE_EVIDENCE_ONLY"
            ):
                issues.append(
                    "%s reproduced AR6 row lacks exact attack/variant/result mapping"
                    % artifact_id
                )
            if (
                not isinstance(ledger_row, dict)
                or ledger_row.get("required_disposition")
                != "COUNTERMODEL_OR_NEGATIVE_EVIDENCE"
                or ledger_row.get("current_repository_representation")
                == "NO_CANONICAL_REPOSITORY_OWNER_IDENTIFIED"
            ):
                issues.append(
                    "%s may not be classified as reproduced against the integrated tree"
                    % artifact_id
                )
        elif status == "NOT_REPRODUCED_RETAINED_PROVENANCE_ONLY":
            if (
                mapping.get("attack_id") is not None
                or mapping.get("variant_id") is not None
                or mapping.get("normative_flow") != "NO_NORMATIVE_OR_PUBLICATION_FLOW"
            ):
                issues.append(
                    "%s unreproduced AR6 row may not enter normative flow" % artifact_id
                )
        else:
            issues.append("%s has an invalid AR6 reproduction status" % artifact_id)
    return issues


def task14_probe_identity(command):
    """Parse one exact Task 14 observation-probe command."""
    tokens = list(command)
    if len(tokens) != 8 or tokens[1] != TASK14_PROBE:
        raise ValueError("command is not an exact Task 14 observation probe")
    if tokens[2] != "--attack-id" or tokens[4] != "--variant-id" or tokens[6] != "--role":
        raise ValueError("Task 14 observation-probe argument order drifted")
    if tokens[7] not in {"control", "mutation"}:
        raise ValueError("Task 14 observation-probe role is invalid")
    return {
        "attack_id": tokens[3],
        "variant_id": tokens[5],
        "role": tokens[7],
    }


def _parse_task14_observation(
    completed, expected, seen_observation_ids=None, trusted_direct_result=None
):
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        raise ValueError(
            "observation probe exited %d%s"
            % (completed.returncode, ": " + detail[-500:] if detail else "")
        )
    try:
        payload = json.loads(completed.stdout)
    except (TypeError, ValueError) as exc:
        raise ValueError("missing machine-readable observation: %s" % exc)
    if not isinstance(payload, dict) or payload.get("schema") != TASK14_OBSERVATION_SCHEMA:
        raise ValueError("missing machine-readable observation schema")
    exact_fields = {
        "schema",
        *expected.keys(),
        "observed_validator_outcome",
        "evidence_process_exit_code",
        "exit_semantics",
        "input_sha256",
        "observation_id",
    }
    if set(payload) != exact_fields:
        raise ValueError(
            "observation field set mismatch: missing=%s extra=%s"
            % (
                sorted(exact_fields - set(payload)),
                sorted(set(payload) - exact_fields),
            )
        )
    for field, value in expected.items():
        if payload.get(field) != value:
            raise ValueError(
                "observation identity mismatch for %s: expected %r, observed %r"
                % (field, value, payload.get(field))
            )
    expected_outcome = "accepted" if expected["role"] == "control" else "rejected"
    if payload.get("observed_validator_outcome") != expected_outcome:
        raise ValueError(
            "%s direct probe observed %s instead of %s"
            % (
                expected["role"],
                payload.get("observed_validator_outcome", "missing"),
                expected_outcome,
            )
        )
    if payload.get("evidence_process_exit_code") != 0:
        raise ValueError(
            "%s evidence process exit semantics drifted: expected 0, observed %r"
            % (
                expected["role"],
                payload.get("evidence_process_exit_code"),
            )
        )
    semantics = payload.get("exit_semantics")
    if (
        not isinstance(semantics, str)
        or "validator acceptance or rejection is carried only by "
        "observed_validator_outcome" not in semantics
    ):
        raise ValueError("%s evidence exit semantics are missing" % expected["role"])
    input_sha256 = payload.get("input_sha256")
    if (
        not isinstance(input_sha256, str)
        or len(input_sha256) != 64
        or any(character not in "0123456789abcdef" for character in input_sha256)
    ):
        raise ValueError("%s direct-probe input digest is invalid" % expected["role"])
    if trusted_direct_result is not None:
        if payload.get("observed_validator_outcome") != trusted_direct_result.get(
            "outcome"
        ):
            raise ValueError(
                "%s observation outcome differs from independent direct execution"
                % expected["role"]
            )
        if input_sha256 != trusted_direct_result.get("input_sha256"):
            raise ValueError(
                "%s observation input digest differs from independent direct execution"
                % expected["role"]
            )
    observation_id = task14_observation_id(
        expected, expected_outcome, input_sha256
    )
    if payload.get("observation_id") != observation_id:
        raise ValueError("%s observation ID does not bind its payload" % expected["role"])
    if seen_observation_ids is not None:
        if observation_id in seen_observation_ids:
            raise ValueError("duplicate observation %s" % observation_id)
        seen_observation_ids.add(observation_id)
    return payload


def run_task14_attacks(
    spec,
    root,
    runner=subprocess.run,
    python=sys.executable,
    direct_executor=execute_direct_probe,
):
    """Run separate controls and mutations and retain their semantic observations."""
    issues = audit_task14_spec(spec, root)
    if issues:
        return [], issues
    results = []
    observation_ids = set()
    registry = load_task14_probe_registry(root)
    for attack in spec["mandatory_attacks"]:
        for variant in attack["variants"]:
            observations = {}
            failed = False
            for role in ("control", "mutation"):
                command = [python] + list(variant[role + "_command"][1:])
                try:
                    completed = runner(
                        command,
                        cwd=str(root),
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        timeout=180,
                    )
                except (OSError, subprocess.TimeoutExpired) as exc:
                    completed = type(
                        "Task14CommandFailure",
                        (),
                        {"returncode": 124, "stdout": "", "stderr": str(exc)},
                    )()
                binding = registry[(attack["attack_id"], variant["variant_id"])]
                expected = expected_task14_observation(binding, role, root)
                try:
                    trusted_direct_result = direct_executor(binding, role)
                except (KeyError, OSError, RuntimeError, ValueError) as exc:
                    issues.append(
                        "%s %s %s: independent direct execution failed: %s"
                        % (
                            attack["attack_id"],
                            variant["variant_id"],
                            role,
                            exc,
                        )
                    )
                    failed = True
                    continue
                try:
                    observations[role] = _parse_task14_observation(
                        completed,
                        expected,
                        observation_ids,
                        trusted_direct_result,
                    )
                except ValueError as exc:
                    issues.append(
                        "%s %s %s: %s"
                        % (
                            attack["attack_id"],
                            variant["variant_id"],
                            role,
                            exc,
                        )
                    )
                    failed = True
            if failed:
                continue
            results.append(
                {
                    "attack_id": attack["attack_id"],
                    "name": attack["name"],
                    "variant_id": variant["variant_id"],
                    "mutation_id": variant["mutation_id"],
                    "neutral_concept": variant["neutral_concept"],
                    "invariant": attack["invariant"],
                    "owner": attack["owner"],
                    "validator_owner": observations["control"]["validator_owner"],
                    "validator_entry_point": variant["validator_entry_point"],
                    "validator_sha256": observations["control"]["validator_sha256"],
                    "control_command": " ".join(variant["control_command"]),
                    "mutation_command": " ".join(variant["mutation_command"]),
                    "control_evidence_selector": observations["control"][
                        "evidence_selector"
                    ],
                    "control_observed_outcome": observations["control"][
                        "observed_validator_outcome"
                    ],
                    "control_evidence_process_exit_code": observations["control"][
                        "evidence_process_exit_code"
                    ],
                    "control_input_sha256": observations["control"]["input_sha256"],
                    "control_observation_id": observations["control"]["observation_id"],
                    "mutation_evidence_selector": observations["mutation"][
                        "evidence_selector"
                    ],
                    "mutation_observed_outcome": observations["mutation"][
                        "observed_validator_outcome"
                    ],
                    "mutation_evidence_process_exit_code": observations["mutation"][
                        "evidence_process_exit_code"
                    ],
                    "mutation_input_sha256": observations["mutation"]["input_sha256"],
                    "mutation_observation_id": observations["mutation"]["observation_id"],
                }
            )
    if issues:
        return [], issues
    return results, issues


def _cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_task14_report(spec, results, root, recursive_totals=None):
    """Render the byte-stable Task 14 report from current executable results."""
    recursive_totals = recursive_totals or {}
    unique_commands = {
        command
        for row in results
        for command in (row["control_command"], row["mutation_command"])
    }
    passed = [
        row
        for row in results
        if row["control_observed_outcome"] == "accepted"
        and row["mutation_observed_outcome"] == "rejected"
    ]
    variants = len(results)
    lines = [
        "# R7E Sol adversarial and mutation report",
        "",
        "This report is derived from the integrated tree. It does not copy historical "
        "R7C/R7D totals or infer interrupted research outcomes.",
        "",
        "## Method and current totals",
        "",
        "- Exact approved Task 13 base: `%s`" % spec.get("task14_exact_base", "UNDECLARED"),
        "- Mandatory attacks: %d" % len(spec.get("mandatory_attacks", [])),
        "- Structured coverage variants: %d" % variants,
        "- Executed separate control/mutation commands: %d" % len(unique_commands),
        "- Passing variants: %d" % len(passed),
        "- Valid controls observed accepted: %d" % sum(
            row["control_observed_outcome"] == "accepted" for row in results
        ),
        "- Invalid mutations observed rejected: %d" % sum(
            row["mutation_observed_outcome"] == "rejected" for row in results
        ),
    ]
    if recursive_totals:
        lines.extend([
            "- Recursive operator families: %d" % recursive_totals.get("families", 0),
            "- Recursive mutants generated: %d" % recursive_totals.get("generated", 0),
            "- Schema-killed: %d" % recursive_totals.get("killed_schema", 0),
            "- Semantic-killed: %d" % recursive_totals.get("killed_semantic", 0),
            "- Justified equivalents: %d" % recursive_totals.get("justified", 0),
            "- Unjustified survivors: %d" % recursive_totals.get("unjustified", 0),
        ])
    lines.extend([
        "",
        "Every row comes from two distinct processes. Each process emits an exact "
        "machine-readable observation bound to the attack, variant, role, production "
        "validator, validator digest, direct-probe selector, concrete-input digest, "
        "and observation ID. The adapter derives acceptance or rejection only from "
        "the production API or CLI result; a probe-process exit code is never treated "
        "as the validator outcome.",
        "",
        "## Mandatory attacks",
        "",
        "| Attack ID | Attack | Variant | Mutation ID | Neutral concept | Invariant | Production validator | Control command / outcome (probe RC) | Mutation command / outcome (probe RC) | Owner |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ])
    for row in results:
        lines.append(
            "| %s | %s | %s | %s | %s | %s | `%s` | `%s` / %s (%d) | `%s` / %s (%d) | %s |"
            % (
                _cell(row["attack_id"]),
                _cell(row["name"]),
                _cell(row["variant_id"]),
                _cell(row["mutation_id"]),
                _cell(row["neutral_concept"]),
                _cell(row["invariant"]),
                _cell(row["validator_entry_point"]),
                _cell(row["control_command"]),
                _cell(row["control_observed_outcome"]),
                row["control_evidence_process_exit_code"],
                _cell(row["mutation_command"]),
                _cell(row["mutation_observed_outcome"]),
                row["mutation_evidence_process_exit_code"],
                _cell(row["owner"]),
            )
        )
    lines.extend([
        "",
        "## Exact direct-observation bindings",
        "",
        "| Variant | Mutation ID | Validator owner | Validator / SHA-256 | Control selector / input / observation | Mutation selector / input / observation |",
        "|---|---|---|---|---|---|",
    ])
    for row in results:
        lines.append(
            "| %s | %s | %s | `%s` / `%s` | `%s` / `%s` / `%s` | `%s` / `%s` / `%s` |"
            % (
                _cell(row["variant_id"]),
                _cell(row["mutation_id"]),
                _cell(row["validator_owner"]),
                _cell(row["validator_entry_point"]),
                _cell(row["validator_sha256"]),
                _cell(row["control_evidence_selector"]),
                _cell(row["control_input_sha256"]),
                _cell(row["control_observation_id"]),
                _cell(row["mutation_evidence_selector"]),
                _cell(row["mutation_input_sha256"]),
                _cell(row["mutation_observation_id"]),
            )
        )
    lines.extend([
        "",
        "## AR6 adversarial reconciliation",
        "",
        "Interrupted AR6 research is excluded from normative and publication flow. "
        "Only entries already dispositioned as countermodels or negative evidence "
        "may inform reproduced attacks; no interrupted claim is promoted.",
        "",
        "| Artifact ID | Tranche | Disposition | Neutral concept | Reproduction status | Exact Task 14 mapping | Production command and observed result | Normative flow |",
        "|---|---|---|---|---|---|---|---|",
    ])
    mappings = {
        row["artifact_id"]: row
        for row in spec.get("task14_ar6_mappings", [])
        if isinstance(row, dict) and row.get("artifact_id")
    }
    result_by_pair = {
        (row["attack_id"], row["variant_id"]): row for row in results
    }
    for row in load_task14_ar6_rows(root):
        artifact_id = row.get("artifact_id", "")
        mapping = mappings.get(artifact_id, {})
        status = mapping.get("reproduction_status", "UNMAPPED")
        pair = (mapping.get("attack_id"), mapping.get("variant_id"))
        observed = result_by_pair.get(pair)
        if status == "REPRODUCED_AGAINST_INTEGRATED_TREE" and observed:
            exact_mapping = "%s / %s" % pair
            command_result = "`%s` -> directly observed %s (probe process rc %d)" % (
                observed["mutation_command"],
                observed["mutation_observed_outcome"],
                observed["mutation_evidence_process_exit_code"],
            )
        else:
            exact_mapping = "none"
            command_result = "not reproduced; retained as provenance only"
        lines.append(
            "| %s | %s | %s | %s | %s | %s | %s | %s |"
            % (
                _cell(artifact_id),
                _cell(row.get("research_tranche", "")),
                _cell(row.get("required_disposition", "")),
                _cell(mapping.get("neutral_concept", "")),
                _cell(status),
                _cell(exact_mapping),
                _cell(command_result),
                _cell(mapping.get("normative_flow", "")),
            )
        )
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------- schema loading
def load_schemas():
    sdir = os.path.join(ROOT, "schemas")
    schemas, resources = {}, []
    for fn in sorted(os.listdir(sdir)):
        if fn.endswith(".schema.json"):
            doc = json.load(open(os.path.join(sdir, fn), encoding="utf-8"))
            schemas[fn] = doc
            resources.append((fn, Resource.from_contents(doc)))
            resources.append((doc.get("$id", fn), Resource.from_contents(doc)))
    return schemas, Registry().with_resources(resources)


class Ctx(object):
    def __init__(self, schemas, registry):
        self.schemas = schemas
        self.registry = registry

    def accepts(self, sname, inst):
        v = Draft202012Validator(self.schemas[sname], registry=self.registry)
        return not list(v.iter_errors(inst))

    def valid_against(self, sub, doc, inst):
        """Is `inst` valid against the subschema `sub` living in document `doc`?"""
        probe = dict(sub)
        probe.setdefault("$schema", "https://json-schema.org/draft/2020-12/schema")
        probe["$id"] = doc.get("$id", "orthemology/anonymous.json")
        try:
            v = Draft202012Validator(probe, registry=self.registry)
            return not list(v.iter_errors(inst))
        except Exception:
            return False

    def deref(self, ref, doc):
        if ref.startswith("#"):
            node = doc
            for part in ref.lstrip("#/").split("/"):
                if part:
                    node = node[part]
            return node, doc
        fn = ref.split("/")[-1]
        target = self.schemas[fn]
        return target, target

    def effective(self, sub, doc, inst, depth=0):
        """Merge $ref / allOf / applicable if-then / matching anyOf-oneOf branch."""
        eff = {"properties": {}, "required": set(), "items": None, "additional": None,
               "uniqueItems": False, "doc": doc}
        if depth > 12 or not isinstance(sub, dict):
            return eff

        def merge(other):
            eff["properties"].update(other["properties"])
            eff["required"] |= other["required"]
            eff["items"] = other["items"] or eff["items"]
            eff["additional"] = other["additional"] if other["additional"] is not None \
                else eff["additional"]
            eff["uniqueItems"] = eff["uniqueItems"] or other["uniqueItems"]
            if other["doc"] is not doc:
                eff["doc"] = other["doc"]

        if "$ref" in sub:
            tgt, tdoc = self.deref(sub["$ref"], doc)
            merge(self.effective(tgt, tdoc, inst, depth + 1))
        for k, v in (sub.get("properties") or {}).items():
            eff["properties"][k] = (v, eff["doc"])
        eff["required"] |= set(sub.get("required") or [])
        if "items" in sub:
            eff["items"] = (sub["items"], doc)
        if isinstance(sub.get("additionalProperties"), dict):
            eff["additional"] = (sub["additionalProperties"], doc)
        if sub.get("uniqueItems"):
            eff["uniqueItems"] = True
        for branch in (sub.get("allOf") or []):
            merge(self.effective(branch, doc, inst, depth + 1))
        if "if" in sub:
            taken = "then" if self.valid_against(sub["if"], doc, inst) else "else"
            if taken in sub:
                merge(self.effective(sub[taken], doc, inst, depth + 1))
        for key in ("anyOf", "oneOf"):
            for branch in (sub.get(key) or []):
                if self.valid_against(branch, doc, inst):
                    merge(self.effective(branch, doc, inst, depth + 1))
                    break
        return eff


def walk(ctx, sub, doc, inst, path=()):
    """Yield (path, value, effective_schema) for every node of `inst`."""
    eff = ctx.effective(sub, doc, inst)
    yield path, inst, eff
    if isinstance(inst, dict):
        for k in sorted(inst):
            child = eff["properties"].get(k) or eff["additional"]
            if child is None:
                continue
            for out in walk(ctx, child[0], child[1], inst[k], path + (k,)):
                yield out
    elif isinstance(inst, list) and eff["items"]:
        for i, v in enumerate(inst):
            for out in walk(ctx, eff["items"][0], eff["items"][1], v, path + (i,)):
                yield out


# ------------------------------------------------------------------ path access
def get(root, path):
    node = root
    for p in path:
        node = node[p]
    return node


def setv(root, path, value):
    get(root, path[:-1])[path[-1]] = value


def delv(root, path):
    parent = get(root, path[:-1])
    if isinstance(parent, list):
        del parent[path[-1]]
    else:
        del parent[path[-1]]


def pstr(path):
    return "/".join(str(p) for p in path) or "<root>"


# ---------------------------------------------------------------- kill checking
class Bundle(object):
    def __init__(self, fn, parts):
        self.fn = fn
        self.parts = parts


class Engine(object):
    def __init__(self, ctx, bundles):
        self.ctx = ctx
        self.bundles = bundles
        self.results = {fid: {"generated": 0, "killed_schema": 0, "killed_semantic": 0,
                              "survivors": []} for fid, _, _ in FAMILIES}

    def emit(self, fam, bundle, idx, path, mutated_part_instance, note=""):
        """Record one mutant: mutate part `idx` of `bundle` and test both layers."""
        r = self.results[fam]
        r["generated"] += 1
        sname = bundle.parts[idx]["schema"]
        sig = "%s#%d %s %s%s" % (bundle.fn, idx, fam, pstr(path), (" " + note) if note else "")
        if not self.ctx.accepts(sname, mutated_part_instance):
            r["killed_schema"] += 1
            return
        parts = [dict(p) for p in bundle.parts]
        parts[idx] = {"schema": sname, "instance": mutated_part_instance}
        if collect_issues(parts):
            r["killed_semantic"] += 1
            return
        r["survivors"].append(sig)


# ------------------------------------------------------------- mutation families
def generate(engine, ctx, bundle):
    parts = bundle.parts
    schemas = ctx.schemas

    # bundle-level referent inventories (a reference can only be broken where it
    # currently resolves; mutating an unresolvable reference proves nothing)
    episode_ids = {p["instance"].get("episode_id") for p in parts
                   if p["schema"] == "orthing-episode.schema.json"}
    token_ids = set()
    for p in parts:
        if p["schema"] == "metaorthemma.schema.json":
            token_ids.add(p["instance"]["token_id"])
        if p["schema"] == "orthing-episode.schema.json":
            token_ids |= {t["token_id"] for t in p["instance"].get("meta_tokens", [])}
    ledger_claims = {}
    for p in parts:
        if p["schema"] == "claim-ledger.schema.json":
            ledger_claims[p["instance"].get("episode_id")] = {
                c["claim_id"] for c in p["instance"].get("claims", [])}
    episode_by_id = {p["instance"].get("episode_id"): p["instance"] for p in parts
                     if p["schema"] == "orthing-episode.schema.json"}

    for idx, part in enumerate(parts):
        sname, inst = part["schema"], part["instance"]
        sdoc = schemas[sname]

        # ---- structural families 1-4 over every node
        for path, value, eff in walk(ctx, sdoc, sdoc, inst):
            if isinstance(value, dict):
                for key in sorted(eff["required"]):
                    if key not in value:
                        continue
                    kpath = path + (key,)
                    m = copy.deepcopy(inst)
                    delv(m, kpath)
                    engine.emit("1", bundle, idx, kpath, m)

                    kv = value[key]
                    if isinstance(kv, str) and kv != "":
                        m = copy.deepcopy(inst)
                        setv(m, kpath, "")
                        engine.emit("2", bundle, idx, kpath, m)
                    if isinstance(kv, list) and kv:
                        m = copy.deepcopy(inst)
                        setv(m, kpath, [])
                        engine.emit("3", bundle, idx, kpath, m, note="[]")
                    if isinstance(kv, dict) and kv:
                        m = copy.deepcopy(inst)
                        setv(m, kpath, {})
                        engine.emit("3", bundle, idx, kpath, m, note="{}")
            if isinstance(value, list) and value and eff["uniqueItems"]:
                m = copy.deepcopy(inst)
                get(m, path).append(copy.deepcopy(value[0]))
                engine.emit("4", bundle, idx, path, m, note="duplicate-member")

        # ---- 4b: collide two ids that must differ (unique by id, not by value)
        for coll, key in (("evidence", "evidence_id"), ("meta_tokens", "token_id")):
            seq = inst.get(coll) if isinstance(inst, dict) else None
            if isinstance(seq, list) and len(seq) >= 2:
                m = copy.deepcopy(inst)
                m[coll][1][key] = m[coll][0][key]
                engine.emit("4", bundle, idx, (coll, 1, key), m, note="id-collision")
        if sname == "claim-ledger.schema.json" and len(inst.get("claims", [])) >= 2:
            m = copy.deepcopy(inst)
            m["claims"][1]["claim_id"] = m["claims"][0]["claim_id"]
            engine.emit("4", bundle, idx, ("claims", 1, "claim_id"), m, note="id-collision")

        # ---- 5: unknown-reference-id (only where the reference resolves today)
        def break_ref(path, guard=True):
            if not guard:
                return
            m = copy.deepcopy(inst)
            setv(m, path, MUTANT_MARK)
            engine.emit("5", bundle, idx, path, m)

        if sname == "verdict-record.schema.json":
            claims_here = ledger_claims.get(inst.get("episode_id"), set())
            for i in range(len(inst.get("per_token_v3c", []))):
                break_ref(("per_token_v3c", i, "token_id"), bool(token_ids))
            for i in range(len(inst.get("claim_verdicts", []))):
                break_ref(("claim_verdicts", i, "claim_id"), bool(claims_here))
            for i in range(len(inst.get("claim_reasoning_paths", []))):
                break_ref(("claim_reasoning_paths", i, "claim_id"), bool(claims_here))
            for mapname in ("rel_spec", "perturb_spec"):
                for k in sorted(inst.get(mapname, {})):
                    if claims_here:
                        m = copy.deepcopy(inst)
                        m[mapname][MUTANT_MARK] = m[mapname].pop(k)
                        engine.emit("5", bundle, idx, (mapname, k), m, note="rekey")
        if sname == "claim-ledger.schema.json":
            ep = episode_by_id.get(inst.get("episode_id"))
            for ci, c in enumerate(inst.get("claims", [])):
                for j in range(len(c.get("evidence_ids", []))):
                    break_ref(("claims", ci, "evidence_ids", j), ep is not None)
                for j in range(len(c.get("depends_on_tokens", []))):
                    break_ref(("claims", ci, "depends_on_tokens", j), bool(token_ids))
                for j in range(len(c.get("depends_on_claims", []))):
                    break_ref(("claims", ci, "depends_on_claims", j))
        if sname == "handoff.schema.json":
            for role in ("sender_episode", "receiver_episode"):
                break_ref((role,), bool(episode_ids))

        # ---- 6: analysis-version-mismatch
        if sname == "orthing-episode.schema.json":
            for ti in range(len(inst.get("meta_tokens", []))):
                m = copy.deepcopy(inst)
                m["meta_tokens"][ti]["analysis"]["version"] = "MUTANT-VERSION"
                engine.emit("6", bundle, idx, ("meta_tokens", ti, "analysis", "version"), m)
        if sname == "claim-ledger.schema.json" and episode_by_id.get(inst.get("episode_id")):
            for ci in range(len(inst.get("claims", []))):
                if "analysis" in inst["claims"][ci]:
                    m = copy.deepcopy(inst)
                    m["claims"][ci]["analysis"]["version"] = "MUTANT-VERSION"
                    engine.emit("6", bundle, idx, ("claims", ci, "analysis", "version"), m)
        if sname == "verdict-record.schema.json" and episode_by_id.get(inst.get("episode_id")):
            m = copy.deepcopy(inst)
            m["index"]["analysis_version"] = "MUTANT-VERSION"
            engine.emit("6", bundle, idx, ("index", "analysis_version"), m)

        # ---- 7: occurrence-version-mismatch. Only generated where a SECOND record
        # in the bundle carries the same occurrence version: with nothing to
        # desynchronise from, the mutation is vacuous rather than undetected.
        if sname == "orthing-episode.schema.json":
            occ_key = (inst.get("occurrence") or {}).get("identity_key")
            has_witness = (
                any(p["schema"] == "orthemma.schema.json"
                    and p["instance"].get("identity_key") == occ_key for p in parts)
                or bool(inst.get("meta_tokens"))
                or any(p["schema"] == "handoff.schema.json"
                       and inst.get("episode_id") in (p["instance"].get("sender_episode"),
                                                      p["instance"].get("receiver_episode"))
                       for p in parts))
            if has_witness:
                m = copy.deepcopy(inst)
                m["occurrence"]["version"] = "MUTANT-VERSION"
                engine.emit("7", bundle, idx, ("occurrence", "version"), m)
            for ti in range(len(inst.get("meta_tokens", []))):
                m = copy.deepcopy(inst)
                m["meta_tokens"][ti]["anchor"]["version"] = "MUTANT-VERSION"
                engine.emit("7", bundle, idx, ("meta_tokens", ti, "anchor", "version"), m)
        if sname == "orthemma.schema.json" and episode_by_id:
            m = copy.deepcopy(inst)
            m["version"] = "MUTANT-VERSION"
            engine.emit("7", bundle, idx, ("version",), m)
        if sname == "handoff.schema.json" and episode_ids:
            for field in ("identity_key", "version"):
                m = copy.deepcopy(inst)
                m["subject"][field] = MUTANT_MARK
                engine.emit("7", bundle, idx, ("subject", field), m)

        # ---- 8: delete-disposition-conditional-field
        if sname == "claim-ledger.schema.json":
            cond = {
                "unresolved": ["responsible_queue", "next_review_condition"],
                "deferred": ["trigger", "review_date"],
                "transferred": ["receiver", "transfer_record"],
                "owner-assigned": ["owner", "acceptance_state"],
                "risk-accepted": ["risk_owner", "rationale", "scope", "review_trigger"],
                "validated-resolved": ["evidence_refs", "verdict_refs"],
            }
            for ri, r in enumerate(inst.get("residuals", [])):
                fields = [f for f in cond.get(r.get("disposition"), []) if r.get(f)]
                for f in fields:
                    m = copy.deepcopy(inst)
                    del m["residuals"][ri][f]
                    engine.emit("8", bundle, idx, ("residuals", ri, f), m)
                if len(fields) > 1:
                    m = copy.deepcopy(inst)
                    for f in fields:
                        del m["residuals"][ri][f]
                    engine.emit("8", bundle, idx, ("residuals", ri, "*"), m, note="all-conditionals")

        # ---- 9: claim-dependency-cycle
        if sname == "claim-ledger.schema.json":
            cl = inst.get("claims", [])
            if cl:
                m = copy.deepcopy(inst)
                m["claims"][0]["depends_on_claims"] = [m["claims"][0]["claim_id"]]
                engine.emit("9", bundle, idx, ("claims", 0, "depends_on_claims"), m, note="self")
            if len(cl) >= 2:
                m = copy.deepcopy(inst)
                m["claims"][0]["depends_on_claims"] = [m["claims"][1]["claim_id"]]
                m["claims"][1]["depends_on_claims"] = [m["claims"][0]["claim_id"]]
                engine.emit("9", bundle, idx, ("claims", "0<->1", "depends_on_claims"), m,
                            note="mutual")

        if sname == "verdict-record.schema.json":
            statuses, req = inst["statuses"], inst["required_path"]
            # ---- 10: remove-required-verdict-status
            for v in req:
                if v in statuses:
                    m = copy.deepcopy(inst)
                    del m["statuses"][v]
                    engine.emit("10", bundle, idx, ("statuses", v), m)
            # ---- 11: contradict-pathway-summary
            for state in ("adequate", "defective", "undetermined"):
                if state != inst["pathway_state"]:
                    m = copy.deepcopy(inst)
                    m["pathway_state"] = state
                    engine.emit("11", bundle, idx, ("pathway_state",), m, note="->" + state)
            for ci, crp in enumerate(inst.get("claim_reasoning_paths", [])):
                for state in ("adequate", "defective", "undetermined"):
                    if state == crp["reasoning_path_adequate"] or state == inst["pathway_state"]:
                        continue  # equal-to-episode-state is family 18's business
                    m = copy.deepcopy(inst)
                    m["claim_reasoning_paths"][ci]["reasoning_path_adequate"] = state
                    engine.emit("11", bundle, idx,
                                ("claim_reasoning_paths", ci, "reasoning_path_adequate"), m,
                                note="->" + state)
            # ---- 12: na-without-reason (anywhere, not just on the required path)
            for v in sorted(inst.get("na_reasons", {})):
                m = copy.deepcopy(inst)
                del m["na_reasons"][v]
                engine.emit("12", bundle, idx, ("na_reasons", v), m)
            # ---- 15: postdate-reliability-declaration
            for k in sorted(inst.get("rel_spec", {})):
                m = copy.deepcopy(inst)
                m["rel_spec"][k]["declared_at"] = "2099-01-01T00:00:00Z"
                engine.emit("15", bundle, idx, ("rel_spec", k, "declared_at"), m)
            # ---- 16: violate-perturbation-invariant
            for k in sorted(inst.get("perturb_spec", {})):
                ps = inst["perturb_spec"][k]
                if ps.get("invariants"):
                    m = copy.deepcopy(inst)
                    m["perturb_spec"][k]["varied_fields"] = \
                        list(m["perturb_spec"][k]["varied_fields"]) + [ps["invariants"][0]]
                    engine.emit("16", bundle, idx, ("perturb_spec", k, "varied_fields"), m)
            # ---- 18: collapse-claim-path-into-episode-path
            for ci, crp in enumerate(inst.get("claim_reasoning_paths", [])):
                if crp["reasoning_path_adequate"] != inst["pathway_state"]:
                    m = copy.deepcopy(inst)
                    m["claim_reasoning_paths"][ci]["reasoning_path_adequate"] = \
                        inst["pathway_state"]
                    engine.emit("18", bundle, idx,
                                ("claim_reasoning_paths", ci, "reasoning_path_adequate"), m,
                                note="->episode " + inst["pathway_state"])

        # ---- 13 / 14: metaorthemma typing and binding
        def token_paths():
            if sname == "metaorthemma.schema.json":
                yield ()
            if sname == "orthing-episode.schema.json":
                for ti in range(len(inst.get("meta_tokens", []))):
                    yield ("meta_tokens", ti)

        for tp in token_paths():
            tok = get(inst, tp) if tp else inst
            m = copy.deepcopy(inst)
            second = copy.deepcopy(tok["of_type"])
            second["mu_id"] = second["mu_id"] + "-second"
            target = get(m, tp) if tp else m
            target["of_type"] = [copy.deepcopy(tok["of_type"]), second]
            engine.emit("13", bundle, idx, tp + ("of_type",), m)

            m = copy.deepcopy(inst)
            target = get(m, tp) if tp else m
            target["binding"] = {}
            engine.emit("14", bundle, idx, tp + ("binding",), m)

        # ---- 19: inheritance self-edge / ghost parent (D1)
        if sname == "analysis.schema.json":
            m = copy.deepcopy(inst)
            m["inherits_from"] = {"analysis_id": inst["analysis_id"],
                                  "version": inst["version"]}
            engine.emit("19", bundle, idx, ("inherits_from",), m, note="self")
            m = copy.deepcopy(inst)
            m["inherits_from"] = {"analysis_id": MUTANT_MARK, "version": "1"}
            engine.emit("19", bundle, idx, ("inherits_from",), m, note="ghost-parent")

        # ---- 20: cross-episode token collision (D3)
        if sname == "orthing-episode.schema.json" and inst.get("meta_tokens"):
            own = {t["token_id"] for t in inst["meta_tokens"]}
            for other in sorted(token_ids - own):
                m = copy.deepcopy(inst)
                m["meta_tokens"][0]["token_id"] = other
                engine.emit("20", bundle, idx, ("meta_tokens", 0, "token_id"), m,
                            note="->" + other)
                break

        # ---- 21: token scope leakage across ledgers (D4)
        if sname == "orthing-episode.schema.json" and len(ledger_claims) >= 2:
            foreign = sorted(set().union(*(c for e2, c in ledger_claims.items()
                                           if e2 != inst.get("episode_id"))) or set())
            for ti in range(len(inst.get("meta_tokens", []))):
                if foreign:
                    m = copy.deepcopy(inst)
                    m["meta_tokens"][ti].setdefault("scope", {})["claims"] = [foreign[0]]
                    m["meta_tokens"][ti]["scope"].pop("no_claim_dependency_reason", None)
                    engine.emit("21", bundle, idx, ("meta_tokens", ti, "scope", "claims"), m,
                                note="->" + foreign[0])

        # ---- 22: ghost metaortheme reference (D5)
        mu_ids_declared = {p2["instance"].get("mu_id") for p2 in parts
                           if p2["schema"] == "metaortheme.schema.json"}
        if sname == "orthing-episode.schema.json":
            gc = inst.get("governing_configuration") or {}
            for ri, r in enumerate(gc.get("mu_refs", [])):
                if r.get("mu_id") in mu_ids_declared:
                    m = copy.deepcopy(inst)
                    m["governing_configuration"]["mu_refs"][ri]["mu_version"] = "MUTANT-VERSION"
                    engine.emit("22", bundle, idx,
                                ("governing_configuration", "mu_refs", ri, "mu_version"), m)
            for ti, t in enumerate(inst.get("meta_tokens", [])):
                if (t.get("of_type") or {}).get("mu_id") in mu_ids_declared:
                    m = copy.deepcopy(inst)
                    m["meta_tokens"][ti]["of_type"]["mu_version"] = "MUTANT-VERSION"
                    engine.emit("22", bundle, idx,
                                ("meta_tokens", ti, "of_type", "mu_version"), m)

        # ---- 23: precedence self-edge / 2-cycle (D5)
        if sname == "orthing-episode.schema.json":
            gc = inst.get("governing_configuration") or {}
            ids = [r["mu_id"] for r in gc.get("mu_refs", [])]
            if ids:
                m = copy.deepcopy(inst)
                m["governing_configuration"]["precedence"] = \
                    list(gc.get("precedence", [])) + [[ids[0], ids[0]]]
                engine.emit("23", bundle, idx, ("governing_configuration", "precedence"), m,
                            note="self-edge")
            if len(ids) >= 2:
                m = copy.deepcopy(inst)
                m["governing_configuration"]["precedence"] = [[ids[0], ids[1]],
                                                              [ids[1], ids[0]]]
                engine.emit("23", bundle, idx, ("governing_configuration", "precedence"), m,
                            note="2-cycle")

        # ---- 24: mixed-offset time reversal / naive timestamp (D7)
        if sname == "verdict-record.schema.json" and inst.get("rel_spec"):
            import datetime as _dt
            raw = inst.get("index", {}).get("decision_time")
            try:
                base = _dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
            except (AttributeError, ValueError):
                base = None
            for k in sorted(inst["rel_spec"]):
                if base is not None:
                    post = (base + _dt.timedelta(hours=3)).astimezone(
                        _dt.timezone(_dt.timedelta(hours=-5)))
                    val = post.isoformat()
                    if val < raw:  # string-compares BEFORE while being AFTER in UTC
                        m = copy.deepcopy(inst)
                        m["rel_spec"][k]["declared_at"] = val
                        engine.emit("24", bundle, idx, ("rel_spec", k, "declared_at"), m,
                                    note="mixed-offset-postdated")
                m = copy.deepcopy(inst)
                m["rel_spec"][k]["declared_at"] = "2026-01-01T00:00:00"
                engine.emit("24", bundle, idx, ("rel_spec", k, "declared_at"), m,
                            note="naive")

        # ---- 25: inverted token validity (D7)
        for tp25 in ([()] if sname == "metaorthemma.schema.json" else []) + \
                    ([("meta_tokens", ti) for ti in range(len(inst.get("meta_tokens", [])))]
                     if sname == "orthing-episode.schema.json" else []):
            tok = get(inst, tp25) if tp25 else inst
            eff = (tok.get("validity") or {}).get("effective_from")
            if isinstance(eff, str) and eff:
                m = copy.deepcopy(inst)
                target = get(m, tp25) if tp25 else m
                target["validity"]["expiry"] = "2000-01-01T00:00:00Z"
                engine.emit("25", bundle, idx, tp25 + ("validity", "expiry"), m,
                            note="expiry-before-effective")

        # ---- 26: silent external reference (D6)
        if sname == "orthing-episode.schema.json" and inst.get("record_mode") == "audit-ready":
            for ri in range(len(inst.get("external_refs", []))):
                m = copy.deepcopy(inst)
                del m["external_refs"][ri]
                engine.emit("26", bundle, idx, ("external_refs", ri), m, note="stripped")
                m = copy.deepcopy(inst)
                m["external_refs"][ri]["resolution_status"] = "unresolved"
                engine.emit("26", bundle, idx,
                            ("external_refs", ri, "resolution_status"), m, note="unresolved")
            ean = inst.get("analysis", {})
            if ean.get("version") in {p2["instance"].get("version") for p2 in parts
                                      if p2["schema"] == "analysis.schema.json"
                                      and p2["instance"].get("analysis_id") == ean.get("analysis_id")}:
                m = copy.deepcopy(inst)
                m["analysis"]["version"] = "MUTANT-VERSION"
                engine.emit("26", bundle, idx, ("analysis", "version"), m,
                            note="analysis-desynchronised")

        # ---- 27: omitted claim-reasoning verdict (D8 omission attack). Generated
        # only where the claim's ledger record is in the bundle: the derivation is
        # recomputed from the LEDGER claim's declared shape, so with no ledger the
        # omission is unverifiable and the mutant proves nothing (same guard
        # philosophy as family 5).
        if sname == "verdict-record.schema.json":
            claims_here27 = ledger_claims.get(inst.get("episode_id"), set())
            for ci, crp in enumerate(inst.get("claim_reasoning_paths", [])):
                if crp.get("claim_id") not in claims_here27:
                    continue
                for vi in range(len(crp.get("req_reason", []))):
                    m = copy.deepcopy(inst)
                    del m["claim_reasoning_paths"][ci]["req_reason"][vi]
                    engine.emit("27", bundle, idx,
                                ("claim_reasoning_paths", ci, "req_reason", vi), m,
                                note="-" + crp["req_reason"][vi])

        # ---- 17: collapse a candidate SET into one partial profile
        if sname == "orthing-episode.schema.json":
            prof = (inst.get("candidates") or {}).get("profile")
            if isinstance(prof, list) and prof:
                merged = {}
                for member in prof:
                    merged.update(member)
                m = copy.deepcopy(inst)
                m["candidates"]["profile"] = merged
                engine.emit("17", bundle, idx, ("candidates", "profile"), m,
                            note="set->single-partial-profile")
                m = copy.deepcopy(inst)
                m["candidates"]["profile"] = ["partial: %s" % sorted(merged)]
                engine.emit("17", bundle, idx, ("candidates", "profile"), m,
                            note="members->prose")


# ------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true",
                    help="list every survivor signature")
    ap.add_argument(
        "--write-adversarial-report",
        action="store_true",
        help="write the derived Task 14 report after every executable gate passes",
    )
    args = ap.parse_args()

    schemas, registry = load_schemas()
    ctx = Ctx(schemas, registry)

    spec_path = os.path.join(ROOT, "tests", "schema-mutations", "mutation-spec.json")
    spec = json.load(open(spec_path, encoding="utf-8"))
    equivalents = {e["signature"]: e["reason"] for e in spec.get("justified_equivalents", [])}
    task14_inventory_issues = audit_task14_spec(spec, ROOT)

    edir = os.path.join(ROOT, "examples")
    bundles = []
    for fn in sorted(os.listdir(edir)):
        if fn.endswith(".json"):
            ex = json.load(open(os.path.join(edir, fn), encoding="utf-8"))
            if ex.get("parts"):
                bundles.append(Bundle(fn, ex["parts"]))

    # the engine's premise: every unmutated bundle is issue-free, so any issue a
    # mutant raises is attributable to the mutation and to nothing else
    baseline_bad = [b.fn for b in bundles if collect_issues(b.parts)]
    if baseline_bad:
        print("FATAL: baseline bundles already carry semantic issues: %s" % baseline_bad)
        sys.exit(2)

    engine = Engine(ctx, bundles)
    for b in bundles:
        generate(engine, ctx, b)

    declared_ops = {o["id"] for o in spec.get("operators", [])}
    print("Recursive mutation report — %d example bundles, %d operator families"
          % (len(bundles), len(FAMILIES)))
    print("Kill criterion: rejected by the hardened JSON Schema, or flagged by "
          "validate_cross_record_semantics.")
    print("")
    print("%-4s %-46s %9s %8s %9s %10s" %
          ("fam", "operator family", "generated", "schema", "semantic", "survivors"))
    print("-" * 92)

    tot = {"generated": 0, "killed_schema": 0, "killed_semantic": 0, "survivors": 0}
    unjustified, justified, empty_families, undeclared = [], [], [], []
    for fid, name, desc in FAMILIES:
        r = engine.results[fid]
        surv = r["survivors"]
        just = [s for s in surv if s in equivalents]
        unj = [s for s in surv if s not in equivalents]
        justified += [(s, equivalents[s]) for s in just]
        unjustified += unj
        if r["generated"] == 0:
            empty_families.append("%s %s" % (fid, name))
        if name not in declared_ops:
            undeclared.append(name)
        print("%-4s %-46s %9d %8d %9d %10s" %
              (fid, name, r["generated"], r["killed_schema"], r["killed_semantic"],
               ("%d (%d justified)" % (len(surv), len(just))) if surv else "0"))
        tot["generated"] += r["generated"]
        tot["killed_schema"] += r["killed_schema"]
        tot["killed_semantic"] += r["killed_semantic"]
        tot["survivors"] += len(surv)
        if args.verbose and surv:
            for s in surv:
                print("        survivor: %s%s" % (s, "  [justified]" if s in equivalents else ""))
    print("-" * 92)
    print("%-4s %-46s %9d %8d %9d %10d" %
          ("", "TOTAL", tot["generated"], tot["killed_schema"], tot["killed_semantic"],
           tot["survivors"]))
    print("")
    print("Descriptions:")
    for fid, name, desc in FAMILIES:
        print("  %-3s %-46s %s" % (fid, name, desc))
    print("")

    if justified:
        print("Justified equivalent mutants (declared in mutation-spec.json, each with a reason "
              "why the mutation does not change what the record claims):")
        for sig, reason in justified:
            print("  - %s\n      %s" % (sig, reason))
        print("")

    fails = 0
    if empty_families:
        print("FAIL: operator families that generated no mutant at all (a family with nothing to "
              "bite is not evidence): %s" % empty_families)
        fails += 1
    if undeclared:
        print("FAIL: operator families missing from tests/schema-mutations/mutation-spec.json: %s"
              % sorted(set(undeclared)))
        fails += 1
    if unjustified:
        print("FAIL: %d UNJUSTIFIED surviving mutant(s) — accepted by both layers and not declared "
              "equivalent:" % len(unjustified))
        for s in unjustified:
            print("  - %s" % s)
        fails += 1

    task14_results = []
    task14_execution_issues = list(task14_inventory_issues)
    if not task14_inventory_issues:
        task14_results, task14_execution_issues = run_task14_attacks(spec, ROOT)
    if task14_execution_issues:
        print("FAIL: Task 14 mandatory attack program:")
        for issue in task14_execution_issues:
            print("  - %s" % issue)
        fails += 1
    else:
        unique_commands = {
            command
            for row in task14_results
            for command in (row["control_command"], row["mutation_command"])
        }
        print(
            "PASS: Task 14 accounted for %d explicit variants through %d separate "
            "control/mutation command(s)." % (len(task14_results), len(unique_commands))
        )

    report = render_task14_report(
        spec,
        task14_results,
        ROOT,
        recursive_totals={
            "families": len(FAMILIES),
            "generated": tot["generated"],
            "killed_schema": tot["killed_schema"],
            "killed_semantic": tot["killed_semantic"],
            "justified": len(justified),
            "unjustified": len(unjustified),
        },
    )
    report_path = pathlib.Path(ROOT) / TASK14_REPORT
    if args.write_adversarial_report and not fails:
        report_path.write_text(report, encoding="utf-8", newline="\n")
        print("WROTE: %s" % TASK14_REPORT)
    elif not args.write_adversarial_report:
        if not report_path.exists():
            print("FAIL: derived Task 14 report is missing: %s" % TASK14_REPORT)
            fails += 1
        elif report_path.read_text(encoding="utf-8") != report:
            print("FAIL: derived Task 14 report has drifted: %s" % TASK14_REPORT)
            fails += 1

    if not fails:
        print("PASS: every generated mutant is killed at a declared layer, or is declared "
              "equivalent with a stated reason.")
    print("TOTAL: %d failures" % fails)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
