"""Participating finite-law diagnostic; standard probability, not a new theorem."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

def law(samples, f):
    d={}
    for x,p in samples:
        k=f(x);d[k]=d.get(k,F(0))+p
    return d

iid=[(u,F(1,4)) for u in product(range(2),repeat=2)]
shared=[((u,u),F(1,2)) for u in range(2)]
checks=[]
def check(name, p):
    if not p: raise RuntimeError(name)
    checks.append(name)
for t in range(2):
    check('uniform_marginal_'+str(t),law(iid,lambda u:u[t])==law(shared,lambda u:u[t])=={0:F(1,2),1:F(1,2)})
check('history_laws_differ',law(iid,lambda u:u)!=law(shared,lambda u:u))
check('repeat_event_half_vs_one',law(iid,lambda u:u[0]==u[1])[True]==F(1,2) and law(shared,lambda u:u[0]==u[1])[True]==1)
for first in range(2):
    for source,name,expected in [(iid,'iid',{0:F(1,2),1:F(1,2)}),(shared,'shared',{first:F(1)})]:
        denom=sum(p for u,p in source if u[0]==first)
        conditional=[(u,p/denom) for u,p in source if u[0]==first]
        check(name+'_conditional_'+str(first),law(conditional,lambda u:u[1])==expected)
print(json.dumps({'status':'PASS','checks':checks,'count':len(checks),'scope':'One-state emitted-history counterexample. Marginal seed uniformity does not entail conditional-history freshness. No source-compiler or philosophical-warrant claim.'},indent=2))
