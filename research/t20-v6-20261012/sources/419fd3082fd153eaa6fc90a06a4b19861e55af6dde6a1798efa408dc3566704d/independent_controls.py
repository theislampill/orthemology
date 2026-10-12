#!/usr/bin/env python3
"""Independent exact review controls; imports no candidate code.
Finite examples supplement the written universal proofs. SymPy exact expressions
and rational arithmetic are used; numerical signs are not accepted as proof.
"""
import argparse, hashlib, itertools, json
from pathlib import Path
import sympy as s

x, y, z, t, r = s.symbols('x y z t r', real=True)
Q=s.Rational
records=[]

def check(name, condition, **details):
    assert condition, (name, details)
    records.append({'name':name,'pass':True,**details})

def zero(v): return s.simplify(v)==0

def B(F,p,vs):
    return s.expand(-sum(s.diff(F,a)*s.diff(p,a) for a in vs)-F*p)

def expectation(poly, law, vs):
    return s.expand(sum(w*s.sympify(poly).subs(dict(zip(vs,pt))) for pt,w in law))

def velocity(F,p,law,vs):
    return s.simplify(expectation(B(F,p,vs),law,vs)+expectation(F,law,vs)*expectation(p,law,vs))

def degree(p,vs): return s.Poly(p,*vs).total_degree()

def leading(p,vs):
    po=s.Poly(p,*vs); n=po.total_degree()
    return s.Add(*(c*s.prod(a**k for a,k in zip(vs,mon)) for mon,c in po.terms() if sum(mon)==n))

def parity_witness(F,phi,vs):
    nonconstant=[p for p in phi if p!=0 and degree(p,vs)>=1]
    p=max(nonconstant,key=lambda p:degree(p,vs))
    D,K=degree(F,vs),degree(p,vs); M=D+K
    H=s.expand(leading(F,vs)*leading(p,vs))
    direction=next(v for v in itertools.product(range(M+1),repeat=len(vs)) if H.subs(dict(zip(vs,v)))!=0)
    vals=[(tuple(j*a for a in direction),Q(s.binomial(M,j),2**(M-1))) for j in range(M+1)]
    mu,nu=vals[::2],vals[1::2]
    check('parity law positivity and normalization',all(w>0 for _,w in vals) and sum(w for _,w in mu)==sum(w for _,w in nu)==1,M=M,direction=list(direction))
    check('all retained observables and objective match',all(zero(expectation(a,mu,vs)-expectation(a,nu,vs)) for a in [F,*phi]),D=D,K=K)
    predicted=(-1)**(M+1)*s.factorial(M)*H.subs(dict(zip(vs,direction)))/2**(M-1)
    check('normalized velocity has predicted nonzero gap',predicted!=0 and zero(velocity(F,p,mu,vs)-velocity(F,p,nu,vs)-predicted),gap=str(predicted),polynomial=str(p))
    check('highest-degree term and degree gap',degree(B(F,p,vs),vs)==M and zero(leading(B(F,p,vs),vs)+H))
    for n in range(4):
        q=p
        for _ in range(n): q=B(F,q,vs)
        check('generator iterate degree',degree(q,vs)==K+n*D,iteration=n,degree=degree(q,vs))
    return mu,nu

# Arbitrary shifted coefficients, independent axes, sparse multivariate leading
# forms, repeated and zero descriptors, and the smallest admitted D=K=1 case.
cases=[
 (x,[x],(x,)),
 (x**2/2,[x,x**2,x**3],(x,)),
 (3*x**5-2*x+7,[s.Integer(0),s.Integer(4),x**3+2*x+1,2*x**3+4*x+2],(x,)),
 (x**4+x**2,[x**7],(x,)),
 (x*y+x,[x**2+y,y**2-2*x,x**2+y,s.Integer(1)],(x,y)),
 (x*y*(x-y)+z**2,[x*y+z,z**2+x,s.Integer(0)],(x,y,z)),
 (x,[y,y**4],(x,y)),
]
for args in cases: parity_witness(*args)

