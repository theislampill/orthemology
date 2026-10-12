#!/usr/bin/env python3
"""Exact finite controls for RESULT.md, not a replacement for its general proof.

Each negative support case must exhibit an actual fibre ambiguity; no numerical
solver or failure-to-find-certificate is used as evidence of nonexistence.
"""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform

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


def is_zero(v):
    if isinstance(v, S.MatrixBase):
        return all(S.simplify(x) == 0 for x in v)
    return S.simplify(v) == 0


def mass(p):
    return sum(p)


def law(p):
    return mass(p) == 1 and all(x >= 0 for x in p)


def alpha(L, p):
    return (L.T * p)[0]


def posterior(L, p):
    a = alpha(L, p)
    assert a > 0
    return S.diag(*L) * p / a


def support_certificate(M, support):
    """Find a rational v=M^T a: v_Z=0, v_S>=1 via active systems.

    The search is small and exact. All candidates are checked by substitution.
    No-candidate is not taken as proof: the caller also requires a fibre witness.
    """
    support = sorted(support)
    if not support:
        return S.zeros(M.rows, 1), S.zeros(M.cols, 1)
    zeros = [i for i in range(M.cols) if i not in support]
    null = M[:, zeros].T.nullspace() if zeros else list(S.eye(M.rows).columnspace())
    if not null:
        return None
    N = S.Matrix.hstack(*null)
    A = M[:, support].T * N
    d = A.cols
    assert A.rank() == d
    for active in combinations(range(len(support)), d):
        B = A[list(active), :]
        if B.det() == 0:
            continue
        t = B.inv() * S.ones(d, 1)
        if all(x >= 1 for x in A * t):
            a = N * t
            v = M.T * a
            assert all(v[i] == 0 for i in zeros)
            assert all(v[i] >= 1 for i in support)
            return a, v
    return None


def kernel_circuits(M):
    """Enumerate small minimal column dependencies, without external libraries."""
    out = []
    for size in range(1, min(M.rows + 1, M.cols) + 1):
        for indices in combinations(range(M.cols), size):
            ns = M[:, list(indices)].nullspace()
            if len(ns) != 1 or any(x == 0 for x in ns[0]):
                continue
            v = S.zeros(M.cols, 1)
            c = ns[0] / ns[0][0]
            for i, value in zip(indices, c):
                v[i] = value
            assert is_zero(M * v)
            out.append(v)
    return out


def fibre_witness(M, support, circuits):
    """Find p possible, q impossible, with Mp=Mq, using kernel circuits."""
    for raw in circuits:
        for d in (raw, -raw):
            if not all(d[i] >= 0 for i in support):
                continue
            if not any(d[i] > 0 for i in support):
                continue
            positive = S.Matrix([max(x, 0) for x in d])
            negative = S.Matrix([max(-x, 0) for x in d])
            assert mass(positive) == mass(negative) > 0
            p = positive / mass(positive)
            q = negative / mass(negative)
            assert law(p) and law(q) and is_zero(M * (p - q))
            assert sum(p[i] for i in support) > 0
            assert sum(q[i] for i in support) == 0
            return p, q
    return None


def all_supports_case(name, M, expected, expected_count):
    assert M.rank() == M.rows
    assert M.col_join(S.ones(1, M.cols)).rank() == M.rows
    circuits = kernel_circuits(M)
    yes = no = 0
    for mask in range(1 << M.cols):
        support = {i for i in range(M.cols) if mask & (1 << i)}
        cert = support_certificate(M, support)
        witness = fibre_witness(M, support, circuits)
        assert (cert is not None) == expected(support), (name, mask, "certificate")
        assert (witness is not None) == (not expected(support)), (name, mask, "witness")
        if cert is not None:
            a, v = cert
            assert is_zero(v - M.T * a)
            assert all(v[i] >= 0 for i in range(M.cols))
            assert {i for i in range(M.cols) if v[i] > 0} == support
            yes += 1
        else:
            p, q = witness
            indicator = S.Matrix([int(i in support) for i in range(M.cols)])
            assert alpha(indicator, p) > 0 and alpha(indicator, q) == 0
            no += 1
    check(name + ": every support has exact certificate or fibre counterexample",
          yes == expected_count and yes + no == (1 << M.cols),
          {"supports": yes + no, "certified": yes, "counterexamples": no,
           "kernel_circuits": len(circuits)})
    return yes, no


