#!/usr/bin/env python3
"""Exact finite controls; not a formal proof of the universal theorem."""
import sympy as s
x,y,t=s.symbols('x y t', real=True)
pts=[{x:0,y:0},{x:1,y:0},{x:0,y:1}]
ell=x+2*y
lam=[ell.subs(pt) for pt in pts]
checks=0
def check(z):
    global checks
    assert s.simplify(z)==0, z
    checks+=1
for j in range(3):
    b=s.prod((ell-lam[k])/(lam[j]-lam[k]) for k in range(3) if k!=j)
    for coordinate in (x,y):
        p=(coordinate-pts[j][coordinate])*b**2
        for k,pt in enumerate(pts):
            check(p.subs(pt))
            for c in (x,y):
                check(s.diff(p,c).subs(pt)-int(j==k and c==coordinate))
w=s.symbols('w0:3', positive=True)
V=s.Matrix([[lam[j]**k for j in range(3)] for k in range(3)])
B=V*s.diag(*w)*V.T
check(B.det()-s.prod(w)*s.prod((lam[j]-lam[i])**2 for i in range(3) for j in range(i+1,3)))
for a,b in zip(V.inv()*V*s.Matrix(w),w): check(a-b)
for coordinate in (x,y):
    mixed=V*s.Matrix([w[j]*pts[j][coordinate] for j in range(3)])
    recovered=V.inv()*mixed
    for j in range(3): check(recovered[j]/w[j]-pts[j][coordinate])
# Genuine changing direction, signed linear h=x-2ty, U=(t,-t²).
raw=[s.Rational(1,6),s.Rational(1,3)*s.exp(-t),s.Rational(1,2)*s.exp(t*t)]
Z=sum(raw); wt=[a/Z for a in raw]
def L(p): return sum(wt[j]*p.subs(pts[j]) for j in range(3))
h=x-2*t*y
for total in range(5):
    for a in range(total+1):
        p=x**a*y**(total-a)
        check(s.diff(L(p),t)+L(h*p)-L(h)*L(p))
check(sum(wt)-1)
for q in [x+y,1+x-y,x*x+y*y-1]:
    check(L(q*q)-sum(wt[j]*q.subs(pts[j])**2 for j in range(3)))
# Signed polynomial energy; no SOS or autonomy premise.
h2=(1+t)*x*x-(1+t*t)*y*y+t*x*y
raw2=[s.Rational(1,6),s.Rational(1,3)*s.exp(-t-t*t/2),s.Rational(1,2)*s.exp(t+t**3/3)]
Z2=sum(raw2); wt2=[a/Z2 for a in raw2]
def L2(p): return sum(wt2[j]*p.subs(pts[j]) for j in range(3))
for total in range(5):
    for a in range(total+1):
        p=x**a*y**(total-a)
        check(s.diff(L2(p),t)+L2(h2*p)-L2(h2)*L2(p))
# Finite boundary factors are strictly positive: no disappearing weight.
e=s.symbols('e0:3', positive=True)
new=[w[j]*e[j]/sum(w[k]*e[k] for k in range(3)) for j in range(3)]
assert all(z.is_positive is True for z in new)
checks+=3
check(sum(new)-1)
print(f'PASS: {checks} exact identity/positivity controls.')
print('Continuous test: g(t)=(1,-2t), U(t)=(t,-t²), three fixed atoms.')
print('No enumeration claim for the general theorem; no floating-point checks.')
