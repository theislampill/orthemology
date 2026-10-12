#!/usr/bin/env python3
"""Reproducible finite/dimensionless consistency checks for The Last Moat.

These are tests of toy instances and numerical examples, not proof-assistant
verification, physical experiments, or evidence of any real communication bypass.
No third-party packages or network access are required.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable, Iterable


def require(condition: bool, message: str) -> None:
    """A check not disabled by Python's -O option."""
    if not condition:
        raise AssertionError(message)


def close(actual: float, expected: float, *, tolerance: float = 1e-9) -> None:
    require(math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance),
            f"{actual!r} differs from {expected!r}")


def midpoint(function: Callable[[float], float], stop: float, steps: int = 20000) -> float:
    step = stop / steps
    return step * math.fsum(function((i + 0.5) * step) for i in range(steps))


def h2(p: float) -> float:
    if not 0.0 <= p <= 1.0:
        raise ValueError("Probability must be between zero and one.")
    return -math.fsum(q * math.log2(q) for q in (p, 1.0 - p) if q > 0.0)


def powerset(items: Iterable[Any]) -> list[frozenset[Any]]:
    sequence = tuple(items)
    return [frozenset(s) for n in range(len(sequence) + 1)
            for s in itertools.combinations(sequence, n)]


def gramian_table() -> dict[str, Any]:
    rows = []
    for b, energy, expected in ((0.0, 1.0, False), (0.2, 1.0, False),
                                (0.2, 4.0, True), (1.0, 1.0, True)):
        gramian = b * b * (1.0 - math.exp(-2.0)) / 2.0
        received = math.sqrt(energy * gramian)
        robust = energy * gramian > 0.15 ** 2
        require(robust == expected, "Unexpected robust-bit classification.")
        rows.append({"b": b, "input_norm_squared_budget": energy,
                     "gramian": gramian, "max_received_magnitude": received,
                     "robust_bit_at_noise_radius_0_15": robust})
    return {"rows": rows, "units": "dimensionless"}


def gramian_quadrature() -> dict[str, Any]:
    analytical = (1.0 - math.exp(-2.0)) / 2.0
    numerical = midpoint(lambda s: math.exp(-2.0 * s), 1.0)
    close(numerical, analytical, tolerance=1e-9)
    return {"analytical": analytical, "midpoint_quadrature": numerical,
            "absolute_error": abs(numerical - analytical)}


def optimal_scalar_inputs() -> dict[str, Any]:
    b, energy, horizon = 0.2, 4.0, 1.0
    gramian = b * b * (1.0 - math.exp(-2.0 * horizon)) / 2.0
    control = lambda s: math.sqrt(energy / gramian) * b * math.exp(-(horizon - s))
    norm_squared = midpoint(lambda s: control(s) ** 2, horizon)
    output = midpoint(lambda s: b * math.exp(-(horizon - s)) * control(s), horizon)
    close(norm_squared, energy, tolerance=1e-8)
    close(output, math.sqrt(energy * gramian), tolerance=1e-9)
    require(2.0 * output > 2.0 * 0.15, "Noise balls should be disjoint.")
    return {"integrated_input_norm_squared": norm_squared, "output": output}


def equality_fails_zero_error() -> dict[str, Any]:
    radius = 0.15
    centre_minus, centre_plus = -radius, radius
    ambiguous_observation = 0.0
    require(abs(ambiguous_observation - centre_minus) <= radius, "First ball missing zero.")
    require(abs(ambiguous_observation - centre_plus) <= radius, "Second ball missing zero.")
    return {"centres": [centre_minus, centre_plus], "shared_observation": 0.0}


def nonlinear_margin() -> dict[str, Any]:
    sigma, kappa, amplitude, delta = 0.8, 0.1, 0.4, 0.15
    transform = lambda u: sigma * u - kappa * u * abs(u)
    sufficient_margin = amplitude * sigma - kappa * amplitude ** 2
    separation = abs(transform(amplitude) - transform(-amplitude))
    close(separation, 2.0 * sufficient_margin)
    require(sufficient_margin > delta, "Chosen nonlinear example must separate.")
    return {"sufficient_margin": sufficient_margin, "actual_separation": separation,
            "noise_diameter": 2.0 * delta}