bindings = json.loads((HERE / "INPUT_BINDINGS.json").read_text())
for entry in bindings["local_inputs"]:
    data = (ROOT / entry["path"]).read_bytes()
    check("bound input " + entry["path"], len(data) == entry["bytes"]
          and hashlib.sha256(data).hexdigest() == entry["sha256"])

states = list(product((-1, 1), repeat=3))
M = S.Matrix([[1] * 8]
             + [[a[i] for a in states] for i in range(3)]
             + [[a[i] * a[j] for a in states] for i, j in ((0, 1), (0, 2), (1, 2))])
h = S.Matrix([x * y * z for x, y, z in states])
q = S.Matrix([Q(1 + x*y + x*z + y*z, 4) for x, y, z in states])
L = S.Matrix([q[i] * (1 + Q(x, 3)) for i, (x, y, z) in enumerate(states)])
zero_indices = [i for i, value in enumerate(q) if value == 0]
positive_indices = [i for i, value in enumerate(q) if value > 0]

check("pairwise rank, parity kernel, and exact q indicator",
      M.rank() == 7 and M.nullspace() == [h]
      and {states[i] for i in positive_indices} == {(-1, -1, -1), (1, 1, 1)}
      and all(q[i] == 1 for i in positive_indices) and len(zero_indices) == 6)
exposing = S.Matrix([Q(1, 4), 0, 0, 0, Q(1, 4), Q(1, 4), Q(1, 4)])
check("q is a nonnegative retained support witness for L",
      is_zero(M.T * exposing - q) and all(x >= 0 for x in q)
      and {i for i, x in enumerate(L) if x > 0} == set(positive_indices))
check("L has unretained cubic coefficient 1/12 and valid scaled likelihood",
      (h.T * L)[0] / 8 == Q(1, 12)
      and M.col_join(L.T).rank() == 8
      and set(L) == {0, Q(2, 3), Q(4, 3)}
      and all(0 <= Q(3, 4)*x <= 1 for x in L))

eps = Q(1, 2)
p_plus = S.Matrix([(1 + eps * v) / 8 for v in h])
p_minus = S.Matrix([(1 - eps * v) / 8 for v in h])
check("interior parity priors retain exactly the same pairwise record",
      law(p_plus) and law(p_minus) and all(x > 0 for x in p_plus)
      and all(x > 0 for x in p_minus)
      and M * p_plus == M * p_minus == S.Matrix([1, 0, 0, 0, 0, 0, 0]))
check("same feasible status, different branch mass and retained posterior",
      alpha(q, p_plus) == alpha(q, p_minus) == Q(1, 4)
      and alpha(L, p_plus) == Q(7, 24) and alpha(L, p_minus) == Q(5, 24)
      and alpha(Q(3, 4)*L, p_plus) == Q(7, 32)
      and alpha(Q(3, 4)*L, p_minus) == Q(5, 32)
      and M * posterior(L, p_plus) == S.Matrix([1, Q(5, 7), Q(5, 7), Q(5, 7), 1, 1, 1])
      and M * posterior(L, p_minus) == S.Matrix([1, Q(-1, 5), Q(-1, 5), Q(-1, 5), 1, 1, 1]))
check("q descends as probability but not as retained normalized posterior",
      alpha(q, p_plus) == alpha(q, p_minus)
      and (M * posterior(q, p_plus))[1] == eps
      and (M * posterior(q, p_minus))[1] == -eps)

