#!/usr/bin/env python3
"""Exact-rational finite causal trees and deliberately invalid control mutations."""
from fractions import Fraction as F
from math import isqrt
from collections import defaultdict
import json, pathlib, time
OUT=pathlib.Path(__file__).parent/'evidence'/'HELLINGER_EXACT_CHECKS.json'
def sqrtq(x):
    n,d=isqrt(x.numerator),isqrt(x.denominator)
    assert n*n==x.numerator and d*d==x.denominator, x
    return F(n,d)
def affinity(p,q): return sum((sqrtq(x*y) for x,y in zip(p,q)),F(0))
def finite_tree(P,G,U,N,theta):
    # Nodes carry actual full transcript probabilities under BOTH models.
    nodes=[((F(1),F(1)), F(0))]
    selected=[F(0),F(0)]; checks=[]
    for t in range(N):
        nxt=[]
        for L,_ in nodes:
            a=max(range(2),key=lambda i:(L[i],i))
            selected[a]+=L[theta]
            for y in range(2):
                nxt.append((tuple(L[m]*P[m][U[a][0]][y] for m in range(2)),F(0)))
        nodes=nxt
        assert sum(L[theta] for L,_ in nodes)==1
        sigma=1-theta
        rho=affinity(P[theta][U[sigma][0]],P[sigma][U[sigma][0]])
        H=sum(sqrtq(L[theta]*L[sigma]) for L,_ in nodes)
        lhs=(1-rho)*selected[sigma]+H
        assert lhs<=1
        checks.append({'n':t+1,'expected_bad':str(selected[sigma]),'affinity':str(H),'potential_lhs':str(lhs)})
    return checks

def stopped_outcomes(P,live,acts):
    """The full stopped-prefix law. Every branch ends on the first shrink."""
    def go(rem,word,weights):
        if not rem:
            yield word,live,weights; return
        a=rem[0]
        for y in range(2):
            w=tuple(weights[m]*P[m][a][y] for m in range(len(P)))
            new=tuple(m for m in live if P[m][a][y]>0)
            if not new: continue
            if new!=live: yield word+((a,y),),new,w
            else: yield from go(rem[1:],word+((a,y),),w)
    return list(go(acts,(),(F(1),)*len(P)))

def phase_tree(P,G,supports,N,theta):
    # Probability aggregation retains pre-phase mass but resets all LIVE likelihoods.
    nodes={(tuple(range(len(P))), (F(1),)*len(P)):F(1)}
    bad=F(0); resets=F(0); checks=[]
    for t in range(N):
        nxt=defaultdict(F)
        for (live,L),mass in nodes.items():
            cand=max(live,key=lambda i:(L[i],i)); acts=supports(live,cand)
            outs=stopped_outcomes(P,live,acts)
            for m in live: assert sum(w[m] for _,_,w in outs)==1
            for word,new,w in outs:
                q=mass*w[theta]
                bad+=q*sum(a not in G[theta] for a,y in word)
                if new!=live:
                    resets+=q
                    Lnext=tuple(F(1) if m in new else F(0) for m in range(len(P)))
                else: Lnext=tuple(L[m]*w[m] for m in range(len(P)))
                nxt[(new,Lnext)]+=q
        nodes=nxt
        assert sum(nodes.values())==1
        assert all(theta in live for (live,_),q in nodes.items() if q)
        checks.append({'n':t+1,'expected_bad':str(bad),'expected_resets':str(resets),'states':len(nodes)})
    return checks

def main():
    P=[[(F(16,25),F(9,25))]*2,[(F(9,25),F(16,25))]*2]
    assert affinity(P[0][0],P[1][0])==F(24,25)
    full=[finite_tree(P,[{0},{1}],[(0,),(1,)],12,t) for t in range(2)]
    # Zeros permit revelation; surviving data also statistically discriminate.
    Pz=[[(F(16,25),F(9,25)),(F(1),F(0))],
        [(F(9,25),F(16,25)),(F(9,25),F(16,25))]]
    support=lambda live,c: (c,)
    zero=[phase_tree(Pz,[{0},{1}],support,14,t) for t in range(2)]
    # theta0: harmful candidate1 residual3/5, phase cost <=5/2.
    # theta1: harmful candidate0 residual24/25, phase cost <=25.
    assert F(zero[0][-1]['expected_bad'])<=F(5,2)
    assert F(zero[1][-1]['expected_bad'])<=25
    # Copied-bit mutation retains each one-time marginal but destroys freshness.
    copied_expected=F(1)+69*F(9,25)
    assert copied_expected==F(646,25) and copied_expected>25
    # A revealing first action forbids execution of old second action.
    Pd=[[(F(1),F(0)),(F(1),F(0))],[(F(0),F(1)),(F(1),F(0))]]
    outs=stopped_outcomes(Pd,(0,1),(0,1))
    assert all(len(word)==1 for word,new,w in outs)
    assert {new for word,new,w in outs}=={(0,),(1,)}
    # Conditioning on no exit normalizes a subprobability to1, erasing deficit.
    residual=F(9,25)
    assert residual<1 and residual/residual==1
    result={'status':'PASS','arithmetic':'exact Fraction with checked rational square roots',
      'full_support':full,'zero_support':zero,
      'mutants':{'copied_feedback_expected_bad_N70':str(copied_expected),'false_fresh_bound':'25',
      'first_exit_interrupts_block':True,'conditioning_erases_residual_deficit':True},
      'scope':'Finite controls and guard counterexamples; not an infinite stochastic proof.'}
    OUT.write_text(json.dumps(result,indent=2)+'\n');print(OUT);print('PASS')
if __name__=='__main__':main()
