#!/usr/bin/env python3
"""Independent exact controls. Imports no author module; never edits author bytes."""
import hashlib, json, pathlib, platform
import sympy as S
R=S.Rational
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent
checks=[]
def reduce(x):
    expanded=S.expand_log(S.sympify(x),force=True)
    def rational_log(z):
        arg=z.args[0]
        num,den=arg.as_numer_denom()
        return sum(k*S.log(prime) for prime,k in S.factorint(num).items())-sum(k*S.log(prime) for prime,k in S.factorint(den).items())
    expanded=expanded.replace(lambda z:z.func==S.log and z.args[0].is_Rational and z.args[0]>0,rational_log)
    # Preserve additive prime-log normal form instead of building enormous powers.
    return S.cancel(S.expand(expanded))
def eq(x,y):
    if isinstance(x,(list,tuple)):
        assert len(x)==len(y)
        for a,b in zip(x,y): eq(a,b)
    else: assert reduce(x-y)==0, (x,y,reduce(x-y))
def dot(x,y): return sum(a*b for a,b in zip(x,y))
def KL(q,p): return reduce(sum(a*S.log(a/b) for a,b in zip(q,p) if a))
def norm(q): return tuple(S.cancel(a/sum(q)) for a in q)
def update(p,L): return norm(tuple(a*b for a,b in zip(p,L)))
def add(name,**detail):
    checks.append({'name':name,'status':'PASS',**detail})
    print('PASS',len(checks),name)

# Fresh curved-family certificate, deliberately asymmetric (no swapping argument).
c=(R(1,3),)*3
rA=(R(1,2),R(1,3),R(1,6))
pA=(R(192,209),R(16,209),R(1,209))
v=tuple(a-b for a,b in zip(rA,c))
eq(dot(v,v),R(1,18))
eq(KL(rA,pA),S.log(R(209,96)))
grad=tuple(1+S.log(a/b) for a,b in zip(rA,pA))
lam=18*S.log(2)
eq(tuple(g+lam*n for g,n in zip(grad,v)),(1+S.log(R(209,48)),)*3)
# For t in the disk, v.(t-rA)<=0 by Cauchy-Schwarz; hence grad.(t-rA)>=0.
# Strict convexity of KL supplies uniqueness, including any nonsymmetric t.
assert dot(tuple(a-b for a,b in zip(pA,c)),tuple(a-b for a,b in zip(pA,c)))>R(1,18)
add('asymmetric curved conditional: exact outward-normal optimality certificate',
    minimizer=list(map(str,rA)),cost=str(S.log(R(209,96))))

# A different active block forces an internal coordinate to zero and an inequality.
pB=(R(3,64),R(1,4),R(45,64)); rB=(R(3,4),R(1,4),S.Integer(0))
t=S.symbols('t',positive=True)
f=t*S.log(t/pB[0])+(1-t)*S.log((1-t)/pB[1])
eq(S.diff(f,t),S.log(16*t/(3*(1-t))))
eq((16*t/(3*(1-t))).subs(t,R(3,4)),16)
eq(S.diff(f,t,2),1/(t*(1-t)))
eq(KL(rB,pB),S.log(8))
# Thus on 3/4<=t<=1 the strictly increasing objective is minimized at 3/4.
add('forced-zero coordinate inside an active nonsingleton conditional block',cost='log(8)')

# Three normalized outcomes, two selected blocks, one wholly omitted block.
weights=(R(1,2),R(1,3),R(1,6))
p=tuple(weights[0]*a for a in pA)+tuple(weights[1]*a for a in pB)+(weights[2],)
columns=((R(1,2),R(1,3),R(1,6)),(R(1,4),R(1,4),R(1,2)),(R(1,3),R(1,2),R(1,6)))
rows=tuple((columns[0][j],)*3+(columns[1][j],)*3+(columns[2][j],) for j in range(3))
assert all(a>0 for row in rows for a in row)
eq(tuple(sum(row[i] for row in rows) for i in range(7)),(1,)*7)
penalties=(R(96,209),R(1,8))
def repair(v):
    aa=sum(v[:3])*penalties[0]; bb=sum(v[3:6])*penalties[1]
    z=aa+bb
    return tuple(aa*a/z for a in rA)+tuple(bb*b/z for b in rB)+(S.Integer(0),),z
