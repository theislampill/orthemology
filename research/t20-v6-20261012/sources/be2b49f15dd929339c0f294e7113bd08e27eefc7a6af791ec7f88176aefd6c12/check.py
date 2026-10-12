from fractions import Fraction as F
from itertools import product
checks=0
def check(p,msg):
 global checks
 if not p: raise RuntimeError(msg)
 checks+=1
L=[tuple(F(n,40) for n in ns) for ns in ((1,9,9,21),(9,1,21,9))]
def loss(v,x,y):
 a,b,c,d=v
 return x*b+(1-x)*(a+b)*F(3,5)+y*c+(1-y)*(c+d)*F(3,5)
# Independent exact endpoint calculation, theta/audit order inherited.
values={(x,y):tuple(loss(v,F(x),F(y)) for v in L) for x,y in product((0,1),repeat=2)}
check(values[(1,1)]==(F(9,20),F(11,20)),'risky both')
check(values[(0,0)]==(F(3,5),F(3,5)),'defer both')
check(values[(1,0)]==(F(27,40),F(19,40)),'risk/defer')
check(values[(0,1)]==(F(3,8),F(27,40)),'defer/risk')
check(min(max(v) for v in values.values())==F(11,20),'deterministic optimum')
check(tuple(loss(v,F(1),F(2,3)) for v in L)==(F(21,40),)*2,'randomized attainable')
# Analytic lower bound for ALL x,y in [0,1]: weighted loss L1/4+3L2/4 = 3/5-3x/40 >=21/40.
# Coefficients determined exactly at basis points; affinity independently verified below.
for x,y in product((F(0),F(1),F(2,3)),repeat=2):
 z=[loss(v,x,y) for v in L]
 check(z[0]/4+3*z[1]/4==F(3,5)-F(3,40)*x,'dual lower bound identity')
 check(max(z)>=F(21,40),'global lowerbound control')
for i in range(101):
 lam=F(i,100);v=tuple((1-lam)*a+lam*b for a,b in zip(*L))
 for x,y in product((F(0),F(1),F(2,3)),repeat=2):
  check(loss(v,x,y)==(1-lam)*loss(L[0],x,y)+lam*loss(L[1],x,y),'fixed model affine segment')
for v in L:check(v[0]+v[1]==F(1,4),'audit mass fixed')
# Rectangular worst conditional loss at each branch: 9/10 and7/10.
check(max(v[1]/(v[0]+v[1]) for v in L)==F(9,10),'branch A1 worst')
check(max(v[2]/(v[2]+v[3]) for v in L)==F(7,10),'branch A0 worst')
check(F(1,4)*F(9,10)+F(3,4)*F(7,10)==F(3,4),'spliced risky bound')
check(F(11,20)+F(1,40)==F(23,40)<F(3,5),'det inquiry preferred')
check(F(21,40)+F(1,40)==F(11,20)<F(3,5),'random inquiry preferred')
check(F(3,5)+F(1,40)>F(3,5),'rectangular skip preferred')
for v in L:
 check(F(1,2)*(v[0]+v[2])+F(1,2)*(v[1]+v[3])==F(1,2),'free-menu fairguess')
check(F(1,2)<F(21,40)+F(1,40),'free-menu reversal fails')
print({'status':'PASS','explicit_checks':checks,'scope':'Exact controls plus coefficient check for written dual lower bound; no kernel verification'})
