from fractions import Fraction as F
import json
from pathlib import Path

def require(c,name):
    if not c: raise RuntimeError(name)
    checks.append(name)
checks=[]
# Exact infinite geometric-series identities.
geom=lambda q:q/(1-q)
require(geom(F(1,2))==1,'observed marginal normalizes')
require(geom(F(1,2))==1,'original integrated second moment is one')
Z=geom(F(1,4))+geom(F(1,8))-geom(F(1,16))
require(Z==F(43,105),'global joint audit normalizer')
require(geom(F(1,2))/Z==F(105,43),'global audited second moment remains finite')
# Polynomial bound valid for 0<epsilon<=1/2:
# 5/4 - (1+epsilon-epsilon^2) = (epsilon-1/2)^2 >=0.
import sympy as s
e=s.symbols('e',real=True)
require(s.expand(s.Rational(5,4)-(1+e-e**2)-(e-s.Rational(1,2))**2)==0,'universal denominator upper bound identity')
for N in (1,2,10,100):
    partial=sum(1/(1+F(1,2**n)-F(1,2**(2*n))) for n in range(1,N+1))
    require(partial>=F(4*N,5),'conditional partial moment lower bound '+str(N))
result={'checks':len(checks),'passed':checks,'global_normalizer':str(Z),'global_second_moment':str(1/Z),'evidence':'Exact rational/symbolic controls; divergence is established by the accompanying uniform bound proof, not finite enumeration.'}
print(json.dumps(result,indent=2))
