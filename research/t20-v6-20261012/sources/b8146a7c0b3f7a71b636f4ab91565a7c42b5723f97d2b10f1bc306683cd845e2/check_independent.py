import sympy as s
import json
F=s.Rational
checks=[]
def ck(name, condition):
    if not bool(condition): raise RuntimeError(name)
    checks.append(name)
def z(e): return s.simplify(e)==0
def div(p,q,m,b): return s.simplify(sum(m[i]*b(p[i]/m[i],q[i]/m[i]) for i in range(len(m))))
def l1(v): return sum(abs(t) for t in v)
def law(v): return all(t>0 for t in v) and sum(v)==1
x,y=s.symbols('x y',positive=True)
# A different nonconvex generator/normalization witness from the author's root controls.
b3=lambda x,y:(x-y)**2*(x+2*y)/6
H=s.hessian(b3(x,y),(x,y))
ck('cubic determinant negative off diagonal',z(H.det()+(x-y)**2))
v=s.Matrix([1,2]); ck('cubic negative Hessian direction', (v.T*H.subs({x:2,y:1})*v)[0]==-2)
mu=s.Matrix([F(1,10),F(1,10),F(4,5)])
p=s.Matrix([F(9,40),F(7,40),F(3,5)])
q=s.Matrix([F(3,20),F(1,20),F(4,5)])
K=s.Matrix([[1,1,0],[0,0,1]])
ck('normalized positive cubic witness',all(law(t) for t in (mu,p,q)))
ck('cubic transport strictly increases divergence',div(K*p,K*q,K*mu,b3)-div(p,q,mu,b3)==F(1,80))
# Symbolic normalized-buffer identity, with arbitrary scalar pairs.
e,t,a,c,d,f=s.symbols('e t a c d f', real=True)
A=t*a+(1-t)*c; B=t*d+(1-t)*f
m=s.Matrix([e*t,e*(1-t),1-e]); P=s.Matrix([e*t*a,e*(1-t)*c,1-e*A]); Q=s.Matrix([e*t*d,e*(1-t)*f,1-e*B])
ck('buffer normalization exact',z(sum(m)-1) and z(sum(P)-1) and z(sum(Q)-1))
ck('buffer cancels leaving scalar Jensen defect',z(div(P,Q,m,b3)-div(K*P,K*Q,K*m,b3)-e*(t*b3(a,d)+(1-t)*b3(c,f)-b3(A,B))))
# Hessian/reciprocal tangent identity with independent symbolic jets.
a,c,d,hx,hy,hpy,delta=s.symbols('a c d hx hy hpy delta', real=True)
jet=s.Matrix([[a,-c],[-c,c-delta*d]])
ck('reciprocal tangent determinant identity',z(jet.det().subs({a:1/hx,c:1/hy,d:-hpy/hy**2})-(hy+hpy*delta-hx)/(hx*hy**2)))
# Positive power family and strict-concavity degeneracy.
b=lambda x,y:x**F(3,2)-y**F(3,2)-F(3,2)*s.sqrt(y)*(x-y)
u,v=s.symbols('u v',positive=True)
HP=s.hessian(b(x,y),(x,y)).subs({x:u*u,y:v*v})
ck('power Hessian positive off diagonal determinant',z(HP.det()-9*(u-v)**2/(32*u*v**3)))
ck('power Hessian positive leading minor',HP[0,0]==3/(4*u))
ck('diagonal equality remains despite strict reciprocal concavity',z(b(x,x)))
# Different triple obstruction: an affine relation holds after K but not before K.
mu=s.Matrix([F(1,6),F(1,3),F(1,4),F(1,4)])
p=s.Matrix([F(1,12),F(5,12),F(1,3),F(1,6)])
q=s.Matrix([F(1,12),F(5,12),F(1,6),F(1,3)])
K=s.Matrix([[1,1,0,0],[0,0,1,0],[0,0,0,1]])
ck('triple witness positive laws',all(law(t) for t in (mu,p,q)))
ck('positive-power exact equality',z(div(p,q,mu,b)-div(K*p,K*q,K*mu,b)))
ck('positive-power equality divergence positive',div(p,q,mu,b)>0)
ck('coarse affine relation obstructs even linear triple recovery',K*mu==(K*p+K*q)/2 and mu!=(p+q)/2)
R=s.diag(*q)*K.T*s.diag(*[1/t for t in K*q])
ck('q Bayes reverse is stochastic',all(t>=0 for t in R) and all(sum(R[:,j])==1 for j in range(R.cols)))
ck('q Bayes reverse recovers pair',R*K*p==p and R*K*q==q)
ck('q Bayes reverse fails reference',R*K*mu!=mu)
# Nondeterministic equality channel with overlapping support within identical pairs.
K2=s.Matrix([[1,1,F(1,3),0],[0,0,F(2,3),0],[0,0,0,1]])
# Above mixes diagonal with off-diagonal and MUST strictly contract.
ck('mixed diagonal and off-diagonal fiber must lose divergence',div(p,q,mu,b)>div(K2*p,K2*q,K2*mu,b))
# Endpoint quadratic equality does not imply pair recoverability.
mu=s.Matrix([F(1,3)]*3);p=s.Matrix([F(1,4),F(5,12),F(1,3)]);q=s.Matrix([F(1,6),F(1,3),F(1,2)])
K=s.Matrix([[1,1,0],[0,0,1]]);b2=lambda x,y:(x-y)**2/2
ck('quadratic counterexample laws positive normalized',all(law(t) for t in (mu,p,q)))
ck('quadratic positive equality value',div(p,q,mu,b2)==div(K*p,K*q,K*mu,b2)==F(1,16))
ck('quadratic pair reverse impossible signed norm obstruction',l1(p-F(4,3)*q)==F(7,18) and l1(K*p-F(4,3)*K*q)==F(1,3))
ck('strict reciprocal contrast does not have same equality',div(p,q,mu,b)>div(K*p,K*q,K*mu,b))
print(json.dumps({'status':'PASS','checks':checks,'count':len(checks),'scope':'Exact independent fixtures and symbolic identities. Global equivalences require the written proof, not finite testing.'},indent=2))