q,z=repair(p)
eq(z,R(1361,5016))
eq(q,(R(576,1361),R(384,1361),R(192,1361),R(627,5444),R(209,5444),0,0))
eq(KL(q,p),-S.log(z))
a=tuple(dot(p,L) for L in rows); b=tuple(dot(q,L) for L in rows)
eq(a,(R(7,18),R(1,3),R(5,18)))
for L,aa,bb in zip(rows,a,b):
    pp=update(p,L); qq,zp=repair(pp)
    eq(qq,update(q,L)); eq(zp,z*bb/aa)
    eq(KL(qq,pp),-S.log(zp))
assert q[5]==q[6]==0 and sum(q[:3])>0 and sum(q[3:6])>0
add('three-outcome commutation with asymmetric disk, positive conditional costs, internal zero, and omitted block',
    Z=str(z),projected_prior=list(map(str,q)),original_outcomes=list(map(str,a)),repaired_outcomes=list(map(str,b)))

# Independently check mass-cost reduction including non-unit active input mass.
u,vv,w,h=S.symbols('u v w h',positive=True)
w0=w/(w+h); w1=h/(w+h)
s0,s1,e0,e1=S.symbols('s0 s1 e0 e1',positive=True)
Z=s0*e0+s1*e1
obj=w0*S.log(w0/s0)+w1*S.log(w1/s1)-w0*S.log(e0)-w1*S.log(e1)
star=(s0*e0/Z,s1*e1/Z)
eq(obj,KL((w0,w1),star)-S.log(Z))
add('independent symbolic block-mass KL gap identity with unnormalized active masses')

# Boundary-approximation control for a proper segment with no full-support law.
e=S.symbols('epsilon',positive=True)
c0=(R(2,3),R(1,3),0)
pe=((2-e)/3,R(1,3),e/3)
qe=((2-e)/(3-e),1/(3-e),0)
eq(sum(qe),1)
eq(qe[0]-R(1,3),(3-2*e)/(3*(3-e)))
eq(R(2,3)-qe[0],e/(3*(3-e)))
eq(tuple(S.limit(x,e,0,dir='+') for x in qe),c0)
eq(KL(qe,pe),-S.log(3-e)+S.log(3))
# For 0<e<1, this is exactly -log(1-e/3); no logarithm branch is crossed.
eq(tuple(pi-(1-e)*ci for pi,ci in zip(pe,c0)),(e/3,)*3)
A,B=S.symbols('A B',positive=True)
binKL=A*S.log(A/B)+(1-A)*S.log((1-A)/(1-B))
eq(S.diff(binKL,A,2)-4,(2*A-1)**2/(A*(1-A)))
# An all-boundary singleton exposes nonvacuity of E when C has no positive member.
c_single=(R(1,3),R(2,3),0); L=(R(1,4),R(3,4),R(1,2))
eq(update(c_single,L),(R(1,7),R(6,7),0))
assert update(c_single,L)!=c_single
add('positive-input approximation of a boundary segment plus all-boundary noninvariance witness')

