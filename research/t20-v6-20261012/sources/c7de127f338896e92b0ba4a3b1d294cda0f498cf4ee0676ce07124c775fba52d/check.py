import sympy as s
from fractions import Fraction as F
n=0
def ck(v):
 global n
 if not v:raise AssertionError(n)
 n+=1
a,t,d=s.symbols('a t d',real=True)
v=s.Matrix([s.Rational(1,3)*(1+t*u)**a for u in [-s.Rational(1,2),0,s.Rational(1,2)]])
J=s.Matrix.hstack(v.subs(t,0),s.diff(v,t).subs(t,0),s.diff(v,t,2).subs(t,0))
ck(s.simplify(J.det()-a*a*(a-1)/108)==0)
f=(-1+s.sqrt(6+5*d*d))/5
ck(s.simplify(s.diff(f,d,2)-6/(6+5*d*d)**s.Rational(3,2))==0)
endpoint=1/(2+s.sqrt(2));midpoint=1/(1+s.sqrt(6))
ck(bool(endpoint>midpoint))
# Root supplied finite-reaction endpoint counterexample, evaluate exact radical identity.
p=s.Matrix([s.Rational(1,2),s.Rational(1,4),s.Rational(1,4)])
q=s.Matrix([s.Rational(1,4),s.Rational(1,2),s.Rational(1,4)])
def R(v):
 w=v.applyfunc(s.sqrt)
 return w/sum(w)
ck(s.simplify(R(p)[2]-endpoint)==0)
ck(s.simplify(R(q)[2]-endpoint)==0)
ck(s.simplify(R((p+q)/2)[2]-midpoint)==0)
# Disjoint profile simplex: transformed weights reach requested mixtures.
# Choose a=1/2, uniform reference on four coordinates.
v1=s.Matrix([s.Rational(1,4),s.Rational(3,4),0,0]);v2=s.Matrix([0,0,s.Rational(1,2),s.Rational(1,2)])
z1=sum(v1.applyfunc(s.sqrt));z2=sum(v2.applyfunc(s.sqrt))
for b in [s.Rational(1,4),s.Rational(1,2),s.Rational(3,4)]:
 l=(b/z1)**2/((b/z1)**2+((1-b)/z2)**2)
 err=R(l*v1+(1-l)*v2)-(b*R(v1)+(1-b)*R(v2))
 ck(all(s.simplify(x)==0 for x in err))
print({'status':'PASS','checks':n,'derivative_rank_determinant':str(s.factor(J.det())),'boundary_second_derivative':str(s.simplify(s.diff(f,d,2))),'scope':'finite reaction, not general full OU split'})
# Same-outcome stochastic instrument incompatibility.
c0,c1=s.symbols('c0 c1',real=True)
eq=[c1*s.sqrt(x)+c0*s.sqrt(1-x)-1 for x in [s.Rational(1,4),s.Rational(1,2),s.Rational(3,4)]]
ck(s.solve(eq,[c0,c1])==[])
ck(s.simplify(eq[0].subs({c0:1/s.sqrt(2),c1:1/s.sqrt(2)})-((1+s.sqrt(3))/(2*s.sqrt(2))-1))==0)
# Normalising each column changes the common multiplier across states.
Z=[s.sqrt(x)+s.sqrt(1-x) for x in [s.Rational(1,4),s.Rational(1,2),s.Rational(3,4)]]
ck(s.simplify(Z[0]-Z[1])!=0)
print({'instrument_controls':'PASS','total_checks':n})
q=(F(1,2),F(1,4),F(1,4));tot=sum(x*x for x in q);p=tuple(x*x/tot for x in q)
L=(F(1,4),F(1,2),F(3,4));g=sum(x*y for x,y in zip(p,L));p1=tuple(x*y/g for x,y in zip(p,L));g2=sum(x*y for x,y in zip(p1,L))
ck(p==(F(2,3),F(1,6),F(1,6)) and g==F(3,8))
ck(p1==(F(4,9),F(2,9),F(1,3)) and g2==F(17,36) and g*g2==F(17,96))
z=sum(x*y for x,y in zip(q,L));q2=tuple(x*y/z for x,y in zip(q,L));norm2=sum(x*x for x in q2);p2=tuple(x*x/norm2 for x in q2)
ck(q2==(F(2,7),F(2,7),F(3,7)) and p2==(F(4,17),F(4,17),F(9,17)))
print({'coordinate_repair':'PASS','total_checks':n})
