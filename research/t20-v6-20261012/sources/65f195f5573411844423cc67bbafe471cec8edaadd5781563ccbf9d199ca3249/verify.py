#!/usr/bin/env python3
"""Exact finite controls; ordinary proofs are in RESULT.md, not replaced by tests."""
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import platform
import sys

import sympy as S

HERE = Path(__file__).resolve().parent
Q = S.Rational
checks = []


def zero(a):
    if isinstance(a, S.MatrixBase):
        return all(S.factor(x) == 0 for x in a)
    return S.factor(a) == 0


def check(name, condition, detail=None):
    assert condition, name
    record = {"name": name, "passed": True}
    if detail is not None:
        record["detail"] = detail
    checks.append(record)
    print(f"PASS {len(checks):02d}: {name}", flush=True)


def stabilizer_constraints(M):
    """In row-basis coordinates f=M.T*a, impose M diag(f) ker(M)=0."""
    h_basis = M.nullspace()
    rows = []
    for h in h_basis:
        for i in range(M.rows):
            rows.append([
                sum(M[i, x] * M[j, x] * h[x] for x in range(M.cols))
                for j in range(M.rows)
            ])
    return S.Matrix(rows) if rows else S.zeros(0, M.rows)


def product_moments(sizes, k):
    states = list(product(*(range(q) for q in sizes)))
    rows = [[S.Integer(1)] * len(states)]
    for order in range(1, k + 1):
        for slots in combinations(range(len(sizes)), order):
            for labels in product(*(range(sizes[i] - 1) for i in slots)):
                rows.append([
                    S.prod(S.Integer(x[i] == a) - Q(1, sizes[i])
                           for i, a in zip(slots, labels))
                    for x in states
                ])
    return S.Matrix(rows)


def field(M, p, g):
    return -(S.diag(*p) - p * p.T) * M.T * g


def covariance(phi, p):
    z = phi * p
    return phi * S.diag(*p) * phi.T - z * z.T


# Complete proper product spaces, including nonbinary contrasts.
for sizes, k in [((2, 2), 1), ((2, 2, 2), 1), ((2, 2, 2), 2),
                 ((2, 2, 2, 2), 1), ((2, 2, 2, 2), 2),
                 ((2, 2, 2, 2), 3), ((2, 3), 1),
                 ((2, 2, 3), 1), ((2, 2, 3), 2), ((3, 3), 1)]:
    M = product_moments(sizes, k)
    K = stabilizer_constraints(M)
    expected = S.eye(M.rows)[:, 0]
    check(f"proper stabilizer {sizes}, k={k}",
          M.rank() == M.rows and K.rank() == M.rows - 1
          and K.nullspace() == [expected],
          {"states": M.cols, "retained_dimension": M.rows,
           "constraint_rank": K.rank(), "stabilizer_dimension": 1})

Mfull = product_moments((2, 3), 2)
check("full-order observables permit every fitness", Mfull.rank() == 6
      and stabilizer_constraints(Mfull).rows == 0)
Mpartition = S.Matrix([[1, 1, 1, 1], [0, 0, 1, 1]])
check("blockconstant observable space stabilizes itself",
      zero(stabilizer_constraints(Mpartition)))

# General finite V: a block with two hidden-bit correlation plus one atom.
states = list(product((-1, 1), repeat=2))
Mbit = S.Matrix([[1] * 4, [x for x, y in states], [y for x, y in states]])
phi = Mbit[1:, :]
Mmix = S.Matrix([[1, 1, 1, 1, 1], [1, 1, 1, 1, 0],
                 [x for x, y in states] + [0],
                 [y for x, y in states] + [0]])
Kmix = stabilizer_constraints(Mmix)
check("mixed-block stabilizer has exactly two block indicators",
      Kmix.rank() == 2 and Kmix.nullspace() == [S.eye(4)[:, 0], S.eye(4)[:, 1]])
w, u, v, c = S.symbols("w u v c", real=True)
pmix = S.Matrix([(w + u*x + v*y + c*x*y)/4 for x, y in states] + [1-w])
check("mixed-block mass objective closes", zero(Mmix * field(Mmix, pmix, S.Matrix([0, 1, 0, 0]))
      - S.Matrix([0, -w*(1-w), -u*(1-w), -v*(1-w)])))
pmix_plus = pmix.subs({w: Q(1, 2), u: 0, v: 0, c: Q(1, 4)})
pmix_minus = pmix.subs({w: Q(1, 2), u: 0, v: 0, c: -Q(1, 4)})
check("mixed-block within-block objective fails at same record",
      Mmix*pmix_plus == Mmix*pmix_minus
      and (Mmix*field(Mmix, pmix_plus, S.Matrix([0, 0, 1, 0])))[3] == -Q(1, 4)
      and (Mmix*field(Mmix, pmix_minus, S.Matrix([0, 0, 1, 0])))[3] == Q(1, 4))

