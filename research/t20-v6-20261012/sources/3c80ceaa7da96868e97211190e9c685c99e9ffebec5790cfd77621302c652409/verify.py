"""Author controls: exact symbolic identities; universal proofs are in REPORT.md."""
from pathlib import Path
import hashlib,json
import sympy as s
ROOT=Path(__file__).resolve().parent
checks=[]
def check(name, condition):
    if not bool(condition): raise AssertionError(name)
    checks.append(name)
def eq(x,y): return s.simplify(x-y)==0
def R(p,pi,a):
    w=[r**(1-a)*x**a for x,r in zip(p,pi)]
    return [s.simplify(x/sum(w)) for x in w]
def veq(x,y): return all(eq(a,b) for a,b in zip(x,y))
rat=s.Rational
p=[rat(1,2),rat(1,4),rat(1,4)]; q=[rat(1,4),rat(1,2),rat(1,4)]
pi=[rat(1,3)]*3
rp,rq=R(p,pi,rat(1,2)),R(q,pi,rat(1,2))
rm=R([(x+y)/2 for x,y in zip(p,q)],pi,rat(1,2))
check('endpoint third coordinate',eq(rp[2],1/(2+s.sqrt(2))) and eq(rq[2],rp[2]))
check('midpoint third coordinate',eq(rm[2],1/(1+s.sqrt(6))))
check('strict midpoint exclusion exact radical comparison',s.sqrt(6)>1+s.sqrt(2))
d=s.symbols('d',real=True); g=(s.sqrt(6+5*d*d)-1)/5
check('strict curved graph Hessian formula',eq(s.diff(g,d,2),6/(6+5*d*d)**rat(3,2)))
x,y,z=s.symbols('x y z',real=True)
check('conic affine identity',s.expand(((1-z+d)/2)**2+((1-z-d)/2)**2-3*z*z)==(d*d-5*z*z-2*z+1)/2)
for k in range(21):
    t=rat(k,20); v=[t*x+(1-t)*y for x,y in zip(p,q)]; out=R(v,pi,rat(1,2))
    check(f'conic and inverse {k}',eq(out[0]**2+out[1]**2,3*out[2]**2) and veq(R(out,pi,2),v))
    check(f'quadratic membership {k}',eq(out[0]**2+out[1]**2-3*out[2]**2,0))
# Positive two-block segment with unequal reference and nontrivial profiles.
p2=[rat(1,6),rat(1,3),rat(1,2)]
q2=[rat(1,12),rat(1,6),rat(3,4)]
ref=[rat(1,2),rat(1,3),rat(1,6)]
a=rat(1,2); r1,r0=R(p2,ref,a),R(q2,ref,a)
for k in range(11):
    t=rat(k,10); out=R([t*x+(1-t)*y for x,y in zip(p2,q2)],ref,a)
    beta=s.simplify((out[2]-r0[2])/(r1[2]-r0[2]))
    check(f'two-block hull identity {k}',veq(out,[beta*x+(1-beta)*y for x,y in zip(r1,r0)]) and beta>=0 and beta<=1)
# Explicit Vandermonde witness for the obstructed three-ratio segment.
u=[s.Integer(1),-rat(1,2),s.Integer(0)]
mat=s.Matrix([[s.prod(a-j for j in range(k))*v**k for v in u] for k in range(3)])
check('Vandermonde derivative determinant',mat.det()!=0)
# Disjoint support simplex, plus inverse weight construction with unequal Z_j.
vs=[[rat(1,3),rat(2,3),0,0],[0,0,rat(1,4),rat(3,4)]]
ref4=[rat(1,10),rat(2,10),rat(3,10),rat(4,10)]
zs=[sum(ref4[i]**(1-a)*v[i]**a for i in range(4)) for v in vs]
rs=[R(v,ref4,a) for v in vs]
for k in range(11):
    beta=[rat(k,10),1-rat(k,10)]
    raw=[(b/Z)**(1/a) for b,Z in zip(beta,zs)]; lam=[s.simplify(v/sum(raw)) for v in raw]
    inp=[sum(lam[j]*vs[j][i] for j in range(2)) for i in range(4)]
    check(f'disjoint simplex inverse weights {k}',veq(R(inp,ref4,a),[sum(beta[j]*rs[j][i] for j in range(2)) for i in range(4)]))
# Gaussian full-split inherited density curvature; normalizers cancel.
w=s.symbols('w',real=True)
ls=-7*w*w/12+s.log(s.cosh(2*w/3))/2
lm=-7*w*w/12+s.log(s.cosh(w/3))
check('actual Gaussian true curvature',s.diff(ls,w,2).subs(w,0)==-rat(17,18))
check('actual Gaussian endpoint-mixture curvature',s.diff(lm,w,2).subs(w,0)==-rat(19,18))
check('Gaussian curvature gap',s.diff(ls-lm,w,2).subs(w,0)==rat(1,9))
# Pure reaction audit commutation on a specified positive finite model.
L=[s.Integer(1),s.Integer(2),s.Integer(3)]
def B(v,L):
    raw=[x*l for x,l in zip(v,L)]; return [x/sum(raw) for x in raw]
check('paired reaction audit identity',veq(R(B(p,L),pi,a),B(R(p,pi,a),[x**a for x in L])))
# Same-outcome instrument obstruction: no simultaneous proportional row scaling.
c0,c1=s.symbols('c0 c1', positive=True)
rows=[[rat(1,2),1/s.sqrt(2),s.sqrt(3)/2],[s.sqrt(3)/2,1/s.sqrt(2),rat(1,2)]]
sol=s.solve([c1*rows[0][0]+c0*rows[1][0]-1,c1*rows[0][2]+c0*rows[1][2]-1],(c0,c1))
check('instrument endpoints force equal scales',eq(sol[c0],sol[c1]))
check('instrument endpoint scales violate middle',not eq((sol[c0]+sol[c1])/s.sqrt(2),1))
check('instrument middle scale violates endpoints',not eq((1+s.sqrt(3))/(2*s.sqrt(2)),1))
check('statewise row normalization changes posterior odds',not eq(rows[0][0]/(rows[0][0]+rows[1][0])/(rows[0][1]/(rows[0][1]+rows[1][1])),rows[0][0]/rows[0][1]))
bindings=json.loads((ROOT/'INPUT_BINDINGS.json').read_text())
for item in bindings:
    check('unchanged input '+item['path'],hashlib.sha256((ROOT.parent/item['path']).read_bytes()).hexdigest()==item['sha256'])
result={'status':'PASS','assertion_groups':len(checks),'checks':checks,'scope':'Exact symbolic author controls, not independent review or universal numerical certification.'}
(ROOT/'CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','assertion_groups':len(checks)}))
