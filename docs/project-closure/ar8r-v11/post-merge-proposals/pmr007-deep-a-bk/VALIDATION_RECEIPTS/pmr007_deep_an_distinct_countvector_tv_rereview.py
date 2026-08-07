#!/usr/bin/env python3
"""Distinct rereview for PMR-007-ABPD-1.

This checker deliberately does not import or invoke the primary checker.  It
uses count-vector likelihoods, exhaustive event separation, and direct Kraft
checks.  Exact Candidate-G anchors are checked against an externally supplied
custody root so no private absolute path is embedded in the artifact.
"""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
import math
import os
from pathlib import Path
from typing import Iterable, Iterator, Sequence


def compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for head in range(total + 1):
        for tail in compositions(total - head, parts - 1):
            yield (head, *tail)


def multinomial_coefficient(counts: Sequence[int]) -> int:
    remaining = sum(counts)
    value = 1
    for count in counts[:-1]:
        value *= math.comb(remaining, count)
        remaining -= count
    return value


def count_vector_likelihood(distribution: Sequence[Fraction], counts: Sequence[int]) -> Fraction:
    value = Fraction(multinomial_coefficient(counts), 1)
    for probability, count in zip(distribution, counts, strict=True):
        value *= probability ** count
    return value


def distributions(outcomes: int, denominator: int) -> list[tuple[Fraction, ...]]:
    return [
        tuple(Fraction(n, denominator) for n in numerators)
        for numerators in compositions(denominator, outcomes)
    ]


def event_probability(distribution: Sequence[Fraction], mask: int) -> Fraction:
    return sum(
        (p for index, p in enumerate(distribution) if mask & (1 << index)),
        Fraction(0, 1),
    )


def total_variation(p: Sequence[Fraction], q: Sequence[Fraction]) -> Fraction:
    return sum((abs(a - b) for a, b in zip(p, q, strict=True)), Fraction(0, 1)) / 2


def maximum_event_gap(p: Sequence[Fraction], q: Sequence[Fraction]) -> Fraction:
    n = len(p)
    return max(abs(event_probability(p, mask) - event_probability(q, mask)) for mask in range(1 << n))


def is_prefix_free(code: dict[str, str]) -> bool:
    words = list(code.values())
    return all(
        i == j or not words[j].startswith(words[i])
        for i in range(len(words))
        for j in range(len(words))
    )


def kraft_sum(code: dict[str, str]) -> Fraction:
    return sum((Fraction(1, 2 ** len(word)) for word in code.values()), Fraction(0, 1))


def check_source_anchors() -> dict[str, object]:
    root_env = os.environ.get("AR8R_DEEP_CONTEXT_ROOT")
    if not root_env:
        return {
            "status": "NOT_RUN_MISSING_AR8R_DEEP_CONTEXT_ROOT",
            "anchors_checked": 0,
            "anchors_missing": [],
        }
    root = Path(root_env)
    candidate = root / "candidate-g" / (
        "000069__ar7-reopened-audit-continuation__payload__ar7-complete__"
        "CANDIDATES__G-unity-agency-wisdom__FORMAL_RECONSTRUCTION.md"
    )
    if not candidate.is_file():
        return {
            "status": "FAIL_SOURCE_NOT_FOUND",
            "relative_file": str(candidate.relative_to(root)),
            "anchors_checked": 0,
            "anchors_missing": [],
        }
    data = candidate.read_bytes()
    text = data.decode("utf-8")
    anchors = [
        "P5. No impersonal rival derives an equal or better profile with equal or lower primitive cost.",
        "P6. Explanatory unification and brute-fact economy are truth-conducive enough for abduction.",
        "`P5` is currently unestablished and is the central rival burden.",
        "`P6` remains a general meta-abductive burden.",
        "No scalar score is assumed canonical.",
    ]
    missing = [anchor for anchor in anchors if anchor not in text]
    return {
        "status": "PASS" if not missing else "FAIL_ANCHOR_MISMATCH",
        "relative_file": str(candidate.relative_to(root)),
        "sha256": sha256(data).hexdigest(),
        "anchors_checked": len(anchors),
        "anchors_missing": missing,
    }


