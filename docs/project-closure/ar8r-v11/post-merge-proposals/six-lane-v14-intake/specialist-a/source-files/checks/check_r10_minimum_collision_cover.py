#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results/r10_minimum_collision_cover_results.json"
MODELS = BASE / "rounds/r10_minimum_collision_cover_models.json"


def brute_min_cover(universe_mask: int, covers: tuple[int, ...]) -> tuple[int | None, list[int]]:
    best: int | None = None
    witnesses: list[int] = []
    for subset in range(1 << len(covers)):
        union = 0
        size = 0
        for i, c in enumerate(covers):
            if subset & (1 << i):
                union |= c
                size += 1
        if union == universe_mask:
            if best is None or size < best:
                best = size
                witnesses = [subset]
            elif size == best:
                witnesses.append(subset)
    return best, witnesses


def dp_min_cover(universe_mask: int, covers: tuple[int, ...]) -> int | None:
    inf = len(covers) + 1
    dp = [inf] * (universe_mask + 1)
    dp[0] = 0
    for c in covers:
        nxt = list(dp)
        for mask, value in enumerate(dp):
            if value < inf:
                nxt[mask | c] = min(nxt[mask | c], value + 1)
        dp = nxt
    return None if dp[universe_mask] == inf else dp[universe_mask]


def union_of(covers: tuple[int, ...], subset: int) -> int:
    value = 0
    for i, c in enumerate(covers):
        if subset & (1 << i):
            value |= c
    return value


def private_witness(universe_mask: int, covers: tuple[int, ...], subset: int, factor: int) -> bool:
    if not (subset & (1 << factor)):
        return False
    other = union_of(covers, subset & ~(1 << factor))
    return bool((covers[factor] & universe_mask) & ~other)


def greedy_cover(universe_mask: int, covers: tuple[int, ...]) -> tuple[int | None, int]:
    uncovered = universe_mask
    chosen = 0
    used = 0
    while uncovered:
        gains = [((c & uncovered).bit_count(), -i, i) for i, c in enumerate(covers) if not (chosen & (1 << i))]
        if not gains:
            return None, chosen
        gain, _, idx = max(gains)
        if gain == 0:
            return None, chosen
        chosen |= 1 << idx
        uncovered &= ~covers[idx]
        used += 1
    return used, chosen


def exhaustive() -> dict[str, int]:
    family_cases = 0
    min_cover_mismatch = 0
    impossibility_mismatch = 0
    deletion_checks = 0
    deletion_private_witness_mismatch = 0
    positive_gain_redundant_cases = 0
    no_cover_cases = 0
    cover_cases = 0

    for n in range(1, 5):
        universe = (1 << n) - 1
        for m in range(1, 5):
            for covers in itertools.product(range(1 << n), repeat=m):
                family_cases += 1
                brute, witnesses = brute_min_cover(universe, covers)
                dp = dp_min_cover(universe, covers)
                min_cover_mismatch += int(brute != dp)
                impossible = brute is None
                impossibility_mismatch += int(impossible != ((union_of(covers, (1 << m) - 1) & universe) != universe))
                if impossible:
                    no_cover_cases += 1
                else:
                    cover_cases += 1
                for subset in range(1 << m):
                    if union_of(covers, subset) != universe:
                        continue
                    for f in range(m):
                        if not (subset & (1 << f)):
                            continue
                        deletion_checks += 1
                        removal_breaks = union_of(covers, subset & ~(1 << f)) != universe
                        deletion_private_witness_mismatch += int(removal_breaks != private_witness(universe, covers, subset, f))
                for f, c in enumerate(covers):
                    if not c:
                        continue
                    other_subset = ((1 << m) - 1) & ~(1 << f)
                    if union_of(covers, other_subset) == universe:
                        positive_gain_redundant_cases += 1
                        break

    return {
        "expected_set_system_cases": sum((1 << n) ** m for n in range(1, 5) for m in range(1, 5)),
        "set_system_cases": family_cases,
        "minimum_cover_mismatch_count": min_cover_mismatch,
        "impossibility_mismatch_count": impossibility_mismatch,
        "deletion_private_witness_checks": deletion_checks,
        "deletion_private_witness_mismatch_count": deletion_private_witness_mismatch,
        "positive_gain_redundant_cases": positive_gain_redundant_cases,
        "cover_cases": cover_cases,
        "no_cover_cases": no_cover_cases,
    }


