#!/usr/bin/env python3
"""Independent exact finite laws, derived by simulating the original run first.
No author's expected-law code is imported. Histories here are chronological;
right-appending newest-first restarts are implemented by prepending the old
chronological history. Two independent constructions of the ORIGINAL law are
crosschecked: complete preallocated oracle tables and sequential path products.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict,Counter
from pathlib import Path
import json,hashlib
COUNTS=Counter();W=(F(2,7),F(5,7))
def check(p,k):
    assert p,k
    COUNTS[k]+=1

def action(code,r,h):
    # Full causal history, with seed and two remembered records plus absolute length.
    if not h:return (code >> r)&1
    _,last_a,last_y=h[-1]
    old_y=h[-2][2] if len(h)>1 else 0
    bit=r+2*last_y+4*last_a
    return ((code>>bit)&1) ^ ((code>>8)&1 and len(h)%2) ^ ((code>>9)&1 and old_y)

def run(code,r,ys,old=(),initial=0,wrong_append=False,wrong_state=False):
    tail=();state=initial
    for y in ys:
        history=tail+old if wrong_append else old+tail
        a=action(code,r,history)
        tail+=((state,a,y),)
        state=y if not wrong_state else initial
    return tail

def conditional_from_original(code,rows,m,L):
    """Enumerate every full original receipt word, then restrict/read out."""
    joints=defaultdict(lambda:defaultdict(F));seeds=defaultdict(lambda:defaultdict(F))
    for r in (0,1):
        for ys in product((0,1),repeat=m+L):
            full=run(code,r,ys);mass=W[r]
            for s,a,y in full:
                q=rows[2*s+a];mass*=q if y else 1-q
            if mass:
                old=full[:m];tail=full[m:]
                joints[old][tail]+=mass;seeds[old][r]+=mass
    out={}
    for old,d in joints.items():
        mass=sum(d.values());out[old]=(mass,{t:v/mass for t,v in d.items()},{r:seeds[old][r]/mass for r in (0,1)})
    return out

def posterior_from_actions(code,old):
    keep=[]
    for r in (0,1):
        keep.append(all(action(code,r,old[:i])==old[i][1] and old[i][0]==(old[i-1][2] if i else 0) for i in range(len(old))))
    z=sum(W[r] for r in (0,1) if keep[r])
    return {r:W[r]/z if keep[r] else F(0) for r in (0,1)} if z else None

def restarted(code,rows,old,L,post,wrong_append=False,wrong_state=False):
    out=defaultdict(F);state=old[-1][2] if old else 0
    for r in (0,1):
        for ys in product((0,1),repeat=L):
            tail=run(code,r,ys,old,state,wrong_append,wrong_state);mass=post[r]
            for s,a,y in tail:
                q=rows[2*s+a];mass*=q if y else 1-q
            if mass:out[tail]+=mass
    return dict(out)

def killed(tail,D,late=False):
    answer=[(True,())];alive=True
    for n,rec in enumerate(tail,1):
        if not late:alive=alive and rec[:2] in D
        answer.append((True,tail[:n]) if alive else (False,()))
        if late:alive=alive and rec[:2] in D
    return tuple(answer)

def pushkill(law,D,late=False):
    out=defaultdict(F)
    for t,v in law.items():out[killed(t,D,late)]+=v
    return dict(out)

def full_oracle_original(code,rows,H):
    """Every row at every clock time is sampled first, jointly independent.
    Unused entries are integrated out by explicit enumeration, not by an assumption.
    All row probabilities are quarters so exact integer weights suffice.
    """
    nums=tuple(int(q*4) for q in rows);out=defaultdict(int)
    for bits in product((0,1),repeat=4*H):
        likelihood=1
        for j,b in enumerate(bits):likelihood*=nums[j%4] if b else 4-nums[j%4]
        if not likelihood:continue
        for r,rw in ((0,2),(1,5)):
            h=();s=0
            for n in range(H):
                a=action(code,r,h);y=bits[4*n+2*s+a];h+=((s,a,y),);s=y
            out[h]+=rw*likelihood
    return {h:F(v,7*4**(4*H)) for h,v in out.items()}

codes=[0,1,2,3,27,54,105,150,165,195,240,255,257,365,614,1023]
row_controls=[tuple(F(v,4) for v in xs) for xs in [(0,1,2,4),(4,2,1,0),(1,1,3,3),(3,1,1,3),(1,3,3,1),(2,2,2,2)]]
for code in codes:
    for rows in row_controls:
        oracle=full_oracle_original(code,rows,3)
        sequential=conditional_from_original(code,rows,0,3)[()][1]
        check(oracle==sequential,'complete_oracle_vs_original_path_law')
        check(sum(oracle.values())==1,'full_oracle_normalization')

models=list(product((F(1,4),F(3,4)),repeat=4))+row_controls[:2]
allcodes=sorted(set(codes+[(j*197)%1024 for j in range(96)]))
mutants=Counter();saved=[]
for code in allcodes:
    for rows in models:
        for m in (0,1,2):
            original=conditional_from_original(code,rows,m,3)
            check(sum(mass for mass,_,_ in original.values())==1,'prefix_partition')
            for old,(mass,law,post) in original.items():
                check(sum(law.values())==1,'conditional_probability')
                check(post==posterior_from_actions(code,old),'derived_common_posterior')
                check(law==restarted(code,rows,old,3,post),'actual_markov_restart')
                for t in law:
                    check(t[0][0]==(old[-1][2] if old else 0),'restart_latest_observed_state')
                if old:
                    for name,bad in [('prior_reset',restarted(code,rows,old,3,dict(enumerate(W)))),('append_reversal',restarted(code,rows,old,3,post,wrong_append=True)),('state_reset',restarted(code,rows,old,3,post,wrong_state=True))]:
                        if bad!=law:
                            mutants[name]+=1
                            if not any(v['mutant']==name for v in saved):saved.append({'mutant':name,'code':code,'rows':[str(x) for x in rows],'old':old})

# Cross-model equality compares original conditioned experiments directly.
for code in codes:
    cached=[conditional_from_original(code,p,2,3) for p in models]
    for i,P in enumerate(models):
        for j,Q in enumerate(models):
            D={divmod(e,2) for e in range(4) if P[e]==Q[e]}
            for old in cached[i].keys()&cached[j].keys():
                mp,lp,pp=cached[i][old];mq,lq,pq=cached[j][old]
                check(pp==pq,'cross_model_common_posterior')
                check(pushkill(lp,D)==pushkill(lq,D),'conditional_killed_full_law')
                check({t:v for t,v in lp.items() if all(x[:2] in D for x in t)}=={t:v for t,v in lq.items() if all(x[:2] in D for x in t)},'no_outside_restricted_law')
                if mp!=mq:COUNTS['unequal_prefix_likelihood_controls']+=1
                if any(x[:2] not in D for x in old):COUNTS['old_prefix_outside_retained_set_controls']+=1
                if pushkill(lp,D,late=True)!=pushkill(lq,D,late=True):mutants['late_killing']+=1
for name in ('prior_reset','append_reversal','state_reset','late_killing'):check(mutants[name]>0,'mutant_rejected_'+name)
report={'status':'PASS','exact_assertions':sum(v for k,v in COUNTS.items() if not k.endswith('_controls')),'counts':dict(COUNTS),'mutant_disagreements':dict(mutants),'first_mutant_witnesses':saved,'scope':'Bounded exact observed laws; full preallocated-oracle controls crosscheck original path construction. Not a substitute for infinite-law or almost-sure kernel proofs.'}
print(json.dumps(report,indent=2))
