#!/usr/bin/env python3
"""Independent finite exact controls; not a replacement for the general proofs."""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from itertools import product, combinations
from math import gcd, comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
COUNTS = Counter()


def check(ok, family):
    assert ok, family
    COUNTS[family] += 1


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


PREDECESSORS = {
    'global-calibration-ambiguity/MANIFEST.json': '819b9c5eda8de1fd35b34714d24964ce02d4a41b5c6419413bcd8d82a6febe6c',
    'global-calibration-ambiguity/RESULT.md': 'ec620e491fd1c58cdc9dc0bcc8700784b79b4b399247ca1e2a235438138cf827',
    'grouped-mixture-identification/RESULT.md': 'c5f5a0aa82292fdea78e8939012abd5070ed3a855d270330db27d645e34c5239',
    'grouped-mixture-identification/PROCESS_AND_ORACLE_BOUNDARIES.md': '5e67e1c1db5d2a46dde90a84b93fdfab941fb096de1ae6683b6c5ade139dc793',
}
for path, expected in PREDECESSORS.items():
    check(digest(BASE / path) == expected, 'predecessor_before')


def moment(counts, weights, t, r):
    return sum((w * (t ** j) ** r for j, w in zip(counts, weights)), Q())


def word(counts, weights, t, outcomes):
    def probability(j):
        z = t ** j  # convention j=0 gives 1 even at t=0
        ans = Q(1)
        for y in outcomes:
            ans *= z if y else 1-z
        return ans
    return sum((w * probability(j) for j, w in zip(counts, weights)), Q())


