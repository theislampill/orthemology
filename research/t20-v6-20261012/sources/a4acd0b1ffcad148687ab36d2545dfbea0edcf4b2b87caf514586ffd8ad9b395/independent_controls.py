#!/usr/bin/env python3
"""Independent direct certificates and adversarial exact controls.

No import of the author checker, support search, kernel-circuit enumeration,
linear-programming result, or numerical optimizer. Tests supplement the proof.
"""
from itertools import combinations, product
from pathlib import Path
import json
import platform
import sympy as s

HERE = Path(__file__).resolve().parent
R = s.Rational
checks = []


def check(name, condition, detail=None):
    assert bool(condition), name
    row = {"name": name, "passed": True}
    if detail is not None:
        row["detail"] = detail
    checks.append(row)
    print(f"PASS {len(checks):02}: {name}")


def col(xs):
    return s.Matrix(xs)


def eq(A, B):
    return A.shape == B.shape and all(s.simplify(a-b) == 0 for a,b in zip(A,B))


def law(p):
    return sum(p) == 1 and all(a >= 0 for a in p)


def value(L, p):
    return (L.T*p)[0]


def bayes(L, p):
    a = value(L,p)
    assert a > 0
    return s.diag(*L)*p/a


def support(v):
    return {i for i,x in enumerate(v) if x > 0}


def certificate(M, a, L):
    v = M.T*a
    assert all(x >= 0 for x in v)
    assert all(x >= 0 for x in L)
    assert support(v) == support(L)
    return v


def ambiguity(M, L, p, q):
    return law(p) and law(q) and M*p == M*q and value(L,p)>0 and value(L,q)==0

# A triangle whose supplied columns include two edge-interior points and one
# strict interior point. This is different from the author's selected matrices.
M = s.Matrix([[1,1,1,1,1,1], [0,2,0,1,0,R(1,2)], [0,0,2,0,1,R(1,2)]])
L = col([0,0,1,0,R(3,4),R(1,4)])
a = col([0,0,1])
v = certificate(M,a,L)
check("nonvertex edge and interior columns: saturated bottom-face certificate",
      v == col([0,0,2,0,1,R(1,2)]) and M.rank()==3 and support(v)=={2,4,5})
check("same-support likelihood need not itself be retained",
      M.col_join(L.T).rank()==4)

# The signed relation moves probability from a vertex/vertex mixture to its
# supplied edge midpoint. Full-support priors keep feasibility trivial while
# exposing the probability/posterior distinction.
d = col([-R(1,2),0,-R(1,2),0,1,0])
b = s.ones(6,1)/6
p, q = b+d/12, b-d/12
check("nonvertex control: positive equal-record priors have different masses",
      law(p) and law(q) and min(p)>0 and min(q)>0 and M*p==M*q
      and value(L,p)-value(L,q)==R(1,24))
check("nonvertex control: feasibility certificate does not retain posterior",
      M*bayes(L,p) != M*bayes(L,q) and value(v,p)==value(v,q)>0)

# An invertible change of displayed record coordinates hides the literal mass
# row; append redundant rows to test the nonessential full-row-rank convention.
A = s.Matrix([[2,1,0],[0,1,1],[1,0,1]])
N = A*M
ap = A.T.inv()*a
u = A.T.inv()*col([1,0,0])
check("mass need only belong to the row space, not be a displayed row",
      A.det()!=0 and eq(N.T*u,s.ones(6,1)) and not any(list(N.row(i))==[1]*6 for i in range(3))
      and eq(certificate(N,ap,L),v))
Nr = N.col_join(N.row(0)+2*N.row(2))
check("redundant retained rows do not alter support certification",
      Nr.rank()==3 and eq(certificate(Nr,col(list(ap)+[0]),L),v))
check("empty and full support endpoints survive transformed coordinates",
      eq(certificate(N,s.zeros(3,1),s.zeros(6,1)),s.zeros(6,1))
      and eq(certificate(N,u,col([1,2,3,4,5,6])),s.ones(6,1)))

# Zero-column hull being a face is insufficient without saturation.
e = s.eye(6)
Lmid = col([0,0,0,1,0,0])
check("supplied edge midpoint must inherit zero status of its face",
      ambiguity(M,Lmid,e[:,3],(e[:,0]+e[:,1])/2))
