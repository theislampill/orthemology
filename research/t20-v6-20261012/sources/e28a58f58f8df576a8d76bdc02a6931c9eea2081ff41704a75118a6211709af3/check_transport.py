"""Bounded transport controls, not a new optimizer or a complexity proof.

Compare independent finite Set-Cover enumeration with the unchanged inherited
tree and whole-DAG compilers. Run from any directory with Python 3.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "certificate-compilation-boundary-20261009/compiler.py"
SOURCE_HASH = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
spec = importlib.util.spec_from_file_location("inherited_cost_compiler", SOURCE)
C = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = C
spec.loader.exec_module(C)
EXACT_SOURCE = HERE.parent / "source-sensitive-proof-compilation-20261009/guarded_compiler.py"
EXACT_SOURCE_HASH = hashlib.sha256(EXACT_SOURCE.read_bytes()).hexdigest()
exact_spec = importlib.util.spec_from_file_location("inherited_exact_compiler", EXACT_SOURCE)
G = importlib.util.module_from_spec(exact_spec)
sys.modules[exact_spec.name] = G
exact_spec.loader.exec_module(G)


def grammar(n, sets, binary=False):
    js = [f"s{j}" for j in range(len(sets))] + [f"x{i}" for i in range(n)]
    rs = [C.Rule(f"choose{j}", f"s{j}", (), frozenset(), 1)
          for j in range(len(sets))]
    rs += [C.Rule(f"member{i}_{j}", f"x{i}", (f"s{j}",), frozenset(), 0)
           for i in range(n) for j, s in enumerate(sets) if i in s]
    if binary and n > 1:
        rs.append(C.Rule("prefix1", "a1", ("x0", "x1"), frozenset(), 0))
        js.append("a1")
        for i in range(2, n):
            js.append(f"a{i}")
            rs.append(C.Rule(f"prefix{i}", f"a{i}", (f"a{i-1}", f"x{i}"), frozenset(), 0))
        premises = (f"a{n-1}",)
    else:
        premises = tuple(f"x{i}" for i in range(n))
    js.append("goal")
    rs.append(C.Rule("finish", "goal", premises, frozenset(), 0))
    return tuple(js), tuple(rs)


def covers(n, sets):
    return [tuple(j for j, flag in enumerate(flags) if flag)
            for flags in product((False, True), repeat=len(sets))
            if set(range(n)) <= set().union(*(sets[j] for j, flag in enumerate(flags) if flag))]


def minimum(front):
    if not front:
        return None
    assert all(s == frozenset() for s, _ in front)
    return int(min(c for _, c in front))


def cover_witness(n, sets, selected):
    # Assign each element one selected covering set, discard selected sets unused
    # by this assignment, and create one paid node per remaining set identity.
    assigned = [next(j for j in selected if i in sets[j]) for i in range(n)]
    nodes, refs = [], {}
    for j in sorted(set(assigned)):
        refs[j] = len(nodes)
        nodes.append((C.Rule(f"choose{j}", f"s{j}", (), frozenset(), 1), ()))
    elements = []
    for i, j in enumerate(assigned):
        elements.append(len(nodes))
        nodes.append((C.Rule(f"member{i}_{j}", f"x{i}", (f"s{j}",), frozenset(), 0), (refs[j],)))
    nodes.append((C.Rule("finish", "goal", tuple(f"x{i}" for i in range(n)), frozenset(), 0), tuple(elements)))
    return C.Dag(tuple(nodes), len(nodes) - 1)


def used_sets(witness):
    return {int(rule.head[1:]) for rule, _ in witness.nodes if rule.head.startswith("s")}


def check_case(n, sets, binary=False):
    js, rs = grammar(n, sets, binary)
    cv = covers(n, sets)
    expected = min(map(len, cv), default=None)
    tree, _ = C.compile_tree(js, rs)
    dag = C.compile_dag(js, rs)
    assert minimum(dag["goal"]) == expected
    assert minimum(tree["goal"]) == (n if cv else None)
    for pair, witness in dag["goal"].items():
        head, support, cost, size = C.dag_value(witness)
        chosen = used_sets(witness)
        assert set(range(n)) <= set().union(*(sets[j] for j in chosen))
        assert len(chosen) <= cost
        assert size <= len(js)
        assert (support, cost) == pair and head == "goal"
    for selected in cv:
        witness = cover_witness(n, sets, selected)
        _, support, cost, _ = C.dag_value(witness)
        assert support == frozenset() and cost <= len(selected)
    return len(cv)


def check_exact_support(n, sets):
    target = frozenset(range(n))
    cv = covers(n, sets)
    expected = min(map(len, cv), default=None)
    looping = (G.Rule("seed", "q", (), frozenset(), 0),) + tuple(
        G.Rule(f"add{j}", "q", ("q",), s, 1) for j, s in enumerate(sets))
    table, _ = G.compile_exact(("q",), tuple(range(n)), looping)
    row = table["q"].get(target)
    assert (int(row[0]) if row else None) == expected
    if row:
        assert G.tree_value(row[1], looping)[:3] == ("q", target, expected)
    # Relaxing exact support to support contained in the available inventory
    # changes the objective: the empty-support seed always wins at price zero.
    assert min(cost for support, (cost, _) in table["q"].items() if support <= target) == 0

    js = tuple(f"q{j}" for j in range(len(sets)+1))
    chain = [G.Rule("seed", "q0", (), frozenset(), 0)]
    for j, s in enumerate(sets, 1):
        chain.extend((G.Rule(f"skip{j}", f"q{j}", (f"q{j-1}",), frozenset(), 0),
                      G.Rule(f"take{j}", f"q{j}", (f"q{j-1}",), s, 1)))
    table, _ = G.compile_exact(js, tuple(range(n)), tuple(chain))
    row = table[js[-1]].get(target)
    assert (int(row[0]) if row else None) == expected
    if row:
        q, support, cost, height, size = G.tree_value(row[1], tuple(chain))
        assert (q, support, cost) == (js[-1], target, expected)
        assert height == size == len(sets)+1
        path, cursor = [], row[1]
        while True:
            path.append(cursor.rule)
            if not cursor.children:
                break
            cursor = cursor.children[0]
        assert len({rule.head for rule in path}) == len(path)
        nodes = tuple((rule, () if i == 0 else (i-1,)) for i, rule in enumerate(reversed(path)))
        assert C.dag_value(C.Dag(nodes, len(nodes)-1))[:3] == (js[-1], target, expected)


def main():
    count, forward_witnesses = 0, 0
    for n in range(4):
        for m in range(4):
            for bits in product((False, True), repeat=n*m):
                sets = tuple(frozenset(i for i in range(n) if bits[j*n+i]) for j in range(m))
                forward_witnesses += check_case(n, sets)
                check_exact_support(n, sets)
                count += 1
    binary_cases = [
        (0, ()), (1, (frozenset(),)), (1, (frozenset({0}),)),
        (3, (frozenset({0, 1, 2}),)),
        (3, (frozenset({0}), frozenset({1}), frozenset({2}))),
        (3, (frozenset({0, 1}), frozenset({1, 2}))),
    ]
    for n, sets in binary_cases:
        check_case(n, sets, binary=True)

    # Explicit arbitrary witness with duplicate paid occurrences of one label.
    s = C.Rule("choose0", "s0", (), frozenset(), 1)
    x0 = C.Rule("member0_0", "x0", ("s0",), frozenset(), 0)
    x1 = C.Rule("member1_0", "x1", ("s0",), frozenset(), 0)
    r = C.Rule("finish", "goal", ("x0", "x1"), frozenset(), 0)
    duplicate = C.Dag(((s, ()), (s, ()), (x0, (0,)), (x1, (1,)), (r, (2, 3))), 4)
    assert C.dag_value(duplicate)[2] == 2
    assert len(used_sets(duplicate)) == 1
    assert C.dag_value(C.prune_dag(duplicate))[2] == 1

    # Fixed complete witness checking differs from certifying that it is cheapest.
    sets = (frozenset({0}), frozenset({1}), frozenset({0, 1}))
    independently_selected = cover_witness(2, sets, (0, 1))
    globally_shared = cover_witness(2, sets, (2,))
    assert C.dag_value(independently_selected)[2] == 2
    assert C.dag_value(globally_shared)[2] == 1

    # Sum→max is not a sharing correction: disjoint paid leaves still cost two.
    singles = (frozenset({0}), frozenset({1}))
    assert C.dag_value(cover_witness(2, singles, (0, 1)))[2] == 2
    wrong_max = max(1, 1)
    assert wrong_max == 1

    # Omitting an uncovered obligation changes provability, not only price.
    js, rs = grammar(2, (frozenset({0}),))
    assert not C.compile_dag(js, rs)["goal"]
    bad_rs = rs[:-1] + (C.Rule("finish", "goal", ("x0",), frozenset(), 0),)
    assert minimum(C.compile_dag(js, bad_rs)["goal"]) == 1
    # Charging every structural check positively adds only a fixed offset here.
    for n, sets in binary_cases:
        js, rs = grammar(n, sets)
        unit = tuple(C.Rule(r.name, r.head, r.premises, r.support, 1) for r in rs)
        cv = covers(n, sets)
        expected = min(map(len, cv), default=None)
        assert minimum(C.compile_dag(js, unit)["goal"]) == (n + 1 + expected if cv else None)
        tree, _ = C.compile_tree(js, unit)
        assert minimum(tree["goal"]) == (2*n + 1 if cv else None)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH
    assert hashlib.sha256(EXACT_SOURCE.read_bytes()).hexdigest() == EXACT_SOURCE_HASH
    result = {
        "status": "PASS", "set_systems_checked": count,
        "cover_to_dag_witnesses_checked": forward_witnesses,
        "binary_goal_controls": len(binary_cases),
        "exact_support_loop_and_acyclic_chain_instances_each": count,
        "controls": {
            "empty_universe_zero_cost": "PASS",
            "uncovered_element_no_proof": "PASS",
            "tree_cost_equals_universe_size_when_coverable": "PASS",
            "shared_cost_equals_cover_minimum": "PASS",
            "duplicate_paid_set_nodes_do_not_help": "PASS",
            "local_ties_can_lose_sharing": {"independent": 2, "shared": 1},
            "max_aggregation_false_fix": {"incorrect": 1, "actual": 2},
            "dropped_obligation_false_fix": "REJECTED_BY_ORIGINAL_GRAMMAR",
            "all_rules_unit_cost_fixed_offset": "PASS_ON_SIX_CONTROLS",
            "exact_support_chain_tree_and_dag_cost_agree": "PASS",
            "relax_exact_support_to_inventory_subset_gives_zero": "PASS",
        },
        "inherited_compiler_sha256": SOURCE_HASH,
        "inherited_compiler_unchanged": True,
        "inherited_exact_compiler_sha256": EXACT_SOURCE_HASH,
        "inherited_exact_compiler_unchanged": True,
        "limits": "Finite interface controls only. General reduction and NP membership are written proofs; no Lean theorem, solver, performance or approximation claim."
    }
    (HERE / "CHECK_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
