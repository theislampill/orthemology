#!/usr/bin/env python3
"""Separately implemented finite checks; not an independent researcher review."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from contracts import Contract,coarsest_refinement,sidecar,finite_values,conditioned,total_variation


def partitions(xs):
    if not xs:
        yield []
    else:
        for p in partitions(xs[1:]):
            yield [(xs[0],)]+p
            for i in range(len(p)):
                yield p[:i]+[(xs[0],)+p[i]]+p[i+1:]


def oracle_stable(p,successors,labels,costs):
    loc={s:i for i,b in enumerate(p) for s in b}
    for b in p:
        first=b[0]
        for s in b[1:]:
            if labels[s]!=labels[first] or costs[s]!=costs[first] or loc[successors[s]]!=loc[successors[first]]:
                return False
    return True


def require(ok,msg):
    if not ok: raise RuntimeError(msg)


def run():
    counts={'three_state_contracts':0,'candidate_partitions':0,'value_bound_instances':0,'conditioning_bound_instances':0}
    states=('0','1','2'); allp=list(partitions(list(states)))
    for target in product(states,repeat=3):
        for ls in product((0,1),repeat=3):
            for cs in product((0,1),repeat=3):
                labels=dict(zip(states,ls));costs=dict(zip(states,cs));succ=dict(zip(states,target))
                c=Contract(states,('a',),('o',),labels,{s:('a',) for s in states},
                           {(s,'a'):F(costs[s]) for s in states},
                           {(s,'a'):(('o',succ[s],F(1)),) for s in states})
                out,_=coarsest_refinement(c,{s:0 for s in states})
                stable=[]
                for p in allp:
                    counts['candidate_partitions']+=1
                    if oracle_stable(p,succ,labels,costs): stable.append(p)
                minimum=min(len(p) for p in stable)
                require(len(out)==minimum,'Refinement did not match exhaustive oracle')
                outloc={s:i for i,b in enumerate(out) for s in b}
                for p in stable:
                    require(all(len({outloc[s] for s in b})==1 for b in p),'Stable partition did not refine output')
                k,m,bits=sidecar(c,{s:0 for s in states},out)
                require(m==minimum and bits==(m-1).bit_length(),'Sidecar mismatch')
                counts['three_state_contracts']+=1

    for p1,p2 in product((F(0),F(1,2),F(1)),repeat=2):
        for c1,c2 in product((F(0),F(1)),repeat=2):
            q=(p1+p2)/2; cost=(c1+c2)/2; eps=abs(p1-p2)/2; delta=abs(c1-c2)/2
            c=Contract(('x','y','done'),('a',),('wait','finish'),
                {'x':'working','y':'working','done':'done'}, {s:('a',) for s in ('x','y','done')},
                {('x','a'):c1,('y','a'):c2,('done','a'):F(0)},
                {('x','a'):(('wait','x',1-p1),('finish','done',p1)),
                 ('y','a'):(('wait','y',1-p2),('finish','done',p2)),
                 ('done','a'):(('finish','done',F(1)),)})
            d=Contract(('coarse','done'),('a',),('wait','finish'),
                {'coarse':'working','done':'done'}, {'coarse':('a',),'done':('a',)},
                {('coarse','a'):cost,('done','a'):F(0)},
                {('coarse','a'):(('wait','coarse',1-q),('finish','done',q)),
                 ('done','a'):(('finish','done',F(1)),)})
            for h in range(7):
                a=finite_values(c,h,{'x':F(1),'y':F(1),'done':F(0)})
                b=finite_values(d,h,{'coarse':F(1),'done':F(0)})
                bound=h*delta+eps*(h+F(h*(h-1),2))
                require(abs(a['x']-b['coarse'])<=bound and abs(a['y']-b['coarse'])<=bound,'Finite-horizon bound failed')
                counts['value_bound_instances']+=1

    laws=[(F(a,4),F(b,4),F(4-a-b,4)) for a in range(5) for b in range(5-a)]
    for p,q in product(laws,repeat=2):
        for l in product((F(0),F(1,2),F(1)),repeat=3):
            zp=sum((a*b for a,b in zip(p,l)),F(0));zq=sum((a*b for a,b in zip(q,l)),F(0))
            if not zp or not zq:continue
            pp=conditioned(p,l);qq=conditioned(q,l)
            require(total_variation(pp,qq)<=min(F(1),2*total_variation(p,q)/min(zp,zq)),'Conditioning bound failed')
            counts['conditioning_bound_instances']+=1
    return {'status':'PASS','counts':counts,'scope':'Exact finite corroboration, not general proof or external review'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