# Symbolic equality uses exact rational-function simplification, not sampling.
t = S.symbols("epsilon", real=True)
for sign in (1, -1):
    p = S.Matrix([(1 + sign*t*v)/8 for v in h])
    raw = M * S.diag(*L) * p
    assert is_zero(raw[0] - (Q(1, 4) + sign*t/12))
    for i in (1, 2, 3):
        assert is_zero(raw[i] / raw[0] - (1 + sign*3*t)/(3 + sign*t))
    for i in (4, 5, 6):
        assert is_zero(raw[i] - raw[0])
check("symbolic epsilon branch and posterior formulas", True)

singleton = S.Matrix([int(a == (1, 1, 1)) for a in states])
boundary_plus = S.Matrix([(1 + x)/8 for x in h])
boundary_minus = S.Matrix([(1 - x)/8 for x in h])
check("singleton normalized-only branch has boundary feasibility ambiguity",
      law(boundary_plus) and law(boundary_minus)
      and M * boundary_plus == M * boundary_minus
      and alpha(singleton, boundary_plus) == Q(1, 4)
      and alpha(singleton, boundary_minus) == 0
      and M * posterior(singleton, p_plus) == M * posterior(singleton, p_minus))

check("six zero columns expose a dimension-five facet of dimension-six P",
      M[:, zero_indices].rank() == len(zero_indices) == 6 and M.rank() == 7)
for size in (0, 1, 2):
    for scope in combinations(range(3), size):
        observed = {tuple(states[i][j] for j in scope) for i in zero_indices}
        assert observed == set(product((-1, 1), repeat=size))
check("six zero atoms cover every unary/pair assignment, excluding local nonnegative sums", True)

p0 = S.Matrix([Q(1, 6) if i in zero_indices else 0 for i in range(8)])
check("uniform six-zero law lies on facet with expected pairwise record",
      law(p0) and alpha(q, p0) == 0
      and M * p0 == S.Matrix([1, 0, 0, 0, Q(-1, 3), Q(-1, 3), Q(-1, 3)]))
tables = {}
for i, j in combinations(range(3), 2):
    table = {assignment: sum(p0[k] for k, a in enumerate(states)
                             if (a[i], a[j]) == assignment)
             for assignment in product((-1, 1), repeat=2)}
    assert all(value > 0 for value in table.values())
    assert all(value == (Q(1, 6) if a == b else Q(1, 3))
               for (a, b), value in table.items())
    tables[str((i, j))] = {str(k): str(v) for k, v in table.items()}
check("all local pair cells positive despite global boundary record", True, tables)
check("boundary record has a unique six-zero representation",
      M[:, zero_indices].nullspace() == []
      and M[:, zero_indices] * S.ones(6, 1)/6 == M * p0)

# Uniform-reference tilt exp(-t*(xy+xz+yz)): let a=exp(-4t)>0,
# factor out exp(t). Six zero atoms have weight 1 and two others weight a.
a = S.symbols("a", positive=True)
tilt = S.Matrix([1/(6+2*a) if i in zero_indices else a/(6+2*a) for i in range(8)])
check("uniform exponential leaf approaches boundary only as parameter diverges",
      is_zero(mass(tilt) - 1) and is_zero(alpha(q, tilt) - a/(3+a))
      and tilt.applyfunc(lambda value: S.limit(value, a, 0, dir="+")) == p0)

rho = Q(-2, 5)
proposed_tables = {(x, y): (1+rho*x*y)/4 for x, y in product((-1, 1), repeat=2)}
C = S.Matrix(3, 3, lambda i, j: 1 if i == j else rho)
outside_record = S.Matrix([1, 0, 0, 0, rho, rho, rho])
check("positive local tables and positive-definite proposed covariance do not ensure realizability",
      all(x > 0 for x in proposed_tables.values())
      and set(proposed_tables.values()) == {Q(3, 20), Q(7, 20)}
      and sum(proposed_tables.values()) == 1
      and all(sum(v for (x, y), v in proposed_tables.items() if x == s) == Q(1, 2)
              for s in (-1, 1))
      and C.eigenvals() == {Q(1, 5): 1, Q(7, 5): 2}
      and (exposing.T * outside_record)[0] == Q(-1, 20))

