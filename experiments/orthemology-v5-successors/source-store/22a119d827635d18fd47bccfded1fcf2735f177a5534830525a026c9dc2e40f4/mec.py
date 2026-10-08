"""Iterative maximal end components of a finite state/action pair set.

All positive successors of a retained action must remain inside its state set.
No parity conditions or nonrevelation assumptions are applied by this module.
"""
from dependencies import checked_pairs, natural, used


def _strongly_connected(states, edges):
    """Iterative Kosaraju decomposition, including zero-outdegree singletons."""
    seen, finish = set(), []
    for source in sorted(states):
        if source in seen:
            continue
        seen.add(source)
        pending = [(source, iter(sorted(edges[source])))]
        while pending:
            state, targets = pending[-1]
            target = next(targets, None)
            if target is None:
                finish.append(state)
                pending.pop()
            elif target not in seen:
                seen.add(target)
                pending.append((target, iter(sorted(edges[target]))))
    reverse = {s: set() for s in states}
    for source in states:
        for target in edges[source]:
            reverse[target].add(source)
    assigned, components = set(), []
    for source in reversed(finish):
        if source in assigned:
            continue
        component, pending = {source}, [source]
        assigned.add(source)
        while pending:
            for target in reverse[pending.pop()]:
                if target not in assigned:
                    assigned.add(target)
                    component.add(target)
                    pending.append(target)
        components.append(frozenset(component))
    return tuple(sorted(components, key=lambda c: tuple(sorted(c))))


def maximal_components(model, theta, pairs):
    """Return canonical, pair-maximal candidate end components.

Each nonterminal work item splits its states into at least two SCCs. There
are at most 2*n-1 processed nonempty state sets, with no recursive Python
calls and no state/action subset enumeration.
"""
    natural(theta, 2)
    pairs = tuple(sorted(checked_pairs(model, pairs)))
    if not pairs:
        return ()
    support = {(s, a): frozenset(y for y, p in enumerate(model.rows[theta][s][a]) if p)
               for s, a in pairs}
    pending, result = [used(pairs)], []
    while pending:
        states = pending.pop()
        retained = tuple(e for e in pairs if e[0] in states and support[e] <= states)
        edges = {s: set() for s in states}
        for pair in retained:
            edges[pair[0]].update(support[pair])
        components = _strongly_connected(states, edges)
        if len(components) == 1:
            if used(retained) == states:
                result.append(retained)
            # A single SCC without a departing action can only be a singleton.
        else:
            pending.extend(reversed(components))
    return tuple(sorted(result))
