"""Exhaustive exact finite synthesis; no complexity or probability-law claim."""
from collections import deque
from model import validate_model
from finite import all_components, reachable, safe_known, safe_uncertain, used, checked_region
from certificates import Positive, Negative, Route, check_positive, check_negative


def known_operator(model, K):
    K = checked_region(model, K)
    pairs = safe_known(model, K)
    components = all_components(model, 1, pairs)
    targets = frozenset(s for c in components for s in used(c))
    return frozenset(s for s in K if reachable(model, s, pairs, 1) & targets)


def uncertain_operator(model, K, W):
    K, W = checked_region(model, K), checked_region(model, W)
    pairs = safe_uncertain(model, K, W)
    winners = set(W)
    for theta in (0, 1):
        components = all_components(model, theta, pairs, True)
        targets = {s for c in components for s in used(c)}
        targets.update(s for s, a in pairs for y in K
                       if model.rows[theta][s][a][y] and not model.rows[0][s][a][y])
        winners.intersection_update(s for s in W if reachable(model, s, pairs, theta, True) & targets)
    return frozenset(winners)


def descend(model, operator):
    region = frozenset(range(model.n_states))
    trace = [tuple(sorted(region))]
    while True:
        next_region = operator(region)
        if not next_region <= region:
            raise RuntimeError('operator failed descent invariant')
        trace.append(tuple(sorted(next_region)))
        if next_region == region:
            return tuple(trace)
        region = next_region


def shortest_route(model, source, theta, pairs, components, K, uncertain):
    """BFS paths; choose shortest total route, then lexicographic edge sequence."""
    queue = deque((source,))
    paths = {source: ()}
    while queue:
        s = queue.popleft()
        for x, a in pairs:
            if x != s:
                continue
            for y, p in enumerate(model.rows[theta][s][a]):
                if p and (not uncertain or model.rows[0][s][a][y]) and y not in paths:
                    paths[y] = paths[s] + ((a, y),)
                    queue.append(y)
    candidates = []
    for s, steps in paths.items():
        for index, c in enumerate(components):
            if s in used(c):
                candidates.append(Route(source, steps, index, None))
        if uncertain:
            for x, a in pairs:
                if x == s:
                    for y in sorted(K):
                        if model.rows[theta][s][a][y] and not model.rows[0][s][a][y]:
                            candidates.append(Route(source, steps, None, (a, y)))
    if not candidates:
        raise RuntimeError('fixed region has no route')

    def key(route):
        edges = route.steps + (() if route.reveal is None else (route.reveal,))
        return len(edges), edges, int(route.reveal is not None), route.component or 0
    return min(candidates, key=key)


def solve(model):
    model = validate_model(model)
    kt = descend(model, lambda K: known_operator(model, K))
    K = frozenset(kt[-1])
    wt = descend(model, lambda W: uncertain_operator(model, K, W))
    W = frozenset(wt[-1])
    if model.initial not in W:
        result = Negative(kt, wt)
        checked = check_negative(model, result)
    else:
        D1, D = safe_known(model, K), safe_uncertain(model, K, W)
        known = all_components(model, 1, D1)
        uncertain = tuple(all_components(model, t, D, True) for t in (0, 1))
        kr = tuple(shortest_route(model, s, 1, D1, known, K, False) for s in sorted(K))
        wr = tuple(tuple(shortest_route(model, s, t, D, uncertain[t], K, True) for s in sorted(W)) for t in (0, 1))
        result = Positive(tuple(sorted(K)), tuple(sorted(W)), D1, D, known, uncertain, kr, wr)
        checked = check_positive(model, result)
    if checked is None:
        raise RuntimeError('internally synthesized body failed independent submitted-body validation')
    return checked
