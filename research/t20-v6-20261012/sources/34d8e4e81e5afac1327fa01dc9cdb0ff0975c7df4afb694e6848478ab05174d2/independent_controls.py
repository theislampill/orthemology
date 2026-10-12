#!/usr/bin/env python3
"""Independent exact controls; imports no author code and writes off-packet."""
from pathlib import Path
from itertools import product
import argparse
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHOR = ROOT / 'completion-bayes-commutation-20261010'
PINS = {
    'RESULT.md': '3ae148739d915bcc9dc8d59c934b3a33ff46c79ef34407e4b47c1432ecef86a2',
    'MANIFEST.json': '6ac3dfba213dfa10b606c8b6e16287568222cc8433923a638dc243226c337d53',
}
checks = []


def check(name, condition, detail=None):
    assert condition, name
    row = {'name': name, 'passed': True}
    if detail is not None:
        row['detail'] = detail
    checks.append(row)
    print(f'PASS {len(checks):02}: {name}', flush=True)


def norm(p):
    p = s.Matrix(p)
    return p / sum(p)


def bayes(p, likelihood):
    weighted = p.multiply_elementwise(s.Matrix(likelihood))
    return norm(weighted) if sum(weighted) else None


def equal(a, b):
    return all(s.expand(x) == 0 for x in a - b)


def algebra(M, likelihood):
    return M.col_join(M * s.diag(*likelihood)).rank() == M.rank()


def posterior_identity(M, pnum, qnum, likelihood, variables):
    D = s.diag(*likelihood)
    p_mass, q_mass = sum(D * pnum), sum(D * qnum)
    numerators = (M * D * pnum) * q_mass - (M * D * qnum) * p_mass
    return all(s.Poly(s.expand(e), *variables).is_zero for e in numerators)


def verify_bindings():
    for filename, digest in PINS.items():
        assert hashlib.sha256((AUTHOR / filename).read_bytes()).hexdigest() == digest
    manifest = json.loads((AUTHOR / 'MANIFEST.json').read_text())
    for row in manifest['files']:
        data = (AUTHOR / row['path']).read_bytes()
        assert len(data) == row['bytes']
        assert hashlib.sha256(data).hexdigest() == row['sha256']
    bindings = json.loads((AUTHOR / 'INPUT_BINDINGS.json').read_text())
    for row in bindings['inputs']:
        snapshot = (AUTHOR / row['snapshot_path']).read_bytes()
        assert len(snapshot) == row['bytes']
        assert hashlib.sha256(snapshot).hexdigest() == row['sha256']
    return len(manifest['files']), len(bindings['inputs'])


