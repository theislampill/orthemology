#!/usr/bin/env python3
"""Exact finite controls for the declared adapter; no metaphysical certification."""
from fractions import Fraction
from itertools import product, permutations
from collections import deque
from pathlib import Path
import hashlib
import json


COUNTS = {}


def check(group, proposition):
    if not proposition:
        raise AssertionError(group)
    COUNTS[group] = COUNTS.get(group, 0) + 1


def ident(n):
    return tuple(range(n))


def compose(q, p):
    """q after p."""
    return tuple(q[x] for x in p)


def inverse(p):
    q = [None] * len(p)
    for x, y in enumerate(p):
        q[y] = x
    return tuple(q)


def all_filters(n, worlds):
    sets = [frozenset(i for i in range(n) if mask & (1 << i))
            for mask in range(1 << n)]
    return product(sets, repeat=worlds)


def direct_sections(n, worlds, edges, filters):
    """Definition by tuples; independent of tree/holonomy construction."""
    return {s for s in product(range(n), repeat=worlds)
            if all(s[w] in filters[w] for w in range(worlds))
            and all(g[s[v]] == s[w] for (v, w), g in edges.items())}


def tensor_value(n, worlds, edges, filters, boolean):
    """Explicit product of characteristic-array coefficients then contraction."""
    scalar = 0
    for s in product(range(n), repeat=worlds):
        coeff = 1
        for w in range(worlds):
            coeff *= int(s[w] in filters[w])
        for (v, w), g in edges.items():
            alignment_tensor = int(s[w] == g[s[v]])
            coeff *= alignment_tensor
        scalar = int(bool(scalar or coeff)) if boolean else scalar + coeff
    return scalar


def tree_data(n, worlds, edges, root=0, reverse_order=False):
    adjacency = [[] for _ in range(worlds)]
    for (v, w), g in edges.items():
        adjacency[v].append((w, g))
        adjacency[w].append((v, inverse(g)))
    charts = {root: ident(n)}
    todo = deque([root])
    while todo:
        v = todo.popleft()
        for w, g in sorted(adjacency[v], reverse=reverse_order):
            if w not in charts:
                charts[w] = compose(g, charts[v])
                todo.append(w)
    if len(charts) != worlds:
        raise ValueError("Connected alignment graph required")
    cycles = {edge: compose(inverse(charts[w]), compose(g, charts[v]))
              for edge, g in edges.items() for v, w in [edge]}
    fixed = frozenset(b for b in range(n)
                      if all(h[b] == b for h in cycles.values()))
    return charts, cycles, fixed


def root_sections(n, worlds, edges, filters, reverse_order=False):
    charts, cycles, fixed = tree_data(n, worlds, edges,
                                     reverse_order=reverse_order)
    accepted = {b for b in fixed
                if all(charts[w][b] in filters[w] for w in range(worlds))}
    return {tuple(charts[w][b] for w in range(worlds)) for b in accepted}


def gauge(edges, filters, pi):
    renamed_edges = {(v, w): compose(pi[w], compose(g, inverse(pi[v])))
                     for (v, w), g in edges.items()}
    renamed_filters = tuple(frozenset(pi[w][x] for x in a)
                            for w, a in enumerate(filters))
    return renamed_edges, renamed_filters


def exhaustive_triangle():
    cases = 0
    gauge_cases = 0
    coherent_counts = {}
    for n in range(4):
        perms = list(permutations(range(n)))
        coherent_counts[n] = 0
        for graph_index, gs in enumerate(product(perms, repeat=3)):
            edges = dict(zip(((0, 1), (0, 2), (1, 2)), gs))
            charts, cycles, fixed = tree_data(n, 3, edges)
            coherent = all(h == ident(n) for h in cycles.values())
            coherent_counts[n] += int(coherent)
            check("full_coherence_iff_all_sections", coherent == (len(fixed) == n))
            for filters in all_filters(n, 3):
                expected = direct_sections(n, 3, edges, filters)
                result = root_sections(n, 3, edges, filters)
                check("triangle_root_vs_tuples", result == expected)
                check("triangle_boolean_tensor", tensor_value(n, 3, edges, filters, True)
                      == int(bool(expected)))
                check("triangle_count_tensor", tensor_value(n, 3, edges, filters, False)
                      == len(expected))
                check("triangle_count_bound", len(expected) <= n)
                if coherent:
                    common_axis = {b for b in range(n)
                                   if all(charts[w][b] in filters[w] for w in range(3))}
                    check("coherent_and_before_or", len(expected) == len(common_axis))
                cases += 1
            # Every possible gauge is checked for every triangle edge table.
            # Filters vary deterministically across those cases, not just all-true.
            for gauge_index, pi in enumerate(product(perms, repeat=3)):
                filters = tuple(frozenset(x for x in range(n)
                                 if ((graph_index + 3 * gauge_index + w) % (1 << n))
                                 & (1 << x)) for w in range(3))
                expected = direct_sections(n, 3, edges, filters)
                ep, ap = gauge(edges, filters, pi)
                expected_renamed = {tuple(pi[w][s[w]] for w in range(3)) for s in expected}
                check("gauge_section_bijection",
                      direct_sections(n, 3, ep, ap) == expected_renamed)
                tp, hp, kp = tree_data(n, 3, ep)
                check("gauge_holonomy_conjugacy", all(
                    hp[e] == compose(pi[0], compose(h, inverse(pi[0])))
                    for e, h in cycles.items()))
                check("gauge_fixed_set", kp == frozenset(pi[0][b] for b in fixed))
                gauge_cases += 1
    check("coherent_triangle_counts", coherent_counts == {0: 1, 1: 1, 2: 4, 3: 36})
    return {"tuple_filter_cases": cases, "gauge_cases": gauge_cases,
            "coherent_edge_tables_by_n": coherent_counts}


