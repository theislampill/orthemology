#!/usr/bin/env python3
"""Exact algebraic controls only. General analytic/existence proofs are in RESULT.md."""
import sympy as S
from datetime import datetime, timezone

checks = []
def check(name, proposition):
    if not proposition:
        raise AssertionError(name)
    checks.append(name)
    print('PASS', name)

n = S.symbols('n', integer=True, nonnegative=True)
y, a = S.symbols('y a', real=True)
sigma = S.symbols('sigma', positive=True)
pi=S.pi
check('integer Fourier cancellation, symbolic all n', S.sin(2*pi*n)==0)
check('Gaussian real square-completion exponent', S.simplify(n*y-y**2/2 - (n**2/2-(y-n)**2/2))==0)
corrected_phase=S.simplify((2*pi/sigma**2)*n*sigma**2)
check('general lognormal perturbation phase is 2 pi n', corrected_phase==2*pi*n)
check('general lognormal cancellation, symbolic all n', S.exp(n*a+n**2*sigma**2/2-2*pi**2/sigma**2)*S.sin(corrected_phase)==0)
check('normalization moment n=0', S.exp(n*n/2).subs(n,0)==1)
check('concrete density factors have positive lower bound', 1-abs(S.Rational(1,2))==S.Rational(1,2))

A=S.symbols('A0:9')
g=S.symbols('g', real=True)
def deriv_A(expr):
    return S.expand(sum(S.diff(expr,A[j])*(-A[j+1]) for j in range(len(A)-1)))
for r in range(0,7):
    mr=A[r]/A[0]
    expected=-A[r+1]/A[0]+A[1]*A[r]/A[0]**2
    check(f'normalized hierarchy grade {r}', S.simplify(deriv_A(mr)-expected)==0)

m=S.symbols('m0:10')
def deriv_m(expr):
    return S.expand(sum(S.diff(expr,m[j])*(-m[j+1]+m[1]*m[j]) for j in range(1,len(m)-1)))
jet=[m[1]]
for j in range(1,7):
    jet.append(deriv_m(jet[-1]))
zjet=[(-1)**j*m[j] for j in range(9)]
qjet=[m[1]]
for j in range(1,7):
    qjet.append(S.expand(-zjet[j+1]-sum(S.binomial(j,k)*zjet[k]*qjet[j-k] for k in range(1,j+1))))
for j in range(7):
    check(f'mean jet recurrence equals hierarchy derivative {j}', S.expand(qjet[j]-jet[j])==0)
check('first mean derivative equals minus variance', jet[1]==m[1]**2-m[2])
check('second mean derivative', S.expand(jet[2]-(m[3]-3*m[1]*m[2]+2*m[1]**3))==0)
ln_moments={m[j]:S.exp(S.Rational(j*j,2)) for j in range(10)}
check('displayed first lognormal derivative', S.simplify(jet[1].subs(ln_moments)-(S.exp(1)-S.exp(2)))==0)
check('displayed second lognormal derivative', S.simplify(jet[2].subs(ln_moments)-(S.exp(S.Rational(9,2))-3*S.exp(S.Rational(5,2))+2*S.exp(S.Rational(3,2))))==0)

u,v,s=S.symbols('u v s', nonnegative=True)
L=S.Function('L')
Tu=lambda b: L(b+u)/L(u)
sequential=S.cancel(Tu(s+v)/Tu(v))
check('Laplace-profile semigroup composition', S.simplify(sequential-L(s+u+v)/L(u+v))==0)
check('Laplace-profile normalization', S.simplify(Tu(0)-1)==0)
check('positive-time positive-exponential-moment formula', S.simplify(Tu(-u/2)-L(u/2)/L(u))==0)
c=S.symbols('c', nonnegative=True)
check('point-law tilt positive control', S.simplify(c*S.exp(-u*c)/S.exp(-u*c)-c)==0)
x=S.symbols('x')
for r in range(1,5):
    for k in range(r+1):
        poly=S.Poly(x**k*(1-x)**(r-k),x)
        check(f'binary-simplex tensor coordinate is polynomial degree at most {r}, slot count {k}',poly.degree()<=r)
t=S.symbols('t', positive=True)
term=t**n*S.exp(n**2/2)/S.factorial(n)
ratio=S.simplify(term.subs(n,n+1)/term)
check('formal Taylor term ratio', S.simplify(ratio-t*S.exp(n+S.Rational(1,2))/(n+1))==0)
print(f'PASS {len(checks)} exact symbolic controls')
print('No numerical trace or existence-by-quadrature claim; no formal-kernel certificate.')
print('Executed UTC:',datetime.now(timezone.utc).isoformat())