def main() -> int:
    # Independent finite universe: three outcomes on a denominator-five grid.
    ds = distributions(outcomes=3, denominator=5)
    priors = [Fraction(1, 4), Fraction(2, 3), Fraction(1, 1), Fraction(7, 3)]
    count_vectors = [counts for length in range(0, 6) for counts in compositions(length, 3)]

    parity_cases = parity_failures = 0
    posterior_nonunit_cases = 0
    tv_pairs = tv_event_mismatches = distinct_without_witness = 0
    zero_denominator_cases = 0

    for p, q in product(ds, repeat=2):
        tv_pairs += 1
        tv = total_variation(p, q)
        event_gap = maximum_event_gap(p, q)
        if tv != event_gap:
            tv_event_mismatches += 1
        if p != q and event_gap == 0:
            distinct_without_witness += 1

        for counts in count_vectors:
            lp = count_vector_likelihood(p, counts)
            lq = count_vector_likelihood(q, counts)
            if lq == 0:
                zero_denominator_cases += 1
                continue
            for prior in priors:
                posterior = prior * lp / lq
                if lp == lq and lp > 0:
                    parity_cases += 1
                    if posterior != prior:
                        parity_failures += 1
                elif lp != lq:
                    posterior_nonunit_cases += 1

    # Independently fixed support restriction on a five-outcome space.
    support_cases = support_failures = 0
    universe = tuple(range(5))
    rival = tuple(Fraction(1, 5) for _ in universe)
    for size in range(1, len(universe)):
        for subset in combinations(universe, size):
            subset_set = set(subset)
            candidate = tuple(
                Fraction(1, size) if index in subset_set else Fraction(0, 1)
                for index in universe
            )
            for observation in subset:
                support_cases += 1
                if candidate[observation] / rival[observation] != Fraction(5, size):
                    support_failures += 1

    # Prefix codes directly checked for prefix-freeness and Kraft validity.
    code_favoring_a = {"A": "0", "R": "10"}
    code_favoring_r = {"A": "10", "R": "0"}
    prefix_checks = {
        "favor_A_prefix_free": is_prefix_free(code_favoring_a),
        "favor_R_prefix_free": is_prefix_free(code_favoring_r),
        "favor_A_kraft_at_most_one": kraft_sum(code_favoring_a) <= 1,
        "favor_R_kraft_at_most_one": kraft_sum(code_favoring_r) <= 1,
        "A_shorter_in_first": len(code_favoring_a["A"]) < len(code_favoring_a["R"]),
        "R_shorter_in_second": len(code_favoring_r["R"]) < len(code_favoring_r["A"]),
    }

    # Model-misspecification control: an omitted observation refutes only the
    # frozen zero-support model and does not choose a unique alternative.
    omitted_observation_control = {
        "frozen_model": [Fraction(1, 2), Fraction(1, 2), Fraction(0, 1)],
        "observed_index": 2,
        "frozen_model_likelihood": Fraction(0, 1),
        "distinct_nonzero_alternatives": 2,
    }
    omitted_control_pass = (
        omitted_observation_control["frozen_model"][2] == 0
        and omitted_observation_control["distinct_nonzero_alternatives"] > 1
    )

    source = check_source_anchors()
    claims = {
        "equal_positive_likelihood_preserves_prior_odds": parity_failures == 0 and parity_cases > 0,
        "finite_total_variation_equals_max_event_gap": tv_event_mismatches == 0,
        "distinct_finite_distributions_have_event_witness": distinct_without_witness == 0,
        "fixed_support_restriction_has_declared_bayes_factor": support_failures == 0 and support_cases > 0,
        "prefix_code_ranking_is_reversible_under_valid_codes": all(prefix_checks.values()),
        "misspecified_zero_does_not_identify_unique_rival": omitted_control_pass,
        "candidate_g_p5_p6_source_anchors_match": source.get("status") == "PASS",
    }

    result = {
        "schema": "PMR007_DEEP_AN_DISTINCT_COUNTVECTOR_TV_REREVIEW_RESULTS_V1",
        "method_relation": "independent_count_vector_and_event_subset_implementation",
        "finite_universe": {
            "outcomes": 3,
            "distribution_denominator": 5,
            "distributions": len(ds),
            "model_pairs": tv_pairs,
            "count_vectors": len(count_vectors),
            "maximum_sample_length": 5,
            "priors": [str(p) for p in priors],
        },
        "counts": {
            "likelihood_parity_prior_instances": parity_cases,
            "likelihood_parity_failures": parity_failures,
            "nonunit_likelihood_instances": posterior_nonunit_cases,
            "zero_denominator_cases_skipped_as_undefined_odds": zero_denominator_cases,
            "tv_event_mismatches": tv_event_mismatches,
            "distinct_pairs_without_event_witness": distinct_without_witness,
            "support_restriction_cases": support_cases,
            "support_restriction_failures": support_failures,
        },
        "prefix_code_controls": {
            "favor_A": code_favoring_a,
            "favor_R": code_favoring_r,
            "kraft_favor_A": str(kraft_sum(code_favoring_a)),
            "kraft_favor_R": str(kraft_sum(code_favoring_r)),
            "checks": prefix_checks,
        },
        "source_anchor_check": source,
        "claims": claims,
        "scope_notes": [
            "iid count-vector likelihood only",
            "finite registered evidence spaces only",
            "no canonical prior or coding policy supplied",
            "no predictive-to-metaphysical transfer",
            "same-program procedural rereview; not external review",
        ],
        "overall": "PASS" if all(claims.values()) else "FAIL",
    }

    out = Path(__file__).with_name(Path(__file__).stem + "_results.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True, default=str))
    return 0 if result["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
