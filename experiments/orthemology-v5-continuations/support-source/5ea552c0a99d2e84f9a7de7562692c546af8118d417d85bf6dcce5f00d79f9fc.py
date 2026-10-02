#!/usr/bin/env python3
"""Reviewer-written exact structural checks, independent of the author scripts.

Finite corroboration only. The general proof relies on the inspected arithmetic
argument and Azarpendar–Jafari Theorem 1.1, not these computations.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import gcd
import hashlib
import json


def require(test, reason):
    if not test:
        raise ValueError(reason)


@lru_cache(None)
def integer_partitions(n, minimum=1):
    if n == 0:
        return ((),)
    return tuple((first,)+tail for first in range(minimum,n+1)
                 for tail in integer_partitions(n-first,first))


def direct_adversary_profile(parts):
    """Maximise minimum corruption fraction by budget convolution, no floors."""
    profile=[Q(1)]
    for size in parts:
        next_profile=[Q(-1)]*(len(profile)+size)
        for used,old in enumerate(profile):
            for corrupt in range(size+1):
                candidate=min(old,Q(corrupt,size))
                if candidate>next_profile[used+corrupt]:
                    next_profile[used+corrupt]=candidate
        profile=next_profile
    return profile


def formula(n,b,m,offset=None):
    if m>b:
        return Q(0)
    offset=m-1 if offset is None else offset
    return max(Q((q*(b-m+1)+offset)//n,q) for q in range(1,n-m+2))


def transfer(parts,a,q,N):
    """Independently execute the contradiction, checking every transition."""
    require(0<a<q and gcd(a,q)==1,"transfer requires a reduced positive fraction below 1")
    parts=list(parts)
    n=sum(parts); m=len(parts); delta=a*n-q*N
    require(delta>=m,"not a purported bad optimal-threshold instance")
    shift=(-pow(a,-1,q))%q
    require(1<=shift<q,"invalid transfer amount")
    steps=0; positive_steps=0; zero_steps=0
    while True:
        quotients=[a*s//q for s in parts]
        residues=[a*s%q for s in parts]
        excess=sum(quotients)-N
        zeros=[i for i,r in enumerate(residues) if r==0]
        require(excess>=0,"threshold ceased to be feasible")
        if excess>=len(zeros):
            break
        donor=zeros[0]
        require(parts[donor]%q==0 and parts[donor]>=q,"zero donor is not a positive multiple of q")
        if excess:
            require(len(zeros)>=2,"missing zero recipient")
            recipient=zeros[1]
            predicted_excess=excess-1; predicted_zeros=len(zeros)-2
            positive_steps+=1
        else:
            eligible=[i for i,r in enumerate(residues) if r>=2]
            require(eligible,"residue sum does not supply required recipient")
            recipient=eligible[0]
            predicted_excess=excess; predicted_zeros=len(zeros)-1
            zero_steps+=1
        before_sum=sum(residues)
        old_recipient_residue=residues[recipient]
        parts[donor]-=shift; parts[recipient]+=shift; steps+=1
        after_residues=[a*s%q for s in parts]
        require(all(s>=1 for s in parts) and sum(parts)==n and len(parts)==m,"transfer changed the partition domain")
        require(after_residues[donor]==1 and after_residues[recipient]==(old_recipient_residue-1)%q,"wrong modular update")
        require(sum(a*s//q for s in parts)-N==predicted_excess,"incorrect floor-excess update")
        require(sum(r==0 for r in after_residues)==predicted_zeros,"incorrect zero count update")
        require(sum(after_residues)==before_sum+(q if excess else 0),"residue sum update failed")
        require(steps<=m,"nonterminating residue process")
    # Explicit left perturbation works even if the process stops immediately.
    eta=Q(1,2*q*max(parts))
    lower=Q(a,q)-eta
    require(0<=lower<Q(a,q),"invalid left perturbation")
    require(sum((lower*s).__floor__() for s in parts)>=N,"left perturbation failed")
    return steps,positive_steps,zero_steps,tuple(parts),lower


def run():
    counts={"partitions_directly_evaluated":0,"all_budget_partition_comparisons":0,
            "global_parameter_cases":0,"attained_denominator_checks":0,
            "partition_threshold_equivalence_cases":0,"exhaustive_residue_inputs":0,
            "positive_excess_transfers":0,"zero_excess_transfers":0,
            "immediate_left_perturbations":0,"copy_parameter_cases":0,
            "constructed_copy_edges":0}
    digest=hashlib.sha256(); examples=[]; transfer_examples={}
    for n in range(1,23):
        best={}
        for parts in integer_partitions(n):
            m=len(parts)
            profile=direct_adversary_profile(parts)
            counts["partitions_directly_evaluated"]+=1
            for b in range(n):
                key=(b,m); candidate=profile[b]
                if key not in best or candidate<best[key][0]:
                    best[key]=(candidate,parts)
                counts["all_budget_partition_comparisons"]+=1
            # Check both threshold equivalences against direct min-max values
            # at exact breakpoints and representatives of intervening cells.
            if n<=10:
                breaks=sorted({Q(c,s) for s in parts for c in range(s+1)})
                probes=breaks+[(x+y)/2 for x,y in zip(breaks,breaks[1:])]
                for t in probes:
                    for b in range(m-1,n):
                        ceil_sum=sum(-((-t*s).__floor__()) for s in parts)
                        require((profile[b]>=t)==(ceil_sum<=b),"ceil/risk inequality reversed")
                        if t<1:
                            floor_sum=sum((t*s).__floor__() for s in parts)
                            require((profile[b]<=t)==(floor_sum>=b-m+1),"strict-cost floor criterion fails")
                        counts["partition_threshold_equivalence_cases"]+=1
        for (b,m),(value,parts) in best.items():
            expected=formula(n,b,m)
            require(value==expected,("formula vs direct allocation",n,b,m,value,expected))
            counts["global_parameter_cases"]+=1
            if value:
                a,q=value.numerator,value.denominator;N=b-m+1
                require(0<a<q and 0<=a*n-q*N<=m-1,"optimal residue inequality fails")
                require(q<=n-m+1 and any(s%q==0 for s in parts),"attained reduced denominator fails")
                require(value<=Q(b,n),"weighted-average upper bound fails")
                counts["attained_denominator_checks"]+=1
            if (n,b,m) in ((7,3,2),(11,5,2),(9,4,3),(7,2,2),(12,5,3),(20,8,5)):
                examples.append({"u":n,"b":b,"M":m,"value":str(value),"partition":parts})
            digest.update(repr((n,b,m,value,parts)).encode())

    # Exhaustive residue counter-hypotheses, not random probability rows.
    # Include E=z cases where the immediate left perturbation is essential.
    for n in range(3,21):
        for parts in integer_partitions(n):
            m=len(parts)
            if not 2<=m<=8:
                continue
            for q in range(2,min(10,max(parts)+1)):
                for a in range(1,q):
                    if gcd(a,q)!=1:
                        continue
                    f=sum(a*s//q for s in parts);z=sum(a*s%q==0 for s in parts)
                    for excess in range(z+1):
                        N=f-excess;b=N+m-1
                        if N<1 or b>=n or a*n-q*N<m:
                            continue
                        result=transfer(parts,a,q,N)
                        steps,positive,zero,out,lower=result
                        counts["exhaustive_residue_inputs"]+=1
                        counts["positive_excess_transfers"]+=positive
                        counts["zero_excess_transfers"]+=zero
                        counts["immediate_left_perturbations"]+=(steps==0)
                        for label,condition in [("positive_excess",positive>0),("zero_excess",zero>0),("immediate",steps==0)]:
                            if condition and label not in transfer_examples:
                                transfer_examples[label]={"input_partition":parts,"a":a,"q":q,"N":N,
                                                          "output_partition":out,"smaller_threshold":str(lower)}
                        digest.update(repr((parts,a,q,N,result)).encode())
    require(all(counts[x]>0 for x in ("positive_excess_transfers","zero_excess_transfers","immediate_left_perturbations")),"missing residue branch coverage")

    # Test every admissible numerator as well as every denominator, instead of
    # checking only the optimum. Build actual disjoint copy edges canonically.
    repeated_projection_example=None
    for n in range(2,26):
        for b in range(1,n):
            k=n-b
            for m in range(1,b+1):
                N=b-m+1
                for q in range(2,n-m+2):
                    for a in range(1,q):
                        delta=a*n-q*N
                        chromatic_num=q*(b+1)-a*n
                        chromatic=(chromatic_num+q-2)//(q-1)
                        require((chromatic>m)==(delta<=m-1),"chromatic strictness equivalence fails")
                        if delta>m-1:
                            continue
                        s=q-a; expanded=s*n
                        require(1<=s<=q and q>=2 and k>=1 and expanded>=q*k,"source hypothesis violation")
                        require(chromatic==(expanded-q*(k-1)+q-2)//(q-1)>m,"source substitution mismatch")
                        counts["copy_parameter_cases"]+=1
                        if n<=10:
                            # Consecutive groups of k roots cyclically use each
                            # root at most ceil(q*k/n)<=s times. Tag occurrences
                            # as distinct copies; each individual group has no
                            # repeated original label because k<=n.
                            used=[0]*n;vertices=[];projections=[]
                            for j in range(q):
                                vertex=[]
                                for r in range(j*k,(j+1)*k):
                                    root=r%n;vertex.append((root,used[root]));used[root]+=1
                                require(len({i for i,c in vertex})==k,"nontransversal expanded vertex")
                                vertices.append(tuple(vertex));projections.append(frozenset(i for i,c in vertex))
                            require(len({copy for vertex in vertices for copy in vertex})==q*k,"copy edge not disjoint")
                            require(max(used)<=s and all(q-c>=a for c in used),"projection multiplicity/complement lower bound fails")
                            require(all(len(projection)==k for projection in projections),"projection changes corruption cardinality")
                            if len(set(projections))<q and repeated_projection_example is None:
                                repeated_projection_example={"u":n,"b":b,"M":m,"a":a,"q":q,
                                                             "projected_sets":[sorted(p) for p in projections]}
                            counts["constructed_copy_edges"]+=1
    require(repeated_projection_example is not None,"missing repeated-projection control")

    # Invalid variants have concrete, exact counterexamples.
    bad=formula(4,2,2,offset=2)
    true=formula(4,2,2)
    require((bad,true)==(Q(1,2),Q(1,3)),"delta<=M mutation not caught")
    require((2*(2+1)-1*4+2-2)//(2-1)==2,"bad threshold should yield only M colors")
    # q copies instead of q-a copies: two disjoint expanded sets may project
    # to the same two roots. Their complements have mass zero under delta_0.
    wrong_vertices=[[(0,0),(1,0)],[(0,1),(1,1)]]
    require(len({p for v in wrong_vertices for p in v})==4,"wrong-copy example not an expanded edge")
    wrong_complement_sum=sum(0 not in {r for r,c in v} for v in wrong_vertices)
    require(wrong_complement_sum==0<1,"wrong-copy capacity mutant not rejected")
    try:
        transfer((3,4),2,6,2)
    except ValueError as error:
        require("reduced" in str(error),"noncoprime input rejected for wrong reason")
    else:
        raise ValueError("unreduced residue arithmetic was accepted")
    require(formula(7,2,2)==Q(1,6),"composite uniformity test failed")
    zero_endpoints=0
    for n in range(1,31):
        for b in range(n):
            for m in {b+1,n+1,2*n+3}:
                require(formula(n,b,m)==0,"zero endpoint including excess messages fails")
                zero_endpoints+=1
    return {"status":"PASS","scope":"Finite exact structural corroboration; no sampling of continuous codebooks and no substitute for the external theorem",
            "counts":counts,"zero_endpoint_cases":zero_endpoints,"examples":examples,
            "transfer_examples":transfer_examples,"repeated_projection_example":repeated_projection_example,
            "negative_controls":{"delta_le_M_instead_of_M_minus_1":{"u":4,"b":2,"M":2,"false_value":str(bad),"actual_partition_value":str(true)},
                                 "q_copies_instead_of_q_minus_a":"rejected by repeated projected sets with zero complement mass",
                                 "unreduced_modular_transfer":"explicitly rejected",
                                 "source_prime_only_restriction":{"u":7,"b":2,"M":2,"required_optimal_denominator":6}},
            "arithmetic_sha256":digest.hexdigest()}


if __name__=="__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
