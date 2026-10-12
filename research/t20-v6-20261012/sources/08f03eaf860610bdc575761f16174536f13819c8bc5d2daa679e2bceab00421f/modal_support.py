"""Exact finite support and modal-absence operations.

Sets of contributors are integer bit masks. No function infers that the
model's possible worlds are the metaphysically possible worlds.
"""
from __future__ import annotations
from itertools import product
from typing import Iterable, Sequence


def subsets(mask: int) -> tuple[int, ...]:
    if mask < 0:
        raise ValueError('mask must be nonnegative')
    out = []
    sub = mask
    while True:
        out.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask
    return tuple(sorted(out))


def minimise(family: Iterable[int]) -> tuple[int, ...]:
    fs = sorted(set(family), key=lambda a: (a.bit_count(), a))
    out: list[int] = []
    for a in fs:
        if a < 0:
            raise ValueError('negative mask')
        if not any((b & a) == b for b in out):
            out.append(a)
    return tuple(sorted(out))


def supported(supports: Iterable[int], active: int) -> bool:
    return any((c & active) == c for c in supports)


def blockers(supports: Sequence[int], n: int) -> tuple[int, ...]:
    """Includes degenerate families: b(empty)={empty}; b({empty})=empty."""
    if n < 0 or any(s < 0 or s >= 1 << n for s in supports):
        raise ValueError('invalid finite ground set')
    return minimise(a for a in range(1 << n) if all(a & c for c in supports))


def closure(n: int, seeds: int, rules: Sequence[tuple[int, int]]) -> int:
    """Least Horn closure. Each (antecedent_mask, head_index) is positive."""
    if n < 0 or not 0 <= seeds < 1 << n:
        raise ValueError('invalid state')
    for antecedent, head in rules:
        if not 0 <= antecedent < 1 << n or not 0 <= head < n:
            raise ValueError('invalid rule')
    state = seeds
    while True:
        new = state
        for antecedent, head in rules:
            if (antecedent & state) == antecedent:
                new |= 1 << head
        if new == state:
            return state
        state = new


def minimal_supports(n: int, seed_indices: Sequence[int],
                     rules: Sequence[tuple[int, int]]) -> tuple[tuple[int, ...], ...]:
    """Independent antichain fixed-point algorithm, not seed enumeration.

    Supports are masks in the *atom* index space; only declared seed atoms
    may appear. Empty-antecedent rules are explicitly supported, not hidden.
    """
    if n < 0 or any(not 0 <= s < n for s in seed_indices):
        raise ValueError('invalid seeds')
    for antecedent, head in rules:
        if not 0 <= antecedent < 1 << n or not 0 <= head < n:
            raise ValueError('invalid rule')
    current: list[tuple[int, ...]] = [() for _ in range(n)]
    for s in seed_indices:
        current[s] = (1 << s,)
    while True:
        new = list(current)
        for antecedent, head in rules:
            antecedents = [i for i in range(n) if antecedent >> i & 1]
            terms = []
            for choices in product(*(current[i] for i in antecedents)):
                merged = 0
                for term in choices:
                    merged |= term
                terms.append(merged)
            new[head] = minimise((*new[head], *terms))
        if new == current:
            return tuple(new)
        current = new


def absence_complex(active_worlds: Sequence[int], n: int) -> frozenset[int]:
    if not active_worlds:
        raise ValueError('possible-world family must be nonempty')
    full = (1 << n) - 1
    if any(not 0 <= a <= full for a in active_worlds):
        raise ValueError('invalid active-world mask')
    return frozenset(d for a in active_worlds for d in subsets(full ^ a))


def necessary_active(active_worlds: Sequence[int], n: int) -> int:
    absence_complex(active_worlds, n)
    out = (1 << n) - 1
    for a in active_worlds:
        out &= a
    return out


def union_closed(complex_: Iterable[int]) -> bool:
    c = frozenset(complex_)
    return all(a | b in c for a in c for b in c)


def skeleton_bounds(known: frozenset[int], n: int, k: int
                    ) -> tuple[frozenset[int], frozenset[int]]:
    """Lower/upper downsets compatible with a COMPLETE k-skeleton."""
    if not 0 <= k <= n or 0 not in known:
        raise ValueError('invalid complete skeleton')
    if any(a < 0 or a >= 1 << n or a.bit_count() > k for a in known):
        raise ValueError('skeleton contains an out-of-scope set')
    if any(b not in known for a in known for b in subsets(a)):
        raise ValueError('skeleton is not downward closed')
    upper = frozenset(a for a in range(1 << n)
                      if all(b in known for b in subsets(a) if b.bit_count() <= k))
    return known, upper


def necessary_from_complex(supports: Sequence[int], complex_: Iterable[int], n: int) -> bool:
    return not any(c in complex_ for c in blockers(supports, n))


def audit(supports: Sequence[int], known: frozenset[int], n: int, k: int) -> str:
    lower, upper = skeleton_bounds(known, n, k)
    if necessary_from_complex(supports, upper, n):
        return 'NECESSARY_FOR_ALL_COMPLETIONS'
    if not necessary_from_complex(supports, lower, n):
        return 'NOT_NECESSARY_FOR_ALL_COMPLETIONS'
    return 'UNDETERMINED'
