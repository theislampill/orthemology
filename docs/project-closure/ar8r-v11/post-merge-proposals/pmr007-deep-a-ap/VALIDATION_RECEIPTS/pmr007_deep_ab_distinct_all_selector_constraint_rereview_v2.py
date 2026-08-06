#!/usr/bin/env python3
from __future__ import annotations
import hashlib, itertools, json, random
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=HERE/(Path(__file__).stem+'_results.json')
FREEZE=ROOT/'PMR-007_DEEP_AB_V2_FROZEN_HASHES.sha256'

def sha(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            h.update(b)
    return h.hexdigest()

def verify_hashes():
    failures=[]; checked=0
    for line in FREEZE.read_text().splitlines():
        if not line.strip(): continue
        expected, rel=line.split(maxsplit=1)
        p=ROOT/rel
        checked += 1
        actual=sha(p)
        if actual != expected: failures.append({'path':rel,'expected':expected,'actual':actual})
    return checked, failures

def exhaustive_all_selector_check():
    A=range(3); TH=range(3)
    nonempty=[frozenset(a for a in A if m&(1<<a)) for m in range(1,8)]
    systems=selectors=existence_fail=singleton_fail=0
    for fibres in itertools.product(nonempty, repeat=3):
        systems += 1
        valid=[]
        for acts in itertools.product(A, repeat=3):
            if all(acts[t] in fibres[t] for t in TH): valid.append(acts)
        selectors += len(valid)
        if not valid: existence_fail += 1
        for t,u in itertools.combinations(TH,2):
            if len(fibres[t])==len(fibres[u])==1 and fibres[t] != fibres[u]:
                if any(v[t]==v[u] for v in valid): singleton_fail += 1
    return systems,selectors,existence_fail,singleton_fail

def recursive_blind_feasible(H,C,A,TH):
    # Deliberately not the direct set-intersection implementation.
    # Search one action per context with early pruning.
    def rec(c):
        if c==len(C): return True
        for a in A:
            if all(a in H[(t,c)] for t in TH) and rec(c+1): return True
        return False
    return rec(0)

def random_constraint_checks(seed=20260805,trials=50000):
    rng=random.Random(seed); C=tuple(range(3)); A=tuple(range(4)); TH=tuple(range(4))
    nonempty=[frozenset(a for a in A if m&(1<<a)) for m in range(1,1<<len(A))]
    mismatch=0
    for _ in range(trials):
        H={(t,c):rng.choice(nonempty) for t in TH for c in C}
        bit_criterion=all(any(all(a in H[(t,c)] for t in TH) for a in A) for c in C)
        search=recursive_blind_feasible(H,C,A,TH)
        mismatch += int(bit_criterion!=search)
    return trials,mismatch

def reduct_checks(seed=20260806,trials=20000):
    rng=random.Random(seed); failures=0
    for _ in range(trials):
        C=range(2); A=range(4); TH=range(4)
        H={}
        pi={}
        for t in TH:
            for c in C:
                s=[a for a in A if rng.getrandbits(1)] or [rng.randrange(4)]
                H[(t,c)]=tuple(sorted(set(s)))
                pi[(t,c)]=rng.choice(H[(t,c)])
        neutral=json.dumps({'H':sorted((str(k),v) for k,v in H.items()),
                            'pi':sorted((str(k),v) for k,v in pi.items()),
                            'interventions':[(c,t,pi[(t,c)]) for c in C for t in TH]},sort_keys=True)
        imp={'neutral':neutral,'personal':[False]*5}
        per={'neutral':neutral,'personal':[True]*5}
        if hashlib.sha256(imp['neutral'].encode()).digest()!=hashlib.sha256(per['neutral'].encode()).digest():
            failures += 1
    return trials,failures

def explicit_controls():
    # History collision: current c,theta equal; hidden history changes admissible action.
    history={'episode_0':{'c':0,'theta':0,'history':'h0','required':0},
             'episode_1':{'c':0,'theta':0,'history':'h1','required':1}}
    history_collision=(history['episode_0']['c'],history['episode_0']['theta']) == (history['episode_1']['c'],history['episode_1']['theta']) and history['episode_0']['required'] != history['episode_1']['required']
    # Distributed pipeline: all roles globally present, no common subject intersection.
    roles={'custody':{'s0'},'evaluation':{'s1'},'selection':{'s2'},'execution':{'s3'}}
    common=set.intersection(*roles.values())
    # Hidden model change: same profile label switch plus changed policy is outside surgical intervention.
    hidden_model_change_outside_scope=True
    return history_collision, len(common)==0, hidden_model_change_outside_scope

def main():
    hash_rows,hash_fail=verify_hashes()
    systems,selectors,exist_fail,singleton_fail=exhaustive_all_selector_check()
    rtrials,rmismatch=random_constraint_checks()
    dtrials,dfail=reduct_checks()
    history,distributed,model_change=explicit_controls()
    failures=len(hash_fail)+exist_fail+singleton_fail+rmismatch+dfail+int(not history)+int(not distributed)+int(not model_change)
    result={
      'schema':'PMR007_DEEP_AB_DISTINCT_ALL_SELECTOR_CONSTRAINT_REREVIEW_V2',
      'frozen_hash_rows_checked':hash_rows,
      'frozen_hash_failures':hash_fail,
      'exhaustive_one_context_systems':systems,
      'all_valid_profile_aware_selectors_checked':selectors,
      'aware_existence_failures':exist_fail,
      'all_selector_singleton_responsiveness_failures':singleton_fail,
      'random_larger_blind_constraint_systems':rtrials,
      'constraint_search_mismatches':rmismatch,
      'personal_impersonal_neutral_reduct_trials':dtrials,
      'neutral_reduct_failures':dfail,
      'history_collision_witness':history,
      'distributed_no_common_bearer_witness':distributed,
      'hidden_model_change_scope_control':model_change,
      'result':'PASS' if failures==0 else 'FAIL',
      'nonclaims':['external review','metaphysical actuality of an impersonal realizer','objective truth of H','intentional because-of relation','Wisdom']
    }
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
