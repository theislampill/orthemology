"""Independent complete finite replay, with exact allowed-subset MEC tests."""
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
REFERENCE=ROOT/'tranche18/research/hidden-change/reference-v1'
EFFICIENT=ROOT/'tranche18/research/hidden-change/efficient-v1'
PRIOR=HERE.parent/'hidden-change-reference/oracle.py'
spec=importlib.util.spec_from_file_location('prior_independent_oracle',PRIOR)
prior=importlib.util.module_from_spec(spec);sys.modules[spec.name]=prior;spec.loader.exec_module(prior)
sys.path[:0]=[str(EFFICIENT),str(REFERENCE)]
from oracle import (raw_model,subsets,full_pairs,all_end_components,maximal_allowed,qualifying,target_union)
from model import validate_model
from certificates import Positive,Negative,check_positive,check_negative as original_negative
from efficient import known_components,uncertain_components,known_operator,uncertain_operator,solve
from mec import maximal_components
from negative import check_negative


def census(name,generator,expected_count):
    start=time.monotonic()
    result=dict(name=name,models=0,positive=0,negative=0,known_operator_comparisons=0,
                uncertain_operator_comparisons=0,mec_comparisons=0,end_component_coverage_checks=0,
                target_union_comparisons=0,representative_soundness_checks=0,signed_body_checks=0)
    for index,inp in enumerate(generator()):
        try:
            model=validate_model(raw_model(inp))
            expected_regions=prior.regions(inp)
            if inp.a==1: assert expected_regions==prior.one_action_chain_regions(inp)
            for k in subsets(range(inp.n)):
                assert known_operator(model,k)==prior.eligible_known(inp,k)
                result['known_operator_comparisons']+=1
                for w in subsets(range(inp.n)):
                    assert uncertain_operator(model,k,w)==prior.eligible_uncertain(inp,k,w)
                    result['uncertain_operator_comparisons']+=1
            ends={theta:all_end_components(inp,theta) for theta in (0,1)}
            good={(theta,uncertain):tuple(c for c in ends[theta] if qualifying(inp,theta,c,uncertain))
                  for theta,uncertain in ((1,False),(0,True),(1,True))}
            for allowed in subsets(full_pairs(inp)):
                for theta in (0,1):
                    actual=maximal_components(model,theta,allowed)
                    assert isinstance(actual,tuple) and actual==tuple(sorted(set(actual)))
                    assert all(c and c==tuple(sorted(set(c))) for c in actual)
                    sets=frozenset(frozenset(c) for c in actual)
                    assert sets==maximal_allowed(ends[theta],allowed)
                    result['mec_comparisons']+=1
                    for end in ends[theta]:
                        if end<=allowed:
                            assert any(end<=c for c in sets)
                            result['end_component_coverage_checks']+=1
                for theta,uncertain in ((1,False),(0,True),(1,True)):
                    actual=uncertain_components(model,theta,allowed) if uncertain else known_components(model,allowed)
                    assert isinstance(actual,tuple) and actual==tuple(sorted(set(actual)))
                    expected=[c for c in good[theta,uncertain] if c<=allowed]
                    assert target_union(actual)==target_union(expected)
                    result['target_union_comparisons']+=1
                    for c in actual:
                        assert c==tuple(sorted(set(c))) and frozenset(c)<=allowed and qualifying(inp,theta,frozenset(c),uncertain)
                        result['representative_soundness_checks']+=1
            body=solve(model)
            if inp.initial in expected_regions[1]:
                assert isinstance(body,Positive) and check_positive(model,body) is not None
                assert (frozenset(body.K),frozenset(body.W))==expected_regions
                result['positive']+=1
            else:
                assert isinstance(body,Negative)
                assert check_negative(model,body) is not None and original_negative(model,body) is not None
                assert (frozenset(body.k_trace[-1]),frozenset(body.w_trace[-1]))==expected_regions
                result['negative']+=1
            result['models']+=1;result['signed_body_checks']+=1
        except BaseException:
            print(json.dumps(dict(campaign=name,index=index,raw=raw_model(inp)),default=str),flush=True)
            raise
        if result['models']%2000==0:
            print(json.dumps(dict(progress=name,models=result['models'],elapsed=round(time.monotonic()-start,3))),flush=True)
    assert result['models']==expected_count
    result['elapsed_seconds']=round(time.monotonic()-start,6)
    print(json.dumps(result,sort_keys=True),flush=True)
    return result

CAMPAIGNS={
    'one_action':('two_state_one_action',prior.two_state_one_action,13122),
    'one_state':('one_state_up_to_three_actions',prior.one_state_up_to_three_actions,500),
    'numerical':('two_state_two_action_state_homogeneous',prior.two_state_two_action_state_homogeneous,6561)}
if __name__=='__main__':
    selected=sys.argv[1:] or list(CAMPAIGNS)
    result=dict(python=sys.version,platform=platform.platform(),
                scope='Exact bounded evidence; complexity follows from structural source/proof review, not timings.',
                campaigns=[census(*CAMPAIGNS[key]) for key in selected])
    (HERE/('CAMPAIGN_'+'_'.join(selected)+'_v1.json')).write_text(json.dumps(result,indent=2)+'\n')
