from fractions import Fraction as F
import sympy as s
p=s.symbols('p',positive=True)
lr=(8*p-s.Rational(3,2))*(1-p)/(p*(s.Rational(13,2)-8*p))
der=s.factor(s.diff(lr,p))
checks=0
def check(c):
 global checks
 if not c: raise AssertionError(checks)
 checks+=1
check(s.simplify(lr.subs(p,s.Rational(1,4))-s.Rational(1,3))==0)
check(s.simplify(lr.subs(p,s.Rational(3,4))-3)==0)
num,den=s.fraction(der)
print('LR derivative:',der)
# derivative numerator positive for all real p: quadratic has negative discriminant, positive leading coefficient
poly=s.Poly(num,p)
check(poly.degree()==2 and poly.LC()>0 and s.discriminant(poly.as_expr(),p)<0)
for i in range(101):
 x=F(1,4)+F(i,200)
 for typ in ['K','L']:
  z=F(1,8) if typ=='K' else F(2,5)*x-F(3,40)
  law=(z,F(1,4)-z,x-z,F(3,4)-x+z)
  check(min(law)>0 and sum(law)==1)
  check(law[0]+law[2]==x)
  check(law[0]+law[1]==F(1,4))
  r=z*(1-x)/(x*(F(1,4)-z))
  check(F(1,3)<=r<=3)
  check(z/F(1,4)==(F(1,2) if typ=='K' else F(8,5)*x-F(3,10)))
# Null-boundary compact convex variant: 0<=v<=1/2, v^2<=u<=v/2.
# Joint law (theta1 audit1,theta0 audit1,theta1 audit0,theta0 audit0)
for i in range(1,101):
 v=F(i,200)
 for j in range(11):
  u=v*v+F(j,10)*(v/F(2)-v*v)
  law=(u,v-u,(1-v)/2,(1-v)/2)
  check(min(law)>0 and sum(law)==1)
  check(0<u/v<=F(1,2))
print({'checks':checks,'status':'PASS','universal_claim':'ordinary algebra/convex proof; grid is finite control'})
