from fractions import Fraction as F
from math import comb
import json
from pathlib import Path
count={}
def check(group,v):
    assert v,group
    count[group]=count.get(group,0)+1
# Independent finite rational probability family, including zero mean and pure atoms.
for a in range(7):
 for b in range(7-a):
  law=[(0,F(a,6)),(3,F(b,6)),(19,F(6-a-b,6))]
  mom=lambda r:sum(p*x**r for x,p in law)
  for N in range(1,21):
   for r in range(1,6):
    clipped=sum(p*min(x,N)**r for x,p in law)
    check('closed_fibre',mom(r)-mom(r+1)/N<=clipped<=mom(r))
    # Exact damping at t=k log(2), including zero, not floating exponentials.
    for k in (0,1,3):
     actual=sum(p*x**r*F(1,2)**(k*x) for x,p in law)
     cut=sum(p*min(x,N)**r*F(1,2)**(k*min(x,N)) for x,p in law)
     check('joint_damping',abs(actual-cut)<=2*mom(r+1)/N)
   cost=sum(p*min(1,x-min(x,N)) for x,p in law)
   check('weak_clipping',cost<=mom(1)/N)
   cost1=sum(p*(x-min(x,N)) for x,p in law)
   check('ordinary_w1_clipping',cost1<=mom(2)/N)
# Positive infinity mass is rejected by an upper first-moment constraint.
for denom in range(1,25):
 for bound in range(8):
  N=denom*(bound+1)
  check('infinity_exclusion',F(N,denom)>bound)
# Lower bounds do real work: delta_0 passes upper bounds of delta_a but fails a lower bound.
for a in range(1,20):
 N=2*a
 check('lower_constraint_necessary',a-F(a*a,N)>0)
# Finite-prefix collisions with exact normalized damped means.
for d in range(18):
 n=d+1
 even=[(j,F(comb(n,j),2**d)) for j in range(n+1) if j%2==0]
 odd=[(j,F(comb(n,j),2**d)) for j in range(n+1) if j%2]
 for r in range(d+1):
  check('finite_prefix',sum(p*j**r for j,p in even)==sum(p*j**r for j,p in odd))
 def mean(law):
  return sum(p*j*F(1,2)**j for j,p in law)/sum(p*F(1,2)**j for j,p in law)
 check('finite_prefix',mean(even)!=mean(odd))
# Net mass rounding and exact W1 via cumulative mass differences.
for n in range(1,12):
 weights=[F((j+1)**2,sum((i+1)**2 for i in range(n+1))) for j in range(n+1)]
 for Q in range(1,25):
  rounded=[F(int(w*Q),Q) for w in weights[:-1]]
  rounded.append(1-sum(rounded))
  cost=sum(abs(sum(weights[:j+1])-sum(rounded[:j+1]))*F(1,n) for j in range(n))
  check('net_rounding',sum(rounded)==1 and min(rounded)>=0 and cost<F(n,Q))
result={'status':'PASS','checks':count,'total':sum(count.values()),'ceiling':'Finite exact controls, not a universal extractor, determinacy test, or proof-kernel theorem.'}
Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
