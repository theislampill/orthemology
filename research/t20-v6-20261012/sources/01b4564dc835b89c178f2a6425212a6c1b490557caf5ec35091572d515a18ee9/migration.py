"""Finite synthetic migration certificate checks, using exact rational flow.

Graphs are already-compiled controller products. Public implementability,
authority and world adequacy are caller-supplied contracts, not inferred here.
"""
from collections import defaultdict, deque
from fractions import Fraction


def coupling(source, destination, relation):
    """Return an R-supported exact marginal coupling, or None if impossible."""
    for distribution in (source, destination):
        if (not distribution or any(p <= 0 for p in distribution.values())
                or sum(distribution.values()) != 1):
            raise ValueError('Marginals must be positive distributions summing exactly to one')
    start, end = ('flow_source',), ('flow_sink',)
    capacity = defaultdict(dict)
    def edge(u, v, cap):
        capacity[u][v] = Fraction(cap)
        capacity[v].setdefault(u, Fraction(0))
    for x, mass in source.items():
        edge(start, ('left', x), mass)
    for y, mass in destination.items():
        edge(('right', y), end, mass)
    for x, y in relation:
        if x in source and y in destination:
            edge(('left', x), ('right', y), 1)
    residual = {u: dict(es) for u, es in capacity.items()}
    value = Fraction(0)
    while True:
        predecessor = {start: None}
        todo = deque([start])
        while todo and end not in predecessor:
            u = todo.popleft()
            for v, cap in residual[u].items():
                if cap > 0 and v not in predecessor:
                    predecessor[v] = u
                    todo.append(v)
        if end not in predecessor:
            break
        path = []
        v = end
        while v != start:
            u = predecessor[v]
            path.append((u, v)); v = u
        amount = min(residual[u][v] for u, v in path)
        value += amount
        for u, v in path:
            residual[u][v] -= amount
            residual[v][u] += amount
    if value != 1:
        return None
    result = {}
    for x, y in relation:
        u, v = ('left', x), ('right', y)
        if v in capacity.get(u, {}):
            flow = capacity[u][v] - residual[u][v]
            if flow > 0:
                result[x, y] = flow
    assert all(sum(w for (p, q), w in result.items() if p == x) == mass
               for x, mass in source.items())
    assert all(sum(w for (p, q), w in result.items() if q == y) == mass
               for y, mass in destination.items())
    return result


def _common_checks(source, destination, bad_source, bad_destination,
                   relation, initial_pairs, licensed_destination):
    violations = []
    if not initial_pairs:
        violations.append(('empty_initial_support',))
    for pair in initial_pairs:
        if pair not in relation:
            violations.append(('initial_pair_uncovered',) + pair)
    for p, q in relation:
        if p not in source or q not in destination:
            violations.append(('undefined_related_state', p, q))
        if q in bad_destination and p not in bad_source:
            violations.append(('bad_reflection', p, q))
    for q in destination:
        if q not in licensed_destination:
            violations.append(('destination_license', q))
        if not destination[q]:
            violations.append(('destination_dead_end', q))
    return violations


def verify_probabilistic_migration(source, destination, bad_source, bad_destination,
                                   relation, initial_pairs, licensed_destination):
    """Check pointwise coupling for declared initial actual-pair support.

    For initial distributions, a separate initial marginal coupling is required.
    This function's initial_pairs argument instead specifies all possible actual
    migration pairs, each of which must satisfy the relation.
    """
    violations = _common_checks(source, destination, bad_source, bad_destination,
                                relation, initial_pairs, licensed_destination)
    couplings = {}
    for p, q in relation:
        if p not in source or q not in destination:
            continue
        witness = coupling(source[p], destination[q], relation)
        if witness is None:
            violations.append(('no_probability_coupling', p, q))
        else:
            couplings[p, q] = witness
    return {'valid': not violations, 'violations': violations, 'couplings': couplings}


def verify_rank_migration(source, destination, bad_source, bad_destination, rank_source,
                          relation, initial_pairs, licensed_destination):
    violations = _common_checks(source, destination, bad_source, bad_destination,
                                relation, initial_pairs, licensed_destination)
    for p, successors in source.items():
        if p not in rank_source or not isinstance(rank_source[p], int) or rank_source[p] < 0:
            violations.append(('missing_or_invalid_source_rank', p))
            continue
        if not successors:
            violations.append(('source_dead_end', p))
        for np in successors:
            if (np not in rank_source or
                    rank_source[p] < int(p in bad_source) + rank_source[np]):
                violations.append(('source_rank_edge', p, np))
    for p, q in relation:
        if p not in source or q not in destination:
            continue
        for nq in destination[q]:
            if not any((np, nq) in relation for np in source[p]):
                violations.append(('step_match', p, q, nq))
    lifted = {}
    for q in destination:
        fibre = [rank_source[p] for p, dq in relation if dq == q and p in rank_source]
        if fibre:
            lifted[q] = min(fibre)
    if not violations:
        for q, successors in destination.items():
            if q not in lifted:
                continue
            for nq in successors:
                assert nq in lifted
                assert lifted[q] >= int(q in bad_destination) + lifted[nq]
    return {'valid': not violations, 'violations': violations,
            'destination_rank': lifted}
