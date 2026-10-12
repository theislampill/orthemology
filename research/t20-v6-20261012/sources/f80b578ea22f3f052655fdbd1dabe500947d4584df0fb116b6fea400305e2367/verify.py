#!/usr/bin/env python3
"""Exact author controls for repair/evidence commutation; no sampling."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as S


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
R = S.Rational
checks: list[dict] = []


def simp(x):
    return S.simplify(S.expand_log(S.sympify(x), force=True))


def equal(a, b):
    if isinstance(a, (tuple, list)):
        assert isinstance(b, (tuple, list)) and len(a) == len(b), (a, b)
        for x, y in zip(a, b):
            equal(x, y)
    else:
        assert simp(a - b) == 0, (a, b, simp(a - b))


def law(p):
    assert all(x >= 0 for x in p), p
    equal(sum(p), 1)


def bayes(p, likelihood):
    alpha = sum(x * l for x, l in zip(p, likelihood))
    assert alpha > 0
    return tuple(S.cancel(x * l / alpha) for x, l in zip(p, likelihood))


def kl(q, p):
    assert all(x > 0 for x in p)
    return simp(sum(x * S.log(x / y) for x, y in zip(q, p) if x != 0))


def channel(rows):
    assert rows
    assert all(x > 0 for row in rows for x in row)
    equal(tuple(map(sum, zip(*rows))), (1,) * len(rows[0]))


def project_known(p, blocks, conditionals, penalties):
    """Evaluate proven formula when exact within-block minimizers are supplied.

    penalties are exact exp(-d_a), not values fitted by an optimizer.
    """
    masses = tuple(sum(p[i] for i in block) for block in blocks)
    z = sum(s * e for s, e in zip(masses, penalties))
    assert z > 0
    weights = tuple(S.cancel(s * e / z) for s, e in zip(masses, penalties))
    q = [S.Integer(0)] * len(p)
    for block, r, weight in zip(blocks, conditionals, weights):
        law(r)
        for i, ri in zip(block, r):
            q[i] = S.cancel(weight * ri)
    law(q)
    return tuple(q), weights, z


def add(name, **details):
    checks.append({"name": name, "status": "PASS", **details})
    print(f"PASS {len(checks):02d}: {name}")


# Input integrity is checked separately from the twelve mathematical groups.
bindings = json.loads((HERE / "INPUT_BINDINGS.json").read_text())
for binding in bindings["inputs"]:
    data = (ROOT / binding["path"]).read_bytes()
    assert hashlib.sha256(data).hexdigest() == binding["sha256"]
    assert len(data) == binding["bytes"]
print(f"PASS input integrity: {len(bindings['inputs'])} bound predecessor reports")


# 1. Symbolic softmax minimization identity and evidence reweighting.
s = S.symbols("s0:3", positive=True)
e = S.symbols("e0:3", positive=True)
k = S.symbols("k0:3", positive=True)
t = S.symbols("t0:3", positive=True)
alpha = S.symbols("alpha", positive=True)
z = sum(si * ei for si, ei in zip(s, e))
w_star = tuple(si * ei / z for si, ei in zip(s, e))
w = tuple(ti / sum(t) for ti in t)
objective = sum(wi * S.log(wi / si) - wi * S.log(ei)
                for wi, si, ei in zip(w, s, e))
gap = sum(wi * S.log(wi / vi) for wi, vi in zip(w, w_star)) - S.log(z)
equal(objective, gap)
for wi, si, ei in zip(w_star, s, e):
    # KKT gradients agree across blocks: d_i=-log e_i.
    equal(S.log(wi / si) + 1 - S.log(ei), 1 - S.log(z))
new_s = tuple(ki * si / alpha for ki, si in zip(k, s))
new_z = sum(si * ei for si, ei in zip(new_s, e))
new_w = tuple(si * ei / new_z for si, ei in zip(new_s, e))
repaired_alpha = sum(ki * wi for ki, wi in zip(k, w_star))
equal(new_w, tuple(ki * wi / repaired_alpha for ki, wi in zip(k, w_star)))
equal(new_z, z * repaired_alpha / alpha)
add("symbolic three-block softmax identity, KKT, and commutation")


# 2. Independent exact conditional-minimizer control for the curved disk.
tt = S.symbols("t", positive=True)
sym_conditional = (tt, (1 - tt) / 2, (1 - tt) / 2)
radius_expr = sum((x - R(1, 3)) ** 2 for x in sym_conditional)
equal(radius_expr, R(3, 2) * (tt - R(1, 3)) ** 2)
equal(radius_expr.subs(tt, R(1, 6)), R(1, 24))
equal(radius_expr.subs(tt, R(1, 2)), R(1, 24))
assert R(1, 24) < R(1, 6)
raw_a = (R(4, 5), R(1, 10), R(1, 10))
ra = (R(1, 2), R(1, 4), R(1, 4))
f = sum(q * S.log(q / p) for q, p in zip(sym_conditional, raw_a))
equal(S.diff(f, tt), S.log(tt / (4 * (1 - tt))))
# On [1/6,1/2], t/[4(1-t)] is increasing with upper bound 1/4<1.
equal(S.diff(tt / (4 * (1 - tt)), tt), 1 / (4 * (1 - tt) ** 2))
equal((tt / (4 * (1 - tt))).subs(tt, R(1, 2)), R(1, 4))
equal(kl(ra, raw_a), S.log(R(5, 4)))
equal(sum((x - R(1, 3)) ** 2 for x in raw_a), R(49, 150))
assert R(49, 150) > R(1, 24)
add("curved conditional projection and exact cost log(5/4)")


# 3. Main off-model example: both actual channel outcomes, explicit targets.
blocks = ((0, 1, 2), (3, 4))
rb = (R(1, 2), R(1, 2))
penalties = (R(4, 5), S.Integer(1))
p = (R(2, 5), R(1, 20), R(1, 20), R(1, 4), R(1, 4))
plus = (R(3, 4),) * 3 + (R(1, 4),) * 2
minus = tuple(1 - x for x in plus)
channel((plus, minus))
q, weights, z0 = project_known(p, blocks, (ra, rb), penalties)
equal(q, (R(2, 9), R(1, 9), R(1, 9), R(5, 18), R(5, 18)))
equal(weights, (R(4, 9), R(5, 9)))
equal(z0, R(9, 10))
equal(kl(q, p), S.log(R(10, 9)))
targets = ((R(6, 17), R(3, 17), R(3, 17), R(5, 34), R(5, 34)),
           (R(2, 19), R(1, 19), R(1, 19), R(15, 38), R(15, 38)))
for row, target, expected_z, expected_alpha in zip(
        (plus, minus), targets, (R(17, 20), R(19, 20)), (R(17, 36), R(19, 36))):
    bp = bayes(p, row)
    projected, _, zp = project_known(bp, blocks, (ra, rb), penalties)
    equal(projected, target)
    equal(bayes(q, row), target)
    equal(zp, expected_z)
    equal(sum(x * y for x, y in zip(q, row)), expected_alpha)
    equal(sum(x * y for x, y in zip(p, row)), R(1, 2))
    equal(kl(projected, bp), -S.log(expected_z))
    equal(-S.log(zp), -S.log(z0) + S.log(R(1, 2)) - S.log(expected_alpha))
add("informative curved-block join: both off-model orders and value identity",
    projected_prior=list(map(str, q)), posteriors=[list(map(str, x)) for x in targets])


# 4. The conditional families are variable, not fixed templates.
feasible = (R(1, 6),) * 3 + (R(3, 8), R(1, 8))
fa = (R(1, 3),) * 3
fb = (R(3, 4), R(1, 4))
equal(project_known(feasible, blocks, (fa, fb), (1, 1))[0], feasible)
raw_a2 = (R(1, 10), R(4, 5), R(1, 10))
ra2 = (R(1, 4), R(1, 2), R(1, 4))
rb2 = (R(4, 5), R(1, 5))
equal(kl(ra2, raw_a2), S.log(R(5, 4)))
p2 = tuple(R(2, 3) * x for x in raw_a2) + tuple(R(1, 3) * x for x in rb2)
q2, w2, _ = project_known(p2, blocks, (ra2, rb2), penalties)
equal(w2, (R(8, 13), R(5, 13)))
equal(q2, (R(2, 13), R(4, 13), R(2, 13), R(4, 13), R(1, 13)))
for row in (plus, minus):
    equal(project_known(bayes(p2, row), blocks, (ra2, rb2), penalties)[0], bayes(q2, row))
assert ra2 != ra and rb2 != rb and fa != ra and fb != rb
add("variable curved and segment conditionals at feasible and off-model inputs")


# 5. Inactive channel block and a boundary-valued repair.
p6 = (R(4, 15), R(1, 30), R(1, 30), R(1, 6), R(1, 6), R(1, 3))
rows6 = (plus + (R(1, 2),), minus + (R(1, 2),))
channel(rows6)
q6, w6, z6 = project_known(p6, blocks, (ra, rb), penalties)
equal(q6, q + (S.Integer(0),))
equal(w6, weights)
equal(z6, R(3, 5))
assert q6[-1] == 0 and all(x > 0 for x in p6)
for row, target in zip(rows6, targets):
    projected = project_known(bayes(p6, row), blocks, (ra, rb), penalties)[0]
    equal(projected, target + (S.Integer(0),))
    equal(projected, bayes(q6, row))
add("inactive block omission with positive input and boundary output")


# 6. Coordinate faces, a one-block channel, and the one-state case.
pf = (R(1, 5), R(3, 10), R(1, 2))
rf = (R(1, 4), R(1, 2), R(3, 4))
qf = (R(2, 7), S.Integer(0), R(5, 7))
face = lambda v: (v[0] / (v[0] + v[2]), S.Integer(0), v[2] / (v[0] + v[2]))
equal(face(pf), qf)
for row in (rf, tuple(1 - x for x in rf)):
    equal(face(bayes(pf, row)), bayes(qf, row))
for row in ((R(2, 5),) * 5, (R(3, 5),) * 5):
    equal(bayes(p, row), p)
    equal(bayes(q, row), q)
equal(bayes((S.Integer(1),), (R(2, 3),)), (S.Integer(1),))
add("coordinate face, uninformative one-block channel, and one-state limits")


# 7. Boundary approximation without defining boundary second-argument projection.
eps = S.symbols("eps", positive=True)
pe = (1 - 2 * eps / 3, eps / 3, eps / 3)
qe = ((3 - 2 * eps) / (3 - eps), eps / (3 - eps), S.Integer(0))
# C=Delta({1,2}), c=e_1. Exact renormalization establishes its projection.
equal(qe[:2], (pe[0] / (pe[0] + pe[1]), pe[1] / (pe[0] + pe[1])))
equal(sum(qe), 1)
equal(tuple(S.limit(x, eps, 0, dir="+") for x in qe), (1, 0, 0))
projected_cost = -S.log(1 - eps / 3)
comparison_cost = -S.log(1 - 2 * eps / 3)
equal(S.limit(projected_cost, eps, 0, dir="+"), 0)
equal(S.limit(comparison_cost, eps, 0, dir="+"), 0)
# The ordered log arguments give the sandwich for 0<eps<1.
equal((1 - eps / 3) - (1 - 2 * eps / 3), eps / 3)
equal((1 - 2 * eps / 3) - (1 - eps), eps / 3)
aa, bb = S.symbols("aa bb", positive=True)
binary = aa * S.log(aa / bb) + (1 - aa) * S.log((1 - aa) / (1 - bb))
equal(S.diff(binary, aa, 2), 1 / (aa * (1 - aa)))
equal(1 / (aa * (1 - aa)) - 4, (2 * aa - 1) ** 2 / (aa * (1 - aa)))
add("boundary approximation and elementary Pinsker curvature identity")


# 8. One selected forward-stable likelihood fails off-model commutation.
binary_project = lambda v: (max(v[0], R(1, 2)), 1 - max(v[0], R(1, 2)))
pb = (R(1, 4), R(3, 4))
lb = (R(3, 4), R(1, 4))
equal(binary_project(pb), (R(1, 2), R(1, 2)))
left = binary_project(bayes(pb, lb))
right = bayes(binary_project(pb), lb)
equal(left, (R(1, 2), R(1, 2)))
equal(right, (R(3, 4), R(1, 4)))
assert left != right
equal(bayes((R(1, 2), R(1, 2)), tuple(1 - x for x in lb)), (R(1, 4), R(3, 4)))
equal(3 * tt / (1 + 2 * tt) - R(1, 2), (4 * tt - 1) / (2 * (1 + 2 * tt)))
add("single forward-preserving likelihood versus complete normalized channel")


# 9. Inherited fixed-marginal evidence erasure; no new-credit countermodel.
old_p = (R(1, 2), R(1, 4), R(1, 4))
old_plus = (R(3, 4), R(1, 4), R(1, 4))
old_minus = tuple(1 - x for x in old_plus)
fixed_project = lambda v: (R(1, 2), v[1] / (2 * (v[1] + v[2])), v[2] / (2 * (v[1] + v[2])))
for row, target in zip((old_plus, old_minus),
                       ((R(3, 4), R(1, 8), R(1, 8)), (R(1, 4), R(3, 8), R(3, 8)))):
    equal(bayes(old_p, row), target)
    equal(fixed_project(target), old_p)
    assert fixed_project(target) != bayes(fixed_project(old_p), row)
add("inherited fixed-marginal information-erasure regression")


# 10. Zero-entry extension is not silently asserted.
zero_p = (R(1, 2), R(1, 2))
zero_q = (S.Integer(1), S.Integer(0))
zero_row = (S.Integer(0), S.Integer(1))
equal(sum(x * y for x, y in zip(zero_p, zero_row)), R(1, 2))
equal(sum(x * y for x, y in zip(zero_q, zero_row)), 0)
equal(bayes(zero_p, zero_row), (0, 1))
add("zero-entry scope guard: possible before repair, undefined afterward")


# 11. Euclidean projection does not inherit the KL commutation theorem.
u = S.Matrix((R(3, 4), R(1, 4), 0))
v = S.Matrix((0, 0, 1))
d = u - v
ep = (R(1, 10), R(2, 5), R(1, 2))
el = (R(3, 4), R(3, 4), R(1, 4))
def euclidean_weight(prior):
    return S.cancel((S.Matrix(prior) - v).dot(d) / d.dot(d))
ew = euclidean_weight(ep)
ew_after = euclidean_weight(bayes(ep, el))
equal(ew, R(27, 65))
equal(ew_after, R(81, 130))
eq = tuple(ew * u[i] + (1 - ew) * v[i] for i in range(3))
beq = bayes(eq, el)
equal(sum(beq[:2]), R(81, 119))
assert 0 < ew < 1 and 0 < ew_after < 1
assert ew_after != sum(beq[:2])
add("Euclidean projection countercontrol: 81/130 differs from 81/119")


# 12. Different operator: moment-fibre entropy completion onto product model.
states = ((-1, -1), (-1, 1), (1, -1), (1, 1))
def means(prior):
    return tuple(sum(prior[i] * state[j] for i, state in enumerate(states)) for j in (0, 1))
def completion(prior):
    mx, my = means(prior)
    return tuple((1 + mx * x) * (1 + my * y) / 4 for x, y in states)
def determinant(prior):
    return prior[0] * prior[3] - prior[1] * prior[2]
unary_plus = tuple(R(2 + x, 4) for x, y in states)
unary_minus = tuple(1 - x for x in unary_plus)
channel((unary_plus, unary_minus))
uniform = (R(1, 4),) * 4
for sign in (-1, 1):
    prior = tuple((1 + sign * R(1, 2) * x * y) / 4 for x, y in states)
    assert all(x > 0 for x in prior)
    equal(means(prior), (0, 0))
    equal(completion(prior), uniform)
    lhs = completion(bayes(prior, unary_plus))
    rhs = bayes(completion(prior), unary_plus)
    equal(means(lhs), (R(1, 2), sign * R(1, 4)))
    equal(means(rhs), (R(1, 2), 0))
    assert lhs != rhs
    equal(determinant(lhs), 0)
    equal(determinant(rhs), 0)
# Model preservation independently: a unary reweighting multiplies both
# products in the 2x2 determinant by the same factor / normalizer^2.
a0, a1, b0, b1, lx0, lx1 = S.symbols("a0 a1 b0 b1 lx0 lx1", positive=True)
prod = (a0 * b0, a0 * b1, a1 * b0, a1 * b1)
reweighted = (lx0 * prod[0], lx0 * prod[1], lx1 * prod[2], lx1 * prod[3])
equal(determinant(reweighted), 0)
add("entropy-completion orientation guard with positive unary evidence")


assert len(checks) == 12
result = {
    "status": "PASS",
    "mathematical_control_groups": len(checks),
    "input_reports_verified": len(bindings["inputs"]),
    "arithmetic": "Exact SymPy symbolic and rational arithmetic; no sampling or numerical optimization",
    "verification_scope": "Author controls supplement the ordinary proof, not formal certification or independent review",
    "checks": checks,
}
(HERE / "CHECK_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"PASS all {len(checks)} exact mathematical control groups")
