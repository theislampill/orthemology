#!/usr/bin/env python3
"""Finite exact-rational corroboration only; not a proof of computability theorems."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
counts = {}

def checked(group, condition):
    assert condition, group
    counts[group] = counts.get(group, 0) + 1

def l1(v):
    return sum(map(abs, v), F(0))

def tv(p, q):
    return l1([x-y for x, y in zip(p, q)]) / 2

def mul(p, P):
    return tuple(sum((p[i]*P[i][j] for i in range(len(p))), F(0))
                 for j in range(len(P[0])))

def envelope_vertices(c):
    # Independent vertex description: all but at most one box coordinate is tight.
    out = set()
    for free in range(len(c)):
        other = [i for i in range(len(c)) if i != free]
        for bits in product([0, 1], repeat=len(other)):
            p = [F(0)] * len(c)
            for i, bit in zip(other, bits):
                p[i] = c[i] if bit else F(0)
            p[free] = 1-sum(p)
            if 0 <= p[free] <= c[free]:
                out.add(tuple(p))
    return sorted(out)

def cap_formula(c):
    C = sum(c)
    return max(min(F(1), C-1, s, C-s)
               for bits in product([0, 1], repeat=len(c))
               for s in [sum((x*b for x, b in zip(c, bits)), F(0))])

# Compare the subset formula with independent extreme-point diameter calculation.
caps = []
for n in (1, 2, 3):
    for nums in product(range(5), repeat=n):
        c = tuple(F(x, 4) for x in nums)
        if sum(c) >= 1:
            caps.append(c)
caps += [(F(9,10), F(9,10), F(1,5)), (F(1,2),)*4,
         (F(1,4), F(1,3), F(1,2), F(3,4)), (F(1),F(1,3))]
for c in caps:
    vertices = envelope_vertices(c)
    checked('nonempty_cap_vertices', bool(vertices))
    D = max(tv(p, q) for p in vertices for q in vertices)
    checked('diameter_formula_against_vertices', D == cap_formula(c))
    checked('coarse_cap_bound', D <= min(F(1), sum(c)-1))
    partition = any(1 <= sum(x*b for x,b in zip(c,bits)) <= sum(c)-1
                    for bits in product([0,1], repeat=len(c)))
    checked('capacity_partition_iff_diameter_one', (D == 1) == partition)

# Sharp family at each rational C in [1,2], and exact stationary values.
for r in [F(k,16) for k in range(17)]:
    C = 1+r
    P = ((F(1), F(0)), (1-r, r))
    checked('sharp_cap_domination', all(P[i][j] <= (F(1),r)[j]
                                       for i in range(2) for j in range(2)))
    checked('sharp_contraction_ratio', tv(P[0], P[1]) == C-1)
    checked('sharp_stationary_delta', mul((F(1),F(0)),P) == (F(1),F(0)))

# Cesaro telescoping, exact stationary balance and all branch distinctions.
for a,b in product([F(0),F(1,8),F(1,3),F(1)], repeat=2):
    P=((1-a,a),(b,1-b))
    if a+b:
        pi=(b/(a+b),a/(a+b))
        checked('two_state_stationary_formula', mul(pi,P)==pi)
    for x in [F(0),F(1,3),F(1,2),F(1)]:
        p=(x,1-x)
        total=[F(0),F(0)]
        orbit=p
        for N in range(1,17):
            total=[total[i]+orbit[i] for i in range(2)]
            orbit=mul(orbit,P)
            mean=tuple(v/N for v in total)
            residual=tuple(mul(mean,P)[i]-mean[i] for i in range(2))
            checked('cesaro_telescope',residual==tuple((orbit[i]-p[i])/N
                                                       for i in range(2)))
            checked('cesaro_residual_bound',l1(residual)<=F(2,N))

for n in range(1,33):
    t=F(1,2**n)
    P=((1-t,t),(F(0),F(1)))
    q=(F(1,2),F(1,2))
    checked('tiny_residual_fixed_solution_error',
            l1([mul(q,P)[i]-q[i] for i in range(2)])==t and tv(q,(0,1))*2==1)
    checked('opposite_forced_stationaries',
            mul((F(0),F(1)),P)==(F(0),F(1)) and
            mul((F(1),F(0)),((F(1),F(0)),(t,1-t)))==(F(1),F(0)))

# Countably supported product lift: retain exact analytic tail, do not renormalize it.
for N in range(1,20):
    g=[F(1,2**(m+1)) for m in range(N)]
    checked('product_lift_cap_tail',2-2*sum(g)==F(2,2**N))
    for a,b in [(F(1,8),F(0)),(F(0),F(1,8)),(F(1,3),F(1,8))]:
        P=((1-a,a),(b,1-b))
        pi=(b/(a+b),a/(a+b))
        for j,m in product(range(2),range(N)):
            checked('product_lift_stationary_coordinate',
                    sum(pi[i]*P[i][j]*g[m] for i in range(2))==pi[j]*g[m])
            checked('product_lift_row_cap',
                    all(P[i][j]*g[m]<=g[m] for i in range(2)))

# A finite event schedule exercises the birth-death formulas, not noncomputability.
increments={3:F(1,16),7:F(1,64),12:F(1,256)}
def w(n):
    return F(1) if n==0 else F(1,2**n)+increments.get(n,F(0))
def h(n):
    return min(w(n),w(n+1))/4
def bd(i,j):
    if j==i+1: return h(i)/w(i)
    if i and j==i-1: return h(i-1)/w(i)
    if i==j: return 1-h(i)/w(i)-(h(i-1)/w(i) if i else 0)
    return F(0)
for n in range(25):
    checked('birth_death_row_stochastic',sum(bd(n,j) for j in range(max(0,n-1),n+2))==1)
    checked('birth_death_diagonal_bound',bd(n,n)>=F(1,2))
    checked('birth_death_detailed_balance',w(n)*bd(n,n+1)==w(n+1)*bd(n+1,n))
    checked('birth_death_cap_invariance_identity',
            sum(w(i)*bd(i,n) for i in range(max(0,n-1),n+2))==w(n))

# Exact negative controls against common overclaims.
cap=(F(3,4),F(3,4)); I=((F(1),F(0)),(F(0),F(1)))
checked('invariance_without_row_domination',cap_formula(cap)==F(1,2)
        and I[0][0]>cap[0]
        and all(mul(p,I)==p for p in envelope_vertices(cap)))
rows=((F(1,2),F(1,2),F(0)),(F(1,2),F(0),F(1,2)),(F(0),F(1,2),F(1,2)))
checked('pair_overlap_without_common_minorant',
        max(tv(p,q) for p in rows for q in rows)==F(1,2)
        and sum(min(row[j] for row in rows) for j in range(3))==0)
checked('cap_mass_two_can_still_contract',cap_formula((F(9,10),F(9,10),F(1,5)))==F(9,10))
checked('correspondence_fixed_interval_control',
        all(mul((t,1-t),((t,1-t),(t,1-t)))==(t,1-t)
            for t in [F(1,3),F(1,2),F(2,3)]))

result={'status':'PASS','scope':'Finite exact-rational corroboration only',
        'cap_instances':len(caps),'checks':counts,'total_checks':sum(counts.values()),
        'excluded_claims':['Universal computability proof','Noncomputability proof',
                           'Infinite-dimensional universal refinement','Lean/kernel verification']}
(HERE/'CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
