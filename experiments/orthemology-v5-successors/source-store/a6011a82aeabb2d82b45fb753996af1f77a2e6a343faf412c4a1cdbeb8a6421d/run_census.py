"""Replay the independent, explicitly bounded complete finite census."""
import json
import platform
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
REFERENCE=HERE.parents[1]/'research'/'hidden-change'/'reference-v1'
sys.path.insert(0,str(REFERENCE))
from oracle import (raw_model, regions, subsets, good_component,
                    eligible_known, eligible_uncertain,
                    one_action_chain_regions, two_state_one_action,
                    one_state_up_to_three_actions)
from model import validate_model
from finite import component
from certificates import Positive, Negative, check_positive, check_negative
from synthesis import solve, known_operator, uncertain_operator


def census(name, generator, expected_count):
    start=time.monotonic()
    result=dict(name=name,models=0,positive=0,negative=0,
                known_operator_comparisons=0,uncertain_operator_comparisons=0,
                component_comparisons=0,signed_body_checks=0)
    for index,inp in enumerate(generator()):
        try:
            expected=regions(inp)
            if inp.a==1:
                assert expected==one_action_chain_regions(inp)
            model=validate_model(raw_model(inp))
            for k in subsets(range(inp.n)):
                assert known_operator(model,k)==eligible_known(inp,k)
                result['known_operator_comparisons']+=1
                for w in subsets(range(inp.n)):
                    assert uncertain_operator(model,k,w)==eligible_uncertain(inp,k,w)
                    result['uncertain_operator_comparisons']+=1
            for pairs in subsets((s,a) for s in range(inp.n) for a in inp.menus[s]):
                canonical=tuple(sorted(pairs))
                for theta,uncertain in ((1,False),(0,True),(1,True)):
                    assert component(model,theta,canonical,uncertain=uncertain)==good_component(inp,theta,pairs,uncertain)
                    result['component_comparisons']+=1
            body=solve(model)
            if inp.initial in expected[1]:
                assert isinstance(body,Positive)
                assert check_positive(model,body) is not None
                assert (frozenset(body.K),frozenset(body.W))==expected
                result['positive']+=1
            else:
                assert isinstance(body,Negative)
                assert check_negative(model,body) is not None
                assert (frozenset(body.k_trace[-1]),frozenset(body.w_trace[-1]))==expected
                result['negative']+=1
            result['models']+=1
            result['signed_body_checks']+=1
        except BaseException:
            print(json.dumps(dict(campaign=name,index=index,raw=raw_model(inp)),default=str),flush=True)
            raise
    assert result['models']==expected_count
    result['elapsed_seconds']=round(time.monotonic()-start,6)
    print(json.dumps(result,sort_keys=True),flush=True)
    return result


if __name__=='__main__':
    data=dict(python=sys.version,platform=platform.platform(),
              scope='Exact bounded census; no probabilistic theorem inferred.',
              campaigns=[census('two_state_one_action',two_state_one_action,13122),
                         census('one_state_up_to_three_actions',one_state_up_to_three_actions,500)])
    (HERE/'CENSUS_RESULT_v1.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
