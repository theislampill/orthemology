import sympy as s,json
x,y=s.symbols('x y',positive=True);u,v=s.symbols('u v',positive=True)
checks=[]
def ck(name,c):
 if not bool(c):raise RuntimeError(name)
 checks.append(name)
phi=lambda t:t**s.Rational(3,2)
b=lambda a,c:phi(a)-phi(c)-s.Rational(3,2)*s.sqrt(c)*(a-c)
H=s.hessian(b(x,y),(x,y));Huv=H.subs({x:u*u,y:v*v})
ck('power3/2 determinant factor',s.simplify(Huv.det()-9*(u-v)**2/(32*u*v**3))==0)
fine=s.Rational(1,16)*(b(4,1)+b(1,1));coarse=s.Rational(1,8)*b(s.Rational(5,2),1)
gap=(18-5*s.sqrt(10))/32
ck('positive power transport gap',s.simplify(fine-coarse-gap)==0)
ck('gap positivity by exact squaring',18**2>25*10)
# Tangent-line characterisation determinant identity in symbolic jet data.
a,c,d=s.symbols('a c d',positive=True);t=s.symbols('t',real=True)
jet=s.Matrix([[a,-c],[-c,c-t*d]])
ck('Hessian determinant criterion',s.expand(jet.det()-(a*c-a*t*d-c*c))==0)
# Entropy and quadratic equality null directions.
be=x*s.log(x/y)-x+y;He=s.hessian(be,(x,y))
ck('entropy null ratio direction',He*s.Matrix([x,y])==s.zeros(2,1))
Hq=s.hessian((x-y)**2/2,(x,y))
ck('quadratic null difference direction',Hq*s.Matrix([1,1])==s.zeros(2,1))
# Paired diagonal segment is a genuine equality set for every generator.
ck('power diagonal value',s.simplify(b(x,x))==0)
ck('power diagonal null tangent',s.simplify(H.subs(y,x)*s.Matrix([1,1]))==s.zeros(2,1))
p=s.Matrix([s.Rational(1,8),s.Rational(1,8),s.Rational(1,4),s.Rational(1,2)])
q=s.Matrix([s.Rational(1,8),s.Rational(1,8),s.Rational(1,2),s.Rational(1,4)])
mu=s.Matrix([s.Rational(1,8),s.Rational(3,8),s.Rational(1,4),s.Rational(1,4)])
K=s.Matrix([[1,1,0,0],[0,0,1,0],[0,0,0,1]])
F=p.row_join(q).row_join(mu);C=K*F;R=F*C.inv()
ck('coarse three-object matrix determinant',C.det()==-s.Rational(1,16))
ck('unique linear recovery has negative entry',R[1,1]==-s.Rational(1,8))
ck('linear recovery equations',R*C==F)
div=lambda p,q,m:sum(m[i]*b(p[i]/m[i],q[i]/m[i]) for i in range(len(p)))
ck('positive-divergence equality witness',s.simplify(div(p,q,mu)-div(K*p,K*q,K*mu))==0)
ck('equality witness is not identical laws',p!=q)
print(json.dumps({'count':len(checks),'checks':checks,'scope':'Exact symbolic/rational controls. The global theorem requires the written Jensen/buffer proof; no finite test certifies it.'},indent=2))