# Universal forward-difference identity checked at many degrees, with rational
# coefficients independently formed; this is a control, not universal proof.
for M in range(2,15):
    values=[sum((-1)**j*s.binomial(M,j)*j**k for j in range(M+1)) for k in range(M+1)]
    check('binomial annihilation and degree-M output',all(a==0 for a in values[:-1]) and values[-1]==(-1)**M*s.factorial(M),M=M)

# Rebuild the evaluation-duality construction by coefficient ranks and greedy
# exact evaluation bases. This does not import the author's implementation.
def polynomial_basis(polys,vs):
    polys=[s.expand(p) for p in polys]
    mons=sorted(set(mon for p in polys for mon,_ in s.Poly(p,*vs).terms()))
    C=s.Matrix([[s.Poly(p,*vs).coeff_monomial(mon) for p in polys] for mon in mons])
    return [polys[j] for j in C.rref()[1]]

def evaluation_witness(F,phi,vs):
    p=max((q for q in phi if q!=0),key=lambda q:degree(q,vs))
    basis=polynomial_basis([s.Integer(1),F,*phi],vs); g=B(F,p,vs)
    W=basis+[g]; n=len(W)
    check('target raises coefficient-space rank',len(polynomial_basis(W,vs))==n)
    points=[]; A=s.zeros(n,0)
    for pt in itertools.product(range(degree(g,vs)+1),repeat=len(vs)):
        col=s.Matrix([a.subs(dict(zip(vs,pt))) for a in W])
        trial=A.row_join(col)
        if trial.rank()>A.rank():
            A=trial; points.append(pt)
            if A.cols==n: break
    check('finite evaluation basis found',A.shape==(n,n) and A.det()!=0,n=n)
    coeff=A.inv()*s.Matrix([0]*(n-1)+[1])
    check('signed annihilator has zero mass and unit target',sum(coeff)==0 and A*coeff==s.Matrix([0]*(n-1)+[1]))
    mass=sum(c for c in coeff if c>0)
    mu=[(pt,c/mass) for pt,c in zip(points,coeff) if c>0]
    nu=[(pt,-c/mass) for pt,c in zip(points,coeff) if c<0]
    check('evaluation probabilities and support bound',mass>0 and sum(w for _,w in mu)==sum(w for _,w in nu)==1 and len(mu)+len(nu)<=len(basis)+1<=len(phi)+3,support_size=len(mu)+len(nu),dimension_S=len(basis),m=len(phi))
    check('evaluation normalized separation',all(zero(expectation(a,mu,vs)-expectation(a,nu,vs)) for a in [F,*phi]) and zero(velocity(F,p,mu,vs)-velocity(F,p,nu,vs)-1/mass),gap=str(1/mass),mu=[{'point':list(pt),'weight':str(w)} for pt,w in mu],nu=[{'point':list(pt),'weight':str(w)} for pt,w in nu])
for args in [cases[0],cases[3],cases[4]]: evaluation_witness(*args)

mu=[((0,),Q(1,16)),((2,),Q(10,16)),((4,),Q(5,16))]
nu=[((1,),Q(5,16)),((3,),Q(10,16)),((5,),Q(1,16))]
F=x*x/2
check('explicit moment list', [expectation(x**k,mu,(x,)) for k in range(6)]==[1,Q(5,2),Q(15,2),25,90,340] and [expectation(x**k,nu,(x,)) for k in range(6)]==[1,Q(5,2),Q(15,2),25,90,Q(695,2)])
vmu=[velocity(F,x**k,mu,(x,)) for k in (1,2,3)]
vnu=[velocity(F,x**k,nu,(x,)) for k in (1,2,3)]
check('explicit descriptor velocity list',vmu[:2]==vnu[:2] and vmu[2]==-Q(605,4) and vnu[2]==-155 and vmu[2]-vnu[2]==Q(15,4),mu=list(map(str,vmu)),nu=list(map(str,vnu)))

def interior(law):
    orig=dict(law)
    return [((j,),orig.get((j,),s.Integer(0))/2+Q(1,12)) for j in range(6)]
a,b=interior(mu),interior(nu)
check('mixed weights stay exact rational',all(w.is_Rational for _,w in a+b))
check('strict common support mixing',all(w>0 for _,w in a+b) and all(zero(expectation(x**k,a,(x,))-expectation(x**k,b,(x,))) for k in range(5)) and velocity(F,x**3,a,(x,))-velocity(F,x**3,b,(x,))==Q(15,8))

