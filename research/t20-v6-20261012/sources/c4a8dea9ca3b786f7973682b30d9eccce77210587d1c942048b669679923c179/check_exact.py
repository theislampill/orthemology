#!/usr/bin/env python3
"""Exact one-step controls, not a general integrator or a formal proof.

Python fractions implement the positive quartic step. SymPy checks polynomial
identities. No floating-point inputs or calculations are used. Output paths are
fresh-only. Inputs and predecessor files are never edited.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys

import sympy as S

BASE = Path(__file__).resolve().parent


def exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, Q)):
        raise TypeError('only integers and fractions.Fraction are accepted')
    return Q(value)


def merge_law(weights, positions):
    if len(weights) != len(positions) or not weights:
        raise ValueError('one position per positive weight is required')
    weights = [exact(w) for w in weights]
    positions = [exact(x) for x in positions]
    if any(w <= 0 for w in weights) or sum(weights) != 1:
        raise ValueError('weights must be positive and sum exactly to one')
    merged = {}
    for w, x in zip(weights, positions):
        merged[x] = merged.get(x, Q(0)) + w
    positions = sorted(merged)
    return [merged[x] for x in positions], positions


def rational_reweight(weights, values, tau):
    weights = [exact(w) for w in weights]
    values = [exact(f) for f in values]
    tau = exact(tau)
    if tau <= 0 or len(weights) != len(values) or not weights:
        raise ValueError('a positive step and matching nonempty lists are required')
    if any(w <= 0 for w in weights) or sum(weights) != 1:
        raise ValueError('weights must be positive and sum exactly to one')
    c = min(values)
    denominators = [1 + tau * (f - c) for f in values]
    unnormalized = [w / d for w, d in zip(weights, denominators)]
    normalizer = sum(unnormalized)
    return [u / normalizer for u in unnormalized], denominators, normalizer


def quartic_rational_step(weights, positions, tau):
    """F=x^4/4, with certified tau <= 1/(6 M^2); duplicate nodes merged."""
    tau = exact(tau)
    if tau <= 0:
        raise ValueError('step must be positive')
    weights, positions = merge_law(weights, positions)
    radius = max(abs(x) for x in positions)
    if radius and tau > 1 / (6 * radius**2):
        raise ValueError('step exceeds the sufficient quartic guard')
    moved = [x - tau * x**3 for x in positions]
    values = [y**4 / 4 for y in moved]
    new_weights, denominators, normalizer = rational_reweight(weights, values, tau)
    return {
        'weights_before': weights, 'positions_before': positions,
        'weights_after': new_weights, 'positions_after': moved,
        'denominators': denominators, 'normalizer': normalizer,
        'radius': radius, 'tau': tau,
        'potential': 'F(x)=x^4/4',
        'reweighting_rule': 'minimum-shift reciprocal, then normalize',
        'injective_domain': [-radius, radius],
    }


def moment(weights, positions, degree):
    return sum(w * x**degree for w, x in zip(weights, positions))


def sym(value):
    value = exact(value)
    return S.Rational(value.numerator, value.denominator)


def run_checks(original_root=None):
    labels = []
    examples = {}

    def ck(label, condition):
        if not bool(condition):
            raise AssertionError(label)
        labels.append(label)

    def zero(label, expression):
        ck(label, S.cancel(S.expand(expression)) == 0)

    def rejects(label, operation):
        try:
            operation()
        except (ValueError, TypeError):
            ck(label, True)
        else:
            ck(label, False)

    bindings = json.loads((BASE / 'INPUT_BINDINGS.json').read_text())
    for entry in bindings:
        digest = hashlib.sha256((BASE / entry['copy']).read_bytes()).hexdigest()
        ck('copied input hash: ' + entry['original'], digest == entry['sha256'])
        if original_root is not None:
            digest = hashlib.sha256((original_root / entry['original']).read_bytes()).hexdigest()
            ck('original input preserved: ' + entry['original'], digest == entry['sha256'])

    # Universal symbolic Dirac identities, no sample-size inference.
    x, b, tau, f, p = S.symbols('x b tau f p', real=True)
    zero('Dirac selection cancels for arbitrary polynomial value', -f*p+f*p)
    m1, m2 = x+tau*b, x*x+2*tau*x*b
    zero('univariate Dirac Euler variance', m2-m1*m1+tau*tau*b*b)
    zero('moved Dirac restores missing second-order moment',
         (x+tau*b)**2-m2-tau*tau*b*b)
    zero('zero drift Euler Dirac unchanged', (m2-m1*m1).subs(b, 0))

    xx = S.Matrix(S.symbols('x0:3', real=True))
    bb = S.Matrix(S.symbols('b0:3', real=True))
    yy = S.Matrix(S.symbols('y0:3', real=True))
    mean = xx+tau*bb
    second = xx*xx.T+tau*(xx*bb.T+bb*xx.T)
    covariance = second-mean*mean.T
    for i in range(3):
        for j in range(3):
            zero(f'Dirac covariance entry {i},{j}', covariance[i, j]+tau*tau*bb[i]*bb[j])
    q = bb.dot(yy-xx)-tau*bb.dot(bb)
    at_x = dict(zip(yy, xx))
    q2 = q*q
    raw = q2.subs(at_x) + tau*sum(bb[i]*S.diff(q2, yy[i]).subs(at_x) for i in range(3))
    zero('multivariate Dirac separating square', raw+tau*tau*bb.dot(bb)**2)

    for step in [Q(1), Q(1, 2), Q(1, 4), Q(1, 24), Q(1, 2**20)]:
        raw_mean, raw_second = 1-step, 1-2*step
        ck(f'rational Dirac negative variance at {step}', raw_second-raw_mean**2 == -step**2 < 0)
    step = Q(1, 4)
    ck('raw potential decrease can accompany invalidity', Q(1, 4)-step == 0 < Q(1, 4))
    ck('positive moved Dirac second moment', (1-step)**2 == Q(9, 16))
    ck('positive moved Dirac quartic energy', (1-step)**4/4 == Q(81, 1024))

    # Explicit multivariate Hermite witness for a three-atom positive law.
    u, v = S.symbols('u v', real=True)
    variables = (u, v)
    nodes = [(S.Integer(0), S.Integer(0)), (S.Integer(1), S.Integer(0)),
             (S.Integer(0), S.Integer(2))]
    weights = [S.Rational(1, 6), S.Rational(1, 3), S.Rational(1, 2)]
    potential = (u*u+v*v)**2/4
    drift = [-S.diff(potential, z) for z in variables]
    evaluate = lambda poly, node: poly.subs(dict(zip(variables, node)))
    values = [evaluate(potential, node) for node in nodes]
    drifts = [S.Matrix([evaluate(comp, node) for comp in drift]) for node in nodes]
    energy = sum(w*f for w, f in zip(weights, values))
    h = S.Rational(1, 24)
    A = [1-h*(f-energy) for f in values]
    ell = u+2*v
    lambdas = [evaluate(ell, node) for node in nodes]
    target = 2
    ej = S.prod((ell-lambdas[i])/(lambdas[target]-lambdas[i])
                for i in range(len(nodes)) if i != target)
    aj = S.Matrix([evaluate(S.diff(ej, z), nodes[target]) for z in variables])
    bj = drifts[target]
    constant = (abs(A[target])+1)/(2*h*bj.dot(bj))
    displacement = S.Matrix(variables)-S.Matrix(nodes[target])
    witness = S.expand(ej**2*(1-(2*aj+constant*bj).dot(displacement)))
    ck('Hermite witness degree bounded by 2r-1', S.Poly(witness, variables).total_degree() <= 5)
    for i, node in enumerate(nodes):
        zero(f'Hermite witness value at {i}', evaluate(witness, node)-int(i == target))
        for k, z in enumerate(variables):
            expected = -constant*bj[k] if i == target else 0
            zero(f'Hermite witness gradient {i},{k}', evaluate(S.diff(witness, z), node)-expected)
    square = S.expand(witness*witness)
    raw_square = sum(weights[i]*(A[i]*evaluate(square, nodes[i])+
                    h*sum(drifts[i][k]*evaluate(S.diff(square, z), nodes[i])
                          for k, z in enumerate(variables))) for i in range(len(nodes)))
    expected = weights[target]*(A[target]-abs(A[target])-1)
    zero('Hermite raw Euler square certificate identity', raw_square-expected)
    ck('Hermite raw Euler square strictly negative', raw_square < 0)
    examples['multivariate_Hermite_certificate'] = {
        'potential': str(potential), 'tau': str(h), 'target': target,
        'q': str(witness), 'q_degree': S.Poly(witness, variables).total_degree(),
        'raw_Euler_q_squared': str(raw_square),
    }

    # All-immobile converse can fail or succeed on the same stationary support.
    # F=(x^2-1)^2 at {0,1}: gradients zero but energies differ.
    e_stationary = Q(1, 2)
    for t, expected_positive in [(Q(1), True), (Q(2), True), (Q(3), False)]:
        masses = [Q(1, 2)*(1-t*(val-e_stationary)) for val in [Q(1), Q(0)]]
        ck(f'immobile signed masses normalized at {t}', sum(masses) == 1)
        ck(f'immobile coefficient positivity criterion at {t}', all(a >= 0 for a in masses) == expected_positive)
    ck('critical gradients vanish at immobile test positions',
       all(4*z*(z*z-1) == 0 for z in [Q(0), Q(1)]))

    # Symbolic exact reweight covariance and sum-of-squares dissipation.
    w, f0, f1, c = S.symbols('w f0 f1 c', real=True)
    d0, d1 = 1+tau*(f0-c), 1+tau*(f1-c)
    Z = w/d0+(1-w)/d1
    before = w*f0+(1-w)*f1
    after = (w*f0/d0+(1-w)*f1/d1)/Z
    zero('rational reweight pairwise dissipation identity',
         before-after-tau*w*(1-w)*(f0-f1)**2/(Z*d0*d1))
    a0, a1 = S.symbols('a0 a1', real=True)
    zero('two-point covariance pair identity',
         w*f0*a0+(1-w)*f1*a1-(w*f0+(1-w)*f1)*(w*a0+(1-w)*a1)
         -w*(1-w)*(f0-f1)*(a0-a1))
    shift = S.symbols('shift', real=True)
    zero('rational constant shift cancels', (1+tau*((f0+shift)-(c+shift)))-d0)

    # Generic first-order jets; the minimum derivative is not required by proof.
    h0, h1, hc, p0, p1, k0, k1 = S.symbols('h0 h1 hc p0 p1 k0 k1', real=True)
    fs = [f0+tau*h0, f1+tau*h1]
    ps = [p0+tau*k0, p1+tau*k1]
    old_weights = [w, 1-w]
    initial_energy = w*f0+(1-w)*f1
    initial_test = w*p0+(1-w)*p1
    expected_drift = w*k0+(1-w)*k1-(w*f0*p0+(1-w)*f1*p1)+initial_energy*initial_test
    for name, factors in [
        ('rational', [1/(1+tau*(fi-c-tau*hc)) for fi in fs]),
        ('exponential', [S.exp(-tau*fi) for fi in fs]),
    ]:
        normalizer = sum(wi*ai for wi, ai in zip(old_weights, factors))
        new_test = sum(wi*ai*pi for wi, ai, pi in zip(old_weights, factors, ps))/normalizer
        zero(f'{name} first-order test consistency', S.diff(new_test, tau).subs(tau, 0)-expected_drift)
        for i in range(2):
            new_mass = old_weights[i]*factors[i]/normalizer
            zero(f'{name} first-order weight {i}',
                 S.diff(new_mass, tau).subs(tau, 0)+old_weights[i]*([f0, f1][i]-initial_energy))

    # Exact application of the guarded quartic step and its rational invariants.
    cases = [
        ('Dirac', [Q(1)], [Q(1)], Q(1, 6)),
        ('two_atoms', [Q(1, 3), Q(2, 3)], [Q(-1), Q(2)], Q(1, 24)),
        ('three_atoms', [Q(1, 5), Q(1, 3), Q(7, 15)], [Q(-2), Q(-1), Q(3, 2)], Q(1, 24)),
        ('tied_energy', [Q(1, 3), Q(2, 3)], [Q(-1), Q(1)], Q(1, 6)),
        ('zero_radius', [Q(1)], [Q(0)], Q(17)),
    ]
    for name, weights, positions, t in cases:
        result = quartic_rational_step(weights, positions, t)
        weights, positions = result['weights_before'], result['positions_before']
        new_weights, moved = result['weights_after'], result['positions_after']
        ds, normalizer, radius = result['denominators'], result['normalizer'], result['radius']
        values = [z**4/4 for z in moved]
        old_e = sum(wi*xi**4/4 for wi, xi in zip(weights, positions))
        transported_e = sum(wi*fi for wi, fi in zip(weights, values))
        new_e = sum(wi*fi for wi, fi in zip(new_weights, values))
        ck(f'{name}: rational positive weights', all(isinstance(wi, Q) and wi > 0 for wi in new_weights))
        ck(f'{name}: exact normalization', sum(new_weights) == 1)
        ck(f'{name}: denominators at least one', all(di >= 1 for di in ds))
        ck(f'{name}: normalizer positive', normalizer > 0)
        ck(f'{name}: actual segments inside certified interval', all(abs(y) <= abs(x) <= radius for x, y in zip(positions, moved)))
        ck(f'{name}: radius guard Hessian factor', 3*t*radius**2 <= Q(1, 2))
        ck(f'{name}: positions distinct', len(set(moved)) == len(positions))
        ck(f'{name}: transport energy nonincrease', transported_e <= old_e)
        ck(f'{name}: reweight energy nonincrease', new_e <= transported_e)
        gap = t/normalizer*sum(weights[i]*weights[j]*(values[i]-values[j])**2/(ds[i]*ds[j])
                               for i in range(len(weights)) for j in range(i+1, len(weights)))
        ck(f'{name}: exact rational dissipation identity', transported_e-new_e == gap)
        ck(f'{name}: strict reweight iff energies differ', (new_e < transported_e) == (len(set(values)) > 1))
        ck(f'{name}: strict transport iff a gradient is nonzero', (transported_e < old_e) == any(x != 0 for x in positions))
        inverse_unnormalized = [vi*di for vi, di in zip(new_weights, ds)]
        recovered = [ui/sum(inverse_unnormalized) for ui in inverse_unnormalized]
        ck(f'{name}: old weights recovered exactly', recovered == weights)
        shifted, _, _ = rational_reweight(weights, [fi-100 for fi in values], t)
        ck(f'{name}: constant-shift invariance including negative values', shifted == new_weights)
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                ck(f'{name}: pairwise no-collision margin {i},{j}',
                   abs(moved[i]-moved[j]) >= Q(1, 2)*abs(positions[i]-positions[j]))
        moments = [moment(new_weights, moved, n) for n in range(9)]
        ck(f'{name}: all retained moments rational', all(isinstance(m, Q) for m in moments))
        H = S.Matrix([[sym(moments[i+j]) for j in range(5)] for i in range(5)])
        V = S.Matrix([[sym(z)**i for z in moved] for i in range(5)])
        ck(f'{name}: exact Gram factorization', H == V*S.diag(*[sym(wi) for wi in new_weights])*V.T)
        ck(f'{name}: exact Hankel rank', H.rank() == len(moved))
        if name == 'three_atoms':
            for size in range(1, 6):
                for indexes in itertools.combinations(range(5), size):
                    ck(f'{name}: principal minor {indexes}', H.extract(indexes, indexes).det() >= 0)
        examples[name] = {
            'tau': str(t), 'positions_before': list(map(str, positions)),
            'potential': result['potential'], 'reweighting_rule': result['reweighting_rule'],
            'injective_domain': list(map(str, result['injective_domain'])),
            'weights_before': list(map(str, weights)), 'positions_after': list(map(str, moved)),
            'weights_after': list(map(str, new_weights)),
            'energies': {'before': str(old_e), 'after_transport': str(transported_e), 'after_reweight': str(new_e)},
            'Hankel_degree_four_rank': int(H.rank()),
            'moments_through_degree_eight': list(map(str, moments)),
        }

    # Ties cause no ambiguity; duplicates aggregate to the same law.
    tied = quartic_rational_step([Q(1, 3), Q(2, 3)], [-1, 1], Q(1, 6))
    ck('tied energies preserve relative masses', tied['weights_before'] == tied['weights_after'])
    duplicated = quartic_rational_step([Q(1, 6), Q(1, 6), Q(2, 3)], [-1, -1, 2], Q(1, 24))
    merged = quartic_rational_step([Q(1, 3), Q(2, 3)], [-1, 2], Q(1, 24))
    ck('duplicate initial labels merged consistently', duplicated == merged)
    zero_duplicate = quartic_rational_step([Q(1, 4), Q(3, 4)], [0, 0], 2)
    ck('zero-radius duplicate law is one stationary atom',
       zero_duplicate['positions_after'] == [Q(0)] and zero_duplicate['weights_after'] == [Q(1)])
    values = [Q(3), Q(3), Q(-2)]
    ws = [Q(1, 6), Q(1, 3), Q(1, 2)]
    vs, _, _ = rational_reweight(ws, values, Q(1, 7))
    ck('equal energies keep their mass ratio under other competition', vs[0]/vs[1] == ws[0]/ws[1])

    # Actual quartic rational-function step derivative, each test fixed.
    # The first of {-1,2} remains the unique lower-energy node near tau=0.
    nodes1d = [S.Integer(-1), S.Integer(2)]
    ws1d = [S.Rational(1, 3), S.Rational(2, 3)]
    new_nodes = [z-tau*z**3 for z in nodes1d]
    new_values = [z**4/4 for z in new_nodes]
    factors = [1/(1+tau*(fi-new_values[0])) for fi in new_values]
    normalizer = sum(wi*ai for wi, ai in zip(ws1d, factors))
    old_energy = sum(wi*z**4/4 for wi, z in zip(ws1d, nodes1d))
    for n in range(9):
        new_moment = sum(wi*ai*z**n for wi, ai, z in zip(ws1d, factors, new_nodes))/normalizer
        old_moment = sum(wi*z**n for wi, z in zip(ws1d, nodes1d))
        generator = sum(wi*(-n*z**(n+2)-z**(n+4)/4) for wi, z in zip(ws1d, nodes1d))+old_energy*old_moment
        zero(f'actual quartic moment consistency degree {n}', S.diff(new_moment, tau).subs(tau, 0)-generator)
    # At an energy tie {-1,1}, the rational reweight remains exactly unchanged.
    for n in range(7):
        expr = S.Rational(1, 3)*(-1+tau)**n+S.Rational(2, 3)*(1-tau)**n
        generator = sum(wi*(-n*z**(n+2)) for wi, z in zip(ws1d, [-1, 1]))
        zero(f'actual tied-minimum consistency degree {n}', S.diff(expr, tau).subs(tau, 0)-generator)

    # Guard boundaries and controls separating positivity/descent/rank.
    quartic_rational_step([Q(1)], [1], Q(1, 6))
    ck('guard equality accepted', True)
    rejects('oversized sufficient guard rejected', lambda: quartic_rational_step([Q(1)], [1], Q(1, 5)))
    rejects('floating step rejected', lambda: quartic_rational_step([Q(1)], [1], 0.1))
    rejects('floating weight rejected', lambda: quartic_rational_step([1.0], [1], Q(1, 6)))
    rejects('floating node rejected', lambda: quartic_rational_step([Q(1)], [1.0], Q(1, 6)))
    rejects('zero step rejected', lambda: quartic_rational_step([Q(1)], [1], 0))
    rejects('non-normalized weights rejected', lambda: quartic_rational_step([Q(1, 2)], [1], Q(1, 6)))
    rejects('nonpositive weight rejected', lambda: quartic_rational_step([Q(0), Q(1)], [0, 1], Q(1, 6)))
    unsafe_position = Q(1)-Q(3)*Q(1)**3
    ck('oversized quartic step can increase energy while remaining a Dirac', unsafe_position == -2 and unsafe_position**4/4 > Q(1, 4))
    # F=x^2/2, tau=1 gives T(x)=0; positive law but rank drops.
    collapsed = [z-Q(1)*z for z in [Q(-1), Q(2)]]
    ck('quadratic tau L equality can collide', len(set(collapsed)) == 1)
    ck('collision still gives a positive law', moment([Q(1, 3), Q(2, 3)], collapsed, 2) == 0)
    # F=x^2/2 at tau=2/L reflects a point with unchanged energy.
    ck('descent endpoint need not be strict', (Q(1)-Q(2)*Q(1))**2/2 == Q(1, 2))
    # A Hessian checked only at start would miss this explicit overshoot.
    ck('overshoot segment exceeds starting-support region', abs(unsafe_position) > Q(1))

    return labels, examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=BASE/'author-run')
    parser.add_argument('--original-root', type=Path)
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error('output directory already exists; supply a fresh path')
    labels, examples = run_checks(args.original_root)
    args.output_dir.mkdir(parents=True)
    report = {
        'status': 'PASS', 'kind': 'author exact algebraic controls; not formal-kernel verification',
        'check_count': len(labels), 'checks': labels, 'examples': examples,
        'arithmetic': 'fractions.Fraction and SymPy exact identities; no floating point',
        'python_version': sys.version.split()[0], 'sympy_version': S.__version__,
        'original_inputs_checked': args.original_root is not None,
    }
    (args.output_dir/'EXACT_CHECKS.json').write_text(json.dumps(report, indent=2)+'\n')
    print(f'PASS: {len(labels)} exact controls; no floating-point calculations.')
    for name in ['Dirac', 'two_atoms', 'three_atoms', 'tied_energy', 'zero_radius']:
        print(name + ': ' + json.dumps(examples[name]['energies']))
    print('Hermite certificate: ' + examples['multivariate_Hermite_certificate']['raw_Euler_q_squared'])


if __name__ == '__main__':
    main()
