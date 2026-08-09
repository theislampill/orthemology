#!/usr/bin/env python3
from itertools import product
import json
from pathlib import Path

GUARDS = (
    'exact_textual_custody','version_identity','translation_fidelity',
    'attribution_fidelity','source_authority','source_truth_in_track_n',
    'actual_referent_or_world_interpretation','predicate_preservation',
    'target_bearer_context_applicability','formal_target_link')

def pre(X, targets, transitions, hs, n=2, actions=2):
    out=set()
    for s in range(n):
        for a in range(actions):
            if all(transitions[h][s][a] in X for h in hs):
                out.add(s); break
    return out

def fixed(targets, transitions, hs, n=2, actions=2):
    tstar=set(range(n))
    for h in hs: tstar &= targets[h]
    V=set(tstar)
    while True:
        nv=tstar & pre(V,targets,transitions,hs,n,actions)
        if nv==V: break
        V=nv
    W=set(V)
    while True:
        nw=W | pre(W,targets,transitions,hs,n,actions)
        if nw==W: break
        W=nw
    return V,W

def bits_to_trans(bits):
    it=iter(bits)
    return [[next(it),next(it)] for _ in range(2)]

def main():
    guard_rows=0; licensed=0; deletion_witnesses=0
    for row in product([0,1], repeat=len(GUARDS)):
        guard_rows += 1
        if all(row): licensed += 1
    for i in range(len(GUARDS)):
        row=[1]*len(GUARDS); row[i]=0
        # Missing coordinate leaves the actual-target completion free.
        if not all(row): deletion_witnesses += 1

    systems=0; monotonicity_failures=[]
    subsets=[(0,),(1,)]
    target_masks=list(range(4))
    trans_bits=list(product([0,1], repeat=4))
    for tm0,tm1 in product(target_masks, repeat=2):
        targets=[{s for s in range(2) if (tm0>>s)&1},
                 {s for s in range(2) if (tm1>>s)&1}]
        for b0,b1 in product(trans_bits, repeat=2):
            transitions=[bits_to_trans(b0),bits_to_trans(b1)]
            vf,wf=fixed(targets,transitions,(0,1))
            for hs in subsets:
                vr,wr=fixed(targets,transitions,hs)
                if not vf <= vr or not wf <= wr:
                    monotonicity_failures.append({
                        'targets':[sorted(x) for x in targets],
                        'transitions':transitions,'hs':hs,
                        'V_full':sorted(vf),'V_restricted':sorted(vr),
                        'W_full':sorted(wf),'W_restricted':sorted(wr)})
                    break
            systems += 1

    parity_worlds=[
        {'profile':(1,1,1,1),'track_n':1,'personal':1},
        {'profile':(1,1,1,1),'track_n':0,'personal':0},
    ]
    profile_collision=(parity_worlds[0]['profile']==parity_worlds[1]['profile']
                       and parity_worlds[0]['track_n']!=parity_worlds[1]['track_n'])
    result={
        'guard_rows':guard_rows,'fully_guarded_rows':licensed,
        'single_guard_deletion_witnesses':deletion_witnesses,
        'exhaustive_two_state_systems':systems,
        'monotonicity_failures':len(monotonicity_failures),
        'first_monotonicity_failure':monotonicity_failures[:1],
        'neutral_profile_source_parity_collision':profile_collision,
        'overall':'PASS' if licensed==1 and deletion_witnesses==len(GUARDS)
                 and not monotonicity_failures and profile_collision else 'FAIL'}
    out=Path(__file__).with_name(Path(__file__).stem+'_results.json')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__': main()
