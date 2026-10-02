#!/usr/bin/env python3
"""Independent ceil-budget partition enumeration and alternate residue reductions."""
from fractions import Fraction as Q
from functools import lru_cache
import json
import sys


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def ceil(x):
    return -((-x.numerator) // x.denominator)


@lru_cache(None)
def parts(u, m, low=1):
    if m == 1:
        return ((u,),) if u >= low else ()
    return tuple((s,) + tail for s in range(low, u // m + 1)
                 for tail in parts(u-s, m-1, s))


@lru_cache(None)
def profile(s):
    # Direct adversarial allocation condition: at threshold t every block
    # needs ceil(t*size) corruptions. This avoids the author's floor-jump code.
    u = sum(s)
    answer = [Q(0)] * u
    candidates = sorted({Q(a, size) for size in s for a in range(size+1)})
    for t in candidates:
        cost = sum(ceil(t*size) for size in s)
        for b in range(cost, u):
            answer[b] = t
    return tuple(answer)


def floor_sum(s, t):
    return sum((t*size).numerator // (t*size).denominator for size in s)


def formula(u, b, m):
    if m > b:
        return Q(0)
    N = b-m+1
    return max(Q((q*N+m-1)//u, q) for q in range(1, u-m+2))


need(not sys.flags.optimize, 'Use unoptimised Python')
counts = dict(parameter_cases=0, integer_partitions=0, optimal_partitions=0,
              minimal_zero_witnesses=0, positive_excess_reductions=0,
              nonunit_residue_reductions=0)
for u in range(2, 25):
    for m in range(1, u):
        partitions = parts(u, m)
        counts['integer_partitions'] += len(partitions)
        for b in range(m, u):
            N = b-m+1
            B = min(profile(s)[b] for s in partitions)
            need(B == formula(u,b,m), 'Formula differs from ceil-budget partition optimum')
            a, q = B.numerator, B.denominator
            need(0 < a < q and q <= u-m+1, 'Reduced fraction bounds')
            need(0 <= a*u-q*N <= m-1, 'Arithmetic minimality inequality')
            optimal = [s for s in partitions if profile(s)[b] == B]
            zmin = min(sum(a*x % q == 0 for x in s) for s in optimal)
            for s in optimal:
                counts['optimal_partitions'] += 1
                residues = [a*x % q for x in s]
                zeros = [i for i,r in enumerate(residues) if r == 0]
                d = floor_sum(s,B)-N
                need(0 <= d < len(zeros), 'Left perturbation invariant')
                if len(zeros) == zmin:
                    need(d == 0 and all(r in (0,1) for r in residues), 'Minimal-zero characterization')
                    counts['minimal_zero_witnesses'] += 1
                if d > 0:
                    # Alternate proof: transfer one root between two zero blocks.
                    changed = list(s); changed[zeros[0]] -= 1; changed[zeros[1]] += 1
                    need(min(changed)>0 and sum(changed)==u, 'Positive block preservation')
                    need(floor_sum(changed,B) == floor_sum(s,B)-1, 'Positive-excess floor change')
                    need(sum(a*x%q==0 for x in changed)==len(zeros)-2, 'Two zeros removed')
                    need(profile(tuple(sorted(changed)))[b] <= B, 'Changed partition feasible')
                    counts['positive_excess_reductions'] += 1
                else:
                    recipients = [i for i,r in enumerate(residues) if r>=2]
                    if recipients:
                        j=recipients[0]; r=residues[j]
                        delta=(pow(a,-1,q)*(1-r))%q
                        need(1 <= delta < q, 'Coprime transfer exists')
                        changed=list(s);changed[zeros[0]]-=delta;changed[j]+=delta
                        need(min(changed)>0 and sum(changed)==u, 'Positive block preservation')
                        need(floor_sum(changed,B)==floor_sum(s,B), 'Deficit transfer keeps floor sum')
                        need(sum(a*x%q==0 for x in changed)==len(zeros)-1, 'One zero removed')
                        need(profile(tuple(sorted(changed)))[b]<=B, 'Changed partition feasible')
                        counts['nonunit_residue_reductions'] += 1
            counts['parameter_cases'] += 1
# Check endpoints beyond the partition dimension, and the prior elementary slices.
for u in range(1, 60):
    for b in range(u):
        need(formula(u,b,1)==Q(b,u), 'One-message endpoint')
        for m in (b+1,u+1,3*u+1):
            need(formula(u,b,m)==0, 'Zero endpoint or duplicate labels')
        if b:
            need(formula(u,b,b)==Q(1,u-b+1), 'Last positive boundary')
for args, value in [((7,3,2),Q(1,3)),((11,5,2),Q(3,8)),((9,4,3),Q(1,4)),
                    ((8,4,3),Q(1,3)),((10,4,3),Q(1,4)),((12,4,3),Q(1,5))]:
    need(formula(*args)==value, 'Numerical continuation')
need(counts['positive_excess_reductions']>0 and counts['nonunit_residue_reductions']>0,
     'Both independent reduction branches must be exercised')
print(json.dumps({'status':'PASS_GENERAL_PRIVATE_ARITHMETIC', 'counts':counts,
                  'partition_universes_through':24,'endpoint_universes_through':59,
                  'scope':'Exact finite arithmetic checks; continuum lower bound depends on the written hypergraph argument'},indent=2))
