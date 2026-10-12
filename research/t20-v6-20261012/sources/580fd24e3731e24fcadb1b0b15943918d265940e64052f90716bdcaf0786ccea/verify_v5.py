#!/usr/bin/env python3
"""Exact sensitivity checks for the clarified workflow boundary.

These check finite abstract records/interleavings, not a concurrent implementation
or a proof of linearizability. All inherited mathematical suites are separate.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json
from pathlib import Path

Q = ('alpha', 'beta')
E = (None,) + Q
Y = tuple(itertools.product(Q, E, E, (0, 1)))

def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def ready(y: tuple) -> bool:
    q, e1, e2, interrupt = y
    return interrupt == 0 and e1 == q and e2 == q

def permitted(record: tuple) -> bool:
    return record[-1] == 'open' or ready(record[:-1])

def check_joint_boundary() -> dict:
    cached_violations, receipts_only, revalidated = [], [], 0
    for before, after in itertools.product(Y, repeat=2):
        # Boundary-readiness is evaluated at the publication effect, not at the
        # initial state of Theorem 8 and not from the cached previous decision.
        current_verdict = 'complete' if ready(after) else 'open'
        require(permitted(after + (current_verdict,)), 'Joint guard false pass')
        revalidated += 1
        if ready(before) and not ready(after):
            cached_violations.append((before, after))
            require(not permitted(after + ('complete',)), 'Cached false pass undetected')
            if before[0] == after[0] and before[3] == after[3]:
                receipts_only.append((before, after))
    require(len(cached_violations) == 68, 'Wrong invalidation population')
    require(len(receipts_only) == 16, 'Receipt-sensitive boundary not covered')
    changed_coordinate_witnesses = {}
    for j, name in enumerate(('candidate_identity', 'first_receipt', 'second_receipt', 'interrupt')):
        pairs = [(a, b) for a, b in cached_violations
                 if a[j] != b[j] and all(a[k] == b[k] for k in range(4) if k != j)]
        require(bool(pairs), 'Missing coordinate witness: ' + name)
        changed_coordinate_witnesses[name] = {'count': len(pairs), 'example': pairs[0]}
    return {'ordered_input_pairs': revalidated,
            'cached_verdict_violations': len(cached_violations),
            'violations_with_candidate_and_interrupt_fixed': len(receipts_only),
            'coordinate_witnesses': changed_coordinate_witnesses,
            'joint_revalidation_records_satisfy_guard': True}

def check_atomic_reads() -> dict:
    # Each read sees the current value of its own register. The assembled tuple
    # never occurs as a state, so individual-read atomicity supplies no snapshot.
    states = [('alpha', 'alpha', 'beta', 0),
              ('alpha', 'beta', 'beta', 0),
              ('alpha', 'beta', 'alpha', 0)]
    require(all(not ready(y) for y in states), 'Witness contains a ready instant')
    observed = (states[0][0], states[0][1], states[2][2], states[2][3])
    require(ready(observed), 'Torn read fails to fool guard')
    require(observed not in states, 'Read unexpectedly coherent')
    require(not permitted(states[-1] + ('complete',)), 'Torn-read completion accepted')
    return {'interleaving_states': states, 'assembled_report': observed,
            'ready_at_any_actual_state': False, 'report_appears_ready': True,
            'single_register_reads_do_not_supply_joint_atomicity': True}

def check_effect_scope() -> dict:
    at_effect = ('alpha', 'alpha', 'alpha', 0, 'complete')
    next_boundary = ('alpha', 'alpha', 'alpha', 1, 'open')
    require(permitted(at_effect), 'Valid effect rejected')
    require(permitted(next_boundary) and not ready(next_boundary[:-1]),
            'Later interrupt not represented as a new open boundary')
    require(not permitted(next_boundary[:-1] + ('complete',)), 'Reusing old verdict accepted')
    return {'frozen_effect_record': at_effect, 'new_boundary': next_boundary,
            'old_scoped_record_remains_valid': True,
            'old_verdict_is_not_current_readiness': True}

def check_label_semantics() -> dict:
    # Deliberately break the immutable-label premise: a label now denotes altered
    # content, while the stored tokens are unchanged. No token-only calculation
    # can re-establish the lost interpretation. This is not an allowed model step.
    situations = [('original_content', True), ('changed_content_under_same_label', False)]
    record = ('alpha', 'alpha', 'alpha', 0)
    require(ready(record), 'Token record unexpectedly not ready')
    require(len({valid for _, valid in situations}) == 2, 'Semantic witness lost')
    return {'same_token_record': record, 'situations': situations,
            'token_only_record_determines_actual_receipt_validity': False,
            'scope': 'Sensitivity to violating the known immutable-label meaning, not an in-model counterexample.'}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = {'status': 'PASS', 'schema': 'icsr-v5-boundary-sensitivity-1',
              'joint_boundary': check_joint_boundary(),
              'atomic_reads': check_atomic_reads(),
              'effect_scope': check_effect_scope(),
              'label_semantics': check_label_semantics(),
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'limits': 'Same-author finite sensitivity checks. No new general theorem, field experiment, timing guarantee, noninterference proof or concurrent implementation verification.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status':'PASS','transition_pairs':len(Y)**2,'cached_false_passes':68,'receipt_only_false_passes':16}))
if __name__ == '__main__':
    main()
