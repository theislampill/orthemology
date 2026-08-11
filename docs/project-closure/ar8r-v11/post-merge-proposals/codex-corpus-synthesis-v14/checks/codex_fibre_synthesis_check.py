#!/usr/bin/env python3
"""Finite regression checks for the bounded fibre-synthesis proposal."""

from __future__ import annotations

import itertools
import json
import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
RESULTS = pathlib.Path(__file__).with_name("codex_fibre_synthesis_check_results.json")


def functions(domain_size: int, codomain_size: int):
    if domain_size == 0:
        yield ()
        return
    if codomain_size == 0:
        return
    yield from itertools.product(range(codomain_size), repeat=domain_size)


def fibre_constant(observation, target) -> bool:
    return all(
        observation[x] != observation[y] or target[x] == target[y]
        for x in range(len(observation))
        for y in range(len(observation))
    )


def surjective(observation, codomain_size: int) -> bool:
    return set(observation) == set(range(codomain_size))


def full_decoder_exists(observation, target, obs_size: int, target_size: int) -> bool:
    return any(
        all(decoder[observation[x]] == target[x] for x in range(len(observation)))
        for decoder in functions(obs_size, target_size)
    )


def main() -> int:
    full_cases = 0
    full_failures = []
    for x_size, obs_size, target_size in itertools.product(range(4), repeat=3):
        for observation in functions(x_size, obs_size):
            for target in functions(x_size, target_size):
                actual = full_decoder_exists(
                    observation, target, obs_size, target_size
                )
                expected = fibre_constant(observation, target) and (
                    surjective(observation, obs_size) or target_size > 0
                )
                full_cases += 1
                if actual != expected:
                    full_failures.append(
                        {
                            "x_size": x_size,
                            "obs_size": obs_size,
                            "target_size": target_size,
                            "observation": observation,
                            "target": target,
                            "actual": actual,
                            "expected": expected,
                        }
                    )

    pair_cases = 0
    pair_failures = []
    refinement_cases = 0
    refinement_failures = []
    for x_size, obs_size, q_size, g_size in itertools.product(range(3), repeat=4):
        for observation in functions(x_size, obs_size):
            for query in functions(x_size, q_size):
                for guard in functions(x_size, g_size):
                    pair_target = tuple(zip(query, guard))
                    pair_actual = fibre_constant(observation, pair_target)
                    pair_expected = fibre_constant(
                        observation, query
                    ) and fibre_constant(observation, guard)
                    pair_cases += 1
                    if pair_actual != pair_expected:
                        pair_failures.append(
                            {
                                "observation": observation,
                                "query": query,
                                "guard": guard,
                            }
                        )

                    joint = tuple(zip(observation, guard))
                    refinement_actual = fibre_constant(joint, query)
                    refinement_expected = all(
                        observation[x] != observation[y]
                        or guard[x] != guard[y]
                        or query[x] == query[y]
                        for x in range(x_size)
                        for y in range(x_size)
                    )
                    refinement_cases += 1
                    if refinement_actual != refinement_expected:
                        refinement_failures.append(
                            {
                                "observation": observation,
                                "query": query,
                                "refinement": guard,
                            }
                        )

    result = {
        "schema": "ar8r-codex-fibre-synthesis-check-v14",
        "scope": "FINITE_EXHAUSTIVE_REGRESSION_NOT_GENERAL_PROOF",
        "full_codomain_cases": full_cases,
        "full_codomain_failures": len(full_failures),
        "pair_guard_cases": pair_cases,
        "pair_guard_failures": len(pair_failures),
        "joint_refinement_cases": refinement_cases,
        "joint_refinement_failures": len(refinement_failures),
        "empty_off_range_countermodel": {
            "domain_size": 0,
            "observation_codomain_size": 1,
            "target_codomain_size": 0,
            "fibre_constant": True,
            "surjective": False,
            "target_inhabited": False,
            "full_decoder_exists": False,
        },
        "status": "PASS"
        if not full_failures and not pair_failures and not refinement_failures
        else "FAIL",
        "failure_examples": {
            "full_codomain": full_failures[:3],
            "pair_guard": pair_failures[:3],
            "joint_refinement": refinement_failures[:3],
        },
    }
    RESULTS.write_bytes((json.dumps(result, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
