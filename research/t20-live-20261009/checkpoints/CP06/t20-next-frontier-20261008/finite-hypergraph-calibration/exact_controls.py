#!/usr/bin/env python3
"""Exact rational finite-panel controls; no endpoint samples are drawn."""
from fractions import Fraction as F
from itertools import product, combinations
from math import prod
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent; results={}
def save(n,v):results[n]=v;print('PASS',n)
def Q(H,x):return prod(((1-prod((x[i] for i in S),start=F(1)))**n for S,n in H.items()),start=F(1))
def contrast(H,S,x,fixed=None):
    z=F(1);fixed={} if fixed is None else fixed
    for bits in product([0,1],repeat=len(S)):
        y=[F(0)]*len(x)
        for i,a in fixed.items():y[i]=a
        for i,b in zip(S,bits):
            if b:y[i]=x[i]
        q=Q(H,y)
        if q<=0:raise ValueError('raw masked probability is not positive')
        z*=q**((-1)**(len(S)-sum(bits)))
    return z
def iroot(n,k):
    lo,hi=0,1
    while hi**k<n:hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**k<n:lo=mid
        else:hi=mid
    if hi**k==n:return hi
    if lo**k==n:return lo
    raise ValueError('not an exact integer power')
def rational_root(z,k):return F(iroot(z.numerator,k),iroot(z.denominator,k))
def P(H,S,x):return 1-rational_root(contrast(H,S,x),H[S])
def rank(A,n=None):
    if not A:return 0
    Z=[[F(v) for v in row] for row in A];r=0
    for c in range(len(Z[0])):
        j=next((j for j in range(r,len(Z)) if Z[j][c]),None)
        if j is None:continue
        Z[r],Z[j]=Z[j],Z[r];pivot=Z[r][c];Z[r]=[z/pivot for z in Z[r]]
        for j in range(len(Z)):
            if j!=r:
                z=Z[j][c];Z[j]=[a-z*b for a,b in zip(Z[j],Z[r])]
        r+=1
        if r==len(Z):break
    return r
def incidence(E,V):return [[int(i in S) for i in V] for S in E]

maskchecks=0
H={(0,):2,(1,):1,(0,1):3,(0,2):2,(0,1,2):4}
for x in product([F(1,5),F(1,3),F(2,3)],repeat=3):
    for S,n in H.items():
        assert contrast(H,S,x)==(1-prod((x[i] for i in S),start=F(1)))**n
        assert P(H,S,x)==prod((x[i] for i in S),start=F(1));maskchecks+=1
save('raw_mask_product_extraction_with_background',maskchecks)

gauge_cases=[({(0,1):2,(0,2):3},[F(6,5),F(5,6),F(5,6)]),
             ({(0,1):2,(0,1,2):3,(2,):4},[F(6,5),F(5,6),F(1)]),
             ({(0,1):1,(1,2):2,(2,3):3,(0,3):4},[F(6,5),F(5,6),F(6,5),F(5,6)])]
raw=0
for H,c in gauge_cases:
    r=len(c);base=[F(i+2,10) for i in range(r)]
    levels=[[F(0),a,3*a/2] for a in base]
    assert all(c[i]*levels[i][-1]<1 for i in range(r))
    for S in H:assert prod((c[i] for i in S),start=F(1))==1
    for x in product(*levels):
        xx=[c[i]*x[i] for i in range(r)]
        assert Q(H,x)==Q(H,xx);raw+=1
    for i in range(r):
        knots=[(F(0),F(0)),(F(1,3),c[i]*base[i]),(F(2,3),c[i]*3*base[i]/2),(F(1),F(1))]
        assert all(x1<x2 and y1<y2 for (x1,y1),(x2,y2) in zip(knots,knots[1:]))
save('complete_interior_zero_grid_gauge_and_homeomorphic_extension',raw)

E=[(0,1),(0,2),(1,2)];u=[F(1,5),F(1,3),F(2,5)];ps=[prod(u[i] for i in S) for S in E]
assert rank(incidence(E,range(3)))==3
for i in range(3):
    others=[j for j in range(3) if j!=i]
    byedge={S:p for S,p in zip(E,ps)}
    rec=rational_root(byedge[tuple(sorted((i,others[0])))]*byedge[tuple(sorted((i,others[1])))]/byedge[tuple(others)],2)
    assert rec==u[i]
