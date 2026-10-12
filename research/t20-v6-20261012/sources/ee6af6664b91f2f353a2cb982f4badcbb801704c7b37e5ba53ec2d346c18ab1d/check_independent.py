#!/usr/bin/env python3
"""Independent exact adversarial controls; no author test code is imported.
The universal results require the separately written mathematical review.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sympy as S

ROOT = Path(__file__).resolve().parent
checks = []

def require(name, condition, detail=None):
    if not bool(condition):
        raise RuntimeError(name)
    item = {"name": name, "passed": True}
    if detail is not None:
        item["detail"] = detail
    checks.append(item)

def zero(expr):
    if isinstance(expr, S.MatrixBase):
        return all(S.simplify(t) == 0 for t in expr)
    return S.simplify(expr) == 0

def partition(n):
    if n == 0:
        yield ()
        return
    for p in partition(n-1):
        yield p + ((n-1,),)
        for j in range(len(p)):
            yield p[:j] + (p[j] + (n-1,),) + p[j+1:]

def refinement(p, q):
    return tuple(tuple(sorted(set(a)&set(b))) for a in p for b in q if set(a)&set(b))

def supported(mask, p):
    return mask == 0 or any(all(not(mask & (1<<i)) or i in b for i in range(5)) for b in p)

# This is an exhaustive finite support-of-monomial control, not a C2 proof.
ps = list(partition(5))
count = 0
for p, q in itertools.product(ps, repeat=2):
    r = refinement(p,q)
    for mask in range(32):
        if (supported(mask,p) and supported(mask,q)) != supported(mask,r):
            raise RuntimeError("partition intersection failed")
        count += 1
require("all five-label partition-pair interaction supports", True,
        {"partitions":len(ps),"pair_mask_cases":count})

# Independent nonpolynomial homogeneous fixture and the anchored constant repair.
q = S.symbols('q1:4', positive=True)
x = S.symbols('x1:4', real=True)
F = q[0]*S.sin(x[0]) + q[1]*q[2]/(q[1]+q[2])*(x[1]-x[2])**2
anchor = {q[0]:2,q[1]:3,q[2]:4,x[0]:0,x[1]:1,x[2]:3}
cells = ((0,), (1,2))
Fstar = F.subs(anchor)
fs, ks, hs = [], [], []
for cell in cells:
    outside={var:val for var,val in anchor.items() if var not in tuple(q[i] for i in cell)+tuple(x[i] for i in cell)}
    f = F.subs(outside)-Fstar
    k = S.simplify(sum(q[i]*S.diff(f,q[i]) for i in cell)-f)
    fs.append(f); ks.append(k); hs.append(f+k)
    require("Euler anchored defect is constant for cell "+str(cell), not k.free_symbols)
    require("corrected summand is homogeneous for cell "+str(cell),
            zero(sum(q[i]*S.diff(hs[-1],q[i]) for i in cell)-hs[-1]))
require("constant defects sum to anchor",zero(sum(ks)-Fstar))
require("C2 summands recover exact original F",zero(sum(hs)-F))
t=S.symbols('t',positive=True)
require("nonpolynomial full extension scales linearly",zero(F.subs(dict(zip(q,[t*a for a in q])), simultaneous=True)-t*F))

# Exact group-action and gradient obstructions, independently constructed.
w=S.Matrix([S.Rational(1,4)]*4)
a=S.Matrix([2,2,1,1]); b=S.Matrix([2,1,2,1])
def tilt(w,a):
    z=sum(w[i]*a[i] for i in range(len(w)))
    return S.Matrix([w[i]*a[i]/z for i in range(len(w))])
def push(w,a,v):
    z=sum(w[i]*a[i] for i in range(len(w)))
    dz=sum(v[i]*a[i] for i in range(len(w)))
    return S.Matrix([a[i]*v[i]/z-a[i]*w[i]*dz/z**2 for i in range(len(w))])
def odds(w): return S.cancel(w[0]*w[3]/(w[1]*w[2]))
require("row and column leave odds unchanged",odds(tilt(tilt(w,a),b))==odds(w))
require("missing singleton action changes odds",odds(tilt(w,S.Matrix([2,1,1,1])))!=odds(w))
eps=S.Matrix([1,-1,-1,1])
field=lambda p: -odds(p)*eps
res=field(tilt(w,a))-push(w,a,field(w))
require("invariant rho energy fails Fisher covariance",res==S.Matrix([S.Rational(1,3),-S.Rational(1,3),S.Rational(1,3),-S.Rational(1,3)]))
y1,y2,y3=S.symbols('y1:4',positive=True); y4=1-y1-y2-y3
th=S.log(y1)+S.log(y4)-S.log(y2)-S.log(y3)
require("theta field exact mixed-derivative obstruction",zero(S.diff(-th,y2)-(1/y4+1/y2)))
normal=S.Matrix([1,-1,-1]); row=S.Matrix([1,1,0]); col=S.Matrix([1,0,1])
require("log-odds Euclidean metric permits theta energy interaction",normal.dot(row)==0 and normal.dot(col)==0,
        "Under Euclidean log-odds metric, grad(theta^2/2)=theta*(1,-1,-1); this is row/column equivariant and not singleton-equivariant.")

# Fixed complete instruments vs action orbits. Includes zero branch and tagged reduction.
rows=S.Matrix([[S.Rational(3,4),S.Rational(3,4),S.Rational(1,4),S.Rational(1,4)],
               [S.Rational(1,4),S.Rational(1,4),S.Rational(3,4),S.Rational(3,4)]])
cols=S.Matrix([[S.Rational(3,4),S.Rational(1,4),S.Rational(3,4),S.Rational(1,4)],
               [S.Rational(1,4),S.Rational(3,4),S.Rational(1,4),S.Rational(3,4)]])
tagged=(rows/3).col_join(cols*S.Rational(2,3))
require("tagged cone instrument is complete",list(S.ones(1,4)*tagged)==[1]*4)
require("tagged full outcome columns separate refinement cells",len({tuple(tagged[:,i]) for i in range(4)})==4)
for l,mat,beta in ((0,rows,S.Rational(1,3)),(1,cols,S.Rational(2,3))):
    for j in range(2):
        require("tagged conditional equals original "+str((l,j)),tilt(w,S.Matrix(list(mat[j,:]))*beta)==tilt(w,S.Matrix(list(mat[j,:]))))
mid=(tilt(w,S.Matrix(list(rows[0,:])))+tilt(w,S.Matrix(list(cols[0,:]))))/2
require("convexification destroys orbit odds invariant",odds(mid)==S.Rational(3,4))
# Occupied final intersections always imply occupied prefixes; exclude zero final mass.
z=S.Matrix([0,S.Rational(1,3),0,S.Rational(2,3)])
for rowcell,colcell in itertools.product(((0,1),(2,3)),((0,2),(1,3))):
    cell=set(rowcell)&set(colcell)
    final=sum(z[i] for i in cell)
    prefix=sum(z[i] for i in rowcell)
    if final>0:
        require("positive intersection has valid prefix "+str(cell),prefix>0)
        first=S.Matrix([z[i]/prefix if i in rowcell else 0 for i in range(4)])
        secondmass=sum(first[i] for i in colcell)
        second=S.Matrix([first[i]/secondmass if i in colcell else 0 for i in range(4)])
        direct=S.Matrix([z[i]/final if i in cell else 0 for i in range(4)])
        require("sequential conditional equals direct "+str(cell),second==direct)
    else:
        require("zero intersection branch vector is zero "+str(cell),all(z[i]==0 for i in cell))

# Restricted controls: exact six-state fixture independently derived.
points=[(xx,yy,1-xx-yy) for xx in (S.Rational(0),S.Rational(1,2)) for yy in (S.Rational(0),S.Rational(1,4),S.Rational(1,2))]
A=S.Matrix.hstack(*(S.Matrix(p) for p in points)); w6=S.ones(6,1)/6

def grouped_matrix(A,v):
    signatures=list((v.T*A))
    vals=list(dict.fromkeys(signatures)); groups=[[i for i,t in enumerate(signatures) if t==value] for value in vals]
    B=S.Matrix.vstack(*(S.Matrix(A.rows,A.cols,lambda i,j:A[i,j] if j in group else 0) for group in groups))
    return B,signatures,groups

vx=S.Matrix([1,0,0]); B,lams,groups=grouped_matrix(A,vx)
require("six-state ranks and sidecar cost",(A.rank(),B.rank(),B.rank()-A.rank())==(3,4,1))
h=S.Matrix([1,-2,1,0,0,0])/24; k=S.Matrix([1,0,-1,-1,0,1])/24
for delta in (h,k):
    require("both signed fixture laws strictly positive "+str(list(delta)),all(t>0 for t in w6+delta) and all(t>0 for t in w6-delta))
require("distinct complete laws share B",h!=S.zeros(6,1) and B*h==S.zeros(B.rows,1))
require("q-only fixture loses exactly B information",A*k==S.zeros(3,1) and B*k!=S.zeros(B.rows,1))
require("q-only fixture even retains signature masses",sum(k[:3])==0 and sum(k[3:])==0)
factor=S.symbols('factor',positive=True)
factors=S.Matrix([1,1,1,factor,factor,factor])
require("same B implies identical symbolic full q histories",zero(A*tilt(w6+h,factors)-A*tilt(w6-h,factors)))
qdiff=S.simplify(A*tilt(w6+k,factors)-A*tilt(w6-k,factors))
require("same mass/scalar response does not recover full q",zero(vx.dot(qdiff)) and not zero(qdiff),str(qdiff))
require("declared half-tilt separates y",qdiff.subs(factor,S.Rational(1,2))[1]!=0,str(qdiff.subs(factor,S.Rational(1,2))))

def velocity(p,g):
    q=A*p; f=A.T*g
    return -S.diag(*p)*(f-S.ones(6,1)*(g.dot(q)))
vy=S.Matrix([0,1,0]); gap=A*(velocity(w6+h,vy)-velocity(w6-h,vy))
require("expanded y fitness separates old quotient",gap[1]!=0,str(gap))
for v in (vx,vy,S.Matrix([1,1,0]),S.Matrix([1,3,0]),S.ones(3,1),S.zeros(3,1)):
    BV,ls,gs=grouped_matrix(A,v)
    D=S.diag(*ls); O=S.Matrix.vstack(*(A*D**r for r in range(len(gs))))
    require("observable polynomial closure equals B rowspace "+str(list(v)),O.rank()==BV.rank()==O.col_join(BV).rank())
    kernel=A.nullspace(); K=S.Matrix.hstack(*kernel) if kernel else S.zeros(A.cols,0)
    require("rank subtraction on retained-output fibre "+str(list(v)),(BV*K).rank()==BV.rank()-A.rank())
    if len(gs)==1:
        require("single-signature/gauge dynamics vanish "+str(list(v)),zero(velocity(w6+h,v)) and BV==A)
require("one dimensional control may require all weights",grouped_matrix(A,S.Matrix([1,3,0]))[0].rank()==6)
# Gauge-shifting every control leaves signatures' equality relation and dynamics unchanged.
require("mass covector gauge does not change quotient",grouped_matrix(A,vx+7*S.ones(3,1))[2]==groups)
require("mass covector gauge does not change flow",zero(velocity(w6+k,vx+7*S.ones(3,1))-velocity(w6+k,vx)))
# For s=1 equality means full q equality, not equality of trivial control response.
require("zero control scalar alone cannot imply full-q equality",A[:,0]!=A[:,1] and (S.zeros(3,1).dot(A[:,0]))==(S.zeros(3,1).dot(A[:,1])))
# One-state zero-dimensional case.
A1=S.Matrix([S.Rational(1,3),S.Rational(2,3)])
require("one-state sidecar cost zero",A1.rank()==1 and grouped_matrix(A1,S.Matrix([5,2]))[0].rank()-A1.rank()==0)

# Nine-state composition control: isolated profiles do not compose.
A9=S.Matrix.hstack(*(S.Matrix([S.Rational(i,4),S.Rational(j,4),1-S.Rational(i+j,4)]) for i in range(3) for j in range(3)))
w9=S.ones(9,1)/9
contrast=[1,-2,1]
h9=S.Matrix([S.Rational(contrast[i]*contrast[j],100) for i in range(3) for j in range(3)])
Bx=grouped_matrix(A9,vx)[0]; By=grouped_matrix(A9,vy)[0]
require("nine-state contrasting laws positive",all(z>0 for z in w9+h9) and all(z>0 for z in w9-h9))
require("same complete isolated x and y barycentre profiles",zero(Bx*h9) and zero(By*h9))
require("isolated-profile stack loses one dimension",Bx.col_join(By).rank()==8)
require("composed signature quotient needs all nine weights",grouped_matrix(A9,S.Matrix([1,3,0]))[0].rank()==9)
fx=S.Matrix([S.Rational(1,2**i) for i in range(3) for j in range(3)])
fy=S.Matrix([S.Rational(1,2**j) for i in range(3) for j in range(3)])
endpoint=lambda p: A9*tilt(tilt(p,fx),fy)
gap9=S.simplify(endpoint(w9+h9)-endpoint(w9-h9))
require("literal successive permitted corrections separate",not zero(gap9),str(gap9))
require("sequential and joint tilt normalization agree",tilt(tilt(w9+h9,fx),fy)==tilt(w9+h9,S.matrix_multiply_elementwise(fx,fy)))
require("missing nine-state tensor has rank one",S.Matrix(3,3,list(h9)).rank()==1)

print(json.dumps({"status":"PASS","check_count":len(checks),"checks":checks,"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"sympy_version":S.__version__,"limits":"Exact finite/algebraic controls; universal proofs and domain assumptions require REVIEW.md."},indent=2))
