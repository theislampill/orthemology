#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json,datetime

def cert(P,good,live,acts,stay,p,s):
 block=acts[p,s]
 progress=any(not stay[p,a,y] and P[s,a,y]>0 for a in block for y in [False,True])
 self_ok=set(block)<=good[s] and all(not all(P[s,a,y]==P[t,a,y] for a in block for y in [False,True]) or set(block)<=good[t] for t in live[p])
 return progress or self_ok

def check_contracts(phases,models,P,good,live,acts,stay,nxt,rank,theta):
 assert all(sum(P[t,a,y] for y in [False,True])==1 for t in models for a in [False,True])
 assert all(P[t,a,y]>=0 for t in models for a in [False,True] for y in [False,True])
 assert all(live[p] for p in phases)
 assert all(cert(P,good,live,acts,stay,p,s) for p in phases for s in live[p])
 retention=True;decrease=True
 for p in phases:
  if theta not in live[p]:continue
  for s in models:
   for a in acts[p,s]:
    for y in [False,True]:
     if not stay[p,a,y] and P[theta,a,y]>0:
      q=nxt[p,s,y];retention &= theta in live[q];decrease &= rank[q]<rank[p]
 return retention,decrease

P={(t,a,y):F(int(y)) for t in [False,True] for a in [False,True] for y in [False,True]}
# Every selected block exits back to itself and is bad: all contracts except strict rank.
phases=[0];models=[False,True];live={0:{False,True}};good={False:set(),True:set()}
acts={(0,s):[False] for s in models};stay={(0,a,y):False for a in [False,True] for y in [False,True]};nxt={(0,s,y):0 for s in models for y in [False,True]};rank={0:0}
assert check_contracts(phases,models,P,good,live,acts,stay,nxt,rank,True)==(True,False)
selfreset=[{'horizon':n,'actual_deterministic_bad_charge':n} for n in range(21)]
# Rank drops on the first exit, but the true model is discarded. Wrong singleton then persists.
phases=[0,1];live={0:{False,True},1:{False}};good={False:{False},True:{True}}
acts={(p,s):[p==0] for p in phases for s in models}
stay={(p,a,y):p==1 for p in phases for a in [False,True] for y in [False,True]}
nxt={(p,s,y):1 for p in phases for s in models for y in [False,True]};rank={0:1,1:0}
assert check_contracts(phases,models,P,good,live,acts,stay,nxt,rank,True)==(False,True)
truthdrop=[]
for n in range(21):
 p=0;charge=0
 for i in range(n):
  s=max(live[p]);block=acts[p,s];charge+=sum(a not in good[True] for a in block)
  y=True
  if not stay[p,block[0],y]:p=nxt[p,s,y]
 assert charge==max(0,n-1)
 truthdrop.append({'horizon':n,'actual_deterministic_bad_charge':charge})
# The live mask is safe only because the actual selector is proved live.
selected=True;live_now={False};plan=[False];good_true={True}
masked=sum(a not in good_true for a in plan) if selected in live_now else 0
assert masked==0 and sum(a not in good_true for a in plan)==1
# Empty menus satisfy live self-verification and incur zero charge, but no physical actions.
empty={(p,s):[] for p in phases for s in models}
assert all(cert(P,good,live,empty,stay,p,s) for p in phases for s in live[p])
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'horizon_checks':42,'zero_support_law':{'false':'0','true':'1'},'self_reset_without_rank':selfreset,'truth_dropped_despite_rank':truthdrop,'out_of_live_mask_counterexample':{'masked_charge':0,'literal_bad_count':1},'empty_menu_vacuity':True,'scope':'Exact deterministic finite countermodels for deleted assumptions. They are not counterexamples to the admitted generated theorem; all its hypotheses are retained in the positive result.'}
Path(__file__).resolve().parents[1].joinpath('GUARD_COUNTERMODELS.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: rank, true-retention, live-mask and empty-menu controls')
