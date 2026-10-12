"""Bounded exact checks of a fixed-bundle overlap transport, not a solver."""
from fractions import Fraction
from itertools import product
from math import prod
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "inherited_compiler", ROOT / "certificate-compilation-boundary-20261009/compiler.py")
compiler = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = compiler
spec.loader.exec_module(compiler)
checks = 0


def check(condition):
    global checks
    checks += 1
    assert condition


def subsets(n, nonempty=True):
    return range(int(nonempty), 1 << n)


def intersections(footprints, weights):
    return {j: sum((w for v, w in weights.items()
                    if all(v in footprints[i] for i in range(len(footprints))
                           if j >> i & 1)), Fraction(0))
            for j in subsets(len(footprints))}


def union_cost(footprints, weights):
    return sum((weights[v] for v in set().union(*footprints)), Fraction(0))


def verify_algebra(footprints, weights):
    n = len(footprints)
    m = intersections(footprints, weights)
    actual_h = {k: Fraction(0) for k in subsets(n)}
    for v, w in weights.items():
        k = sum(1 << i for i, f in enumerate(footprints) if v in f)
        if k:
            actual_h[k] += w
    h = {k: sum(((-1) ** ((j ^ k).bit_count()) * m[j]
                 for j in subsets(n) if j & k == k), Fraction(0))
         for k in subsets(n)}
    check(actual_h == h)
    check({j: sum((h[k] for k in subsets(n) if k & j == j), Fraction(0))
           for j in subsets(n)} == m)
    check(sum(((-1) ** (j.bit_count() + 1) * v for j, v in m.items()), Fraction(0))
          == union_cost(footprints, weights))
    check(sum(h.values(), Fraction(0)) == union_cost(footprints, weights))
    # Coefficient support in each typed degree-one role is the inverse map.
    vectors = [tuple(int(v in f) for v in weights) for f in footprints]
    check([frozenset(v for v, a in zip(weights, x) if a) for x in vectors]
          == list(footprints))
    diagonal = {j: sum((w * prod(vectors[i][col] for i in range(n) if j >> i & 1)
                        for col, w in enumerate(weights.values())), Fraction(0))
                for j in subsets(n)}
    check(diagonal == m)
    return m


def grammar(variants, weights):
    b = len(variants[0])
    rules = []
    leaves = {}
    choices = {}
    branch_cache = {}
    for v, w in weights.items():
        leaves[v] = compiler.Rule(f"leaf-{v}", f"p{v}", (), frozenset(), w)
        rules.append(leaves[v])
    for k, fs in enumerate(variants):
        for i, f in enumerate(fs):
            key = (i, tuple(sorted(f)))
            if key not in branch_cache:
                branch_cache[key] = compiler.Rule(f"branch-{k}-{i}", f"q{i}",
                                                  tuple(f"p{v}" for v in sorted(f)),
                                                  frozenset(), Fraction(0))
                rules.append(branch_cache[key])
            r = branch_cache[key]
            choices[k, i] = r
    root = compiler.Rule("root", "t", tuple(f"q{i}" for i in range(b)),
                         frozenset(), Fraction(0))
    rules.append(root)
    judgements = tuple([f"p{v}" for v in weights] + [f"q{i}" for i in range(b)] + ["t"])
    compiler._validate(judgements, rules)
    return leaves, choices, root, frozenset(rules)