Lint = col([1,1,1,1,1,0])
check("a singleton nonvertex zero set is not automatically a face",
      ambiguity(M,Lint,e[:,0]/2+e[:,1]/4+e[:,2]/4,e[:,5]))

D = s.Matrix([[1,1,1],[0,0,1]])
E = s.eye(3)
check("duplicate columns cannot have opposite support status",
      ambiguity(D,col([1,0,0]),E[:,0],E[:,1]))
Ld = col([R(1,4),R(3,4),0])
vd = certificate(D,col([1,-1]),Ld)
check("duplicate endpoint support allows feasibility and posterior without probability",
      vd==col([1,1,0]) and D*bayes(Ld,E[:,0])==D*bayes(Ld,E[:,1])==col([1,0])
      and value(Ld,E[:,0])!=value(Ld,E[:,1]))
Di = s.Matrix([[1,1,1,1],[-1,0,0,1]])
Ei=s.eye(4)
Li=col([0,R(1,3),R(2,3),0])
check("duplicate interior support keeps constant posterior but loses feasibility",
      Di*bayes(Li,Ei[:,1])==Di*bayes(Li,Ei[:,2])==col([1,0])
      and ambiguity(Di,Li,Ei[:,1],(Ei[:,0]+Ei[:,3])/2))

# Injectivity on the normalized simplex is not ambient linear row-space descent
# without mass retention.
B = s.Matrix([[0,1]])
check("omitting mass destroys row-space iff although p is affinely recoverable",
      B.col_join(s.ones(1,2)).rank()==2 and B.col_join(s.Matrix([[1,0]])).rank()==2
      and all(value(col([1,0]),col([1-t,t]))==1-t for t in [0,R(1,4),R(2,3),1]))
check("mass-only proper event gives explicit opposite-status point masses",
      ambiguity(s.ones(1,3),col([0,1,0]),col([0,1,0]),col([1,0,0])))
check("nonnegativity of likelihood is essential to zero-support equivalence",
      value(col([1,-1]),col([R(1,2),R(1,2)]))==0)
check("any nonzero nonnegative likelihood is feasible at every positive prior",
      min(p)>0 and all(value(col([int(i==j) for i in range(6)]),p)>0 for j in range(6)))

# Pairwise binary controls: use a character-by-subset construction rather than
# the author's explicit row list, and start with the probability-valued event.
states = list(product((1,-1),repeat=3))
scopes = [J for k in range(3) for J in combinations(range(3),k)]
P = s.Matrix([[s.prod(w[j] for j in J) for w in states] for J in scopes])
h = col([s.prod(w) for w in states])
g = col([int(len(set(w))==1) for w in states])
gcoef = col([R(1,4),0,0,0,R(1,4),R(1,4),R(1,4)])
Levent = col([g[i]*R(3+w[0],4) for i,w in enumerate(states)])
check("pairwise q indicator is a nonnegative row-space witness",
      P.rank()==7 and P*h==s.zeros(7,1) and eq(P.T*gcoef,g)
      and eq(certificate(P,gcoef,Levent),g) and set(Levent)=={0,R(1,2),1})
pp, pm = (s.ones(8,1)+h/2)/8, (s.ones(8,1)-h/2)/8
check("scaled event has exact distinct masses at one shared positive record",
      law(pp) and law(pm) and min(pp)>0 and min(pm)>0 and P*pp==P*pm
      and value(Levent,pp)==R(7,32) and value(Levent,pm)==R(5,32))
check("scaled event has exact different retained posterior unary means",
      P*bayes(Levent,pp)==col([1,R(5,7),R(5,7),R(5,7),1,1,1])
      and P*bayes(Levent,pm)==col([1,-R(1,5),-R(1,5),-R(1,5),1,1,1]))
check("event probability itself is unretained despite retained feasibility",
      value(Levent,h)/8==R(1,16) and P.col_join(Levent.T).rank()==8)
check("retained event q has known probability but unknown posterior",
      value(g,pp)==value(g,pm)==R(1,4)
      and (P*bayes(g,pp))[1]==R(1,2) and (P*bayes(g,pm))[1]==-R(1,2))
