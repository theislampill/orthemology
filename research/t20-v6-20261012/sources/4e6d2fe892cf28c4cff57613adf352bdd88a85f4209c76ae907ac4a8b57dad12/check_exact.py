from fractions import Fraction as F
from itertools import product
import json, sys
n=0
def check(b, label):
 global n
 n+=1
 if not b: raise RuntimeError(label)
def bounds(t): return 12*t*t-4*t+F(4,9), -6*t*t+5*t-F(2,3)
def wordmass(w,t,s):
 return [1-4*t+s,-F(1,2)+3*t-s,F(1,3)-2*t+s,t-s,s][sum(w)]
def actual(t,s,c):
 out=[F(0)]*6
 for w in product((0,1),repeat=4):
  p=wordmass(w,t,s)
  check(p>=0,'complete word positivity')
  if w[:2]!=(1,1):continue
  x,y=w[2:]; reports=[0,1,0,x,1-x,1]
  for i,r in enumerate(reports):out[i]+=3*p*(int(r!=y)+(c if i>=2 else 0))
 return out
def formula(t,s,c):return [3*t,1-3*t,c+3*t,c+6*(t-s),c+1-6*(t-s),c+1-3*t]
c=F(1,10); t=F(1,4)
L,U=bounds(t)
check((L,U)==(F(7,36),F(5,24)),'C4 fibre')
fixtures=[(t,L),(t,U),(F(1,6),F(0)),(t,t),(F(1,3),F(1,3))]
for t0,s0 in fixtures:
 masses=[wordmass(w,t0,s0) for w in product((0,1),repeat=4)]
 check(sum(masses)==1,'law normalization')
 words=list(product((0,1),repeat=4))
 check(sum(p for p,w in zip(masses,words) if w[0])==F(1,2),'first moment')
 check(sum(p for p,w in zip(masses,words) if w[0] and w[1])==F(1,3),'history mass')
 z=actual(t0,s0,c)
 check(z==formula(t0,s0,c),'six independent complete-word losses')
 rt=(1-z[1])/3; rs=rt-(c+1-z[4])/6
 check((rt,rs)==(t0,s0),'profile inverse')
a,b=actual(t,L,c),actual(t,U,c)
check(a[1]==b[1]==F(1,4),'same posterior skip collision')
check((a[4],b[4])==(F(23,30),F(17,20)),'distinct invert losses')
check(b[4]-a[4]==F(1,12),'exact lost interaction')
# Every tested tag assignment collides; finite check illustrates universal pigeonhole proof.
M=3
ss=[L+(U-L)*F(j,M) for j in range(M+1)]
for tags in product(range(M),repeat=M+1):
 found=False
 for i in range(M+1):
  for j in range(i):
   if tags[i]==tags[j] and formula(t,ss[i],c)[4]!=formula(t,ss[j],c)[4]:found=True
 check(found,'finite tags cannot separate chosen fibre')
vertices=fixtures[2:]
mat=[actual(x,y,c) for x,y in vertices]
eta=[F(17,25),F(8,25),F(0)]
v=F(21,50)
check(max(F(4,5)*r[1]+F(1,5)*r[4] for r in mat)==v,'inherited E4 primal')
check(min(sum(eta[j]*mat[j][i] for j in range(3)) for i in range(6))==v,'inherited E4 dual')
check(a!=b,'same fixed C4 minimax answer does not imply same model profile')
# Each rational full-word row has a finite counting realization; counts use common denominator.
from math import lcm
for x,y in fixtures:
 ps=[wordmass(w,x,y) for w in product((0,1),repeat=4)]
 D=lcm(*(p.denominator for p in ps))
 counts=[p*D for p in ps]
 check(all(k.denominator==1 for k in counts) and sum(counts)==D,'rational seed counting repair')
mutation=sys.argv[1] if len(sys.argv)>1 else None
if mutation=='posterior_sufficient':check(a==b,'REJECT posterior-only preserves losses')
if mutation=='minimax_implies_profile':check(a==b,'REJECT common fixed-game answer preserves losses')
if mutation=='uniform_seed_three':check(all((p*3).denominator==1 for p in [F(1,4),F(3,4)]),'REJECT seed-size ignores denominators')
print(json.dumps({'status':'PASS','checks':n,'scope':'exact finite controls; universal results require written proofs'}))
