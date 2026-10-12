#!/usr/bin/env python3
"""Finite counterexample checks for The Properties of a Composition.

These exhaustive checks cover the finite domains declared below. They are not a
formal verification of the general proofs or evidence of physical applicability.
Python 3.10+; standard library only. No network or input-file modifications.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def union_masks(masks: Iterable[int]) -> int:
    result = 0
    for mask in masks:
        result |= mask
    return result


def check_domain(dimensions: tuple[int, ...]) -> dict[str, object]:
    """Enumerate every relation, covering scope family, and Boolean predicate."""
    n = len(dimensions)
    states = tuple(itertools.product(*(range(d) for d in dimensions)))
    size = len(states)
    full = (1 << size) - 1
    relations = range(1, full + 1)
    scopes = tuple(
        tuple(i for i in range(n) if scope_bits & (1 << i))
        for scope_bits in range(1, 1 << n)
    )
    # Projection identities are computed directly from the tuples, independently
    # of the natural-join criterion or the conclusions under test.
    local_maps: list[tuple[int, ...]] = []
    projections: list[list[int]] = []
    for scope in scopes:
        local_states = tuple(itertools.product(*(range(dimensions[i]) for i in scope)))
        index = {value: i for i, value in enumerate(local_states)}
        mapping = tuple(index[tuple(x[i] for i in scope)] for x in states)
        local_maps.append(mapping)
        table = [0] * (full + 1)
        for relation in relations:
            low_bit = relation & -relation
            x_index = low_bit.bit_length() - 1
            table[relation] = table[relation ^ low_bit] | (1 << mapping[x_index])
        projections.append(table)

    covers = 0
    families = 0
    predicate_checks = 0
    composition_checks = 0
    unique_families = 0
    for cover_bits in range(1, 1 << len(scopes)):
        scope_ids = tuple(i for i in range(len(scopes)) if cover_bits & (1 << i))
        if set().union(*(set(scopes[i]) for i in scope_ids)) != set(range(n)):
            continue
        covers += 1
        by_local: dict[tuple[int, ...], list[int]] = {}
        for relation in relations:
            signature = tuple(projections[s][relation] for s in scope_ids)
            by_local.setdefault(signature, []).append(relation)
        for signature, compatible in by_local.items():
            families += 1
            # Direct implementation of equation (3), not the union of candidate
            # relations (the latter is checked separately).
            join = union_masks(
                1 << x_index
                for x_index in range(size)
                if all(
                    signature[j] & (1 << local_maps[s][x_index])
                    for j, s in enumerate(scope_ids)
                )
            )
            context = f"dimensions={dimensions}, scopes={scope_ids}, R={signature}"
            require(join in compatible, f"Join is not compatible: {context}")
            require(join == union_masks(compatible), f"Join not greatest: {context}")
            require(
                tuple(projections[s][join] for s in scope_ids) == signature,
                f"Join fails exact projection: {context}",
            )
            for truth_set in range(full + 1):
                predicate_checks += 1
                good = join & truth_set
                possible_by_criterion = all(
                    projections[s][good] == signature[j]
                    for j, s in enumerate(scope_ids)
                )
                possible_by_enumeration = any(k & truth_set == k for k in compatible)
                require(
                    possible_by_criterion == possible_by_enumeration,
                    f"Theorem 1 existence: {context}, p={truth_set}",
                )
                if possible_by_criterion:
                    require(good in compatible, f"Greatest good relation missing: {context}")
                    require(
                        all(k & good == k for k in compatible if k & truth_set == k),
                        f"Greatest-good maximality: {context}",
                    )
                warranted_by_criterion = join & truth_set == join
                warranted_by_enumeration = all(k & truth_set == k for k in compatible)
                require(
                    warranted_by_criterion == warranted_by_enumeration,
                    f"Theorem 1 warrant: {context}, p={truth_set}",
                )
                if not possible_by_criterion:
                    require(
                        all(k & (full ^ truth_set) for k in compatible),
                        f"Failure-of-possibility quantifier: {context}, p={truth_set}",
                    )
            has_forced_completion = True
            for x_index in range(size):
                if not join & (1 << x_index):
                    continue
                singleton_witness = any(
                    sum(
                        bool(join & (1 << y_index))
                        and local_maps[s][y_index] == local_maps[s][x_index]
                        for y_index in range(size)
                    ) == 1
                    for s in scope_ids
                )
                if not singleton_witness:
                    has_forced_completion = False
                    require(
                        join ^ (1 << x_index) in compatible,
                        f"Proposition 3 deletion witness: {context}",
                    )
            require(
                has_forced_completion == (len(compatible) == 1),
                f"Proposition 3 uniqueness: {context}",
            )
            unique_families += len(compatible) == 1
            for k in compatible:
                composition_checks += 1
                # Directly enumerate theories as truth sets, not merely count
                # their sizes. This checks both inclusion and strictness.
                theory_k = {p for p in range(full + 1) if k & p == k}
                theory_j = {p for p in range(full + 1) if join & p == join}
                require(theory_j <= theory_k, f"Equation (7) inclusion: {context}")
                require(
                    (theory_j < theory_k) == (k != join),
                    f"Equation (7) strictness: {context}",
                )
    return {
        "dimensions": list(dimensions),
        "joint_configurations": size,
        "nonempty_relations": full,
        "covering_scope_families": covers,
        "distinct_consistent_local_families_across_covers": families,
        "local_family_predicate_combinations": predicate_checks,
        "composition_theory_combinations": composition_checks,
        "uniquely_determined_local_families": unique_families,
        "status": "PASS",
    }


def check_consistency() -> dict[str, object]:
    """All nonempty singleton/pair descriptions on three binary coordinates."""
    n = 3
    states = tuple(itertools.product((0, 1), repeat=n))
    scopes = ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2))
    maps = [tuple(tuple(x[i] for i in s) for x in states) for s in scopes]
    options = []
    for scope in scopes:
        tuples = tuple(itertools.product((0, 1), repeat=len(scope)))
        options.append(tuple(
            frozenset(tuples[i] for i in range(len(tuples)) if mask & (1 << i))
            for mask in range(1, 1 << len(tuples))
        ))
    possible_signatures = set()
    for mask in range(1, 1 << len(states)):
        possible_signatures.add(tuple(
            frozenset(mapping[i] for i in range(len(states)) if mask & (1 << i))
            for mapping in maps
        ))
    checked = 0
    consistent = 0
    for descriptions in itertools.product(*options):
        checked += 1
        join = tuple(
            i for i in range(len(states))
            if all(maps[s][i] in descriptions[s] for s in range(len(scopes)))
        )
        by_join = bool(join) and all(
            frozenset(maps[s][i] for i in join) == descriptions[s]
            for s in range(len(scopes))
        )
        by_enumeration = descriptions in possible_signatures
        require(by_join == by_enumeration, "Section 1 consistency equivalence failed")
        consistent += by_enumeration
    return {"local_families": checked, "consistent": consistent,
            "inconsistent": checked - consistent, "status": "PASS"}


def check_parity() -> dict[str, object]:
    cases = []
    for n in range(2, 9):
        states = tuple(itertools.product((0, 1), repeat=n))
        relations = tuple(
            tuple(x for x in states if sum(x) % 2 == b) for b in (0, 1)
        )
        require(set(relations[0]).isdisjoint(relations[1]), "Parity relations overlap")
        require(all(len(k) == 2 ** (n - 1) for k in relations), "Wrong parity population")
        for scope_bits in range((1 << n) - 1):
            scope = tuple(i for i in range(n) if scope_bits & (1 << i))
            expected = set(itertools.product((0, 1), repeat=len(scope)))
            for k in relations:
                observed = {tuple(x[i] for i in scope) for x in k}
                require(observed == expected, f"Parity projection failed for n={n}, S={scope}")
        cases.append({"components": n, "proper_scopes": (1 << n) - 1,
                      "configurations_per_parity_relation": 2 ** (n - 1)})
    return {"cases": cases, "status": "PASS"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write the exact result JSON to this path")
    args = parser.parse_args()
    result = {
        "schema": "composition-paper-finite-checks-v1",
        "scope_limit": (
            "Exhaustive checks only over the declared finite models; not a formal proof "
            "of the general results, peer review, or validation of a physical/metaphysical application."
        ),
        "domains": [check_domain((2, 2)), check_domain((2, 3)), check_domain((2, 2, 2))],
        "consistency": check_consistency(),
        "parity": check_parity(),
        "status": "PASS",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
