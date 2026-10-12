#!/usr/bin/env python3
"""Independent exact finite controls; these do not prove the measure theorems."""

import json
from collections import Counter

import sympy as sp
from sympy.functions.combinatorial.numbers import stirling


counts = Counter()


def check(category, assertion):
    if not assertion:
        raise AssertionError(category)
    counts[category] += 1


# The damped-coordinate quotient identity with an arbitrary positive denominator.
ar, ar1, a0, a1 = sp.symbols("ar ar1 a0 a1", nonzero=True)
check("hierarchy", sp.simplify((-ar1 * a0 + ar * a1) / a0**2
      - (-ar1 / a0 + (a1 / a0) * (ar / a0))) == 0)
B0, B1, Br, Br1, w = sp.symbols("B0 B1 Br Br1 w")
D = B0 - w
check("hierarchy", sp.simplify((-Br1 * D + Br * B1) / D**2
      - (-Br1 / D + (B1 / D) * (Br / D))) == 0)
check("atom_recombination", sp.simplify(D * 1 + w - B0) == 0)
check("atom_recombination", sp.simplify(D * (Br / D) - Br) == 0)
k, r = sp.symbols("k r", integer=True)
check("initial_lattice_moments", sp.expand(r*k-k**2/2-r**2/2+(k-r)**2/2) == 0)

# b_n = u^(n^2), with u = q^(-1/2).  Rational u>1 gives exact moments.
for u in [sp.Rational(2), sp.Rational(3, 2), sp.Rational(5, 3)]:
    for N in range(8):
        H = sp.Matrix(N+1, N+1, lambda i, j: u**((i+j)**2))
        minor = H[1:, 1:]
        denominator = minor.det() if N else sp.Integer(1)
        product = sp.prod(1-u**(-2*j) for j in range(1, N+1))
        ratio = H.det()/denominator
        check("gram_vandermonde_ratio", ratio == product)
        check("gram_positive_definite", all(H[:j, :j].det() > 0 for j in range(1, N+2)))
        check("christoffel_inverse", sp.cancel(1/H.inv()[0, 0] - product) == 0)
        if N:
            # Complete the square for the unique constrained polynomial minimum.
            h = H[1:, 0]
            coeff = sp.Matrix([1, *list(-minor.inv()*h)])
            check("constrained_minimum", (coeff.T*H*coeff)[0] == product)
        # The degree-zero coordinate alone receives the removed zero atom.
        for atom in [product/2, product, (product+1)/2]:
            G = H.copy()
            G[0, 0] -= atom
            check("rank_one_determinant", sp.cancel(G.det()-H.det()*(1-atom/product)) == 0)
            if atom <= product:
                # PSD follows by Schur complement here; principal-minor checks
                # independently cover these finite exact examples.
                all_nonnegative = all(G.extract(idx, idx).det() >= 0
                                      for size in range(1, N+2)
                                      for idx in sp.utilities.iterables.combinations(range(N+1), size))
                check("rank_one_psd", all_nonnegative)
            else:
                check("rank_one_negative", G.det() < 0)

# Two purely symbolic determinant identities, independent of numerical q choices.
u = sp.symbols("u", positive=True)
for N in range(1, 4):
    H = sp.Matrix(N+1, N+1, lambda i, j: u**((i+j)**2))
    check("symbolic_vandermonde_ratio", sp.factor(H.det()
          - H[1:, 1:].det()*sp.prod(1-u**(-2*j) for j in range(1, N+1))) == 0)

# Exact factorial-to-raw transformation, partition estimate and binomial envelope.
x, y = sp.symbols("x y")
for n in range(1, 17):
    check("stirling_transform", sp.expand(sum(stirling(n, j, kind=2)*sp.ff(x, j)
          for j in range(n+1))-x**n) == 0)
    for j in range(n+1):
        check("partition_bound", stirling(n, j, kind=2) <= sp.binomial(n, j)*n**(n-j))
    check("moment_envelope", sp.expand(sum(sp.binomial(n, j)*n**(n-j)*y**j
          for j in range(n+1))-(n+y)**n) == 0)

# Factorial PGF differentiation, including the sign and time-scale factors.
s, z, t = sp.symbols("s z t", positive=True)
for rate in [sp.Rational(1, 3), sp.Rational(2), sp.Rational(7, 2)]:
    pgf = sp.exp(s*rate*(z-1))
    check("poisson_laplace_substitution", sp.simplify(pgf.subs(z, 1-t/s)-sp.exp(-t*rate)) == 0)
    for j in range(9):
        check("poisson_factorial_moments", sp.diff(pgf, z, j).subs(z, 1) == (s*rate)**j)

# Rational finite product/tail instances.  Infinite limiting statements are
# justified in REVIEW.md, never by these finite checks.
for q in [sp.Rational(1, 4), sp.Rational(1, 3), sp.Rational(2, 5)]:
    for N in range(9):
        for M in range(N+1, N+6):
            wN = sp.prod(1-q**j for j in range(1, N+1))
            wM = sp.prod(1-q**j for j in range(1, M+1))
            check("product_tail", 0 < wN-wM <= q**(N+1)/(1-q))

print(json.dumps({
    "status": "PASS",
    "assertions": sum(counts.values()),
    "categories": dict(sorted(counts.items())),
    "scope": "Exact finite algebraic controls only; universal positivity, source theorems, determinacy, analyticity, Carleman divergence, and effective recovery require the ordinary proof review.",
}, indent=2, sort_keys=True))
