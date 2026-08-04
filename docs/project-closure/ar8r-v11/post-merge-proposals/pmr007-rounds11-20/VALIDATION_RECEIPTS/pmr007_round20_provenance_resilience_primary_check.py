from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import FrozenSet, Iterable, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "pmr007_round20_provenance_resilience_primary_check_results.json"

@dataclass(frozen=True)
class Action:
    blocks: FrozenSet[int]
    roots: FrozenSet[int]


def powerset(items: Sequence[int]) -> Iterable[FrozenSet[int]]:
    for r in range(len(items) + 1):
        for c in itertools.combinations(items, r):
            yield frozenset(c)


def tau(root_universe: Sequence[int], family: Sequence[FrozenSet[int]]) -> float:
    """Minimum hitting-set size; tau(empty family)=0, empty edge => infinity."""
    if not family:
        return 0
    if any(len(edge) == 0 for edge in family):
        return math.inf
    for r in range(len(root_universe) + 1):
        for c in itertools.combinations(root_universe, r):
            s = frozenset(c)
            if all(s & edge for edge in family):
                return r
    raise AssertionError("finite nonempty edge family must have a transversal")


def kappa(root_universe: Sequence[int], path_count: int, actions: Sequence[Action]) -> float:
    vals = []
    for p in range(path_count):
        fam = [a.roots for a in actions if p in a.blocks]
        vals.append(tau(root_universe, fam))
    return min(vals)


def survives(root_universe: Sequence[int], path_count: int, actions: Sequence[Action], F: FrozenSet[int]) -> bool:
    # Conjunctive dependency semantics: any corrupted required root disables action.
    for p in range(path_count):
        if not any(p in a.blocks and not (F & a.roots) for a in actions):
            return False
    return True


def f_robust(root_universe: Sequence[int], path_count: int, actions: Sequence[Action], f: int) -> bool:
    for F in powerset(root_universe):
        if len(F) <= f and not survives(root_universe, path_count, actions, F):
            return False
    return True


def theorem_holds(root_universe: Sequence[int], path_count: int, actions: Sequence[Action], f: int) -> bool:
    return f_robust(root_universe, path_count, actions, f) == (kappa(root_universe, path_count, actions) > f)


def canonicalize_actions(actions: Sequence[Action]) -> Tuple[Tuple[Tuple[int, ...], Tuple[int, ...]], ...]:
    return tuple(sorted((tuple(sorted(a.blocks)), tuple(sorted(a.roots))) for a in actions))


def exhaustive_single_path() -> dict:
    checked = 0
    mismatches = []
    duplicate_failures = []
    enlargement_failures = []
    deletion_failures = []
    contraction_failures = []

    for r in range(1, 5):
        roots = tuple(range(r))
        all_edges = list(powerset(roots))
        # Exhaust all blocker families of size <=4; enough to include empty edge and duplicates separately.
        for size in range(0, min(4, len(all_edges)) + 1):
            for family_tuple in itertools.combinations(all_edges, size):
                actions = [Action(frozenset({0}), e) for e in family_tuple]
                for f in range(r + 1):
                    checked += 1
                    if not theorem_holds(roots, 1, actions, f):
                        mismatches.append({"r": r, "family": [sorted(e) for e in family_tuple], "f": f})
                        if len(mismatches) >= 10:
                            return locals()

                # Copied action does not change kappa/direct robustness.
                if actions:
                    dup = actions + [actions[0]]
                    if kappa(roots, 1, dup) != kappa(roots, 1, actions):
                        duplicate_failures.append({"r": r, "family": [sorted(e) for e in family_tuple]})

                # Adding a blocker cannot lower kappa; deleting cannot raise it.
                unused = [e for e in all_edges if e not in family_tuple]
                if unused:
                    enlarged = actions + [Action(frozenset({0}), unused[0])]
                    if kappa(roots, 1, enlarged) < kappa(roots, 1, actions):
                        enlargement_failures.append({"r": r, "family": [sorted(e) for e in family_tuple], "added": sorted(unused[0])})
                if actions:
                    deleted = actions[1:]
                    if kappa(roots, 1, deleted) > kappa(roots, 1, actions):
                        deletion_failures.append({"r": r, "family": [sorted(e) for e in family_tuple]})

                # Contract roots 0 and 1 when possible; tau may not increase.
                if r >= 2:
                    def h(x: int) -> int:
                        return 0 if x in (0, 1) else x - 1
                    new_roots = tuple(range(r - 1))
                    contracted_actions = [Action(a.blocks, frozenset(h(x) for x in a.roots)) for a in actions]
                    if kappa(new_roots, 1, contracted_actions) > kappa(roots, 1, actions):
                        contraction_failures.append({"r": r, "family": [sorted(e) for e in family_tuple]})
    return {
        "checked": checked,
        "mismatches": mismatches,
        "duplicate_failures": duplicate_failures,
        "enlargement_failures": enlargement_failures,
        "deletion_failures": deletion_failures,
        "contraction_failures": contraction_failures,
    }


