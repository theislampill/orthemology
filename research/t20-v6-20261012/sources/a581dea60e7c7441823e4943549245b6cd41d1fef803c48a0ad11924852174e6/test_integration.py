#!/usr/bin/env python3
from itertools import product
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import json,datetime

def alpha(e,t): return F(1,2)+(e if t else -e)
def law(e,t,y):return alpha(e,t) if y else 1-alpha(e,t)
def good(a,e,q):return q*q<=a*(F(1,2)+e)**2+(1-a)*F(1,2)**2 and (1-q)**2<=a*(F(1,2)-e)**2+(1-a)*F(1,2)**2

def choose(e,initial,hist,tape,order):
 count=Counter(hist)
 scores={t:F(1) for t in [False,True]}
 for t in scores:
  for a in [False,True]:
   for k in range(count[a]):scores[t]*=law(e,t,tape[a][k])
 best=initial
 for t in order:
  if scores[best]<=scores[t]:best=t
 assert scores[best]==max(scores.values())
 return best

def run(e,initial,tape,n,order):
 hist=[]
 for k in range(n):hist.append(choose(e,initial,hist,tape,order))
 return hist,choose(e,initial,hist,tape,order)

locality=target=0
for en in [1,2,4]:
 e=F(en,16)
 for t,a in product([False,True],repeat=2):
  q=F(1,2)+alpha(e,a)*e
  assert good(alpha(e,t),e,q)==(a==t) and 0<q<1
  assert sum(law(e,t,y) for y in [False,True])==1
  target+=1
 for order in [(False,True),(True,False)]:
  for initial in [False,True]:
   for bits in product([False,True],repeat=6):
    tape={False:bits[:3],True:bits[3:]}
    for n in range(4):
     hist,selected=run(e,initial,tape,n,order);counts=Counter(hist)
     assert sum(counts.values())==n
     for a in [False,True]:
      for k in range(counts[a],3):
       altered={False:list(tape[False]),True:list(tape[True])};altered[a][k]=not altered[a][k]
       assert run(e,initial,altered,n,order)==(hist,selected)
       locality+=1
# Full support never provides finite certainty for both candidate models.
finite_errors=[]
for e in [F(1,8),F(1,4)]:
 for theta in [False,True]:
  for order in [(False,True),(True,False)]:
   for n in [1,2,4,8]:
    error=F(0)
    for bits in product([False,True],repeat=n):
     tape={False:[],True:[]};hist=[];mass=F(1)
     for y in bits:
      a=choose(e,False,hist,tape,order)
      tape[a].append(y);hist.append(a);mass*=law(e,theta,y)
     if choose(e,False,hist,tape,order)!=theta:error+=mass
    assert 0<error<1
    finite_errors.append({'epsilon':str(e),'theta':theta,'order':order,'n':n,'error':str(error)})
# Identical coordinate marginals with total temporal dependence are insufficient.
for theta in [False,True]:
 p=alpha(F(1,4),theta)
 assert p!=p*p
 for bit in [False,True]:
  tape={False:[bit]*24,True:[bit]*24}
  for order in [(False,True),(True,False)]:
   for initial in [False,True]:
    for n in range(1,21):assert run(F(1,4),initial,tape,n,order)[1]==bit
 # Persistent random bit causes eventual wrong selection with probability 1/4.
 assert (p if not theta else 1-p)==F(1,4)
# A one-step peek changes a zero-history decision when only unread entries change.
assert choose(F(1,4),False,[False],{False:[False],True:[]},(False,True))!=choose(F(1,4),False,[False],{False:[True],True:[]},(False,True))
res={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target_label_cases':target,'unacquired_coordinate_locality_checks':locality,'finite_error_probabilities':finite_errors,'persistent_bit_counterexample_error':'1/4','scope':'Exact rational specialization tested for both possible fixed Boolean list orders; not execution/extraction of the noncomputable real Lean selector. Finite tests do not prove the almost-sure limit.'}
Path(__file__).resolve().parents[1].joinpath('FINITE_CONTROLS.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k!='finite_error_probabilities'},indent=2))