Md = S.Matrix([[1, 1, 1], [0, 0, 1]])
Ld = S.Matrix([Q(1, 2), 1, 0])
e0, e1 = S.eye(3)[:, 0], S.eye(3)[:, 1]
vd = S.Matrix([1, 1, 0])
check("duplicate-column example retains feasibility plus posterior but not probability",
      support_certificate(Md, {0, 1}) is not None
      and is_zero(vd - Md.T * S.Matrix([1, -1]))
      and Md * e0 == Md * e1
      and Md * posterior(Ld, e0) == Md * posterior(Ld, e1) == S.Matrix([1, 0])
      and alpha(Ld, e0) == Q(1, 2) and alpha(Ld, e1) == 1)

line = S.Matrix([[1, 1, 1], [0, Q(1, 2), 1]])
middle = S.Matrix([0, 1, 0])
ends = S.Matrix([Q(1, 2), 0, Q(1, 2)])
check("convex-hull face without column saturation does not suffice",
      line * middle == line * ends and alpha(middle, middle) == 1
      and alpha(middle, ends) == 0)

without_mass = S.Matrix([[0, 1]])
missing_support = S.Matrix([1, 0])
check("mass retention is needed for row-space rather than affine certification",
      without_mass.rank() == 1
      and without_mass.col_join(S.ones(1, 2)).rank() == 2
      and without_mass.col_join(missing_support.T).rank() == 2)

positive_parity = {i for i in range(8) if h[i] == 1}
negative_parity = set(range(8)) - positive_parity
counts = []
counts.append(all_supports_case("three-bit pairwise matrix", M,
    lambda U: not U or bool(U & positive_parity) and bool(U & negative_parity), 226))
counts.append(all_supports_case("collinear nonvertex columns", line,
    lambda U: set(range(3))-U in (set(), {0}, {2}, {0, 1, 2}), 4))
counts.append(all_supports_case("duplicate endpoint columns", Md,
    lambda U: U in (set(), {0, 1}, {2}, {0, 1, 2}), 4))
triangle = S.Matrix([[1, 1, 1, 1], [0, 1, 0, Q(1, 3)], [0, 0, 1, Q(1, 3)]])
facial_zeros = (set(), {0}, {1}, {2}, {0, 1}, {0, 2}, {1, 2}, {0, 1, 2, 3})
counts.append(all_supports_case("triangle with supplied interior column", triangle,
    lambda U: set(range(4))-U in facial_zeros, 8))
counts.append(all_supports_case("mass-only matrix", S.ones(1, 3),
    lambda U: U in (set(), {0, 1, 2}), 2))
counts.append(all_supports_case("full record matrix", S.eye(3),
    lambda U: True, 8))
check("all-support sweep totals", sum(x+y for x, y in counts) == 304
      and sum(x for x, y in counts) == 252 and sum(y for x, y in counts) == 52,
      {"support_patterns": 304, "exact_certificates": 252, "explicit_fibre_ambiguities": 52})

check("empty support and strictly positive endpoints have v=0 and v=1 certificates",
      support_certificate(M, set())[1] == S.zeros(8, 1)
      and is_zero(M.T * S.Matrix([1, 0, 0, 0, 0, 0, 0]) - S.ones(8, 1)))

result = {
    "status": "PASS",
    "arithmetic": "Exact SymPy integers, rationals, and symbolic rational identities; no numerical optimizer.",
    "python_version": platform.python_version(),
    "sympy_version": S.__version__,
    "assertion_groups": len(checks),
    "support_patterns": 304,
    "exact_support_certificates": 252,
    "explicit_fibre_ambiguities": 52,
    "checks": checks,
    "scope": "Bounded author controls for a written general proof; no formal-kernel or independent-review claim."
}
(HERE / "CONTROL_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"PASS: {len(checks)} assertion groups; 304 support patterns (252 certificates, 52 ambiguities).")
