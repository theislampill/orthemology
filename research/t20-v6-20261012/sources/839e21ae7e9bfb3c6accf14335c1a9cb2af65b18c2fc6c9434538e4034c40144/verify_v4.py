#!/usr/bin/env python3
"""Exact finite checks of the new workflow; not empirical or general certification."""
from __future__ import annotations
import argparse, hashlib, itertools as it, json
from pathlib import Path
from collections import defaultdict
Q = ('alpha', 'beta')
E = (None,) + Q
Y = list(it.product(Q, E, E, (0, 1)))
X = [y+(c,) for y in Y for c in ('open', 'complete')]
def require(ok, message):
    if not ok: raise AssertionError(message)
def readiness(y):
    q,e1,e2,b=y
    return b == 0 and e1 == e2 == q
def invariant(x): return x[-1] != 'complete' or readiness(x[:-1])
def observe0(y): return (y[3], y[1] is not None, y[2] is not None)
def observe1(y): return y
def determines(states, record, target):
    fibres=defaultdict(set)
    for w in states: fibres[record(w)].add(target(w))
    return all(len(v)==1 for v in fibres.values()), fibres

def relational_checks():
    K=[x for x in X if invariant(x)]; scopes=[]
    for j in range(5):
        old={x[j] for x in X}; new={x[j] for x in K}
        require(old==new,'Exact local possibility lost')
        scopes.append({'coordinate':j,'local_values':len(old),
                       'completion_counts':{str(t):sum(x[j]==t for x in K) for t in old}})
    require(len(X)==72 and len(K)==38,'Unexpected boundary population')
    stale=('beta','alpha','alpha',0,'complete')
    require(stale in X and stale not in K,'Further-invariant witness failed')
    generated=[]
    for y in Y:
        generated.append(y+('open',))
        q,e1,e2,b=y
        if not b and e1==q and e2==q:generated.append(y+('complete',))
    require(set(generated)==set(K),'Operational rule differs from relation')
    return {'record_population':len(X),'admissible_records':len(K),'rejected_records':len(X)-len(K),
            'scopes':scopes,'witness':stale,'guard_relation_exact':True,
            'limit':'Singleton boundary-record projections, not complete temporal behaviours.'}

def access_checks():
    a=('beta','alpha','alpha',0); b=('beta','beta','beta',0)
    coarse,fibres=determines(Y,observe0,readiness); fine,_=determines(Y,observe1,readiness)
    require(not coarse and fine,'Wrong record-sufficiency result')
    require(observe0(a)==observe0(b) and readiness(a)!=readiness(b),'Pair witness failed')
    W=list(it.product((0,1),Y))
    def ell(w):return (w[0],observe0(w[1]) if w[0]==0 else observe1(w[1]))
    def connect(w):return (1,w[1])
    for w in W:
        final=connect(w) if w[0]==0 else w
        require(final[1]==w[1],'Connection mutated underlying target')
        require(readiness(ell(final)[1])==readiness(w[1]),'Wrong initial verdict')
    require(ell((0,a))==ell((0,b)) and ell(connect((0,a)))!=ell(connect((0,b))),
            'Connection did not violate congruence')
    ack,_=determines(Y,lambda y:(observe0(y),'connected'),readiness)
    require(not ack,'Acknowledgement incorrectly decides')
    return {'input_states':len(Y),'method_environment_states':len(W),'policy_cases':len(W),
            'coarse_fibres':len(fibres),'ambiguous_coarse_fibres':sum(len(v)>1 for v in fibres.values()),
            'coarse_record_decides':coarse,'fine_record_decides':fine,'acknowledgement_decides':ack,
            'congruence_violation_pair':[a,b],
            'limit':'Accurate reports and static candidate bindings; no empirical reliability or repertoire expansion.'}

def scheduling_checks():
    def publish(y,i,r):
        z=list(y);z[i+1]=r;return tuple(z)
    def stop(y):return y[:3]+(1,)
    commutations=0
    for y,r1,r2 in it.product(Y,Q,Q):
        require(publish(publish(y,0,r1),1,r2)==publish(publish(y,1,r2),0,r1),
                'Independent updates failed to commute')
        commutations+=1
    histories=[]
    for q in Q:
        for events in it.permutations(('job1','job2','interrupt')):
            y=(q,None,None,0)
            for event in events:
                y=stop(y) if event=='interrupt' else publish(y,int(event[-1])-1,q)
            require(not readiness(y),'Interrupt did not block completion')
            histories.append({'candidate':q,'events':events,'final':y})
        for order in it.permutations((0,1)):
            y=(q,None,None,0)
            for i in order:y=publish(y,i,q)
            require(readiness(y),'Valid job order failed')
    old=('alpha','alpha','alpha',0); after=stop(old)+('complete',)
    require(readiness(old) and not invariant(after),'Unprotected-boundary race missing')
    return {'commuting_updates':commutations,'interrupt_histories':histories,'positive_job_orders':4,
            'unprotected_boundary_witness':{'before':old,'after':after},
            'limit':'Independent register updates only; no general noninterference or speedup result.'}

def admission_checks():
    states=[(y,eta) for y in Y for eta in (0,1)]; target=lambda v:int(readiness(v[0]) and v[1])
    without,_=determines(states,lambda v:observe1(v[0]),target)
    with_permission,fibres=determines(states,lambda v:(observe1(v[0]),v[1]),target)
    require(not without and with_permission,'Permission distinction lost')
    omega=(0,1,2);record=lambda w:0 if w==0 else 1;h=lambda w:1 if w!=2 else 0
    global_factor,_=determines(omega,record,h)
    require(all(h(w)==1 for w in omega if record(w)==0) and not global_factor,
            'Local positive verdict improperly demands global decision')
    return {'situations':len(states),'fine_without_permission_decides':without,
            'fine_with_permission_decides':with_permission,
            'positive_admission_fibres':sum(v=={1} for v in fibres.values()),
            'local_positive_without_global_decision':True,
            'limit':'Finite check; the arbitrary-set criterion rests on its written proof.'}

def negative_checks():
    mutants={
        'presence_instead_of_binding':lambda y:not y[3] and y[1] is not None and y[2] is not None,
        'interrupt_ignored':lambda y:y[1]==y[2]==y[0],
        'second_job_ignored':lambda y:not y[3] and y[1]==y[0],
        'current_candidate_ignored':lambda y:not y[3] and y[1]==y[2] and y[1] is not None}
    witnesses={}
    for name,fn in mutants.items():
        bad=[y for y in Y if fn(y) and not readiness(y)]
        require(bad,'Undiscriminating mutant '+name)
        witnesses[name]={'counterexample_count':len(bad),'witness':bad[0]}
    before=('beta','alpha','alpha',0);after=('alpha','alpha','alpha',0)
    require(not readiness(before) and readiness(after),'Initial/current target distinction failed')
    witnesses['mutating_target_instead_of_observing_initial_state']={'before':before,'after':after}
    return {'rejected_shortcuts':witnesses,'limit':'Constructed adverse cases, not mutations of general theorem proofs.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    result={'status':'PASS','schema':'icsr-v4-workflow-checks-1',
            'relational':relational_checks(),'access':access_checks(),'scheduling':scheduling_checks(),
            'admission':admission_checks(),'negative_controls':negative_checks(),
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'limits':'Same-author exact finite model checks, not independent review, field validation, proof-assistant certification or performance evidence.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','boundary_records':len(X),'method_states':len(Y)*2,'guard_mutants':4}))
if __name__=='__main__':main()
