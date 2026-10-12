#!/usr/bin/env python3
"""Bounded exact controls for RESULT.md; no general claim is proved by enumeration.

The stabilizer calculation uses marginal-indicator rows and ambient likelihood
coordinates, independently of the ANOVA highest-component proof.
"""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform
import sys

import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
Q = S.Rational
checks = []


def check(name, condition, detail=None):
    assert condition, name
    item = {"name": name, "passed": True}
    if detail is not None:
        item["detail"] = detail
    checks.append(item)
    print(f"PASS {len(checks):02d}: {name}", flush=True)


def zero(value):
    if isinstance(value, S.MatrixBase):
        return all(S.factor(v) == 0 for v in value)
    return S.factor(value) == 0


def indicator_rows(states, slots):
    slots = tuple(sorted(slots))
    assignments = sorted({tuple(x[i] for i in slots) for x in states})
    return S.Matrix([[int(tuple(x[i] for i in slots) == a) for x in states]
                     for a in assignments])


def marginal_basis(sizes, facets):
    states = list(product(*(range(q) for q in sizes)))
    rows = [[1] * len(states)]
    for face in facets:
        rows.extend(indicator_rows(states, face).tolist())
    candidates = S.Matrix(rows)
    pivots = candidates.T.rref()[1]
    return states, candidates[list(pivots), :]


def ambient_stabilizer_constraints(M):
    # For unknown L in R^X, every retained row v and h in ker M impose
    # <v L,h>=0. This avoids assuming L is already in the retained row space.
    rows = [[M[i, j] * h[j] for j in range(M.cols)]
            for h in M.nullspace() for i in range(M.rows)]
    return S.Matrix(rows) if rows else S.zeros(0, M.cols)


def downward(facets):
    return {frozenset(s) for t in facets for k in range(len(t) + 1)
            for s in combinations(t, k)}


def posterior(p, likelihood):
    raw = S.diag(*likelihood) * p
    return raw / sum(raw)


def fisher(p, fitness):
    return -(S.diag(*p) - p * p.T) * fitness


# This packet's exact direct inputs, without silently re-running changed
# predecessor transitive dependency gates or adopting their review status.
bindings = json.loads((HERE / "INPUT_BINDINGS.json").read_text())
for entry in bindings["local_inputs"]:
    data = (ROOT / entry["path"]).read_bytes()
    check("bound input " + entry["path"],
          len(data) == entry["bytes"]
          and hashlib.sha256(data).hexdigest() == entry["sha256"])


# Every family is small and selected for a distinct structural boundary.
cases = [
    ("binary star", (2, 2, 2, 2), [(0, 1), (0, 2), (0, 3)], 8, 2),
    ("four-slot edge chain", (2, 2, 2, 2), [(0, 1), (1, 2), (2, 3)], 8, 1),
    ("disjoint cliques", (2, 2, 2, 2), [(0, 1), (2, 3)], 7, 1),
    ("categorical star", (3, 2, 2), [(0, 1), (0, 2)], 9, 3),
    ("two-slot categorical core", (2, 3, 2, 2), [(0, 1, 2), (0, 1, 3)], 18, 6),
    ("omitted coordinate", (2, 3), [(0,)], 2, 2),
    ("mass only", (2, 3), [()], 1, 1),
    ("full marginal", (2, 3), [(0, 1)], 6, 6),
    ("proper order two", (2, 2, 2), [(0, 1), (0, 2), (1, 2)], 7, 1),
]
for name, sizes, facets, expected_r, expected_a in cases:
    states, M = marginal_basis(sizes, facets)
    C = set.intersection(*(set(t) for t in facets))
    core = indicator_rows(states, C)
    K = ambient_stabilizer_constraints(M)
    actual = S.Matrix.hstack(*K.nullspace())
    family = downward(facets)
    formula_r = sum(S.prod(sizes[i] - 1 for i in t) for t in family)
    check("stabilizer " + name,
          M.rows == expected_r == formula_r
          and actual.cols == expected_a == core.rows
          and zero(K * core.T)
          and actual.row_join(core.T).rank() == expected_a,
          {"alphabet_sizes": sizes, "facets": facets, "core": sorted(C),
           "states": len(states), "retained_dimension": M.rows,
           "constraint_rank": K.rank(), "stabilizer_dimension": actual.cols})


