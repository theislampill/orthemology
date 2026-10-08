"""Polynomial threshold representatives for the exact two-mode finite problem."""
from collections import deque
from dependencies import (checked_pairs, natural, validate_model, checked_region, safe_known,
                          safe_uncertain, used, Positive, Negative, shortest_route, check_positive)
from mec import maximal_components


def _even_values(model, theta, pairs):
    return tuple(sorted({model.priorities[theta][s][a] for s, a in pairs
                         if model.priorities[theta][s][a] % 2 == 0}))


def _attains(model, theta, pairs, value):
    return any(model.priorities[theta][s][a] == value for s, a in pairs)


def known_components(model, pairs):
    """Good known1 representatives with exactly the exhaustive target union."""
    pairs = tuple(sorted(checked_pairs(model, pairs)))
    result = set()
    for value in _even_values(model, 1, pairs):
        allowed = tuple((s, a) for s, a in pairs if model.priorities[1][s][a] >= value)
        result.update(c for c in maximal_components(model, 1, allowed)
                      if _attains(model, 1, c, value))
    return tuple(sorted(result))


def uncertain_components(model, theta, pairs):
    """Sound qualifying representatives covering every qualifying source.

Case A keeps a distinguishing pair and an attained even own minimum.
Case B uses full numerical row equality and two separately attained even
minima. Thresholds are distinct input values, irrespective of magnitude.
"""
    natural(theta, 2)
    pairs = tuple(sorted(checked_pairs(model, pairs)))
    nonrevealing = tuple((s, a) for s, a in pairs
                         if all(not p or model.rows[0][s][a][y]
                                for y, p in enumerate(model.rows[theta][s][a])))
    equal = frozenset((s, a) for s, a in nonrevealing
                      if model.rows[0][s][a] == model.rows[1][s][a])
    result = set()
    for value in _even_values(model, theta, nonrevealing):
        allowed = tuple((s, a) for s, a in nonrevealing
                        if model.priorities[theta][s][a] >= value)
        result.update(c for c in maximal_components(model, theta, allowed)
                      if _attains(model, theta, c, value) and any(e not in equal for e in c))
    for value0 in _even_values(model, 0, equal):
        for value1 in _even_values(model, 1, equal):
            allowed = tuple(sorted((s, a) for s, a in equal
                                   if model.priorities[0][s][a] >= value0
                                   and model.priorities[1][s][a] >= value1))
            result.update(c for c in maximal_components(model, theta, allowed)
                          if _attains(model, 0, c, value0) and _attains(model, 1, c, value1))
    return tuple(sorted(result))


def _backward_reachable(model, theta, pairs, targets, compatible_only):
    """Multi-source reverse graph search with all selected positive edges."""
    predecessors = {}
    for s, a in pairs:
        for y, p in enumerate(model.rows[theta][s][a]):
            if p and (not compatible_only or model.rows[0][s][a][y]):
                predecessors.setdefault(y, set()).add(s)
    reached, pending = set(targets), deque(targets)
    while pending:
        for source in predecessors.get(pending.popleft(), ()):
            if source not in reached:
                reached.add(source)
                pending.append(source)
    return frozenset(reached)


def known_operator(model, K):
    K = checked_region(model, K)
    pairs = safe_known(model, K)
    targets = frozenset(s for c in known_components(model, pairs) for s in used(c))
    return K & _backward_reachable(model, 1, pairs, targets, False)


def uncertain_operator(model, K, W):
    K, W = checked_region(model, K), checked_region(model, W)
    pairs = safe_uncertain(model, K, W)
    winners = W
    for theta in (0, 1):
        targets = {s for c in uncertain_components(model, theta, pairs) for s in used(c)}
        targets.update(s for s, a in pairs for y in K
                       if model.rows[theta][s][a][y] and not model.rows[0][s][a][y])
        winners &= _backward_reachable(model, theta, pairs, targets, True)
    return winners


def descend(model, operator):
    """Whole-carrier descent with exact terminal repetition and no truncation."""
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


def solve(model):
    """Return a checked original-schema Positive or Negative, using no oracle.

    Malformed models, exhaustion, and internal failures are execution errors.
    The representative body can differ from the reference's exhaustive body;
    its certificate meaning and controller interface remain exactly the same.
    """
    model = validate_model(model)
    kt = descend(model, lambda K: known_operator(model, K))
    K = frozenset(kt[-1])
    wt = descend(model, lambda W: uncertain_operator(model, K, W))
    W = frozenset(wt[-1])
    if model.initial not in W:
        from negative import check_negative
        checked = check_negative(model, Negative(kt, wt))
    else:
        D1, D = safe_known(model, K), safe_uncertain(model, K, W)
        known = known_components(model, D1)
        uncertain = tuple(uncertain_components(model, theta, D) for theta in (0, 1))
        kr = tuple(shortest_route(model, s, 1, D1, known, K, False) for s in sorted(K))
        wr = tuple(tuple(shortest_route(model, s, theta, D, uncertain[theta], K, True)
                         for s in sorted(W)) for theta in (0, 1))
        body = Positive(tuple(sorted(K)), tuple(sorted(W)), D1, D, known, uncertain, kr, wr)
        checked = check_positive(model, body)
    if checked is None:
        raise RuntimeError('internally synthesized body failed submitted-body validation')
    return checked
