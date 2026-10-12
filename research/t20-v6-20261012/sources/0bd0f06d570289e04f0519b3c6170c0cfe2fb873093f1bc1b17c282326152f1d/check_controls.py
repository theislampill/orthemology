#!/usr/bin/env python3
"""Independent finite rational checker controls; no author routines imported.
Enumeration checks local constructors, not ATM acceptance or complexity.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import json

checks=0
def ck(v):
    global checks
    assert v
    checks+=1
TOP=('top',);BOT=('bottom',)
def advance(m,s,claim,branch,ins):
    if s in (TOP,BOT):return s
    i,sigma,q,h=s
    if i==h and sigma!=claim:return BOT
    write,nxt,shift=ins[branch]
    h1=h+shift
    if not 0<=h1<m:return BOT
    if nxt=='A':return TOP
    if nxt=='R':return BOT
    return (i,write if i==h else sigma,q,h1)
def emit(tag,s):return ('ACC',TOP) if s==TOP else ('REJ',BOT) if s==BOT else (tag,s)
def kernel(m,s,claim,choice,univ,ins):
    d=defaultdict(F)
    is_univ=univ and s not in (TOP,BOT)
    for b,p in [(0,F(1,2)),(1,F(1,2))] if is_univ else [(choice,F(1))]:
        d[emit(('U',b) if is_univ else 'E',advance(m,s,claim,b,ins))]+=p
    return dict(d)

# A second evaluator computes the successful tuple first and then uses an
# explicit rejecting predicate. It does not call the first evaluator.
def oracle(m,s,claim,choice,univ,ins):
    if s==TOP:return {('ACC',TOP):F(1)}
    if s==BOT:return {('REJ',BOT):F(1)}
    i,g,q,h=s
    result=defaultdict(F)
    branches=range(2) if univ else [choice]
    for b in branches:
        w,c,d=ins[b];newh=h+d
        reject=(i==h and g!=claim) or newh<0 or newh>=m or c=='R'
        if reject:out=('REJ',BOT)
        elif c=='A':out=('ACC',TOP)
        else:out=(('U',b) if univ else 'E',(i,w if i==h else g,q,newh))
        result[out]+=F(1,len(branches))
    return dict(result)

def pd(row):
    per=defaultdict(set)
    for (o,s),p in row.items():
        if p>0:per[o].add(s)
    return all(len(ss)<=1 for ss in per.values())
def lift(out):
    o,s=out
    if s in (TOP,BOT):return s
    last=o if isinstance(o,tuple) and o[0]=='U' else 'E'
    return s+(last,)
def erase(s):return s if s in (TOP,BOT) else s[:4]
def observe(s):return 'ACC' if s==TOP else 'REJ' if s==BOT else s[4]

instructions=list(product([False,True],['Q','A','R'],[-2,-1,0,1,2]))
rows=0
for m in [1,2]:
    states=[(i,g,0,h) for i in range(m) for g in [False,True] for h in range(m)]+[TOP,BOT]
    for ins in product(instructions,repeat=2):
        for univ in [False,True]:
            for s in states:
                for claim,choice in product([False,True],repeat=2):
                    row=kernel(m,s,claim,choice,univ,ins)
                    ck(row==oracle(m,s,claim,choice,univ,ins))
                    ck(sum(row.values())==1)
                    ck(set(row.values())<={F(1,2),F(1)})
                    ck(pd(row))
                    lifted=defaultdict(F)
                    for out,p in row.items():lifted[lift(out)]+=p
                    roundtrip=defaultdict(F)
                    for ls,p in lifted.items():roundtrip[(observe(ls),erase(ls))]+=p
                    ck(dict(roundtrip)==row)
                    ck(pd({(observe(ls),ls):p for ls,p in lifted.items()}))
                    if univ:ck(row==kernel(m,s,claim,not choice,univ,ins))
                    for (o,t),p in row.items():
                        ck((o=='ACC')==(t==TOP));ck((o=='REJ')==(t==BOT))
                        if t not in (TOP,BOT):ck(t[0]==s[0])
                    rows+=1

# Truthful observations are independent of the checked index. Check full tape
# updates separately, on both control kinds and every two-cell Boolean tape.
honest=0
for tape in product([False,True],repeat=2):
    for h in range(2):
        for ins in product(instructions,repeat=2):
            for univ,choice in product([False,True],repeat=2):
                observations=[]
                for i in range(2):
                    s=(i,tape[i],0,h);row=kernel(2,s,tape[h],choice,univ,ins)
                    obs=defaultdict(F)
                    for (o,t),p in row.items():obs[o]+=p
                    observations.append(dict(obs))
                    for branch in [0,1]:
                        w,c,d=ins[branch];t=advance(2,s,tape[h],branch,ins)
                        if c=='Q' and 0<=h+d<2:
                            newtape=list(tape);newtape[h]=w
                            ck(t==(i,newtape[i],0,h+d))
                ck(observations[0]==observations[1]);honest+=1

for m in range(1,9):
    tape=[bool(i%2) for i in range(m)]
    init={(i,tape[i],0,0):F(1,m) for i in range(m)}
    ck(sum(init.values())==1);ck(len(init)==m);ck(all(p>0 for p in init.values()))
    ck({observe(s+('E',)) for s in init}=={'E'})

s0=(0,False,0,0);s1=(1,False,0,0)
badboot={('E',s0):F(1,2),('E',s1):F(1,2)}
fork=((False,'Q',0),(True,'Q',0))
good=kernel(2,s0,False,False,True,fork)
hidden={('E',s):p for (o,s),p in good.items()}
negative={
 'known_boot_hidden_selection_not_pd':not pd(badboot),
 'suppressed_branch_receipt_not_pd':not pd(hidden),
 'invalid_copy_receipt_not_preserved':observe(lift(('ACC',s0)))!='ACC',
 'revealed_initial_label_not_common':len({('index',s[0]) for s in [s0,s1]})!=1,
 'out_of_bounds_acceptance_must_reject':advance(2,s0,False,0,((False,'A',-1),)*2)==BOT,
 'unchecked_false_read_can_survive':advance(2,s1,True,0,fork)==s1 and advance(2,s0,True,0,fork)==BOT,
}
for v in negative.values():ck(v)
print(json.dumps({'status':'PASS_INDEPENDENT_LOCAL_CONTROLS','exact_assertions':checks,
 'kernel_rows':rows,'honest_index_pairs':honest,'negative_controls':negative,
 'formal_complexity_credit':False,'global_path_law_credit':False},indent=2,sort_keys=True))
