#!/usr/bin/env python3
"""Independent exact bounded controls; no import or execution of author modules.
Uses Fraction linear algebra and formal prime-log arithmetic. SymPy is used only
for explicit rational-function limits. These checks do not prove the theorems.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import sympy as sp

checks=[]
def ck(name, condition, detail=None):
    assert condition, name
    item={'name':name,'passed':True}
    if detail is not None:item['detail']=detail
    checks.append(item)
    print(f'PASS {len(checks):02d}: {name}')
def norm(a):
    a=list(map(Q,a)); assert all(x>=0 for x in a)
    s=sum(a)
    if not s:raise ValueError('zero branch: no posterior')
    return [x/s for x in a]
def bayes(p,l):return norm([x*y for x,y in zip(p,l)])
def mean(v,p):return [sum(p[i]*v[i][j] for i in range(len(p))) for j in range(len(v[0]))]
def cov(v,p):
    m=mean(v,p); d=len(m)
    return [[sum(p[i]*v[i][j]*v[i][k] for i in range(len(p)))-m[j]*m[k] for k in range(d)]for j in range(d)]
def det(a):
    a=[list(map(Q,row))for row in a];d=Q(1)
    for i in range(len(a)):
        pivot=next((j for j in range(i,len(a))if a[j][i]),None)
        if pivot is None:return Q(0)
        if pivot!=i:a[i],a[pivot]=a[pivot],a[i];d=-d
        p=a[i][i];d*=p
        for j in range(i+1,len(a)):
            f=a[j][i]/p
            for k in range(i,len(a)):a[j][k]-=f*a[i][k]
    return d
def logq(x):
    x=Q(x);assert x>0;out={}
    for n,sgn in [(x.numerator,1),(x.denominator,-1)]:
        k=2
        while k*k<=n:
            while n%k==0:out[k]=out.get(k,Q(0))+sgn;n//=k
            k+=1
        if n>1:out[n]=out.get(n,Q(0))+sgn
    return {k:v for k,v in out.items()if v}
def combine(terms):
    out={}
    for coeff,lg in terms:
        for p,v in lg.items():out[p]=out.get(p,Q(0))+coeff*v
    return {p:v for p,v in out.items()if v}
def entropy(p,r):return combine((x,logq(x/y))for x,y in zip(p,r)if x)
def kl(p,q):
    assert all(y>0 for x,y in zip(p,q)if x)
    return entropy(p,q)
def support(p):return {i for i,x in enumerate(p)if x}
def mult(a,b):return [x*y for x,y in zip(a,b)]

# Zero-dimensional model, nonnormalized reference, and a genuinely smaller chart.
r0=[2,5,7];q0=norm(r0)
ck('dimension-zero family has fixed reference proportions',q0==[Q(1,7),Q(5,14),Q(1,2)] and bayes(q0,[3,3,3])==q0 and bayes(q0,[1,2,1])!=q0)
ck('zero-dimensional hard omission cannot preserve its only saturated stratum',support(bayes(q0,[1,0,1]))=={0,2} and q0!=bayes(q0,[1,0,1]))

# Different configuration from the author: triangle, duplicate vertex, edge point,
# hypotenuse point, and a strictly interior supplied atom.
v=[(0,0),(0,0),(1,0),(2,0),(0,2),(1,1),(1,Q(1,2))]
r=list(map(Q,[2,5,3,7,11,13,17]));bottom={0,1,2,3}
L=[Q(2)**x if y==0 else Q(0) for x,y in v]
q=bayes(norm(r),L)
ck('saturated triangle edge includes duplicate and nonvertex atoms',q==list(map(lambda n:Q(n,41),[2,5,6,28,0,0,0])) and mean(v,q)==[Q(62,41),Q(0)] and support(q)==bottom)
s=sp.symbols('s',positive=True)
w=[sp.Rational(a.numerator,a.denominator)*2**x*s**int(2*y) for a,(x,y)in zip(r,v)]
ray=[x/sum(w)for x in w]
ck('explicit normal ray suppresses every off-face supplied atom',[sp.limit(x,s,0,dir='+')for x in ray]==[sp.Rational(x.numerator,x.denominator)for x in q])
endpoint=[Q(10,41),0,0,Q(31,41),0,0,0]
ck('same boundary mean does not determine support or duplicate weights',mean(v,endpoint)==mean(v,q) and support(endpoint)!=support(q) and q[0]/q[1]==Q(2,5))
expected=combine([(Q(62,41),logq(2)),(-1,logq(41))])
ck('formal prime-log entropy identity holds for an alternative boundary law',entropy(q,r)==expected and combine([(1,entropy(endpoint,r)),(-1,kl(endpoint,q)),(-1,entropy(q,r))])=={} and endpoint[0]/q[0]==5 and endpoint[3]/q[3]==Q(31,28))
ck('reference normalization changes entropy by a constant only',bayes(norm(r),L)==bayes(r,L) and combine([(1,entropy(q,norm(r))),(-1,entropy(q,r)),(-1,logq(sum(r)))])=={})
C=cov(v,q);var=C[0][0];z=mean(v,q)[0]
score=[q[i]*(v[i][0]-z) for i in bottom]
fisher=sum(score[j]**2/q[i]for j,i in enumerate(sorted(bottom)))
mean_lift=sum((q[i]*(v[i][0]-z)/var)**2/q[i]for i in bottom)
ck('face tangent metric is positive after removing its normal redundancy',var>0 and C[0][1]==C[1][0]==C[1][1]==0 and fisher==var and mean_lift==1/var,{'variance':str(var),'mean_metric':str(1/var)})
psi=[(3*x+5,)for x,y in v]
ck('affine coordinate changes transform covariance and inverse metric correctly',cov(psi,q)[0][0]==9*var and 9/cov(psi,q)[0][0]==1/var)

# Intersection law and a globally inadmissible likelihood admissible on a face.
left=[Q(3)**int(y) if x==0 else 0 for x,y in v]
base=norm(r);joint=bayes(bayes(base,L),left)
ck('two positive face branches commute and retain duplicate-vertex proportions',joint==bayes(bayes(base,left),L)==[Q(2,7),Q(5,7),0,0,0,0,0])
nonfacial=[1,1,0,0,0,0,1]
ck('boundary criterion depends on support intersection rather than global likelihood support',support(nonfacial)=={0,1,6} and 0<v[6][0] and 0<v[6][1] and sum(v[6])<2 and bayes(q,nonfacial)==joint)
split=[1,0,0,0,0,0,1]
ck('splitting a duplicate fails even at an unchanged vertex mean',mean(v,bayes(q,split))==[0,0] and bayes(q,split)!=joint)
try:bayes(q,[int(y==2)for x,y in v]);blocked=False
except ValueError:blocked=True
ck('disjoint-face likelihood has zero branch and no normalized posterior',sum(a*int(y==2)for a,(x,y)in zip(q,v))==0 and blocked)

# Full-rank covariance also cannot certify membership in the chosen closure.
square=list(product((-1,1),repeat=2));p3=[Q(1,3)]*3+[Q(0)]
prod=[Q(4,9),Q(2,9),Q(2,9),Q(1,9)]
C3=cov(square,p3)
ck('nonfacial law can have an interior mean and positive definite full covariance',mean(square,p3)==mean(square,prod)==[Q(-1,3),Q(-1,3)] and C3[0][0]>0 and det(C3)==Q(16,27) and p3[0]*p3[3]!=p3[1]*p3[2] and prod[0]*prod[3]==prod[1]*prod[2])
rn=norm([1,2,4,9]);hard=[0,0,Q(1,2),Q(1,2)]
edge=bayes(rn,hard)
ck('local hard evidence preserves a nonproduct reference residual class',edge==[0,0,Q(4,13),Q(9,13)] and rn[0]*rn[3]/(rn[1]*rn[2])==Q(9,8) and edge[0]*edge[3]*rn[1]*rn[2]==edge[1]*edge[2]*rn[0]*rn[3])
pplus=[Q(2+x*y,8)for x,y in square]
pminus=[Q(2-x*y,8)for x,y in square]
ck('local closed-model update is distinct from all-prior retained sufficiency',mean(square,pplus)==mean(square,pminus)==[0,0] and mean(square,bayes(pplus,hard))==[1,Q(1,2)] and mean(square,bayes(pminus,hard))==[1,Q(-1,2)])

# Pairwise six-atom facet: fresh Fraction computation, principal minors and kernel.
cube=list(product((-1,1),repeat=3));facet=[i for i,(x,y,z)in enumerate(cube)if not x==y==z]
pf=[Q(1,6)if i in facet else 0 for i in range(8)]
phi=[(x,y,z,x*y,x*z,y*z)for x,y,z in cube];full=cov(phi,pf);reduced=[row[:5]for row in full[:5]]
minors=[det([row[:k]for row in reduced[:k]])for k in range(1,6)]
normal=[0,0,0,1,1,1]
ck('pairwise facet has a positive five-dimensional relative covariance and lost normal',all(x>0 for x in minors) and det(full)==0 and all(sum(row[i]*normal[i]for i in range(6))==0 for row in full),{'leading_principal_minors':list(map(str,minors))})
pairs=[(0,1),(0,2),(1,2)];assignments=set(product((-1,1),repeat=2))
witness={str(pair):{str(a):next(i for i in facet if (cube[i][pair[0]],cube[i][pair[1]])==a)for a in sorted(assignments)}for pair in pairs}
ck('six supported atoms witness every pair assignment, forcing any preserving hard factor positive everywhere',all({(cube[i][j],cube[i][k])for i in facet}==assignments for j,k in pairs),witness)
def soft_path(coeffs):
    weights=[sp.prod(coeff*s if state[j]==state[k] else 1 for coeff,(j,k)in zip(coeffs,pairs))for state in cube]
    branch=sp.expand(sum(weights)/8)
    lim=[sp.limit(x/sum(weights),s,0,dir='+')for x in weights]
    return branch,lim
b1,l1=soft_path([1,1,1]);b2,l2=soft_path([1,2,3])
ck('distinct bounded pair-local soft paths share an impossible hard limit but different posteriors',sp.limit(b1,s,0,dir='+')==sp.limit(b2,s,0,dir='+')==0 and l1==[sp.Rational(x.numerator,x.denominator) if isinstance(x,Q)else x for x in pf] and l1!=l2 and all(l2[i]>0 for i in facet) and all(l2[i]==0 for i in range(8)if i not in facet),{'equal_rate_branch':str(b1),'unequal_rate_branch':str(b2),'unequal_rate_limit':list(map(str,l2)),'probability_valued_domain':'0 < s <= 1/3'})
ck('impossible limiting event and direct nonlocal positive event remain different',all(not all(state[j]!=state[k]for j,k in pairs)for state in cube) and Q(len(facet),len(cube))==Q(3,4))

result={'status':'PASS','scope':'Independent bounded exact rational and symbolic controls; no author code imported; universal proofs separately reviewed.','assertion_groups':len(checks),'checks':checks}
out=Path(__file__).resolve().parent
(out/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS: {len(checks)} independent exact assertion groups')
