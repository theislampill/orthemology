#!/usr/bin/env python3
"""Independent exact controls for a bounded mathematical proof review.

These calculations corroborate finite examples; they do not prove universal
cone claims or certify a physical model. No author file is written.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
results = []


def record(name, detail):
    results.append({"name": name, "passed": True, "detail": detail})


def rank(matrix):
    """Exact forward elimination, separate from the author's RREF routine."""
    a = [list(map(Q, row)) for row in matrix]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        for i in range(row + 1, len(a)):
            multiple = a[i][col] / a[row][col]
            for j in range(col, len(a[0])):
                a[i][j] -= multiple * a[row][j]
        row += 1
        if row == len(a):
            break
    return row


def ray_equations(rays):
    d = len(rays[0])
    equations = []
    for k, ray in enumerate(rays):
        for i in range(d):
            eq = [Q(0)] * (d*d + len(rays))
            for j, value in enumerate(ray):
                eq[d*i+j] = value
            eq[d*d+k] = -ray[i]
            equations.append(eq)
    return equations


def matvec(matrix, vector):
    return tuple(sum((Q(a)*b for a, b in zip(row, vector)), Q(0)) for row in matrix)


def likelihood_update(state, likelihood):
    raw = tuple(x*l for x, l in zip(state, likelihood))
    mass = sum(raw)
    return mass, None if not mass else tuple(x/mass for x in raw)


# Six-projector eigenvector constraints, reconstructed in trace/Bloch coordinates.
rays = [(Q(1),) + tuple(Q(sign if i == k else 0) for i in range(3))
        for k in range(3) for sign in (-1, 1)]
equations = ray_equations(rays)
identity = tuple(Q(int(i == j)) for i in range(4) for j in range(4)) + (Q(1),)*6
assert all(sum(a*b for a, b in zip(row, identity)) == 0 for row in equations)
assert rank(equations) == 21 and len(identity) == 22
record("six-projector rigidity", "Independent 24 by 22 system has rank 21; scalar identity spans its nullspace.")


# A nonsimplicial indecomposable square cone, plus one independent ray.
square_plus_ray = [(Q(1), Q(a), Q(b), Q(0)) for a, b in [(1,1),(1,-1),(-1,1),(-1,-1)]]
square_plus_ray.append((Q(0), Q(0), Q(0), Q(1)))
eq = ray_equations(square_plus_ray)
assert len(eq[0]) == 21 and rank(eq) == 19
p_square = tuple(Q(int(i == j and i < 3)) for i in range(4) for j in range(4)) + (Q(1),)*4 + (Q(0),)
p_ray = tuple(Q(int(i == j == 3)) for i in range(4) for j in range(4)) + (Q(0),)*4 + (Q(1),)
assert all(sum(a*b for a, b in zip(row, v)) == 0 for row in eq for v in [p_square, p_ray])
record("signed graph with two components", "Square-cone-plus-ray constraints have nullity two, exactly the independent component scalars.")


# Feasible-cone projections and prior-dependent local realization, including endpoints.
first_rows = []
for t in [Q(0), Q(1,8), Q(1,4), Q(3,8), Q(1,2)]:
    p = (Q(1,2), t, Q(1,2)-t)
    likelihood = (2*t, Q(1), Q(0))
    raw = (t, t, Q(0))
    mass, posterior = likelihood_update(p, likelihood)
    assert mass == 2*t
    assert tuple(p[i]*likelihood[i] for i in range(3)) == raw
    assert posterior == ((Q(1,2),Q(1,2),Q(0)) if t else None)
    complement = tuple(1-z for z in likelihood)
    mass2, posterior2 = likelihood_update(p, complement)
    assert mass + mass2 == 1
    assert tuple(p[i]*complement[i] for i in range(3)) == (Q(1,2)-t,Q(0),Q(1,2)-t)
    assert posterior2 == ((Q(1,2),Q(0),Q(1,2)) if t != Q(1,2) else None)
    first_rows.append(likelihood[0])
assert len(set(first_rows)) == 5
coefficients = [[1,0,0],[0,1,0],[1,0,0],[0,0,1]]
augmented = [a+[b] for a, b in zip(coefficients,[1,1,0,0])]
assert rank(coefficients) == 3 and rank(augmented) == 4
record("local realization and no uniform passive lift", "Endpoints have correctly undefined zero branches; local likelihoods vary with t, while the uniform lift equations are inconsistent.")


