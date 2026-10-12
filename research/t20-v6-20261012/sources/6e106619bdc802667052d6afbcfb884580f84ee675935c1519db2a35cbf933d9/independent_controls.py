#!/usr/bin/env python3
"""Independent exact-matrix review controls. Does not use author's graph oracle.

A policy is accepted iff I-Q for its reachable nonterminal product states is
nonsingular over the rationals. Q uses arbitrary positive rational edge weights,
not a graph's reachability-to-goal test. These finite tests do not prove general
policy completeness; the written review supplies the argument and attribution.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from pathlib import Path
import importlib.util, random, json, hashlib, sys
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'snapshot/stochastic-exact-inquiry-20261010'
spec=importlib.util.spec_from_file_location('candidate_solver',SOURCE/'solver.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
classify=module.classify
stats=defaultdict(int)

def members(mask,n): return tuple(i for i in range(n) if mask>>i&1)
def is_goal(mask,labels): return len({labels[i] for i in members(mask,len(labels))})==1

def matrix_solve(A,b):
    # Fraction Gauss-Jordan; rank deficiency is an exact nontermination witness.
    n=len(A); M=[list(A[i])+[b[i]] for i in range(n)]
    for k in range(n):
        j=next((j for j in range(k,n) if M[j][k]),None)
        if j is None:return None
        M[k],M[j]=M[j],M[k]
        c=M[k][k];M[k]=[x/c for x in M[k]]
        for j in range(n):
            if j!=k and M[j][k]:
                c=M[j][k];M[j]=[a-c*b for a,b in zip(M[j],M[k])]
    return [r[-1] for r in M]

def evaluate_strategy(rows,labels,initial,legal,strategy,skew=False):
    n=len(labels); start=sum(1<<x for x in initial)
    pending=[(x,start) for x in initial]; visited=set(pending); trans={}
    while pending:
        x,mask=pending.pop(); edges=defaultdict(F)
        if is_goal(mask,labels):trans[x,mask]={};continue
        aa=strategy[mask]
        if not aa:
            # No licensed move and no sound stop means permanent nontermination.
            trans[x,mask]={(x,mask):F(1)};continue
        for a in aa:
            rr=sorted(rows[a][x],key=repr)
            ws=list(range(1,len(rr)+1)) if skew else [1]*len(rr)
            for (y,o),weight in zip(rr,ws):
                target=0
                for z in members(mask,n):
                    for yp,op in rows[a][z]:
                        if op==o:target |= 1<<yp
                edges[y,target]+=F(weight,len(aa)*sum(ws))
        assert sum(edges.values())==1
        trans[x,mask]=dict(edges)
        for v in edges:
            if v not in visited:visited.add(v);pending.append(v)
    states=sorted(v for v in visited if not is_goal(v[1],labels))
    pos={v:i for i,v in enumerate(states)}; n=len(states)
    A=[[F(int(i==j)) for j in range(n)] for i in range(n)]
    for v in states:
        for u,p in trans[v].items():
            if u in pos:A[pos[v]][pos[u]]-=p
    stats['exact_policy_matrices']+=1
    t=matrix_solve(A,[F(1)]*n)
    if t is None:return False,None
    assert all(v>=1 for v in t)
    # Validate the solution, without relying on elimination status alone.
    assert all(sum(A[i][j]*t[j] for j in range(n))==1 for i in range(n))
    return True,max(t,default=F(0))

def oracle(rows,labels,initial,legal=None,skew=False):
    n=len(labels); actions=tuple(rows)
    legal=[set(actions) for _ in labels] if legal is None else legal
    masks=[m for m in range(1,1<<n) if not is_goal(m,labels)]
    options=[]
    for mask in masks:
        aa=[a for a in actions if all(a in legal[x] for x in members(mask,n))]
        options.append([tuple(aa[i] for i in range(len(aa)) if s>>i&1) for s in range(1,1<<len(aa))] or [()])
    for selection in product(*options):
        yes,t=evaluate_strategy(rows,labels,initial,legal,dict(zip(masks,selection)),skew)
        if yes:return True,t
    return False,None

def compare(rows,labels,initial,legal=None,kind='other',skew=False):
    actual=classify(rows,labels,initial,legal)
    expected,t=oracle(rows,labels,initial,legal,skew)
    assert actual['almost_sure']==expected,(kind,rows,labels,initial,legal,actual['almost_sure'],expected)
    if actual['almost_sure']:
        # Verify the produced controller itself, with no access to actual x.
        strategy={sum(1<<x for x in B):tuple(aa) for B,aa in actual['safe_actions'].items()}
        yes,bound=evaluate_strategy(rows,labels,initial,legal,strategy,skew)
        assert yes
        stats['constructed_policies_verified']+=1
    assert not actual['sure'] or actual['almost_sure']
    stats[kind]+=1
    return actual,t

# Exhaustive 3-state, 1-action models. Each of the 2 same-label states has
# one of 15 nonempty row supports; the opposite-label state one of 3.
def supports(cells):
    return [tuple(cells[i] for i in range(len(cells)) if k>>i&1) for k in range(1,1<<len(cells))]
opt0=supports([(x,o) for x in (0,1) for o in ('a','b')])
opt1=supports([(2,o) for o in ('a','b')])
for rr in product(opt0,opt0,opt1):
    for initial in ({0,2},{1,2},{0,1,2}):
        compare({'a':rr},[0,0,1],initial,kind='exhaustive_three_state_one_action')

rng=random.Random(4102026)
for k in range(384):
    rows={a:[rng.choice(opt0),rng.choice(opt0),rng.choice(opt1)] for a in ('a','b','c')}
    legal=[{a for a in rows if rng.randrange(4)} for _ in range(3)]
    compare(rows,[0,0,1],rng.choice([{0,2},{1,2},{0,1,2}]),legal,kind='seeded_three_state_three_actions',skew=True)

# Four states allow actual hidden transitions on BOTH answer labels.
opts=[supports([(y,o) for y in group for o in ('a','b')]) for group in ((0,1),(2,3))]
for k in range(512):
    rows={'a':[rng.choice(opts[x//2]) for x in range(4)]}
    legal=[{'a'} if rng.randrange(7) else set() for _ in range(4)]
    initial=rng.choice([{0,2},{0,1,2},{0,2,3},{0,1,2,3}])
    compare(rows,[0,0,1,1],initial,legal,kind='seeded_four_state_one_action',skew=True)

controls={}
# Important stationary randomization witness: neither fixed action works.
rows={'a':[{(0,'0'),(0,'w')},{(1,'w')}], 'b':[{(0,'w')},{(1,'1'),(1,'w')}]}
r,t=compare(rows,[0,1],{0,1},kind='named_controls')
assert r['almost_sure'] and not r['sure']
start=3
assert not evaluate_strategy(rows,[0,1],{0,1},None,{start:('a',)})[0]
assert not evaluate_strategy(rows,[0,1],{0,1},None,{start:('b',)})[0]
controls['randomization_replaces_support_memory']={'uniform_expected_queries':str(t),'deterministic_fixed_actions_fail':True,'sure':False}
# Each action has a positive chance of an irreversible mixed-label trap.
rows={'a':[{(0,'0'),(2,'w')},{(1,'1'),(3,'w')},{(2,'w')},{(3,'w')}]}
r,t=compare(rows,[0,1,0,1],{0,1},kind='named_controls')
assert not r['almost_sure'] and len(r['rounds'])>=3
controls['elimination_cascade']={'rounds':r['rounds'],'almost_sure':False}
# Unsafe action exposes a receipt at forbidden state; it cannot be attempted.
rows={'a':[{(0,'0')},{(1,'1')}]}
r,t=compare(rows,[0,1],{0,1},[{'a'},set()],kind='named_controls')
assert not r['almost_sure']
controls['refusal_not_free_observation']=True
# A sound stopping declaration at an initially homogeneous support needs no action.
r,t=compare({},[0,0],{0,1},[set(),set()],kind='named_controls')
assert r['sure_rank']==0 and r['almost_sure']
controls['goal_with_empty_menu_stops']=True
# All mixed deadends remain losing.
r,t=compare({},[0,1],{0,1},[set(),set()],kind='named_controls')
assert not r['almost_sure']
controls['mixed_empty_menu_loses']=True
# True non-PD state branching with immediately different future observation laws.
rows={'a':[{(0,'w'),(1,'w')},{(1,'0')},{(2,'w'),(2,'1')}]}
r,t=compare(rows,[0,0,1],{0,2},kind='named_controls')
assert r['almost_sure'] and not r['sure']
assert {o for _,o in rows['a'][0]}!={o for _,o in rows['a'][1]}
controls['nonclone_hidden_branch']={'almost_sure':True,'sure':False,'uniform_max_expected_queries':str(t),'future_observation_supports_differ':True}
# Correctly reject one-sided reveal despite a support-level path to goal.
rows={'a':[{(0,'r'),(0,'w')},{(1,'w')}]}
r,t=compare(rows,[0,1],{0,1},kind='named_controls')
assert not r['almost_sure']
for n in range(64):
    survive=F(1,2)+F(1,2)**(n+1)
    hazard=(F(1,2)**(n+2))/survive
    assert hazard==F(1,2*(2**n+1))
controls['one_sided_reveal_trap']={'almost_sure':False,'exact_prefix_checks':64,'limiting_failure_mass':'1/2'}
# Changing only positive weights never affects a qualitative result.
for rows,labels in [({'a':[{(0,'0'),(0,'w')},{(1,'1'),(1,'w')}]},[0,1]), ({'a':[{(0,'0'),(0,'w')},{(1,'w')}]},[0,1])]:
    r,t=compare(rows,labels,{0,1},kind='weight_variant_controls',skew=True)

out={'status':'PASS','method':'exhaustive stationary action-support policies; exact Fraction nonsingularity of I-Q; no use of candidate graph oracle','counts':dict(stats),'controls':controls,'candidate_solver_sha256':hashlib.sha256((SOURCE/'solver.py').read_bytes()).hexdigest(),'limitations':['Finite controls corroborate; they do not prove arbitrary-policy completeness.','These are exact stipulated-model checks, not empirical warrant or kernel verification.']}
(ROOT/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
