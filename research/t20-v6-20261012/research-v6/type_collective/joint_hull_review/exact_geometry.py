import sympy as S,json,hashlib
from itertools import combinations,product
from pathlib import Path
b=Path(__file__).parent
C=[(1,1,1,1,0,0),(0,0,1,0,1,0),(0,0,1,0,0,1),(0,0,0,1,1,0),(0,0,0,1,0,1),(0,0,0,0,1,1)]
high=[tuple(int(i in k)for i in range(4))for k in combinations(range(4),2)]
P=[(a,a)+t for a,t in product([0,1],high)]
wc=list(map(S.Rational,['1/4','1/8','1/8','1/8','1/8','1/4']));wp=[S.Rational(1,8)if v[0]==0 else S.Rational(1,24)for v in P];p=S.Matrix([S.Rational(1,4)]*2+[S.Rational(1,2)]*4)
def bary(v,w):return sum((a*S.Matrix(x)for a,x in zip(w,v)),S.zeros(6,1))
def diff(v):return S.Matrix.hstack(*[S.Matrix(x)-S.Matrix(v[-1])for x in v[:-1]])
assert sum(wc)==sum(wp)==1 and min(wc)>0 and min(wp)>0
assert bary(C,wc)==bary(P,wp)==p
assert {v[:2]for v in C}=={v[:2]for v in P}
assert {v[2:]for v in C}=={v[2:]for v in P}
DC,DP=diff(C),diff(P);assert DC.rank()==DP.rank()==S.Matrix.hstack(DC,DP).rank()==4
constraint=S.Matrix([[1,-1,0,0,0,0],[0,0,1,1,1,1]])
assert constraint*DC==S.zeros(2,5)and constraint*DP==S.zeros(2,11)
h=S.Matrix([1,0,0,0,0,0]);assert constraint*h==S.Matrix([1,0])
four=[(a,a)+(1,1,0,0)for a in [0,1]]+[(a,a)+(0,0,1,1)for a in [0,1]];assert all(v in P for v in four)
x=(1,1,0,0,1,1);assert x in P and x[0]>x[2]and all(v[0]<=v[2]for v in C)
r={'status':'PASS_EXACT_RATIONAL_GEOMETRY','C_vertices':C,'P_vertices':P,'C_weights':list(map(str,wc)),'P_weights':list(map(str,wp)),'common_context':list(map(str,p)),'ranks':{'C':4,'P':4,'joint':4},'common_tangent_constraints':['h0=h1','h2+h3+h4+h5=0'],'block_projections_equal':True,'h_transverse':True,'four_product_test_truths_members':True,'proper_joint_hull_witness':x,'proof_scope':'Exact finite barycentric/rank/membership checks only; nonlinear strict repair and epsilon obstruction reuse independently read original theorem bodies. Intrinsic interior justified in written review.'}
(b/'EXACT_GEOMETRY.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
