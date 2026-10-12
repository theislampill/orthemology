"""Independent finite controls for exact-support guarded tree saturation.
No proof-DAG optimization or external source mutation.
"""
from itertools import product
from random import Random
import json

# rule = (head, ordered premises, local support bitset, cost, guard truth set)
def all_pairs_step(old, rules):
    new = [set(x) for x in old]
    for head, premises, local, weight, allowed in rules:
        for children in product(*(old[q] for q in premises)):
            supports = tuple(s for s, _ in children)
            if supports not in allowed:
                continue
            support, cost = local, weight
            for s, c in children:
                support |= s
                cost += c
            new[head].add((support, cost))
    return new

def exact_step(old, rules):
    new = [dict(x) for x in old]
    for head, premises, local, weight, allowed in rules:
        for supports in product(*(old[q] for q in premises)):
            if supports not in allowed:
                continue
            support = local
            for s in supports:
                support |= s
            cost = weight + sum(old[q][s] for q, s in zip(premises, supports))
            if support not in new[head] or cost < new[head][support]:
                new[head][support] = cost
    return new

def minima(pairs):
    out=[]
    for xs in pairs:
        d={}
        for s,c in xs:
            d[s]=min(c,d.get(s,c))
        out.append(d)
    return out

def frontier(xs):
    return {(s,c) for s,c in xs if not any((u,d)!=(s,c) and (u | s)==s and d<=c for u,d in xs)}

rng=Random(701903)
comparisons=0
for case in range(100):
    rules=[]
    for _ in range(8):
        arity=rng.randrange(3)
        premises=tuple(rng.randrange(2) for _ in range(arity))
        tuples=list(product(range(2),repeat=arity))
        allowed={x for x in tuples if rng.randrange(2)}
        rules.append((rng.randrange(2),premises,rng.randrange(2),rng.randrange(3),allowed))
    exact=[{},{}]
    oracle=[set(),set()]
    at_bound=None
    for height in range(1,6):
        exact=exact_step(exact,rules)
        oracle=all_pairs_step(oracle,rules)
        assert exact==minima(oracle),(case,height,exact,minima(oracle))
        comparisons+=1
        if height==4:
            at_bound=exact
        if height==5:
            assert exact==at_bound,(case,'failed H=4 fixed point')

# Two judgements and two tokens; terminal requires exact {a}. Larger {a,b}
# is rejected, and smaller empty support cannot substitute for {a}.
rules=[(0,(),0,0,{()}),(0,(),3,0,{()}),
       (0,(0,),1,0,{(0,),(1,),(2,),(3,)}),
       (1,(0,),0,0,{(1,)})]
exact=[{},{}]
pareto=[set(),set()]
rounds=[]
for h in range(1,7):
    exact=exact_step(exact,rules)
    pareto=[frontier(x) for x in all_pairs_step(pareto,rules)]
    rounds.append({'height':h,'exact':[dict(x) for x in exact],'pareto':[sorted(x) for x in pareto]})
assert rounds[1]['exact'][1]=={}
assert rounds[2]['exact'][1]=={1:0}
assert pareto[1]==set()

# Sharp height 2*(2+1)=6: q0 -> q1, with two support-gated return edges.
sharp=[(0,(1,),0,0,{(0,),(1,),(2,),(3,)}),
       (1,(),0,0,{()}), (1,(0,),1,0,{(0,)}),(1,(0,),2,0,{(1,)})]
exact=[{},{}]
first=None
for h in range(1,8):
    exact=exact_step(exact,sharp)
    if 3 in exact[0] and first is None:
        first=h
assert first==6
print(json.dumps({'status':'pass','seed':701903,'random_grammars':100,
                  'oracle_round_comparisons':comparisons,
                  'oracle':'all attained support-cost pairs, without dominance or same-support minimization',
                  'random_scope':'2 judgements, 1 evidence token, 8 rules, arity 0..2, weights 0..2, arbitrary Boolean support guards',
                  'sharp_bound_first_round':first,
                  'frontier_counterexample_terminal_first_round':3,
                  'frontier_counterexample_rounds':rounds},indent=2))
