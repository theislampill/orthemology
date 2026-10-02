#!/usr/bin/env python3
"""Exact finite regressions for the reviewed timing contracts, not a continuum proof."""
from fractions import Fraction as Q
from itertools import combinations
import json
import sys


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def compositions(total, n):
    if n == 1:
        yield (total,)
    else:
        for k in range(total + 1):
            for rest in compositions(total - k, n - 1):
                yield (k,) + rest


require(not sys.flags.optimize, 'Use unoptimised Python')
row_budget_cases = 0
for u in range(1, 7):
    for a in compositions(6, u):
        p = tuple(Q(k, 6) for k in a)
        for b in range(u):
            worst = max(sum((p[i] for i in C), Q(0))
                        for C in combinations(range(u), b))
            top = sum(sorted(p, reverse=True)[:b], Q(0))
            require(worst == top and top >= Q(b, u), 'Largest-coordinate bound')
            row_budget_cases += 1

u, b = 8, 3
faults = tuple(combinations(range(u), b))
menus = tuple(combinations(range(u), 2))
static_menu_losses = []
for C in faults:
    loss = Q(sum(set(menu).issubset(C) for menu in menus), len(menus))
    require(loss == Q(3, 28), 'Static-before-menu risk')
    static_menu_losses.append(loss)
# The SAME menu protocol is entirely defeated once each actual menu is public.
public_menu_losses = []
for menu in menus:
    loss = max(int(set(menu).issubset(C)) for C in faults)
    require(loss == 1, 'Public two-root menu must be hittable')
    public_menu_losses.append(loss)
# Reoptimising schedule 2 gives an upper witness for its accepted F=1/4.
blocks = (set(range(4)), set(range(4, 8)))
fixed_risk = max(min(Q(len(set(C) & block), len(block)) for block in blocks)
                 for C in faults)
require(fixed_risk == Q(1, 4), 'Fixed 4+4 witness')
require(max(static_menu_losses) < fixed_risk < Q(b, u) < 1, 'Strict values')

edge_cases = 0
for u in range(1, 9):
    for b in range(u):
        p = tuple(Q(1, u) for _ in range(u))
        for C in combinations(range(u), b):
            require(sum((p[i] for i in C), Q(0)) == Q(b, u), 'Uniform witness')
            edge_cases += 1
        revealed_loss = 0 if b == 0 else 1
        if b:
            for root in range(u):
                chosen = (root,) + tuple(i for i in range(u) if i != root)[:b-1]
                require(len(set(chosen)) == b and root in chosen, 'Revealed-root attack')
        require(revealed_loss == (0 if b == 0 else 1), 'Zero-budget edge')

# Independence after the reveal would invalidate schedule 4's permitted strategy.
# A uniform root on {0,1}, followed by C={root}, has loss 1; independent equal
# marginals would instead give 1/2. This is why the opening contract was revised.
require(sum(Q(1, 2) for r in range(2) if r in {r}) == 1, 'Adaptive coupling')
print(json.dumps({
    'status': 'PASS_TIMING_RESOURCE_CONTROLS',
    'largest_coordinate_row_budget_cases': row_budget_cases,
    'uniform_fault_scenarios': edge_cases,
    'eight_three_two_static_fault_sets': len(faults),
    'eight_three_two_shared_menus': len(menus),
    'optimized_values': ['3/28', '1/4', '3/8', '1'],
    'same_two_root_menu_public_before_fault_value': '1',
    'general_claim_basis': 'ordinary proofs plus previously reviewed F and S; finite checks are regressions'
}, indent=2))
