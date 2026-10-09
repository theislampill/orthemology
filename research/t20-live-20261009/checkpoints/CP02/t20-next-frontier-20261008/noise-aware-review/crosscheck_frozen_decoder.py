from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
import random
import sys

sys.dont_write_bytecode=True
root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('robust_author_frozen',root/'frozen/robust_masks.py')
author=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=author
spec.loader.exec_module(author)


def endpoint_law(model,profile,mask,roots,bound,eta=F(0)):
    p=F(1,2*bound)
    rates=[p+eta if mask>>i&1 else eta for i in range(roots)]
    law={0:F(1)}
    for (support,guard,outputs),count in model.items():
        if support&profile!=support or guard&profile:
            continue
        chance=F(1)
        for i in range(roots):
            if support>>i&1:
                chance*=rates[i]
        for _ in range(count):
            nxt=defaultdict(F)
            for outcome,weight in law.items():
                nxt[outcome]+=weight*(1-chance)
                nxt[outcome|outputs]+=weight*chance
            law=dict(nxt)
    assert sum(law.values())==1
    assert all(weight>=0 for weight in law.values())
    return law


def independent_panel(model,roots,effects,bound,eta=F(0)):
    out={}
    for profile in range(1,1<<roots):
        for mask in range(1,1<<roots):
            if mask&profile!=mask:
                continue
            law=endpoint_law(model,profile,mask,roots,bound,eta)
            for query in range(1,1<<effects):
                out[profile,mask,query]=sum((mass for endpoint,mass in law.items() if not endpoint&query),F(0))
    return out


rng=random.Random(190081008)
cases=coordinates=0
max_terms=0
for roots,effects,bound in ((1,2,2),(2,3,4),(3,2,6),(4,1,8)):
    p=F(1,2*bound)
    epsilon=p**roots/(16*(1<<roots))
    eta=epsilon/(2*roots*bound)
    possibilities=[(s,g,t) for s in range(1,1<<roots) for g in range(1<<roots) if not s&g for t in range(1,1<<effects)]
    for _ in range(10):
        counts=defaultdict(int)
        for _ in range(bound):
            counts[rng.choice(possibilities)]+=1
        counts=dict(counts)
        ideal=independent_panel(counts,roots,effects,bound)
        actual=independent_panel(counts,roots,effects,bound,eta)
        assert ideal==author.exact_panel(counts,roots,effects,bound)
        assert all(q>=F(1,2) for q in ideal.values())
        assert all(abs(actual[key]-ideal[key])<=bound*roots*eta for key in ideal)
        observed={key:min(F(1),max(F(0),q+epsilon/2*rng.choice((-1,1)))) for key,q in actual.items()}
        assert all(abs(observed[key]-ideal[key])<=epsilon for key in ideal)
        recovered,certificates=author.certify_guarded_effect_histogram(observed,roots,effects,bound)
        assert recovered==counts
        max_terms=max(max_terms,max(c['series_terms'] for c in certificates.values()))
        cases+=1
        coordinates+=len(observed)
receipt={'independent_convolution_guarded_effect_models':cases,'perturbed_probability_coordinates':coordinates,'root_effect_bound_cases':[[1,2,2],[2,3,4],[3,2,6],[4,1,8]],'largest_author_series_budget':max_terms,'noise':'Independent convolution at uniformly upward-biased gate rates, including leakage, followed by bounded rational endpoint-probability perturbations.'}
(root/'results/CROSSCHECK_METRICS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
