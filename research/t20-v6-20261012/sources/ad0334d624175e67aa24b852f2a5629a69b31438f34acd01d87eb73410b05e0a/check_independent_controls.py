#!/usr/bin/env python3
"""Exact algebraic controls; supplements, and does not prove, the theorem."""
import hashlib
import json
from pathlib import Path
import sympy as S

HERE = Path(__file__).resolve().parent
checks = []

def check(name, value):
    assert bool(value), name
    checks.append(name)
    print("PASS", name)

def zero(name, expression):
    check(name, S.simplify(expression) == 0)

accepted = HERE / "inputs/accepted-V-RESULT.md"
check("accepted V exact supplied digest", hashlib.sha256(accepted.read_bytes()).hexdigest()
      == "7ffed76cdfb23ee725bd4030c22dd03bb1f66934d885a6800caf260fdb0741bd")

s, t, u = S.symbols("s t u", positive=True)
x, y = S.symbols("x y", real=True)
g = (x + t*y)**2
K = S.integrate(g.subs(t, u), (u, 0, t))
Q = S.Matrix([[t, t**2/2], [t**2/2, t**3/3]])
c = t**3 / (4*(t**2+3))
zero("rank-one cumulative integral", K - (t*x**2+t**2*x*y+t**3*y**2/3))
zero("rank-one Gramian determinant", Q.det()-t**4/12)
zero("instantaneous null direction", g.subs(x, -t*y))
zero("Gramian completed square", K - (t*(x+t*y/2)**2+t**3*y**2/12))
zero("chosen cumulative rate is determinant over trace", c-Q.det()/S.trace(Q))
M = Q-c*S.eye(2)
zero("radial-slack determinant", M.det()-c**2)
zero("radial-slack first pivot", M[0,0]-3*t*(t**2+4)/(4*(t**2+3)))
check("radial-slack first pivot strictly positive", M[0,0].simplify().is_positive)
check("cumulative rate strictly positive", c.is_positive)
zero("explicit cumulative SOS slack", K-c*(x*x+y*y)
     -M[0,0]*(x+M[0,1]/M[0,0]*y)**2-c**2/M[0,0]*y*y)

# If rotation stops at time one, interior windows can lose all radial coercivity.
Kstop = K.subs(t, 1)+(t-1)*(x+y)**2
zero("stopped rotation cumulative integral", Kstop-(t*x*x+(2*t-1)*x*y+(t-S.Rational(2,3))*y*y))
zero("stopped rotation fixed lower certificate", Kstop-S.Rational(1,16)*(x*x+y*y)
     -(S.Rational(15,16)*(x+S.Rational(8,15)*y)**2
       +S.Rational(1,240)*y*y+(t-1)*(x+y)**2))
zero("post-stop window rank one", ((t-s)*(x+y)**2).subs(x, -y))
zero("stopped rate is continuous at the junction", g.subs(t,1)-(x+y)**2)
zero("stopped rate has an actual derivative jump", S.diff(g,t).subs(t,1)
     -S.diff((x+y)**2,t)-2*y*(x+y))

# Simplex symmetrization is verified without any measure or functional.
Kst = S.integrate(g.subs(t,u), (u,s,t))
J = S.Integer(1)
for k in range(1,5):
    J = S.integrate(S.expand(g.subs(t,u)*J.subs(t,u)), (u,s,t))
    zero(f"ordered terminal simplex factor k={k}", J-Kst**k/S.factorial(k))

# Exact backward residual order test, including a false-order discriminator.
latest = S.integrate(u*S.exp(-u), (u,0,1))
earliest = S.integrate((1-u)*S.exp(-u), (u,0,1))
zero("latest-time Volterra residual gives exact identity", 2/S.E+latest-1)
zero("earliest-time residual has nonzero exact defect", 2/S.E+earliest-1-(3/S.E-1))
check("earliest-time residual fails", S.simplify(2/S.E+earliest-1) != 0)

# A genuinely changing one-atom rate checks every finite residual by its endpoint
# derivative and zero initial value. The fundamental theorem then fixes it.
G = t+t*t+t**3/3
A = S.exp(-G)
Kscalar = G-G.subs(t,s)
for n in range(6):
    partial = sum(Kscalar**k/S.factorial(k) for k in range(n+1))
    deficit = A.subs(t,s)-A*partial
    zero(f"changing-rate residual derivative N={n}", S.diff(deficit,t)
         -A*(1+t)**2*Kscalar**n/S.factorial(n))
    zero(f"changing-rate residual zero at lower endpoint N={n}", deficit.subs(t,s))

# Radial SOS domination is a finite identity, not an inequality asserted by sampling.
z, w = S.symbols("z w", nonnegative=True)
for n in range(1,7):
    zero(f"radial binomial SOS difference n={n}", (z+w)**n-z**n
         -sum(S.binomial(n,j)*z**(n-j)*w**j for j in range(1,n+1)))

# Inherited Fourier estimate must be used fixed-frequency first. Its ratio tends
# to zero even after multiplication by a fixed-degree objective.
k = S.symbols("k", positive=True)
for degree in [0,2,5,8]:
    check(f"weighted Fourier ratio tends to zero D={degree}",
          S.limit(S.sqrt(k+degree+1)/(k+1), k,S.oo) == 0)

f = [x+y, x*y-1]
h = [x*x+y, x-y*y]
zero("SOS products require no common time factorization",
     sum(a*a for a in f)*sum(b*b for b in h)-sum((a*b)**2 for a in f for b in h))

# Inherited triangular transfer, rechecked under the cumulative example.
U, Z = S.symbols("U Z", real=True)
for degree in [2,3,5]:
    killing = (x+t*(y-t*x**degree))**2
    zero(f"triangular cumulative pullback m={degree}",
         killing.subs({x:U,y:Z+t*U**degree}, simultaneous=True)-(U+t*Z)**2)
    zero(f"original-coordinate zero graph m={degree}",
         killing.subs(y,t*x**degree-x/t))
    inverse_observable = x+(y-t*x**degree)**2
    zero(f"inverse transport chain identity m={degree}",
         S.diff(inverse_observable,t)+x**degree*S.diff(inverse_observable,y))

result = {"status":"PASS", "count":len(checks), "checks":checks,
          "scope":"Exact symbolic controls supplement the ordinary independent whole-proof review. No universal proof-kernel certification."}
(HERE/"INDEPENDENT_CONTROL_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
print(f"PASS: {len(checks)} independent exact controls")
