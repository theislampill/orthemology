#!/usr/bin/env python3
"""Four discriminating exact reviewer controls; no author implementation imported."""
from fractions import Fraction as R
from pathlib import Path
import json


def v(*xs):
    return tuple(R(x) for x in xs)


def inspect(p, rows):
    n = len(p)
    assert sum(p) == 1 and all(x >= 0 for x in p)
    assert rows and all(len(row) == n for row in rows)
    assert all(0 <= x <= 1 for row in rows for x in row)
    assert all(sum(row[i] for row in rows) == 1 for i in range(n))
    joint = tuple(tuple(p[i] * row[i] for i in range(n)) for row in rows)
    weights = tuple(sum(row) for row in joint)
    posteriors = tuple(tuple(x / a for x in row) if a else None
                       for a, row in zip(weights, joint))
    assert all(sum(a * q[i] for a, q in zip(weights, posteriors) if a) == p[i]
               for i in range(n))
    return weights, posteriors, joint


def all_positive(rows):
    return all(x > 0 for row in rows for x in row)


def serial(x):
    if isinstance(x, R):
        return str(x)
    if isinstance(x, dict):
        return {k: serial(y) for k, y in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(y) for y in x]
    return x


def main():
    findings = []
    # C={(t,1-t):0<t<=3/4} is convex, nonclosed. Its included endpoint
    # is reached by an all-positive channel from an interior prior.
    p, q, r = v('1/2', '1/2'), v('3/4', '1/4'), v('3/8', '5/8')
    rows = (v('1/2', '1/6'), v('1/2', '5/6'))
    weights, posteriors, _ = inspect(p, rows)
    assert weights == v('1/3', '2/3') and posteriors == (q, r)
    assert all_positive(rows)
    member = lambda x: 0 < x[0] <= R(3, 4) and sum(x) == 1
    assert all(member(x) for x in posteriors)
    assert not member(v(0, 1))  # Closure is not admissibility.
    # At q (the included extreme endpoint), choosing p as a branch would
    # force the residual beyond C. The report gives the all-weight argument.
    alpha = R(1, 3)
    residual = tuple((x - alpha*y)/(1-alpha) for x, y in zip(q, p))
    assert residual == v('7/8', '1/8') and not member(residual)
    findings.append({'name': 'nonclosed_C_boundary_positive_reachability',
                     'weights': weights, 'posteriors': posteriors,
                     'extreme_endpoint_residual_outside_C': residual})

    # Distinct completions on a zero-prior state do not change supported
    # joint law. A third row can exist but have zero probability at p.
    p = v('1/2', '1/2', 0)
    positive_a = (v('1/4', '3/4', '2/7'), v('3/4', '1/4', '5/7'))
    positive_b = (v('1/4', '3/4', '5/11'), v('3/4', '1/4', '6/11'))
    aa, ab = inspect(p, positive_a), inspect(p, positive_b)
    assert aa == ab and all_positive(positive_a) and all_positive(positive_b)
    with_null = (v('1/4', '3/4', '1/7'), v('3/4', '1/4', '2/7'), v(0, 0, '4/7'))
    aw, aq, aj = inspect(p, with_null)
    assert aw == v('1/2', '1/2', 0) and aq[:2] == aa[1] and aq[2] is None
    assert aj[:2] == aa[2] and aj[2] == v(0, 0, 0)
    findings.append({'name': 'arbitrary_off_support_and_zero_outcome',
                     'positive_completion_weights': aa[0], 'posteriors': aq})

    # A variable-depth tree reaches an extreme support face, stops on the
    # first branch, and continues uninformatively on the other branch.
    root = (v(1, 0, '2/5'), v(0, 1, '3/5'))
    root_w, root_q, _ = inspect(p, root)
    second = (v('3/7', '1/4', '2/3'), v('4/7', '3/4', '1/3'))
    second_w, second_q, _ = inspect(root_q[1], second)
    assert second_w == v('1/4', '3/4') and second_q == (root_q[1], root_q[1])
    flat = (root[0],) + tuple(tuple(root[1][i]*row[i] for i in range(3)) for row in second)
    fw, fq, _ = inspect(p, flat)
    assert fw == v('1/2', '1/8', '3/8')
    assert fq == (v(1, 0, 0), v(0, 1, 0), v(0, 1, 0))
    assert all(q[2] == 0 for q in fq)
    findings.append({'name': 'variable_depth_flattening_with_support_loss',
                     'flattened_rows': flat, 'weights': fw, 'posteriors': fq})

    # Literal transcription of the packet's displayed second-stage kernels,
    # rather than rerunning its posterior-first witness generator.
    p = v('1/2', '1/4', '1/4')
    first = (v('1/2', '1/4', '3/4'), v('1/2', '3/4', '1/4'))
    seconds = ((v('1/2', '1/4', '7/12'), v('1/2', '3/4', '5/12')),
               (v('1/2', '5/12', '3/4'), v('1/2', '7/12', '1/4')))
    first_w, first_q, _ = inspect(p, first)
    flat = []
    for first_row, current, rows in zip(first, first_q, seconds):
        sw, sq, _ = inspect(current, rows)
        assert sw == v('1/2', '1/2') and all_positive(rows)
        assert all(q[0] == R(1, 2) for q in sq)
        flat += [tuple(x*y for x, y in zip(first_row, row)) for row in rows]
    fw, fq, _ = inspect(p, tuple(flat))
    assert fw == v('1/4', '1/4', '1/4', '1/4')
    assert fq == (v('1/2', '1/16', '7/16'), v('1/2', '3/16', '5/16'),
                  v('1/2', '5/16', '3/16'), v('1/2', '7/16', '1/16'))
    findings.append({'name': 'literal_two_stage_witness', 'weights': fw, 'posteriors': fq})

    result = {'status': 'PASS', 'control_groups': len(findings),
              'scope': 'Four fixed exact reviewer controls; not a universal proof or large enumeration.',
              'results': findings}
    Path(__file__).with_name('INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(serial(result), indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'control_groups': len(findings)}, sort_keys=True))


if __name__ == '__main__':
    main()
