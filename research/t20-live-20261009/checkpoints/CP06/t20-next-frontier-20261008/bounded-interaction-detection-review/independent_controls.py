#!/usr/bin/env python3
"""Independent rational-interval controls, not a proof or uniform cost bound."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, hashlib, os

OUT=Path(__file__).resolve().parent
STATS={'world_name_runs':0,'support_decisions':0,'raw_queries':0,'max_bits':0,'unary_signs':0,'unary_recoveries':0}

def subsets(mask):
    t=mask
    while True:
        yield t
        if not t: break
        t=(t-1)&mask

def mul(xs):
    r=F(1)
    for x in xs:r*=x
    return r

class World:
    def __init__(self,d,counts,powers=None,high=False):
        self.d=d;self.counts=counts;self.powers=powers or tuple(range(1,d+1));self.high=high
    def rate(self,i,x):
        return 1-(1-x)**self.powers[i] if self.high else x**self.powers[i]
    def q(self,x):
        return mul((1-mul(self.rate(i,x[i]) for i in range(self.d) if s>>i&1))**n for s,n in self.counts.items() if n)

class Oracle:
    def __init__(self,world,style):self.world=world;self.style=style;self.calls=0;self.maxbits=0
    def interval(self,x,bits):
        # Algorithm sees only a valid rational centre and its requested error.
        eps=F(1,2**bits);q=self.world.q(x)
        if self.style=='above':centre=q+eps
        elif self.style=='below':centre=q-eps
        elif self.style=='floor':centre=F((q*2**bits).__floor__(),2**bits)
        else:
            code=sum((i+1)*(v.numerator+v.denominator) for i,v in enumerate(x))+bits
            centre=q+eps if code%2 else q-eps
        self.calls+=1;self.maxbits=max(self.maxbits,bits)
        assert abs(centre-q)<=eps
        return max(F(0),centre-eps),min(F(1),centre+eps)

def quotient_interval(values,signs):
    lo=F(1);hi=F(1)
    for (a,b),sgn in zip(values,signs):
        if sgn==1:lo*=a;hi*=b
        else:
            if a<=0:return None
            lo/=b;hi/=a
    return max(F(0),lo),min(F(1),hi)

def support_detection(d,M,oracle):
    assert isinstance(M,int) and M>=0
    allmask=(1<<d)-1
    if M==0:return set(),{},set(),[]
    corners={}
    for mask in range(1<<d):
        x=tuple(F((mask>>i)&1) for i in range(d))
        lo,hi=oracle.interval(x,3)
        # Both decisions are strict and justified by the {0,1} promise.
        if hi<F(1,2):corners[mask]=True
        elif lo>F(1,2):corners[mask]=False
        else:raise AssertionError('corner not separated')
    if not corners[allmask]:return set(),{},set(),[]
    minimal=[s for s in range(1,allmask+1) if corners[s] and not any(corners[t] for t in subsets(s) if t!=s)]
    A=0
    for s in minimal:A|=s
    B=allmask^A
    lambdas={}
    for s in minimal:
        x=tuple(F(1,2) if s>>i&1 else F(0) for i in range(d))
        bits=1
        while True:
            lo,hi=oracle.interval(x,bits)
            if hi<1:break
            bits+=1
        lower=(1-hi)/M
        assert lower>0
        for i in range(d):
            if s>>i&1:lambdas[i]=max(lambdas.get(i,F(0)),lower)
    grid=[]
    for u in subsets(A):
        for v in subsets(B):
            x=tuple(F(1,2) if u>>i&1 else F(1) if v>>i&1 else F(0) for i in range(d))
            grid.append((u,v,x))
    found=set()
    for t in subsets(A):
        if not t:continue
        gap=mul(lambdas[i] for i in range(d) if t>>i&1)
        cut=1-gap/2
        for h in subsets(B): # H=empty is essential.
            leaves=[(u,v,x) for u,v,x in grid if u&t==u and v&h==v]
            signs=[(-1)**((t.bit_count()-u.bit_count())+(h.bit_count()-v.bit_count())) for u,v,x in leaves]
            bits=1
            while True:
                intervals=[oracle.interval(x,bits) for u,v,x in leaves]
                iv=quotient_interval(intervals,signs)
                if iv is not None:
                    lo,hi=iv
                    if hi<cut:found.add(t|h);break
                    if lo>cut:break
                bits+=1
            STATS['support_decisions']+=1
    return found,lambdas,set(i for i in range(d) if A>>i&1),minimal

def isolated(oracle,s,x,bits):
    d=len(x);masks=list(subsets(s))
    vals=[oracle.interval(tuple(x[i] if t>>i&1 else F(0) for i in range(d)),bits) for t in masks]
    return quotient_interval(vals,[(-1)**(s.bit_count()-t.bit_count()) for t in masks])

def root_bracket(y,degree,bits):
    lo=F(0);hi=F(1)
    for unused in range(bits):
        mid=(lo+hi)/2
        if mid**degree<=y:lo=mid
        else:hi=mid
    return lo,hi

def power_interval(iv,num,den,bits):
    lo,hi=iv
    return root_bracket(lo**num,den,bits)[0],root_bracket(hi**num,den,bits)[1]

def complement(iv):return 1-iv[1],1-iv[0]
def times(a,b):return a[0]*b[0],a[1]*b[1]
def minus(a,b):return a[0]-b[1],a[1]-b[0]

def unary_sign(oracle,i,s,n,h):
    d=oracle.world.d
    commands=[tuple(F(1,4) if j==i else F(1,2) for j in range(d)),tuple(F(3,4) if j==i else F(1,2) for j in range(d))]
    bits=4
    while True:
        zs=[isolated(oracle,s,x,bits) for x in commands]
        us=[isolated(oracle,1<<i,x,bits) for x in commands]
        if all(iv is not None for iv in zs+us):
            ps=[complement(power_interval(z,1,n,bits)) for z in zs]
            rs=[complement(power_interval(u,h.denominator,h.numerator,bits)) for u in us]
            D=minus(times(rs[1],ps[0]),times(rs[0],ps[1]))
            if D[1]<0:STATS['unary_signs']+=1;return -1
            if D[0]>0:STATS['unary_signs']+=1;return 1
        bits+=2

def recover_unary(oracle,i,s,n,M):
    lo=1;hi=M
    while lo<hi:
        k=(lo+hi)//2
        if unary_sign(oracle,i,s,n,F(2*k+1,2))>0:hi=k
        else:lo=k+1
    return lo

def inventories(d,M):
    masks=list(range(1,1<<d))
    def rec(j,left,out):
        if j==len(masks):yield dict(out);return
        for n in range(left+1):
            if n:out[masks[j]]=n
            else:out.pop(masks[j],None)
            yield from rec(j+1,left-n,out)
        out.pop(masks[j],None)
    yield from rec(0,M,{})

def accumulate(o):
    STATS['raw_queries']+=o.calls;STATS['max_bits']=max(STATS['max_bits'],o.maxbits)

def check_world(w,M,style):
    o=Oracle(w,style)
    got,lb,A,mins=support_detection(w.d,M,o)
    expected={s for s,n in w.counts.items() if n}
    assert got==expected,(w.d,w.counts,M,style,got)
    assert all(lower<=w.rate(i,F(1,2)) for i,lower in lb.items())
    if expected:
        Amask=sum(1<<i for i in A)
        assert all(s&Amask for s in expected)
    STATS['world_name_runs']+=1;accumulate(o)

for d,M in [(0,0),(0,3),(1,3),(2,4),(3,3),(4,2)]:
    for counts in inventories(d,M):
        for style in ['above','below','alternating','floor']:
            check_world(World(d,counts),M,style)

# Overlapping minimal supports; swallowed interactions; no singleton routes;
# unused B coordinates; H empty; all roots in A; tiny interior A rates.
special=[
    (World(4,{1:2,3:1,5:1,15:2}),6),
    (World(4,{3:2,5:1,7:2,15:1}),6),
    (World(4,{3:1,12:1,15:2}),4),
    (World(4,{1:1}),1),
    (World(3,{7:1}),1),
    (World(3,{1:7,3:1,7:1},powers=(80,3,2)),9),
    (World(3,{1:5,2:4,3:2,7:1},powers=(10,7,3),high=True),12),
]
for w,M in special:
    for style in ['above','below','alternating','floor']:check_world(w,M,style)

# Positive anchored unary counts, with lower-order nuisance routes and unknown maps.
for m in range(1,9):
    for style in ['above','below','alternating','floor']:
        w=World(3,{1:m,2:2,3:3,7:1},powers=(3,2,1))
        o=Oracle(w,style)
        assert unary_sign(o,0,3,3,F(2*m-1,2))==-1
        assert unary_sign(o,0,3,3,F(2*m+1,2))==1
        assert recover_unary(o,0,3,3,m+6)==m
        STATS['unary_recoveries']+=1;accumulate(o)

# Full count-fibre controls: positive integer tuples, total ceiling, and collapse.
fibres=[]
for k in range(5):
    for budget in range(k,k+4):
        tuples=[t for t in product(range(1,budget+1),repeat=k) if sum(t)<=budget]
        if k==0:assert tuples==[()]
        else:
            assert (len(tuples)==1)==(budget==k)
            assert all({t[i] for t in tuples}==set(range(1,budget-k+2)) for i in range(k))
        fibres.append({'isolated_roots':k,'residual_budget':budget,'feasible_tuples':len(tuples)})

# Explicit same-response bounded unary gauge; both actual maps rational.
for x in [F(i,16) for i in range(17)]:
    assert (1-x)**2==1-(2*x-x*x)

prior=json.loads((OUT/'PRIOR_SHA256.json').read_text())
b=Path(os.environ.get('PRIOR_BINDING_BASE',str(OUT.parent)))
assert all(hashlib.sha256((b/p).read_bytes()).hexdigest()==h for p,h in prior.items())
result={'status':'PASS','stats':STATS,'count_fibre_controls':fibres,'prior_files_unchanged':len(prior),'scope':'finite exact controls only; all-name correctness and termination require the proof in REVIEW.md'}
(OUT/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
