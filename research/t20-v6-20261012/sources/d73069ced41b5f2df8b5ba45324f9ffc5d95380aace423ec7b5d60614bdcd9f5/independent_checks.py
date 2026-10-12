from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
norm=lambda x:sum(abs(a) for a in x)
def mul(x,P):return [sum(x[i]*P[i][j] for i in range(len(x))) for j in range(len(P[0]))]
def minus(x,y):return [a-b for a,b in zip(x,y)]
rows=[[F(i,4),F(j,4),F(4-i-j,4)] for i in range(5) for j in range(5-i)]
n=0;strict=0
for P in product(rows,repeat=3):
 cap=[max(row[j] for row in P) for j in range(3)];C=sum(cap)
 delta=max(norm(minus(x,y))/2 for x in P for y in P)
 assert delta<=min(F(1),C-1)
 for x in P:
  for y in P:assert sum(min(a,b) for a,b in zip(x,y))>=2-C
 if C<2:strict+=1
 n+=1
sharp=[]
for k in range(9):
 rho=F(k,8);C=1+rho;P=[[F(1),F(0)],[1-rho,rho]]
 assert max(norm(minus(x,y))/2 for x in P for y in P)==C-1
 mu=[F(0),F(1)]
 for t in range(9):
  assert norm(minus(mu,[F(1),F(0)]))==2*rho**t
  mu=mul(mu,P)
 sharp.append(str(C))
P=[[F(0),F(1)],[F(1),F(0)]]
cesaro=[]
for N in range(1,21):
 mu=[F(1),F(0)];avg=[F(0),F(0)]
 for k in range(N):
  avg=[a+x/N for a,x in zip(avg,mu)];mu=mul(mu,P)
 residual=norm(minus(mul(avg,P),avg));assert residual<=F(2,N)
 assert residual==(F(2,N) if N%2 else 0)
 cesaro.append(str(residual))
for k in range(1,16):
 e=F(1,2**k)
 P=[[1-e,e],[F(0),F(1)]];Q=[[F(1),F(0)],[e,1-e]]
 assert mul([F(0),F(1)],P)==[F(0),F(1)]
 assert mul([F(1),F(0)],Q)==[F(1),F(0)]
 assert norm(minus(mul([F(1),F(0)],P),[F(1),F(0)]))==2*e
 assert norm(minus([F(0),F(1)],[F(1),F(0)]))==2
# Finite detailed-balance/current control for the symbolic Specker boundary.
w=[F(1)]+[F(1,2**n)+F((n%3),100) for n in range(1,12)]
P=[[F(0) for _ in w] for _ in w]
for i in range(len(w)-1):
 h=min(w[i],w[i+1])/4;P[i][i+1]=h/w[i];P[i+1][i]=h/w[i+1]
for i in range(len(w)):P[i][i]=1-sum(P[i]);assert P[i][i]>=F(1,2)
assert mul(w,P)==w
pi=[x/sum(w) for x in w];assert mul(pi,P)==pi
out={'status':'PASS','three_state_cap_checks':n,'strict_cap_cases':strict,'sharp_cap_totals':sharp,'periodic_Cesaro_residuals':cesaro,'selector_axis_and_small_residual_cases':15,'finite_birth_death_detailed_balance':True,'scope':'Finite rational controls supplement ordinary proofs; they do not establish undecidability or infinite-dimensional effectiveness by enumeration.'}
(R/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
