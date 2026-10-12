from fractions import Fraction as F
from itertools import product
checks=0
def check(p,msg):
 global checks
 if not p:raise RuntimeError(msg)
 checks+=1
V=[tuple(F(n,10) for n in ns) for ns in ((4,2,1,3),(3,1,2,4))]
def risk(v,x,y):
 # x,y probabilities of reporting1 after A1,A0. Both labels freely permitted.
 a,b,c,d=v
 return (1-x)*a+x*b+(1-y)*c+y*d
for v in V:
 check(v[0]+v[2]==F(1,2),'known balanced prior')
 check(risk(v,1,0)==F(3,10),'common Bayes risk')
 check(v[0]>v[1] and v[3]>v[2],'strict common optimal labels')
for k in range(101):
 t=F(k,100);v=tuple((1-t)*a+t*b for a,b in zip(*V))
 check(v[0]+v[2]==F(1,2),'whole segment prior')
 check(risk(v,1,0)==F(3,10),'whole segment exactrisk')
 for x,y in product((F(0),F(1,3),F(1,2),F(1)),repeat=2):
  # Universal lowerbound certified by nonnegative affine excess coefficients.
  check(risk(v,x,y)-F(3,10)==(1-x)*(v[0]-v[1])+y*(v[3]-v[2]),'excessrisk identity')
  check(risk(v,x,y)>=F(3,10),'randomized control')
check(max(v[1]/(v[0]+v[1]) for v in V)==F(1,3),'A1 worst error')
check(max(v[2]/(v[2]+v[3]) for v in V)==F(1,3),'A0 worst error')
spliced=(F(1,3),F(1,6),F(1,6),F(1,3))
check(spliced[0]+spliced[2]==F(1,2),'spliced preserves targetprior')
check(spliced[0]+spliced[1]==F(1,2),'spliced auditmass inoriginalrange')
check(risk(spliced,1,0)==F(1,3)!=F(3,10),'spliced notoriginalsegment')
check(F(3,10)+F(9,50)==F(12,25)<F(1,2),'fixedmodel query preferred')
check(F(1,3)+F(9,50)==F(77,150)>F(1,2),'rectangular skip preferred')
for x in (F(0),F(1,3),F(1,2),F(1)):
 check(F(1,2)*(1-x)+F(1,2)*x==F(1,2),'all skip predictions riskhalf')
rect_priors=[m*q1+(1-m)*q0 for m,q1,q0 in product((F(2,5),F(3,5)),(F(2,3),F(3,4)),(F(1,4),F(1,3)))]
check(min(rect_priors)==F(5,12) and max(rect_priors)==F(7,12),'full rectangular prior range')
check(all((1-p)*F(1,2)+p*F(1,2)==F(1,2) for p in rect_priors),'full rectangular private skip')
print({'status':'PASS','explicit_checks':checks,'scope':'Exact unrestricted-menu controls, universal affine-excess proof written in report'})
