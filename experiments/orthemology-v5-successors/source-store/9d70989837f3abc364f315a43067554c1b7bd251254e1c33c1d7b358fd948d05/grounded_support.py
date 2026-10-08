"""Finite positive Horn support analysis. No empirical or external truth claims."""
from itertools import combinations, product

def minimize(family):
    family=frozenset(frozenset(s) for s in family)
    return frozenset(s for s in family if not any(t < s for t in family))

def minimal_supports(base,rules):
    """Least finite grounded closure, annotating claims with minimal root sets."""
    result={}
    for root,claim in base:
        result[claim]=minimize(tuple(result.get(claim,()))+(frozenset({root}),))
    rules=[(tuple(body),head) for body,head in rules]
    while True:
        changed=False
        for body,head in rules:
            families=[result.get(claim,frozenset()) for claim in body]
            if any(not f for f in families):continue
            candidates=[frozenset().union(*choices) for choices in product(*families)]
            old=result.get(head,frozenset());new=minimize(tuple(old)+tuple(candidates))
            if new!=old:result[head]=new;changed=True
        if not changed:return result

def available_claims(supports,available):
    available=frozenset(available)
    return {claim for claim,family in supports.items() if any(s<=available for s in family)}

def powerset(universe):
    xs=tuple(universe)
    return [frozenset(c) for k in range(len(xs)+1) for c in combinations(xs,k)]

def cuts(supports,universe):
    return frozenset(c for c in powerset(universe) if all(c&s for s in supports))

def minimum_cuts(supports,universe):
    family=cuts(supports,universe)
    if not family:return frozenset()
    size=min(map(len,family))
    return frozenset(c for c in family if len(c)==size)

def quotient_supports(supports,mapping):
    return minimize(frozenset(mapping[x] for x in s) for s in supports)