def fresh_state_bound() -> dict[str, Any]:
    bits, error, cut_rate = 64, 0.01, 2.0
    lower = (bits * (1.0 - error) - h2(error)) / cut_rate
    require(round(lower, 4) == 31.6396, "Printed fresh-state example disagrees.")
    return {"fresh_bits": bits, "error_bound": error,
            "stipulated_cut_rate": cut_rate, "minimum_time_bound": lower,
            "units": "independent information-theoretic toy"}


def support_family() -> dict[str, Any]:
    supports = [frozenset(s) for s in ({"a", "b"}, {"b", "c"}, {"a", "c"})]
    rows = []
    fatal_sizes = []
    for failed in powerset(("a", "b", "c")):
        survives = any(not (s & failed) for s in supports)
        hits_all = all(bool(s & failed) for s in supports)
        require(survives == (not hits_all), "Hitting-set equivalence failed.")
        if len(failed) == 1:
            require(survives, "Every singleton failure should be tolerated.")
        if len(failed) >= 2:
            require(not survives, "Every double/triple failure should defeat catalogue.")
        if hits_all:
            fatal_sizes.append(len(failed))
        rows.append({"failed": sorted(failed), "survives": survives})
    tau = min(fatal_sizes)
    require(tau == 2, "Minimum hitting-set size is not two.")
    return {"minimum_fatal_set_size": tau, "exhaustive_failures": rows}


def encoding_continuity() -> dict[str, Any]:
    encode = [lambda q: q, lambda q: (3 * q + 1) % 7]
    decode = [lambda x: x, lambda x: (5 * (x - 1)) % 7]
    count = 0
    for r in range(2):
        for q in range(7):
            require(decode[r](encode[r](q)) == q, "Encoding inverse failed.")
            for a in range(7):
                physical_step = encode[r]((decode[r](encode[r](q)) + a) % 7)
                require(decode[r](physical_step) == (q + a) % 7,
                        "Execution square does not commute.")
                count += 1
            for s in range(2):
                migrated = encode[s](decode[r](encode[r](q)))
                require(decode[s](migrated) == q, "Migration square does not commute.")
                count += 1
    return {"execution_and_migration_cases": count, "abstract_states": 7,
            "encodings": 2, "physical_experiment": False}


def accumulated_error() -> dict[str, Any]:
    checks = 0
    maxima = {}
    for lipschitz in (0.5, 1.0, 1.2):
        e0 = 0.02
        defects = [0.001 * (1 + (j % 3)) for j in range(25)]
        direct = e0
        for n, defect in enumerate(defects, start=1):
            direct = lipschitz * direct + defect
            formula = lipschitz ** n * e0 + math.fsum(
                lipschitz ** (n - 1 - j) * defects[j] for j in range(n))
            close(direct, formula)
            if lipschitz < 1:
                cap = (lipschitz ** n * e0
                       + max(defects) * (1 - lipschitz ** n) / (1 - lipschitz))
                require(direct <= cap + 1e-12, "Contraction bound violated.")
            checks += 1
        maxima[str(lipschitz)] = direct
    return {"checked_recurrence_instances": checks, "final_errors": maxima}


def finite_viability() -> dict[str, Any]:
    transitions = {
        "stable": {"hold": {"stable"}},
        "recoverable": {"repair": {"stable"}, "idle": {"failed"}},
        "fragile": {"wait": {"fragile", "failed"}},
        "stranded": {"wait": {"fragile"}},
    }
    safe = set(transitions)
    current = safe.copy()
    history = [sorted(current)]
    while True:
        following = {x for x in current
                     if any(next_states <= current
                            for next_states in transitions[x].values())}
        history.append(sorted(following))
        if following == current:
            break
        current = following
    require(current == {"stable", "recoverable"}, "Wrong greatest invariant set.")
    require(history[1] == ["recoverable", "stable", "stranded"], "Wrong first iterate.")
    invariant_sets = []
    for subset in powerset(safe):
        invariant = all(any(successors <= subset
                            for successors in transitions[x].values()) for x in subset)
        if invariant:
            require(subset <= current, "Found invariant set outside the proposed greatest one.")
            invariant_sets.append(sorted(subset))
    return {"iterates": history, "all_controlled_invariant_subsets": invariant_sets}