# Fixed instrument with two pairs of identical columns; arbitrary within-group shapes.
vertices = [(Q(1),Q(0),Q(0),Q(0)), (Q(1,2),Q(1,2),Q(0),Q(0)),
            (Q(0),Q(0),Q(1),Q(0)), (Q(0),Q(0),Q(1,4),Q(3,4))]
likelihood = (Q(3,4),Q(3,4),Q(1,4),Q(1,4))


def in_family(p):
    return all(x >= 0 for x in p) and sum(p) == 1 and p[0] >= p[1] and 3*p[2] >= p[3]


for i in range(5):
    for j in range(5-i):
        for k in range(5-i-j):
            weights = tuple(Q(n,4) for n in (i,j,k,4-i-j-k))
            p = tuple(sum(weights[a]*vertices[a][b] for a in range(4)) for b in range(4))
            assert in_family(p)
            _, post = likelihood_update(p, likelihood)
            assert in_family(post)
            _, inverse = likelihood_update(post, tuple(1/x for x in likelihood))
            assert inverse == p
            for group in ((0,1),(2,3)):
                m = sum(p[i] for i in group)
                if m:
                    q = tuple(p[i]/m if i in group else Q(0) for i in range(4))
                    assert in_family(q)
                    assert likelihood_update(q,likelihood)[1] == q
# A singleton mixed over unequal columns is a closed convex but unstable family.
p = (Q(1,2),Q(0),Q(1,2),Q(0))
assert likelihood_update(p,likelihood)[1] != p
record("fixed-channel grouped stability and inverse", "35 rational mixtures retain arbitrary within-group constraints, reciprocal updating restores each state, and a cross-group extreme singleton fails stability.")


# Compression works only when the declared maps descend.
f = [[1,1,0],[0,0,1]]
e1, e2 = (Q(1),Q(0),Q(0)), (Q(0),Q(1),Q(0))
assert matvec(f,e1) == matvec(f,e2)
bad = [[Q(1,4),0,0],[0,Q(3,4),0],[0,0,Q(1,2)]]
assert matvec(f,matvec(bad,e1)) != matvec(f,matvec(bad,e2))
good = [[Q(1,4),0,0],[0,Q(1,4),0],[0,0,Q(3,4)]]
descended = [[Q(1,4),0],[0,Q(3,4)]]
for p in [(Q(1,3),)*3,e1,e2,(Q(0),Q(0),Q(1))]:
    assert matvec(f,matvec(good,p)) == matvec(descended,matvec(f,p))
    mass, conditional = likelihood_update(p,(Q(1,4),Q(1,4),Q(3,4)))
    coarse_mass, coarse_conditional = likelihood_update(matvec(f,p),(Q(1,4),Q(3,4)))
    assert coarse_mass == mass and matvec(f,conditional) == coarse_conditional
record("intertwining is a necessary extra premise", "A positive mass-preserving quotient identifies e1 and e2 but fails to descend an unequal likelihood; equal fine likelihoods descend and preserve probabilities and conditional images.")


# Two logically different hypotheses have different zero-branch consequences.
x = (Q(0), Q(1))
weak_mass = lambda v: v[0]
assert weak_mass(x) == 0 and x != (Q(0),Q(0))
# Without generatingness, action off span(K) is unconstrained by cone order.
nongenerating_map = [[Q(1,2),0],[0,Q(2)]]
assert matvec(nongenerating_map,(Q(1),Q(0))) == (Q(1,2),Q(0))
assert matvec([[Q(1,2),0],[0,Q(-1)]],(Q(1),Q(0))) == (Q(1,2),Q(0))
record("strict mass and generatingness guards", "A merely nonnegative mass functional can vanish on a nonzero positive state; order on a nongenerating ray does not constrain ambient complementary directions.")


# Dephasing domination witness recomputed as a 2 by 2 matrix.
px = [[Q(1,2),Q(1,2)],[Q(1,2),Q(1,2)]]
j0 = [[Q(1,2),Q(0)],[Q(0),Q(0)]]
residual = [[px[i][j]-j0[i][j] for j in range(2)] for i in range(2)]
assert residual[0][0]*residual[1][1]-residual[0][1]*residual[1][0] == Q(-1,4)
record("dephasing non-domination", "The direct Hermitian residual matrix has determinant -1/4.")


output = {"status": "pass", "check_groups": len(results), "arithmetic": "fractions.Fraction",
          "limitation": "Finite exact controls, not universal proof, formal-kernel certification, or empirical validation.",
          "results": results}
(ROOT / "INDEPENDENT_CHECK_RESULTS.json").write_text(json.dumps(output, indent=2)+"\n")
for result in results:
    print("PASS:",result["name"])
print("PASS:",len(results),"independent exact control groups")
