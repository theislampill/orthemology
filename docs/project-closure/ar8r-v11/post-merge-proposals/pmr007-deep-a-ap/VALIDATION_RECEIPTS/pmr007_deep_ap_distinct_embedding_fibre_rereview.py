#!/usr/bin/env python3
"""Distinct rereview for PMR-007-SWRI-1 V2.

Uses injective source/world embeddings rather than the primary unrestricted
homomorphism family, random independently restricted map families, frozen-hash
verification, and exact translated-source anchors.
"""
from __future__ import annotations

from hashlib import sha256
from itertools import permutations, product
import json
import os
from pathlib import Path
import random

ROLES = 2
SOURCE = (0, 1)
WORLD = (0, 1, 2, 3)
SOURCE_SIG = {0: (1, 1), 1: (1, 0)}


def preserves(mapping, world_sig):
    return all(
        not SOURCE_SIG[s][r] or world_sig[mapping[s]][r]
        for s in SOURCE
        for r in range(ROLES)
    )


def injective_maps():
    return list(permutations(WORLD, len(SOURCE)))


def role_bearers(world_sig):
    return {w for w in WORLD if all(world_sig[w])}


def verify_frozen_hashes(base: Path):
    receipt = base / "PMR-007_DEEP_AP_V2_FROZEN_HASHES.sha256"
    failures = []
    rows = 0
    for line in receipt.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line.split("  ", 1)
        actual = sha256((base / rel).read_bytes()).hexdigest()
        rows += 1
        if actual != expected:
            failures.append({"file": rel, "expected": expected, "actual": actual})
    return {"rows": rows, "failures": failures, "status": "PASS" if not failures else "FAIL"}


def source_check():
    path_text = os.environ.get("AR8R_ASFAHANI_MD")
    if not path_text:
        return {"status": "NOT_RUN_MISSING_AR8R_ASFAHANI_MD"}
    path = Path(path_text)
    text = path.read_text(encoding="utf-8")
    anchors = [
        "The cosmos has an essentially necessary being",
        "He is one",
        "knowing",
        "able",
        "living",
        "possessing volition",
        "speaking",
        "is all undoubtedly true",
        "The titles al-murīd and al-mutakallim are not divine names, but attributes",
    ]
    missing = [anchor for anchor in anchors if anchor not in text]
    return {
        "status": "PASS" if not missing else "FAIL",
        "sha256": sha256(path.read_bytes()).hexdigest(),
        "anchors_checked": len(anchors),
        "anchors_missing": missing,
        "authority": "TRANSLATED_PRIMARY_ACCESS_NOT_ARABIC_PRIMARY_VERIFICATION",
    }


def main():
    base = Path(__file__).resolve().parents[1]
    maps = injective_maps()
    counts = {
        "world_signatures": 0,
        "nonempty_embedding_families": 0,
        "role_complete_embedding_cases": 0,
        "conditional_existence_failures": 0,
        "role_complete_fibre_failures": 0,
        "role_complete_uniqueness_failures": 0,
        "random_restricted_H_cases": 0,
        "singleton_definition_failures": 0,
        "hidden_anchor_witnesses": 0,
        "multiple_candidate_world_witnesses": 0,
    }
    rng = random.Random(7007)

    for bits in product((0, 1), repeat=len(WORLD) * ROLES):
        world_sig = {
            w: tuple(bits[w * ROLES:(w + 1) * ROLES])
            for w in WORLD
        }
        counts["world_signatures"] += 1
        valid = [m for m in maps if preserves(m, world_sig)]
        bearers = role_bearers(world_sig)
        fibre = {m[0] for m in valid}
        if valid:
            counts["nonempty_embedding_families"] += 1
            if not fibre or not fibre.issubset(bearers):
                counts["conditional_existence_failures"] += 1
        role_complete = all(any(m[0] == w for m in valid) for w in bearers)
        if valid and role_complete:
            counts["role_complete_embedding_cases"] += 1
            if fibre != bearers:
                counts["role_complete_fibre_failures"] += 1
            if (len(fibre) == 1) != (len(bearers) == 1):
                counts["role_complete_uniqueness_failures"] += 1

        # Independently restricted map families: exact singleton criterion is
        # definitional, while hidden-anchor witnesses are explicitly exercised.
        if valid:
            for _ in range(8):
                chosen = [m for m in valid if rng.random() < 0.45]
                if not chosen:
                    chosen = [rng.choice(valid)]
                counts["random_restricted_H_cases"] += 1
                candidate_fibre = {m[0] for m in chosen}
                if (len(candidate_fibre) == 1) != (len({m[0] for m in chosen}) == 1):
                    counts["singleton_definition_failures"] += 1
                if len(bearers) >= 2 and len(candidate_fibre) == 1:
                    counts["hidden_anchor_witnesses"] += 1

        if len(bearers) >= 2:
            counts["multiple_candidate_world_witnesses"] += 1

    # Two candidate worlds, each internally unique but with different bearers,
    # demonstrate that within-world uniqueness does not select the actual world.
    world_a = {0: (1, 1), 1: (1, 0), 2: (0, 1), 3: (0, 0)}
    world_b = {0: (1, 0), 1: (1, 1), 2: (0, 1), 3: (0, 0)}
    multiple_world_control = (
        len(role_bearers(world_a)) == 1
        and len(role_bearers(world_b)) == 1
        and role_bearers(world_a) != role_bearers(world_b)
    )

    hashes = verify_frozen_hashes(base)
    source = source_check()
    claims = {
        "frozen_hashes_match": hashes["status"] == "PASS",
        "translated_source_anchors_match": source["status"] == "PASS",
        "nonempty_role_preserving_embeddings_have_candidate_role_bearer": counts["conditional_existence_failures"] == 0,
        "role_complete_embedding_fibre_equals_role_bearers": counts["role_complete_fibre_failures"] == 0,
        "role_complete_unique_iff_unique_role_bearer": counts["role_complete_uniqueness_failures"] == 0,
        "singleton_fibre_criterion_exact_for_restricted_H": counts["singleton_definition_failures"] == 0,
        "hidden_anchor_countermodels_exercised": counts["hidden_anchor_witnesses"] > 0,
        "multiple_world_nonselection_control": multiple_world_control,
    }
    result = {
        "schema": "PMR007_DEEP_AP_DISTINCT_EMBEDDING_FIBRE_REREVIEW_RESULTS_V1",
        "method_relation": "injective_embedding_and_random_map_family_implementation",
        "counts": counts,
        "frozen_hashes": hashes,
        "source_anchor_check": source,
        "multiple_world_control": multiple_world_control,
        "claims": claims,
        "scope_notes": [
            "finite candidate source/world structures",
            "relative denotation only",
            "role preservation not full reflection",
            "translated-primary access only",
            "same-program procedural rereview; not external review",
        ],
        "overall": "PASS" if all(claims.values()) else "FAIL",
    }
    out = Path(__file__).with_name(Path(__file__).stem + "_results.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
