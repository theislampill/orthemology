"""Bounded exact comparison of forged canonical negative traces."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import time
from run_campaign import prior
from oracle import fixture,raw_model,subsets
from model import validate_model
from certificates import check_negative as baseline
from negative import check_negative as fast
HERE=Path(__file__).resolve().parent

def oracle_trace(inp,operator):
    current=frozenset(range(inp.n));trace=[tuple(sorted(current))]
    while True:
        nxt=operator(current);trace.append(tuple(sorted(nxt)))
        if nxt==current:return tuple(trace)
        current=nxt

def inputs():
    yield fixture(2)
    yield fixture(2,d=lambda t,s,a:1)
    yield fixture(2,p=lambda t,s,a:tuple(Q(y==(1-s if t==0 else s)) for y in range(2)),d=lambda t,s,a:s)
    yield fixture(2,p=lambda t,s,a:(Q(1),Q(0)) if t==0 and s==0 else (Q(0),Q(1)),d=lambda t,s,a:1 if t==1 and s==0 else 0)

if __name__=='__main__':
    start=time.monotonic();total=accepted=0
    for inp in inputs():
        m=validate_model(raw_model(inp))
        kt=oracle_trace(inp,lambda k:prior.eligible_known(inp,k))
        wt=oracle_trace(inp,lambda w:prior.eligible_uncertain(inp,frozenset(kt[-1]),w))
        regions=tuple(tuple(sorted(s)) for s in subsets(range(inp.n)))
        for length in range(inp.n+4):
            for trace in product(regions,repeat=length):
                for field in ('k_trace','w_trace'):
                    body=dict(k_trace=kt,w_trace=wt);body[field]=trace
                    expected=baseline(m,body);actual=fast(m,body)
                    assert actual==expected,(raw_model(inp),body,actual,expected)
                    total+=1;accepted+=actual is not None
    result=dict(models=4,body_comparisons=total,accepted=accepted,
                description='Every canonical region trace of length zero through n+3, substituted separately for both traces.',
                elapsed_seconds=round(time.monotonic()-start,6))
    print(json.dumps(result),flush=True)
    (HERE/'NEGATIVE_CAMPAIGN_v1.json').write_text(json.dumps(result,indent=2)+'\n')
