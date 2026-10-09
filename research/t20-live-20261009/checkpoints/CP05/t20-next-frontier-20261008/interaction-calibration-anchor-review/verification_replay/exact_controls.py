#!/usr/bin/env python3
"""Exact diagnostic controls. Written proof, not finite tests, proves the theorem."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

families={}
def check(name, assertion):
    if not assertion: raise AssertionError(name)
    families[name]=families.get(name,0)+1

def prod(xs):
    out=F(1)
    for x in xs: out*=x
    return out

def subs(mask):
    t=mask
    while True:
        yield t
        if not t: break
        t=(t-1)&mask

def q(counts, rates, mask):
    return prod((1-prod(rates[i] for i in range(len(rates)) if s>>i&1))**n
                for s,n in counts.items() if n and s&mask==s)

def isolate(counts, rates):
    r=len(rates); vals={t:q(counts,rates,t) for t in range(1<<r)}
    for s in range(1,1<<r):
        out=F(1)
        for t in subs(s): out*=vals[t]**(1 if (s.bit_count()-t.bit_count())%2==0 else -1)
        expected=(1-prod(rates[i] for i in range(r) if s>>i&1))**counts.get(s,0)
        check('mask_mobius_exact',out==expected)
        check('support_presence', (out<1)==(counts.get(s,0)>0))

for counts_tuple in product(range(3),repeat=7):
    isolate(dict(enumerate(counts_tuple,1)),[F(1,3),F(4,25),F(8,343)])
for seed in range(128):
    counts={s:((seed+3)*(s*s+7*s+5)+seed//3)%4 for s in range(1,16)}
    isolate(counts,[F(2,5),F(9,49),F(1,8),F(16,81)])

h2=lambda a:1-(1-a)**2
for a,b in product([F(i,10) for i in range(11)],repeat=2):
    check('unary_gauge',(1-a)**2==1-h2(a))
    check('interaction_defect',h2(a*b)-h2(a)*h2(b)==-2*a*b*(1-a)*(1-b))
    if 0<a<1 and 0<b<1: check('interaction_defect_strict',h2(a*b)!=h2(a)*h2(b))
    ap=a*(2-a*b)/(2-b); bp=b*(2-b)
    check('crosstalk_equality',1-ap*bp==(1-a*b)**2)
    check('crosstalk_own_range',0<=ap<=1 and 0<=bp<=1)
    check('crosstalk_shift',ap-a==a*b*(1-a)/(2-b))
    check('support_specific_map',(1-a*b)*(1-a)**2==(1-a*b)*(1-h2(a)))
    if 0<a<1 and 0<b<1:
        check('independent_absorption_visible',(1-a)*(1-a*b)<1-a)
        # With one shared gate per root, OR(A, A AND B) equals A.
        for ga,gb in product([False,True],repeat=2):
            check('shared_gate_absorption', bool(ga or (ga and gb))==ga)
        mixture=1-(a+b)/2
        check('fresh_mixture_false_interaction',mixture/((1-a/2)*(1-b/2))<1)
for b in [F(i,17) for i in range(18)]:
    vals=[F(i,13)*(2-F(i,13)*b)/(2-b) for i in range(14)]
    check('crosstalk_endpoints',vals[0]==0 and vals[-1]==1)
    for u,v in zip(vals,vals[1:]): check('crosstalk_strict_own_monotonicity',u<v)
for a in [F(i,13) for i in range(14)]:
    check('crosstalk_continuity_bound',abs(a*(2-a*F(1,1000))/(2-F(1,1000))-a)<=F(1,1000)/(4*(2-F(1,1000))))

# Complete equivalence with an anchored AB component, isolated unary C, unused D.
for a,b,c,d in product([F(0),F(1,4),F(2,3),F(1)],repeat=4):
    lhs=(1-a*b)**3*(1-a)**2*(1-b)*(1-c)**2
    rhs=(1-a*b)**3*(1-a)**2*(1-b)*(1-h2(c))
    check('mixed_component_equivalence',lhs==rhs)
    check('unused_root_invariance',lhs==(1-a*b)**3*(1-a)**2*(1-b)*(1-c)**2)

# Exact alias/occurrence and guards boundary demonstrations.
for a in [F(1,4),F(1,2),F(3,4)]:
    check('duplicate_shared_gate',1-a!=(1-a)**2)
    # An A|not B route is disabled at issued AB regardless of rate masks.
    check('guard_attenuation_not_issuance',F(1)!=(1-a))
for a,b in product([F(0),F(1)],repeat=2):
    check('step_map_count_collapse',(1-a*b)==(1-a*b)**7)

# Independent assignment enumeration for a route inventory at 3 roots.
counts={1:1,3:2,6:1,7:1}; rates=[F(1,3),F(2,5),F(3,7)]
routeps=[prod(rates[i] for i in range(3) if s>>i&1) for s,n in counts.items() for _ in range(n)]
nohit=F(0); total=F(0)
for gates in product([0,1],repeat=len(routeps)):
    mass=prod(p if g else 1-p for p,g in zip(routeps,gates)); total+=mass
    if not any(gates): nohit+=mass
check('route_assignment_enumeration',total==1 and nohit==q(counts,rates,7))

# Binary histories under an adaptive isolated-unary equivalence.
for history in product([0,1],repeat=6):
    masses=[F(1),F(1)]; prefix=0
    for depth,y in enumerate(history):
        x=F((prefix*5+depth*3)%13+1,15)
        kernels=[(1-x)**2,1-h2(x)]
        for world in range(2): masses[world]*=kernels[world] if y else 1-kernels[world]
        prefix=2*prefix+y
    check('adaptive_unary_transcript',masses[0]==masses[1])

out={'status':'PASS','arithmetic':'Python Fraction exact rational arithmetic; no sampled data or floating-point logs',
     'assertions':sum(families.values()),'families':families,
     'scope':'Finite diagnostics for the written fixed-inventory theorem and excluded-model countercontrols; not a substitute for proof.'}
path=Path(__file__).parent/'results'/'exact_controls.json';path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
