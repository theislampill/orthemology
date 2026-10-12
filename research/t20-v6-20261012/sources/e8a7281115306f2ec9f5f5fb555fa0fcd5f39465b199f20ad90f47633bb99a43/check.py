import sympy as s,json,hashlib,pathlib
x,y,a,z,t=s.symbols('x y a z t', real=True)
p=s.Function('p')(x,y); F=s.Function('F')(x,y); G=s.Function('G')(x,y)
vars=(x,y)
def B(f,p):return -sum(s.diff(f,v)*s.diff(p,v) for v in vars)-f*p
def zero(v):assert s.simplify(s.expand(v))==0
checks=[]
def check(name,v):zero(v);checks.append(name)
bracket=sum((sum(s.diff(G,v,w)*s.diff(F,w)-s.diff(F,v,w)*s.diff(G,w) for w in vars))*s.diff(p,v) for v in vars)
check('arbitrary smooth two-dimensional operator commutator',B(F,B(G,p))-B(G,B(F,p))-bracket)
check('commutator annihilates constant',B(F,B(G,s.Integer(1)))-B(G,B(F,s.Integer(1))))
q=s.exp(-t)
ff=lambda v:q*v
gg=lambda v:q*v+a*(1-q)
check('exact quadratic endpoints',gg(ff(z))-ff(gg(z))-a*(1-q)**2)
check('quadratic second order coefficient',s.limit((gg(ff(z))-ff(gg(z)))/t**2,t,0)-a)
p1=s.Function('u')(x)
BF=lambda v:-x*s.diff(v,x)-x*x*v/2
C=lambda v:a*s.diff(v,x)
check('nested bracket has scalar killing component',BF(C(p1))-C(BF(p1))-a*s.diff(p1,x)-a*x*p1)
# A generic drift/killing mismatch has a nonzero scalar term: B=∂x, D=−x multiplication.
check('generic drift scalar commutator control',s.diff(-x*p1,x)+x*s.diff(p1,x)+p1)
# Formal normalization division through order two with matching denominators.
n0,n1,n2,k,d1,d2=s.symbols('n0 n1 n2 k d1 d2')
expr=(n0+t*n1+t*t*(n2+k))/(1+t*d1+t*t*d2)-(n0+t*n1+t*t*n2)/(1+t*d1+t*t*d2)
check('matching mass normalization preserves coefficient',s.limit(expr/t**2,t,0)-k)
root=pathlib.Path(__file__).parent
out={'status':'PASS','checks':checks,'count':len(checks),'verification':'SymPy exact identities; no Lean or empirical validation'}
(root/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