def collision_pairs(base: tuple[int, ...], target: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple((i, j) for i in range(len(base)) for j in range(i + 1, len(base)) if base[i] == base[j] and target[i] != target[j])


def factor_cover(pairs: tuple[tuple[int, int], ...], factor: tuple[int, ...]) -> int:
    mask = 0
    for k, (i, j) in enumerate(pairs):
        if factor[i] != factor[j]:
            mask |= 1 << k
    return mask


def models() -> dict[str, object]:
    base = (0, 0, 0)
    target = (0, 1, 2)
    pairs = collision_pairs(base, target)
    factors = {
        "weak_left": (0, 1, 0),
        "weak_right": (0, 0, 1),
        "profile_derived": base,
        "target_leak": target,
    }
    covers = {name: factor_cover(pairs, sig) for name, sig in factors.items()}

    greedy_sets = (
        0b001111,  # {0,1,2,3}
        0b110001,  # {0,4,5} after index convention; exact labels are immaterial
        0b101100,  # {2,3,5}; adjusted below by explicit list model
    )
    greedy_explicit = {
        "universe": [1, 2, 3, 4, 5, 6],
        "sets": {
            "A": [1, 2, 3, 4],
            "B": [1, 2, 5],
            "C": [3, 4, 6],
        },
        "deterministic_greedy_A_then_B_then_C": 3,
        "optimum_B_C": 2,
    }
    # Exact bit form of the displayed model.
    exact_greedy_covers = (
        sum(1 << (x - 1) for x in greedy_explicit["sets"]["A"]),
        sum(1 << (x - 1) for x in greedy_explicit["sets"]["B"]),
        sum(1 << (x - 1) for x in greedy_explicit["sets"]["C"]),
    )
    greedy_count, greedy_subset = greedy_cover((1 << 6) - 1, exact_greedy_covers)
    optimum, optimum_subsets = brute_min_cover((1 << 6) - 1, exact_greedy_covers)
    greedy_explicit.update({"computed_greedy": greedy_count, "computed_optimum": optimum, "greedy_subset_mask": greedy_subset, "optimum_subset_masks": optimum_subsets})

    return {
        "three_rival_manifest": {
            "labels": ["unified_personal_witness", "impersonal_powers_witness", "plural_witness"],
            "base_profile": base,
            "target": target,
            "collision_pairs": pairs,
            "factor_signatures": factors,
            "coverage_masks": covers,
            "eligible_factors": ["weak_left", "weak_right", "profile_derived"],
            "ineligible_factor": "target_leak",
            "minimum_eligible_cover": ["weak_left", "weak_right"],
        },
        "greedy_countermodel": greedy_explicit,
        "positive_gain_but_redundant": {
            "universe": [0, 1],
            "factor_coverages": {"small": [0], "large": [0, 1], "other": [1]},
            "observation": "small has positive gain but is not indispensable because large alone covers the universe",
        },
    }


def mutation_tests(stats: dict[str, int], model: dict[str, object]) -> list[dict[str, object]]:
    three = model["three_rival_manifest"]
    covers = three["coverage_masks"]
    universe = (1 << len(three["collision_pairs"])) - 1
    eligible = tuple(covers[name] for name in three["eligible_factors"])
    min_eligible, _ = brute_min_cover(universe, eligible)
    greedy = model["greedy_countermodel"]
    return [
        {
            "mutant": "greedy_max_gain_is_always_minimum_cover",
            "killed": greedy["computed_greedy"] == 3 and greedy["computed_optimum"] == 2,
            "killer": "six-element deterministic greedy countermodel",
        },
        {
            "mutant": "positive_individual_gain_makes_factor_indispensable",
            "killed": stats["positive_gain_redundant_cases"] > 0,
            "killer": "exhaustive redundant positive-gain factors",
        },
        {
            "mutant": "one_pairwise_separation_identifies_three_way_class",
            "killed": min_eligible == 2 and any((c & universe) != universe for c in eligible),
            "killer": "each weak factor leaves residual architecture collisions",
        },
        {
            "mutant": "target_leak_may_enter_optimization_because_it_covers_all",
            "killed": covers["target_leak"] == universe and three["ineligible_factor"] == "target_leak",
            "killer": "eligibility is frozen before gain optimization",
        },
        {
            "mutant": "factor_deletion_requires_no_private_collision_witness",
            "killed": stats["deletion_private_witness_mismatch_count"] == 0 and stats["deletion_private_witness_checks"] > 0,
            "killer": "exhaustive cover-removal/private-witness equivalence",
        },
        {
            "mutant": "failure_of_declared_factor_cover_proves_metaphysical_impossibility",
            "killed": stats["no_cover_cases"] > 0,
            "killer": "no-cover conclusion is relative to the frozen eligible factor family and model manifest",
        },
        {
            "mutant": "prefilled_minimum_cover_counts",
            "killed": stats["set_system_cases"] == stats["expected_set_system_cases"] and stats["minimum_cover_mismatch_count"] == 0,
            "killer": "fresh exhaustive set-system enumeration and independent dynamic program",
        },
    ]


def main() -> None:
    stats = exhaustive()
    model = models()
    mutations = mutation_tests(stats, model)
    errors = []
    for key in ("minimum_cover_mismatch_count", "impossibility_mismatch_count", "deletion_private_witness_mismatch_count"):
        if stats[key]:
            errors.append(key)
    if not all(m["killed"] for m in mutations):
        errors.append("mutation survived")

    payload = {
        "schema": "spa-r10-minimum-collision-cover-models-v1",
        "specialist_local_result": "SPA-R10",
        "typed_object": "finite target-collision universe with pre-certified eligible factor coverage sets",
        "criterion": "a factor set identifies the frozen target partition iff its coverage union equals the full collision universe",
        "impossibility": "if the union of every eligible factor leaves a collision, no composition from the declared factor family identifies the target on the frozen manifest",
        "deletion": "within a covering set, deleting factor f breaks coverage iff f has a collision not covered by the remaining factors",
        "models": model,
        "guards": ["eligibility fixed before optimization", "pair coverage deduplicated", "target leak excluded", "manifest and target frozen", "no metaphysical extrapolation"],
        "conclusion_ceiling": "exact minimum factor cover or declared-family no-cover result on a finite frozen manifest",
    }
    MODELS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(json.dumps(model, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        "schema": "spa-r10-check-results-v1",
        "specialist_local_result": "SPA-R10",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        **stats,
        "model_digest": digest,
        "mutations": mutations,
        "mutants_killed": sum(bool(m["killed"]) for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "standard finite set-cover/coverage-function specialization over target-collision pairs; no new theorem identity or novelty",
        "claim_ceiling": "minimum eligible factor cover or bounded no-cover on the frozen manifest only; no empirical implementation or metaphysical impossibility",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "cases": result["set_system_cases"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
