import sympy as s, json
from fractions import Fraction as F
n,t=s.symbols('n t',nonnegative=True)
u=s.symbols('u',nonnegative=True)
c=(1-s.exp(-2*t))/4
a=(s.exp(2*t)-1)/4
checks=[]
def check(name,statement):
    if not statement: raise RuntimeError(name)
    checks.append(name)
check('integrated_potential',s.simplify(s.integrate(n**2*s.exp(-2*u)/2,(u,0,t))-c*n**2)==0)
check('quadratic_tail_cancellation',s.simplify(a*s.exp(-2*t)-c)==0)
check('checkpoint_c',s.simplify(c.subs(t,s.log(2))-s.Rational(3,16))==0)
check('checkpoint_a',s.simplify(a.subs(t,s.log(2))-s.Rational(3,4))==0)
for N in (2,5,15):
    weights=[F(1,(i+1)**2) for i in range(N)];total=sum(weights);mu=[x/total for x in weights]
    L=[F((i+1)**2,4**i) for i in range(N)];Z=sum(p*l for p,l in zip(mu,L));post=[p*l/Z for p,l in zip(mu,L)]
    geom=[F(1,4**i) for i in range(N)];gZ=sum(geom)
    check('finite_geometric_'+str(N),post==[p/gZ for p in geom])
    withdraw=[p/l for p,l in zip(post,L)];wZ=sum(withdraw)
    check('finite_withdrawal_'+str(N),[p/wZ for p in withdraw]==mu)
print(json.dumps({'status':'PASS','count':len(checks),'checks':checks,'scope':'Symbolic coefficient checks and finite cancellation controls; infinite tail and positive-time proof remain written mathematics.'},indent=2))
