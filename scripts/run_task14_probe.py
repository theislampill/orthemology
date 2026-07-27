#!/usr/bin/env python3
"""Emit one machine-readable Task 14 control or mutation observation.

The inventory binds each probe to an existing focused test that calls the
declared production validator.  This wrapper keeps the control and mutation
processes separate and never converts an arbitrary successful command into
both semantic outcomes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

try:
    from scripts.task14_probe_registry import load_registry
    from scripts.task14_direct_probes import execute_direct_probe
except ModuleNotFoundError:
    from task14_probe_registry import load_registry
    from task14_direct_probes import execute_direct_probe

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SPEC_PATH = ROOT / "tests" / "schema-mutations" / "mutation-spec.json"
OBSERVATION_SCHEMA = "orthemology-task14-observation-v1"


def load_variant(attack_id: str, variant_id: str):
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    attacks = [
        row
        for row in spec.get("mandatory_attacks", [])
        if isinstance(row, dict) and row.get("attack_id") == attack_id
    ]
    if len(attacks) != 1:
        raise ValueError("attack identity does not resolve exactly once")
    variants = [
        row
        for row in attacks[0].get("variants", [])
        if isinstance(row, dict) and row.get("variant_id") == variant_id
    ]
    if len(variants) != 1:
        raise ValueError("variant identity does not resolve exactly once")
    registry = load_registry(ROOT)
    binding = registry.get((attack_id, variant_id))
    if binding is None:
        raise ValueError("variant has no closed direct-probe binding")
    return attacks[0], variants[0], binding


def _observation_id(identity: dict, outcome: str, input_sha256: str) -> str:
    canonical = json.dumps(
        {
            **identity,
            "observed_validator_outcome": outcome,
            "input_sha256": input_sha256,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def observe(attack_id: str, variant_id: str, role: str, executor=execute_direct_probe) -> dict:
    attack, variant, binding = load_variant(attack_id, variant_id)
    del attack
    if role not in {"control", "mutation"}:
        raise ValueError("invalid direct-probe role")
    selector = getattr(binding, role + "_evidence_selector")
    validator_path = ROOT / binding.validator_entry_point
    direct = executor(binding, role)
    outcome = direct.get("outcome")
    input_sha256 = direct.get("input_sha256")
    identity = {
        "attack_id": binding.attack_id,
        "variant_id": binding.variant_id,
        "mutation_id": binding.mutation_id,
        "role": role,
        "evidence_selector": selector,
        "validator_owner": binding.validator_owner,
        "validator_entry_point": binding.validator_entry_point,
        "validator_sha256": hashlib.sha256(validator_path.read_bytes()).hexdigest(),
    }
    payload = {
        "schema": OBSERVATION_SCHEMA,
        **identity,
        "observed_validator_outcome": outcome,
        "evidence_process_exit_code": 0,
        "exit_semantics": (
            "0 means direct probe execution succeeded; validator acceptance "
            "or rejection is carried only by observed_validator_outcome"
        ),
        "input_sha256": input_sha256,
    }
    payload["observation_id"] = _observation_id(identity, outcome, input_sha256)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--attack-id", required=True)
    parser.add_argument("--variant-id", required=True)
    parser.add_argument("--role", required=True, choices=("control", "mutation"))
    args = parser.parse_args()
    try:
        payload = observe(args.attack_id, args.variant_id, args.role)
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