# Generic symbolic two-bit fibre controls at arbitrary unary means.
m, n, c, d, a, b, g0 = S.symbols("m n c d a b g0", real=True)
pc = S.Matrix([(1 + m*x + n*y + c*x*y)/4 for x, y in states])
pd = pc.subs(c, d)
g = S.Matrix([g0, a, b])
check("arbitrary two-bit fibre has declared means", Mbit*pc == S.Matrix([1, m, n]))
expectedC = S.Matrix([[1-m*m, c-m*n], [c-m*n, 1-n*n]])
check("symbolic two-bit covariance", zero(covariance(phi, pc)-expectedC))
check("generic projected fibre difference identity",
      zero(Mbit*(field(Mbit, pc, g)-field(Mbit, pd, g))
           + Mbit*S.diag(*(Mbit.T*g))*(pc-pd)))
check("all-mean objective obstruction is exactly (a,b)=0",
      zero(phi*(field(Mbit, pc, g)-field(Mbit, pd, g))
           + (c-d)*S.Matrix([b, a])))
check("mass covector gauge cancels", zero(field(Mbit, pc, S.Matrix([g0, 0, 0]))))

# Exact correlated reference controls.
rho = S.symbols("rho", real=True)
rr = S.Matrix([(1+rho*x*y)/4 for x, y in states])
C0 = S.Matrix([[1, rho], [rho, 1]])
check("all reference correlations share zero unary means", phi*rr == S.zeros(2, 1))
check("reference cometric and inverse", zero(covariance(phi, rr)-C0)
      and zero(C0 * S.Matrix([[1, -rho], [-rho, 1]]) - (1-rho*rho)*S.eye(2)))
check("opposite correlation references yield opposite transverse velocities",
      phi*field(Mbit, rr.subs(rho, Q(1, 2)), S.Matrix([0, 1, 0])) == S.Matrix([-1, -Q(1, 2)])
      and phi*field(Mbit, rr.subs(rho, -Q(1, 2)), S.Matrix([0, 1, 0])) == S.Matrix([-1, Q(1, 2)]))


def odds(p):
    # State order is --,-+,+-,++.
    return S.factor(p[0]*p[3]/(p[1]*p[2]))


check("reference odds ratios distinguish the leaves",
      S.factor(odds(rr) - (1+rho)**2/(1-rho)**2) == 0
      and odds(rr.subs(rho, Q(1, 2))) == 9
      and odds(rr.subs(rho, -Q(1, 2))) == Q(1, 9))

# Positive indeterminates U,V encode exp(theta_1),exp(theta_2).
U, V = S.symbols("U V", positive=True)
raw = S.Matrix([rr[j]*U**x*V**y for j, (x, y) in enumerate(states)])
Z = sum(raw)
pt = raw/Z
zt = phi*pt
Dt = lambda h, q: q*S.diff(h, q)
scorejac = S.Matrix.hstack(pt.applyfunc(lambda h: Dt(h, U)), pt.applyfunc(lambda h: Dt(h, V)))
C = covariance(phi, pt)
check("finite exponential family normalizes", zero(sum(pt)-1))
check("exponential unary tilts preserve reference odds ratio", zero(odds(pt)-odds(rr)))
check("partition gradient equals the mean",
      zero(S.Matrix([Dt(Z, U)/Z, Dt(Z, V)/Z])-zt))
meanjac = S.Matrix.hstack(zt.applyfunc(lambda h: Dt(h, U)), zt.applyfunc(lambda h: Dt(h, V)))
check("partition Hessian and mean derivative equal covariance", zero(meanjac-C))
check("leaf tangent is full Fisher lift of statistic covectors",
      zero(scorejac-(S.diag(*pt)-pt*pt.T)*phi.T))
check("induced parameter Fisher metric equals covariance",
      zero(scorejac.T*S.diag(*[1/x for x in pt])*scorejac-C))
check("leaf tangents are Fisher-orthogonal to moment fibre",
      zero(scorejac.T*S.diag(*[1/x for x in pt])*Mbit.nullspace()[0]))
check("full fine and leaf Fisher objective gradients coincide",
      zero(field(Mbit, pt, S.Matrix([g0, a, b])) + scorejac*S.Matrix([a, b])))
check("exact mean dynamics use covariance cometric",
      zero(phi*field(Mbit, pt, S.Matrix([g0, a, b])) + C*S.Matrix([a, b])))

