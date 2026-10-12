#!/usr/bin/env python3
"""Standalone exact controls for the separately marked review supplement."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json

BITS=list(product((0,1),repeat=3))
checks=0

def check(condition):
    global checks
    assert condition
    checks+=1

def correctness(p,t):
    return {c:({0:1-3*p+3*p*p-t,1:p-2*p*p+t,2:p*p-t,3:t}[sum(c)]) for c in BITS}

def joint(p,a,t0,t1):
    result={}
    for x,t in ((0,t0),(1,t1)):
        for c,mass in correctness(p,t).items():
            result[(x,)+tuple(x if b else 1-x for b in c)]=mass*(a if x else 1-a)
    return result

def marginal(law,indices):
    result={}
    for state,mass in law.items():
        key=tuple(state[i] for i in indices)
        result[key]=result.get(key,F(0))+mass
    return result

def posterior(law):
    return law[(1,1,1,1)]/(law[(1,1,1,1)]+law[(0,1,1,1)])

models=0
for p in (F(11,20),F(3,5),F(5,8),F(2,3),F(3,4),F(9,10)):
    L=p*(2*p-1);K=1-3*p+3*p*p
    grid=[L+F(i,4)*(K-L) for i in range(5)]
    for a in (F(1,5),F(1,2),F(2,3),F(4,5)):
        minimum=a*L/(a*L+(1-a)*(1-p)**2)
        check(posterior(joint(p,a,L,L))==minimum)
        for t0,t1 in product(grid,repeat=2):
            law=joint(p,a,t0,t1)
            check(sum(law.values())==1 and min(law.values())>=0)
            check(minimum<=posterior(law)<=1)
            check(posterior(law)==a*t1/(a*t1+(1-a)*(K-t0)))
            raw=marginal(law,(1,2,3))
            beta=a*t1-(1-a)*t0
            check(raw[(1,1,1)]==(1-a)*K+beta)
            for t in (t0,t1):
                c=correctness(p,t)
                for indices in combinations(range(3),2):
                    m=marginal(c,indices)
                    check(m=={(0,0):(1-p)**2,(0,1):p*(1-p),(1,0):p*(1-p),(1,1):p*p})
            if L<t0<K and L<t1<K:
                check(min(law.values())>0)
            if t0==K:
                check(posterior(law)==1)
            else:
                check(t1/(K-t0)>=L/(1-p)**2)
            models+=1

p=F(3,5);a=F(2,3)
first=joint(p,a,F(1,5),F(1,5))
second=joint(p,a,F(11,50),F(21,100))
check(min(first.values())>0 and min(second.values())>0)
for size in range(4):
    for indices in combinations(range(4),size):
        check(marginal(first,indices)==marginal(second,indices))
check(first!=second)
raw=marginal(first,(1,2,3))
expected={c:({3:F(4,25),0:F(3,25),2:F(2,15),1:F(8,75)}[sum(c)]) for c in BITS}
check(raw==expected)
check(posterior(first)==F(5,6))
check(posterior(second)==F(7,8))
results={'status':'PASS','exact_assertions':checks,'truth_asymmetric_grid_models':models,'unequal_prior_collision_posteriors':['5/6','7/8'],'every_proper_marginal_identical':True,'full_support':True,'scope':'Author-stage exact controls of the independent review supplement, not a separate independent review or closure.'}
text=json.dumps(results,indent=2)+'\n'
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(text)
print(text,end='')
