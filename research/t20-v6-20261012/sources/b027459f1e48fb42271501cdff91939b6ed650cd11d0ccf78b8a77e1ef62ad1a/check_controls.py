#!/usr/bin/env python3
"""Exact finite controls; not a universal inverse implementation or halting proof."""
from fractions import Fraction as F
from itertools import product
from math import prod, comb
from pathlib import Path
import json

checks = {}
def check(group, condition):
    if not condition:
        raise AssertionError(group)
    checks[group] = checks.get(group, 0) + 1

def component(x, r, a):
    return x**a * (1-x)**(r-a)
def tensor(k, r):
    return tuple(prod((k[a] for a in ix), start=F(1)) for ix in product(range(len(k)), repeat=r))
def moment(p, ks, r):
    ts = [tensor(k,r) for k in ks]
    return tuple(sum((p[j]*ts[j][i] for j in range(len(p))),F(0)) for i in range(len(ts[0])))
def l1(x): return sum(map(abs,x),F(0))

# Interior perturbations of b_j=2^(-j-1), with cap c_j=2^(-j), C=2.
# Unlisted tails are unchanged and sum to 2^-N for b, 2^(1-N) for c.
collisions=[]
for R in range(9):
    N=R+2
    xs=[F(1,j+2) for j in range(N)]
    hs=[1/prod((xs[j]-xs[i] for i in range(N) if i!=j), start=F(1)) for j in range(N)]
    bs=[F(1,2**(j+1)) for j in range(N)]
    cs=[2*b for b in bs]
    t=min(bs[j]/(2*abs(hs[j])) for j in range(N))
    pp=[bs[j]+t*hs[j] for j in range(N)]
    pm=[bs[j]-t*hs[j] for j in range(N)]
    check('finite_cutoff', sum(hs)==0)
    check('finite_cutoff', sum(pp)+F(1,2**N)==1)
    check('finite_cutoff', sum(pm)+F(1,2**N)==1)
    check('finite_cutoff', all(0<pp[j]<cs[j] and 0<pm[j]<cs[j] for j in range(N)))
    for r in range(R+1):
        for a in range(r+1):
            check('finite_cutoff', sum((hs[j]*component(xs[j],r,a) for j in range(N)),F(0))==0)
    nextdiff=sum((2*t*hs[j]*xs[j]**(R+1) for j in range(N)),F(0))
    check('finite_cutoff', nextdiff==2*t and nextdiff!=0)
    collisions.append({'R':R,'active_block':N,'perturbation':str(t),'next_moment_difference':str(nextdiff)})

# Finite-dimensional operator norms and mass in grade arrays.
ks=[(F(1),F(0),F(0)),(F(0),F(1,3),F(2,3)),(F(1,2),F(1,4),F(1,4))]
laws=[(F(1,4),F(1,4),F(1,2)),(F(1,2),F(1,3),F(1,6)),(F(0),F(1),F(0))]
for r in range(6):
    for p in laws:
        a=moment(p,ks,r)
        check('tensor_norm',sum(a)==1 and min(a)>=0)
        for q in laws:
            b=moment(q,ks,r)
            diff=tuple(x-y for x,y in zip(a,b))
            check('tensor_norm',max(map(abs,diff))<=l1(diff)<=l1(tuple(x-y for x,y in zip(p,q))))

# Duplicate columns, despite different labelled laws.
for r in range(9):
    check('duplicate_alias',moment((F(1,3),F(2,3)),[(F(2,5),F(3,5))]*2,r)==moment((F(2,3),F(1,3)),[(F(2,5),F(3,5))]*2,r))

# Accumulation at a listed atom. The infinite metric bound is proved by sum r/2^r=2.
for j in range(1,17):
    x=F(1,2**j)
    partial=F(0)
    for r in range(1,13):
        dif=max(abs(component(x,r,a)-component(F(0),r,a)) for a in range(r+1))
        check('accumulation',dif<=r*x)
        partial+=F(1,2**r)*dif
    check('accumulation',partial<=2*x)
    check('accumulation',l1((F(1),F(-1)))==2)

# Moment band triangle and recovery-center margins.
for n in range(25):
    delta=F(1,2**n); eta=delta/4
    check('band_arithmetic',2*eta<=delta)
for k in range(25):
    eps=F(1,2**k)
    check('band_arithmetic',eps/2+eps/4<eps)

# Finite toy event sets test encoding and the baseline/tail algebra only.
def pair(e,t): return (e+t)*(e+t+1)//2+t
seen=set()
for e in range(20):
    for t in range(20):
        j=1+pair(e,t)
        check('event_pairing',j>=1 and j not in seen)
        seen.add(j)
events={0:1,2:0,3:4,5:2,8:1}
weights={1+pair(e,t):F(1,4**(e+1)) for e,t in events.items()}
alpha=sum(weights.values(),F(0))
check('event_mass',0<=alpha<=F(1,3))
for e in range(20):
    w=F(1,4**(e+1))
    # Sum all later possible digits = w/3; error w/12 leaves threshold 2w/3 strict.
    check('digit_gap',w/3+w/12<2*w/3<w-w/12)
for r in range(1,8):
    for a in range(r+1):
        base=component(F(0),r,a)
        direct=(1-alpha)*base+sum((p*component(F(1,2**j),r,a) for j,p in weights.items()),F(0))
        baseline=base+sum((p*(component(F(1,2**j),r,a)-base) for j,p in weights.items()),F(0))
        check('event_moments',direct==baseline)
        for N in (1,2,5,10,20):
            trunc=base+sum((p*(component(F(1,2**j),r,a)-base) for j,p in weights.items() if j<N),F(0))
            check('event_moments',abs(direct-trunc)<=F(r,2**N))

# A bounded positive reweighting can leave the original cap, but respects (M/m)c.
p=(F(3,4),F(1,4)); c=(F(3,4),F(3,4)); factors=(F(2),F(1,2))
z=sum((x*a for x,a in zip(p,factors)),F(0)); out=tuple(x*a/z for x,a in zip(p,factors))
check('tilt_cap',out[0]>c[0])
check('tilt_cap',all(out[j]<=4*c[j] for j in range(2)))
check('tilt_cap',sum(out)==1 and min(factors)<=z<=max(factors))

# Coefficients of direct all-moment tilt continuation, before exponential summation.
xs=(F(0),F(1,3),F(3,4)); ps=(F(1,4),F(1,4),F(1,2)); u=(F(2),F(-1))
for s in range(5):
    for a in range(s+1):
        for r in range(7):
            direct=sum((p*component(x,s,a)*(u[0]*x+u[1]*(1-x))**r for x,p in zip(xs,ps)),F(0))
            contracted=sum((comb(r,b)*u[0]**b*u[1]**(r-b)*sum((p*component(x,s+r,a+b) for x,p in zip(xs,ps)),F(0)) for b in range(r+1)),F(0))
            check('direct_tilt_coefficients',direct==contracted)

result={'status':'PASS','checks':sum(checks.values()),'groups':checks,'finite_cutoff_witnesses':collisions,'limits':'Exact finite rational controls only. No universal inverse implementation, finite sampling theorem, universal termination replay, or computability/noncomputability proof by testing.'}
path=Path(__file__).with_name('CONTROLS.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