# Symbolic masses verify the whole clique-update formula for arbitrary priors,
# not just independent or conveniently chosen prior families.
for sizes, facets, ell in [
    ((2, 2, 2), [(0, 1), (0, 2)], [Q(1, 4), Q(3, 4)]),
    ((3, 2, 2), [(0, 1), (0, 2)], [Q(1, 5), Q(1, 2), Q(4, 5)]),
]:
    states, M = marginal_basis(sizes, facets)
    masses = S.Matrix(S.symbols(f"p0:{len(states)}", nonnegative=True))
    L = S.Matrix([ell[x[0]] for x in states])
    raw = S.diag(*L) * masses
    Crows = indicator_rows(states, (0,))
    check(f"arbitrary-prior core branch probability {sizes}",
          zero(sum(raw) - (S.Matrix(ell).T * Crows * masses)[0]))
    for face in facets:
        B = indicator_rows(states, face)
        assignments = sorted({tuple(x[i] for i in face) for x in states})
        reweight = S.diag(*[ell[a[0]] for a in assignments])
        check(f"arbitrary-prior clique numerator {sizes}, {face}",
              zero(B * raw - reweight * B * masses))


# A genuinely correlated three-bit star: both priors violate conditional
# independence of leaves given the center, yet core evidence closes exactly.
bits = list(product((-1, 1), repeat=3))
star = S.Matrix([[1] * 8] + [[fn(c, a, b) for c, a, b in bits]
    for fn in [lambda c,a,b:c, lambda c,a,b:a, lambda c,a,b:b,
               lambda c,a,b:c*a, lambda c,a,b:c*b]])
pp = S.Matrix([(1 + c*a/Q(4) + c*b/Q(3) + a*b/Q(5))/8 for c,a,b in bits])
pm = S.Matrix([(1 + c*a/Q(4) + c*b/Q(3) - a*b/Q(5))/8 for c,a,b in bits])
Lc = S.Matrix([(1+c/Q(2))/2 for c,a,b in bits])
La = S.Matrix([(1+a/Q(2))/2 for c,a,b in bits])
qp, qm = posterior(pp, Lc), posterior(pm, Lc)
check("correlated star priors share the complete retained record",
      all(v > 0 for v in pp) and all(v > 0 for v in pm)
      and star*pp == star*pm == S.Matrix([1, 0, 0, 0, Q(1,4), Q(1,3)]))
check("neither star prior assumes conditional independence",
      all(sum(p[k]*a*b for k,(c,a,b) in enumerate(bits) if c == center)
          * sum(p[k] for k,(c,a,b) in enumerate(bits) if c == center)
          != sum(p[k]*a for k,(c,a,b) in enumerate(bits) if c == center)
          * sum(p[k]*b for k,(c,a,b) in enumerate(bits) if c == center)
          for p in [pp,pm] for center in [-1,1]))
check("center evidence updates every retained star marginal exactly",
      (Lc.T*pp)[0] == (Lc.T*pm)[0] == Q(1,2)
      and star*qp == star*qm == S.Matrix([1,Q(1,2),Q(1,8),Q(1,6),Q(1,4),Q(1,3)])
      and qp != qm)
check("leaf evidence has equal probability but unequal retained posterior",
      (La.T*pp)[0] == (La.T*pm)[0] == Q(1,2)
      and (star*posterior(pp,La))[3] == Q(1,10)
      and (star*posterior(pm,La))[3] == -Q(1,10))
fc = S.Matrix([c for c,a,b in bits])
fa = S.Matrix([a for c,a,b in bits])
check("center objective has equal nonzero projected Fisher fields",
      star*fisher(pp,fc) == star*fisher(pm,fc)
      == S.Matrix([0,-1,-Q(1,4),-Q(1,3),0,0]))
check("leaf objective projected Fisher field distinguishes hidden dependence",
      (star*fisher(pp,fa))[3] == -Q(1,5)
      and (star*fisher(pm,fa))[3] == Q(1,5))


