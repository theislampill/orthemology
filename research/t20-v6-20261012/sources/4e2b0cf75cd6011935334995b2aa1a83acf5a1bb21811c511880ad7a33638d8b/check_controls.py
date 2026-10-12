#!/usr/bin/env python3
"""Exact finite controls for the independently reviewed ordinary theorem.

These test polynomial identities and one exactly evaluated tilt. They do not
replace the infinite-dimensional domination and weak-evolution proof.
"""
from pathlib import Path
import hashlib
import json
import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED = "6943a1c274b177d107c8935e7d12d6a9e5094aa79df41546fb8e7d4d121914ce"
SOURCE = ROOT / "compact-initial-law-preservation-20261010/RESULT.md"

assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
x, y, v, z, t = S.symbols("x y v z t", real=True)
q0, q1, q2 = S.symbols("q0 q1 q2", real=True)
a0, a1, a2 = S.symbols("a0 a1 a2", positive=True)
P = x * (x - 1) * (x - 2)
U = (9*x - 5*x*x)/2
V = (5*x*x - 7*x)/2
e = [(x-1)*(x-2)/2, x*(2-x), x*(x-1)/2]
points = [(0,0,0), (1,2,-1), (2,-1,3)]
initial = [S.Rational(1,2), S.Rational(1,3), S.Rational(1,6)]

def zero(expr):
    assert S.cancel(S.expand(expr)) == 0, expr

def rem(expr):
    return S.rem(S.expand(expr), P, x)

for j, ej in enumerate(e):
    for k, point in enumerate(points):
        zero(ej.subs(x, point[0]) - int(j == k))
    zero(rem(ej*ej-ej))
    for k, ek in enumerate(e):
        zero(rem(ej*ek-int(j == k)*ej))
zero(sum(e)-1)
for point in points:
    zero(U.subs(x,point[0])-point[1])
    zero(V.subs(x,point[0])-point[2])
    zero(P.subs(x,point[0]))

# The entire finite algebra, not a sample of moment degrees: every polynomial
# factors through R[x]/(P) after y=U(x), v=V(x), and the e_j are its atoms.
q = q0*e[0] + q1*e[1] + q2*e[2]
zero(rem(q*q - q0*q0*e[0] - q1*q1*e[1] - q2*q2*e[2]))
for j, ej in enumerate(e):
    zero(rem(x*x*ej-j*j*ej))
zero(rem(x**3)-(3*x*x-2*x))
zero(rem(x**4)-(7*x*x-6*x))

# Autonomous h=x^2: use z=exp(-t). The normalized identity is exact for an
# arbitrary observable's three atom values, so covers every polynomial after
# passage through the finite evaluation algebra.
attenuation = [S.Integer(1), z, z**4]
mass = [initial[j]*attenuation[j] for j in range(3)]
normalizer = sum(mass)
values = [q0,q1,q2]
Lp = sum(mass[j]*values[j] for j in range(3))/normalizer
Lh = sum(mass[j]*j*j for j in range(3))/normalizer
Lhp = sum(mass[j]*j*j*values[j] for j in range(3))/normalizer
zero(-z*S.diff(Lp,z)+Lhp-Lh*Lp)

# Explicit positive quadratic-form decompositions; for 0<z<=1 the displayed
# coefficients establish both square positivity and square-order domination.
square = sum(mass[j]*values[j]**2 for j in range(3))
square_initial = sum(initial[j]*values[j]**2 for j in range(3))
zero(square-(3*q0*q0+2*z*q1*q1+z**4*q2*q2)/6)
zero(square_initial-square-(2*(1-z)*q1*q1+(1-z**4)*q2*q2)/6)

# Continuous time-varying h_t=(x+t)^2, still with two undamped coordinates.
# Apply the exact mass derivation da_j/dt=-(j+t)^2 a_j to the normalized
# observable. This also tests cancellation of the scalar shift t^2.
aa = [a0,a1,a2]
rates = [(j+t)**2 for j in range(3)]
total = sum(aa)
F = sum(aa[j]*values[j] for j in range(3))/total
Fprime = sum(S.diff(F,aa[j])*(-rates[j]*aa[j]) for j in range(3))
mean_rate = sum(aa[j]*rates[j] for j in range(3))/total
mean_product = sum(aa[j]*rates[j]*values[j] for j in range(3))/total
zero(Fprime+mean_product-mean_rate*F)
for j in range(3):
    zero(S.diff(j*j*t+j*t*t+t**3/3,t)-rates[j])

# At t=log(2), z=1/2 gives a completely rational, nontrivial exact endpoint.
endpoint_mass = [S.cancel(a.subs(z,S.Rational(1,2))) for a in mass]
endpoint_total = sum(endpoint_mass)
endpoint_weights = [S.cancel(a/endpoint_total) for a in endpoint_mass]
assert endpoint_mass == [S.Rational(1,2),S.Rational(1,6),S.Rational(1,96)]
assert endpoint_total == S.Rational(65,96)
assert endpoint_weights == [S.Rational(48,65),S.Rational(16,65),S.Rational(1,65)]
means = [sum(endpoint_weights[j]*points[j][i] for j in range(3)) for i in range(3)]
assert means == [S.Rational(18,65),S.Rational(31,65),S.Rational(-13,65)]

# The inherited linear-energy contrast is a global obstruction to SOS shifting.
# x+c takes a negative value at x=-c-1 for every scalar c.
c = S.symbols("c", real=True)
zero((x+c).subs(x,-c-1)+1)

result = {
    "status": "passed",
    "reviewed_result_sha256": EXPECTED,
    "controls": [
        "finite evaluation algebra and complete idempotent multiplication identities",
        "square positivity and square-order domination decompositions",
        "normalized autonomous hierarchy for arbitrary atom observable values",
        "continuous time-varying SOS hierarchy and exact integrated energy",
        "rational endpoint at t=log(2) with two undamped coordinates",
        "nonconstant linear energies cannot be made globally SOS by scalar shifts",
    ],
    "endpoint": {
        "initial_weights": list(map(str,initial)),
        "unnormalized_weights": list(map(str,endpoint_mass)),
        "normalizer": str(endpoint_total),
        "normalized_weights": list(map(str,endpoint_weights)),
        "coordinate_means": list(map(str,means)),
    },
    "limits": "Exact finite controls supplement, rather than prove, the all-time/all-degree ordinary theorem. No Lean, field-priority, or integration claim.",
}
(HERE / "CONTROL_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