def group_generated(n, generators):
    found = {ident(n)}
    todo = [ident(n)]
    while todo:
        p = todo.pop()
        for g in generators:
            h = compose(g, p)
            if h not in found:
                found.add(h)
                todo.append(h)
    return found


def holonomy_controls():
    i2, swap = (0, 1), (1, 0)
    edges = {(0, 1): i2, (0, 2): i2, (1, 2): swap}
    filters = ({0, 1},) * 3
    check("swap_no_point", not direct_sections(2, 3, edges, filters))
    uniform = (Fraction(1, 2), Fraction(1, 2))
    check("swap_normalized_parallel_average", sum(uniform) == 1
          and all(tuple(uniform[inverse(g)[x]] for x in range(2)) == uniform
                  for g in edges.values()))
    check("swap_average_not_copyable", not is_copyable(uniform))
    check("swap_boolean_parallel_not_copyable", not is_copyable((1, 1), boolean=True))
    # Two independent cycles; every holonomy element fixes something, no common point.
    h1 = (0, 1, 3, 2, 5, 4)
    h2 = (1, 0, 2, 3, 5, 4)
    group = group_generated(6, (h1, h2))
    check("all_loops_have_individual_fix", len(group) == 4
          and all(any(h[x] == x for x in range(6)) for h in group))
    check("no_common_loop_fixed_point", not any(
        all(h[x] == x for h in group) for x in range(6)))
    edges6 = {(0, 1): ident(6), (1, 2): ident(6), (0, 2): h1,
              (0, 3): ident(6), (3, 4): ident(6), (0, 4): h2}
    check("two_cycle_no_section", not direct_sections(6, 5, edges6, (set(range(6)),) * 5))
    # Check this graph, then a square where reversing BFS really changes the tree.
    for generators in ((h1, h2), (h1, ident(6)), (ident(6), ident(6))):
        altered = dict(edges6)
        altered[(0, 2)], altered[(0, 4)] = generators
        for filters in ((set(range(6)),) * 5,
                        ({0, 2, 4}, {0, 1, 2}, {0, 2}, {0, 3}, {0, 5})):
            check("tree_choice_independence",
                  root_sections(6, 5, altered, filters) ==
                  root_sections(6, 5, altered, filters, reverse_order=True))
    different_charts = 0
    for gs in product(permutations(range(3)), repeat=4):
        square = dict(zip(((0, 1), (0, 2), (1, 3), (2, 3)), gs))
        t1, _, k1 = tree_data(3, 4, square)
        t2, _, k2 = tree_data(3, 4, square, reverse_order=True)
        different_charts += int(t1 != t2)
        check("different_tree_same_fixed_points", k1 == k2)
        for af in (({0, 1, 2},) * 4, ({0, 2}, {0, 1}, {1, 2}, {0, 1, 2})):
            check("different_tree_same_sections", root_sections(3, 4, square, af) ==
                  root_sections(3, 4, square, af, reverse_order=True))
    check("alternate_tree_test_nontrivial", different_charts > 0)
    return {"swap_fixed_labels": 0, "v4_group_size": len(group),
            "v4_fixed_labels_per_element": sorted(sum(h[x] == x for x in range(6)) for h in group),
            "v4_common_fixed_labels": 0, "square_cases_with_different_tree_charts": different_charts}


def is_copyable(z, boolean=False, modulus=None):
    def mul(x, y):
        return x * y if modulus is None else (x * y) % modulus
    eps = int(any(z)) if boolean else sum(z)
    if modulus is not None:
        eps %= modulus
    return eps == 1 and all(
        (z[i] if i == j else 0) == mul(z[i], z[j])
        for i in range(len(z)) for j in range(len(z)))


