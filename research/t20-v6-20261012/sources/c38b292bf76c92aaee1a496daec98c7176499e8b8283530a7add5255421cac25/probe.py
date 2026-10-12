"""Finite research controls. Not a trust authority, runtime, or proof kernel."""
from math import inf


def essential(n, output):
    assert len(output) == 1 << n
    return frozenset(i for i in range(n)
                     if any(output[x] != output[x ^ (1 << i)]
                            for x in range(1 << n)))


def closure(n, output, actions):
    current = essential(n, output)
    while True:
        extra = frozenset(i for a in actions for j in current
                          for i in essential(n, tuple((y >> j) & 1 for y in a)))
        enlarged = current | extra
        if enlarged == current:
            return current
        current = enlarged


def minimize(output, actions):
    """Independent Moore refinement: uses neither coordinate essentiality nor closure."""
    def labels(signatures):
        ids = {}
        return tuple(ids.setdefault(s, len(ids)) for s in signatures)
    classes = labels(output)
    while True:
        refined = labels(tuple((output[x], tuple(classes[a[x]] for a in actions))
                               for x in range(len(output))))
        if refined == classes:
            return classes
        classes = refined


def resets(n):
    return tuple(tuple((x | (1 << i)) if b else (x & ~(1 << i))
                       for x in range(1 << n))
                 for i in range(n) for b in (0,1))


def frontier(catalogue, inventory):
    pairs = set((s & ~inventory, k) for s,k in catalogue)
    return tuple(sorted((s,k) for s,k in pairs
                        if not any((t,c)!=(s,k) and t & s == t and c<=k
                                   for t,c in pairs)))


def output_for_catalogue(n, catalogue):
    return tuple(min((k for s,k in catalogue if s & x == s), default=inf)
                 for x in range(1 << n))
