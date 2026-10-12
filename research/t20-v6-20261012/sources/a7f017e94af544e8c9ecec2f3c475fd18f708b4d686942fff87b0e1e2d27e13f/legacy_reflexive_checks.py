#!/usr/bin/env python3
"""Bounded checks for Composition and Self-Revision.

This uses only Python's standard library.  It verifies finite examples and
small exhaustive model classes; it is not a proof-assistant formalisation,
independent review, novelty assessment, or empirical validation.

Usage: python verify_models.py --output verification.json
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import deque
from pathlib import Path
from typing import Iterable, Sequence

Bits = tuple[int, ...]


def require(condition: bool, message: str) -> None:
    """Do not use assert: checks must remain active under python -O."""
    if not condition:
        raise RuntimeError(message)


def projection(relation: Iterable[Bits], coordinates: Sequence[int]) -> set[Bits]:
    return {tuple(row[i] for i in coordinates) for row in relation}


def check_parity(max_n: int = 8) -> dict:
    results = []
    for n in range(3, max_n + 1):
        full = set(itertools.product((0, 1), repeat=n))
        relations = [set(), set()]
        # Generate by choosing n-1 free coordinates and completing the parity.
        for prefix in itertools.product((0, 1), repeat=n - 1):
            for sigma in (0, 1):
                relations[sigma].add(prefix + ((sum(prefix) + sigma) % 2,))
        require(relations[0].isdisjoint(relations[1]), f"n={n}: not disjoint")
        require(relations[0] | relations[1] == full, f"n={n}: union wrong")
        require(all(len(r) == 2 ** (n - 1) for r in relations), "wrong sizes")
        require(all(sum(x) % 2 == 0 for x in relations[0]), "even invariant fails")
        require(all(sum(x) % 2 == 1 for x in relations[1]), "odd invariant fails")
        subsystems = [j for k in range(1, n)
                      for j in itertools.combinations(range(n), k)]
        projections = [dict(), dict()]
        for j in subsystems:
            expected = set(itertools.product((0, 1), repeat=len(j)))
            for sigma in (0, 1):
                projections[sigma][j] = projection(relations[sigma], j)
                require(projections[sigma][j] == expected,
                        f"n={n}, J={j}, sigma={sigma}: projection wrong")
        for sigma in (0, 1):
            joined = {x for x in full if all(
                tuple(x[i] for i in j) in projections[sigma][j]
                for j in subsystems)}
            require(joined == full, "proper projection join not full product")
            require(relations[sigma] < joined, "join unexpectedly lossless")
        results.append({"n": n, "states_per_relation": len(relations[0]),
                        "proper_nonempty_coordinate_subsets": len(subsystems),
                        "projection_equalities_checked": len(subsystems),
                        "both_joins_equal_full_product": True})
    return {"status": "PASS", "scope": "n=3 through n=8; all nonempty proper coordinate projections",
            "cases": results}



def check_lossless_restriction() -> dict:
    """All nonempty relations on a binary triple, including negative controls."""
    full = tuple(itertools.product((0, 1), repeat=3))
    coordinate_sets = [j for k in (1, 2) for j in itertools.combinations(range(3), k)]
    classes: dict[tuple, list[set[Bits]]] = {}
    lossless_classes: dict[tuple, list[set[Bits]]] = {}
    for mask in range(1, 1 << len(full)):
        relation = {x for i, x in enumerate(full) if mask & (1 << i)}
        projected = [projection(relation, j) for j in coordinate_sets]
        key = tuple(tuple(sorted(p)) for p in projected)
        classes.setdefault(key, []).append(relation)
        joined = {x for x in full if all(
            tuple(x[i] for i in j) in p
            for j, p in zip(coordinate_sets, projected))}
        if joined == relation:
            lossless_classes.setdefault(key, []).append(relation)
    require(sum(len(v) for v in classes.values()) == 255, "missing relation")
    require(all(len(v) == 1 for v in lossless_classes.values()),
            "record fails to identify relation in independently restricted lossless class")
    # The unrestricted record may also describe lossy relations.  Therefore its
    # sufficiency cannot itself establish that the restriction holds.
    ambiguous = sum(len(v) > 1 for v in classes.values())
    require(ambiguous > 0, "unrestricted negative control disappeared")
    even = {x for x in full if sum(x) % 2 == 0}
    even_key = tuple(tuple(sorted(projection(even, j))) for j in coordinate_sets)
    full_key = tuple(tuple(sorted(projection(set(full), j))) for j in coordinate_sets)
    require(even_key == full_key, "lossless-restriction negative control failed")
    return {"status": "PASS", "relations_examined": 255,
            "proper_projection_record_classes": len(classes),
            "ambiguous_unrestricted_record_classes": ambiguous,
            "lossless_relations": sum(len(v) for v in lossless_classes.values()),
            "records_identify_relations_within_lossless_class": True,
            "full_product_and_even_parity_have_same_record": True,
            "scope": "all 255 nonempty relations on three binary coordinates"}


def partitions(m: int) -> Iterable[tuple[int, ...]]:
    """All set partitions of {0,...,m-1} as restricted-growth label vectors."""
    def grow(prefix: tuple[int, ...]):
        if len(prefix) == m:
            yield prefix
            return
        for next_label in range(max(prefix) + 2):
            yield from grow(prefix + (next_label,))
    if m < 1:
        raise ValueError("m must be positive")
    yield from grow((0,))


def constant_on_fibres(record: Sequence[int], values: Sequence[int]) -> bool:
    return all(record[i] != record[j] or values[i] == values[j]
               for i in range(len(record)) for j in range(len(record)))


def check_factorisation() -> dict:
    n_records = n_predicates = true_cases = 0
    details = []
    for m in range(1, 5):
        records = list(partitions(m))
        require(len(set(records)) == len(records), "duplicate partition")
        require(len(records) == (1, 2, 5, 15)[m - 1], "partition generator incomplete")
        case_count = 0
        for record in records:
            n_records += 1
            k = max(record) + 1
            # Independent finite lookup enumeration: no appeal to the criterion.
            possible_outputs = {tuple(f[label] for label in record)
                                for f in itertools.product((0, 1), repeat=k)}
            for target in itertools.product((0, 1), repeat=m):
                fibre_constancy = constant_on_fibres(record, target)
                lookup_exists = target in possible_outputs
                require(fibre_constancy == lookup_exists, "factorisation equivalence failed")
                n_predicates += 1
                case_count += 1
                true_cases += int(fibre_constancy)
        details.append({"state_count": m, "partitions": len(records),
                        "predicate_record_pairs": case_count})
    return {"status": "PASS", "record_partitions": n_records,
            "predicate_record_pairs": n_predicates, "factorisable_pairs": true_cases,
            "scope": "all partitions and Boolean predicates on 1 through 4 states",
            "cases": details}


def congruent(labels: Sequence[int], action: Sequence[int]) -> bool:
    return all(labels[w] != labels[v] or labels[action[w]] == labels[action[v]]
               for w in range(len(labels)) for v in range(len(labels)))


def check_action_congruence() -> dict:
    records = maps_examined = congruent_maps = checked_reachable_pairs = 0
    negative_controls = 0
    details = []
    for m in range(1, 5):
        maps = list(itertools.product(range(m), repeat=m))
        require(len(maps) == m ** m, "action enumeration incomplete")
        for labels in partitions(m):
            records += 1
            maps_examined += len(maps)
            allowed = [a for a in maps if congruent(labels, a)]
            congruent_maps += len(allowed)
            equivalent = {(w, v) for w in range(m) for v in range(m)
                          if labels[w] == labels[v]}
            # Reachability under every congruent action, not just a fixed depth.
            # Closure of this finite pair graph covers action strings of any length
            # for this bounded state space and action repertoire.
            reached = set(equivalent)
            queue = deque(equivalent)
            while queue:
                w, v = queue.popleft()
                require(labels[w] == labels[v], "observational distinction appeared")
                for a in allowed:
                    successor = (a[w], a[v])
                    if successor not in reached:
                        reached.add(successor)
                        queue.append(successor)
            require(reached <= equivalent, "congruence closure failed")
            checked_reachable_pairs += len(reached)
            bad_maps = [a for a in maps if not congruent(labels, a)]
            if bad_maps:
                witness = next(((a, w, v) for a in bad_maps
                                for w, v in equivalent
                                if labels[a[w]] != labels[a[v]]), None)
                require(witness is not None, "no separating negative control")
                negative_controls += 1
            details.append({"states": m, "record_partition": list(labels),
                            "actions_examined": len(maps), "congruent_actions": len(allowed),
                            "closed_equivalent_pairs": len(reached),
                            "noncongruent_action_witness_exists": bool(bad_maps)})
    return {"status": "PASS", "partitions": records,
            "partition_action_pairs_examined": maps_examined,
            "congruent_partition_action_pairs": congruent_maps,
            "equivalent_pairs_in_closed_graphs": checked_reachable_pairs,
            "separating_negative_controls": negative_controls,
            "scope": "all observation partitions and all total actions on 1 through 4 states; pair-graph closure",
            "limit": "The general adaptive-controller theorem is justified by the manuscript's induction, not by these finite checks.",
            "cases": details}


def check_self_reconnection() -> dict:
    states = list(itertools.product((0, 1), repeat=2))
    observe = lambda w: (w[0], w[0] * w[1])
    reconnect = lambda w: (1, w[1])
    rows = [{"state": list(w), "observation": list(observe(w)),
             "after_reconnection": list(reconnect(w)),
             "after_observation": list(observe(reconnect(w)))} for w in states]
    require(observe((0, 0)) == observe((0, 1)), "initial uncertainty absent")
    require(observe(reconnect((0, 0))) != observe(reconnect((0, 1))), "no separation after action")
    require(all(reconnect(w)[1] == w[1] for w in states), "external bit changed")
    capability = [int(observe((s, 0)) != observe((s, 1))) for s in (0, 1)]
    require(capability == [0, 1], "capability result incorrect")
    # Exposing only the connection setting does NOT reveal b, before or after u.
    observe_setting_only = lambda w: w[0]
    require(observe_setting_only(reconnect((0, 0))) == observe_setting_only(reconnect((0, 1))),
            "connection readback confused with external response")
    # Uniform repair can establish a post-state property without diagnosing b.
    require(all(reconnect(w)[0] == 1 for w in states), "uniform repair failed")
    return {"status": "PASS", "states": rows, "capability_before_after": capability,
            "stable_external_bit": True, "same_action_in_both_initial_cases": True,
            "congruence_break_witness": [[0, 0], [0, 1]],
            "setting_only_readback_does_not_identify_external_bit": True,
            "uniform_repair_does_not_require_prior_diagnosis": True,
            "scope": "the four-state deterministic construction only"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("verification.json"))
    args = parser.parse_args()
    result = {
        "document": "Composition and Self-Revision: Global Properties, Evidence, and Open Systems",
        "verification_kind": "bounded exhaustive model checks and construction checks",
        "overall_status": "PASS",
        "not_claimed": ["proof-assistant certification", "independent peer review", "novelty or priority",
                        "empirical validation", "universal effectiveness of a self-revising system"],
        "higher_order_relations": check_parity(),
        "factorisation": check_factorisation(),
        "lossless_restriction": check_lossless_restriction(),
        "action_congruence": check_action_congruence(),
        "self_reconnection": check_self_reconnection(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: (v.get("status") if isinstance(v, dict) else v)
                      for k, v in result.items() if k not in ("not_claimed",)}, indent=2))


if __name__ == "__main__":
    main()
