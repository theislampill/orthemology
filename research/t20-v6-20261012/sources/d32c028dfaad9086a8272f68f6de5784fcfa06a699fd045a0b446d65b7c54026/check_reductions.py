from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import prod
import hashlib,json

def interp(laws,labels,word):
 m=len(laws)
 if m==1:return F(labels[0])
 H=F(0)
 for i in range(m):
  factors=[]
  for pos,j in enumerate(j for j in range(m) if j!=i):
   z=next(z for z in range(len(laws[i])) if laws[i][z]!=laws[j][z])
   factors.append((F(word[pos]==z)-laws[j][z])/(laws[i][z]-laws[j][z]))
  H+=labels[i]*prod(factors)
 return H

def main():
 interpolation=0;sticky=0;cycles=0;hazards=0
 families=[[(F(1,2),F(1,2))],[(1-p,p) for p in [F(1,4),F(1,2),F(3,4)]],[(1-p,p) for p in [F(0),F(1,3),F(2,3),F(1)]],[(F(1,2),F(1,2),F(0)),(F(0),F(1,2),F(1,2)),(F(1,3),F(1,3),F(1,3))]]
 for laws in families:
  m=len(laws);r=max(1,m-1);words=list(product(range(len(laws[0])),repeat=r))
  for labels in product([0,1],repeat=m):
   table={w:interp(laws,labels,w) for w in words}
   B=max(F(1),*(abs(v) for v in table.values()));delta=1/(2*B)
   rewards={w:(v-1)/(2*B) for w,v in table.items()}
   assert max(rewards.values())-min(rewards.values())<=1
   for i,law in enumerate(laws):
    mean=sum(prod(law[x] for x in w)*table[w] for w in words)
    rmean=sum(prod(law[x] for x in w)*rewards[w] for w in words)
    assert mean==labels[i] and rmean==(0 if labels[i] else -delta);interpolation+=1
 # Arbitrary realised rewards: the charging inequalities themselves are pathwise.
 for K in [1,2,3,4]:
  for high in range(K):
   low=set(range(K))-{high}
   for T in range(1,11):
    for word in product([-1,1],repeat=T):
     arm=0;counts=[0]*K;sums=[0]*K;A=0;L=0;H=0;E=0
     for reward in word:
      counts[arm]+=1;sums[arm]+=reward
      mean=F(sums[arm],counts[arm]);L+=arm in low
      H+=arm==high and mean<F(-1,4)
      E+=arm in low and mean>=F(-1,4)
      if mean<F(-1,4):A+=1;arm=(arm+1)%K
     assert A<=K*(H+1) and L<=1+A+E;sticky+=1
 # Remembered actions separate two cycle laws that state-only recording merges.
 p0={'a':F(1,4),'b':F(3,4)};p1={'a':F(3,4),'b':F(1,4)}
 c0={(a,y):F(1,2)*(p if y else 1-p) for a,p in p0.items() for y in [0,1]}
 c1={(a,y):F(1,2)*(p if y else 1-p) for a,p in p1.items() for y in [0,1]}
 assert sum(c0.values())==sum(c1.values())==1 and c0!=c1
 for y in [0,1]:assert sum(c0[a,y] for a in p0)==sum(c1[a,y] for a in p1);cycles+=1
 for a in p0:
  assert c0[a,1]/(c0[a,0]+c0[a,1])==p0[a]
  assert c1[a,1]/(c1[a,0]+c1[a,1])==p1[a];cycles+=2
 # Stopped two-action law for a half-probability revealing symbol.
 law={'exit_1':F(1,2),'exit_01':F(1,4),'no_00':F(1,4)}
 assert sum(law.values())==1
 unconditional_no_exit_mean=law['no_00'];conditional_no_exit_mean=F(1)
 assert unconditional_no_exit_mean!=conditional_no_exit_mean
 for j in range(1,51):
  survival=F(1,4)**(j-1)
  assert survival==(1-F(3,4))**(j-1)
  total=sum(F(1,4)**k for k in range(j))
  assert total<=F(4,3);hazards+=1
 # Equal stopped laws with a first-step support change do not identify later rows.
 first_rows=[(F(1),F(0)),(F(1),F(0)),(F(0),F(1))]
 second_rows=[(F(1),F(0)),(F(0),F(1)),(F(1,2),F(1,2))]
 B={0,1,2};successor={i for i in B if first_rows[i][0]>0}
 assert successor=={0,1} and first_rows[0]==first_rows[1] and second_rows[0]!=second_rows[1]
 # A permitted pre-exit action can be impermissible immediately after revelation.
 menu={frozenset(B):{'a','b'},frozenset(successor):{'b'}}
 assert 'a' in menu[frozenset(B)] and 'a' not in menu[frozenset(successor)]
 out={'status':'PASS','interpolation_model_label_checks':interpolation,'arbitrary_reward_path_charging_checks':sticky,'cycle_action_retention_checks':cycles,'exact_hazard_partial_sums':hazards,'censoring_bias_control':True,'unplayed_row_identification_countercontrol':True,'nonmonotone_menu_countercontrol':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Fresh exact finite corroboration of ordinary proof review; not kernel qualification'}
 Path(__file__).with_name('evidence').joinpath('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
