"""Exact finite controls for the written proofs; not a general proof or runtime."""
from fractions import Fraction as F
from itertools import combinations
import json


def posterior(mask, roots, prior=(F(1, 2), F(1, 2))):
    weights = list(prior)
    for i, likelihood in enumerate(roots):
        if mask & (1 << i):
            weights = [w * l for w, l in zip(weights, likelihood)]
    z = sum(weights)
    return tuple(w / z for w in weights)


def normalize(weights):
    z = sum(weights)
    return tuple(x / z for x in weights)


def quotient(roots, mode):
    n = 1 << len(roots)
    outputs = [posterior(x, roots) for x in range(n)]
    def label(values):
        index = {}
        return [index.setdefault(v, len(index)) for v in values]
    classes = label(outputs)
    while True:
        signature = []
        for x in range(n):
            successors = []
            for i in range(len(roots)):
                if mode in ('activate', 'both'):
                    successors.append(classes[x | (1 << i)])
                if mode in ('deactivate', 'both'):
                    successors.append(classes[x & ~(1 << i)])
            signature.append((outputs[x], tuple(successors)))
        refined = label(signature)
        if refined == classes:
            return classes
        classes = refined


def run():
    roots = [(F(2), F(1)), (F(2), F(1))]
    q0, qa, qb, qab = [posterior(x, roots) for x in range(4)]
    assert q0 == (F(1, 2), F(1, 2))
    assert qa == qb == (F(2, 3), F(1, 3))
    assert qab == (F(4, 5), F(1, 5))
    assert posterior(1 & ~1, roots) != posterior(2 & ~1, roots)
    assert posterior(1 | 1, roots) != posterior(2 | 1, roots)
    assert posterior(1 | 1, roots) != posterior(1 | 2, roots)
    # Ordinary repeat multiplication is not root-idempotent.
    assert normalize(tuple(x * l for x, l in zip(qa, roots[0]))) == qab != qa

    overlap_checks = 0
    for k in range(1, 7):
        roots_k = [(F(i + 2), F(1)) for i in range(k)]
        for e in range(1 << k):
            for f in range(1 << k):
                qe, qf, qi = [posterior(m, roots_k) for m in (e, f, e & f)]
                fused = normalize(tuple(a * b / c for a, b, c in zip(qe, qf, qi)))
                assert fused == posterior(e | f, roots_k)
                overlap_checks += 1

    quotient_rows = []
    for k in range(0, 7):
        # Add one positive constant likelihood to check its irrelevance.
        rs = [(F(2), F(1))] * k + [(F(3), F(3))]
        for mode in ('activate', 'deactivate', 'both'):
            partition = quotient(rs, mode)
            assert len(set(partition)) == 1 << k
            for x, y in combinations(range(1 << len(rs)), 2):
                assert (partition[x] == partition[y]) == ((x & ((1 << k) - 1)) == (y & ((1 << k) - 1)))
            quotient_rows.append({'informative_roots': k, 'constant_roots': 1,
                                  'alphabet': mode, 'posterior_values': k + 1,
                                  'continuation_classes': len(set(partition))})

    # One log-likelihood direction need not imply collisions: binary-place exponents.
    injective = [(F(2 ** (2 ** i)), F(1)) for i in range(6)]
    assert len({posterior(x, injective) for x in range(64)}) == 64
    # Positivity firewall: a hard indicator update is genuinely idempotent.
    hard = (F(1), F(0))
    qhard = normalize(tuple(a * b for a, b in zip(q0, hard)))
    assert normalize(tuple(a * b for a, b in zip(qhard, hard))) == qhard
    return {'status': 'PASS', 'exact_arithmetic': 'fractions.Fraction',
            'overlap_pairs_checked': overlap_checks,
            'partition_checks': quotient_rows,
            'posterior_collision_and_named_operation_controls': 'PASS',
            'rank_one_injective_control': 'PASS',
            'nonpositive_likelihood_scope_control': 'PASS',
            'assurance': 'Finite deterministic controls only; general claims have written proofs.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
