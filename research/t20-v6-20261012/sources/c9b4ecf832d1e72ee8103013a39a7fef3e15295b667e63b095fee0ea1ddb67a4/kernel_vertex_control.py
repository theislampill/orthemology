from fractions import Fraction as F
checks=0
def check(x,msg):
 global checks
 if not x:raise RuntimeError(msg)
 checks+=1
def path(p):return ((1-p)**2,(1-p)*p,p*(1-p),p*p)
check(sum(path(F(1,2))[1:3])==F(1,2),'interior alternating event')
check(all(sum(path(p)[1:3])==0 for p in (F(0),F(1))),'endpoint alternating event')
for i in range(21):
 p0=F(i,20)
 for j in range(21):
  p=F(j,20);v=path(p)
  EX1=v[2]+v[3]; EX1X2=v[3]
  value=2*p0*EX1-EX1X2
  check(value==p0*p0-(p-p0)**2,'exposing functional identity')
  check((value==p0*p0)==(p==p0),'unique maximizer on controls')
print({'status':'PASS','explicit_checks':checks,'scope':'Exact rational controls; universal argument written separately'})