save('triangle_without_unary_anchors',{'base':u,'products':ps})

A=incidence([(0,1),(0,1,2)],range(3));rr=rank(A)
flags=[rank(A+[[int(j==i) for j in range(3)]])==rr for i in range(3)]
assert flags==[False,False,True]
save('partial_identification_AB_ABC',flags)

graphs=0
for n in range(2,6):
    edges=list(combinations(range(n),2))
    for bits in product([0,1],repeat=len(edges)):
        E=[S for S,b in zip(edges,bits) if b];V=sorted(set(i for S in E for i in S))
        A=incidence(E,V);seen={};biparts=[]
        for root in V:
            if root in seen:continue
            seen[root]=0;todo=[root];vertices=[];ok=True
            while todo:
                i=todo.pop();vertices.append(i)
                for S in E:
                    if i not in S:continue
                    j=S[1] if S[0]==i else S[0]
                    if j not in seen:seen[j]=1-seen[i];todo.append(j)
                    elif seen[j]==seen[i]:ok=False
            if ok:biparts.append(vertices)
        assert len(V)-rank(A)==len(biparts)
        anchors=[[int(i==comp[0]) for i in V] for comp in biparts]
        assert rank(A+anchors)==len(V);graphs+=1
save('unsigned_graph_bipartite_and_odd_cycle_criterion',graphs)

A=incidence([(0,1),(0,2)],range(3));v=[1,-1,-1]
assert all(sum(a*b for a,b in zip(row,v))==0 for row in A) and sum(v)!=0
assert rank(A)==2 and rank(A+[[1,1,1]])==3
assert rank(incidence(list(combinations(range(4),3)),range(4)))==4
save('false_probability_mass_row_and_higher_hyperedges',True)

def interpolate(knots,x):
    for (a,p),(b,q) in zip(knots,knots[1:]):
        if a<=x<=b:return p+(q-p)*(x-a)/(b-a)
    raise ValueError(x)
identity=[(F(0),F(0)),(F(1),F(1))]
changed=[(F(0),F(0)),(F(1,3),F(1,3)),(F(1,2),F(11,20)),(F(2,3),F(2,3)),(F(1),F(1))]
H={(0,1):1,(0,2):1,(1,2):1}
for x in product([F(0),F(1,3),F(2,3)],repeat=3):
    xx=[interpolate(changed,x[0]),x[1],x[2]]
    assert Q(H,x)==Q(H,xx)
x=[F(1,2),F(1,3),F(1,3)];xx=[F(11,20),x[1],x[2]]
assert Q(H,x)!=Q(H,xx)
save('full_rank_does_not_determine_unsampled_values',True)

def root_interval(z,d,bits):
    lo,hi=F(0),F(1)
    for _ in range(bits):
        mid=(lo+hi)/2
        if mid**d==z:return mid,mid
        if mid**d<z:lo=mid
        else:hi=mid
    return lo,hi
sign_calls=0;maxbits=0
def unary_sign(Z1,Z2,rho,k):
    global sign_calls,maxbits
    bits=8
    while bits<=512:
        a,b=root_interval(Z1*Z1,2*k+1,bits);c,d=root_interval(Z2*Z2,2*k+1,bits)
        lo=(1-d)-rho*(1-a);hi=(1-c)-rho*(1-b)
        if lo>0 or hi<0:
            sign_calls+=1;maxbits=max(maxbits,bits);return 1 if lo>0 else -1
        bits*=2
    raise RuntimeError('finite control cap inconclusive')
def recover_unary(Z1,Z2,rho):
    hi=1
    while unary_sign(Z1,Z2,rho,hi)<0:hi*=2
    lo=1
    while lo<hi:
        k=(lo+hi)//2
        if unary_sign(Z1,Z2,rho,k)>0:hi=k
        else:lo=k+1
    return lo
recoveries=[]
for n in [1,2,3,7,15]:
    for a1,a2 in [(F(1,5),F(2,5)),(F(1,3),F(3,4)),(F(1,8),F(1,2))]:
        Z1=(1-a1)**n;Z2=(1-a2)**n;rho=a2/a1
        assert recover_unary(Z1,Z2,rho)==n
        assert 1-rational_root(Z1,n)==a1
        recoveries.append({'n':n,'a1':a1,'a2':a2})
