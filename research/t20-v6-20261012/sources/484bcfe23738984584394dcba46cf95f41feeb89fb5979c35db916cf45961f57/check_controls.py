#!/usr/bin/env python3
"""Finite exact controls; not a universal singleton-extraction implementation."""
from fractions import Fraction as F
from math import comb, factorial
from itertools import product
from pathlib import Path
import hashlib, json

checks = 0
def check(value):
    global checks
    assert value
    checks += 1

def moment(law,r): return sum((p*x**r for x,p in law), F(0))
def clip(y,R): return F(R) if y == 1 else min(y/(1-y),F(R))
def w1(a,b):
    atoms=sorted(set(x for x,p in a+b)); result=F(0)
    for l,h in zip(atoms,atoms[1:]):
        ca=sum(p for x,p in a if x<=l); cb=sum(p for x,p in b if x<=l)
        result += abs(ca-cb)*(h-l)
    return result

laws=[]
for xs in [(0,1,3),(0,2,11),(1,4,17)]:
    for a in range(1,5):
        for b in range(1,5):
            laws.append([(F(xs[0]),F(a,10)),(F(xs[1]),F(b,10)),(F(xs[2]),F(10-a-b,10))])
for law in laws:
    for r in range(1,7):
        for R in range(1,9):
            actual=moment(law,r)
            truncated=sum(p*min(x,R)**r for x,p in law)
            check(0<=actual-truncated<=moment(law,r+1)/R)
            check(actual-moment(law,r+1)/R<=truncated<=actual)
    for R in range(1,9):
        check(sum(p for x,p in law if x>R)<=moment(law,1)/R)
        # Exact clipping transport cost for bounded ground metric.
        check(sum(p*min(F(1),abs(x-min(x,R))) for x,p in law)<=moment(law,1)/R)

# Global clipping and powered-clipping Lipschitz controls, including y=1.
ys=[F(j,20) for j in range(21)]
for R in (1,2,5,10):
    for a,b in product(ys, repeat=2):
        check(abs(clip(a,R)-clip(b,R))<=(1+R)**2*abs(a-b))
        for r in (1,2,3):
            check(abs(clip(a,R)**r-clip(b,R)**r)<=r*R**(r-1)*(1+R)**2*abs(a-b))

# Net rounding: rational grid measures with non-grid rational weights.
for n in range(1,8):
    for Q in range(1,12):
        raw=[F(j+1,sum(range(1,n+2))) for j in range(n+1)]
        rounded=[F((p*Q).numerator//(p*Q).denominator,Q) for p in raw[:-1]]
        rounded.append(1-sum(rounded))
        aa=[(F(j,n),p) for j,p in enumerate(raw)]
        bb=[(F(j,n),p) for j,p in enumerate(rounded)]
        check(all(p>=0 for p in rounded) and sum(rounded)==1)
        check(w1(aa,bb)<=F(n,Q))

# Distinct determinate finite-support laws with arbitrary finite equal prefix.
for d in range(0,14):
    n=d+1
    even=[(F(j),F(comb(n,j),2**d)) for j in range(n+1) if j%2==0]
    odd=[(F(j),F(comb(n,j),2**d)) for j in range(n+1) if j%2]
    check(moment(even,0)==moment(odd,0)==1)
    for r in range(d+1): check(moment(even,r)==moment(odd,r))
    def tilted_mean(law):
        return sum(p*x*F(1,2)**int(x) for x,p in law)/sum(p*F(1,2)**int(x) for x,p in law)
    check(tilted_mean(even)<tilted_mean(odd))

# Moment/cumulant Bell inversion from calibrated variance-jet entries.
for law in laws:
    mm=[moment(law,r) for r in range(10)]
    kap=[F(0)]*10
    for n in range(1,10):
        kap[n]=mm[n]-sum(F(comb(n-1,j))*kap[j+1]*mm[n-1-j] for j in range(n-1))
    jet=[(-1)**(k+2)*kap[k+2] for k in range(8)]
    reconstructed_k=[F(0),mm[1]]+[(-1)**n*jet[n-2] for n in range(2,10)]
    recovered=[F(1)]
    for n in range(9):
        recovered.append(sum(F(comb(n,j))*reconstructed_k[j+1]*recovered[n-j] for j in range(n+1)))
        check(recovered[-1]==mm[n+1])
    check(jet[0]==mm[2]-mm[1]**2)

# Rational quotient error budget, including zero numerators.
for D in (F(1,8),F(1,3),F(1)):
    eta=D/8
    for z in (D,2*D,3*D):
        for a in (F(0),F(1,3),F(3)):
            K=max(a,F(1))
            for ea,ez in product((-eta,F(0),eta),repeat=2):
                check(abs((a+ea)/(z+ez)-a/z)<=2*eta/D+2*K*eta/D**2)

# Strict-extension moment formula ratios and cosh generating-function coefficients.
for n in range(30):
    check(F(factorial(2*n+3),factorial(n+1))/F(factorial(2*n+1),factorial(n))==F((2*n+3)*(2*n+2),n+1))
    check(F(factorial(2*n+1),factorial(2*n))==2*n+1)

root=Path(__file__).parent
ledger=json.loads((root/'SOURCE_LEDGER.json').read_text())
for item in ledger['local_inputs']:
    check(hashlib.sha256((root/item['copy']).read_bytes()).hexdigest()==item['sha256'])
print(json.dumps({'status':'PASS','exact_checks':checks,'scope':'Finite rational controls and input hashes; no universal extraction implementation or kernel proof.'},indent=2))
