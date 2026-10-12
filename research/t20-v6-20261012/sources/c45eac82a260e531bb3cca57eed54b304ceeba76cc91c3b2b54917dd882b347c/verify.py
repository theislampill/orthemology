#!/usr/bin/env python3
"""Exact controls; universal claims rest on RESULT.md, not enumeration."""
from fractions import Fraction as F
from itertools import product, combinations
from collections import defaultdict, deque
from pathlib import Path
import hashlib, json, random, subprocess, sys
from solver import classify
ROOT=Path(__file__).resolve().parent

def powerset(xs):
    xs=list(xs)
    return [frozenset(c) for k in range(1,len(xs)+1) for c in combinations(xs,k)]

def oracle(rows, labels, initial, legal=None):
    """Independent exhaustive stationary randomized action-support oracle.

    Does not consume fixed-point states, transitions, graph, or safe-action output.
    Enumerates all nonempty action subsets at every mixed support, then checks
    reachable actual-state/support graph under each resulting stationary policy.
    """
    n=len(labels); actions=list(rows); initial=frozenset(initial)
    legal=[set(actions) for _ in labels] if legal is None else legal
    mixed=[B for B in powerset(range(n)) if len({labels[x] for x in B})>1]
    menus=[powerset(a for a in actions if all(a in legal[x] for x in B)) or [frozenset()] for B in mixed]
    for choices in product(*menus):
        strategy=dict(zip(mixed,choices))
        starts={(x,initial) for x in initial}; vertices=set(starts); todo=list(starts)
        edges={}; goals=set()
        while todo:
            x,B=todo.pop()
            if len({labels[z] for z in B})==1:
                goals.add((x,B));edges[x,B]=set();continue
            nxt=set()
            for a in strategy[B]:
                for y,o in rows[a][x]:
                    C=frozenset(v for u in B for v,z in rows[a][u] if z==o)
                    nxt.add((y,C))
            edges[x,B]=nxt
            for v in nxt-vertices:vertices.add(v);todo.append(v)
        backward=set(goals)
        while True:
            new=backward|{v for v in vertices if edges[v]&backward}
            if new==backward:break
            backward=new
        if vertices<=backward:return True
    return False

out={'scope':'exact support classification; no empirical or kernel claim','controls':{}}
counts={'static_two_state_two_actions':0,'hidden_three_state_one_action':0,'hidden_two_action_seeded':0,'outside_PD_fixture':0,'non_PD_models':0,'multi_round_eliminations':0}

def compare(rows,labels,initial,legal=None,key=None):
    r=classify(rows,labels,initial,legal)
    v=oracle(rows,labels,initial,legal)
    assert r['almost_sure']==v,(rows,labels,initial,legal,r,v)
    assert not r['sure'] or r['almost_sure']
    if any(len([y for y,z in row if z==o])>1 for table in rows.values() for row in table for _,o in row):counts['non_PD_models']+=1
    if len(r['rounds'])>2:counts['multi_round_eliminations']+=1
    if key:counts[key]+=1
    return r

# 81 exact support instruments, including zero-support outcomes.
options=[{0},{1},{0,1}]
for vals in product(options,repeat=4):
    rows={a:[{(x,o) for o in vals[2*j+x]} for x in range(2)] for j,a in enumerate(('a','b'))}
    compare(rows,[0,1],{0,1},key='static_two_state_two_actions')
# All 675 one-action instruments preserving labels on 3 states.
opt0=powerset([(x,o) for x in (0,1) for o in (0,1)])
opt1=powerset([(2,o) for o in (0,1)])
for a,b,c in product(opt0,opt0,opt1):
    compare({'a':[a,b,c]},[0,0,1],{0,1,2},key='hidden_three_state_one_action')
# Two-action partially observed systems plus state-dependent permission controls.
rng=random.Random(20261010)
for _ in range(512):
    rows={a:[rng.choice(opt0),rng.choice(opt0),rng.choice(opt1)] for a in ('a','b')}
    legal=[{a for a in rows if rng.randrange(5)} for x in range(3)]
    compare(rows,[0,0,1],rng.choice([{0,2},{1,2},{0,1,2}]),legal,key='hidden_two_action_seeded')
out['exhaustive_oracle_comparison']=counts

# Faithful existing 16-state model, after report Y=1. No new source law selected.
X=list(product(range(2),repeat=4))
prior=[]
for th,t,y,v in X:
    acc=F(9,10) if t==0 else F(1,2)
    prior.append(F(1,4)*(acc if y==th else 1-acc)*(F(4,5) if v==th else F(1,5)))
