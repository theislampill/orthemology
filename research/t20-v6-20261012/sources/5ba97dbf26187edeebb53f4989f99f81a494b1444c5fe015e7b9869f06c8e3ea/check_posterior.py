#!/usr/bin/env python3
"""Exact finite posterior controls, separate from the general Lean proof."""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import json

prior={0:F(1,3),1:F(2,3)}
probs=[F(0),F(1,4),F(1,2),F(3,4),F(1)]
policies=list(product(product((0,1),repeat=3),repeat=2))
def action(pol,r,h):return pol[r][0] if not h else pol[r][1+h[0][1]]
def compatible(pol,r,h):
    return all(action(pol,r,h[i+1:])==a for i,(a,y) in enumerate(h))
def likelihood(rows,h):
    p=F(1)
    for a,y in h:p*=rows[a] if y==0 else 1-rows[a]
    return p

def joint(rows,pol):
    nodes=[(r,(),w) for r,w in prior.items()];ans=defaultdict(F)
    for _ in range(2):
        nxt=[]
        for r,h,w in nodes:
            a=action(pol,r,h)
            for y,p in [(0,rows[a]),(1,1-rows[a])]:
                if p:nxt.append((r,((a,y),)+h,w*p))
        nodes=nxt
    for r,h,w in nodes:ans[(r,h)]+=w
    return dict(ans)

positive=0;null=0;shared=0;nontrivial=0
for pol in policies:
    expected={};seen={}
    for rows in product(probs,repeat=2):
        j=joint(rows,pol)
        allh=list(product(product((0,1),repeat=2),repeat=2))
        for h in allh:
            seedweights={r:prior[r] if compatible(pol,r,h) else F(0) for r in prior}
            c=sum(seedweights.values());l=likelihood(rows,h)
            assert all(j.get((r,h),0)==seedweights[r]*l for r in prior)
            mass=sum(j.get((r,h),0) for r in prior)
            assert mass==c*l
            if mass:
                posterior={r:j.get((r,h),0)/mass for r in prior}
                common={r:seedweights[r]/c for r in prior}
                assert posterior==common
                positive+=1
                if posterior!=prior:nontrivial+=1
                if h in seen:assert posterior==seen[h];shared+=1
                seen[h]=posterior
                # One genuinely unused fresh Bernoulli row remains independent.
                future_p=rows[0]
                for r in prior:
                    for b,q in [(0,future_p),(1,1-future_p)]:
                        assert j.get((r,h),0)*q/mass==posterior[r]*q
            else:null+=1
# Deliberately coarsening away the selected action destroys seed cancellation.
# Seed chooses its own action; P and Q assign different likelihoods to y=0.
coarseP={0:prior[0]*F(1,4),1:prior[1]*F(3,4)}
coarseQ={0:prior[0]*F(3,4),1:prior[1]*F(1,4)}
coarseP={r:w/sum(coarseP.values()) for r,w in coarseP.items()}
coarseQ={r:w/sum(coarseQ.values()) for r,w in coarseQ.items()}
assert coarseP!=coarseQ
# Model-dependent initial seed laws do not cancel to one shared posterior.
assert {0:F(1,3),1:F(2,3)}!={0:F(2,3),1:F(1,3)}
print(json.dumps({'status':'PASS_EXACT_POSTERIOR_CONTROLS','positive_prefix_model_cases':positive,
 'null_prefix_model_cases':null,'cross_model_comparisons':shared,'nontrivial_seed_updates':nontrivial,
 'checks':{'likelihood_factorization':True,'posterior_cancellation':True,
 'full_history_required_coarse_outcome_counterexample':True,
 'same_seed_prior_required':True,'fresh_future_one_step_factorization':True},
 'scope':'Bounded exact checks. Future iid marginal and shifted-trajectory identification are not inferred from these controls.'},indent=2))
