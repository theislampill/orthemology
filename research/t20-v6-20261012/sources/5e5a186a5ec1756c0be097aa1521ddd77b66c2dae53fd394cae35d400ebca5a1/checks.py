"""Exact controls for a source-bound D5/D6 review, not a hybrid simulator.

Run with Python or optimized Python. Every check uses an explicit exception.
Only finite rational holding-time kernels are processed by the refinement code.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical(blocks):
    return tuple(sorted(tuple(sorted(b)) for b in blocks))


def base_partition(labels):
    groups = {}
    for state, label in labels.items():
        groups.setdefault(label, []).append(state)
    return canonical(groups.values())


def signature(state, partition, kernel, timed):
    block_of = {s: i for i, b in enumerate(partition) for s in b}
    sums = {}
    for (time, outcome, target), mass in kernel.get(state, {}).items():
        key = (time, outcome, block_of[target]) if timed else (outcome, block_of[target])
        sums[key] = sums.get(key, F(0)) + mass
    return tuple(sorted(sums.items()))


def refine(labels, kernel, timed):
    partition = base_partition(labels)
    history = [partition]
    while True:
        groups = []
        for block in partition:
            local = {}
            for state in block:
                key = signature(state, partition, kernel, timed)
                local.setdefault(key, []).append(state)
            groups.extend(local.values())
        updated = canonical(groups)
        if updated == partition:
            return partition, history
        partition = updated
        history.append(partition)


def sidecar_bits(partition, labels):
    counts = {}
    for block in partition:
        values = {labels[s] for s in block}
        require(len(values) == 1, "Partition does not refine retained label")
        label = next(iter(values))
        counts[label] = counts.get(label, 0) + 1
    alphabet = max(counts.values())
    return alphabet, (alphabet - 1).bit_length()


def marginal(kernel, positions):
    result = {}
    for atom, mass in kernel.items():
        key = tuple(atom[i] for i in positions)
        result[key] = result.get(key, F(0)) + mass
    return result


def all_partitions(states):
    if not states:
        yield ()
        return
    first, *rest = states
    for partition in all_partitions(rest):
        yield canonical(((first,),) + partition)
        for i, block in enumerate(partition):
            yield canonical(partition[:i] + ((first,) + block,) + partition[i + 1:])


def is_finer(fine, coarse):
    return all(any(set(b) <= set(c) for c in coarse) for b in fine)


def stable(partition, labels, kernel):
    for block in partition:
        if len({labels[s] for s in block}) != 1:
            return False
        if len({signature(s, partition, kernel, True) for s in block}) != 1:
            return False
    return True


def atom_probability(kernel, predicate):
    return sum((mass for atom, mass in kernel.items() if predicate(atom)), F(0))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--original-root', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    checks = []
    bindings = json.loads((root / 'INPUT_BINDINGS.json').read_text())
    for binding in bindings:
        require(hashlib.sha256((root / binding['snapshot']).read_bytes()).hexdigest() == binding['sha256'],
                'Source snapshot hash mismatch')
        if args.original_root is not None:
            require(hashlib.sha256((args.original_root / binding['source']).read_bytes()).hexdigest() == binding['sha256'],
                    'Original source hash mismatch')
    checks.append('Three source snapshots match; originals also match when requested')

    # D5: L=(1,0). Varying discarded metric does not obstruct closure.
    fine_metric_at_0 = (F(1), F(1))
    fine_metric_at_1 = (F(1), F(2))
    require(1 / fine_metric_at_0[0] == 1 / fine_metric_at_1[0] == 1,
            'Positive cometric control failed')
    checks.append('D5 positive control: hidden metric variation with retained cometric one')

    # The source two-leaf control, checked by exact arithmetic.
    cometrics = (F(1), F(2))
    times = tuple(1 / value for value in cometrics)
    require(times == (F(1), F(1, 2)), 'D5 event times must differ at fixed physical time')
    # Fixed objective j(z1,z2)=z1 does not detect changes in the second column.
    a0, a1 = ((F(1), F(0)), (F(0), F(1))), ((F(1), F(0)), (F(0), F(2)))
    require(tuple(row[0] for row in a0) == tuple(row[0] for row in a1), 'Fixed-objective control failed')
    require(tuple(row[1] for row in a0) != tuple(row[1] for row in a1), 'All-objective obstruction missing')
    checks.append('D5 negative and fixed-objective controls agree with the source quantifiers')

    labels = {'slow': 'active', 'fast': 'active', 'done': 'done'}
    timing = {'fast': {(F(1), 'finish', 'done'): F(1)},
              'slow': {(F(2), 'finish', 'done'): F(1)}}
    untimed, _ = refine(labels, timing, False)
    timed, _ = refine(labels, timing, True)
    require(untimed == canonical((('slow', 'fast'), ('done',))), 'Untimed states should merge')
    require(timed == canonical((('slow',), ('fast',), ('done',))), 'Timed states must split')
    before_deadline = {s: atom_probability(k, lambda atom: atom[0] <= F(3, 2)) for s, k in timing.items()}
    require(before_deadline == {'fast': F(1), 'slow': F(0)}, 'Deadline discrepancy missing')
    require(sidecar_bits(untimed, labels) == (1, 0), 'Untimed bit count mismatch')
    require(sidecar_bits(timed, labels) == (2, 1), 'Timed bit count mismatch')
    checks.append('Hidden deterministic holding time: untimed zero bits versus timed one bit')

    # Exponential Markov control at horizon log(2): exp(-h log(2))=2**(-h).
    survival = {rate: F(1, 2 ** rate) for rate in (1, 2)}
    require(survival == {1: F(1, 2), 2: F(1, 4)}, 'Exponential survival control failed')
    checks.append('Hidden rates one and two have unequal exact survival at log two')

    labels = {'aligned': 'active', 'crossed': 'active', 'done': 'done'}
    correlated = {
        'aligned': {(F(1), 'zero', 'done'): F(1, 2), (F(2), 'one', 'done'): F(1, 2)},
        'crossed': {(F(1), 'one', 'done'): F(1, 2), (F(2), 'zero', 'done'): F(1, 2)},
    }
    require(marginal(correlated['aligned'], (0,)) == marginal(correlated['crossed'], (0,)),
            'Holding-time marginals must agree')
    require(marginal(correlated['aligned'], (1, 2)) == marginal(correlated['crossed'], (1, 2)),
            'Untimed branch marginals must agree')
    event = lambda atom: atom[0] <= 1 and atom[1] == 'zero'
    require(atom_probability(correlated['aligned'], event) == F(1, 2), 'Aligned probability mismatch')
    require(atom_probability(correlated['crossed'], event) == 0, 'Crossed probability mismatch')
    require(sidecar_bits(refine(labels, correlated, False)[0], labels) == (1, 0), 'Untimed correlation count mismatch')
    require(sidecar_bits(refine(labels, correlated, True)[0], labels) == (2, 1), 'Timed correlation count mismatch')
    checks.append('Equal separate timing and branch marginals lose their joint correlation')

    labels = {'start0': 'start', 'start1': 'start', 'wait0': 'wait', 'wait1': 'wait', 'done': 'done'}
    future = {'start0': {(F(1), 'advance', 'wait0'): F(1)},
              'start1': {(F(1), 'advance', 'wait1'): F(1)},
              'wait0': {(F(1), 'finish', 'done'): F(1)},
              'wait1': {(F(2), 'finish', 'done'): F(1)}}
    final, history = refine(labels, future, True)
    require([len(p) for p in history] == [3, 4, 5], 'Expected two successive timing refinements')
    require(sidecar_bits(final, labels) == (2, 1), 'Continuation sidecar count mismatch')
    partitions = list(all_partitions(sorted(labels)))
    require(len(partitions) == len(set(partitions)) == 52, 'Five-state partition oracle failed')
    candidates = [p for p in partitions if stable(p, labels, future)]
    require(final in candidates and all(is_finer(p, final) for p in candidates), 'Timed partition is not coarsest')
    checks.append('Timed refinement propagates to predecessor states; all 52 partitions cross-checked')

    labels = {'s0': 'active', 's1': 'active', 'd0': 'done', 'd1': 'done'}
    positive = {'s0': {(F(1), 'zero', 'd0'): F(1, 3), (F(2), 'one', 'd0'): F(2, 3)},
                's1': {(F(1), 'zero', 'd1'): F(1, 3), (F(2), 'one', 'd1'): F(2, 3)}}
    retained, _ = refine(labels, positive, True)
    require(retained == canonical((('s0', 's1'), ('d0', 'd1'))), 'Positive timed quotient should merge')
    require(sidecar_bits(retained, labels) == (1, 0), 'Positive quotient should need no sidecar')
    # At physical horizon 3/2, running cost rate 2 until absorption, jump cost 5.
    def expected_cost(kernel):
        return sum((mass * (2 * min(time, F(3, 2)) + (5 if time <= F(3, 2) else 0))
                    for (time, outcome, target), mass in kernel.items()), F(0))
    require(expected_cost(positive['s0']) == expected_cost(positive['s1']) == F(13, 3),
            'Retained running and jump costs failed')
    checks.append('Positive timed quotient retains deadline law and accumulated physical-time costs')

    result = {'status': 'PASS', 'control_groups': len(checks), 'checks': checks,
              'scope': 'Exact examples and finite timed refinement only; analytic proofs remain in the report',
              'original_sources_checked': args.original_root is not None}
    output = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