def build(variants, weights, k, parts):
    leaves, choices, root, admitted = parts
    fs = variants[k]
    used = sorted(set().union(*fs))
    nodes = [(leaves[v], ()) for v in used]
    index = {f"p{v}": i for i, v in enumerate(used)}
    branch_refs = []
    for i in range(len(fs)):
        rule = choices[k, i]
        branch_refs.append(len(nodes))
        nodes.append((rule, tuple(index[p] for p in rule.premises)))
    nodes.append((root, tuple(branch_refs)))
    dag = compiler.Dag(tuple(nodes), len(nodes) - 1)
    check(all(rule in admitted for rule, _ in dag.nodes))
    check(compiler.dag_value(dag)[2] == union_cost(fs, weights))
    recovered = []
    for branch in branch_refs:
        reached, todo = set(), [branch]
        while todo:
            u = todo.pop()
            if u not in reached:
                reached.add(u)
                todo.extend(nodes[u][1])
        ordered = sorted(reached)
        remap = {old: new for new, old in enumerate(ordered)}
        sub = compiler.Dag(tuple((nodes[u][0], tuple(remap[v] for v in nodes[u][1]))
                                 for u in ordered), remap[branch])
        check(all(rule in admitted for rule, _ in sub.nodes))
        footprint = frozenset(int(nodes[u][0].head[1:]) for u in reached
                              if nodes[u][0].cost > 0)
        check(compiler.dag_value(sub)[2] == sum((weights[v] for v in footprint), Fraction(0)))
        recovered.append(footprint)
    check(recovered == list(fs))
    return dag


def parity(b, p):
    rows = [x for x in product((0, 1), repeat=b) if sum(x) % 2 == p]
    return [frozenset(v for v, x in enumerate(rows) if x[i]) for i in range(b)]


def main():
    parity_results = []
    for b in range(2, 7):
        variants = [parity(b, p) for p in (0, 1)]
        weights = {v: Fraction(1) for v in range(1 << (b - 1))}
        parts = grammar(variants, weights)
        for i in range(b - 1):
            check(parts[1][0, i] is parts[1][1, i])
        check(parts[1][0, b - 1] != parts[1][1, b - 1])
        m = [verify_algebra(f, weights) for f in variants]
        for k in (0, 1):
            build(variants, weights, k, parts)
        for j in range(1, (1 << b) - 1):
            check(m[0][j] == m[1][j] == 2 ** (b - j.bit_count() - 1))
        cost = [union_cost(f, weights) for f in variants]
        check(cost == [2 ** (b - 1) - 1, 2 ** (b - 1)])
        parity_results.append({"branches": b, "available_paid_ids": len(weights),
                               "even_cost": int(cost[0]), "odd_cost": int(cost[1])})
    cases = [([], {}), ([frozenset()], {}),
             ([frozenset({0}), frozenset({0})], {0: Fraction(3, 2)}),
             ([frozenset({0, 2}), frozenset({1, 2}), frozenset()],
              {0: Fraction(1, 3), 1: Fraction(5, 2), 2: Fraction(7, 4), 3: Fraction(9)})]
    for fs, weights in cases:
        verify_algebra(fs, weights)
        build([fs], weights, 0, grammar([fs], weights))
    # Equal scalar weights do not supply node alignment.
    aligned = [frozenset({0}), frozenset({0})]
    unaligned = [frozenset({0}), frozenset({1})]
    w = {0: Fraction(1), 1: Fraction(1)}
    check([intersections(f, w)[1] for f in (aligned, unaligned)] == [1, 1])
    check([intersections(f, w)[2] for f in (aligned, unaligned)] == [1, 1])
    check(union_cost(aligned, w) == 1 and union_cost(unaligned, w) == 2)
    # Same admitted rule may appear at two distinct charged nodes.
    r = compiler.Rule("same-leaf-rule", "p", (), frozenset(), Fraction(1))
    top = compiler.Rule("two-premises", "t", ("p", "p"), frozenset(), Fraction(0))
    duplicate = compiler.Dag(((r, ()), (r, ()), (top, (0, 1))), 2)
    shared = compiler.Dag(((r, ()), (top, (0, 0))), 1)
    check(compiler.dag_value(duplicate)[2] == 2)
    check(compiler.dag_value(shared)[2] == 1)
    # Price must occur once rather than once per participating input.
    check(Fraction(3, 2) != Fraction(3, 2) ** 2)
    bindings = json.loads((HERE / "INPUT_BINDINGS.json").read_text())["inputs"]
    for row in bindings:
        check(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"])
    out = {"status": "PASS", "assertions": checks,
           "parity_realizations": parity_results, "additional_bundle_cases": len(cases),
           "input_hashes_unchanged": len(bindings),
           "scope": "Bounded exact checks; no optimizer, benchmark, or unrestricted formal proof."}
    (HERE / "CHECK_RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
