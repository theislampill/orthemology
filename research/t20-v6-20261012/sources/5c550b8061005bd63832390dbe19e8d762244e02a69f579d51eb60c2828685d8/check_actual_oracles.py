#!/usr/bin/env python3
"""Independent exact controls, generated from complete three-row oracle laws.
The posterior factorization is checked against actual simulated history fibers;
it is not used to construct their probabilities.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict, Counter
import json, hashlib
from pathlib import Path

prior=(F(2,5),F(3,5))
grid=(F(0),F(1,3),F(1,2),F(2,3),F(1))
policies=tuple(product((0,1),repeat=6))
allh=((),)+tuple((x,) for x in product((0,1),repeat=2))+tuple(product(tuple(product((0,1),repeat=2)),repeat=2))
counts=Counter()
assertions=0
def check(label,condition):
    global assertions
    assert condition,label
    counts[label]+=1
    assertions+=1

def action(pol,r,h):
    return pol[r] if not h else pol[2+2*r+h[0][1]]
def compatibility(pol,r,h):
    return all(action(pol,r,h[j+1:])==a for j,(a,y) in enumerate(h))
def feedback_fiber(omega,h):
    return all(omega[2*(len(h)-1-j)+a]==y for j,(a,y) in enumerate(h))
def rowmass(rows,a,y):
    return rows[a] if y else 1-rows[a]
def likelihood(rows,h):
    ans=F(1)
    for a,y in h:ans*=rowmass(rows,a,y)
    return ans

def run():
    across={}
    for rows in product(grid,repeat=2):
        oracle=[]
        for omega in product((0,1),repeat=6):
            w=F(1)
            for t in range(3):
                for a in range(2):w*=rowmass(rows,a,omega[2*t+a])
            if w:oracle.append((omega,w))
        check('full_oracle_law_normalized',sum(w for _,w in oracle)==1)
        for pol in policies:
            joint=defaultdict(F);tailjoint=defaultdict(F);paths={}
            for r in (0,1):
                for omega,w in oracle:
                    h=();paths[(r,omega)]=[h]
                    joint[(r,h)]+=prior[r]*w
                    for t in range(2):
                        a=action(pol,r,h);y=omega[2*t+a];h=((a,y),)+h
                        paths[(r,omega)].append(h)
                        joint[(r,h)]+=prior[r]*w
                    tailjoint[(r,h,omega[4:6])]+=prior[r]*w
            for h in allh:
                cseed=tuple(prior[r] if compatibility(pol,r,h) else F(0) for r in (0,1))
                c=sum(cseed);ell=likelihood(rows,h)
                actual=sum(joint[(r,h)] for r in (0,1))
                check('actual_prefix_factorization',actual==c*ell)
                check('feedback_fiber_mass',sum(w for omega,w in oracle if feedback_fiber(omega,h))==ell)
                for r in (0,1):
                    check('actual_seed_joint_factorization',joint[(r,h)]==cseed[r]*ell)
                if actual:
                    posterior=tuple(joint[(r,h)]/actual for r in (0,1))
                    check('positive_posterior_normalized',sum(posterior)==1)
                    check('posterior_is_normalized_seed_restriction',posterior==tuple(w/c for w in cseed))
                    if posterior!=prior:counts['nontrivial_seed_updates']+=1
                    key=(pol,h)
                    if key in across:check('cross_model_posterior_equality',posterior==across[key])
                    across[key]=posterior
                    # Entire finite feedback sample, including used and unused rows.
                    for r in (0,1):
                        for omega,w in oracle:
                            observed=paths[(r,omega)][len(h)]==h
                            lhs=prior[r]*w/actual if observed else F(0)
                            conditional_feedback=w/ell if feedback_fiber(omega,h) else F(0)
                            check('actual_conditional_seed_feedback_product',lhs==posterior[r]*conditional_feedback)
                    # The genuinely unused third row comes from the original oracle
                    # enumeration, rather than being multiplied onto a posterior.
                    if len(h)==2:
                        for r in (0,1):
                            for tail in product((0,1),repeat=2):
                                raw=rowmass(rows,0,tail[0])*rowmass(rows,1,tail[1])
                                check('enumerated_unused_row_product',tailjoint[(r,h,tail)]/actual==posterior[r]*raw)
                else:
                    counts['null_prefixes_not_normalized']+=1
                    check('null_prefix_has_zero_seed_mass',all(joint[(r,h)]==0 for r in (0,1)))
                    if ell and not c:counts['survival_without_seed_compatibility_is_insufficient']+=1
    # Coarsening away the selected action changes the seed posterior by model.
    def coarse(rows):
        masses=tuple(prior[r]*rows[r] for r in (0,1));z=sum(masses)
        return tuple(w/z for w in masses)
    pp=coarse((F(1,4),F(3,4)));qq=coarse((F(3,4),F(1,4)))
    check('coarse_outcome_counterexample',pp==(F(2,11),F(9,11)) and qq==(F(2,3),F(1,3)) and pp!=qq)
    # A common posterior is not generally the original seed prior.
    check('posterior_need_not_equal_prior',(F(1),F(0))!=prior)
    # Seed-feedback conditional product alone does not make used feedback fresh.
    # Constant first action0 and observed receipt1 fixes oracle[0] to1; both
    # seeds remain possible and independent of this now-degenerate coordinate.
    conditioned=defaultdict(F);event_mass=F(0)
    for r in (0,1):
        for omega in product((0,1),repeat=6):
            if omega[0]==1:
                mass=prior[r]*F(1,64)
                event_mass+=mass
                conditioned[(r,omega[0])]+=mass
    check('used_coordinate_event_has_actual_mass',event_mass==F(1,2))
    for r in (0,1):
        for b in (0,1):
            check('used_coordinate_still_independent_of_seed',
                  conditioned[(r,b)]/event_mass==prior[r]*(F(1) if b else F(0)))
    used_marginal=sum(conditioned[(r,1)] for r in (0,1))/event_mass
    check('conditional_independence_does_not_imply_fresh_marginal',
          used_marginal==1 and used_marginal!=F(1,2))
    # Newest-first histories require the old prefix on the right.
    old=((0,0),);new=((1,1),)
    pi=lambda h:h[0][1] if h else 0
    check('wrong_history_append_order_counterexample',pi(new+old)!=pi(old+new))
    # State-consistent restart must use the last observed state, not s0.
    s0=0;last_observed=1
    check('wrong_markov_restart_state_counterexample',last_observed!=s0)
    result={'status':'PASS','arithmetic':'exact Fraction; no sampled simulations',
            'policies':len(policies),'row_models':len(grid)**2,'seed_prior':[str(x) for x in prior],
            'oracle_rows':3,'all_prefix_lengths':[0,1,2],
            'total_assertions':assertions,'counts':dict(sorted(counts.items())),
            'scope':'Finite corroboration only. The general fresh infinite-tail marginal and shifted trajectory law remain outside the author packet and this review.',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':run()
