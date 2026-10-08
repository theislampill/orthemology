"""Independent finite mathematical oracle, derived before implementation read.

No import from the reference package is permitted here.  Unlike its prescribed
descending operators, this oracle exhausts ALL candidate regions and takes the
union of regions that directly satisfy the positive existential clauses.
Reachability is computed by Boolean transitive closure, not path-search code.
This is bounded exact finite evidence, not a probabilistic theorem prover.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product


@dataclass(frozen=True)
class Input:
    n: int
    a: int
    initial: int
    menus: tuple
    rows: tuple
    priorities: tuple


def subsets(items):
    items = tuple(items)
    for size in range(len(items) + 1):
        for selected in combinations(items, size):
            yield frozenset(selected)


def pairs_in(m, region):
    return frozenset((s, a) for s in region for a in m.menus[s])


def closure(m, pairs, theta, compatible=False):
    """Boolean transitive closure, including the empty path at every state."""
    matrix = [[i == j for j in range(m.n)] for i in range(m.n)]
    for s, a in pairs:
        for y in range(m.n):
            if m.rows[theta][s][a][y] > 0 and (
                not compatible or m.rows[0][s][a][y] > 0
            ):
                matrix[s][y] = True
    for k in range(m.n):
        for i in range(m.n):
            for j in range(m.n):
                matrix[i][j] = matrix[i][j] or (matrix[i][k] and matrix[k][j])
    return matrix


def good_component(m, theta, pairs, uncertain):
    if not pairs or any(s not in range(m.n) or a not in m.menus[s] for s, a in pairs):
        return False
    used = {s for s, a in pairs}
    for s, a in pairs:
        for y in range(m.n):
            if m.rows[theta][s][a][y] > 0:
                if y not in used:
                    return False
                if uncertain and m.rows[0][s][a][y] == 0:
                    return False
    reach = closure(m, pairs, theta)
    if not all(reach[s][t] for s in used for t in used):
        return False
    if not uncertain:
        return theta == 1 and min(m.priorities[1][s][a] for s, a in pairs) % 2 == 0
    for rival in (0, 1):
        if all(m.rows[rival][s][a] == m.rows[theta][s][a] for s, a in pairs):
            if min(m.priorities[rival][s][a] for s, a in pairs) % 2:
                return False
    return True


def safe_known(m, k):
    return frozenset((s, a) for s, a in pairs_in(m, k)
                     if all(p == 0 or y in k for y, p in enumerate(m.rows[1][s][a])))


def safe_uncertain(m, k, w):
    return frozenset((s, a) for s, a in pairs_in(m, w)
                     if all((p == 0 or y in w) and
                            (m.rows[1][s][a][y] == 0 or p > 0 or y in k)
                            for y, p in enumerate(m.rows[0][s][a])))


def eligible_known(m, k):
    allowed = safe_known(m, k)
    targets = set()
    for pairs in subsets(allowed):
        if good_component(m, 1, pairs, False):
            targets.update(s for s, a in pairs)
    reach = closure(m, allowed, 1)
    return frozenset(s for s in k if any(reach[s][t] for t in targets))


def eligible_uncertain(m, k, w):
    allowed = safe_uncertain(m, k, w)
    answer = set(w)
    for theta in (0, 1):
        targets = set()
        for pairs in subsets(allowed):
            if good_component(m, theta, pairs, True):
                targets.update(s for s, a in pairs)
        for s, a in allowed:
            if any(m.rows[theta][s][a][y] > 0 and m.rows[0][s][a][y] == 0
                   and y in k for y in range(m.n)):
                targets.add(s)
        reach = closure(m, allowed, theta, compatible=True)
        answer.intersection_update(s for s in w if any(reach[s][t] for t in targets))
    return frozenset(answer)


def regions(m):
    """Find largest feasible regions by complete powerset census, no iteration."""
    carrier = tuple(range(m.n))
    feasible_k = [k for k in subsets(carrier) if eligible_known(m, k) == k]
    k = frozenset().union(*feasible_k)
    feasible_w = [w for w in subsets(carrier) if eligible_uncertain(m, k, w) == w]
    w = frozenset().union(*feasible_w)
    assert eligible_known(m, k) == k
    assert eligible_uncertain(m, k, w) == w
    return k, w


def two_state_one_action():
    """13122 inputs: 3^4 row choices * 3^4 priorities * 2 initials."""
    choices = (Fraction(0), Fraction(1, 2), Fraction(1))
    for probs in product(choices, repeat=4):
        rows = tuple(tuple(((probs[2*t+s], 1-probs[2*t+s]),) for s in range(2))
                     for t in range(2))
        for priorities in product(range(3), repeat=4):
            labels = tuple(tuple((priorities[2*t+s],) for s in range(2)) for t in range(2))
            for initial in range(2):
                yield Input(2, 1, initial, ((0,), (0,)), rows, labels)


def one_state_up_to_three_actions():
    """500 inputs: sum_(a=1..3) (2^a-1)*2^(2a); all stochastic rows unique."""
    for a in range(1, 4):
        rows = tuple((tuple((Fraction(1),) for _ in range(a)),) for _ in range(2))
        for menu in subsets(range(a)):
            if not menu:
                continue
            for priorities in product(range(2), repeat=2*a):
                labels = ((tuple(priorities[:a]),), (tuple(priorities[a:]),))
                yield Input(1, a, 0, (tuple(sorted(menu)),), rows, labels)


def two_state_two_action_state_homogeneous():
    """6561 cases: 3^4 exact full-support rows * 3^4 departure priorities.

    Every mode/action row and priority is the same at both source states;
    initial=0 and both actions are available. Different actions may provide
    different numerical mode information despite every support being equal.
    """
    choices=(Q for Q in (Fraction(1,3),Fraction(1,2),Fraction(2,3)))
    for probs in product(tuple(choices),repeat=4):
        rows=tuple(tuple(tuple((probs[2*t+a],1-probs[2*t+a]) for a in range(2))
                         for s in range(2)) for t in range(2))
        for labels in product(range(3),repeat=4):
            priorities=tuple(tuple(tuple(labels[2*t+a] for a in range(2))
                                   for s in range(2)) for t in range(2))
            yield Input(2,2,0,((0,1),(0,1)),rows,priorities)


def raw_model(m):
    """Adapt independently defined semantic input to the published raw API."""
    return dict(n_states=m.n, n_actions=m.a, initial=m.initial,
                menus=[list(menu) for menu in m.menus],
                rows=[[[[str(p) for p in row] for row in state] for state in mode]
                      for mode in m.rows],
                priorities=m.priorities)


def one_action_chain_regions(m):
    """Independent Markov-chain semantics, without any certificate predicates.

    A fixed chain wins AS from s iff every reachable bottom SCC has even
    minimum priority. Robust one-change success additionally requires P1 AS
    success from EVERY state reachable from s under P0, because each such
    finite path admits a deterministic change index at its endpoint.
    """
    assert m.a == 1 and all(menu == (0,) for menu in m.menus)
    graphs = [{s: {y for y, p in enumerate(m.rows[t][s][0]) if p > 0}
               for s in range(m.n)} for t in (0, 1)]
    all_reachable = []
    good = []
    for theta, graph in enumerate(graphs):
        reach = {}
        for start in range(m.n):
            seen, fringe = {start}, [start]
            while fringe:
                node = fringe.pop()
                for other in graph[node] - seen:
                    seen.add(other)
                    fringe.append(other)
            reach[start] = seen
        sccs = {frozenset(y for y in reach[s] if s in reach[y]) for s in range(m.n)}
        bad_bottoms = [c for c in sccs
                       if all(graph[s] <= c for s in c)
                       and min(m.priorities[theta][s][0] for s in c) % 2]
        good.append(frozenset(s for s in range(m.n)
                              if not any(reach[s] & c for c in bad_bottoms)))
        all_reachable.append(reach)
    k = good[1]
    w = frozenset(s for s in good[0] if all_reachable[0][s] <= k)
    return k, w


if __name__ == '__main__':
    for name, campaign in (("two_state_one_action", two_state_one_action),
                           ("one_state_up_to_three_actions", one_state_up_to_three_actions)):
        total = positive = 0
        for m in campaign():
            k, w = regions(m)
            if m.a == 1:
                assert (k, w) == one_action_chain_regions(m)
            total += 1
            positive += m.initial in w
        print(name, dict(total=total, positive=positive, negative=total-positive))
