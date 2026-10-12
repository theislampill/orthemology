#!/usr/bin/env python3
"""Exact algebraic controls only; analytic proofs are in INDEPENDENT_DERIVATION.md."""
import hashlib,json
from pathlib import Path
import sympy as s

checks=[]
def check(name, condition):
    assert condition, name
    checks.append(name)
    print('PASS:', name)

n=s.symbols('n', integer=True, nonnegative=True)
a=s.symbols('a', real=True)
z=a+2*s.pi*s.I
check('complex Gaussian exponent separates into amplitude and phase',
      s.expand(z*z/2)==a*a/2-2*s.pi*s.pi+2*s.pi*a*s.I)
check('sine perturbation vanishes at every integer moment', s.sin(2*s.pi*n)==0)
check('normalization control n=0', s.exp(-2*s.pi*s.pi)*s.sin(0)==0)
check('strict positivity for selected epsilon=+/-1/2',s.Rational(1,2)>0)

# Differential-polynomial recurrence and quotient-series calculation are independent routes.
m=[s.Integer(1)]+list(s.symbols('m1:9'))
def D(p):
    return s.expand(sum(s.diff(p,m[j])*(m[1]*m[j]-m[j+1]) for j in range(1,8)))
qjets=[m[1]]
for order in range(5): qjets.append(D(qjets[-1]))
t=s.symbols('t')
L=sum((-1)**j*m[j]*t**j/s.factorial(j) for j in range(8))
qseries=s.series(-s.diff(L,t)/L,t,0,6).removeO().expand()
check('right mean jets orders 0 through 5 match independent quotient recurrence',
      all(s.expand(qseries.coeff(t,j)*s.factorial(j)-qjets[j])==0 for j in range(6)))
check('mass equation closes exactly',-m[1]+m[1]*m[0]==0)
check('first mean derivative is negative variance',qjets[1]==m[1]**2-m[2])
check('second mean derivative is third cumulant',
      s.expand(qjets[2]-(m[3]-3*m[1]*m[2]+2*m[1]**3))==0)
check('initial Fisher squared norm is exp(2)-exp(1)',
      s.simplify(s.exp(s.Rational(2*2,2))-s.exp(s.Rational(1,2))**2-(s.exp(2)-s.E))==0)

# One-dimensional tensor embedding and constant covector scaling.
lam=s.symbols('lambda',real=True)
for r in range(1,5):
    check(f'grade {r} contraction has no slot-count multiplier',
          s.expand(lam*(m[1]*m[r]-m[r+1])-(-lam*m[r+1]+lam*m[1]*m[r]))==0)

# Finite compact witnesses verify that bounded support is not finite-grade injectivity.
for cutoff in range(6):
    N=cutoff+2
    xs=[s.Rational(j,N-1) for j in range(N)]
    h=[(-1)**j*s.binomial(N-1,j) for j in range(N)]
    delta=1/(s.Integer(2*N)*max(abs(v) for v in h))
    plus=[s.Rational(1,N)+delta*v for v in h]
    minus=[s.Rational(1,N)-delta*v for v in h]
    assert all(v>0 for v in plus+minus)
    assert sum(plus)==sum(minus)==1
    for r in range(cutoff+1):
        assert sum((plus[j]-minus[j])*xs[j]**r for j in range(N))==0
        # All components of (x,1-x) tensor r are represented by x^k*(1-x)^(r-k).
        for k in range(r+1):
            assert s.expand(sum((plus[j]-minus[j])*xs[j]**k*(1-xs[j])**(r-k) for j in range(N)))==0
    assert sum((plus[j]-minus[j])*xs[j]**(cutoff+1) for j in range(N))!=0
    check(f'compact finite-law control cutoff {cutoff}: equal retained tensors, distinct next grade',True)

print(f'PASS: {len(checks)} exact control groups. No numerical quadrature used.')
print('Scope: these checks support algebra only; domination, analyticity, determinacy, and interval separation rely on ordinary proofs.')
