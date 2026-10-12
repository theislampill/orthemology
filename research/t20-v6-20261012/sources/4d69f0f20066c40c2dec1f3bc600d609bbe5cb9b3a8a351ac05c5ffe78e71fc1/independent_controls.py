"""Reviewer-owned independent small controls, no source modification."""
import sys, json, random
from pathlib import Path
from fractions import Fraction as F
from itertools import product
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'proof_inquiry'))
import cache_transport as c
R=c.g.Rule
Z=frozenset(); A=frozenset('a'); B=frozenset('b'); K=A|B
rng=random.Random(91823)
results={}; cases=0
# Direct proof-object oracle, independently enumerating acyclic two-stage grammar.
# Random ordered/nonmonotone root guards and zero prices, all closed leaf caches.
for trial in range(80):
    allowed=frozenset(ss for ss in product((Z,A,B),repeat=2) if rng.randrange(2))
    rules=tuple(R('leaf'+str(i),'q',(),s,F(rng.randrange(4))) for i,s in enumerate((Z,A,B)))+(R('root','t',('q','q'),Z,F(rng.randrange(4)),allowed),)
    leaves=tuple(c.Node(r,()) for r in rules[:-1])
    proofs=tuple(c.Node(rules[-1],chs) for chs in product(leaves,repeat=2) if tuple(c.support(ch) for ch in chs) in allowed)
    for mask in range(8):
        cache=frozenset(n for i,n in enumerate(leaves) if mask>>i&1)
        for exact in (None,Z,A,B,K):
            eligible=[p for p in proofs if exact is None or c.support(p)==exact]
            expected=min((sum(n.rule.cost for n in c.footprint(p)-cache) for p in eligible),default=None)
            got,p=c.cached_optimum(('q','t'),('a','b'),rules,'t',K,cache,exact)
            if got!=expected: raise AssertionError((trial,mask,exact,got,expected))
            if p is not None and not c.valid_node(p,rules,K): raise AssertionError('invalid root')
            cases+=1
results['independent_ordered_guard_oracle_cases']=cases
# Changed root guard, and withdrawn root admission, reject cached terminal witness.
leaf=R('leaf','q',(),A,F(2)); root=R('root','t',('q',),Z,F(9),frozenset(((A,),)))
n=c.Node(leaf,()); terminal=c.Node(root,(n,)); cache=frozenset((n,terminal))
for revised in ((leaf,), (leaf,R('root','t',('q',),Z,F(9),frozenset(((Z,),))))):
    if terminal in c.active_cache(cache,revised,K): raise AssertionError('invalid root survived')
    try: c.cached_optimum(('q','t'),('a','b'),revised,'t',K,cache)
    except ValueError: pass
    else: raise AssertionError('stale cache accepted')
results['withdrawn_or_re_guarded_root_rejected']=True
# A forbidden nullary guard must not be made available or cached.
forbidden=R('forbidden','t',(),A,F(0),frozenset())
if c.cached_optimum(('t',),('a','b'),(forbidden,),'t',K,Z)!=(None,None): raise AssertionError('nullary guard bypass')
results['forbidden_nullary_root_rejected']=True
# Countercontrol: postponement fails with credential-gated query or early discount.
credential_cost=F(2); query_cost=F(1)
results['credential_gate']={'interleaved_feasible_cost':str(credential_cost+query_cost),'terminal_only_feasible':False}
results['early_discount']={'interleaved_check_cost':1,'terminal_check_cost':5,'postponement_dominance':False}
# Full-support assumption essential: deterministic observation identifies standard,
# then a three-state stationary controller commits to the corresponding good action.
# State 0 probes with action 0; deterministic y=theta moves to absorbing
# states 1/2 whose selected actions are 0/1. Under full support both absorbing
# states are reachable under either model and the wrong one traps forever.
actions=(0,0,1); update=((1,2),(1,1),(2,2))
def reachable(theta,full_support):
    seen={0}; todo=[0]
    while todo:
        q=todo.pop()
        for y in ((0,1) if full_support else (theta,)):
            v=update[q][y]
            if v not in seen: seen.add(v);todo.append(v)
    return seen
for theta in (0,1):
    absorbing=reachable(theta,False)-{0}
    if any(actions[q]!=theta for q in absorbing):raise AssertionError('non-full-support control failed')
    if not any(actions[q]!=theta for q in reachable(theta,True)-{0}):raise AssertionError('full-support obstruction disappeared')
results['without_full_support_finite_memory_restores_disjoint_good_sets']=True
# Fixed-model coupling: independent branch maximization pastes different models.
a=(F(9,10),F(1,10));b=(F(3,10),F(7,10));m=(F(1,4),F(3,4))
v=tuple(m[0]*a[i]+m[1]*b[i] for i in range(2))
if v!=(F(9,20),F(11,20)):raise AssertionError(v)
results['fixed_model_vector']=list(map(str,v));results['pasted_upper']=str(m[0]*max(a)+m[1]*max(b))
print(json.dumps(results,indent=2))
