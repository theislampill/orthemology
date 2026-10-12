from fractions import Fraction as Q
count=0
def check(c):
 global count
 count+=1
 if not c: raise RuntimeError('rational-cut root guard failed')
for n in range(0,31):
 special=Q(1,2)+Q(1,2**(n+1))
 other=Q(1,2**(n+1))
 check(special+(2**n-1)*other==1)
 check(special>Q(1,2))
 if n:
  check(other<Q(1,2))
 check(special-Q(1,2)==Q(1,2**(n+1)))
print({'status':'PASS','explicit_checks':count,'scope':'finite numerical controls for separately proved all-depth mixed-law boundary'})
