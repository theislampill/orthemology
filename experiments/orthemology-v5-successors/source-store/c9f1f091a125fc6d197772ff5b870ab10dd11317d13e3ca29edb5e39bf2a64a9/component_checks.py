"""Independent pre-source adversarial specification tests."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
REFERENCE=ROOT/'tranche18/research/hidden-change/reference-v1'
EFFICIENT=ROOT/'tranche18/research/hidden-change/efficient-v1'
sys.path[:0]=[str(EFFICIENT),str(REFERENCE)]
from oracle import (fixture,raw_model,full_pairs,subsets,all_end_components,
                    maximal_allowed,qualifying,target_union)
from model import validate_model
from mec import maximal_components
from efficient import known_components,uncertain_components


def verify_components(inp):
    model=validate_model(raw_model(inp))
    all_ends={theta:all_end_components(inp,theta) for theta in (0,1)}
    for allowed in subsets(full_pairs(inp)):
        for theta in (0,1):
            actual=maximal_components(model,theta,allowed)
            assert isinstance(actual,tuple)
            assert actual==tuple(sorted(set(actual)))
            actual_sets=frozenset(frozenset(c) for c in actual)
            assert actual_sets==maximal_allowed(all_ends[theta],allowed),(inp,theta,allowed,actual)
            for c in actual:
                assert c==tuple(sorted(set(c))) and frozenset(c)<=allowed
            for c in all_ends[theta]:
                if c<=allowed: assert any(c<=got for got in actual_sets)
            sources=[target_union((c,)) for c in actual_sets]
            assert all(not (sources[i]&sources[j]) for i in range(len(sources)) for j in range(i))
        for theta,uncertain in ((1,False),(0,True),(1,True)):
            actual=uncertain_components(model,theta,allowed) if uncertain else known_components(model,allowed)
            assert actual==tuple(sorted(set(actual)))
            assert all(frozenset(c)<=allowed and qualifying(inp,theta,frozenset(c),uncertain) for c in actual)
            expected=[c for c in all_ends[theta] if c<=allowed and qualifying(inp,theta,c,uncertain)]
            assert target_union(actual)==target_union(expected),(inp,theta,allowed,actual,expected)
    return model

