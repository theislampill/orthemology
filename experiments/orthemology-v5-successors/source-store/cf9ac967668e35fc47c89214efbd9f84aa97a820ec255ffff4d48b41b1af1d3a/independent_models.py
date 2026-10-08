"""Independent ordinary baselines. No imports from candidate implementation.

Read-cost model values are synthetic; actual source witnesses are not assigned
counterfactual role worlds. Costs are exact Fractions or math.inf.
"""
from fractions import Fraction
from itertools import combinations
from math import inf


class InvalidStack(ValueError):
    pass


def direct_stack(events, incoming):
    """Concrete bottom-first stack; tuple events: enter, leave, exit, emit.

    Selected emit carries a fresh ID; emit(None) is unselected. Origins may be
    arbitrary equality-comparable immutable keys. A pop may never empty stack.
    """
    if not incoming:
        raise InvalidStack('empty incoming stack')
    stack = list(reversed(incoming))
    outputs = []
    ids = set()
    for op, arg in events:
        if op == 'enter':
            stack.append(arg)
        elif op in ('leave', 'exit'):
            if len(stack) < 2:
                raise InvalidStack('underflow at prefix')
            if op == 'exit' and stack[-1] != arg:
                raise InvalidStack('origin mismatch')
            stack.pop()
        elif op == 'emit':
            if arg is not None:
                if arg in ids:
                    raise InvalidStack('duplicate output occurrence')
                ids.add(arg)
                outputs.append((arg, stack[-1]))
        else:
            raise InvalidStack('unknown event')
    return tuple(reversed(stack)), tuple(outputs)


def direct_demand(outputs, selected, holdings):
    """Requires original bindings to have been resolved before this call."""
    by_id = dict(outputs)
    if len(by_id) != len(outputs):
        raise ValueError('duplicate output occurrence')
    keys = {by_id[t] for t in selected}
    if any(holdings.get(k) is False for k in keys):
        return False, frozenset()
    unresolved = frozenset(k for k in keys if holdings.get(k) is not True)
    return (True if not unresolved else None), unresolved


def subset_cover(demand, actions):
    """Enumerate every subset, rather than using interval suffix recurrence.

    actions=(id, coverage, exact_positive_cost), fully available only.
    """
    if any(Fraction(cost) <= 0 for _, _, cost in actions):
        raise ValueError('nonpositive read cost')
    demand = set(demand)
    best, witness = inf, None
    for size in range(len(actions) + 1):
        for subset in combinations(actions, size):
            seen = set()
            for _, coverage, _ in subset:
                seen.update(coverage)
            if demand <= seen:
                cost = sum((Fraction(a[2]) for a in subset), Fraction())
                if cost < best:
                    best, witness = cost, tuple(a[0] for a in subset)
    return best, witness


def partition_minimax(verdicts, response_columns, costs, initial_blocks=None):
    """Bottom-up complete knowledge-state DP, no covering algorithm.

    Enumerates all nonempty subsets of worlds; decisions are allowed only when
    all their verdicts match. Full response equality partitions the subset.
    Every informative outcome is a strict subset, so increasing popcount gives
    a nonrecursive finite proof order. Noninformative positive-cost actions
    cannot help; impossible total decisions have infinite value.
    """
    if len(response_columns) != len(costs):
        raise ValueError('menu mismatch')
    costs = tuple(Fraction(c) for c in costs)
    if any(c <= 0 for c in costs):
        raise ValueError('nonpositive read cost')
    n = len(verdicts)
    if not n:
        raise ValueError('empty world family')
    if any(len(col) != n for col in response_columns):
        raise ValueError('response table mismatch')
    values = {}
    for count in range(1, n + 1):
        for subset in combinations(range(n), count):
            mask = sum(1 << i for i in subset)
            if len({verdicts[i] for i in subset}) == 1:
                values[mask] = Fraction()
                continue
            best = inf
            for col, c in zip(response_columns, costs):
                blocks = {}
                for i in subset:
                    blocks[col[i]] = blocks.get(col[i], 0) | (1 << i)
                if len(blocks) <= 1:
                    continue
                worst = max(values[b] for b in blocks.values())
                best = min(best, c + worst)
            values[mask] = best
    if initial_blocks is None:
        initial_blocks = ((1 << n) - 1,)
    return max(values[b] for b in initial_blocks)


def star_locality(worlds, demand, actions, public_metadata=None):
    """Full finite all-positive-star checker, independently defined.

    worlds is sequence mapping key->bool. actions=(coverage,response_column).
    A star alternative may vary irrelevant labels but must preserve every
    noncovered COMPLETE response and the observed public metadata.
    """
    demand = frozenset(demand)
    public_metadata = tuple(public_metadata or [None] * len(worlds))
    for center, world in enumerate(worlds):
        if not all(world[k] for k in demand):
            continue
        if all(any(
            public_metadata[j] == public_metadata[center]
            and not other[k]
            and all(other[t] == world[t] for t in demand - {k})
            and all(k in coverage or column[j] == column[center]
                    for coverage, column in actions)
            for j, other in enumerate(worlds)) for k in demand):
            return True
    return False


def self_test():
    assert direct_stack([('enter','b'),('leave',None),('emit','z')], ['a']) == (('a',), (('z','a'),))
    try:
        direct_stack([('leave',None),('enter','b')], ['a'])
    except InvalidStack:
        pass
    else:
        raise AssertionError('invalid prefix accepted')
    assert subset_cover({'a','b'}, [('both',{'a','b'},100),('a',{'a'},1),('b',{'b'},1)])[0] == 2
    worlds = [dict(a=a,b=b) for a in [False,True] for b in [False,True]]
    verdicts = [w['a'] and w['b'] for w in worlds]
    cols = [tuple(w[k] for w in worlds) for k in ['a','b']]
    assert partition_minimax(verdicts, cols, [1,10]) == 11
    assert star_locality(worlds, {'a','b'}, [(frozenset({k}),col) for k,col in zip(['a','b'],cols)])
    leak = tuple(verdicts)
    assert partition_minimax(verdicts, cols+[leak], [1,10,1]) == 1
    assert not star_locality(worlds, {'a','b'}, [(frozenset(),leak)])
    assert subset_cover(set(),[])[0] == 0
    assert subset_cover({'a'},[])[0] == inf
    print('independent reference self-tests: PASS')

if __name__ == '__main__':
    self_test()
