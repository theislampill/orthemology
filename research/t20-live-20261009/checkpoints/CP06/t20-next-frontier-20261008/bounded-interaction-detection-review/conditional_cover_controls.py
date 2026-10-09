#!/usr/bin/env python3
"""Independent conditional-cover controls: no target-count ceiling input."""
from fractions import Fraction as F
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent
STATS={'runs':0,'raw_queries':0,'max_bits':0,'uncovered_rejections':0}

def prod(xs):
    ans=F(1)
    for x in xs:ans*=x
    return ans

def subsets(s):
    x=s
    while True:
        yield x
        if x==0:break
        x=(x-1)&s

class Oracle:
    def __init__(self,d,counts,style):self.d=d;self.counts=counts;self.style=style;self.calls=0;self.maxbits=0
    def interval(self,x,bits):
        true=prod((1-prod(x[i]**(i+1) for i in range(self.d) if s>>i&1))**n for s,n in self.counts.items() if n)
        eps=F(1,2**bits)
        if self.style==0:q=true+eps
        elif self.style==1:q=true-eps
        elif self.style==2:q=F((true*2**bits).__floor__(),2**bits)
        else:q=true+eps if (bits+sum(z.numerator+z.denominator for z in x))%2 else true-eps
        self.calls+=1;self.maxbits=max(self.maxbits,bits)
        return max(F(0),q-eps),min(F(1),q+eps)

def isolate(oracle,s,base,bits):
    lo=hi=F(1)
    for t in subsets(s):
        x=tuple(base[i] if t>>i&1 else F(0) for i in range(oracle.d))
        a,b=oracle.interval(x,bits)
        if (s.bit_count()-t.bit_count())%2:
            if a<=0:return None
            lo/=b;hi/=a
        else:lo*=a;hi*=b
    return max(F(0),lo),min(F(1),hi)

def root_bracket(y,n,bits):
    a=F(0);b=F(1)
    for unused in range(bits):
        mid=(a+b)/2
        if mid**n<=y:a=mid
        else:b=mid
    return a,b

def conditional_presence(oracle,known_counts,target):
    # known_counts is separately supplied positive-support/count information.
    covered=0
    for s,n in known_counts.items():
        assert n>0;covered|=s
    if target==0 or target&covered!=target:raise ValueError('target not wholly covered')
    base=tuple(F(1,2) for i in range(oracle.d));bounds={}
    for s,n in known_counts.items():
        bits=2
        while True:
            iv=isolate(oracle,s,base,bits)
            if iv is not None:
                # P=1-Z^(1/n); upper root endpoint supplies lower P bound.
                ell=1-root_bracket(iv[1],n,bits)[1]
                if ell>0:break
            bits+=2
        for i in range(oracle.d):
            if s>>i&1:bounds[i]=max(bounds.get(i,F(0)),ell)
    gap=prod(bounds[i] for i in range(oracle.d) if target>>i&1)
    cut=1-gap/2;bits=2
    while True:
        iv=isolate(oracle,target,base,bits)
        if iv is not None:
            if iv[1]<cut:return True
            if iv[0]>cut:return False
        bits+=2

for target in [1,2,4,5,7]:
    for count in [0,1,5,37]:
        for style in range(4):
            counts={3:2,6:3,target:count}
            o=Oracle(3,counts,style)
            assert conditional_presence(o,{3:2,6:3},target)==bool(count)
            STATS['runs']+=1;STATS['raw_queries']+=o.calls;STATS['max_bits']=max(STATS['max_bits'],o.maxbits)
# The input family need not cover roots outside the target.
for target in [1,2]:
    for count in [0,1,17]:
        for style in range(4):
            o=Oracle(3,{3:1,target:count,4:7},style)
            assert conditional_presence(o,{3:1},target)==bool(count)
            STATS['runs']+=1;STATS['raw_queries']+=o.calls;STATS['max_bits']=max(STATS['max_bits'],o.maxbits)
# No unsupported decision for targets containing an uncovered coordinate.
for target in [4,5,6,7]:
    o=Oracle(3,{3:1,4:7},0)
    try:conditional_presence(o,{3:1},target)
    except ValueError:
        assert o.calls==0;STATS['uncovered_rejections']+=1
    else:raise AssertionError('uncovered target was accepted')
res={'status':'PASS','stats':STATS,'scope':'conditional positive-support cover only; no supplied or inferred target count bound'}
(OUT/'CONDITIONAL_COVER_CONTROLS.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
