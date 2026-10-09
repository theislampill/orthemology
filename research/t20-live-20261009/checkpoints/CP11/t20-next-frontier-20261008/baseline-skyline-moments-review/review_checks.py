#!/usr/bin/env python3
"""Bounded review checks. These are controls, not a proof or a source witness."""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import sympy as s

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = {
    "baseline-skyline-moments/RESULT.md": "b7bdcfa8b7288d69d569b6ed904c314fe58e4795c92549a6d525c433ad7c139f",
    "baseline-skyline-moments/controls.py": "3f65d6f86cda2dccb9c64705a12b238d95ae04205e2508e6266ed47c8edc4fbb",
    "baseline-skyline-moments/CONTROL_RESULTS.json": "83094e37c1749ed43c2363eba0d8914f18b946558e15cba0ddfbe211859abc41",
    "baseline-skyline-moments/CONTROL_RUN.log": "55550692c7ede266d518acb1b20e326eb80d50555bf27acb87c822df6feceb19",
    "baseline-skyline-moments/SOURCE_AUDIT.md": "0d9fff67c3d4f59f4f6b034269e11688ed952d6c68c8d4ef8468819d903962ed",
    "baseline-skyline-moments/OPERATION_LOG.md": "e99f59574baa8ee4aa9068d3bf6820244fb46e27571a2fef9f5c5364cf97a951",
    "baseline-skyline-moments/SHA256SUMS": "1f712341faa82e63b931a17a998518d2d61ad5ccd109cfe56d94229854083807",
    "retained-skyline-likelihood/RESULT.md": "e5dce85e41eaf41e69c373c26793478fa057de293502c22eb0a133f85221b345",
    "skyline-count-information/RESULT.md": "b96715873d240787ea6343538b4df54d94dc4bd7a52b79615fcaa9b2d34c2e4d",
    "skyline-likelihood-score/RESULT.md": "ba6345d03e5fe9d2735f221ee45f5ee6b6f05508ce4d96f8ba9a86ceb3da5b5f",
}


def h(n, p=1):
    return sum((F(1, j**p) for j in range(1, n+1)), F(0))


def product_integral(n, weight=0):
    return sum((F((-1)**j * comb(n, j), (j+weight+1)**2)
                for j in range(n+1)), F(0))


def incomparable(n):
    # Direct multinomial expansion of (u+v-uv)^j, rather than the
    # source control's complementary-product double sum.
    out = F(0)
    for j in range(n+1):
        inner = F(0)
        for a in range(j+1):
            for b in range(j-a+1):
                c = j-a-b
                coefficient = factorial(j)//(factorial(a)*factorial(b)*factorial(c))
                inner += F(coefficient*(-1)**c, (a+c+1)*(b+c+1))
        out += F((-1)**j*comb(n, j), (j+2)**2)*inner
    return out


def check_exact(n):
    m = n+1
    u = product_integral(n)
    u2 = 2*(product_integral(n, 1)+incomparable(n))
    ku = F(0) if n == 0 else n*(product_integral(n-1, 1)+2*incomparable(n-1))
    assert u == h(m)/m
    assert u2 == (h(m+1)**2-h(m+1,2)+2*(h(m+1)-1))/(m*(m+1))
    assert ku == (h(m)**2-h(m,2)+h(m)-1)/m
    c2 = h(n)**2+h(n)-h(n,2)-2*m*ku+m*m*u2
    delta = -2*h(m)/m+F(2,m*m)-(h(m)**2-h(m,2)-4)/(m+1)-2*(h(m)+1)/(m+1)**2
    assert c2 == h(n)+delta
    et = F(0) if n == 0 else n*product_integral(n-1, 1)
    eq = (c2-h(n))/(2*m*m)+2*(et/m-product_integral(n, 1))
    if n >= 1:
        assert u2 != 2*incomparable(n)
        assert ku != n*2*incomparable(n-1)
        assert abs(delta) <= 11*h(m)**2/m
    return {"n": n, "EU2": str(u2), "EKU": str(ku), "ECm2": str(c2), "EQ": str(eq)}


def symbolic_checks():
    m, hm, gm = s.symbols("m h g", positive=True)
    hn, gn = hm-1/m, gm-1/m**2
    hp, gp = hm+1/(m+1), gm+1/(m+1)**2
    u2 = (hp**2-gp+2*(hp-1))/(m*(m+1))
    ku = (hm**2-gm+hm-1)/m
    k2 = hn**2+hn-gn
    delta = -2*hm/m+2/m**2-(hm**2-gm-4)/(m+1)-2*(hm+1)/(m+1)**2
    assert s.simplify(k2-2*m*ku+m*m*u2-hn-delta) == 0
    assert s.simplify(hn-m*hm/m+1/m) == 0
    assert s.simplify(hn-(m-1)*hm/m-(hm-1)/m) == 0
    et = (hm-1)/m
    em1 = (hp-1)/(m*(m+1))
    eq_direct = (k2-2*m*ku+m*m*u2-hn)/(2*m*m)+2*(et/m-em1)
    eq_source = delta/(2*m*m)+2*((hm-1)/(m*m*(m+1))-1/(m*(m+1)**2))
    assert s.simplify(eq_direct-eq_source) == 0
    x, y = s.symbols("x y")
    u1 = x+y-x*y
    m11 = (x*x+(1-x*x)*y*y)/4
    q1 = ((1-2*u1)**2-1)/8+x*y-2*m11
    assert s.integrate(u1**2, (x,0,1), (y,0,1)) == s.Rational(11,18)
    assert s.integrate((1-2*u1)**2, (x,0,1), (y,0,1)) == s.Rational(4,9)
    assert s.integrate((1-u1)**2, (x,0,1), (y,0,1)) == s.Rational(1,9)
    assert s.integrate(q1, (x,0,1), (y,0,1)) == -s.Rational(7,72)
    return {"compensation_identity": "PASS", "means": "PASS", "EQ_identity": "PASS",
            "direct_n1_sample_integration": "PASS", "EQ_factored": str(s.factor(eq_direct))}


def main():
    for relative, digest in EXPECTED.items():
        assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest() == digest, relative
    here = Path(__file__).resolve().parent
    assert (here/"source-rerun/controls.py").read_bytes() == (ROOT/"baseline-skyline-moments/controls.py").read_bytes()
    assert (here/"source-rerun/CONTROL_RESULTS.json").read_bytes() == (ROOT/"baseline-skyline-moments/CONTROL_RESULTS.json").read_bytes()
    rows = [check_exact(n) for n in range(17)]
    assert rows[0] == {"n":0,"EU2":"1","EKU":"0","ECm2":"1","EQ":"0"}
    assert rows[1] == {"n":1,"EU2":"11/18","EKU":"3/4","ECm2":"4/9","EQ":"-7/72"}
    result = {"status":"PASS", "source_digests":EXPECTED, "multinomial_geometric_checks":rows,
              "symbolic_checks":symbolic_checks(), "source_control_json_byte_match":True,
              "scope":"Finite deterministic controls plus algebra; no external witness, world validation, or closure authority."}
    (here/"CHECK_RESULTS.json").write_text(json.dumps(result, indent=2)+"\n")
    print("PASS: 10 source digests unchanged; exact copied controls and generated JSON match.")
    print("PASS: separate multinomial geometric checks n=0..16; wrong-orientation candidates rejected.")
    print("PASS: symbolic compensation and Q-mean identities; direct n=1 sample integration.")


if __name__ == "__main__":
    main()
