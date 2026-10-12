#!/usr/bin/env python3
"""Derive the quartic variance jet directly from the weighted characteristic."""
import json
import sympy as s
x,t=s.symbols('x t', real=True)
v=s.symbols('v', positive=True)
d=1+2*t*x*x
q=t*x**4/(4*d)
w=s.exp(-q)
h=x*x/d

def E(p):
    return s.expand(sum(c*(0 if a[0]%2 else s.factorial2(a[0]-1)*v**(a[0]//2)) for a,c in s.Poly(s.expand(p),x).terms()))
checks=[]
def ck(name,expr):
    assert s.simplify(expr)==0, (name,expr)
    checks.append(name)

ck('integrated quartic killing derivative',s.diff(q,t)-x**4/(4*d*d))
ck('characteristic squared derivative',s.diff(h,t)+2*h*h)
W=[s.simplify(s.diff(w,t,j).subs(t,0)) for j in range(3)]
N=[s.simplify(s.diff(h*w,t,j).subs(t,0)) for j in range(3)]
ck('weight first derivative at zero',W[1]+x**4/4)
ck('weight second derivative at zero',W[2]-x**6-x**8/16)
ck('unnormalized second-moment first derivative',N[1]+2*x**4+x**6/4)
ck('unnormalized second-moment second derivative',N[2]-8*x**6-2*x**8-x**10/16)
z0,z1,z2=map(E,W)
n0,n1,n2=map(E,N)
first=s.expand(n1-n0*z1)
second=s.expand(n2-2*n1*z1-n0*z2+2*n0*z1*z1)
restricted=s.expand(s.diff(first,v)*first)
gap=s.factor(second-restricted)
ck('exact full first derivative',first+6*v*v+3*v**3)
ck('exact full second derivative',second-120*v**3-186*v**4-48*v**5)
ck('restricted Gaussian second derivative',restricted-72*v**3-90*v**4-27*v**5)
ck('positive factorization',gap-3*v**3*(v+4)*(7*v+4))
ck('unit-variance second derivative gap',gap.subs(v,1)-165)
assert gap.is_positive
checks.append('symbolic positivity for v>0')
print(json.dumps({'status':'PASS','count':len(checks),'checks':checks,'method':'Direct right-time derivatives of weighted-characteristic numerator and normalizer, independent of author moment-hierarchy differentiation. Analytic domination is in REVIEW.md.','first':str(first),'full_second':str(second),'restricted_second':str(restricted),'gap':str(gap)},indent=2))
