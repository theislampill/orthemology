"""Independent bounded pair-powerset oracle, written before efficient source read.

No imports from efficient or reference production are permitted. Reachability
uses Boolean transitive closure. MECs are maximal exact end-component pair
subsets, not inferred from any graph decomposition algorithm.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations

@dataclass(frozen=True)
class Input:
    n: int
    a: int
    initial: int
    menus: tuple
    rows: tuple
    priorities: tuple

def subsets(items):
    items=tuple(sorted(items))
    for size in range(len(items)+1):
        for chosen in combinations(items,size):
            yield frozenset(chosen)

def full_pairs(m):
    return frozenset((s,a) for s in range(m.n) for a in m.menus[s])

def reachability(m,theta,pairs):
    reach=[[s==t for t in range(m.n)] for s in range(m.n)]
    for s,a in pairs:
        for t,p in enumerate(m.rows[theta][s][a]):
            if p>0: reach[s][t]=True
    for via in range(m.n):
        for s in range(m.n):
            for t in range(m.n):
                reach[s][t]=reach[s][t] or (reach[s][via] and reach[via][t])
    return reach

def end_component(m,theta,pairs):
    if not pairs or not pairs<=full_pairs(m): return False
    sources={s for s,a in pairs}
    for s,a in pairs:
        if any(p>0 and t not in sources for t,p in enumerate(m.rows[theta][s][a])):
            return False
    reach=reachability(m,theta,pairs)
    return all(reach[s][t] for s in sources for t in sources)

def qualifying(m,theta,pairs,uncertain):
    if not end_component(m,theta,pairs): return False
    if not uncertain:
        return theta==1 and min(m.priorities[1][s][a] for s,a in pairs)%2==0
    if any(p>0 and m.rows[0][s][a][t]==0
           for s,a in pairs for t,p in enumerate(m.rows[theta][s][a])):
        return False
    # Literal implication for BOTH modes; no reliance on the refinement split.
    for rival in (0,1):
        if all(m.rows[rival][s][a]==m.rows[theta][s][a] for s,a in pairs):
            if min(m.priorities[rival][s][a] for s,a in pairs)%2: return False
    return True

def all_end_components(m,theta):
    return tuple(p for p in subsets(full_pairs(m)) if end_component(m,theta,p))

def maximal_allowed(all_components,allowed):
    candidates=[p for p in all_components if p<=allowed]
    return frozenset(p for p in candidates if not any(p<q for q in candidates))

def target_union(components):
    return frozenset(s for c in components for s,a in c)

def fixture(n=1,a=1,p=None,d=None,menus=None,initial=0):
    p=p or (lambda t,s,a:tuple(Q(y==s) for y in range(n)))
    d=d or (lambda t,s,a:0)
    return Input(n,a,initial,menus or tuple(tuple(range(a)) for _ in range(n)),
                 tuple(tuple(tuple(tuple(p(t,s,a)) for a in range(a)) for s in range(n)) for t in (0,1)),
                 tuple(tuple(tuple(d(t,s,a) for a in range(a)) for s in range(n)) for t in (0,1)))

def raw_model(m):
    return dict(n_states=m.n,n_actions=m.a,initial=m.initial,menus=m.menus,
                rows=tuple(tuple(tuple(tuple(str(p) for p in row) for row in state) for state in mode) for mode in m.rows),
                priorities=m.priorities)
