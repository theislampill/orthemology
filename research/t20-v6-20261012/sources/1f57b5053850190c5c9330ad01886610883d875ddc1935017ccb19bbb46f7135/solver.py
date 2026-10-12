"""Exact finite support algorithm for zero-error stopping under hidden-state instruments.

No probability approximation, empirical identification, or source authentication.
Input rows list precisely the positive (successor, observation) cells.
"""
from collections import defaultdict, deque


def classify(rows, labels, initial, legal=None):
    n = len(labels)
    actions = tuple(rows)
    initial = frozenset(initial)
    if not initial or not initial <= set(range(n)):
        raise ValueError('nonempty valid initial support required')
    legal = [set(actions) for _ in labels] if legal is None else legal
    if len(legal) != n:
        raise ValueError('one permission menu per labelled hidden state required')
    for a, table in rows.items():
        if len(table) != n:
            raise ValueError('one transition row per labelled hidden state required')
        for x, row in enumerate(table):
            if a in legal[x] and not row:
                raise ValueError('legal action must have nonempty probability support')
            for y, o in row:
                if not 0 <= y < n or labels[y] != labels[x]:
                    raise ValueError('transitions must preserve the initial target label')

    def goal(B):
        return len({labels[x] for x in B}) == 1

    def menu(B):
        return tuple(a for a in actions if all(a in legal[x] for x in B))

    def successors(B, a):
        by_obs = defaultdict(set)
        for x in B:
            for y, o in rows[a][x]:
                by_obs[o].add(y)
        return {o: frozenset(C) for o, C in by_obs.items()}

    # Reachable supports under all legal actions; stopping is available at goals.
    family, pending, trans = {initial}, [initial], {}
    while pending:
        B = pending.pop()
        if goal(B):
            continue
        for a in menu(B):
            trans[B, a] = successors(B, a)
            for C in trans[B, a].values():
                if C not in family:
                    family.add(C)
                    pending.append(C)
    goals = {B for B in family if goal(B)}

    # Sure finite stopping: least attractor, independent of positive weights.
    ranks = {B: 0 for B in goals}
    while True:
        new = {}
        for B in family - ranks.keys():
            depths = [1 + max(ranks[C] for C in trans[B,a].values())
                      for a in menu(B)
                      if all(C in ranks for C in trans[B,a].values())]
            if depths:
                new[B] = min(depths)
        if not new:
            break
        ranks.update(new)

    # Almost-sure: greatest fixed point using actual-state x support vertices.
    region, rounds, final_safe = set(family), [], {}
    while True:
        safe = {B: tuple(a for a in menu(B)
                         if all(C in region for C in trans[B,a].values()))
                for B in region - goals}
        vertices = {(x,B) for B in region for x in B}
        reverse = defaultdict(set)
        for x, B in vertices:
            if B in goals:
                continue
            for a in safe[B]:
                for y, o in rows[a][x]:
                    C = trans[B,a][o]
                    reverse[y,C].add((x,B))
        reachable = {(x,B) for B in region & goals for x in B}
        pending = deque(reachable)
        while pending:
            v = pending.popleft()
            for u in reverse[v] - reachable:
                reachable.add(u)
                pending.append(u)
        new = {B for B in region if all((x,B) in reachable for x in B)}
        rounds.append({'region_size':len(region), 'removed':len(region-new)})
        if new == region:
            final_safe = safe
            break
        region = new

    return {'sure': initial in ranks, 'sure_rank': ranks.get(initial),
            'almost_sure': initial in region, 'supports': family,
            'goals':goals, 'winning_supports':region,
            'safe_actions':final_safe, 'rounds':rounds,
            'transitions':trans, 'ranks':ranks}