sp=col([int(w==(1,1,1)) for w in states])
bp,bm=(s.ones(8,1)+h)/8,(s.ones(8,1)-h)/8
check("singleton posterior-only support has boundary feasibility collision",
      ambiguity(P,sp,bp,bm) and P*bayes(sp,pp)==P*bayes(sp,pm))

# Twenty chosen supports cover empty/full, one parity side, both parity sides,
# mixed sizes, and complements. Every claim has a direct positive certificate
# or explicit pair of laws; no failed search establishes a negative result.
chosen=[set(),set(range(8))]
chosen += [{i} for i in range(8)]
chosen += [{i,j} for i,j in [(0,1),(0,3),(0,7),(2,5),(3,4)]]
chosen += [{0,1,2},{0,3,5,6},{1,2,4,7},{0,2,3,4,7},{0,1,2,3,4,5,6}]
yes=no=0
for U in chosen:
    pos=[i for i in U if h[i]==1]
    neg=[i for i in U if h[i]==-1]
    if not U or (pos and neg):
        w=s.zeros(8,1)
        for i in pos:w[i]=len(neg)
        for i in neg:w[i]=len(pos)
        assert support(w)==U and value(w,h)==0
        # Orthogonal character rows have norm squared 8.
        assert eq(P.T*(P*w/8),w)
        yes+=1
    else:
        I=col([int(i in U) for i in range(8)])
        px,qx=(bp,bm) if pos else (bm,bp)
        assert ambiguity(P,I,px,qx)
        no+=1
check("twenty bounded parity-support controls have explicit dual alternatives",
      len(chosen)==20 and yes+no==20,{"positive_certificates":yes,"explicit_ambiguities":no})

Z=[i for i,t in enumerate(g) if t==0]
p0=col([R(1,6) if i in Z else 0 for i in range(8)])
check("six-zero global face is a facet with a unique representing law",
      P[:,Z].rank()==6 and P.rank()==7 and value(g,p0)==0
      and P*p0==col([1,0,0,0,-R(1,3),-R(1,3),-R(1,3)])
      and len(P[:,Z].nullspace())==0)
coverage={}
for J in scopes:
    assignments={tuple(states[i][j] for j in J) for i in Z}
    coverage[str(J)]=len(assignments)
    assert assignments==set(product((1,-1),repeat=len(J)))
check("zeros cover all local assignments, forcing each nonnegative local summand to vanish",
      len(coverage)==7,coverage)
for J in combinations(range(3),2):
    for assignment in product((1,-1),repeat=2):
        cell=sum(p0[i] for i,w in enumerate(states) if tuple(w[j] for j in J)==assignment)
        assert cell==(R(1,6) if assignment[0]==assignment[1] else R(1,3))
check("strictly positive pair cells coexist with a global boundary point",True)

# Rational reparametrization a=exp(-4t), so finite t has a>0. No floating-point
# underflow is mistaken for an actually zero event probability.
z=s.symbols('z',positive=True)
pr=col([z/(6+2*z) if g[i] else 1/(6+2*z) for i in range(8)])
check("finite exponential tilt stays off the facet and tends to it only at infinity",
      s.simplify(value(g,pr)-z/(3+z))==0
      and eq(pr.applyfunc(lambda u:s.limit(u,z,0,dir='+')),p0))

rho=-R(2,5)
C=s.Matrix(3,3,lambda i,j:1 if i==j else rho)
# Sylvester principal minors independently check positive definiteness without
# the author's eigenvalue route.
check("unrealizable proposed covariance is nonetheless positive definite",
      [C[:j,:j].det() for j in (1,2,3)]==[1,R(21,25),R(49,125)])
proposed=col([1,0,0,0,rho,rho,rho])
local=[(1+rho*x*y)/4 for x,y in product((1,-1),repeat=2)]
check("positive compatible local tables fail the global nonnegative-q inequality",
      min(local)==R(3,20) and max(local)==R(7,20) and sum(local)==1
      and (gcoef.T*proposed)[0]==-R(1,20))

result={"status":"PASS","python":platform.python_version(),"sympy":s.__version__,
        "groups":len(checks),"arithmetic":"Exact integers, rationals, symbolic identities and limits",
        "scope":"Direct independent certificates and bounded adversarial controls; no author checker imported and no general theorem inferred from enumeration",
        "checks":checks}
(HERE/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS: {len(checks)} independent control groups.')
