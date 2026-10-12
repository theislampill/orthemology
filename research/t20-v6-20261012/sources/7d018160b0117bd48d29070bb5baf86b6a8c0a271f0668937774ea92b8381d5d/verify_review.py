#!/usr/bin/env python3
"""Bounded exact controls for the independent fixed-channel proof review.

Reads the frozen packet; writes only this separate review directory.
Finite tests support the written review and do not prove universal statements.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'repeatable-channel-constraints-20261010'
EXPECTED_RESULT = '8542fbf86cc2914790bfd0fdcd22920bae8fee9569927524df4e2af3ec527336'


def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def law(*items):
    return tuple(F(x) for x in items)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def update(p, likelihood):
    assert len(p) == len(likelihood)
    weight = dot(p, likelihood)
    return weight, None if weight == 0 else tuple(p[i]*likelihood[i]/weight for i in range(len(p)))


def channel_valid(K):
    assert K and K[0]
    assert all(len(row) == len(K[0]) for row in K)
    assert all(v >= 0 for row in K for v in row)
    assert all(sum(row[i] for row in K) == 1 for i in range(len(K[0])))


def mixture(t, a, b):
    return tuple(t*x+(1-t)*y for x, y in zip(a, b))


def rank(rows):
    A = [list(row) for row in rows]
    piv = 0
    for col in range(len(A[0])):
        pick = next((j for j in range(piv, len(A)) if A[j][col]), None)
        if pick is None:
            continue
        A[piv], A[pick] = A[pick], A[piv]
        c = A[piv][col]
        A[piv] = [x/c for x in A[piv]]
        for j in range(len(A)):
            if j != piv:
                c = A[j][col]
                A[j] = [x-c*y for x, y in zip(A[j], A[piv])]
        piv += 1
        if piv == len(A):
            break
    return piv


def word_row(K, word):
    row = [F(1)]*len(K[0])
    for y in word:
        row = [a*b for a, b in zip(row, K[y])]
    return tuple(row)


def main():
    frozen = sorted(p for p in SOURCE.iterdir() if p.is_file())
    bindings = json.loads((SOURCE/'INPUT_BINDINGS.json').read_text())['inputs']
    inherited = [(SOURCE/e['source_path']).resolve() for e in bindings]
    all_inputs = frozen + inherited
    before = {str(p.relative_to(HERE.parent)): digest(p) for p in all_inputs}
    assert digest(SOURCE/'RESULT.md')['sha256'] == EXPECTED_RESULT
    manifest = json.loads((SOURCE/'MANIFEST.json').read_text())
    for entry in manifest['files']:
        assert digest(SOURCE/entry['path']) == {'bytes': entry['bytes'], 'sha256': entry['sha256']}
    for entry, path in zip(bindings, inherited):
        assert digest(path) == {'bytes': entry['bytes'], 'sha256': entry['sha256']}

    # Execute inspected author functions, deliberately not main(), which writes
    # CHECK_RESULTS.json in the frozen directory. exec creates no __pycache__.
    scope = {'__name__': 'review_read_only_import', '__file__': str(SOURCE/'verify.py')}
    exec(compile((SOURCE/'verify.py').read_text(), str(SOURCE/'verify.py'), 'exec'), scope)
    names = ['globally_stable_inequality', 'curved_local_not_global', 'zero_likelihoods',
             'minimal_hull', 'topology_and_convexity', 'single_likelihood',
             'copied_vs_fresh', 'changing_state', 'block_indicators']
    for name in names:
        scope[name]()
    assert scope['unchanged_inputs']() == 8
    saved = json.loads((SOURCE/'CHECK_RESULTS.json').read_text())
    rerun = json.loads(json.dumps(scope['RESULTS'], default=str))
    assert rerun == saved['results']
    results = []

    # 27 normalized nonnegative channels, each with one impossible outcome;
    # seven nonempty uniform supports per channel. No convex-set enumeration.
    count = 0
    for row in product([F(0), F(1, 2), F(1)], repeat=3):
        K = [row, tuple(1-x for x in row), law(0, 0, 0)]
        channel_valid(K)
        for mask in range(1, 8):
            support = [i for i in range(3) if mask & (1 << i)]
            p = tuple(F(int(i in support), len(support)) for i in range(3))
            branches = [update(p, r) for r in K]
            assert sum(a for a, q in branches) == 1
            assert tuple(sum(a*q[i] for a, q in branches if a) for i in range(3)) == p
            all_fixed = all(q == p for a, q in branches if a)
            one_block = len({tuple(r[i] for r in K) for i in support}) == 1
            assert all_fixed == one_block
            assert branches[-1] == (F(0), None)
            count += 1
    assert update(law(1), law(0)) == (F(0), None)
    assert update(law(1), law(1)) == (F(1), law(1))
    results.append({'control': 'Bayes barycenter and singleton equal-column criterion', 'cases': count,
                    'status': 'PASS', 'extra': 'n=1 and impossible branches checked'})

    # Explicit inverse for positive block-constant likelihoods, with two
    # nontrivial within-block conditional laws. Endpoints are included.
    u, v = law('2/3', '1/3', 0, 0), law(0, 0, '1/4', '3/4')
    K = [law('1/5', '1/5', '3/4', '3/4'), law('4/5', '4/5', '1/4', '1/4')]
    channel_valid(K)
    tests = 0
    for t in [F(0), F(1, 7), F(1, 2), F(5, 6), F(1)]:
        q = mixture(t, u, v)
        for L in K + [law(2, 2, 5, 5)]:
            inverse = update(q, tuple(1/x for x in L))[1]
            assert inverse == mixture(sum(inverse[:2]), u, v)
            assert update(inverse, L)[1] == q
            image = update(q, L)[1]
            assert image == mixture(sum(image[:2]), u, v)
            tests += 1
    results.append({'control': 'Minimal-hull block decomposition and positive surjectivity',
                    'status': 'PASS', 'cases': tests})

    K0 = [law(1, 1, '1/2', '1/2'), law(0, 0, '1/2', '1/2')]
    channel_valid(K0)
    assert update(u, K0[1]) == (F(0), None)
    assert update(v, K0[1])[1] == v
    assert update(mixture(F(1, 2), u, v), K0[1])[1] == v
    results.append({'control': 'A nonnegative outcome has a proper image and an undefined boundary',
                    'status': 'PASS'})

    # Four distinct three-outcome columns; no single outcome row separates all
    # four, and the first column is duplicated at two target states.
    columns = [law('1/6', '1/6', '2/3'), law('1/6', '1/3', '1/2'),
               law('1/3', '1/6', '1/2'), law('1/3', '1/3', '1/3')]
    block_of = [0, 0, 1, 2, 3]
    K = [tuple(columns[j][y] for j in block_of) for y in range(3)]
    channel_valid(K)
    assert all(len(set(c[y] for c in columns)) < 4 for y in range(3))
    indicators = []
    for j in range(4):
        f = [F(1)]*5
        for k in range(4):
            if j == k:
                continue
            y = next(y for y in range(3) if columns[j][y] != columns[k][y])
            f = [x*(K[y][i]-columns[k][y])/(columns[j][y]-columns[k][y])
                 for i, x in enumerate(f)]
        assert f == [F(int(b == j)) for b in block_of]
        indicators.append(f)
    p = law('1/5', '1/10', '1/5', '1/4', '1/4')
    q = law('1/10', '1/5', '1/5', '1/4', '1/4')
    assert p != q
    recovered = [dot(p, f) for f in indicators]
    assert recovered == [F(3, 10), F(1, 5), F(1, 4), F(1, 4)]
    rows = []
    dimensions = []
    for length in range(4):
        for word in product(range(3), repeat=length):
            f = word_row(K, word)
            assert dot(p, f) == dot(q, f)
            rows.append(f)
        dimensions.append(rank(rows))
    assert dimensions == [1, 3, 4, 4]
    results.append({'control': 'Multivariate block interpolation and continuation span', 'status': 'PASS',
                    'word_rows': len(rows), 'span_dimensions': dimensions, 'block_masses': recovered})

    K = [law('1/4', '1/2', '3/4'), law('3/4', '1/2', '1/4')]
    p, q = law('1/4', '1/2', '1/4'), law('3/8', '1/4', '3/8')
    assert [dot(p, r) for r in K] == [dot(q, r) for r in K] == [F(1, 2), F(1, 2)]
    second = word_row(K, (0, 0))
    assert dot(p, second) == F(9, 32)
    assert dot(q, second) == F(19, 64)
    results.append({'control': 'Distinct columns do not identify an arbitrary prior from a one-shot law',
                    'status': 'PASS', 'p_plus_plus': dot(p, second), 'q_plus_plus': dot(q, second)})

    K = [law('3/4', '1/4'), law('1/4', '3/4')]
    p = law('1/2', '1/2')
    cases = 0
    for length in range(6):
        for word in product(range(2), repeat=length):
            alpha, q = update(p, word_row(K, word))
            assert alpha > 0 and all(x > 0 for x in q)
            exponent = word.count(0)-word.count(1)
            assert q[0]/q[1] == F(3)**exponent
            assert q != law('2/5', '3/5')
            cases += 1
    results.append({'control': 'Finite positive words preserve support and the exact odds lattice',
                    'status': 'PASS', 'word_cases': cases, 'maximum_length': 5})

    centre = law('1/3', '1/3', '1/3')
    L = law('3/4', '1/4', '1/2')
    first = update(centre, L)[1]
    fresh = update(first, L)[1]
    copied = update(first, law(1, 1, 1))[1]
    assert sum((x-y)**2 for x, y in zip(first, centre)) == F(1, 18)
    assert sum((x-y)**2 for x, y in zip(fresh, centre)) == F(1, 6)
    assert copied == first != fresh
    results.append({'control': 'Independent disk and copied-receipt arithmetic', 'status': 'PASS'})

    after = {str(p.relative_to(HERE.parent)): digest(p) for p in all_inputs}
    assert before == after
    payload = {'status': 'PASS', 'frozen_result_sha256': EXPECTED_RESULT,
               'source_packet_files_unchanged': len(frozen), 'inherited_inputs_unchanged': len(inherited),
               'author_control_groups_replayed': len(names), 'author_recorded_results_exactly_reproduced': True,
               'independent_control_groups': len(results), 'independent_controls': results,
               'scope': 'Ordinary AI proof review and bounded exact controls; no universal proof by enumeration.'}
    (HERE/'CHECK_RESULTS.json').write_text(json.dumps(payload, indent=2, default=str)+'\n')
    (HERE/'INPUT_HASHES.json').write_text(json.dumps({'unchanged_before_after': True, 'files': before}, indent=2)+'\n')
    print(json.dumps(payload, indent=2, default=str))


if __name__ == '__main__':
    main()
