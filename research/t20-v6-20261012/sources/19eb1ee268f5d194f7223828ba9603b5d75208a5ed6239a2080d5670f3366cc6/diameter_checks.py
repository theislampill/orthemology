from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
norm=lambda x:sum(abs(t) for t in x)
def mul(x,P):return [sum(x[i]*P[i][j] for i in range(len(x))) for j in range(len(x))]
def ext(c,S,m):
 a=sum(c[i] for i in S);b=sum(c)-a
 return [(m*c[i]/a if a else F(0)) if i in S else ((1-m)*c[i]/b if b else F(0)) for i in range(len(c))]
cases=0;partitions=0
for nums in product(range(9),repeat=3):
 c=[F(i,4) for i in nums];C=sum(c)
 if C<1:continue
 values=[];splits=[]
 for bits in product(range(2),repeat=3):
  S={i for i,b in enumerate(bits) if b};a=sum(c[i] for i in S);b=C-a
  d=min(F(1),a)+min(F(1),b)-1
  assert d==min(F(1),C-1,a,b)
  p=ext(c,S,min(F(1),a));q=ext(c,S,max(F(0),1-b))
  assert sum(p)==sum(q)==1 and all(0<=x<=cap for x,cap in zip(p,c)) and all(0<=x<=cap for x,cap in zip(q,c))
  assert norm([x-y for x,y in zip(p,q)])/2==d
  values.append(d)
  if a>=1 and b>=1:
   splits.append(S);P=[p if i in S else q for i in range(3)]
   assert mul(p,P)==p and mul(q,P)==q and p!=q
   partitions+=1
 D=max(values);assert (D==1)==bool(splits);assert D<=min(F(1),C-1)
 cases+=1
assert max(min(F(1),sum([F(9,10),F(9,10),F(1,5)])-1,sum(c for c,b in zip([F(9,10),F(9,10),F(1,5)],bits) if b),sum(c for c,b in zip([F(9,10),F(9,10),F(1,5)],bits) if not b)) for bits in product(range(2),repeat=3))==F(9,10)
# Dyadic cap has full interval subset sums. Check finite truncation error against exact D.
prefix_cases=0
for C in [F(1),F(3,2),F(2),F(3)]:
 for N in range(1,9):
  c=[C/F(2**(j+1)) for j in range(N)]
  DN=max(min(F(1),C-1,sum(v for v,b in zip(c,bits) if b),C-sum(v for v,b in zip(c,bits) if b)) for bits in product(range(2),repeat=N))
  D=min(F(1),C-1);tail=C/F(2**N)
  assert DN<=D<=DN+tail;prefix_cases+=1
out={'status':'PASS','finite_caps':cases,'stationary_split_witnesses':partitions,'dyadic_prefix_tail_controls':prefix_cases,'C2_strict_contraction_cap':'(9/10,9/10,1/5)','C2_strict_coefficient':'9/10','scope':'Finite exact rational controls, not a proof of general subset-sum computability or effective maximizing-partition choice.'}
(R/'DIAMETER_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