def run():
    check('frozen author pins, 14 manifest members, and 6 bound input snapshots match', verify_bindings() == (14, 6))

    # Non-simplex square; vertex (0,0) has two atoms. Its aggregate
    # reference is (5,3,3,5), deliberately nonuniform AND nonproduct.
    M = s.Matrix([[1] * 5, [0, 0, 0, 1, 1], [0, 0, 1, 0, 1]])
    reference = s.Matrix([1, 4, 3, 3, 5])
    U, V = s.symbols('U V', positive=True)
    T, H = s.symbols('T H', real=True)
    qnum = s.Matrix([1, 4, 3 * V, 3 * U, 5 * U * V])
    k_dup = s.Matrix([1, -1, 0, 0, 0])
    k_square = s.Matrix([1, 0, -1, -1, 1])
    pnum = qnum + T * k_dup + H * k_square
    check('independent nonproduct reference and complete kernel parameterization',
          5 * 5 != 3 * 3 and equal(M * pnum, M * qnum)
          and s.Matrix.hstack(k_dup, k_square).rank() == 5 - M.rank())

    # Direct closure membership for this model follows from duplicate
    # proportions, square odds, and explicit square supports. This is
    # not an invocation of the theorem being reviewed.
    vertex_supports = [{0, 1}, {2}, {3}, {4}]
    proper_supports = vertex_supports + [{0, 1, 2}, {0, 1, 3}, {2, 4}, {3, 4}]
    accepted = stabilized = declined = 0
    accepted_arrays = []
    for likelihood in product((0, 1, 2), repeat=5):
        if not any(likelihood):
            continue
        support = {i for i, value in enumerate(likelihood) if value}
        full = len(support) == 5
        saturated = full or support in proper_supports
        duplicate_ratio = not ({0, 1} & support) or likelihood[0] == likelihood[1]
        odds = not full or likelihood[0] * likelihood[4] == likelihood[2] * likelihood[3]
        rhs_in_model = saturated and duplicate_ratio and odds
        moments_agree = posterior_identity(M, pnum, qnum, likelihood, (U, V, T, H))
        direct_commutation = rhs_in_model and moments_agree
        in_algebra = algebra(M, likelihood)
        vertex_exception = support in vertex_supports and len({likelihood[i] for i in support}) == 1
        assert direct_commutation == (in_algebra or vertex_exception), likelihood
        assert in_algebra == (len(set(likelihood)) == 1), likelihood
        if direct_commutation:
            accepted_arrays.append(list(likelihood))
        accepted += direct_commutation
        stabilized += in_algebra
        declined += not direct_commutation
    check('242 likelihoods: exact symbolic commutation on a nonuniform nonproduct duplicate square',
          (accepted, stabilized, declined) == (10, 2, 232),
          {'likelihood_arrays': 242, 'commuting': accepted, 'stabilizing': stabilized,
           'noncommuting': declined, 'accepted_arrays': accepted_arrays,
           'method': 'Independent duplicate-ratio/odds/support membership and polynomial posterior-record identities over a complete positive-fibre parameterization'})

    q = norm(reference)
    anti = s.Matrix([0, 0, s.Rational(1, 2), s.Rational(1, 2), 0])
    diagonal = s.Matrix([s.Rational(1, 2), 0, 0, 0, s.Rational(1, 2)])
    vertex = s.Matrix([1, 1, 0, 0, 0])
    vertex_completion = s.Matrix([s.Rational(1, 5), s.Rational(4, 5), 0, 0, 0])
    check('nonuniform branch invention concerns actual-law feasibility, while another same-record law permits the event',
          equal(M * anti, M * q) and equal(M * diagonal, M * q)
          and (vertex.T * anti)[0] == 0 and (vertex.T * diagonal)[0] == s.Rational(1, 2)
          and (vertex.T * q)[0] == s.Rational(5, 16))
    check('possible boundary vertex branch commutes while completion restores absent duplicates',
          bayes(diagonal, vertex) == s.Matrix([1, 0, 0, 0, 0])
          and bayes(q, vertex) == vertex_completion
          and equal(M * bayes(diagonal, vertex), M * vertex_completion))
    p_positive = q + s.Rational(1, 64) * k_square
    check('positive-input branch mass need not agree in the commuting vertex exception',
          min(p_positive) > 0 and equal(M * p_positive, M * q)
          and (vertex.T * p_positive)[0] == s.Rational(21, 64)
          and (vertex.T * q)[0] == s.Rational(20, 64))
    check('unequal and partial duplicate weights fail despite identical supported columns',
          bayes(q, [1, 2, 0, 0, 0]) == s.Matrix([s.Rational(1, 9), s.Rational(8, 9), 0, 0, 0])
          and bayes(q, [1, 2, 0, 0, 0]) != vertex_completion
          and bayes(q, [1, 0, 0, 0, 0]) != vertex_completion)
    local = s.Matrix([0, 0, 0, 1, 1])
    local_posterior = bayes(p_positive, local)
    local_closed = bayes(q, local)
    check('nonuniform local facial likelihood preserves mass and the closed model but fails arbitrary-input commutation',
          (local.T * p_positive)[0] == (local.T * q)[0]
          and local_posterior != local_closed
          and (M * local_posterior)[2] != (M * local_closed)[2]
          and all(local_posterior[i] == 0 for i in (0, 1, 2)))

    # Interior duplicate support: even the entire fibre is not a face.
    M_mid = s.Matrix([[1] * 4, [-1, 0, 0, 1]])
    mid_reference = norm([2, 3, 5, 2])
    mid_selected = bayes(mid_reference, [0, 1, 1, 0])
    check('full duplicate fibre at a nonvertex is not a commuting exception',
          M_mid[:, [1, 2]].rank() == 1
          and equal(M_mid * mid_selected, M_mid * mid_reference)
          and mid_selected != mid_reference
          and mid_selected == s.Matrix([0, s.Rational(3, 8), s.Rational(5, 8), 0]))

    # d=0: R is constant, so direct law equality is simple and exact.
    r0 = norm([1, 3, 5])
    d0_accepted = 0
    for likelihood in product((0, 1, 2), repeat=3):
        if not any(likelihood):
            continue
        direct = bayes(r0, likelihood) == r0
        assert direct == (len(set(likelihood)) == 1)
        d0_accepted += direct
    check('d=0 sweep: only full-support constant likelihoods commute',
          d0_accepted == 2, {'likelihood_arrays': 26, 'commuting': 2})
    check('zero likelihood has no normalized branch and remains outside the nonzero theorem',
          bayes(r0, [0, 0, 0]) is None)

    # Nonsimplex square pyramid with a duplicated apex. The complement
    # really is an entire face, so its vertex exception lies in A(V).
    M_pyramid = s.Matrix([[1] * 6, [0, 1, 0, 1, 0, 0],
                          [0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1]])
    apex = s.Matrix([0, 0, 0, 0, 1, 1])
    W = s.symbols('W', positive=True)
    a, b = s.symbols('a b', nonnegative=True)
    pqnum = s.Matrix([1, 2 * U, 3 * V, 7 * U * V, 5 * W, 11 * W])
    ppnum = pqnum + T * s.Matrix([1, -1, -1, 1, 0, 0]) + H * s.Matrix([0, 0, 0, 0, 1, -1])
    likelihood = s.Matrix([a, a, a, a, b, b])
    check('nonsimplex pyramid has a retained stabilizing duplicate-apex indicator',
          M_pyramid.rank() == 4 and M_pyramid[:, :4].rank() == 3
          and M_pyramid.T * s.Matrix([0, 0, 0, 1]) == apex
          and algebra(M_pyramid, apex))
    check('nonsimplex-pyramid stabilizer has symbolic posterior descent and exact branch mass, including zero block limits',
          equal(M_pyramid * ppnum, M_pyramid * pqnum)
          and posterior_identity(M_pyramid, ppnum, pqnum, likelihood, (U, V, W, T, H, a, b))
          and s.expand(sum(likelihood.multiply_elementwise(ppnum - pqnum))) == 0
          and algebra(M_pyramid, [0, 0, 0, 0, 2, 2])
          and algebra(M_pyramid, [2, 2, 2, 2, 0, 0]))

    # All nonempty supports of the five-atom square: explicit minimal
    # faces via active coordinate bounds contain every original atom.
    states = [(0, 0), (0, 0), (0, 1), (1, 0), (1, 1)]
    branches = 0
    for weights in product((0, 1), repeat=5):
        if not any(weights):
            continue
        p = norm(weights)
        means = [sum(p[i] * states[i][j] for i in range(5)) for j in range(2)]
        completion_support = {i for i, state in enumerate(states)
                              if all(means[j] not in (0, 1) or state[j] == means[j] for j in range(2))}
        support = {i for i, value in enumerate(weights) if value}
        assert support <= completion_support
        for event in product((0, 1), repeat=5):
            if not any(event):
                continue
            actual = any(event[i] and i in support for i in range(5))
            completed = any(event[i] and i in completion_support for i in range(5))
            assert not actual or completed
            branches += 1
    check('all 961 duplicate-square support/event pairs preserve every actual possible branch', branches == 961)
    check('frozen author bytes and direct snapshots remain unchanged after review controls', verify_bindings() == (14, 6))
    result = {'status': 'PASS', 'scope': 'Independent finite symbolic/rational controls, not formal proof or field novelty.',
              'assertion_groups': len(checks), 'author_pins': PINS, 'checks': checks}
    print(f'PASS: {len(checks)} independent assertion groups')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'REVIEW_CONTROLS.json').write_text(json.dumps(result, indent=2) + '\n')