save('positive_unary_half_integer_interval_search',{'recoveries':len(recoveries),'certified_sign_calls':sign_calls,'max_bits':maxbits})
for k,bits in product([0,1,3],[8,16,32]):
    a,b=root_interval(F(1),2*k+1,bits)
    lo=(1-b)-2*(1-a);hi=(1-a)-2*(1-b)
    assert lo<=0<=hi
save('zero_count_stalls_this_cut_without_claiming_absence_impossibility',True)

H={(1,):2,(2,):1,(0,1):4,(0,2):2,(1,2):4,(0,1,2):3}
assert Q(H,[F(1),F(0),F(0)])==1
reduced={}
for S,n in H.items():
    T=tuple(i for i in S if i!=0)
    assert T
    reduced[T]=reduced.get(T,0)+n
assert reduced[(1,2)]==7
bc=0
for b,c in product([F(0),F(1,4),F(1,2)],[F(0),F(1,5),F(2,5)]):
    assert Q(H,[F(1),b,c])==Q(reduced,[F(0),b,c]);bc+=1
for a in [F(1,3),F(2,3)]:
    x=[a,F(1,4),F(1,5)]
    Pfull=P(H,(0,1,2),x)
    Ered=contrast(H,(1,2),x,{0:F(1)})
    Pred=1-rational_root(Ered,7)
    assert Pfull/Pred==a
save('boundary_reduced_inventory_and_triple_point_reconstruction',{'grid_equalities':bc,'original_count':3,'aggregate_count':7})

H={(0,):5,(0,1):3};a1,a2=F(1,5),F(2,5);b=F(1,3)
rho=P(H,(0,1),[a2,b])/P(H,(0,1),[a1,b])
nA=recover_unary(Q(H,[a1,F(0)]),Q(H,[a2,F(0)]),rho)
assert nA==5 and Q(H,[F(1),F(0)])==0 and Q(H,[F(0),F(1)])==1
agg=nA+H[(0,1)]
for aa in [a1,a2]:
    red=Q(H,[aa,F(1)]);Pa=1-rational_root(red,agg)
    assert P(H,(0,1),[aa,b])/Pa==b
try:contrast(H,(1,),[a1,b],{0:F(1)})
except ValueError:pass
else:raise AssertionError('unary-saturated raw boundary contrast accepted')
save('boundary_pair_with_unary_neighbor_and_saturation_guard',{'unary_count':nA,'reduced_count':agg})

def floor(q):return q.numerator//q.denominator
uniform=[]
for power,eps in product([1,2,7],[F(1,8),F(1,32)]):
    bits=0
    while F(1,2**bits)>eps/8:bits+=1
    den=2**bits;calls=0
    for m in range(1,15):
        N=2**m;lower=[];upper=[]
        for j in range(N+1):
            val=F(j,N)**power;calls+=1
            if j in [0,N]:l=h=val
            else:l=F(floor(val*den),den);h=min(F(1),l+F(1,den))
            assert l<=val<=h and h-l<=eps/8
            lower.append(l);upper.append(h)
        span=max(upper[j+1]-lower[j] for j in range(N))
        if span<eps/2:break
    else:raise RuntimeError('uniform-approximation control cap inconclusive')
    aa=[];mx=F(0)
    for l in lower:mx=max(mx,l);aa.append(mx)
    gg=[(1-eps/4)*v+(eps/4)*F(j,N) for j,v in enumerate(aa)]
    assert gg[0]==0 and gg[-1]==1 and all(a<b for a,b in zip(gg,gg[1:]))
    assert span+eps/4<eps
    for j in range(N):
        for h in range(5):
            z=F(h,4);x=F(j,N)+z/N;g=(1-z)*gg[j]+z*gg[j+1]
            assert abs(g-x**power)<eps
    uniform.append({'power':power,'epsilon':eps,'mesh':N,'point_calls':calls,'max_cell_enclosure_span':span})
save('all_command_point_oracle_uniform_polygonal_controls',uniform)

def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v) for v in x]
    return x
(HERE/'results').mkdir(exist_ok=True)
(HERE/'results'/'exact_controls.json').write_text(json.dumps(enc({'families_passed':len(results),'controls':results}),indent=2)+'\n')
print('ALL',len(results),'EXACT CONTROL FAMILIES PASS')
