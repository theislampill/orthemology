#!/usr/bin/env python3
"""Exact finite controls for the fixed-prior constrained-splitting note.

Standard library only. These finite checks supplement, not replace, the proofs.
Run in any working directory: python3 /path/to/verify.py.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


def vec(*xs):
    return tuple(F(x) for x in xs)


def mix(a, q, r):
    return tuple(a * x + (1 - a) * y for x, y in zip(q, r))


def bary(weights, qs):
    return tuple(sum(a * q[i] for a, q in zip(weights, qs)) for i in range(len(qs[0])))


def law(p):
    return all(x >= 0 for x in p) and sum(p) == 1


def support(p):
    return tuple(i for i, x in enumerate(p) if x > 0)


def channel(p, weights, qs):
    assert law(p) and all(law(q) for q in qs)
    assert len(weights) == len(qs) and all(a > 0 for a in weights)
    assert sum(weights) == 1 and bary(weights, qs) == p
    # Off-support columns are arbitrary stochastic columns; use positive weights.
    k = tuple(tuple(a * q[i] / p[i] if p[i] else a for i in range(len(p)))
              for a, q in zip(weights, qs))
    assert all(sum(row[i] for row in k) == 1 for i in range(len(p)))
    assert all(0 <= x <= 1 for row in k for x in row)
    for a, q, row in zip(weights, qs, k):
        aa, qq = posterior(p, row)
        assert aa == a and qq == q
    return k


def posterior(p, likelihood):
    z = sum(x * y for x, y in zip(p, likelihood))
    assert z > 0
    return z, tuple(x * y / z for x, y in zip(p, likelihood))


def positive(k):
    return all(x > 0 for row in k for x in row)


def in_fixed_mass(q):
    return law(q) and q[0] == F(1, 2)


def serializable(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {k: serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [serializable(x) for x in obj]
    return obj


def main():
    groups = []
    p = vec('1/2', '1/4', '1/4')
    q_plus = vec('1/2', '1/8', '3/8')
    q_minus = vec('1/2', '3/8', '1/8')
    half = (F(1, 2), F(1, 2))
    k = channel(p, half, (q_plus, q_minus))
    assert k == (vec('1/2', '1/4', '3/4'), vec('1/2', '3/4', '1/4'))
    assert positive(k) and all(in_fixed_mass(q) for q in (q_plus, q_minus))
    groups.append({'name': 'inherited_actual_prior_fixed_mass', 'prior': p,
                   'channel_rows': k, 'posteriors': (q_plus, q_minus), 'weights': half})

    # The homogenized equality is proportional to (1,-1,-1).
    # Its first pivot connects to both free coordinates: all graph labels agree
    # for any globally preserving likelihood. These actual likelihoods do not.
    assert all(not (row[0] == row[1] == row[2]) for row in k)
    other = vec('1/2', '1/2', 0)
    _, other_q = posterior(other, k[0])
    assert other_q == vec('2/3', '1/3', 0) and not in_fixed_mass(other_q)
    _, repeated = posterior(q_plus, k[0])
    assert repeated == vec('4/9', '1/18', '1/2') and not in_fixed_mass(repeated)
    groups.append({'name': 'global_and_repeated_failure', 'other_prior': other,
                   'other_posterior': other_q, 'repeated_plus': repeated})

    # A two-step adaptive continuation stays feasible by changing the declared
    # second kernel with the observed first receipt. This is not a fixed-channel
    # repetition or a statement that the kernels are physically available.
    leaves, transcript_rows, node_rows = [], [], []
    for first_q, first_row in zip((q_plus, q_minus), k):
        t = first_q[1]
        d = min(t, F(1, 2) - t) / 2
        next_qs = (vec(F(1, 2), t - d, F(1, 2) - t + d),
                   vec(F(1, 2), t + d, F(1, 2) - t - d))
        next_k = channel(first_q, half, next_qs)
        assert positive(next_k) and all(in_fixed_mass(q) for q in next_qs)
        assert next_k != k
        node_rows.append(next_k)
        for q, row in zip(next_qs, next_k):
            transcript = tuple(x * y for x, y in zip(first_row, row))
            z, actual_q = posterior(p, transcript)
            assert z == F(1, 4) and actual_q == q
            leaves.append(q)
            transcript_rows.append(transcript)
    assert bary((F(1, 4),) * 4, leaves) == p
    assert channel(p, (F(1, 4),) * 4, leaves) == tuple(transcript_rows)
    groups.append({'name': 'adaptive_two_stage_and_flattening', 'second_kernels': node_rows,
                   'leaf_posteriors': leaves, 'leaf_weights': (F(1, 4),) * 4,
                   'flattened_channel': transcript_rows})

    # General asymmetric segment with boundary endpoints and an unused state.
    a, b = vec('1/2', '1/2', 0, 0), vec('1/2', 0, '1/2', 0)
    lam, shrink = F(2, 3), F(1, 3)
    pp = mix(lam, a, b)
    original = channel(pp, (lam, 1-lam), (a, b))
    assert not positive(original)
    aa, bb = mix(shrink, a, pp), mix(shrink, b, pp)
    kk = channel(pp, (lam, 1-lam), (aa, bb))
    assert positive(kk) and aa != bb and support(aa) == support(bb) == support(pp)
    assert (kk[0][3], kk[1][3]) == (lam, 1-lam)
    groups.append({'name': 'asymmetric_positive_shrink_and_off_support', 'prior': pp,
                   'original_posteriors': (a, b), 'shrunken_posteriors': (aa, bb), 'channel': kk})

    # Exact single-posterior reachability: initial residual has a zero coordinate;
    # lowering its outcome weight makes both posteriors have the prior support.
    pp = vec('1/2', '1/4', '1/4')
    qq, rr = vec('1/2', '1/8', '3/8'), vec('1/2', '1/2', 0)
    lam0, lam1 = F(2, 3), F(1, 3)
    assert mix(lam0, qq, rr) == pp
    rr1 = tuple((x-lam1*y)/(1-lam1) for x, y in zip(pp, qq))
    assert rr1 == vec('1/2', '5/16', '3/16')
    assert positive(channel(pp, (lam1, 1-lam1), (qq, rr1)))
    groups.append({'name': 'strict_individual_reachability_lower_weight', 'selected': qq,
                   'original_residual': rr, 'positive_residual': rr1})

    # Minimal face is stricter than the ambient support stratum. At the lower
    # endpoint of C={q1>=1/2} in Delta_2, a favourable individual branch stays in
    # C, but its complementary branch must leave C if the experiment informs X.
    pp, lp, lm = vec('1/2', '1/2'), vec('3/4', '1/4'), vec('1/4', '3/4')
    _, good = posterior(pp, lp)
    _, bad = posterior(pp, lm)
    assert good[0] >= F(1, 2) and bad[0] < F(1, 2)
    assert support(good) == support(pp)
    for weight in (F(1, 10), F(1, 4), F(1, 2)):
        residual = tuple((x-weight*y)/(1-weight) for x, y in zip(pp, good))
        assert residual[0] < F(1, 2)
    groups.append({'name': 'complete_experiment_not_one_favourable_branch',
                   'extreme_prior': pp, 'feasible_branch': good, 'infeasible_branch': bad})

    # A simplex boundary posterior is reachable by a nonnegative channel but
    # not by any all-positive likelihood on the current prior support.
    pp = vec('1/2', '1/2', 0)
    aa, bb = vec(1, 0, 0), vec(0, 1, 0)
    kk = channel(pp, half, (aa, bb))
    assert not positive(kk) and kk[0][2] == kk[1][2] == F(1, 2)
    groups.append({'name': 'general_vs_strict_support_reachability', 'channel': kk})

    # Exact positive segment controls on all 19 selected interior priors;
    # the same construction lies in the open segment, so closedness is unused.
    grid_count = 0
    for j in range(1, 20):
        t = F(j, 40)
        pp = vec(F(1, 2), t, F(1, 2)-t)
        d = min(t, F(1, 2)-t) / 2
        qs = (vec(F(1, 2), t-d, F(1, 2)-t+d),
              vec(F(1, 2), t+d, F(1, 2)-t-d))
        kk = channel(pp, half, qs)
        assert positive(kk) and qs[0] != qs[1]
        assert all(in_fixed_mass(q) and all(x > 0 for x in q) for q in qs)
        grid_count += 1
    groups.append({'name': 'nonclosed_segment_positive_controls', 'priors_checked': grid_count})

    # Extreme p permits arbitrarily labelled but noninformative signals.
    pp = vec(1, 0, 0)
    kk = channel(pp, half, (pp, pp))
    assert positive(kk)
    groups.append({'name': 'extreme_noninformative_signal', 'prior': pp, 'channel': kk})

    # Convexity is essential for reducing arbitrary finite decompositions to a
    # two-point segment in C: a triangle centroid plus its three vertices is not
    # convex and has a three-point decomposition without a two-point one.
    pp = vec('1/3', '1/3', '1/3')
    vertices = (vec(1, 0, 0), vec(0, 1, 0), vec(0, 0, 1))
    kk = channel(pp, (F(1, 3),) * 3, vertices)
    assert kk == vertices
    assert all(any(pp[i] > 0 and a[i] == b[i] == 0 for i in range(3))
               for idx, a in enumerate(vertices) for b in vertices[idx+1:])
    groups.append({'name': 'nonconvex_three_point_decomposition_boundary', 'prior': pp})

    # Existing declared channels can all be uninformative at a nonextreme p.
    pp = vec('1/2', '1/2')
    only_channel = (vec('1/3', '1/3'), vec('2/3', '2/3'))
    assert all(posterior(pp, row)[1] == pp for row in only_channel)
    groups.append({'name': 'abstract_possibility_not_available_information', 'channel': only_channel})

    out = Path(__file__).resolve().parent
    bindings = json.loads((out/'INPUT_BINDINGS.json').read_text())
    for item in bindings['inputs']:
        raw = (out/item['source_path']).read_bytes()
        assert len(raw) == item['bytes'] and hashlib.sha256(raw).hexdigest() == item['sha256']
    groups.append({'name': 'inherited_inputs_unchanged', 'inputs_checked': len(bindings['inputs'])})
    result = {'status': 'PASS', 'control_groups': len(groups), 'arithmetic': 'fractions.Fraction',
              'proof_scope': 'Exact finite controls only; universal statements have separate written proofs.',
              'results': serializable(groups)}
    (out/'CHECK_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status':'PASS','control_groups':len(groups),'segment_priors':grid_count,
                      'inherited_inputs_unchanged':len(bindings['inputs'])}, sort_keys=True))


if __name__ == '__main__':
    main()
