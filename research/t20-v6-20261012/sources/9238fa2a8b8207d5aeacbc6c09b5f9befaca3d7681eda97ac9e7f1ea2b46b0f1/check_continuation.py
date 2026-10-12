#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import json

prior={0:F(1,3),1:F(2,3)}
grid=[F(1,4),F(1,2),F(3,4)]
policies=list(product(product((0,1),repeat=3),repeat=2))
def action(pol,r,h):return pol[r][0] if not h else pol[r][1+h[0][1]]
def kill(path,D,delay=False):
    out=[]
    for h in path:
        checked=h[1:] if delay else h
        alive=all(a in D for a,y in checked)
        out.append((alive,h if alive else ()))
    return tuple(out)
def advance(rows,pol,r,h):
    a=action(pol,r,h)
    for y,p in [(0,rows[a]),(1,1-rows[a])]:
        if p:yield ((a,y),)+h,p

def actual_conditionals(rows,pol,D,delay=False):
    masses=defaultdict(F);seedweights=defaultdict(F);outputs=defaultdict(lambda:defaultdict(F));raws=defaultdict(lambda:defaultdict(F))
    for r,pr in prior.items():
        for old,pold in advance(rows,pol,r,()):
            masses[old]+=pr*pold;seedweights[(old,r)]+=pr*pold
            nodes=[(old,((),),pr*pold)]
            for n in (1,2):
                nxt=[]
                for h,path,w in nodes:
                    for hh,p in advance(rows,pol,r,h):nxt.append((hh,path+(hh[:n],),w*p))
                nodes=nxt
            for h,path,w in nodes:
                outputs[old][kill(path,D,delay)]+=w;raws[old][path]+=w
    return ({h:{k:w/masses[h] for k,w in law.items()} for h,law in outputs.items()},
      {h:{r:seedweights[(h,r)]/masses[h] for r in prior} for h in masses},
      {h:{k:w/masses[h] for k,w in law.items()} for h,law in raws.items()},dict(masses))
def restart(rows,pol,old,posterior,D,wrong_side=False):
    raw=defaultdict(F)
    for r,pr in posterior.items():
        nodes=[((),((),),pr)]
        for n in (1,2):
            nxt=[]
            for tail,path,w in nodes:
                h=old+tail if wrong_side else tail+old
                a=action(pol,r,h)
                for y,p in [(0,rows[a]),(1,1-rows[a])]:
                    if p:
                        tt=((a,y),)+tail;nxt.append((tt,path+(tt,),w*p))
            nodes=nxt
        for tail,path,w in nodes:
            if w:raw[path]+=w
    return dict(raw)

restart_cases=0;transfer_cases=0;different_prefix_likelihoods=0
for p0,p1,q1 in product(grid,repeat=3):
    for pol in policies:
        lp,sp,rp,mp=actual_conditionals((p0,p1),pol,{0})
        lq,sq,rq,mq=actual_conditionals((p0,q1),pol,{0})
        assert lp.keys()==lq.keys()
        for h in lp:
            assert sp[h]==sq[h]
            assert lp[h]==lq[h]
            assert rp[h]==restart((p0,p1),pol,h,sp[h],{0})
            assert rq[h]==restart((p0,q1),pol,h,sq[h],{0})
            transfer_cases+=1;restart_cases+=2
            if mp[h]!=mq[h]:different_prefix_likelihoods+=1
# Delayed killing reveals the first outside receipt even after prefix conditioning.
allone=((1,1,1),(1,1,1))
a=actual_conditionals((F(1,2),F(1,4)),allone,{0},True)[0]
b=actual_conditionals((F(1,2),F(3,4)),allone,{0},True)[0]
assert a!=b
# Wrong concatenation reads the old receipt rather than the newest continuation.
react=((1,0,1),(1,0,1));rows=(F(1,2),F(1,2));old=((1,0),)
assert restart(rows,react,old,prior,{0,1})!=restart(rows,react,old,prior,{0,1},True)
# Restoring the old prior instead of the derived posterior changes continuation.
seed_action=((0,0,0),(1,1,1));_,posts,raws,_=actual_conditionals(rows,seed_action,{0,1});h=((1,0),)
assert raws[h]!=restart(rows,seed_action,h,prior,{0,1})
print(json.dumps({'status':'PASS_EXACT_CONDITIONAL_CONTINUATION_CONTROLS','actual_to_restart_comparisons':restart_cases,
 'cross_model_killed_law_comparisons':transfer_cases,'comparisons_with_different_prefix_likelihoods':different_prefix_likelihoods,
 'checks':{'full_conditional_continuation_equals_restart':True,'matching_retained_rows_transfer':True,
 'delayed_kill_counterexample':True,'wrong_append_direction_counterexample':True,'resetting_seed_prior_counterexample':True},
 'scope':'Finite exact controls; infinite observed-law identification is separately proved and cold-replayed in Lean'},indent=2))
