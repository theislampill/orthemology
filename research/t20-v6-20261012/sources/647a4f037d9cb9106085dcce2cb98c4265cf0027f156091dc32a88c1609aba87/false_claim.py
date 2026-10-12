"""Deliberately false transport claims; each must fail for its stated reason."""
from fractions import Fraction as F
import sys
import cache_transport as c

def demand(claim,name):
    if not claim: raise AssertionError('INTENDED_FALSE_CLAIM_REJECTED: '+name)

name=sys.argv[1]
if name=='cache_normalization':
    R=c.g.Rule;e=frozenset(('e',));empty=frozenset()
    rules=(R('qa','q',(),e,F(1)),R('qb','q',(),e,F(2)),R('rq','r',('q',),empty,F(10)),R('tqr','t',('q','r'),empty,F(1)))
    dag=c.g.Dag(((rules[0],()),(rules[1],()),(rules[2],(1,)),(rules[3],(0,2))),3)
    qb=c.Node(rules[1],());cache=frozenset((qb,c.Node(rules[2],(qb,))))
    normalized=c.g.normalize(dag,('q','r','t'),('e',),rules)
    demand(c.incremental_cost(c.from_dag(normalized),cache)<=c.incremental_cost(c.from_dag(dag),cache),name)
elif name=='branch_pasting':
    weights=(F(1,4),F(3,4));branch=((F(9,10),F(1,10)),(F(3,10),F(7,10)))
    fixed=max(sum((weights[o]*branch[o][i] for o in range(2)),F()) for i in range(2))
    pasted=sum((weights[o]*max(branch[o]) for o in range(2)),F())
    demand(fixed==pasted,name)
elif name=='snapshot_survives_revision':
    R=c.g.Rule;e=frozenset(('e',));empty=frozenset()
    rules=(R('qa','q',(),e,F(1)),R('qb','q',(),e,F(2)),R('rq','r',('q',),empty,F(10)),R('tqr','t',('q','r'),empty,F(1)))
    qa,qb=(c.Node(r,()) for r in rules[:2])
    caches=(frozenset((qa,c.Node(rules[2],(qa,)))),frozenset((qb,c.Node(rules[2],(qb,)))))
    revised=tuple(r for r in rules if r.name!='qa')
    values=[c.cached_optimum(('q','r','t'),('e',),revised,'t',e,c.active_cache(C,revised,e))[0] for C in caches]
    demand(values[0]==values[1],name)
else:
    raise ValueError('Unknown deliberately false claim')
