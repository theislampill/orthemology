from fractions import Fraction as F
from itertools import product
B=[('s',0),('s',1)]+[('q',a,b) for a,b in product([0,1],repeat=2)]
P=list(product(B,repeat=2))
def law(t):
 return {w: {0:F(1,2)-t,1:t-F(1,6),2:F(1,3)-t,3:t}[sum(w)] for w in product([0,1],repeat=3)}
def value(p,t,a,b,c):
 v=0
 for w,m in law(t).items():
  act=p[w[0]]
  if act[0]=='q':d=act[w[1]+1];price=c
  else:d=act[1];price=0
  v+=m*(price + (a if d==1 and w[2]==0 else b if d==0 and w[2]==1 else 0))
 return v
def opt(ts,a,b,c):
 vs=[tuple(value(p,t,a,b,c) for t in ts) for p in P]
 cand=[(max(v),(i,),F(1)) for i,v in enumerate(vs)]
 for i in range(len(vs)):
  for j in range(i):
   x,y=vs[i],vs[j];di=x[0]-x[1];dj=y[0]-y[1]
   if di==dj:continue
   w=-dj/(di-dj)
   if 0<w<1: cand.append((w*x[0]+(1-w)*y[0],(i,j),w))
 v,ix,w=min(cand)
 return v,[P[i] for i in ix],w
if __name__=='__main__':
 for a in [F(1,2),F(1),F(3,2),F(2),F(5,2),F(3),F(4)]:
  for c in [F(0),F(1,100),F(1,24),F(1,12),F(1,8)]:
   r=opt([F(2,9),F(5,18)],a,F(1),c);s=opt([F(1,6),F(1,3)],a,F(1),c)
   if r!=s: print(a,c,'iid',r,'exch',s)
