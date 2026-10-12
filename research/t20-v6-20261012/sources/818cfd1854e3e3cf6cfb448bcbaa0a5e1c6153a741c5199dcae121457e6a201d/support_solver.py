"""Exact finite candidate for support-changing hidden-target Markov restoration.
The ordinary stochastic theorem and historical disposition are separate.
Only nonempty live supports are returned. Bit i denotes hidden model i.
"""
from fractions import Fraction
from types import SimpleNamespace
from common_graph import verifying_components,backward_reach

def solve_supports(probabilities,good,menus):
    # Model identity is numerical, independent of Python container representation.
    probabilities=tuple(tuple(tuple(tuple(row) for row in actions) for actions in states) for states in probabilities)
    good=tuple(frozenset(g) for g in good)
    m=len(probabilities)
    if not m:raise ValueError('Nonempty model family required')
    n=len(probabilities[0])
    if not n:raise ValueError('Nonempty observed state set required')
    k=len(probabilities[0][0])
    if len(good)!=m:raise ValueError('Model/good-set dimension mismatch')
    pairs={(s,a) for s in range(n) for a in range(k)}
    if any(not set(g)<=pairs for g in good):raise ValueError('Invalid good pair')
    for rows in probabilities:
        if len(rows)!=n or any(len(ar)!=k for ar in rows):raise ValueError('Table dimensions differ')
        for ar in rows:
            for row in ar:
                if len(row)!=n or any(not isinstance(p,Fraction) or p<0 for p in row) or sum(row)!=1:
                    raise ValueError('Invalid exact rational probability row')
    order=sorted(range(1,1<<m),key=lambda B:(B.bit_count(),B))
    menu_table={(B,s):frozenset(menus(B,s)) for B in order for s in range(n)}
    if any(not acts<=set(range(k)) for acts in menu_table.values()):raise ValueError('Invalid menu action')
    winning={}
    for B in order:
        models=[t for t in range(m) if B>>t&1]
        updates={(s,a,y):sum(1<<t for t in models if probabilities[t][s][a][y]>0)
                 for s in range(n) for a in range(k) for y in range(n)}
        internal={(s,a):frozenset(y for y in range(n) if updates[s,a,y]==B)
                  for s in range(n) for a in range(k)}
        progress={(t,s,a):any(updates[s,a,y] not in (0,B) and probabilities[t][s][a][y]>0 for y in range(n))
                  for t in models for s in range(n) for a in range(k)}
        zero_good=[frozenset((s,a) for s,a in good[t] if not progress[t,s,a]) for t in models]
        W=frozenset(range(n))
        while True:
            allowed={s:frozenset(a for a in menu_table[B,s]
                       if all(C==0 or (y in W if C==B else y in winning[C])
                              for y in range(n) for C in (updates[s,a,y],))) for s in W}
            family=SimpleNamespace(m=len(models),n=n,a=k,probabilities=[probabilities[t] for t in models],
                                   good=zero_good,menus=allowed,support=internal)
            successor=set(W)
            for local,t in enumerate(models):
                components,_=verifying_components(family,W,local)
                target=set().union(*(C for C,U in components)) if components else set()
                target.update(s for s in W if any(progress[t,s,a] for a in allowed[s]))
                reachable,_=backward_reach(family,W,target)
                successor.intersection_update(reachable)
            if successor==W:break
            W=frozenset(successor)
        winning[B]=set(W)
    return winning
