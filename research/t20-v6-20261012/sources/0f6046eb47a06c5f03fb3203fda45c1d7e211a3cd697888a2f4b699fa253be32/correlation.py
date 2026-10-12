"""Exact finite fixed-marginal coordination and incentive checks.

Marginals, target relations, utilities and action authority are declared inputs.
This module proves no substantive correctness or authority of those inputs.
"""
from collections import defaultdict, deque
from fractions import Fraction as F
from itertools import product


def maximize_relation_mass(mu, nu, relation):
    """Maximize target-relation mass over all couplings; exact rational max flow.

    Every pair outside relation is allowed as a violation. Additional hard action
    exclusions require a constrained transportation problem, not this formula.
    """
    for marginal in (mu,nu):
        if not marginal or any(p<=0 for p in marginal.values()) or sum(marginal.values())!=1:
            raise ValueError('Marginals must be positive and exactly normalized')
    source,sink=('source',),('sink',)
    capacity=defaultdict(dict)
    def add(u,v,amount):
        capacity[u][v]=F(amount);capacity[v].setdefault(u,F(0))
    for x,p in mu.items():add(source,('row',x),p)
    for y,p in nu.items():add(('col',y),sink,p)
    for x,y in relation:
        if x in mu and y in nu:add(('row',x),('col',y),2)
    residual={u:dict(vs) for u,vs in capacity.items()}
    total=F(0)
    while True:
        pred={source:None};todo=deque([source])
        while todo and sink not in pred:
            u=todo.popleft()
            for v,amount in residual[u].items():
                if amount>0 and v not in pred:pred[v]=u;todo.append(v)
        if sink not in pred:break
        path=[];v=sink
        while v!=source:u=pred[v];path.append((u,v));v=u
        amount=min(residual[u][v] for u,v in path);total+=amount
        for u,v in path:residual[u][v]-=amount;residual[v][u]+=amount
    joint={}
    for x,y in relation:
        u,v=('row',x),('col',y)
        if v in capacity.get(u,{}):
            flow=capacity[u][v]-residual[u][v]
            if flow:joint[x,y]=flow
    left={x:F(p)-sum(v for (a,b),v in joint.items() if a==x) for x,p in mu.items()}
    right={y:F(p)-sum(v for (a,b),v in joint.items() if b==y) for y,p in nu.items()}
    deficit=1-total
    if deficit:
        # Maximality ensures any positive leftover row/column pair is outside R.
        for x,y in product(mu,nu):
            amount=left[x]*right[y]/deficit
            if amount:
                assert (x,y) not in relation
                joint[x,y]=joint.get((x,y),F(0))+amount
    assert all(sum(v for (a,b),v in joint.items() if a==x)==p for x,p in mu.items())
    assert all(sum(v for (a,b),v in joint.items() if b==y)==p for y,p in nu.items())
    assert sum(v for pair,v in joint.items() if pair not in relation)==deficit
    return {'minimum_violation':deficit,'coupling':joint,'maximum_relation_mass':total}


def fixed_marginal_law_2x2(p,q,target,allowed=None,ce_games=()):
    """Exact interval solver for prescribed binary marginals and optional CE.

    ce_games may contain several payoff-table pairs; all their incentive
    inequalities are required, a robust common recommendation contract.
    """
    p,q=F(p),F(q)
    if not 0<=p<=1 or not 0<=q<=1:raise ValueError('Marginals must lie in [0,1]')
    pairs=set(product(range(2),repeat=2))
    allowed=pairs if allowed is None else set(allowed)
    target=set(target)
    if not allowed<=pairs or not target<=pairs:raise ValueError('Undeclared joint action')
    # kappa_00=t, kappa_01=p-t, kappa_10=q-t, kappa_11=1-p-q+t.
    cells={(0,0):(F(1),F(0)),(0,1):(F(-1),p),
           (1,0):(F(-1),q),(1,1):(F(1),1-p-q)}
    lower,upper=max(F(0),p+q-1),min(p,q)
    constraints=[]
    for pair in pairs-allowed:
        a,b=cells[pair];constraints.extend([(f'forbid {pair} upper',-a,-b),
                                           (f'forbid {pair} lower',a,b)])
    for h,(u,v) in enumerate(ce_games):
        for rec in range(2):
            row_terms={(rec,j):F(u[rec][j])-F(u[1-rec][j]) for j in range(2)}
            col_terms={(i,rec):F(v[i][rec])-F(v[i][1-rec]) for i in range(2)}
            for label,terms in ((f'game {h} row recommendation {rec}',row_terms),
                                (f'game {h} column recommendation {rec}',col_terms)):
                a=sum(weight*cells[pair][0] for pair,weight in terms.items())
                b=sum(weight*cells[pair][1] for pair,weight in terms.items())
                constraints.append((label,a,b))
    lower_owner='nonnegative joint mass';upper_owner='marginal mass'
    for label,a,b in constraints:
        if a==0:
            if b<0:return {'feasible':False,'conflict':[label],'minimum_violation':None}
        elif a>0:
            value=-b/a
            if value>lower:lower=value;lower_owner=label
        else:
            value=-b/a
            if value<upper:upper=value;upper_owner=label
    if lower>upper:
        return {'feasible':False,'conflict':[lower_owner,upper_owner],
                'inconsistent_bounds':(lower,upper),'minimum_violation':None}
    slope=sum(cells[pair][0] for pair in pairs-target)
    offset=sum(cells[pair][1] for pair in pairs-target)
    t=lower if slope>=0 else upper
    law={pair:a*t+b for pair,(a,b) in cells.items() if a*t+b>0}
    assert all(a*t+b>=0 for _,a,b in constraints)
    assert all(pair in allowed for pair in law)
    return {'feasible':True,'interval':(lower,upper),'coupling':law,
            'minimum_violation':slope*t+offset,'constraints':constraints}
