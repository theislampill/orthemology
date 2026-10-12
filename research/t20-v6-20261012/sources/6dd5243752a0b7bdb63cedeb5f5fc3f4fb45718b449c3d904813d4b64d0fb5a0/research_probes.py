"""Finite exact checks; no empirical or proof-assistant claim.

The atomic and conjunction reference oracle uses linear feasibility bounds,
not the prototype's sign-cell enumeration.
"""
import copy
import itertools as it
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

from gap_disclosure import analyze, build_certificate, verify_certificate
from test_gap_disclosure import base, regime, preference


def feasible(inequalities, low, high):
    """Constraints a*x+b > 0 or >= 0; exact interval intersection."""
    lo,hi,lo_closed,hi_closed=low,high,True,True
    for a,b,strict in inequalities:
        if a==0:
            if not (b>0 if strict else b>=0): return False
            continue
        root=-b/a
        if a>0:
            if root>lo: lo,lo_closed=root,not strict
            elif root==lo: lo_closed=lo_closed and not strict
        else:
            if root<hi: hi,hi_closed=root,not strict
            elif root==hi: hi_closed=hi_closed and not strict
    return lo<hi or (lo==hi and lo_closed and hi_closed)


def reference_conjunction(atoms,low,high):
    yes=feasible(atoms,low,high)
    no=any(feasible([(-a,-b,not strict)],low,high) for a,b,strict in atoms)
    if not yes and not no: return 'NO_ADMISSIBLE_EXTENSION'
    return 'DISAGREEMENT' if yes and no else 'INVARIANT_TRUE' if yes else 'INVARIANT_FALSE'


def atomic_probes():
    counts=Counter(); checks=0
    grid=[F(i,8) for i in range(1,8)]
    for x0,x1,y0,y1 in it.product(range(-2,3),repeat=4):
        d=base({'a':[x0,x1],'b':[y0,y1]})
        slope=F(x0-y0-x1+y1); intercept=F(x1-y1)
        for low,high in it.combinations_with_replacement(grid,2):
            r=regime(d,str(low),str(high))
            for strict in [False,True]:
                actual=analyze(d,r,preference(strict=strict))['status']
                expected=reference_conjunction([(slope,intercept,strict)],low,high)
                assert actual==expected,(d,r,strict,actual,expected)
                checks+=1; counts[actual]+=1
    return {'checks':checks,'statuses':dict(counts),'mismatches':0}


def conjunction_probes():
    checks=0; counts=Counter()
    # Each affine a*x+b is realized by a profile (a+b,b) compared with zero.
    slopes=list(it.product(range(-2,3),repeat=2))
    for (a,b),(c,d),s,t in it.product(slopes,slopes,[False,True],[False,True]):
        data=base({'p':[a+b,b],'q':[c+d,d],'zero':[0,0]})
        target={'op':'and','args':[preference('p','zero',s),preference('q','zero',t)]}
        for low,high in [(F(1,4),F(3,4)),(F(1,2),F(1,2)),(F(3,4),F(1,4))]:
            result=analyze(data,regime(data,str(low),str(high)),target)['status']
            expected=reference_conjunction([(F(a),F(b),s),(F(c),F(d),t)],low,high)
            assert result==expected,(a,b,c,d,s,t,result,expected)
            checks+=1; counts[result]+=1
    return {'checks':checks,'statuses':dict(counts),'mismatches':0}


def dynamic_probes():
    tested=positive=bound_checks=fixed_cases=0
    for n in range(1,5):
        for values in it.product(range(3),repeat=n):
            maximum=max(values); m={i for i,v in enumerate(values) if v==maximum}
            for g in it.product(range(n),repeat=n):
                tested+=1
                if not (all(values[g[x]]>values[x] for x in range(n) if x not in m)
                        and all(g[x] in m for x in m)): continue
                positive+=1
                for x in range(n):
                    steps=0
                    while x not in m:
                        x=g[x]; steps+=1
                        assert steps<=n-len(m)
                    bound_checks+=1
                if all(g[x]==x for x in m):
                    fixed_cases+=1
                    assert {x for x in range(n) if g[x]==x}==m
    # Fixed points = maxima, but a nonmaximal two-cycle prevents convergence.
    assert {i for i in range(3) if (0,2,1)[i]==i}=={0}
    x=1
    for _ in range(10): x=(0,2,1)[x]; assert x!=0
    return {'map_value_pairs':tested,'strict_ascent_cases':positive,
            'trajectory_bounds_checked':bound_checks,'fix_equals_max_cases':fixed_cases,
            'fixed_equals_max_without_convergence_counterexample':
            {'values':[1,0,0],'transition':[0,2,1]},'mismatches':0}


def certificates_and_examples():
    d=base(); r=regime(d); t=preference(); cert=build_certificate(d,r,t)
    assert verify_certificate(d,r,t,cert)['accepted']
    rejected=0
    for key in cert:
        forged=copy.deepcopy(cert); forged.pop(key)
        assert not verify_certificate(d,r,t,forged)['accepted']; rejected+=1
        forged=copy.deepcopy(cert); forged[key]='tampered'
        assert not verify_certificate(d,r,t,forged)['accepted']; rejected+=1
    forged=copy.deepcopy(cert); forged['world_authority']=True
    assert not verify_certificate(d,r,t,forged)['accepted']; rejected+=1
    # Fixed game skeleton, two possible self-interested additive evaluations.
    equilibria={}
    for alpha in [F(1,4),F(1,2),F(3,4)]:
        pay=lambda action: alpha if action==0 else 1-alpha
        equilibria[str(alpha)]=[list(a) for a in it.product(range(2),repeat=2)
            if all(pay(a[i])>=pay(1-a[i]) for i in range(2))]
    assert equilibria=={'1/4':[[1,1]],'1/2':[[0,0],[0,1],[1,0],[1,1]],'3/4':[[0,0]]}
    # Scalar likelihood-ratio sufficiency is exact for the fixed binary model.
    correct_lr=F(9)*F(1,9); naive_lr=F(9)*F(9)*F(1,9)
    post=lambda lr: lr/(1+lr)
    assert post(correct_lr)==F(1,2) and post(naive_lr)==F(9,10)
    # Coordinate swap + action swap acts transitively on the two actions.
    assert all(1-choice!=choice for choice in [0,1])
    assert (F(1,2),F(1,2))[::-1]==(F(1,2),F(1,2))
    example={'base':d,'regime':r,'target':t,'certificate':cert}
    Path('example_certificate.json').write_text(json.dumps(example,indent=2)+'\n')
    return {'certificate_mutations_rejected':rejected,
            'fixed_geometry_pure_nash_sets':equilibria,
            'duplicate_source_posteriors':{'correct':str(post(correct_lr)),'naive':str(post(naive_lr))},
            'symmetry':{'equivariant_single_action_selection':False,'uniform_weights_invariant':True}}


if __name__=='__main__':
    results={'status':'EXACT_FINITE_RESEARCH_PROBES_NOT_KERNEL_PROOF',
             'atomic':atomic_probes(),'conjunction':conjunction_probes(),
             'dynamics':dynamic_probes(),'examples':certificates_and_examples()}
    Path('research_probe_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