# The same descriptor also lies on the positive rank-two chart. Its closure
# uses the rank promise and gives a third velocity, fully compatible with no-go.
rank2=[(((5-s.sqrt(5))/2,),Q(1,2)),(((5+s.sqrt(5))/2,),Q(1,2))]
check('rank-two common descriptor',all(zero(expectation(x**k,rank2,(x,))-expectation(x**k,mu,(x,))) for k in range(4)))
check('rank-two fourth moment differs',expectation(x**4,rank2,(x,))==Q(175,2) and expectation(x**4,mu,(x,))==expectation(x**4,nu,(x,))==90,rank_two_m4='175/2',rank_three_m4='90')
check('rank-two different admissible closure velocity',velocity(F,x**3,rank2,(x,))==-Q(275,2) and velocity(F,x**3,rank2,(x,)) not in (vmu[2],vnu[2]))
check('drift-only quadratic finite degree closure',all(-s.diff(F,x)*s.diff(x**k,x)==-k*x**k for k in range(1,8)))

# Independently differentiate actual positive-weight trajectory, without the
# moment-generator identity, then compare its derivative with that identity.
def evolved_moment(law,k):
    weights=[w*s.exp(-(1-s.exp(-2*t))*pt[0]**2/4) for pt,w in law]
    return sum(w*(s.exp(-t)*pt[0])**k for (pt,_),w in zip(law,weights))/sum(weights)
for label,law in [('mu',mu),('nu',nu)]:
    for k in (0,1,2,3):
        actual=s.simplify(s.diff(evolved_moment(law,k),t).subs(t,0))
        check('actual normalized trajectory derivative',actual==velocity(F,x**k,law,(x,)),law=label,k=k,derivative=str(actual))
h=evolved_moment(mu,3)-evolved_moment(nu,3)
check('finite-time separation derivative',zero(h.subs(t,0)) and s.simplify(s.diff(h,t).subs(t,0))==Q(15,4))

# Constant boundaries: normalized generator cancels exactly at arbitrary laws.
for C in (s.Integer(0),s.Integer(-3),Q(7,2)):
    for p in (x,x**2+x,x**5):
        check('constant objective stationary',velocity(C,p,mu,(x,))==0,C=str(C),p=str(p))
for C in (s.Integer(0),s.Integer(3)):
    check('constant descriptor stationary',velocity(x**3-x,C,mu,(x,))==0)

# Positive family and finite-time-only boundary controls.
a0,v0=s.symbols('a0 v0',real=True)
den=1+(1-r*r)*v0/2
mean=r*a0/den; var=r*r*v0/den
check('Gaussian mean exact ODE',zero(-r*s.diff(mean,r)+mean+mean*var))
check('Gaussian variance exact ODE',zero(-r*s.diff(var,r)+2*var+var**2))
check('Gaussian initial values',zero(mean.subs(r,1)-a0) and zero(var.subs(r,1)-v0))
# Independent normal density completion: coefficient after tilt is 1/(2v0)+q;
# affine pushforward x -> r*x gives precisely these mean and variance.
q=(1-r*r)/4
check('Gaussian completing square',zero(r*(a0/v0)/(1/v0+2*q)-mean) and zero(r*r/(1/v0+2*q)-var))
# Unrestricted polynomial F may have finite forward escape, so only local
# counterexample existence is needed/claimed. X'=X^2 for F=-x^3/3.
u=s.symbols('u',positive=True)
X=u/(1-u*t); logweight=u*u*((1-u*t)**(-2)-1)/6
check('finite escape local characteristic',zero(s.diff(X,t)-X**2) and zero(s.diff(logweight,t)-X**3/3) and zero(X.subs(t,0)-u))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
    p=Path(args.output); p.parent.mkdir(parents=True,exist_ok=True)
    result={'status':'PASS','control_count':len(records),'arithmetic':'exact SymPy polynomial and rational/symbolic expressions','sympy_version':s.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'controls':records,'limitations':['Finite controls do not replace the universal written proof.','No historical originality, protected integration, formal-kernel proof, or audit/programme closure is certified.']}
    p.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','control_count':len(records),'output':str(p)}))
