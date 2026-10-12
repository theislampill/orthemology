from fractions import Fraction as F
from itertools import product
N=0
def check(x,msg):
 global N
 if not x: raise RuntimeError(msg)
 N+=1
def moment(r,k):return sum(w*p**k for p,w in r)
def law(r):return tuple(sum(w*p**sum(bits)*(1-p)**(2-sum(bits)) for p,w in r) for bits in product((0,1),repeat=2))
for i in range(21):
 mu=F(i,20)
 for j in range(21):
  nu=mu*mu+F(j,20)*(mu-mu*mu)
  r=((F(0),F(1)),) if mu==0 else ((nu/mu,mu*mu/nu),(F(0),1-mu*mu/nu))
  check(all(0<=p<=1 and 0<=w<=1 for p,w in r) and sum(w for p,w in r)==1,'valid twoatom realization')
  check((moment(r,1),moment(r,2))==(mu,nu),'exact moments')
  check(law(r)==(1-2*mu+nu,mu-nu,mu-nu,nu),'exact two-trial law')
A=((F(1,3),F(3,4)),(F(1),F(1,4)))
B=((F(0),F(1,4)),(F(2,3),F(3,4)))
check(law(A)==law(B)==(F(1,3),F(1,6),F(1,6),F(1,3)),'same full two-trial law')
check((moment(A,3),moment(B,3))==(F(5,18),F(2,9)),'distinct third moments')
check(moment(A,3)/moment(A,2)==F(5,6),'A third prediction')
check(moment(B,3)/moment(B,2)==F(2,3),'B third prediction')
exchangeable=(F(0),F(1,2),F(1,2),F(0))
check(exchangeable[1]==exchangeable[2] and sum(exchangeable)==1,'finite exchangeable control')
check(exchangeable[3]<(exchangeable[2]+exchangeable[3])**2,'finite exchangeability outside mixture body')
print({'status':'PASS','explicit_checks':N,'scope':'Exact finite controls; universal sufficiency and continuation-limit argument written separately'})
