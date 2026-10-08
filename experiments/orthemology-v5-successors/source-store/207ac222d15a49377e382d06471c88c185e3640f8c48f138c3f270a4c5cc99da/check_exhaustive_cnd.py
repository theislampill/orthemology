"""Exhaust the declared small CND interpretations; no metaphysical claim.

There are eight (world, effect, respect) slots. A slot has no original
producer, producer 0, or producer 1. This enumerates exactly the CND-satisfying
relations on those finite sorts. Four reception profiles concern producer 0.
"""

import itertools
import json


def check():
    slots = tuple(itertools.product(range(2), repeat=3))
    checked = 0
    antecedent_cases = 0
    for choices in itertools.product((-1, 0, 1), repeat=len(slots)):
        original = {
            (world, agent, effect, respect)
            for (world, effect, respect), agent in zip(slots, choices)
            if agent >= 0
        }
        retained_role = all(
            any(v == world and agent == 0 for v, agent, _, _ in original)
            for world in range(2)
        )
        for received in itertools.product((False, True), repeat=2):
            complete_overlap = all(
                (world, 1, effect, respect) in original
                for world, agent, effect, respect in original
                if agent == 0 and received[world]
            )
            if retained_role and complete_overlap:
                antecedent_cases += 1
                if any(received):
                    raise AssertionError((choices, received))
            checked += 1
    assert checked == 26244
    assert antecedent_cases > 0
    return {
        "status": "PASS",
        "interpretations": checked,
        "antecedent_satisfying_interpretations": antecedent_cases,
        "sort_sizes": {"worlds": 2, "sources": 2, "effects": 2, "respects": 2},
        "scope": "Finite formula corroboration only; no metaphysical possibility claim",
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
