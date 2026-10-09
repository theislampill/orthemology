"""Finite controls for approximation-oracle and coefficient-scope boundaries.
Limit learners below return provisional prefixes, never a stabilization warrant.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations_with_replacement,islice
from collections import Counter
from countable_support import probability,failure,decode_support
from gcd_decoder import histograms_of_weight,decode_gcd,ResourceInconclusive


@dataclass(frozen=True)
class Approximation:
    profile: int|None
    center: Q
    error: Q


def positive_prediction(model,profile=None):
    return probability({e:n for e,n in model.items() if profile is None or e&profile==e})


def guarded_prediction(model,profile):
    answer=Q(1)
    for (p,n),count in model.items():
        if p&profile==p and not n&profile:answer*=failure(p)**count
    return answer


def positive_candidates():
    weight=0
    while True:
        yield from histograms_of_weight(weight);weight+=1


def guarded_candidates():
    """A slow effective enumeration, not an efficient guarded learner."""
    budget=0
    while True:
        universe=(1<<budget)-1
        kinds=[(p,n) for p in range(1,universe+1) for n in range(universe+1) if not p&n]
        for size in range(budget+1):
            for entries in combinations_with_replacement(kinds,size):yield dict(Counter(entries))
        budget+=1


def approximate(value,precision,sign=1):
    error=Q(1,1<<precision)
    center=min(Q(1),max(Q(0),value+sign*error/2))
    return center,error


def positive_learning_prefix(approximation_oracle,stages):
    enumeration=positive_candidates();considered=[];observations=[];outputs=[]
    for stage in range(1,stages+1):
        considered.append(next(enumeration))
        center,error=approximation_oracle(stage+2)
        observations.append(Approximation(None,center,error))
        candidate=next((m for m in considered if all(abs(probability(m)-o.center)<=o.error for o in observations)),None)
        outputs.append(candidate)
    return outputs


def guarded_learning_prefix(approximation_oracle,stages):
    enumeration=guarded_candidates();considered=[];observations=[];outputs=[]
    for stage in range(1,stages+1):
        considered.append(next(enumeration))
        for profile in range(1,stage+1):
            center,error=approximation_oracle(profile,stage+2)
            observations.append(Approximation(profile,center,error))
        candidate=next((m for m in considered if all(abs(guarded_prediction(m,o.profile)-o.center)<=o.error for o in observations)),None)
        outputs.append(candidate)
    return outputs


def inside_value_gap(exact_full_probability,max_inside_count=None):
    """Candidate-dependent finite gap; may be extremely expensive."""
    counts,_=decode_gcd(exact_full_probability)
    root_mask=0
    for e in counts:root_mask|=e
    if not root_mask:return {'root_mask':0,'count_bound':0,'gap':None,'values':(Q(1),)}
    largest_failure=failure(root_mask);current=Q(1);bound=0
    while current*largest_failure>=exact_full_probability:
        if max_inside_count is not None and bound+1>max_inside_count:
            raise ResourceInconclusive('Candidate-specific inside-count bound exceeds the supplied budget.')
        current*=largest_failure;bound+=1
    supports=[s for s in range(1,root_mask+1) if s&root_mask==s]
    values=set()
    for size in range(bound+1):
        for entries in combinations_with_replacement(supports,size):
            value=probability(dict(Counter(entries)))
            if value>=exact_full_probability:values.add(value)
    if exact_full_probability not in values:raise AssertionError('Decoded candidate missing from inside class.')
    gap=min(value-exact_full_probability for value in values if value>exact_full_probability)
    return {'root_mask':root_mask,'count_bound':bound,'gap':gap,'values':tuple(sorted(values))}


def one_effect_absence(model,profile,rates):
    answer=Q(1)
    for positive,count in model.items():
        if positive&profile!=positive:continue
        success=Q(1)
        for i,p in enumerate(rates):
            if positive>>i&1:success*=p
        answer*=(1-success)**count
    return answer
