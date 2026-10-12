#!/usr/bin/env python3
"""Exact finite controls, not a proof-kernel or universal proof substitute."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb, factorial
from pathlib import Path
import platform
import sympy as s

ROOT = Path(__file__).resolve().parent
CHECKS = []
DETAILS = {}


def check(name, assertion):
    if not bool(assertion):
        raise AssertionError(name)
    CHECKS.append(name)


def equal(name, lhs, rhs):
    check(name, s.simplify(lhs-rhs) == 0)


def laws(M):
    norm = s.Integer(2)**(M-1)
    return ({j: s.binomial(M, j)/norm for j in range(M+1) if j % 2 == 0},
            {j: s.binomial(M, j)/norm for j in range(M+1) if j % 2 == 1})


def expectation(law, polynomial, x):
    return s.expand(sum(w*s.sympify(polynomial).subs(x, j) for j, w in law.items()))


def generator(F, p, xs):
    return s.expand(-sum(s.diff(F, x)*s.diff(p, x) for x in xs)-F*p)


def top(p, xs):
    P = s.Poly(p, *xs)
    n = P.total_degree()
    return s.Add(*(c*s.prod(x**e for x, e in zip(xs, powers))
                   for powers, c in P.terms() if sum(powers) == n))


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output_dir):
    for entry in json.loads((ROOT/'INPUT_BINDINGS.json').read_text())['inputs']:
        path = ROOT/entry['snapshot']
        check('input_snapshot:'+entry['source'], hash_file(path) == entry['sha256'])

    # Classical finite-difference identities, with exact standard-library rationals.
    for M in range(2, 19):
        den = 2**(M-1)
        check(f'binomial_even_mass_{M}', sum(comb(M, j) for j in range(0, M+1, 2)) == den)
        check(f'binomial_odd_mass_{M}', sum(comb(M, j) for j in range(1, M+1, 2)) == den)
        for r in range(M+1):
            value = sum(Fraction((-1)**j*comb(M, j)*j**r, den) for j in range(M+1))
            expected = Fraction((-1)**M*factorial(M), den) if r == M else 0
            check(f'binomial_moment_M{M}_r{r}', value == expected)

    x = s.symbols('x')
    # Vary both relevant degrees, including affine F and a descriptor below F's degree.
    for D in range(1, 6):
        for K in range(1, 6):
            F = 2*x**D+x**(D-1)+3
            p = x**K-3*x**(K-1)+2
            M = D+K
            Bp = generator(F, p, [x])
            check(f'degree_D{D}_K{K}', s.degree(Bp, x) == M)
            mu, nu = laws(M)
            em = lambda q: expectation(mu, q, x)
            en = lambda q: expectation(nu, q, x)
            for r in range(M):
                equal(f'full_lower_moments_D{D}_K{K}_r{r}', em(x**r), en(x**r))
            equal(f'energy_D{D}_K{K}', em(F), en(F))
            expected = s.Rational((-1)**(M+1)*factorial(M)*2, 2**(M-1))
            equal(f'raw_gap_D{D}_K{K}', em(Bp)-en(Bp), expected)
            dm = em(Bp)+em(F)*em(p)
            dn = en(Bp)+en(F)*en(p)
            equal(f'normalized_gap_D{D}_K{K}', dm-dn, expected)
            check(f'nonzero_gap_D{D}_K{K}', dm != dn)

    # The displayed quadratic three-coordinate witness.
    F, p, M = x*x/2, x**3, 5
    Bp = generator(F, p, [x])
    mu, nu = laws(M)
    em = lambda q: expectation(mu, q, x)
    en = lambda q: expectation(nu, q, x)
    expected_moments = [1, s.Rational(5, 2), s.Rational(15, 2), 25, 90]
    for r, value in enumerate(expected_moments):
        equal(f'explicit_mu_moment_{r}', em(x**r), value)
        equal(f'explicit_nu_moment_{r}', en(x**r), value)
    equal('explicit_mu_fifth', em(x**5), 340)
    equal('explicit_nu_fifth', en(x**5), s.Rational(695, 2))
    equal('explicit_mu_derivative', em(Bp)+em(F)*em(p), -s.Rational(605, 4))
    equal('explicit_nu_derivative', en(Bp)+en(F)*en(p), -155)
    for r in [1, 2]:
        b = generator(F, x**r, [x])
        equal(f'first_two_derivatives_agree_{r}', em(b)+em(F)*em(x**r), en(b)+en(F)*en(x**r))
    DETAILS['quadratic_witness'] = {
        'mu': {str(k): str(v) for k, v in mu.items()},
        'nu': {str(k): str(v) for k, v in nu.items()},
        'common_moments_0_through_4': list(map(str, expected_moments)),
        'derivative_mu': '-605/4', 'derivative_nu': '-155', 'gap': '15/4'}

    # Positive laws in the same finite-simplex interior.
    mumix = {j: mu.get(j, s.Integer(0))/2+s.Rational(1, 12) for j in range(6)}
    numix = {j: nu.get(j, s.Integer(0))/2+s.Rational(1, 12) for j in range(6)}
    for name, law in [('mu', mumix), ('nu', numix)]:
        check('mixed_exact_rational_'+name, all(w.is_Rational for w in law.values()))
        equal('mixed_mass_'+name, sum(law.values()), 1)
        check('mixed_strict_positivity_'+name, all(w > 0 for w in law.values()))
    emm = lambda q: expectation(mumix, q, x)
    enn = lambda q: expectation(numix, q, x)
    for r in range(5):
        equal('mixed_equal_moment_'+str(r), emm(x**r), enn(x**r))
    equal('mixed_normalized_gap', emm(Bp)+emm(F)*emm(p)-enn(Bp)-enn(F)*enn(p), s.Rational(15, 8))

    # A separate finite-evaluation/Jordan witness uses only dim(S)+1=5 points.
    basis = [s.Integer(1), x, x*x, x**3, Bp]
    E = s.Matrix([[q.subs(x, j) for j in range(5)] for q in basis])
    check('finite_evaluation_invertible', E.det() != 0)
    coeffs = E.inv()*s.Matrix([0, 0, 0, 0, 1])
    positive = sum(c for c in coeffs if c > 0)
    negative = -sum(c for c in coeffs if c < 0)
    equal('jordan_equal_positive_mass', positive, negative)
    check('jordan_nonzero_mass', positive > 0)
    jm = {j: c/positive for j, c in enumerate(coeffs) if c > 0}
    jn = {j: -c/positive for j, c in enumerate(coeffs) if c < 0}
    for q in basis[:-1]+[F]:
        equal('jordan_annihilates_'+str(q), expectation(jm, q, x), expectation(jn, q, x))
    equal('jordan_separates_generator', expectation(jm, Bp, x)-expectation(jn, Bp, x), 1/positive)
    DETAILS['finite_evaluation_witness'] = {'coefficients': list(map(str, coeffs)),
        'positive_mass': str(positive), 'mu': {str(k): str(v) for k, v in jm.items()},
        'nu': {str(k): str(v) for k, v in jn.items()}}

    # Multivariate examples require actual degree-preserving direction selection.
    y, z, r = s.symbols('y z r')
    cases = [([x, y], x*x+x*y+y*y+1, x**3-2*x*y*y+4*y+1),
             ([x, y, z], x**3+y**3+z*z, x*x+y*z+3*z)]
    for index, (xs, f, q) in enumerate(cases):
        D, K = s.Poly(f, *xs).total_degree(), s.Poly(q, *xs).total_degree()
        M = D+K
        fq = top(f, xs)*top(q, xs)
        v = next(v for v in product(range(M+1), repeat=len(xs))
                 if fq.subs(dict(zip(xs, v))) != 0)
        Bq = generator(f, q, xs)
        check(f'multivariate_degree_{index}', s.Poly(Bq, *xs).total_degree() == M)
        line = s.expand(Bq.subs({xx: r*vv for xx, vv in zip(xs, v)}, simultaneous=True))
        lm, ln = laws(M)
        gap = expectation(lm, line, r)-expectation(ln, line, r)
        predicted = s.Rational((-1)**(M+1)*factorial(M), 2**(M-1))*fq.subs(dict(zip(xs, v)))
        equal(f'multivariate_gap_{index}', gap, predicted)
        check(f'multivariate_gap_nonzero_{index}', gap != 0)
        # Every monomial of total degree below M is checked on this line.
        for powers in product(range(M), repeat=len(xs)):
            if sum(powers) < M:
                monomial = s.prod((r*vv)**a for a, vv in zip(powers, v))
                equal(f'multivariate_lower_{index}_{powers}', expectation(lm, monomial, r), expectation(ln, monomial, r))
        DETAILS[f'multivariate_{index}'] = {'direction': list(v), 'gap': str(gap)}

    # Constants are deliberate negative controls for overbroad theorem statements.
    c = s.symbols('c')
    for q in [s.Integer(1), x, x*x+3*x]:
        b = generator(c, q, [x])
        equal('constant_F_stationary_'+str(q), expectation(mu, b, x)+c*expectation(mu, q, x), 0)
    for f in [x, x*x/2, x**5-x]:
        b = generator(f, s.Integer(3), [x])
        equal('constant_descriptor_stationary_'+str(f), expectation(mu, b, x)+3*expectation(mu, f, x), 0)
    # Omitting killing invalidates the degree argument for quadratic F.
    for k in range(1, 8):
        equal('drift_only_quadratic_invariant_'+str(k), -x*s.diff(x**k, x), -k*x**k)

    # Exact positive Gaussian-family control, separate from all finite-law scope.
    t = s.symbols('t', real=True)
    a0 = s.symbols('a0', real=True)
    v0 = s.symbols('v0', positive=True)
    q = (1-s.exp(-2*t))/4
    den = 1+2*q*v0
    a = s.exp(-t)*a0/den
    v = s.exp(-2*t)*v0/den
    equal('gaussian_mean_initial', a.subs(t, 0), a0)
    equal('gaussian_variance_initial', v.subs(t, 0), v0)
    equal('gaussian_mean_ode', s.diff(a, t), -a-a*v)
    equal('gaussian_variance_ode', s.diff(v, t), -2*v-v*v)
    # Completing the square: the tilted initial x-density has these parameters.
    atilt, vtilt = a0/den, v0/den
    exponent = -(x-a0)**2/(2*v0)-q*x*x+(x-atilt)**2/(2*vtilt)
    equal('gaussian_square_completion_x_independent', s.diff(s.expand(exponent), x), 0)

    output_dir.mkdir(parents=True, exist_ok=True)
    result = {'status': 'PASS', 'check_count': len(CHECKS), 'checks': CHECKS,
              'details': DETAILS, 'python': platform.python_version(), 'sympy': s.__version__,
              'scope': 'Finite exact controls supplement written universal proofs; no kernel or independent-review claim.'}
    (output_dir/'CONTROL_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
    (output_dir/'verification.txt').write_text(f'PASS {len(CHECKS)} exact controls\nPython {platform.python_version()}\nSymPy {s.__version__}\n')
    print(f'PASS {len(CHECKS)} exact controls; output: {output_dir}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    main(parser.parse_args().output_dir.resolve())
