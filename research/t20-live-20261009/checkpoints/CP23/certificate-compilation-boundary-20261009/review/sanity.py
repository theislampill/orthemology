"""Independent bounded control for the earliest-representative construction.

No import from the submitted implementation. Nodes use topological IDs, and a
node's rule is fixed by its judgement, its ordered child judgements, support,
and local price. Repeated children and zero charges are included.
"""
from itertools import product
import json


def reachable(children, root):
    seen = set()
    todo = [root]
    while todo:
        node = todo.pop()
        if node not in seen:
            seen.add(node)
            todo.extend(children[node])
    return seen


def argument_lists(before):
    return [()] + [(x,) for x in range(before)] + list(product(range(before), repeat=2))


def main():
    checked = 0
    redirected = 0
    lower_cost = 0
    smaller_support = 0
    for size in range(1, 4):
        for child_tuples in product(*(argument_lists(i) for i in range(size))):
            if reachable(child_tuples, size - 1) != set(range(size)):
                continue
            for judgements in product(range(2), repeat=size):
                representatives = {q: judgements.index(q) for q in set(judgements)}
                new_children = {
                    node: tuple(representatives[judgements[c]] for c in child_tuples[node])
                    for node in representatives.values()
                }
                root = representatives[judgements[size - 1]]
                live = reachable(new_children, root)
                assert len({judgements[i] for i in live}) == len(live)
                assert judgements[root] == judgements[size - 1]
                for node in live:
                    assert len(new_children[node]) == len(child_tuples[node])
                    assert all(c < node for c in new_children[node])
                    assert tuple(judgements[c] for c in new_children[node]) == tuple(
                        judgements[c] for c in child_tuples[node]
                    )
                for supports in product(range(4), repeat=size):
                    old_support = 0
                    new_support = 0
                    for i in range(size):
                        old_support |= supports[i]
                    for i in live:
                        new_support |= supports[i]
                    assert new_support & old_support == new_support
                    for costs in product(range(2), repeat=size):
                        old_cost = sum(costs)
                        new_cost = sum(costs[i] for i in live)
                        assert new_cost <= old_cost
                        checked += 1
                        redirected += any(new_children[i] != child_tuples[i] for i in live)
                        lower_cost += new_cost < old_cost
                        smaller_support += new_support != old_support
    result = {
        'status': 'passed',
        'finite_root_reachable_dags_checked': checked,
        'models_with_actual_redirection': redirected,
        'models_with_strictly_lower_cost': lower_cost,
        'models_with_strictly_smaller_support': smaller_support,
        'scope': '1-3 nodes; 2 judgement labels; 2 evidence tokens; ordered arity 0-2; weights 0 or 1',
        'limitations': 'A finite independent control, not a kernel proof or exhaustive proof of the general theorem.'
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
