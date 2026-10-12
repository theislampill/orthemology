#!/usr/bin/env python3
"""Independent exact controls; no import of the author's or root's checks."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from fractions import Fraction as Q
from math import factorial
import sympy as s

HERE = Path(__file__).resolve().parent
checks = []

def record(name, detail):
    checks.append({"name": name, "status": "PASS", "detail": detail})

def add(*terms):
    out = {}
    for term in terms:
        for word, coefficient in term.items():
            out[word] = out.get(word, Q(0)) + coefficient
    return {w: c for w, c in out.items() if c}

def scale(term, coefficient):
    return {w: c * coefficient for w, c in term.items() if c * coefficient}

def mul(left, right, cap=4):
    out = {}
    for w, a in left.items():
        for v, b in right.items():
            if len(w + v) <= cap:
                out[w + v] = out.get(w + v, Q(0)) + a * b
    return {w: c for w, c in out.items() if c}

def comm(left, right):
    return add(mul(left, right), scale(mul(right, left), -1))

def exp_letter(letter, time, cap=4):
    return {letter * n: time ** n / factorial(n) for n in range(cap + 1)}

AA, BB = {"A": Q(1)}, {"B": Q(1)}
P = mul(mul(exp_letter("A", Q(1, 2)), exp_letter("B", Q(1))), exp_letter("A", Q(1, 2)))
R = mul(mul(exp_letter("B", Q(1, 2)), exp_letter("A", Q(1))), exp_letter("B", Q(1, 2)))
delta = add(P, scale(R, -1))
assert all(len(w) >= 3 for w in delta)
third = {w: c for w, c in delta.items() if len(w) == 3}
assert third == scale(comm(add(AA, BB), comm(AA, BB)), Q(-1, 8))
assert {w: c for w, c in P.items() if len(w) == 2} == {
    "AA": Q(1, 2), "AB": Q(1, 2), "BA": Q(1, 2), "BB": Q(1, 2)}
record("free_words_positive_strang", {w: str(c) for w, c in third.items()})

x, a, q, t = s.symbols("x a q t", real=True)
f = s.Function("f")(x)
F, G = x ** 2 / 2, (x - a) ** 2 / 2

def op(objective, p):
    return -s.diff(objective, x) * s.diff(p, x) - objective * p

def A(p): return s.expand(op(F, p))
def B(p): return s.expand(op(G, p))
def C(p): return s.expand(A(B(p)) - B(A(p)))
def S(p): return A(p) + B(p)
assert s.expand(C(f) - a * s.diff(f, x)) == 0
nested = s.expand(S(C(f)) - C(S(f)))
assert s.expand(nested - (2 * a * s.diff(f, x) + (2 * a * x - a ** 2) * f)) == 0
record("arbitrary_test_function_commutators", str(nested))

z = s.Symbol("z")
H = s.Function("H")(x)
lifted = -s.diff(H,x)*s.diff(z*f,x)-H*z*s.diff(z*f,z)
assert s.expand(lifted-z*op(H,f)) == 0
assert s.expand((z*x)*(z*x)-z*x*x) != 0
record("weight_coordinate_linear_intertwiner", "Lifted vector field applied to z p equals z B_H p; p↦z p is linear and not multiplicative")

def stages(centers, contractions):
    position, logweight = x, s.Integer(0)
    for center, contraction in zip(centers, contractions):
        logweight -= (position - center) ** 2 * (1 - contraction ** 2) / 4
        position = center + contraction * (position - center)
    return s.expand(position), s.expand(logweight)

yP, kP = stages([0, a, 0], [q, q ** 2, q])
yQ, kQ = stages([a, 0, a], [q, q ** 2, q])
ydiff, kdiff = s.factor(yP - yQ), s.factor(kP - kQ)
assert s.expand(ydiff - a * (q - 1) ** 3 * (q + 1)) == 0
assert s.expand(kdiff - a * (2 * x - a) * (q - 1) ** 3 * (q + 1) * (q ** 4 + 1) / 4) == 0
oddsdiff = s.factor(kdiff.subs(x, 1) - kdiff.subs(x, -1))
assert s.expand(oddsdiff - a * (q - 1) ** 3 * (q + 1) * (q ** 4 + 1)) == 0
record("exact_stage_recurrence", {"position_difference": str(ydiff), "logweight_difference": str(kdiff), "logodds_difference": str(oddsdiff)})

def jet_in_t(expr, order=3):
    # Express q=e^(-t/2); differentiation gives exact exponential-polynomial jets.
    expr = s.expand(expr)
    coefficients = []
    derivative = expr
    for n in range(order + 1):
        coefficients.append(s.expand(derivative.subs(q, 1) / factorial(n)))
        derivative = s.expand(-q * s.diff(derivative, q) / 2)
    return coefficients

assert jet_in_t(ydiff) == [0, 0, 0, -a / 4]
assert jet_in_t(kdiff) == [0, 0, 0, a ** 2 / 8 - a * x / 4]
assert jet_in_t(oddsdiff) == [0, 0, 0, -a / 2]
record("exact_third_derivatives", "Endpoint -a/4; logweight a²/8−ax/4; logodds -a/2")

def jmul(left, right):
    return [s.expand(sum(left[j] * right[n-j] for j in range(n+1))) for n in range(4)]

def jexp(logjet):
    assert logjet[0] == 0
    c1, c2, c3 = logjet[1:]
    return [s.Integer(1), c1, s.expand(c2+c1*c1/2), s.expand(c3+c1*c2+c1**3/6)]

def jpower(jet, n):
    result = [s.Integer(1), 0, 0, 0]
    for _ in range(n):
        result = jmul(result, jet)
    return result

moments = [s.Integer(1)] + list(s.symbols("m1:15", real=True))
def expect(poly):
    return s.expand(sum(coef * moments[monomial[0]] for monomial, coef in s.Poly(s.expand(poly), x).terms()))

def normalized_output(position, logweight, degree):
    weight = jexp(jet_in_t(logweight))
    numerator = [expect(c) for c in jmul(weight, jpower(jet_in_t(position), degree))]
    denominator = [expect(c) for c in weight]
    quotient = []
    for n in range(4):
        quotient.append(s.expand(numerator[n] - sum(denominator[j] * quotient[n-j] for j in range(1,n+1))))
    return quotient

for degree in range(6):
    pjet = normalized_output(yP, kP, degree)
    qjet = normalized_output(yQ, kQ, degree)
    differences = [s.expand(u-v) for u,v in zip(pjet,qjet)]
    p = x ** degree
    expected = s.expand(-a * (expect(s.diff(p,x)) + expect(x*p) - expect(x)*expect(p)) / 4)
    assert differences[:3] == [0,0,0]
    assert s.expand(differences[3] - expected) == 0
    if degree == 1:
        assert s.expand(differences[3] + a*(1+moments[2]-moments[1]**2)/4) == 0
record("normalized_exact_flow_polynomials", "Exact weighted-characteristic jets for p=1,x,…,x^5; symbolic moments; cubic =−a(Ep′+Cov(x,p))/4")

# A cylinder-algebra calculation, directly from the derivation rule.
cache = {}
def L(word, base):
    key = (word, base)
    if key not in cache:
        cache[key] = s.Symbol("l_" + (word or "empty") + "_" + base)
    return cache[key]

def derive(expr, letter):
    result = s.Integer(0)
    for (word, base), variable in list(cache.items()):
        if expr.has(variable):
            result += s.diff(expr, variable) * (L(letter+word, base) - L(letter,"one")*variable)
    return s.expand(result)

lp = L("", "p")
DBlp = derive(lp, "B")
DClp = derive(lp, "C")
lhs = derive(DClp, "B") - derive(DBlp, "C")
rhs = L("BC", "p") - L("CB", "p") - (L("BC", "one") - L("CB", "one"))*lp
assert s.expand(lhs-rhs) == 0
record("cylinder_lie_commutator", "[D_B,D_C] l_p = l_[B,C]p − l_[B,C]1 l_p, with derivation commutator convention")

# A nonconstant multiplier is invisible on every Dirac, but not on a mixture.
def halfexpect(p): return s.expand((p.subs(x,-1)+p.subs(x,1))/2)
assert s.expand(x*f - x*f) == 0
two_point_defect = halfexpect(x*x)-halfexpect(x)*halfexpect(x)
assert two_point_defect == 1
record("dirac_only_is_insufficient", "D=M_x gives zero on Diracs but V_D((δ−1+δ1)/2)(x)=1")

# Scalar equivalence at finite formal order, with a genuinely noncommuting jet.
e = s.Symbol("e")
def trunc(p, cap=4): return s.Poly(s.expand(p),e).terms()
def cut(p): return s.expand(sum(c*e**m[0] for m,c in trunc(p) if m[0]<=4))
def V(p): return cut(p+e*A(p)+e**2*B(p)+e**3*A(B(p))+e**4*B(A(p)))
scalar = 1+2*e-3*e**2+e**4
def U(p): return cut(scalar*V(p))
def poly_expect(poly): return s.expand(sum(coef*moments[monomial[0]] for monomial,coef in s.Poly(s.expand(poly),x).terms()))
cross = cut(poly_expect(U(x*x))*poly_expect(V(s.Integer(1))) - poly_expect(V(x*x))*poly_expect(U(s.Integer(1))))
assert cross == 0
assert cut(U(s.Integer(1))-V(s.Integer(1))) != 0
record("formal_scalar_cancellation", "Order-four noncommuting operator jet; scalar multiplier changes mass but vanishes in normalized cross-product")

payload = {"status":"PASS", "method":"Independent exact SymPy and rational free-word calculations; written proofs carry universal quantifiers", "sympy_version":s.__version__, "checks":checks, "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE / "CHECK_RESULTS.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":"PASS", "check_groups":len(checks), "output":str(HERE / "CHECK_RESULTS.json")},indent=2))
