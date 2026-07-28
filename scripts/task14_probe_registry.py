#!/usr/bin/env python3
"""Closed identity anchor for the 77 Task 14 direct probes.

The mutable JSON inventory is accepted only when its complete identity,
ownership, entry-point, and role-specific evidence projection matches this
independently committed digest.  The digest therefore anchors every binding,
not merely the number or names of variants.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import pathlib


REGISTRY_PROJECTION_SHA256 = (
    "229e23d6edc5f4a1853bff571fc848f804d485284ced23aed5d91e091a9dee43"
)


@dataclasses.dataclass(frozen=True)
class ProbeBinding:
    attack_id: str
    variant_id: str
    mutation_id: str
    owner: str
    validator_owner: str
    validator_entry_point: str
    control_evidence_selector: str
    mutation_evidence_selector: str


def _projection(spec: dict) -> list[dict]:
    return [
        {
            "attack_id": attack["attack_id"],
            "variant_id": variant["variant_id"],
            "mutation_id": variant["mutation_id"],
            "owner": attack["owner"],
            "validator_owner": variant["validator_owner"],
            "validator_entry_point": variant["validator_entry_point"],
            "control_evidence_selector": variant["control_evidence_selector"],
            "mutation_evidence_selector": variant["mutation_evidence_selector"],
        }
        for attack in spec["mandatory_attacks"]
        for variant in attack["variants"]
    ]


def load_registry(root: pathlib.Path) -> dict[tuple[str, str], ProbeBinding]:
    spec_path = pathlib.Path(root) / "tests" / "schema-mutations" / "mutation-spec.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    rows = _projection(spec)
    canonical = json.dumps(
        rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    observed = hashlib.sha256(canonical).hexdigest()
    if observed != REGISTRY_PROJECTION_SHA256:
        raise ValueError(
            "Task 14 closed probe registry drifted: expected %s, observed %s"
            % (REGISTRY_PROJECTION_SHA256, observed)
        )
    bindings = {
        (row["attack_id"], row["variant_id"]): ProbeBinding(**row) for row in rows
    }
    if len(rows) != 77 or len(bindings) != 77:
        raise ValueError("Task 14 closed probe registry must contain 77 unique bindings")
    return bindings