signatures = [(1,), (1,2), (2,3), (1,3,4), (2,5,7)]
for v in signatures:
    check(reduce(gcd, v) == 1, 'primitive_signatures')
    for include_zero in [False, True]:
        n = len(v) + include_zero
        weights = tuple(Q(i+1, n*(n+1)//2) for i in range(n))
        for d,e in [(1,2),(2,3),(3,2),(4,6),(5,3)]:
            left = tuple([0] * include_zero + [d*j for j in v])
            right = tuple([0] * include_zero + [e*j for j in v])
            gleft = reduce(gcd, (j for j in left if j))
            gright = reduce(gcd, (j for j in right if j))
            check(tuple(j//gleft for j in left if j) == v, 'gcd_normalization')
            check(tuple(j//gright for j in right if j) == v, 'gcd_normalization')
            check(tuple(Q(e,d)*j for j in left) == right, 'rational_not_integer_rescaling')
            for u in [Q(1,5),Q(1,2),Q(3,4)]:
                t,s = u**e,u**d
                for r in range(9):
                    check(moment(left,weights,t,r) == moment(right,weights,s,r), 'scaled_moment_identity')
                for R in range(1,6):
                    total = Q()
                    for ys in product([0,1],repeat=R):
                        a = word(left,weights,t,ys)
                        check(a == word(right,weights,s,ys), 'scaled_word_identity')
                        q = sum(ys)
                        expansion = sum(((-1)**h * comb(R-q,h) * moment(left,weights,t,q+h) for h in range(R-q+1)), Q())
                        check(a == expansion, 'word_moment_equivalence')
                        total += a
                    check(total == 1, 'grouped_normalization')

# Direct finite Lagrange interpolation controls on rational nodes.
for N in range(2,13):
    nodes = [Q(3,4)**j for j in range(N)]
    coeffs = []
    for j,z in enumerate(nodes):
        den = Q(1)
        for i,y in enumerate(nodes):
            if i != j:
                den *= z-y
        coeffs.append(1/den)
        check((coeffs[-1] > 0) == (j%2==0), 'alternating_interpolation_sign')
    for r in range(N):
        value = sum((c*z**r for c,z in zip(coeffs,nodes)), Q())
        check(value == (1 if r==N-1 else 0), 'interpolation_moment_identity')
    for i,z in enumerate(nodes):
        for j,y in enumerate(nodes):
            value = Q(1)
            for h,node in enumerate(nodes):
                if h != i:
                    value *= (y-node)/(z-node)
            check(value == (1 if i==j else 0), 'lagrange_vandermonde_basis')

# A separately implemented prime-valuation and Bezout rational-node decoder.
def extended_gcd(a,b):
    if b==0:
        return a,1,0
    g,x,y=extended_gcd(b,a%b)
    return g,y,x-(a//b)*y

def bezout_vector(values):
    coefficients=[1]
    g=values[0]
    for value in values[1:]:
        g,x,y=extended_gcd(g,value)
        coefficients=[x*c for c in coefficients]+[y]
    return g,coefficients

def rational_signature(nodes):
    denominator=nodes[0].denominator
    p=2
    while denominator%p:
        p+=1
    vals=[]
    for node in nodes:
        a,b=node.numerator,node.denominator
        val=0
        while a%p==0:
            val+=1
            a//=p
        while b%p==0:
            val-=1
            b//=p
        vals.append(val)
    if any(a>=0 for a in vals):
        return None
    g=reduce(gcd,(abs(a) for a in vals))
    v=tuple(abs(a)//g for a in vals)
    unit,coefficients=bezout_vector(v)
    assert unit==1
    base=Q(1)
    for q,c in zip(nodes,coefficients):
        base*=q**c
    if not 0<base<1 or any(q!=base**j for q,j in zip(nodes,v)):
        return None
    return v,base

for v in signatures+[(3,8),(4,9,11)]:
    for base in [Q(1,2),Q(2,3),Q(3,7),Q(12,35),Q(9,16),Q(25,49)]:
        nodes=tuple(base**j for j in v)
        check(rational_signature(nodes)==(v,base), 'rational_node_decoder')
for nodes in [(Q(3,4),Q(1,2)),(Q(9,16),Q(3,8)),(Q(1,2),Q(1,3))]:
    check(rational_signature(nodes) is None, 'rational_node_membership_rejection')

# Required shifted k=2 obstruction, with two different primitive signatures.
a_counts,a_weights = (1,3),(Q(27,175),Q(148,175))
b_counts,b_weights = (2,4),(Q(111,175),Q(64,175))
t = Q(3,4)
for r in range(3):
    check(moment(a_counts,a_weights,t,r) == moment(b_counts,b_weights,t,r), 'shifted_collision_through_two')
third_gap = moment(a_counts,a_weights,t,3)-moment(b_counts,b_weights,t,3)
check(third_gap == Q(26973,6553600), 'shifted_collision_third_gap')
for ys in product([0,1],repeat=2):
    check(word(a_counts,a_weights,t,ys) == word(b_counts,b_weights,t,ys), 'shifted_pair_law_collision')
check(tuple(j//reduce(gcd,a_counts) for j in a_counts) != tuple(j//reduce(gcd,b_counts) for j in b_counts), 'shifted_different_primitives')

# Fresh-resampling counterfeit and second-moment repair.
for i in range(33):
    x = Q(i,32)
    t = 1-x
    s = (t+t*t)/2
    r_pure = 1-s
    check(r_pure-x == x*(1-x)/2, 'fresh_calibration_deviation')
    check(0 <= r_pure-x <= Q(1,8), 'fresh_uniform_band')
    held = (t*t+t**4)/2
    check(held-s*s == t*t*(1-t)**2/4, 'held_second_gap_formula')
    check((held>s*s) == (0<t<1), 'held_second_gap_strictness')
    for R in range(1,7):
        check(s**R == ((t+t*t)/2)**R, 'fresh_full_law_means')
check((1-(Q(1,2)+Q(1,2)**2)/2)-Q(1,2) == Q(1,8), 'fresh_band_attained')

# Label-dependent calibration makes nonproportional supports indistinguishable.
for u in [Q(1,5),Q(1,2),Q(3,4)]:
    t=u**3
    left_nodes=(t,t**2)
    right_nodes=(t,(u**2)**3)
    check(left_nodes==right_nodes, 'label_dependent_counterfeit_atoms')
    for R in range(1,5):
        for ys in product([0,1],repeat=R):
            def scalar_word(nodes):
                ans=Q()
                for z,w in zip(nodes,(Q(2,5),Q(3,5))):
                    val=w
                    for y in ys:
                        val*=z if y else 1-z
                    ans+=val
                return ans
            check(scalar_word(left_nodes)==scalar_word(right_nodes), 'label_dependent_counterfeit_words')

# Endpoint collapse: only zero mass is retained at survival 0; nothing at 1.
for counts in [(0,1,3),(0,2,8),(0,5,9)]:
    weights = (Q(1,4),Q(1,3),Q(5,12))
    for R in range(1,5):
        for ys in product([0,1],repeat=R):
            expected0 = Q(1,4) if all(ys) else Q(3,4) if not any(ys) else Q()
            check(word(counts,weights,Q(),ys) == expected0, 'survival_zero_collapse')
            check(word(counts,weights,Q(1),ys) == (1 if all(ys) else 0), 'survival_one_collapse')

# Supplied primitive signature: F strictly preserves pure-scale interval separation.
v = (2,3,7)
w0,weights = Q(1,7),(Q(1,7),Q(2,7),Q(3,7))
def F(b):
    return w0 + sum((w*b**j for w,j in zip(weights,v)), Q())
thresholds = []
for D in range(2,17):
    k = D-1
    u = Q(k,k+1)
    tstar,sstar = u**(k+1),u**k
    eta = (sstar-tstar)/2
    thresholds.append(eta)
    check(eta == Q(1,2*(k+1))*Q(k,k+1)**k, 'adjacent_sharp_radius')
    check(F(tstar**k) == F(sstar**(k+1)), 'F_boundary_touch')
    mid = (tstar+sstar)/2
    for lam in [Q(),Q(1,3),Q(7,8),Q(99,100)]:
        A,B = mid-lam*eta,mid+lam*eta
        check(0<tstar<A<=B<sstar<1, 'subcritical_interior')
        for j in range(1,D):
            check(A**j > B**(j+1), 'pure_scale_separation')
            check(F(A**j) > F(B**(j+1)), 'F_scale_separation')
check(all(a>b for a,b in zip(thresholds,thresholds[1:])), 'decreasing_thresholds')

# General pair parameterization and derivative-sign control, all exact.
for d,e in combinations(range(1,10),2):
    last_x = Q(2)
    for m in range(65):
        u = Q(m,64)
        td,se = u**e,u**d
        x = 1-(td+se)/2
        check(td**d == se**e, 'general_pair_power_identity')
        check((1-td)-x == (se-td)/2, 'general_pair_midpoint_deviation')
        check(x < last_x, 'general_pair_command_strict_monotone')
        last_x = x
        if u:
            derivative = d*u**(d-1)-e*u**(e-1)
            bracket = d-e*u**(e-d)
            check((derivative>0)-(derivative<0) == (bracket>0)-(bracket<0), 'general_pair_derivative_sign')
    h=e-d
    if d%h==0:
        a=Q(d,e)
        maxdiff=(1-a)*a**(d//h)
        radius=Q(e-d,2*e)*Q(d,e)**(d//h)
        check(maxdiff/2 == radius, 'general_pair_exact_critical_radius')

# A fixed-command restricted-band feasibility example and extension check.
x0 = Q(1,2)
u = Q(3,4)
b = u**12
eta = Q(1,4)
feasible = []
for d in [1,2,3,4]:
    y0=1-u**(12//d)
    if abs(y0-x0)<=eta:
        feasible.append(d)
    for i in range(65):
        x=Q(i,64)
        y=y0*x/x0 if x<=x0 else y0+(1-y0)*(x-x0)/(1-x0)
        check(0<=y<=1, 'piecewise_feasibility_range')
        check(abs(y-x)<=abs(y0-x0), 'piecewise_feasibility_supremum')
check(feasible == [3,4], 'restricted_band_removes_scale')

# Adaptive held-latent protocols: a randomized choice and an outcome-dependent stop.
def adaptive_law(d,e,left,limit):
    result = defaultdict(Q)
    vs=(0,1,3)
    ws=(Q(1,5),Q(1,2),Q(3,10))
    for seed in [0,1]:
        for v,w in zip(vs,ws):
            def recurse(history,commands,prob):
                n=len(history)
                if n==limit or (n>=2 and history[-2:]==(seed,seed)):
                    result[(seed,commands,history)] += prob
                    return
                u=Q(1+(sum(history)+2*n+seed)%5,6)
                x=1-(u**d+u**e)/2
                t=u**e if left else u**d
                count=d*v if left else e*v
                z=t**count
                recurse(history+(1,),commands+(str(x),),prob*z)
                recurse(history+(0,),commands+(str(x),),prob*(1-z))
            recurse((),(),w/2)
    return dict(result)
for d,e in [(1,2),(2,3),(2,5),(3,7)]:
    for limit in [2,4,6]:
        a=adaptive_law(d,e,True,limit)
        b_law=adaptive_law(d,e,False,limit)
        check(a==b_law, 'adaptive_held_latent_transcript_identity')
        check(sum(a.values(),Q()) == 1, 'adaptive_stopped_normalization')
        if limit>2:
            check(any(len(key[2])<limit and p>0 for key,p in a.items()), 'adaptive_early_stop_exercised')

for path, expected in PREDECESSORS.items():
    check(digest(BASE / path) == expected, 'predecessor_after')

output = {
    'status':'PASS',
    'assertions_passed':sum(COUNTS.values()),
    'families':dict(sorted(COUNTS.items())),
    'shifted_collision':{
        'm1':str(moment(a_counts,a_weights,t=Q(3,4),r=1)),
        'm2':str(moment(a_counts,a_weights,t=Q(3,4),r=2)),
        'm3_gap':str(third_gap),
    },
    'fixed_command_restricted_feasible_scales':feasible,
    'program_sha256':digest(Path(__file__)),
    'predecessor_bindings':PREDECESSORS,
    'scope':'Finite exact diagnostics supporting a separately written mathematical review; no universal theorem is certified by enumeration.'
}
(ROOT/'results'/'independent_controls.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
print(json.dumps(output,indent=2,sort_keys=True))