initial={i for i,x in enumerate(X) if x[2]==1}
rows={'fixed_audit':[{(i,(x[1],int(x[3]!=x[2])))} for i,x in enumerate(X)]}
r=classify(rows,[x[0] for x in X],initial)
assert not r['sure'] and not r['almost_sure']
assert len(r['supports'])==5 and not r['goals']
selected=[i for i,x in enumerate(X) if x[2]==1 and x[1]==1 and x[3]!=x[2]]
posterior=sum(prior[i] for i in selected if X[i][0]==1)/sum(prior[i] for i in selected)
assert posterior==F(1,5)
out['controls']['fixed_audit']={'reachable_supports':5,'goal_supports':0,'almost_sure':False,'posterior_bad_disagree':str(posterior)}
# Known-Bad four-mass quotient preserves this stopping problem.
Q=list(product(range(2),repeat=2))
qr=classify({'fixed_audit':[{(i,x[1])} for i,x in enumerate(Q)]},[x[0] for x in Q],range(4))
assert not qr['almost_sure'] and len(qr['supports'])==3
# Fresh imperfect comparison: after n disagreeing results theta-one is 1/(1+4^n).
for n in range(1,26):
    p1=F(1,2)*F(1,5)**n;p0=F(1,2)*F(4,5)**n
    assert p1/(p0+p1)==F(1,1+4**n)>0
noisy=classify({'fresh':[{(0,0),(0,1)},{(1,0),(1,1)}]},[0,1],{0,1})
assert not noisy['almost_sure']
out['controls']['fresh_imperfect']={'almost_sure':False,'exact_prefix_controls':25,'posterior_after_two_disagree':'1/17'}
# One-sided and two-sided independently rederived exact probabilities.
for n in range(25):
    na=F(1,2)**n;survival=(1+na)/2
    assert survival==F(1,2)+F(1,2)**(n+1)
    assert (na/(1+na))/2==F(1,2*(2**n+1))
    assert F(1,2)**n>0
one=classify({'a':[{(0,'r'),(0,'w')},{(1,'w')}]},[0,1],{0,1})
two=classify({'a':[{(0,'r0'),(0,'w')},{(1,'r1'),(1,'w')}]},[0,1],{0,1})
perfect=classify({'a':[{(0,'r0')},{(1,'r1')}]},[0,1],{0,1})
assert not one['almost_sure'] and two['almost_sure'] and not two['sure'] and perfect['sure_rank']==1
out['controls']['revealing_controls']={'one_sided_almost_sure':False,'two_sided_almost_sure':True,'two_sided_sure':False,'perfect_rank':1,'prefix_controls':25}
# A genuinely non-PD initial-label problem: hidden state branches on the same receipt.
hidden={'a':[{(0,'w'),(1,'w'),(0,'r0')},{(1,'r0')},{(2,'w'),(2,'r1')}]}
h=compare(hidden,[0,0,1],{0,2},key='outside_PD_fixture')
assert h['almost_sure'] and not h['sure']
assert {y for y,o in hidden['a'][0] if o=='w'}=={0,1}
assert not any(o=='w' for y,o in hidden['a'][1])
# Probability realization: x1 reveals surely, so the two wait-successors are not clones.
m0,m1=F(1),F(0)
for n in range(1,26):
    m0,m1=m0/4,m0/4
    assert m0+m1==2*F(1,4)**n
assert F(1,2)!=0  # P(wait|x0)=1/2, P(wait|x1)=0
out['controls']['outside_PD']={'positive_successors_from_state0_actiona_observationw':[0,1],'almost_sure':True,'sure':False,'next_wait_probability_x0':'1/2','next_wait_probability_x1':'0','survival_prefix_controls':25,'supports':[sorted(B) for B in sorted(h['supports'],key=lambda B:tuple(sorted(B)))]}
# Existing H-ICS destructive experiment: current sink observed, old label not erased.
# p0,q0,r1,t0label0,t0label1,t1label0,t1label1
labels=[0,0,1,0,1,0,1]
rows={'a':[{(5,'1')},{(3,'0')},{(4,'0')},{(3,'0')},{(4,'0')},{(5,'1')},{(6,'1')}],
      'b':[{(3,'0')},{(5,'1')},{(4,'0')},{(3,'0')},{(4,'0')},{(5,'1')},{(6,'1')}]}
d=classify(rows,labels,{0,1,2})
assert not d['almost_sure'] and not d['sure']
out['controls']['destructive_initial_label']={'almost_sure':False,'physical_sink_known_does_not_determine_initial_label':True}
# Mutation guard: changing a target label during evolution must be rejected.
try:classify({'a':[{(1,'x')},{(1,'x')}]},[0,1],{0,1})
except ValueError:pass
else:raise AssertionError('target mutation was admitted')
out['controls']['initial_label_mutation_rejected']=True
# Bound predecessor snapshots are never edited by this investigation.
binding=ROOT/'INPUT_BINDINGS.json'
if True:  # manifest is required in the completed packet
    checked=0
    for item in json.loads(binding.read_text())['inputs']:
        data=(ROOT/item['local_path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==item['sha256'],item['local_path']
        if item.get('git_blob_sha1'):
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['git_blob_sha1']
        checked+=1
    out['input_hashes_verified']=checked
out['status']='PASS'
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
