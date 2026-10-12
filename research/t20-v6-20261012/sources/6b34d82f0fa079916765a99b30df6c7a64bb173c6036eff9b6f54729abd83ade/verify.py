#!/usr/bin/env python3
"""One bounded CPC task-family application of inherited H-Continuation/audit math.
No new theorem, no empirical cognition test, no external dependencies.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib, json, math

ROOT=Path(__file__).resolve().parent
S=list(product((0,1),repeat=2))  # target theta, fixed future audit D
u=(Q(1),)*4
theta=tuple(Q(t) for t,d in S)
audit=tuple(Q(d) for t,d in S)
tau=tuple(Q((-1)**t) for t,d in S)
delta=tuple(Q((-1)**d) for t,d in S)
interaction=tuple(a*b for a,b in zip(tau,delta))
pi0=(Q(2,5),Q(1,10),Q(1,10),Q(2,5))
pi1=(Q(1,10),Q(2,5),Q(2,5),Q(1,10))

def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q(0))
def mv(A,x): return tuple(dot(a,x) for a in A)
def rm(a,M): return tuple(dot(a,col) for col in zip(*M))
def mm(A,B): return tuple(rm(a,B) for a in A)
def diag(v): return tuple(tuple(Q(v[i]) if i==j else Q(0) for j in range(4)) for i in range(4))
def rref(rows):
    A=[list(map(Q,row)) for row in rows]; k=0
    for j in range(4):
        p=next((i for i in range(k,len(A)) if A[i][j]),None)
        if p is None: continue
        A[k],A[p]=A[p],A[k];a=A[k][j];A[k]=[x/a for x in A[k]]
        for i in range(len(A)):
            if i!=k and A[i][j]:
                a=A[i][j];A[i]=[x-a*y for x,y in zip(A[i],A[k])]
        k+=1
        if k==len(A):break
    return tuple(tuple(row) for row in A[:k])
def closure(rows,Ms):
    B=rref(rows); dims=[len(B)]
    while True:
        C=rref(list(B)+[rm(b,M) for M in Ms for b in B])
        if C==B:return B,dims
        B=C;dims.append(len(B))
def posterior(r):
    mass=dot(u,r)
    return None if mass==0 else dot(theta,r)/mass

def serial(v):
    if isinstance(v,Q):return str(v)
    if isinstance(v,dict):return {k:serial(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [serial(x) for x in v]
    return v

M=[diag([d==b for t,d in S]) for b in (0,1)]
V=(u,theta,audit)
assert mv(V,pi0)==mv(V,pi1)==(Q(1),Q(1,2),Q(1,2))
assert all(x>=0 for pi in (pi0,pi1) for x in pi)
assert all(sum(pi)==1 for pi in (pi0,pi1))
# This is the inherited audit pair, not a new counterexample.
assert dot(interaction,pi0)==Q(3,5)
assert dot(interaction,pi1)==Q(-3,5)
posteriors=[[posterior(mv(N,pi)) for N in M] for pi in (pi0,pi1)]
assert posteriors==[[Q(1,5),Q(4,5)],[Q(4,5),Q(1,5)]]
assert all(dot(u,mv(N,pi))==Q(1,2) for pi in (pi0,pi1) for N in M)
B,dims=closure(V,M)
assert dims==[3,4] and len(B)==4
# A known finite candidate comparison: one correct conditional probe separates.
assert posteriors[0][1] != posteriors[1][1]
# Same fixed observation is idempotent; contradictory observation impossible.
assert all(mm(N,N)==N for N in M)
assert all(not any(row) for row in mm(M[0],M[1]))
for pi in (pi0,pi1):
    assert posterior(mv(M[0],mv(M[1],pi))) is None
# Reuse the inherited closed Walsh moment update, verifying basis identity.
W=(u,tau,delta,interaction)
Ts=[]
for b,N in enumerate(M):
    s=Q((-1)**b)
    T=((Q(1,2),0,s/2,0),(0,Q(1,2),0,s/2),(s/2,0,Q(1,2),0),(0,s/2,0,Q(1,2)))
    assert mm(W,N)==mm(T,W)
    Ts.append(T)
# Each isolated-coordinate Bernoulli benchmark has true p=1/2 in both laws.
# Every observed bit is assigned likelihood 1/2, even for adaptive coordinate
# choices, provided EACH query draws a fresh independent episode and reads one bit.
for n in range(1,6):
    for qs in product((theta,audit),repeat=n):
        for ys in product((0,1),repeat=n):
            ls=[]
            for pi in (pi0,pi1):
                l=Q(1)
                for q,y in zip(qs,ys):
                    p=dot(q,pi);l*= p if y else 1-p
                ls.append(l)
            assert ls==[Q(1,2)**n,Q(1,2)**n]
# Equal one-bit expected scores are an exact statement, no log numeric needed.
# Illustrative floating-point conditional code lengths do not certify semantics.
h=-(.2*math.log2(.2)+.8*math.log2(.8))
results={
 'status':'PASS; inherited mathematics, single new task-family application',
 'state_order':S,'laws':[pi0,pi1],
 'retained_summary_both':mv(V,pi0),
 'mixed_Walsh_moments':[dot(interaction,pi0),dot(interaction,pi1)],
 'posteriors_D0_D1':posteriors,
 'target_plus_audit_closure_dimensions':dims,
 'same_fixed_audit_idempotent':True,'contradictory_reread_posterior':None,
 'probe_D1_posterior_gap':abs(posteriors[0][1]-posteriors[1][1]),
 'two_candidate_minimax_absolute_conditional_error':Q(3,10),
 'isolated_query_expected_logloss_bits_each':1,
 'isolated_query_iid_likelihood_controls_up_to_length':5,
 'conditional_entropy_bits_approx':h,
 'omission_excess_conditional_logloss_bits_approx':1-h,
 'joint_model_parameters_plus_minus':[[Q(3,5)],[Q(-3,5)]],
 'boundaries':['All marginal-prediction equivalence refers to one coordinate per fresh independent episode.',
               'No claim of perfect realized guesses, causal identification, actual mental states, or testimonial warrant.',
               'One conditional probe separates two declared candidates, not all possible models.',
               'Numbers quantify this finite predictive task only; they are not theological warrant scores.']}
# Bound primary and inherited files, and assert inherited originals unchanged.
bindings=json.loads((ROOT/'INPUT_BINDINGS.json').read_text())
for x in bindings['inherited_inputs']:
    snap=ROOT/x['snapshot']
    assert hashlib.sha256(snap.read_bytes()).hexdigest()==x['sha256']
    original=ROOT.parent/x['original']
    assert hashlib.sha256(original.read_bytes()).hexdigest()==x['sha256']
for x in bindings['primary_sources']:
    assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256']
results['input_bindings_reverified']=True
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(serial(results),indent=2)+'\n')
print(json.dumps(serial(results),indent=2))
