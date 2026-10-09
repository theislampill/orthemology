#!/usr/bin/env python3
"""Fair cover discovery and complete counts, without any count-ceiling input."""
from fractions import Fraction as F
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
STATS={'complete_world_name_runs':0,'positive_count_searches':0,'half_integer_signs':0,'raw_queries':0,'max_bits':0,'bounded_partial_checks':0}
def prod(xs):
    a=F(1)
    for x in xs:a*=x
    return a
def subs(s):
    t=s
    while True:
        yield t
        if not t:break
        t=(t-1)&s
class Oracle:
    def __init__(self,d,counts,style):self.d=d;self._counts=counts;self.style=style;self.calls=0;self.maxbits=0
    def interval(self,x,bits):
        q=prod((1-prod(x[i]**(i+1) for i in range(self.d) if s>>i&1))**n for s,n in self._counts.items() if n)
        e=F(1,2**bits)
        q=q+e if self.style==0 else q-e
        self.calls+=1;self.maxbits=max(self.maxbits,bits)
        return max(F(0),q-e),min(F(1),q+e)
def isolated(o,s,x,bits):
    lo=hi=F(1)
    for t in subs(s):
        a,b=o.interval(tuple(x[i] if t>>i&1 else F(0) for i in range(o.d)),bits)
        if (s.bit_count()-t.bit_count())%2:
            if a<=0:return None
            lo/=b;hi/=a
        else:lo*=a;hi*=b
    return max(F(0),lo),min(F(1),hi)
def root(y,n,bits):
    a=F(0);b=F(1)
    for unused in range(bits):
        mid=(a+b)/2
        if mid**n<=y:a=mid
        else:b=mid
    return a,b
def power(iv,num,den,bits):return root(iv[0]**num,den,bits)[0],root(iv[1]**num,den,bits)[1]
def comp(iv):return 1-iv[1],1-iv[0]
def mul(a,b):return a[0]*b[0],a[1]*b[1]
def sub(a,b):return a[0]-b[1],a[1]-b[0]
def interaction_sign(o,s,h):
    i,j=[i for i in range(o.d) if s>>i&1][:2]
    commands=[tuple(u if z==i else v if z==j else F(1,2) for z in range(o.d)) for u in [F(1,4),F(3,4)] for v in [F(1,4),F(3,4)]]
    bits=4
    while True:
        ivs=[isolated(o,s,x,bits) for x in commands]
        if all(x is not None for x in ivs):
            ps=[comp(power(iv,h.denominator,h.numerator,bits)) for iv in ivs]
            det=sub(mul(ps[0],ps[3]),mul(ps[1],ps[2]))
            if det[1]<0:STATS['half_integer_signs']+=1;return -1
            if det[0]>0:STATS['half_integer_signs']+=1;return 1
        bits+=2
def unary_sign(o,i,s,n,h):
    xs=[tuple(u if z==i else F(1,2) for z in range(o.d)) for u in [F(1,4),F(3,4)]]
    bits=4
    while True:
        zs=[isolated(o,s,x,bits) for x in xs];us=[isolated(o,1<<i,x,bits) for x in xs]
        if all(x is not None for x in zs+us):
            ps=[comp(power(z,1,n,bits)) for z in zs];rs=[comp(power(u,h.denominator,h.numerator,bits)) for u in us]
            det=sub(mul(rs[1],ps[0]),mul(rs[0],ps[1]))
            if det[1]<0:STATS['half_integer_signs']+=1;return -1
            if det[0]>0:STATS['half_integer_signs']+=1;return 1
        bits+=2
def positive_integer(sign):
    hi=1
    while sign(F(2*hi+1,2))<0:hi*=2
    lo=1
    while lo<hi:
        k=(lo+hi)//2
        if sign(F(2*k+1,2))>0:hi=k
        else:lo=k+1
    STATS['positive_count_searches']+=1
    return lo
def discover(o,max_rounds=None):
    # max_rounds belongs only to bounded noncoverage tests, not the theorem.
    full=(1<<o.d)-1;base=tuple(F(1,2) for i in range(o.d));known={};covered=0;bits=2
    if not full:return known
    while max_rounds is None or bits//2<=max_rounds:
        for s in range(1,full+1):
            if s.bit_count()<2 or s in known:continue
            iv=isolated(o,s,base,bits)
            if iv is not None and iv[1]<1:
                known[s]=positive_integer(lambda h:interaction_sign(o,s,h))
                covered|=s
                if covered==full:return known
        bits+=2
    return None # Harness observation, not a negative mathematical decision.
def gap_presence(o,known,s):
    base=tuple(F(1,2) for i in range(o.d));bounds={}
    for t,n in known.items():
        bits=2
        while True:
            iv=isolated(o,t,base,bits)
            if iv is not None:
                ell=1-root(iv[1],n,bits)[1]
                if ell>0:break
            bits+=2
        for i in range(o.d):
            if t>>i&1:bounds[i]=max(bounds.get(i,F(0)),ell)
    cut=1-prod(bounds[i] for i in range(o.d) if s>>i&1)/2;bits=2
    while True:
        iv=isolated(o,s,base,bits)
        if iv is not None:
            if iv[1]<cut:return True
            if iv[0]>cut:return False
        bits+=2
def reconstruct(o):
    known=discover(o)
    full=(1<<o.d)-1
    if not full:return {}
    present={s:gap_presence(o,known,s) for s in range(1,full+1)}
    answer={s:0 for s in present}
    for s,yes in present.items():
        if yes and s.bit_count()>=2:answer[s]=known[s] if s in known else positive_integer(lambda h:interaction_sign(o,s,h))
    for i in range(o.d):
        if present[1<<i]:
            s=next(s for s,n in answer.items() if n>0 and s.bit_count()>=2 and s>>i&1)
            answer[1<<i]=positive_integer(lambda h:unary_sign(o,i,s,answer[s],h))
    return {s:n for s,n in answer.items() if n}
fixtures=[(0,{}),(2,{3:1}),(2,{3:4,1:7,2:3}),(3,{3:2,6:1}),(3,{7:3,1:2}),(3,{3:2,5:1,6:3,7:1,1:2,2:4,4:1}),(4,{3:2,12:3}),(4,{15:4,3:1,1:2,8:3}),(4,{3:1,6:2,12:3,9:1})]
for d,counts in fixtures:
    for style in [0,1]:
        o=Oracle(d,counts,style)
        assert reconstruct(o)==counts
        STATS['complete_world_name_runs']+=1;STATS['raw_queries']+=o.calls;STATS['max_bits']=max(STATS['max_bits'],o.maxbits)
# Missing-cover runs never produce a cover certificate or infer absent interactions.
for d,counts in [(1,{1:1}),(2,{1:4}),(3,{3:2,1:3}),(3,{})]:
    for style in [0,1]:
        o=Oracle(d,counts,style)
        assert discover(o,max_rounds=12) is None
        STATS['bounded_partial_checks']+=1;STATS['raw_queries']+=o.calls;STATS['max_bits']=max(STATS['max_bits'],o.maxbits)
res={'status':'PASS','stats':STATS,'scope':'complete count recovery on promised interaction covers; bounded harness checks make no nontermination or absence inference'}
(OUT/'COVER_DISCOVERY_CONTROLS.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
