#!/usr/bin/env python3
"""Exact finite controls; not a universal proof or measure reconstruction."""
import hashlib
import json
import math
from fractions import Fraction as Q
from pathlib import Path
import sympy as S

ROOT = Path(__file__).resolve().parent
count = 0

def check(statement):
    global count
    assert statement
    count += 1

# Frozen source-copy bindings.
for item in json.loads((ROOT / 'INPUT_BINDINGS.json').read_text()):
    check(hashlib.sha256((ROOT / item['copy']).read_bytes()).hexdigest() == item['sha256'])
    check(hashlib.sha256((ROOT.parent / item['source']).read_bytes()).hexdigest() == item['sha256'])

# Finite atomic exact hierarchy in z=exp(-t).
z = S.symbols('z', positive=True)
support = (0, 1, 3)
weights = (S.Rational(1, 2), S.Rational(1, 3), S.Rational(1, 6))
A = [sum(w * S.Integer(x)**r * z**x for w, x in zip(weights, support)) for r in range(10)]
M = [S.cancel(a/A[0]) for a in A]
for r in range(9):
    check(S.simplify(-z*S.diff(A[r], z) + A[r+1]) == 0)
    check(S.simplify(-z*S.diff(M[r], z) + M[r+1] - M[1]*M[r]) == 0)
check(S.simplify(z*S.diff(S.log(A[0]), z) - M[1]) == 0)

# Rational finite law semigroup and inverse recovery; z stands for exp(-t).
def tilt(w, xs, z):
    raw = [p*z**x for p,x in zip(w,xs)]
    total = sum(raw)
    return tuple(p/total for p in raw)

for xs, w in [((0,1,3),(Q(1,2),Q(1,3),Q(1,6))),
              ((1,2,4),(Q(2,7),Q(3,7),Q(2,7))),
              ((0,),(Q(1),))]:
    for u in (Q(1,2),Q(2,3),Q(3,4),Q(1)):
        recovered = tilt(tilt(w,xs,u),xs,1/u)
        check(recovered == w)
        for v in (Q(1,2),Q(2,5),Q(1)):
            check(tilt(tilt(w,xs,u),xs,v) == tilt(w,xs,u*v))
            for r in range(8):
                final=tilt(w,xs,u*v)
                check(sum(p*x**r for p,x in zip(final,xs)) >= 0)

# Exponential(1) law: a_r(t)=r!/(1+t)^(r+1), all rational controls.
def ar(r,t): return Q(math.factorial(r),1)/(1+t)**(r+1)
for t in (Q(1,4),Q(1,2),Q(1),Q(2),Q(5)):
    for n in range(12):
        check(ar(n,t) <= Q(math.factorial(n),1)/t**n)
    for h in (t/4,t/2,3*t/4):
        for r in range(6):
            for N in range(12):
                partial = sum(h**k*ar(r+k,t)/math.factorial(k) for k in range(N+1))
                check(partial <= ar(r,t-h))

# Countercontrol A: valid delta_0 initial data but negative second moment.
t,e = S.symbols('t e', positive=True)
f = S.exp(-1/t)
a0 = 1-e*f
ar_flat = [(-1)**r*S.diff(a0,t,r) for r in range(7)]
mflat=[a/a0 for a in ar_flat]
for r in range(6):
    check(S.simplify(S.diff(mflat[r],t)+mflat[r+1]-mflat[1]*mflat[r]) == 0)
check(S.simplify(ar_flat[1]/(e*f)-1/t**2) == 0)
check(S.simplify(ar_flat[2]/(e*f)-(2*t-1)/t**4) == 0)
for u in (Q(1,10),Q(1,4),Q(2,5)):
    check((2*u-1)/u**4 < 0)
# The ordinary proof supplies all-order flatness, not finite limit testing.

# Countercontrol B: nonnegative sequence but negative variance.
H=S.symbols('H', positive=True)
linear=[S.Integer(1),1/(H-t)]+[S.Integer(0)]*5
for r in range(6):
    check(S.simplify(S.diff(linear[r],t)+linear[r+1]-linear[1]*linear[r]) == 0)
check(S.simplify(linear[2]-linear[1]**2+1/(H-t)**2)==0)

print(f'PASS: {count} exact controls, including source bindings.')
print('Universal claims are established by the ordinary proof in RESULT.md, not by these finite checks.')