# Finite two-field reweighting with rational coefficients.
A, B = S.symbols("A B", real=True)
lr = S.Matrix([(1+A*x)*(1+B*y) for x, y in states])
newraw = S.diag(*lr)*rr
norm = sum(newraw)
newp = newraw/norm
newcross = sum(x*y*newp[j] for j, (x, y) in enumerate(states))
check("two-field rational tilt moments",
      zero(norm-(1+rho*A*B))
      and zero(phi*newp-S.Matrix([(A+rho*B)/(1+rho*A*B), (B+rho*A)/(1+rho*A*B)]))
      and zero(newcross-(rho+A*B)/(1+rho*A*B)))
q = newp.subs({rho: Q(1, 2), A: Q(1, 3), B: Q(1, 4)})
check("fixed log interaction permits changing raw cross moment",
      odds(q) == 9 and phi*q == S.Matrix([Q(11, 25), Q(2, 5)])
      and sum(x*y*q[j] for j, (x, y) in enumerate(states)) == Q(14, 25)
      and all(x > 0 for x in q))
qC = covariance(phi, q)
qu = S.Matrix([2, -3])
qlift = (S.diag(*q)-q*q.T)*phi.T*qC.inv()*qu
check("exact horizontal lift attains the quotient energy",
      Mbit*qlift == S.Matrix([0, 2, -3])
      and (qlift.T*S.diag(*[1/x for x in q])*qlift)[0] == (qu.T*qC.inv()*qu)[0]
      and zero(qlift.T*S.diag(*[1/x for x in q])*Mbit.nullspace()[0]))

# Local likelihood versus merely additive likelihood.
oneL = S.Matrix([1+Q(1, 2)*x for x, y in states])
onepost = S.diag(*oneL)*rr
onepost = onepost/sum(onepost)
check("single-coordinate positive likelihood preserves leaf", zero(odds(onepost)-odds(rr)))
badL = S.Matrix([1+Q(1, 4)*(x+y) for x, y in states])
badpost = badL/sum(badL)
check("L in unary V does not imply log L in unary V",
      Mbit.col_join(badL.T).rank() == Mbit.rank()
      and odds(badpost) == Q(3, 4)
      and all(0 < Q(2, 3)*x <= 1 for x in badL))

# Exact exponential-time orbit, using s=exp(-t)>0 and d/dt=-s d/ds.
s = S.symbols("s", positive=True)
orbitraw = S.Matrix([rr[j]*s**x for j, (x, y) in enumerate(states)])
orbitnorm = sum(orbitraw)
orbit = orbitraw/orbitnorm
orbitz = phi*orbit
check("linear-objective orbit solves the exact Fisher ODE",
      zero(orbit.applyfunc(lambda h: -s*S.diff(h, s))
           - field(Mbit, orbit, S.Matrix([0, 1, 0]))))
check("linear orbit means have the stated hyperbolic form",
      zero(orbitz - S.Matrix([(s*s-1)/(s*s+1), rho*(s*s-1)/(s*s+1)]))
      and zero(orbitnorm-(s+1/s)/2))

# Product leaf covariance and Legendre metric.
qprod = S.Matrix([(1+m*x)*(1+n*y)/4 for x, y in states])
Cp = S.diag(1-m*m, 1-n*n)
psi = sum((1+t)/2*S.log(1+t)+(1-t)/2*S.log(1-t) for t in (m, n))
check("uniform unary leaf is the product family", zero(covariance(phi, qprod)-Cp)
      and odds(qprod) == 1)
check("product Legendre-dual Hessian is inverse cometric",
      zero(S.hessian(psi, (m, n))*Cp-S.eye(2)))

# No general cone-partition identification: three collinear latent points.
Mmiddle = S.Matrix([[1, 1, 1], [0, Q(1, 2), 1]])
check("scalar stabilizer can coexist with a simplicial image cone",
      stabilizer_constraints(Mmiddle).rank() == 1
      and Mmiddle[:, 1] == (Mmiddle[:, 0]+Mmiddle[:, 2])/2,
      {"extreme_columns": [0, 2], "interior_column": 1,
       "stabilizer_dimension": 1})

report = {
    "scope": "Exact finite algebraic controls; not a formal-kernel or empirical certificate.",
    "python": platform.python_version(),
    "sympy": S.__version__,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "control_groups": len(checks),
    "all_passed": all(c["passed"] for c in checks),
    "checks": checks,
}
(HERE / "CONTROL_RESULTS.json").write_text(json.dumps(report, indent=2) + "\n")
print(f"All {len(checks)} exact control groups passed.")
