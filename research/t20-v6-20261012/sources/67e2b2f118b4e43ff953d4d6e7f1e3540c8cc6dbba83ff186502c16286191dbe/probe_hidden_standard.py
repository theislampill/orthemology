"""Hidden target standards separate sure, finite-memory AS, and general AS.

The empirical model is declared iid synthetic Bernoulli acquisition. Nothing here
establishes actual source independence, a real norm, or permission to guess.
"""
from itertools import product
from fractions import Fraction as F
from math import comb
import json,time
from restoration import classify_chain


def pure_controllers(max_memory=3):
    counts=[]
    for size in range(1,max_memory+1):
        tested=win0=win1=both=0
        for actions in product((0,1),repeat=size):
            bad0={m for m in range(size) if actions[m]!=0}
            bad1={m for m in range(size) if actions[m]!=1}
            for updates in product(range(size),repeat=2*size):
                kernels=[]
                for bias in (F(1,3),F(2,3)):
                    kernel={}
                    for m in range(size):
                        row={}
                        for bit,prob in ((0,1-bias),(1,bias)):
                            dest=updates[2*m+bit]
                            row[dest]=row.get(dest,F(0))+prob
                        kernel[m]=row
                    kernels.append(kernel)
                w0=classify_chain(kernels[0],{0},bad0)['almost_sure']
                w1=classify_chain(kernels[1],{0},bad1)['almost_sure']
                tested+=1;win0+=w0;win1+=w1;both+=w0 and w1
        assert both==0
        counts.append({'memory_states':size,'controllers':tested,
                       'AS_environment_0':win0,'AS_environment_1':win1,'AS_both':both})
    return counts


def randomized_two_memory():
    choices=(frozenset({0}),frozenset({1}),frozenset({0,1}))
    tested=both=0
    for action_supports in product(choices,repeat=2):
        states={(m,a) for m in range(2) for a in action_supports[m]}
        for supports in product(choices,repeat=8):
            kernels=[]
            for bias in (F(1,3),F(2,3)):
                kernel={}
                for m,a in states:
                    row={}
                    for bit,bp in ((0,1-bias),(1,bias)):
                        memory_support=supports[4*m+2*a+bit]
                        for nm in memory_support:
                            for na in action_supports[nm]:
                                prob=bp/F(len(memory_support)*len(action_supports[nm]))
                                row[nm,na]=row.get((nm,na),F(0))+prob
                    kernel[m,a]=row
                kernels.append(kernel)
            initial={(0,a) for a in action_supports[0]}
            w0=classify_chain(kernels[0],initial,{(m,a) for m,a in states if a!=0})['almost_sure']
            w1=classify_chain(kernels[1],initial,{(m,a) for m,a in states if a!=1})['almost_sure']
            tested+=1;both+=w0 and w1
    assert both==0
    return {'memory_states':2,'qualitative_support_controllers':tested,'AS_both':both,
            'probability_scope':'Uniform positive weights represent each support pattern; finite-chain AS depends only on support.'}


def majority_error(m):
    n=2*m
    # Tie breaks toward standard 0. The worse error is under environment 1;
    # symmetry expresses it as P_{1/3}(number of ones >= m).
    return sum(F(comb(n,k)*2**(n-k),3**n) for k in range(m,n+1))


def finite_classifiers():
    values=[]
    for target in (F(1,10),F(1,100),F(1,1000),F(1,10**6)):
        m=1
        while F(8,9)**m>target:m+=1
        exact=majority_error(m)
        assert exact<=F(8,9)**m<=target
        values.append({'requested_error_upper_bound':str(target),'samples':2*m,
                       'chernoff_bound':float(F(8,9)**m),'exact_worst_error':float(exact),
                       'finite_counter_state_upper_bound':(2*m+1)*(2*m+2)//2+2})
    for m in range(1,61):
        assert majority_error(m)<=F(8,9)**m
    return {'positive_error_classifiers':values,'exact_binomial_bound_checks':60,
            'zero_error_finite_declaration':'Impossible by finite-prefix mutual absolute continuity.'}


def main():
    start=time.monotonic()
    result={'pure_finite_memory_Moore_convention':pure_controllers(),
            'randomized_finite_memory':randomized_two_memory(),
            'limit_sure_finite_classifier':finite_classifiers(),
            'general_AS_policy':'After 2m fresh iid samples choose the majority standard; Chernoff errors sum, so only finitely many mistakes almost surely.',
            'root_copy_deletion':'Copying one acquired bit gives two common positive-mass infinite words; no AS policy can satisfy opposite eventual-action targets.',
            'authority_deletion':'If only response h is eligible under h, robust support-based licensing permits neither guess at any finite history; a licensed abstain never restores.',
            'scope':'Finite-controller probes support the general support-BSCC proof. Infinite-time AS uses the stated iid model and mathematical probability proof, not simulation.'}
    result['elapsed_seconds']=round(time.monotonic()-start,3)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