# All-outcome quantifier, operator distinction, and zero-entry guard.
pbin=(R(1,4),R(3,4)); Lbin=(R(3,4),R(1,4))
clip=lambda p:(max(R(1,2),p[0]),1-max(R(1,2),p[0]))
eq(clip(update(pbin,Lbin)),(R(1,2),R(1,2)))
eq(update(clip(pbin),Lbin),(R(3,4),R(1,4)))
eq(update((R(1,2),R(1,2)),tuple(1-l for l in Lbin)),(R(1,4),R(3,4)))
aE=S.Matrix((R(3,4),R(1,4),0)); vE=S.Matrix((0,0,1)); dE=aE-vE
pE=(R(1,10),R(2,5),R(1,2)); LE=(R(3,4),R(3,4),R(1,4))
wE=lambda x:S.cancel((S.Matrix(x)-vE).dot(dE)/dE.dot(dE))
eq(wE(update(pE,LE)),R(81,130))
qE=tuple(wE(pE)*aE[i]+(1-wE(pE))*vE[i] for i in range(3))
eq(sum(update(qE,LE)[:2]),R(81,119))
eq(dot((1,0),(0,1)),0)
eq(dot((R(1,2),R(1,2)),(0,1)),R(1,2))
add('single-outcome, Euclidean, and zero-likelihood domain countercontrols')

# Product completion with a fresh asymmetric positive prior, both unary outcomes.
states=((-1,-1),(-1,1),(1,-1),(1,1))
def mean(v): return tuple(sum(x*s[j] for x,s in zip(v,states)) for j in (0,1))
def product_complete(v):
    mx,my=mean(v)
    return tuple((1+mx*x)*(1+my*y)/4 for x,y in states)
pM=(R(1,2),R(1,6),R(1,12),R(1,4)); qM=product_complete(pM)
eq(qM,(R(7,18),R(5,18),R(7,36),R(5,36)))
rowsM=(tuple(R(2+x,4) for x,y in states),tuple(R(2-x,4) for x,y in states))
for LM in rowsM:
    left=product_complete(update(pM,LM)); right=update(qM,LM)
    assert left!=right
    eq(left[0]*left[3]-left[1]*left[2],0)
    eq(right[0]*right[3]-right[1]*right[2],0)
eq(mean(product_complete(update(pM,rowsM[0]))),(R(1,5),R(1,10)))
eq(mean(update(qM,rowsM[0])),(R(1,5),-R(1,6)))
# Positive product competitor verifies the reverse orientation Pythagorean identity.
other=(R(1,6),R(1,3),R(1,6),R(1,3))
eq(KL(pM,other)-KL(pM,qM),KL(qM,other))
add('asymmetric positive moment-fibre selector countercontrol and opposite-orientation identity')

# Parent-proposed reviewer corollary, not a modification of the frozen author theorem.
V=KL(q,p); vals=tuple(KL(repair(update(p,L))[0],update(p,L)) for L in rows)
eq(dot(a,vals)-V,KL(a,b))
eq(dot(b,vals)-V,-KL(b,a))
assert a!=b
# A strictly positive repaired law makes the forward chain rule finite.
pF=(R(2,5),R(1,20),R(1,20),R(1,4),R(1,4))
qF=(R(2,9),R(1,9),R(1,9),R(5,18),R(5,18))
rowsF=((R(3,4),)*3+(R(1,4),)*2,(R(1,4),)*3+(R(3,4),)*2)
aF=tuple(dot(pF,L) for L in rowsF); bF=tuple(dot(qF,L) for L in rowsF)
eq(sum(aa*KL(update(pF,L),update(qF,L)) for aa,L in zip(aF,rowsF)),KL(pF,qF)-KL(aF,bF))
add('sampling-law-dependent reverse-KL drift and finite forward-KL chain rule',
    original_sampling_delta=str(KL(a,b)),repaired_sampling_delta=str(-KL(b,a)))

# Byte preservation and the independently captured replay receipt are part of review.
for row in json.loads((HERE/'SOURCE_BASELINE.json').read_text()):
    raw=(ROOT/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
replay=json.loads((HERE/'AUTHOR_REPLAY.json').read_text())
assert replay['exit_code']==0 and replay['original_sources_unchanged'] and replay['replayed_receipt_matches_author']
add('source-byte preservation and copied author replay')
result={'status':'PASS','independent_groups':len(checks),'python':platform.python_version(),'sympy':S.__version__, 'scope':'Ordinary proof review and exact controls; no proof-assistant certification, closure, or integration authority','checks':checks}
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS all',len(checks),'independent review groups')
