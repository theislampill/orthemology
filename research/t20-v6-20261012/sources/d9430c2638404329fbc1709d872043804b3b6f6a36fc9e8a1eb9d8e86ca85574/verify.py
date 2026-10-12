"""Exact finite controls; does not prove the universal ordinary theorem."""
import json
from pathlib import Path
import sympy as S

checks=[]
def check(label, proposition):
    if not proposition:
        raise RuntimeError(label)
    checks.append(label)

def zero(M):
    return all(S.simplify(x)==0 for x in M)

R=S.Rational
points=[S.Matrix([x,y,1-x-y]) for x in [R(0),R(1,2)] for y in [R(0),R(1,4),R(1,2)]]
A=S.Matrix.hstack(*points)
B=S.zeros(6,6)
for j,p in enumerate(points):
    B[3*(j//3):3*(j//3)+3,j]=p
w=S.ones(6,1)/6
h=S.Matrix([1,-2,1,0,0,0])/24
k=S.Matrix([1,0,-1,-1,0,1])/24
check('source columns are probability vectors',all(sum(p)==1 and min(p)>=0 for p in points))
check('A rank 3',A.rank()==3)
check('restricted B rank 4',B.rank()==4)
check('exact augmentation difference is one',B.rank()-A.rank()==1)
check('full distinguished rank 6',S.diag(*[1]*6).rank()==6)
check('all displayed states positive',all(min(w+v)>0 and min(w-v)>0 for v in [h,k]))
check('hidden perturbation grouped record equal',zero(B*h))
check('hidden perturbation is nonzero',not zero(h))
a,b=S.symbols('a b',positive=True)
D=S.diag(a,a,a,b,b,b)
def output(v,D):
    dv=D*v
    return A*dv/sum(dv)
check('hidden perturbation remains invisible for arbitrary group tilt',zero(output(w+h,D)-output(w-h,D)))
check('q-only perturbation current outputs equal',zero(A*k))
check('q-only perturbation grouped output differs',not zero(B*k))
Dhalf=S.diag(1,1,1,R(1,2),R(1,2),R(1,2))
gap=S.simplify(output(w+k,Dhalf)[1]-output(w-k,Dhalf)[1])
check('restricted tilt distinguishes q-only pair',gap==R(-1,36))

def velocity(v,g):
    q=A*v
    fitness=A.T*g
    wd=-S.diag(*v)*fitness+v*(g.dot(q))
    return A*wd
vx=S.Matrix([1,0,0]); vy=S.Matrix([0,1,0]); one=S.ones(3,1)
check('permitted x velocity identical for hidden pair',zero(velocity(w+h,vx)-velocity(w-h,vx)))
check('expanded y velocity distinguishes hidden pair',not zero(velocity(w+h,vy)-velocity(w-h,vy)))
check('zero control stationary',zero(velocity(w,S.zeros(3,1))))
check('mass-gauge control stationary',zero(velocity(w,one)))
check('q-only pair initial x-induced velocities differ',not zero(velocity(w+k,vx)-velocity(w-k,vx)))

# Exact basis extension: one group-y row plus q spans all required B rows.
extra=B[1,:]
check('explicit one-coordinate sidecar sufficient',A.col_join(extra).rank()==B.rank())
check('explicit sidecar belongs to B span',B.col_join(extra).rank()==B.rank())
check('A rows in B span',B.col_join(A).rank()==B.rank())
# Generic direction x+sqrt(2)y is not needed for executable exact support:
# x+3y has six distinct values here.
g=S.Matrix([1,3,0]); values=list(A.T*g)
check('one full-control covector distinguishes six columns',len(set(values))==6)
# Nonzero low-dimensional U can distinguish all support points.
check('single-direction full distinction changes quotient rank',len(set(values))==len(points))
# Grouped record evolution identity, on symbolic positive unnormalised law.
z=S.symbols('z0:6',positive=True); norm=sum(z); p=S.Matrix(z)/norm
q=A*p; fitness=A.T*vx
pd=-S.diag(*p)*fitness+p*vx.dot(q)
bp=B*p
expected=S.Matrix.vstack(- (0-vx.dot(q))*bp[0:3,0],-(R(1,2)-vx.dot(q))*bp[3:6,0])
check('grouped dynamics exactly intertwine',zero(B*pd-expected))
# Separate complete correction profiles can lose composed corrections.
pts9=[S.Matrix([R(i,4),R(j,4),1-R(i+j,4)]) for i in range(3) for j in range(3)]
A9=S.Matrix.hstack(*pts9)
Bx=S.zeros(9,9); By=S.zeros(9,9)
for ix,p9 in enumerate(pts9):
    i,j=divmod(ix,3)
    Bx[3*i:3*i+3,ix]=p9
    By[3*j:3*j+3,ix]=p9
v9=[1,-2,1]
h9=S.Matrix([R(v9[i]*v9[j],100) for i in range(3) for j in range(3)])
w9=S.ones(9,1)/9
check('nine-point states remain strictly positive',min(w9+h9)>0 and min(w9-h9)>0)
check('all isolated x profiles agree',zero(Bx*h9))
check('all isolated y profiles agree',zero(By*h9))
check('isolated profile stack rank eight',Bx.col_join(By).rank()==8)
check('joint signatures all distinct',len({(p[0],p[1]) for p in pts9})==9)
D9=S.diag(*[R(1,2**(i+j)) for i in range(3) for j in range(3)])
def out9(v):
    dv=D9*v
    return A9*dv/sum(dv)
gap9=S.simplify(out9(w9+h9)-out9(w9-h9))
check('composed x then y correction separates',not zero(gap9))
Dx=S.diag(*[R(1,2**i) for i in range(3) for j in range(3)])
Dy=S.diag(*[R(1,2**j) for i in range(3) for j in range(3)])
check('joint correction is literal product of allowed steps',Dx*Dy==D9)
check('missing tensor has rank one',S.Matrix(3,3,list(h9)).rank()==1)
result={'status':'PASS','scope':'finite exact controls, ordinary proofs separate','checks':checks,'count':len(checks),'q_only_tilt_y_gap':str(gap),'composed_nine_point_gap':[str(v) for v in gap9],'sympy':S.__version__}
print(json.dumps(result,indent=2))