# Empty-core families: a local likelihood needs an omitted cross interaction.
for name, facets, i, j in [
    ("chain", [(0,1),(1,2),(2,3)], 1, 3),
    ("disjoint cliques", [(0,1),(2,3)], 0, 2),
]:
    states, M = marginal_basis((2,2,2,2), facets)
    signs = [tuple(2*v-1 for v in x) for x in states]
    p1 = S.Matrix([(1 + x[i]*x[j]/Q(2))/16 for x in signs])
    p2 = S.Matrix([(1 - x[i]*x[j]/Q(2))/16 for x in signs])
    L = S.Matrix([(1+x[i]/Q(2))/2 for x in signs])
    target = S.Matrix([[x[j] for x in signs]])
    check(name + " informative evidence fails retained posterior",
          M*p1 == M*p2 and (L.T*p1)[0] == (L.T*p2)[0] == Q(1,2)
          and (target*posterior(p1,L))[0] == Q(1,4)
          and (target*posterior(p2,L))[0] == -Q(1,4))


# A non-pure categorical component remains nonzero under disjoint tensoring.
# The coefficient matrix rank 2 prevents accidentally testing a pure tensor.
states = list(product(range(2), range(3), range(3), range(2)))
contrast = lambda value,label: S.Integer(value == label) - Q(1,3)
LS = S.Matrix([contrast(a,0)*contrast(b,0) + contrast(a,1)*contrast(b,1)
               for c,a,b,d in states])
hU = S.Matrix([(2*c-1)*(2*d-1) for c,a,b,d in states])
product_component = LS.multiply_elementwise(hU)
LS_matrix = S.Matrix([[contrast(a,0)*contrast(b,0)
                       + contrast(a,1)*contrast(b,1) for b in range(3)]
                     for a in range(3)])
check("non-pure categorical forbidden tensor component is nonzero",
      LS_matrix.rank() == 2 and not zero(product_component)
      and all(sum(product_component[k] for k,x in enumerate(states)
                  if all(x[j] == fixed[j] for j in range(4) if j != i)) == 0
              for i in range(4) for fixed in states))


# Normalized-only contracts: uncovered coordinates create cylinders, not atoms.
states, M = marginal_basis((2,3), [(0,)])
L = S.Matrix([Q(1,4), Q(1,2), Q(3,4), 0, 0, 0])
e0, e1 = S.eye(6)[:,0], S.eye(6)[:,1]
check("omitted-coordinate cylinder has constant posterior and unknown probability",
      M*e0 == M*e1 and M*posterior(e0,L) == M*posterior(e1,L)
      and (L.T*e0)[0] != (L.T*e1)[0]
      and not zero(ambient_stabilizer_constraints(M)*L))
check("whole-cylinder support preserves feasibility through covered marginal",
      all((L[j] > 0) == (states[j][0] == 0) for j in range(6)))
Lpartial = S.Matrix([Q(1,4), 0, Q(3,4), 0, 0, 0])
check("partial cylinder can lose feasibility at an identical record",
      M*e0 == M*e1 and (Lpartial.T*e0)[0] > 0 and (Lpartial.T*e1)[0] == 0)

# Singleton revelation survives posterior-only descent on a proper star, while
# opposite boundary parity priors have the same record and different feasibility.
Lsingle = S.Matrix([int(x == (1,1,1)) for x in bits])
peven = S.Matrix([Q(1+c*a*b,8) for c,a,b in bits])
podd = S.Matrix([Q(1-c*a*b,8) for c,a,b in bits])
check("proper-star singleton revelation does not carry feasibility",
      star*peven == star*podd and (Lsingle.T*peven)[0] == Q(1,4)
      and (Lsingle.T*podd)[0] == 0)


# The channel-adapted hierarchy is the span of products with all D-functions.
sizes, facets, D = (2,3,2), [(0,), (1,), (2,)], (0,)
states, M = marginal_basis(sizes, facets)
BD = indicator_rows(states, D)
products = S.Matrix([[M[i,x]*BD[j,x] for x in range(M.cols)]
                     for i in range(M.rows) for j in range(BD.rows)])
_, enlarged = marginal_basis(sizes, [tuple(sorted(set(t)|set(D))) for t in facets])
check("declared core-channel enlargement equals product-module span",
      products.rank() == enlarged.rows == 8
      and products.col_join(enlarged).rank() == 8)


results = {"status":"passed", "assertion_groups":len(checks),
           "python":sys.version, "sympy":S.__version__,
           "platform":platform.platform(),
           "scope":"Author exact finite controls, not independent review or universal enumeration.",
           "checks":checks}
(HERE / "CONTROL_RESULTS.json").write_text(json.dumps(results,indent=2)+"\n")
print(f"ALL {len(checks)} ASSERTION GROUPS PASSED")
