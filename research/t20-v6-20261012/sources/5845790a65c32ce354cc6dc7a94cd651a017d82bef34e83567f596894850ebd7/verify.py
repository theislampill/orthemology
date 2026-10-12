#!/usr/bin/env python3
"""Exact controls for the declared calibrated three-witness family."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json

BITS=list(product((0,1),repeat=3))
checks=0

def check(ok):
    global checks
    assert ok
    checks+=1

def law(p,t):
    masses={3:t,2:p*p-t,1:p-2*p*p+t,0:1-3*p+3*p*p-t}
    return {c:masses[sum(c)] for c in BITS}

def joint(p,t,a=F(1,2)):
    q=law(p,t)
    return {(x,)+tuple(x if z else 1-x for z in c):(a if x else 1-a)*v for x in (0,1) for c,v in q.items()}

def marginal(j,indices):
    out={}
    for state,mass in j.items():
        key=tuple(state[i] for i in indices)
        out[key]=out.get(key,F(0))+mass
    return out

def post(j):
    num=j[(1,1,1,1)]
    return num/(num+j[(0,1,1,1)])

def check_model(p,t):
    q=law(p,t)
    K=1-3*p+3*p*p
    check(sum(q.values())==1)
    check(min(q.values())>=0)
    for i in range(3):
        check(sum(v*c[i] for c,v in q.items())==p)
    for i,j in combinations(range(3),2):
        for u,v in product((0,1),repeat=2):
            check(sum(m for c,m in q.items() if c[i]==u and c[j]==v)==(p if u else 1-p)*(p if v else 1-p))
    jt=joint(p,t)
    check(sum(jt.values())==1)
    check(post(jt)==t/K)
    raw=marginal(jt,(1,2,3))
    for y,v in raw.items():
        check(v==(K/2 if len(set(y))==1 else p*(1-p)/2))
    tau=sum(v*product_sign(z) for z,v in jt.items())
    check(tau==8*t-12*p*p+6*p-1)
    return jt

def product_sign(z):
    ans=1
    for b in z: ans*=2*b-1
    return ans

p=F(3,5)
L=p*(2*p-1)
K=1-3*p+3*p*p
ts=[L,F(13,100),F(1,5),p**3,K]
js=[check_model(p,t) for t in ts]
for size in range(4):
    for idx in combinations(range(4),size):
        base=marginal(js[0],idx)
        for j in js[1:]:check(marginal(j,idx)==base)
check(post(js[0])==F(3,7))
check(post(js[1])==F(13,28))
check(post(js[2])==F(5,7))
check(post(js[3])==F(27,35))
check(post(js[4])==1)
check(min(js[1].values())>0 and min(js[2].values())>0 and min(js[3].values())>0)
check(post(js[1])<F(1,2)<post(js[2]))
# Tensor discrepancy is confined to the full interaction; proper marginals
# were checked directly, without relying on a Fourier sufficiency claim.
for idx in combinations(range(4),4):
    values=[sum(m*product_sign(tuple(s[i] for i in idx)) for s,m in j.items()) for j in js]
    check(len(set(values))==len(values))
# Exhaustive rational grid of admissible p and interpolation parameters.
grid_models=0
for denominator in range(3,26):
    for numerator in range(denominator//2+1,denominator):
        p1=F(numerator,denominator)
        L1=p1*(2*p1-1);K1=1-3*p1+3*p1*p1
        check(K1-L1==(1-p1)**2)
        check(L1>0 and L1<K1 and K1<p1*p1)
        bf=L1/(K1-L1)
        check((bf>=1)==(p1*p1+p1-1>=0))
        for k in range(9):
            t=L1+F(k,8)*(K1-L1)
            j=check_model(p1,t);grid_models+=1
            check(L1/K1<=post(j)<=1)
            if 0<k<8:check(min(j.values())>0)
# General-prior formula and a nonuniform-prior raw-identifiability control.
for a in (F(1,5),F(2,3),F(4,5)):
    for t in ts:
        j=joint(p,t,a)
        check(post(j)==a*t/(a*t+(1-a)*(K-t)))
        raw=marginal(j,(1,2,3))
        check(raw[(1,1,1)]==(1-a)*K+(2*a-1)*t)
        check((post(j)>=a)==(t>=K/2))
    check(marginal(joint(p,ts[1],a),(1,2,3))!=marginal(joint(p,ts[2],a),(1,2,3)))
results={"status":"PASS","exact_rational_assertions":checks,"grid_models":grid_models,"p_3_5_posterior_controls":[str(post(j)) for j in js],"all_proper_marginals_identical":True,"full_support_sign_reversal":True,"unequal_prior_scope_guard":True,"scope":"Finite exact controls supplement the ordinary general proof; no formal-kernel or empirical warrant claim."}
print(json.dumps(results,indent=2))
if __name__=='__main__':Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
