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
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "tests" / "schema-mutations" / "mutation-spec.json"
OBSERVATION_SCHEMA = "orthemology-task14-observation-v1"


def load_variant(attack_id: str, variant_id: str) -> tuple[dict, dict]:
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
    return attacks[0], variants[0]


def observe(attack_id: str, variant_id: str, role: str) -> dict:
    attack, variant = load_variant(attack_id, variant_id)
    selector = variant[role + "_evidence_selector"]
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", selector, "-v"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        raise RuntimeError(
            "%s evidence selector failed with rc=%d%s"
            % (
                role,
                completed.returncode,
                ": " + detail[-1000:] if detail else "",
            )
        )
    validator_path = ROOT / variant["validator_entry_point"]
    return {
        "schema": OBSERVATION_SCHEMA,
        "attack_id": attack["attack_id"],
        "variant_id": variant["variant_id"],
        "mutation_id": variant["mutation_id"],
        "role": role,
        "validator_owner": variant["validator_owner"],
        "validator_entry_point": variant["validator_entry_point"],
        "validator_sha256": hashlib.sha256(validator_path.read_bytes()).hexdigest(),
        "evidence_selector": selector,
        "asserted_validator_outcome": (
            "accepted" if role == "control" else "rejected"
        ),
        "evidence_process_exit_code": completed.returncode,
        "exit_semantics": (
            "0 means the role-specific focused selector completed and its "
            "production-validator assertion passed; it is not the validator's "
            "own exit code"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--attack-id", required=True)
    parser.add_argument("--variant-id", required=True)
    parser.add_argument("--role", required=True, choices=("control", "mutation"))
    args = parser.parse_args()
    try:
        payload = observe(args.attack_id, args.variant_id, args.role)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