def copy_controls():
    real_cases, boolean_cases = 0, 0
    for n in range(5):
        for z in product((Fraction(-1), Fraction(0), Fraction(1, 2), Fraction(1), Fraction(2)), repeat=n):
            one_hot = sum(c == 1 for c in z) == 1 and all(c in (0, 1) for c in z)
            check("real_copyable_iff_onehot", is_copyable(z) == one_hot)
            real_cases += 1
        for z in product((0, 1), repeat=n):
            check("boolean_copyable_iff_onehot", is_copyable(z, boolean=True) == (sum(z) == 1))
            boolean_cases += 1
    check("z6_exception", is_copyable((3, 4), modulus=6))
    return {"real_grid_vectors": real_cases, "boolean_vectors": boolean_cases,
            "ring_counterexample": {"modulus": 6, "vector": [3, 4]}}


def received(dep, target, sources):
    return any((source, target) in dep for source in sources)


def witness_lifting_controls():
    back_cases = 0
    strict_weaker_examples = 0
    for n in range(4):
        all_edges = list(product(range(n), repeat=2))
        for bits in product((False, True), repeat=n * n):
            dep = {edge for edge, yes in zip(all_edges, bits) if yes}
            for retained in all_filters(n, 1):
                retained = retained[0]
                for b in retained:
                    full = received(dep, b, range(n))
                    restricted = received(dep, b, retained)
                    back = not full or restricted
                    check("back_iff_received_equivalence", back == (full == restricted))
                    check("back_iff_nonreceipt_equivalence", back == ((not full) == (not restricted)))
                    check("retained_witness_maps_forward", not restricted or full)
                    if back and any((c, b) in dep for c in set(range(n)) - retained):
                        strict_weaker_examples += 1
                    back_cases += 1
    # Nontrivial holonomy retains target 2 but erases sole supplier 0.
    edges = {(0, 1): (0, 1, 2), (0, 2): (0, 1, 2), (1, 2): (1, 0, 2)}
    _, _, retained = tree_data(3, 3, edges)
    dep = {(0, 2)}
    check("fixed_section_erases_receipt", retained == {2}
          and received(dep, 2, range(3)) and not received(dep, 2, retained))
    check("fixed_section_erases_realisation", any(y == 0 for y in range(3))
          and not any(y == 0 for y in retained))
    # Trivial holonomy, necessary target 0; contingent suppliers 1 and 2.
    E = ({0, 1}, {0, 2})
    deps = ({(1, 0)}, {(2, 0)})
    necessary = set.intersection(*map(set, E))
    check("trivial_holonomy_necessary_filter_erases_receipt", necessary == {0}
          and all(received(dep, 0, range(3)) and not received(dep, 0, necessary)
                  for dep in deps))
    check("contingent_suppliers_exist_locally", all(
        all(c in E[w] and b in E[w] for c, b in deps[w]) for w in range(2)))
    check("variable_supplier_generic_reception", all(
        not any(received(dep, b, range(3)) for dep in deps)
        or all(b not in E[w] or received(deps[w], b, range(3)) for w in range(2))
        for b in range(3)))
    check("back_weaker_than_all_suppliers", strict_weaker_examples > 0)
    return {"back_condition_cases": back_cases,
            "back_holds_with_omitted_supplier_cases": strict_weaker_examples}


def guards_and_loss():
    # Known local-isomorphism loss; passive transport repairs it exactly.
    g = {(0, 1): (0, 1)}
    yes = ({0}, {0})
    no = ({0}, {1})
    check("known_de_re_quantifier_loss", bool(direct_sections(2, 2, g, yes))
          and not direct_sections(2, 2, g, no) and all(no))
    gp, ap = gauge(g, yes, ((0, 1), (1, 0)))
    check("covariant_local_rename_repair", ap == (frozenset({0}), frozenset({1}))
          and gp[(0, 1)] == (1, 0) and bool(direct_sections(2, 2, gp, ap)))
    check("empty_carrier_no_bearer", not direct_sections(0, 1, {}, (set(),))
          and tensor_value(0, 1, {}, (set(),), True) == 0)
    check("nonempty_carrier_empty_existence", not direct_sections(2, 1, {}, (set(),)))
    check("single_actual_world", direct_sections(2, 1, {}, ({1},)) == {(1,)})
    box_empty = all(False for _ in ())
    check("vacuous_box_no_actual_witness", box_empty and not any(
        False and box_empty for _ in range(2)))
    check("vacuous_box_actual_only", any(b == 0 and box_empty for b in range(2)))
    try:
        tree_data(1, 2, {})
    except ValueError:
        check("disconnected_graph_rejected", True)
    else:
        raise AssertionError("disconnected_graph_rejected")


def main():
    result = {"status": "PASS", "scope": "Exact finite mathematical controls only",
              "triangles": exhaustive_triangle(), "copyability": copy_controls(),
              "holonomy": holonomy_controls(), "witness_lifting": witness_lifting_controls()}
    guards_and_loss()
    result["assertions_by_group"] = COUNTS
    result["total_assertions"] = sum(COUNTS.values())
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
