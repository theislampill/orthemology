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


def checked_dag(witness, rules):
    if any(rule not in rules for rule, _ in witness.nodes):
        raise ValueError("A DAG node uses a rule outside the admitted grammar.")
    return C.dag_value(witness)


def checked_tree(witness, rules):
    pending = [witness]
    while pending:
        node = pending.pop()
        if node.rule not in rules:
            raise ValueError("A tree node uses a rule outside the admitted grammar.")
        pending.extend(node.children)
    return C.tree_value(witness)


def check_frontiers(tree, dag, rules):
    for q, frontier in tree.items():
        for (support, cost), witness in frontier.items():
            assert checked_tree(witness, rules)[:3] == (q, support, cost)
    for q, frontier in dag.items():
        for (support, cost), witness in frontier.items():
            assert checked_dag(witness, rules)[:3] == (q, support, cost)


def check_exact_table(table, rules):
    for q, rows in table.items():
        for support, (cost, witness) in rows.items():
            assert G.tree_value(witness, rules)[:3] == (q, support, cost)


def cover_witness(n, sets, selected, binary=False):
    # Assign each element one selected covering set, discard selected sets unused
    # by this assignment, and create one paid node per remaining set identity.
    _, rules = grammar(n, sets, binary)
    by_name = {r.name: r for r in rules}
    assigned = [next(j for j in selected if i in sets[j]) for i in range(n)]
    nodes, refs = [], {}
    for j in sorted(set(assigned)):
        refs[j] = len(nodes)
        nodes.append((by_name[f"choose{j}"], ()))
    elements = []
    for i, j in enumerate(assigned):
        elements.append(len(nodes))
        nodes.append((by_name[f"member{i}_{j}"], (refs[j],)))
    if binary and n > 1:
        nodes.append((by_name["prefix1"], (elements[0], elements[1])))
        for i in range(2, n):
            nodes.append((by_name[f"prefix{i}"], (len(nodes)-1, elements[i])))
        final_refs = (len(nodes)-1,)
    else:
        final_refs = tuple(elements)
    nodes.append((by_name["finish"], final_refs))
    return C.Dag(tuple(nodes), len(nodes) - 1)


def used_sets(witness):
    return {int(rule.head[1:]) for rule, _ in witness.nodes if rule.head.startswith("s")}


def check_case(n, sets, binary=False):
    js, rs = grammar(n, sets, binary)
    cv = covers(n, sets)
    expected = min(map(len, cv), default=None)
    tree, _ = C.compile_tree(js, rs)
    dag = C.compile_dag(js, rs)
    check_frontiers(tree, dag, rs)
    assert minimum(dag["goal"]) == expected
    assert minimum(tree["goal"]) == (n if cv else None)
    for pair, witness in dag["goal"].items():
        head, support, cost, size = checked_dag(witness, rs)
        chosen = used_sets(witness)
        assert set(range(n)) <= set().union(*(sets[j] for j in chosen))
        assert len(chosen) <= cost
        assert size <= len(js)
        assert (support, cost) == pair and head == "goal"
    for selected in cv:
        witness = cover_witness(n, sets, selected, binary)
        _, support, cost, _ = checked_dag(witness, rs)
        assert support == frozenset() and cost <= len(selected)
    return len(cv)


def check_exact_support(n, sets):
    target = frozenset(range(n))
    cv = covers(n, sets)
    expected = min(map(len, cv), default=None)
    looping = (G.Rule("seed", "q", (), frozenset(), 0),) + tuple(
        G.Rule(f"add{j}", "q", ("q",), s, 1) for j, s in enumerate(sets))
    table, _ = G.compile_exact(("q",), tuple(range(n)), looping)
    check_exact_table(table, looping)
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
    check_exact_table(table, tuple(chain))
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
        assert checked_dag(C.Dag(nodes, len(nodes)-1), tuple(chain))[:3] == (js[-1], target, expected)


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
    duplicate_rules = (s, x0, x1, r)
    assert checked_dag(duplicate, duplicate_rules)[2] == 2
    assert len(used_sets(duplicate)) == 1
    assert checked_dag(C.prune_dag(duplicate), duplicate_rules)[2] == 1

    # Fixed complete witness checking differs from certifying that it is cheapest.
    sets = (frozenset({0}), frozenset({1}), frozenset({0, 1}))
    independently_selected = cover_witness(2, sets, (0, 1))
    globally_shared = cover_witness(2, sets, (2,))
    _, rules = grammar(2, sets)
    assert checked_dag(independently_selected, rules)[2] == 2
    assert checked_dag(globally_shared, rules)[2] == 1

    # Sum→max is not a sharing correction: disjoint paid leaves still cost two.
    singles = (frozenset({0}), frozenset({1}))
    _, rules = grammar(2, singles)
    assert checked_dag(cover_witness(2, singles, (0, 1)), rules)[2] == 2
    wrong_max = max(1, 1)
    assert wrong_max == 1

    # Omitting an uncovered obligation changes provability, not only price.
    js, rs = grammar(2, (frozenset({0}),))
    assert not C.compile_dag(js, rs)["goal"]
    bad_rs = rs[:-1] + (C.Rule("finish", "goal", ("x0",), frozenset(), 0),)
    bad_dag = C.compile_dag(js, bad_rs)
    check_frontiers({}, bad_dag, bad_rs)
    assert minimum(bad_dag["goal"]) == 1
    # These objects pass structural traversal but fail admission in the stated
    # target grammar. Preserve the binary-control bug as an explicit rejection.
    non_admitted = C.Dag(((C.Rule("invented", "goal", (), frozenset(), 0), ()),), 0)
    assert C.dag_value(non_admitted)[2] == 0
    binary_sets = (frozenset({0, 1, 2}),)
    _, binary_rules = grammar(3, binary_sets, binary=True)
    old_nary = cover_witness(3, binary_sets, (0,), binary=False)
    assert C.dag_value(old_nary)[2] == 1
    for witness, admitted in ((non_admitted, rs), (old_nary, binary_rules)):
        try:
            checked_dag(witness, admitted)
        except ValueError as error:
            assert "outside the admitted grammar" in str(error)
        else:
            raise AssertionError("Unadmitted rule was accepted.")
    assert checked_dag(cover_witness(3, binary_sets, (0,), binary=True), binary_rules)[2] == 1
    # Charging every structural check positively adds only a fixed offset here.
    for n, sets in binary_cases:
        js, rs = grammar(n, sets)
        unit = tuple(C.Rule(r.name, r.head, r.premises, r.support, 1) for r in rs)
        cv = covers(n, sets)
        expected = min(map(len, cv), default=None)
        dag = C.compile_dag(js, unit)
        assert minimum(dag["goal"]) == (n + 1 + expected if cv else None)
        tree, _ = C.compile_tree(js, unit)
        check_frontiers(tree, dag, unit)
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
            "all_claimed_witness_rules_checked_against_admitted_grammar": "PASS",
            "invented_rule_rejected": "PASS",
            "old_nary_witness_rejected_against_binary_rules": "PASS",
            "binary_forward_witness_uses_binary_admitted_rules": "PASS",
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
