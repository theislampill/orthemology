"""Deterministic structural extension beyond the previous finite classes."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import random
import time
from component_checks import verify_components
from oracle import fixture,subsets
HERE=Path(__file__).resolve().parent

def support_row(n,mask):
    selected={s for s in range(n) if mask>>s&1}
    return tuple(Q(int(s in selected),len(selected)) for s in range(n))

def three_state_supports():
    for masks in product(range(1,8),repeat=3):
        yield fixture(3,p=lambda t,s,a:support_row(3,masks[s]),d=lambda t,s,a:((0,1,2),(2,3,0))[t][s])

def sparse_seeded():
    rng=random.Random(18062026)
    for _ in range(160):
        rows=[[[None]*2 for _ in range(3)] for _ in range(2)]
        for s in range(3):
            for a in range(2):
                rows[0][s][a]=support_row(3,rng.randrange(1,8))
                if rng.randrange(3)==0:
                    rows[1][s][a]=rows[0][s][a]
                else:
                    weights=[rng.randrange(4) for _ in range(3)]
                    if not sum(weights): weights[rng.randrange(3)]=1
                    rows[1][s][a]=tuple(Q(w,sum(weights)) for w in weights)
        labels=[[[rng.randrange(6) for _ in range(2)] for _ in range(3)] for _ in range(2)]
        yield fixture(3,2,p=lambda t,s,a:rows[t][s][a],d=lambda t,s,a:labels[t][s][a])

if __name__=='__main__':
    results=[]
    for name,generator,count in [('three_state_all_equal_mode_support_graphs',three_state_supports,343),
                                 ('three_state_two_action_seeded_sparse',sparse_seeded,160)]:
        start=time.monotonic();total=0;allowed=0
        for inp in generator():
            verify_components(inp);total+=1;allowed+=2**(inp.n*inp.a)
        assert total==count
        result=dict(name=name,models=total,allowed_pair_sets=allowed,mec_comparisons=2*allowed,
                    target_union_comparisons=3*allowed,elapsed_seconds=round(time.monotonic()-start,6))
        print(json.dumps(result),flush=True);results.append(result)
    (HERE/'EXTRA_CAMPAIGN_v1.json').write_text(json.dumps(results,indent=2)+'\n')
