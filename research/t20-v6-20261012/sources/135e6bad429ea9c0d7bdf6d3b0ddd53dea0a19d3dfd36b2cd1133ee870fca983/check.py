from fractions import Fraction as Q
checks=0
def require(p):
 global checks
 checks+=1
 if not p: raise RuntimeError('binary weight control failed')
for b in range(1,25):
 for a in range(b):
  total=Q(0)
  for n in range(21):
   A=(2**n*a)//b; B=(2**(n+1)*a)//b
   d=B-2*A
   require(d in (0,1)); require(d==B%2)
   require(total==Q(A,2**n))
   require(Q(0)<=Q(a,b)-total<Q(1,2**n))
   total+=Q(d,2**(n+1))
print({'status':'PASS','explicit_checks':checks,'scope':'finite controls for separately proved telescoping identity'})
