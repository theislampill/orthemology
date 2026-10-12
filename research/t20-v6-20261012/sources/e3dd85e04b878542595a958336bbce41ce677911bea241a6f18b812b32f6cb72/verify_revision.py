#!/usr/bin/env python3
"""Exact finite checks for clarified examples; not proof or empirical validation."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import itertools as it
import json
from pathlib import Path

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def partitions(n, prefix=()):
    if len(prefix) == n:
        yield prefix
        return
    for k in range(max(prefix, default=-1) + 2):
        yield from partitions(n, prefix + (k,))

def record_checks():
    cases = sufficient = 0
    for n in range(1, 6):
        for record in partitions(n):
            for target in it.product((0, 1), repeat=n):
                constant = all(record[i] != record[j] or target[i] == target[j]
                               for i in range(n) for j in range(n))
                recovered = {}
                for i in range(n):
                    recovered.setdefault(record[i], target[i])
                factor = all(recovered[record[i]] == target[i] for i in range(n))
                require(constant == factor, 'Fibre/factorisation mismatch')
                cases += 1
                sufficient += factor
    return {'cases': cases, 'sufficient_cases': sufficient,
            'scope': 'All set partitions and Boolean targets on one through five elements; no claim to computationally prove the arbitrary-set statement.'}

def policy_checks():
    traces = []
    for initial in it.product((0, 1), repeat=2):
        w = initial
        observe = lambda s: (s[0], s[0]*s[1])
        trace = [('read', observe(w))]
        if observe(w)[0] == 0:
            w = (1, w[1])
            trace += [('connect', w[0]), ('read', observe(w))]
        verdict = observe(w)[1]
        require(verdict == initial[1], 'Reconnection policy failed')
        require(sum(op == 'connect' for op, _ in trace) <= 1, 'Spurious reconnection')
        traces.append({'initial': initial, 'trace': trace, 'verdict': verdict})
    require((0,0*0) == (0,0*1), 'Disconnected records do not coincide')
    require((1,1*0) != (1,1*1), 'Connection fails to distinguish')
    return {'initial_cases': len(traces), 'traces': traces}

def conservation_checks():
    q_in, q_out = (0,0,1), (0,0,1,1)
    input_laws = [(F(i,4),F(j,4),F(4-i-j,4)) for i in range(5) for j in range(5-i)]
    comparisons = 0
    for choices in it.product(range(5), repeat=3):
        T = [[F(0) for _ in range(3)] for _ in range(4)]
        for x, k in enumerate(choices):
            ys = [y for y in range(4) if q_out[y] == q_in[x]]
            T[ys[0]][x], T[ys[1]][x] = F(k,4), F(4-k,4)
        for mu in input_laws:
            nu = [sum(T[y][x]*mu[x] for x in range(3)) for y in range(4)]
            left = [sum(nu[y] for y in range(4) if q_out[y] == v) for v in (0,1)]
            right = [sum(mu[x] for x in range(3) if q_in[x] == v) for v in (0,1)]
            require(left == right, 'Conservation identity failed')
            comparisons += 1
    return {'kernels': 125, 'input_laws_per_kernel': len(input_laws), 'comparisons': comparisons,
            'arithmetic': 'exact rational', 'scope': 'Three inputs, four outputs, two inventory fibres, probabilities in quarter increments.'}

def counterexamples():
    # Compare complete records to target values, not assertion labels.
    def determines(records, answers):
        return all(records[i] != records[j] or answers[i] == answers[j]
                   for i in range(len(records)) for j in range(len(records)))
    hidden = [(0, 0), (0, 1)]
    ell = lambda w: (w[0], w[0] * w[1])
    u = lambda w: (1, w[1])
    target = [w[1] for w in hidden]
    local_records = [ell(w) for w in hidden]
    # A connector acknowledgement reports successful connection, not parity.
    acknowledgement_only = [(ell(w), u(w)[0]) for w in hidden]
    proper_readback = [(ell(w), ell(u(w))) for w in hidden]
    # Identity transition on two states with a constant inventory.
    laws = [(F(1), F(0)), (F(0), F(1))]
    identity = ((F(1), F(0)), (F(0), F(1)))
    outputs = [tuple(sum(identity[y][x]*mu[x] for x in range(2))
                     for y in range(2)) for mu in laws]
    inventory_records = [(sum(nu),) for nu in outputs]
    old_admission = [int(w[0] == 0) for w in hidden]
    revised_target = [w[1] for w in hidden]
    ts = [F(k,17) for k in range(1,17)]
    laws_on_two_states = [(t,1-t) for t in ts]
    witnesses = {
        'disconnected_read_alone_is_not_a_decision': not determines(local_records,target),
        'connection_acknowledgement_without_readback_is_insufficient': not determines(acknowledgement_only,target),
        'proper_reconnection_readback_is_sufficient': determines(proper_readback,target),
        'constant_inventory_does_not_determine_full_output': not determines(inventory_records,outputs),
        'old_admission_does_not_settle_new_target': determines(local_records,old_admission) and not determines(local_records,revised_target),
        'different_weights_can_share_two_state_support': len(set(laws_on_two_states)) == len(ts) and all(all(weight > 0 for weight in law) for law in laws_on_two_states)
    }
    require(all(witnesses.values()), 'Counterexample or positive control failed')
    return {'witnesses': witnesses,
            'local_records': local_records, 'acknowledgement_only': acknowledgement_only,
            'proper_readback': proper_readback, 'initial_targets': target,
            'identity_channel_output_laws': [list(map(str,nu)) for nu in outputs],
            'limit': 'The arbitrary-set and infinite-family conclusions rely on the written argument, not the finite sample.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    result={'status':'PASS','schema':'icsr-editorial-revision-checks-1',
            'record_factorisation':record_checks(),'explicit_method_policy':policy_checks(),
            'conserved_observable':conservation_checks(),'counterexamples':counterexamples(),
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'limits':'Same-author finite checks. General proofs, source reliability, authorisation and empirical performance are not certified by a successful run.'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'record_cases':result['record_factorisation']['cases'],'conservation_comparisons':result['conserved_observable']['comparisons'],'policy_cases':result['explicit_method_policy']['initial_cases']},indent=2))
if __name__=='__main__': main()