def no_channel_example() -> dict[str, Any]:
    # P(Y=1 | M=0) = P(Y=1 | M=1) = 0.3, with a uniform independent message.
    joint = [[0.35, 0.15], [0.35, 0.15]]
    p_m = [math.fsum(row) for row in joint]
    p_y = [math.fsum(row[y] for row in joint) for y in range(2)]
    information = math.fsum(joint[m][y] * math.log2(joint[m][y] / (p_m[m] * p_y[y]))
                            for m in range(2) for y in range(2))
    close(information, 0.0)
    return {"mutual_information_bits": information, "joint_distribution": joint}


def attribution_total_variation() -> dict[str, Any]:
    p0, p1 = [0.1, 0.2, 0.3, 0.4], [0.3, 0.3, 0.2, 0.2]
    tv = math.fsum(abs(a - b) for a, b in zip(p0, p1)) / 2.0
    successes = [0.5 * (1.0 - math.fsum(p0[i] for i in event))
                 + 0.5 * math.fsum(p1[i] for i in event)
                 for event in powerset(range(4))]
    optimal = max(successes)
    close(optimal, (1.0 + tv) / 2.0)
    close(optimal, 0.65)
    return {"total_variation": tv, "best_success_exhaustive": optimal,
            "tests_enumerated": len(successes)}


def commuting_updates() -> dict[str, Any]:
    # Task C depends on A; independent B touches another coordinate.
    tasks = {"A": lambda p: (p[0] + 1, p[1]),
             "B": lambda p: (p[0], p[1] + 4),
             "C": lambda p: (p[0] * 3, p[1])}
    outcomes = []
    for order in itertools.permutations(tasks):
        if order.index("A") >= order.index("C"):
            continue
        state = (2, 5)
        for task in order:
            state = tasks[task](state)
        outcomes.append({"order": list(order), "state": list(state)})
    require(all(row["state"] == [9, 9] for row in outcomes), "Topological order differs.")
    return {"valid_orderings": outcomes}


CHECKS: list[tuple[str, Callable[[], dict[str, Any]]]] = [
    ("scalar_robust_bit_table", gramian_table),
    ("gramian_numerical_integral", gramian_quadrature),
    ("optimal_scalar_control", optimal_scalar_inputs),
    ("closed_noise_balls_at_equality", equality_fails_zero_error),
    ("nonlinear_margin", nonlinear_margin),
    ("fresh_state_transfer_lower_bound", fresh_state_bound),
    ("failure_support_hitting_set", support_family),
    ("exact_encoding_and_migration", encoding_continuity),
    ("error_accumulation", accumulated_error),
    ("finite_viability_kernel", finite_viability),
    ("message_independent_observation", no_channel_example),
    ("attribution_total_variation", attribution_total_variation),
    ("commuting_workflow_updates", commuting_updates),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional path for the JSON report.")
    args = parser.parse_args()
    results = []
    for name, check in CHECKS:
        try:
            details = check()
            results.append({"name": name, "passed": True, "details": details})
        except Exception as exc:
            results.append({"name": name, "passed": False,
                            "error": f"{type(exc).__name__}: {exc}"})
    passed = sum(bool(result["passed"]) for result in results)
    report = {
        "title": "The Last Moat: reproducible toy-model checks",
        "scope": "Finite and dimensionless instances, not physical or proof-assistant validation",
        "total_checks": len(results), "passed_checks": passed,
        "all_passed": passed == len(results), "checks": results,
    }
    encoded = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
