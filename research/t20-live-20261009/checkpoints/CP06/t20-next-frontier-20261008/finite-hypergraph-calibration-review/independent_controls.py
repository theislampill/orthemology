#!/usr/bin/env python3
"""Independent finite calibration controls. Standard library; no author imports.
Exact rational fixtures are converted to certified intervals before recovery.
"""
from fractions import Fraction as F
from itertools import product, combinations
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
stats = {'assertions': 0, 'raw_grid_equalities': 0, 'unary_recoveries': 0,
         'unary_sign_decisions': 0, 'raw_oracle_calls': 0, 'max_precision_bits': 0}

def check(ok):
    stats['assertions'] += 1
    assert ok

def rank(a):
    a = [list(map(F, r)) for r in a]
    if not a: return 0
    r=0
    for c in range(len(a[0])):
        k=next((i for i in range(r,len(a)) if a[i][c]),None)
        if k is None: continue
        a[r],a[k]=a[k],a[r]
        d=a[r][c]; a[r]=[x/d for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                d=a[i][c];a[i]=[x-d*y for x,y in zip(a[i],a[r])]
        r+=1
    return r

def incidence(supports, n):
    return [[int(i in s) for i in range(n)] for s in supports]

def identified(a,i):
    e=[int(j==i) for j in range(len(a[0]))]
    return rank(a+[e])==rank(a)

def qvalue(counts, values):
    q=F(1)
    for s,n in counts.items():
        p=F(1)
        for i in s:p*=values[i]
        q *= (1-p)**n
    return q

def masks(s):
    s=tuple(sorted(s))
    for n in range(len(s)+1):
        for t in combinations(s,n):yield frozenset(t)

def contrast(counts,s,values):
    z=F(1)
    for t in masks(s):
        q=qvalue(counts,[values[i] if i in t else F(0) for i in range(len(values))])
        z *= q if (len(s)-len(t))%2==0 else 1/q
    return z

triangle=incidence([{0,1},{0,2},{1,2}],3)
square=incidence([{0,1},{1,2},{2,3},{3,0}],4)
star=incidence([{0,1},{0,2},{0,3}],4)
partial=incidence([{0,1},{0,1,2}],3)
check(rank(triangle)==3)
check(rank(square)==3)
check(rank(star)==3)
check([identified(partial,i) for i in range(3)]==[False,False,True])
check(rank(square+[[1,0,0,0]])==4)
check(rank(star+[[0,0,1,0]])==4)
check(rank(incidence([{0,1},{1,2},{2,0},{3,4},{4,5}],6))==5)
# Ordinary incidence, not oriented incidence: the odd cycle has no kernel.
check(sum(square[0][i]*[1,-1,1,-1][i] for i in range(4))==0)
check(sum([1,-1,1,-1])==0)
# No mass-zero constraint: star kernel vector has nonzero sum.
star_gauge=[1,-1,-1,-1]
check(all(sum(x*y for x,y in zip(row,star_gauge))==0 for row in star))
check(sum(star_gauge)==-2)

counts={frozenset({0,1}):2,frozenset({1,2}):1,frozenset({2,3}):3,
        frozenset({3,0}):2,frozenset({0,1,2,3}):1}
levels=[[F(0),F(1,5),F(2,5)],[F(0),F(1,4),F(1,2)],
        [F(0),F(1,6),F(1,3)],[F(0),F(1,3),F(2,3)]]
scale=[F(6,5),F(5,6),F(6,5),F(5,6)]
new_levels=[[x*scale[i] for x in l] for i,l in enumerate(levels)]
check(all(0<l[1]<l[2]<1 for l in new_levels))
for choices in product(range(3),repeat=4):
    x=[levels[i][j] for i,j in enumerate(choices)]
    xp=[new_levels[i][j] for i,j in enumerate(choices)]
    check(qvalue(counts,x)==qvalue(counts,xp))
    stats['raw_grid_equalities']+=1
base=[l[1] for l in levels]
for s,n in counts.items():
    p=F(1)
    for i in s:p*=base[i]
    check(contrast(counts,s,base)==(1-p)**n)
# At a unit endpoint, root 0 returns to 1 in both worlds; a neighbor's
# rescaled interior value remains different, so arbitrary endpoint grids fail.
unit=[F(1),levels[1][1],F(0),F(0)]
unitp=[F(1),new_levels[1][1],F(0),F(0)]
check(qvalue(counts,unit)!=qvalue(counts,unitp))
# Triangle inverse and partial AB/ABC inverse, with exact rational controls.
ab,ac,bc=F(1,20),F(1,15),F(1,12)
check(ab*ac/bc==F(1,5)**2)
check(ab*bc/ac==F(1,4)**2)
check(ac*bc/ab==F(1,3)**2)
check(F(1,60)/ab==F(1,3))

# Unary strict-sign controls with rational known H_c values.
a,b=F(1,5),F(2,5);rho=b/a
H2=lambda z:2*z-z*z
check(H2(b)-rho*H2(a)==-b*(b-a)<0)
# c=1/2 and inputs with square complements: H_(1/2)(9/25)=1/5,
# H_(1/2)(16/25)=2/5.
check(F(2,5)-(F(16,25)/F(9,25))*F(1,5)>0)
# Positive unary counts can be traded against calibration if no ratio is given.
for x in [a,b]:check((1-x)**2==1-H2(x))
check(H2(b)/H2(a)!=b/a)

def mul(x,y):return x[0]*y[0],x[1]*y[1]
def div(x,y):
    if y[0]<=0:return None
    return x[0]/y[1],x[1]/y[0]

def root_endpoint(z,p,d,bits):
    """Rational enclosure for z**(p/d), z in [0,1], p,d positive ints."""
    lo,hi=F(0),F(1)
    target=z**p
    for _ in range(bits):
        mid=(lo+hi)/2
        if mid**d<=target:lo=mid
        else:hi=mid
    return lo,hi

def power_interval(z,p,d,bits):
    lo=max(F(0),z[0]);hi=min(F(1),z[1])
    if lo>hi:raise AssertionError('invalid interval')
    return root_endpoint(lo,p,d,bits)[0],root_endpoint(hi,p,d,bits)[1]

def one_minus(z):return 1-z[1],1-z[0]

def make_oracle(n,style):
    # Unknown n is private fixture state; the recovery code sees only the oracle.
    known_ab=2
    cs={frozenset({0}):n,frozenset({1}):3,frozenset({0,1}):known_ab}
    def oracle(a_level,b_level,bits):
        stats['raw_oracle_calls']+=1
        vals=[F(0) if a_level==0 else [a,b][a_level-1],F(1,3) if b_level else F(0)]
        v=qvalue(cs,vals);den=2**bits
        k=v.numerator*den//v.denominator
        if style==0:return max(F(0),F(k,den)),min(F(1),F(k+1,den))
        return max(F(0),F(k-1,den)),min(F(1),F(k+2,den))
    return oracle

def ratio_and_solos(oracle,bits):
    solos=[oracle(l,0,bits) for l in (1,2)]
    qb=oracle(0,1,bits)
    ps=[]
    for l,solo in zip((1,2),solos):
        e=div(oracle(l,1,bits),mul(solo,qb))
        if e is None:return None
        ps.append(one_minus(power_interval(e,1,2,bits)))
    ratio=div(ps[1],ps[0])
    if ratio is None:return None
    return ratio,solos

def unary_cut_interval(oracle,k,bits):
    got=ratio_and_solos(oracle,bits)
    if got is None:return None
    ratio,solos=got
    h=[one_minus(power_interval(z,2,2*k+1,bits)) for z in solos]
    rh=mul(ratio,h[0])
    return h[1][0]-rh[1],h[1][1]-rh[0]

def unary_cut(oracle,k):
    bits=2
    while True:
        stats['max_precision_bits']=max(stats['max_precision_bits'],bits)
        z=unary_cut_interval(oracle,k,bits)
        if z is not None and (z[0]>0 or z[1]<0):
            stats['unary_sign_decisions']+=1
            return 1 if z[0]>0 else -1
        bits*=2

def recover(oracle):
    high=1
    while unary_cut(oracle,high)<0:high*=2
    low=1
    while low<high:
        mid=(low+high)//2
        if unary_cut(oracle,mid)>0:high=mid
        else:low=mid+1
    return low

for n in range(1,13):
    for style in (0,1):
        oracle=make_oracle(n,style)
        check(recover(oracle)==n);stats['unary_recoveries']+=1
        check(unary_cut(oracle,n-1)==-1)
        check(unary_cut(oracle,n)==1)
zero_checks=0
for k in [0,1,2,8]:
    for bits in [8,16,32]:
        z=unary_cut_interval(make_oracle(0,0),k,bits)
        if z is not None:check(z[0]<=0<=z[1]);zero_checks+=1
stats['zero_unary_interval_checks']=zero_checks

# An independently discovered extension: a known interaction product supplies
# a positive lower bound for its participating unary rate. This decides unary
# zero versus positive despite the zero stall of D itself.
def unary_presence(oracle):
    bits=2
    while True:
        stats['max_precision_bits']=max(stats['max_precision_bits'],bits)
        za=oracle(1,0,bits);qb=oracle(0,1,bits);qab=oracle(1,1,bits)
        e=div(qab,mul(za,qb))
        if e is not None:
            p=one_minus(power_interval(e,1,2,bits))
            gap=(1-za[1]-p[1]/2,1-za[0]-p[0]/2)
            if gap[0]>0:return True
            if gap[1]<0:return False
        bits*=2
presence_cases=0
for n in range(13):
    for style in (0,1):
        check(unary_presence(make_oracle(n,style))==(n>0))
        presence_cases+=1
stats['anchored_unary_presence_decisions']=presence_cases

# Boundary reduction: no unary root 0 means setting it to one introduces no
# spontaneous term. Supports differing only by root 0 coalesce additively.
boundary_counts={frozenset({0,1}):2,frozenset({0,1,2}):3,
                 frozenset({1}):1,frozenset({1,2}):4,
                 frozenset({0,2}):5,frozenset({3}):2}
reduced={}
for support,n in boundary_counts.items():
    t=support-{0}
    check(bool(t))
    reduced[t]=reduced.get(t,0)+n
check(reduced[frozenset({1,2})]==7)
check(reduced[frozenset({1})]==3)
boundary_equalities=0
for choices in product(range(3),repeat=3):
    values=[F(1)]+[levels[i+1][j] for i,j in enumerate(choices)]
    check(qvalue(boundary_counts,values)==qvalue(reduced,values))
    check(qvalue(boundary_counts,values)>0)
    boundary_equalities+=1
check(qvalue(boundary_counts,[F(1),F(0),F(0),F(0)])==1)
with_unary=dict(boundary_counts);with_unary[frozenset({0})]=2
check(qvalue(with_unary,[F(1),F(0),F(0),F(0)])==0)
# Products invert to a_i by original/reduced division, with unequal aggregate
# count 7 rather than the original ABC count 3.
for ai in [F(1,5),F(2,5),F(3,5)]:
    vals=[ai,F(1,4),F(1,6),F(1,3)]
    original=contrast(boundary_counts,frozenset({0,1,2}),vals)
    boundary=contrast(reduced,frozenset({1,2}),[F(1)]+vals[1:])
    check(original==(1-ai*vals[1]*vals[2])**3)
    check(boundary==(1-vals[1]*vals[2])**7)
    check((ai*vals[1]*vals[2])/(vals[1]*vals[2])==ai)
stats['boundary_reduction_grid_equalities']=boundary_equalities

# Covered-root support presence: a known positive ABC support supplies all
# three base-rate lower bounds. Every other target's presence is tested with
# certified raw probabilities, not with exact contrast equality.
def general_oracle(counts, style):
    vals=[F(1,5),F(1,4),F(1,3)]
    def oracle(t,bits):
        stats['raw_oracle_calls']+=1
        v=qvalue(counts,[vals[i] if i in t else F(0) for i in range(3)])
        den=2**bits;k=v.numerator*den//v.denominator
        if style==0:return max(F(0),F(k,den)),min(F(1),F(k+1,den))
        return max(F(0),F(k-1,den)),min(F(1),F(k+2,den))
    return oracle

def general_contrast(oracle,s,bits):
    num=(F(1),F(1));den=(F(1),F(1))
    for t in masks(s):
        q=oracle(t,bits)
        if (len(s)-len(t))%2:den=mul(den,q)
        else:num=mul(num,q)
    e=div(num,den)
    if e is None:return None
    return max(F(0),e[0]),min(F(1),e[1])

def covered_presence(oracle,target):
    bits=2;seed=frozenset({0,1,2})
    while True:
        stats['max_precision_bits']=max(stats['max_precision_bits'],bits)
        es=general_contrast(oracle,seed,bits)
        et=general_contrast(oracle,target,bits)
        if es is not None and et is not None:
            p=one_minus(power_interval(es,1,2,bits))
            beta=(p[0]**len(target),p[1]**len(target))
            gap=(1-et[1]-beta[1]/2,1-et[0]-beta[0]/2)
            if gap[0]>0:return True
            if gap[1]<0:return False
        bits*=2
fixture={frozenset({0,1,2}):2,frozenset({1}):1,frozenset({2}):2,
         frozenset({0,1}):3,frozenset({1,2}):1}
covered_cases=0
for style in (0,1):
    oracle=general_oracle(fixture,style)
    for target in masks(frozenset({0,1,2})):
        if target:
            check(covered_presence(oracle,target)==(target in fixture))
            covered_cases+=1
stats['covered_support_presence_decisions']=covered_cases
stats['status']='PASS'
stats['caveat']='Finite controls support the proof audit; observed costs are not uniform bounds.'
text=json.dumps(stats,indent=2,sort_keys=True)+'\n'
(OUT/'INDEPENDENT_CONTROLS.json').write_text(text)
print(text,end='')