def random_multi_path(seed: int = 20032026, trials: int = 100_000) -> dict:
    rng = random.Random(seed)
    mismatches = []
    counts = {"trials": 0, "f_cases": 0}
    for _ in range(trials):
        r = rng.randint(1, 6)
        p = rng.randint(1, 4)
        roots = tuple(range(r))
        actions = []
        for _j in range(rng.randint(0, 9)):
            blocks = frozenset(i for i in range(p) if rng.random() < 0.5)
            if not blocks:
                blocks = frozenset({rng.randrange(p)})
            rootset = frozenset(i for i in range(r) if rng.random() < 0.42)
            actions.append(Action(blocks, rootset))
        counts["trials"] += 1
        for f in range(r + 1):
            counts["f_cases"] += 1
            if not theorem_holds(roots, p, actions, f):
                mismatches.append({
                    "roots": r,
                    "paths": p,
                    "actions": canonicalize_actions(actions),
                    "f": f,
                    "kappa": kappa(roots, p, actions),
                    "direct": f_robust(roots, p, actions, f),
                })
                if len(mismatches) >= 10:
                    return {**counts, "mismatches": mismatches}
    return {**counts, "mismatches": mismatches}


def required_witnesses() -> dict:
    # Positive independent-root construction.
    roots = (0, 1, 2)
    actions = [
        Action(frozenset({0}), frozenset({0})),
        Action(frozenset({0}), frozenset({1})),
        Action(frozenset({1}), frozenset({1})),
        Action(frozenset({1}), frozenset({2})),
    ]
    positive = {
        "kappa": kappa(roots, 2, actions),
        "f1_robust": f_robust(roots, 2, actions, 1),
        "f2_robust": f_robust(roots, 2, actions, 2),
    }

    # Copied-root and common-bottleneck.
    copied = [Action(frozenset({0}), frozenset({0})) for _ in range(8)]
    bottleneck = [Action(frozenset({0}), frozenset({0, j})) for j in (1, 2, 3)]

    # Alternative redundant-support semantics: action disabled only when every support root is corrupted.
    alt_roots = (0, 1)
    alt_action = Action(frozenset({0}), frozenset({0, 1}))
    transversal_prediction = kappa(alt_roots, 1, [alt_action]) > 1
    redundant_support_direct = all(
        not (alt_action.roots <= F) for F in powerset(alt_roots) if len(F) <= 1
    )

    # Compatibility failure at f=0: pathwise certificate passes, joint execution impossible.
    incompatible_actions = [
        Action(frozenset({0}), frozenset({0})),
        Action(frozenset({1}), frozenset({1})),
    ]
    pathwise = f_robust((0, 1), 2, incompatible_actions, 0)
    jointly_executable = False

    # Dynamic rerouting and partial path registry are explicit scope mismatches.
    registered_actions = [Action(frozenset({0}), frozenset({0, 1}))]
    registered_ok = f_robust((0, 1), 1, registered_actions, 0)
    dynamic_actual_ok = False  # new path 1 has no blocker

    # Displayed-label alias contraction.
    displayed = [
        Action(frozenset({0}), frozenset({0})),
        Action(frozenset({0}), frozenset({1})),
    ]
    actual = [
        Action(frozenset({0}), frozenset({0})),
        Action(frozenset({0}), frozenset({0})),
    ]

    return {
        "positive_independent_roots": positive,
        "copied_root": {"actions": len(copied), "kappa": kappa((0,), 1, copied), "f1_robust": f_robust((0,), 1, copied, 1)},
        "common_bottleneck": {"kappa": kappa((0,1,2,3), 1, bottleneck), "f1_robust": f_robust((0,1,2,3), 1, bottleneck, 1)},
        "redundant_support_semantics": {
            "transversal_predicts_f1_robust": transversal_prediction,
            "actual_redundant_support_f1_robust": redundant_support_direct,
            "expected_scope_mismatch": transversal_prediction != redundant_support_direct,
        },
        "incompatible_repairs": {"pathwise_certificate": pathwise, "joint_execution": jointly_executable, "expected_scope_mismatch": pathwise != jointly_executable},
        "dynamic_rerouting": {"registered_fixed_path_certificate": registered_ok, "actual_dynamic_restoration": dynamic_actual_ok, "expected_scope_mismatch": registered_ok != dynamic_actual_ok},
        "displayed_aliases": {"displayed_kappa": kappa((0,1), 1, displayed), "actual_kappa": kappa((0,), 1, actual)},
    }


def main() -> None:
    ex = exhaustive_single_path()
    rnd = random_multi_path()
    witnesses = required_witnesses()
    result = {
        "schema": "PMR007_ROUND20_PRIMARY_CHECK_RESULTS_V1",
        "declared_semantics": "finite static fixed complete path registry; any corrupted required root disables descendant action; pathwise availability",
        "exhaustive_single_path": ex,
        "random_multi_path": rnd,
        "required_witnesses": witnesses,
    }
    failures = []
    for key in ("mismatches", "duplicate_failures", "enlargement_failures", "deletion_failures", "contraction_failures"):
        if ex.get(key): failures.append(f"exhaustive:{key}")
    if rnd.get("mismatches"): failures.append("random:mismatches")
    if witnesses["positive_independent_roots"] != {"kappa": 2, "f1_robust": True, "f2_robust": False}:
        failures.append("positive_witness")
    for k in ("redundant_support_semantics", "incompatible_repairs", "dynamic_rerouting"):
        if not witnesses[k]["expected_scope_mismatch"]:
            failures.append(f"missing_expected_scope_mismatch:{k}")
    if witnesses["displayed_aliases"] != {"displayed_kappa": 2, "actual_kappa": 1}:
        failures.append("displayed_alias_control")
    result["failures"] = failures
    result["overall"] = "PASS" if not failures else "FAIL"
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "overall": result["overall"],
        "exhaustive_cases": ex["checked"],
        "random_trials": rnd["trials"],
        "random_f_cases": rnd["f_cases"],
        "failures": failures,
    }, indent=2))

if __name__ == "__main__":
    main()
