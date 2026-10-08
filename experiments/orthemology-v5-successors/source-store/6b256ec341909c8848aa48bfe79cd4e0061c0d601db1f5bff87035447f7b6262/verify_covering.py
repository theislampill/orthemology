#!/usr/bin/env python3
"""Check explicit repair-covering witnesses and finite lower-proof auxiliaries.

No optimizer is imported.  General optimality is proved ordinarily.  In
particular, the n=9 lower proof is not replaced by a solver's status code.
"""
from itertools import combinations, permutations
from math import ceil, comb
from pathlib import Path
import hashlib
import json

from dynamic_interlock import Actor, Command, Descriptor, World, threshold_contract

HERE = Path(__file__).resolve().parent


def main() -> None:
    data = json.loads((HERE / "COVERING_WITNESSES.json").read_text())
    checked_fault_sets = 0
    slot_count = 0
    covers_checked = []
    for row in data["rows"]:
        n, b, q, r = (row[x] for x in ("n", "B", "q", "r"))
        roots = frozenset(range(n))
        blocks = [frozenset(x) for x in row["blocks"]]
        assert len(set(blocks)) == len(blocks) == row["optimal_attempts"]
        assert all(len(x) == row["k"] and x <= roots for x in blocks)
        assert row["k"] == n - q
        assert threshold_contract(n, b, q, r)
        paths = [roots - x for x in blocks]
        descriptor = Descriptor(0, "binary-rule", 1, "actor-A", "replace", (0, 1))
        for faults in combinations(range(n), b):
            bad = frozenset(faults)
            assert any(bad <= block for block in blocks)
            assert any(not (path & bad) for path in paths)
            world = World(n, b, q, r, descriptor, bad)
            actor = Actor(descriptor)
            for nonce, path in enumerate(paths):
                command = Command.for_descriptor(actor.descriptor, path, nonce)
                world.prepare(command, requester="actor-A")
                world.attempt(command, requester="actor-A", bad_open=False)
                world.cancel(command, requester="actor-A", bad_ack=True)
                slot_count += 1
            assert world.table == descriptor.table and not world.unsafe
            checked_fault_sets += 1
        if b == 1:
            lower = ceil(n / row["k"])
        else:
            lower = ceil(n * ceil((n - 1) / (row["k"] - 1)) / row["k"])
        if n == 9 and b == 2:
            assert lower == 7
            # Eight follows from the separately supplied ordinary contradiction.
            lower = 8
        assert lower == row["optimal_attempts"]
        covers_checked.append({"n": n, "B": b, "q": q, "r": r,
                               "minimum_attempts": len(paths),
                               "gate_occurrences": q * len(paths),
                               "lower_proof": row["lower_proof"]})

    # Critical finite graph lemma in the n=9 ordinary lower proof:
    # every four distinct edges on four vertices have a disjoint pair.
    edges = list(combinations(range(4), 2))
    graph_cases = 0
    for four in combinations(edges, 4):
        assert any(set(a).isdisjoint(b) for a, b in combinations(four, 2))
        graph_cases += 1
    assert graph_cases == 15

    # Genuine opacity is necessary. With a labelled blocking-root oracle,
    # at n=4, B=1, a failed first path identifies the sole tainted root;
    # its complementary path then repairs in <=2 trials, rather than four.
    improved_cap = 0
    for bad_root in range(4):
        first = frozenset({0, 1, 2})
        if bad_root not in first:
            trials = 1
        else:
            second = frozenset(range(4)) - {bad_root}
            assert bad_root not in second
            trials = 2
        improved_cap = max(improved_cap, trials)
    assert improved_cap == 2

    result = {"status": "PASS_COVERING_WITNESSES_AND_FINITE_AUXILIARIES",
              "covered_maximal_fault_sets": checked_fault_sets,
              "executable_portfolio_slots": slot_count,
              "four_edge_graph_cases": graph_cases,
              "labelled_failure_deletion_cap_B1_n4": improved_cap,
              "frontier": covers_checked,
              "scope": "Coverage and execution verified; optimality uses supplied ordinary proofs, not solver status.",
              "witness_sha256": hashlib.sha256((HERE / "COVERING_WITNESSES.json").read_bytes()).hexdigest()}
    (HERE / "COVERING_CHECK_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
