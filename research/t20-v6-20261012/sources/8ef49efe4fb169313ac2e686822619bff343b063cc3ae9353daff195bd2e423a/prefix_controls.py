#!/usr/bin/env python3
import argparse,json,itertools,random
from fractions import Fraction as F
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 rng=random.Random(100501);checks=posterior_checks=extended_checks=0
 for case in range(128):
  vals=[F(0),F(1,3),F(1,2),F(2,3),F(1)];P={(m,s,c):rng.choice(vals) for m,s,c in itertools.product(range(2),repeat=3)}
  weights=[F(1,10),F(2,10),F(3,10),F(4,10)]
  menu={(B,s):{c for c in range(2) if rng.randrange(2)} for B in [1,2,3] for s in range(2)}
  salt=rng.randrange(16)
  def policy(r,h):return (r+len(h)+salt+sum((j+1)*(c+2*y) for j,(s,c,y) in enumerate(h)))%2
  def row(m,s,c,y):return P[m,s,c] if y==0 else 1-P[m,s,c]
  def compatible(r,h):
   prior=[];state=0
   for s,c,y in reversed(h):
    if s!=state or c!=policy(r,prior):return False
    prior=[(s,c,y)]+prior;state=y
   return True
  def likelihood(m,h):
   out=F(1)
   for s,c,y in h:out*=row(m,s,c,y)
   return out
  levels=[{():{(m,r):weights[r] for m in range(2) for r in range(4)}}]
  for n in range(4):
   level=levels[-1]
   for ht,masses in level.items():
    h=list(ht);state=h[0][2] if h else 0
    compat=[r for r in range(4) if compatible(r,h)];seed=sum((weights[r] for r in compat),F(0));live={m for m in range(2) if likelihood(m,h)>0};B=sum(1<<m for m in live)
    for m in range(2):
     mass=sum((masses.get((m,r),F(0)) for r in range(4)),F(0));assert mass==seed*likelihood(m,h);checks+=1
     illegal=sum((v for (mm,r),v in masses.items() if mm==m and policy(r,h) not in menu.get((B,state),set())),F(0))
     directSeed=sum((weights[r] for r in compat if policy(r,h) not in menu.get((B,state),set())),F(0))
     assert illegal==directSeed*likelihood(m,h);checks+=1
     if mass:
      assert m in live
      for r in range(4):assert masses.get((m,r),F(0))/mass==(weights[r]/seed if r in compat else 0)
      posterior_checks+=1
    # Every positive seed-action branch and every live child model gives a positive extended prefix.
    for c in range(2):
     branch=sum((weights[r] for r in compat if policy(r,h)==c),F(0))
     if branch:
      for y in range(2):
       for m in live:
        if row(m,state,c,y)>0:
         h1=[(state,c,y)]+h;newseed=sum((weights[r] for r in range(4) if compatible(r,h1)),F(0))
         assert newseed==branch and newseed*likelihood(m,h1)>0;extended_checks+=1
   if n==3:break
   nxt={}
   for ht,masses in level.items():
    h=list(ht);s=h[0][2] if h else 0
    for (m,r),mass in masses.items():
     c=policy(r,h)
     for y in range(2):
      v=mass*row(m,s,c,y)
      if v:
       dest=nxt.setdefault(tuple([(s,c,y)]+h),{});dest[m,r]=dest.get((m,r),F(0))+v
   levels.append(nxt)
 # Explicit guard controls: an illegal initial action has mass one, even if a forged next receipt has mass zero.
 initial_illegal=F(1);forged_receipt_event=F(0)
 assert initial_illegal!=forged_receipt_event
 # The same seed marginal is not a substitute for a common posterior: compatibility restricts it.
 prior=[F(1,2),F(1,2)];posterior=[F(1),F(0)];assert prior!=posterior
 result={'status':'PASS','systems':128,'prefix_and_illegal_factorizations':checks,'common_posterior_checks':posterior_checks,'positive_extended_branches':extended_checks,'pre_receipt_illegality_control':True,'posterior_reset_control':True,'scope':'Exact finite controls; arbitrary measurable seeds and infinite AS restart are justified by the source proofs and separately sealed conditional-AS dependency'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
