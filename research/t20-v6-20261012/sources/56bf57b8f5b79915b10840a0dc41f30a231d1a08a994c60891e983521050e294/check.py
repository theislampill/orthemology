#!/usr/bin/env python3
"""Exact supporting controls, not an exhaustive proof of the written theorems."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json
import sympy as s
ROOT=Path(__file__).resolve().parent
checks=[]
def ok(name,condition):
    assert condition,name
    checks.append(name)
def zero(name,e):ok(name,s.expand(e)==0 or s.simplify(e)==0)
N=3
# Free associative word algebra, exact fractions; grade records powers of t.
def add(a,b):
    c=dict(a)
    for w,v in b.items():c[w]=c.get(w,Q(0))+v
    return {w:v for w,v in c.items() if v}
def scale(a,c):return {w:v*c for w,v in a.items() if v*c}
def mul(a,b):
    c={}
    for w,v in a.items():
      for z,k in b.items():
        if len(w+z)<=N:c[w+z]=c.get(w+z,Q(0))+v*k
    return {w:v for w,v in c.items() if v}
def bracket(a,b):return add(mul(a,b),scale(mul(b,a),-1))
def exp_letter(i,c):return {(i,)*n:c**n/Q(s.factorial(n)) for n in range(N+1)}
A={(0,):Q(1)}; B={(1,):Q(1)}
P=mul(mul(exp_letter(0,Q(1,2)),exp_letter(1,Q(1))),exp_letter(0,Q(1,2)))
R=mul(mul(exp_letter(1,Q(1,2)),exp_letter(0,Q(1))),exp_letter(1,Q(1,2)))
diff=add(P,scale(R,-1))
ok('free signatures coincide through degree two',all(len(w)==3 for w in diff))
ok('free degree-three Strang discrepancy',diff==scale(bracket(add(A,B),bracket(A,B)),Q(-1,8)))
expected={():Q(1),(0,):Q(1),(1,):Q(1)}
for w in [(0,0),(0,1),(1,0),(1,1)]:expected[w]=Q(1,2)
ok('common lower signature exactly exponential through degree two',{w:v for w,v in P.items() if len(w)<=2}==expected)
# A concrete Chen concatenation control: splitting one F segment preserves all retained grades.
ok('same-letter duration splitting',mul(exp_letter(0,Q(2,3)),exp_letter(0,Q(4,3)))==exp_letter(0,Q(2)))
# Arbitrary polynomial gradient commutator and local nonconstant bracket.
x,y,a,t,q=s.symbols('x y a t q',real=True)
f=s.Function('f')(x,y);g=s.Function('g')(x,y);p=s.Function('p')(x,y)
def gradop(F,p):return -s.diff(F,x)*s.diff(p,x)-s.diff(F,y)*s.diff(p,y)-F*p
transport=sum(sum(s.diff(g,v,w)*s.diff(f,w)-s.diff(f,v,w)*s.diff(g,w) for w in [x,y])*s.diff(p,v) for v in [x,y])
zero('general two-dimensional gradient commutator',gradop(f,gradop(g,p))-gradop(g,gradop(f,p))-transport)
p=s.Function('p')(x)
BF=lambda p:-x*s.diff(p,x)-x*x*p/2
BG=lambda p:-(x-a)*s.diff(p,x)-(x-a)**2*p/2
C=lambda p:BF(BG(p))-BG(BF(p))
zero('translated quadratic first bracket',C(p)-a*s.diff(p,x))
z=s.symbols('z')
zero('exact weight-coordinate intertwiner',-x*s.diff(z*p,x)-x*x*z*s.diff(z*p,z)/2-z*BF(p))
ok('weight-coordinate map is not polynomial algebra map',s.expand((z*x)*(z*x)-z*x*x)!=0)
D=lambda p:-(BF(C(p))+BG(C(p))-C(BF(p)+BG(p)))/8
zero('nested Strang operator',D(p)+a*s.diff(p,x)/4+a*x*p/4-a*a*p/8)
zero('nonconstant mass coefficient',D(s.Integer(1))-(a*a/8-a*x/4))
# Represent each word as actual differential composition and normalize symbolically.
ops=[BF,BG]
def rho(w,p):
    for i in reversed(w):p=s.expand(ops[i](p))
    return p
mom=s.symbols('m0:10')
def mu(p):
    poly=s.Poly(s.expand(p),x)
    return s.expand(sum(coeff*(1 if k[0]==0 else mom[k[0]]) for k,coeff in poly.terms()))
def jet(S,p):
    out=[s.Integer(0)]*(N+1)
    for w,c in S.items():out[len(w)]+=s.Rational(c.numerator,c.denominator)*mu(rho(w,p))
    return [s.expand(z) for z in out]
def quotient(num,den):
    out=[]
    assert den[0]==1
    for n in range(N+1):out.append(s.expand(num[n]-sum(den[k]*out[n-k] for k in range(1,n+1))))
    return out
jP=quotient(jet(P,x),jet(P,s.Integer(1)))
jR=quotient(jet(R,x),jet(R,s.Integer(1)))
for n in range(3):zero(f'normalized mean agrees at degree {n}',jP[n]-jR[n])
zero('normalized mean degree three contains variance',jP[3]-jR[3]+a*(1+mom[2]-mom[1]**2)/4)
zero('Dirac third-order discriminator',(jP[3]-jR[3]).subs({mom[k]:x**k for k in range(1,10)})+a/4)
zero('two-point third-order discriminator',(jP[3]-jR[3]).subs({mom[k]:s.Integer(0 if k%2 else 1) for k in range(1,10)})+a/2)
# Exact positive quadratic flow and weight composition.
def stage(state,c,r):
    pos,logw=state
    return s.expand(c+r*(pos-c)),s.expand(logw-(pos-c)**2*(1-r*r)/4)
PA=(x,s.Integer(0)); QB=PA
for c,r in [(0,q),(a,q*q),(0,q)]:PA=stage(PA,c,r)
for c,r in [(a,q),(0,q*q),(a,q)]:QB=stage(QB,c,r)
E=a*(q-1)**3*(q+1)
W=a*(2*x-a)*(q-1)**3*(q+1)*(q**4+1)/4
zero('exact Strang endpoint difference',PA[0]-QB[0]-E)
zero('exact Strang logweight difference',PA[1]-QB[1]-W)
zero('exact two-point logodds difference',W.subs(x,1)-W.subs(x,-1)-a*(q-1)**3*(q+1)*(q**4+1))
zero('endpoint t-cubed coefficient',s.diff(E.subs(q,s.exp(-t/2)),t,3).subs(t,0)/6+a/4)
zero('logweight t-cubed coefficient',s.diff(W.subs(q,s.exp(-t/2)),t,3).subs(t,0)/6-(a*a/8-a*x/4))
# Scalar-jet normalization and induction first-difference formula in abstract symbols.
e=s.symbols('e');c1,c2,c3,n0,n1,n2,n3,d1,d2,d3,z,h=s.symbols('c1 c2 c3 n0 n1 n2 n3 d1 d2 d3 z h')
cc=1+c1*e+c2*e**2+c3*e**3
num=n0+n1*e+n2*e**2+n3*e**3;den=1+d1*e+d2*e**2+d3*e**3
zero('common scalar jet cancels',cc*num/(cc*den)-num/den)
zero('first differing coefficient normalizes by covariance',s.limit(((num+e**3*z)/(den+e**3*h)-num/den)/e**3,e,0)-(z-h*n0))
u,v,ax,ay,px,py=s.symbols('u v ax ay px py')
zero('two-point scalar-kernel identity',(ax*px+ay*py)/2-(ax+ay)*(px+py)/4-(ax-ay)*(px-py)/4)
ok('nonconstant multiplication invisible on Dirac but not mixture',s.Rational(1,2)*(0*0+1*1)-s.Rational(1,2)**2==s.Rational(1,4))
# General 3x3 operator/cylindrical Lie relation (independent finite control only).
bb=s.Matrix(3,3,s.symbols('b0:9'));dd=s.Matrix(3,3,s.symbols('d0:9'));L=s.Matrix([[1,u,v]])
one=s.Matrix([1,0,0])
def vec(M):
 r=L*M-(L*M*one)[0]*L
 return s.Matrix([r[1],r[2]])
vb,vd=vec(bb),vec(dd)
comm=vd.jacobian([u,v])*vb-vb.jacobian([u,v])*vd-vec(bb*dd-dd*bb)
zero('general finite-matrix normalized Lie coordinate one',comm[0])
zero('general finite-matrix normalized Lie coordinate two',comm[1])
ok('scalar generator kernel finite control',vec(s.eye(3))==s.zeros(2,1))
# Associative quotient cannot kill I and preserve a nonzero B; explicit multiplication failure.
M=s.Matrix([[0,1],[0,0]]);Id=s.eye(2)
ok('scalar span is not associative ideal',M*Id==M and M[0,1]!=0)
# Source identity/preservation controls.
bind=json.loads((ROOT/'INPUT_BINDINGS.json').read_text())
for item in bind['local_inputs']:
    path=ROOT.parent/item['path']; b=path.read_bytes()
    ok('input binding: '+item['path'],hashlib.sha256(b).hexdigest()==item['sha256'])
    if item.get('git_blob'):
        blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        ok('pinned git blob: '+item['path'],blob==item['git_blob'])
for item in bind['external_sources']:
    ok('retained source binding: '+item['path'],hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'])
out={'status':'PASS','count':len(checks),'checks':checks,'scope':'Exact finite symbolic controls supporting ordinary general proofs; no kernel proof, numerical sampling, empirical model, or independent review.'}
(ROOT/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
