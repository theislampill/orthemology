#!/usr/bin/env python3
"""Independent exact finite controls; no imports from the reviewed implementation.
Writes only inside this review directory. Universal claims rely on written proofs.
"""
from fractions import Fraction as Q
from itertools import product, combinations, permutations
from pathlib import Path
import json, hashlib, sys, platform
HERE=Path(__file__).resolve().parent
checks=[]
def record(name,**detail): checks.append(dict(name=name,status='PASS',detail=detail))
def rref(rows,n):
    a=[[Q(x) for x in row] for row in rows]; piv=[]; k=0
    for c in range(n):
        t=next((t for t in range(k,len(a)) if a[t][c]),None)
        if t is None: continue
        a[k],a[t]=a[t],a[k]; z=a[k][c];a[k]=[x/z for x in a[k]]
        for t in range(len(a)):
            if t!=k:
                z=a[t][c]
                if z:a[t]=[x-z*y for x,y in zip(a[t],a[k])]
        piv.append(c);k+=1
        if k==len(a):break
    return a,tuple(piv)
def rank(rows,n):return len(rref(rows,n)[1])
def dot(a,b):return sum((x*y for x,y in zip(a,b)),Q(0))
def in_kernel(H,p):return all(dot(row,p)==0 for row in H)
def normalise(p):
    z=sum(p,Q(0));assert z>0
    return tuple(x/z for x in p)
def bayes(p,L):return normalise(tuple(x*y for x,y in zip(p,L)))
def vertices(H,n):
    # Basic feasible solutions of [1; H]x=(1,0,...,0), independently via
    # augmented Gaussian elimination rather than the reviewed SymPy routine.
    rows=[[Q(1)]*n]+[list(map(Q,row)) for row in H]; target=[Q(1)]+[Q(0)]*len(H);out=set()
    for size in range(1,min(n,rank(rows,n))+1):
        for J in combinations(range(n),size):
            aug=[[row[j] for j in J]+[b] for row,b in zip(rows,target)]
            R,P=rref(aug,size)
            if len(P)!=size or any(all(x==0 for x in row[:size]) and row[-1]!=0 for row in R):continue
            x=[Q(0)]*size
            for k,pivot in enumerate(P):x[pivot]=R[k][-1]
            if any(z<0 for z in x):continue
            v=[Q(0)]*n
            for j,z in zip(J,x):v[j]=z
            out.add(tuple(v))
    return sorted(out)
def components(H,n):
    R,P=rref(H,n);parent=list(range(n));free=set(range(n))-set(P)
    def find(i):
        while parent[i]!=i:i=parent[i]
        return i
    for k,p in enumerate(P):
        for j in free:
            if R[k][j]:parent[find(j)]=find(p)
    return tuple(sorted(tuple(i for i in range(n) if find(i)==a) for a in set(find(i) for i in range(n))))
def rank_accept(H,L,S):
    rows=[[Q(row[i]) for i in S] for row in H]
    transformed=[[Q(row[i])*L[i] for i in S] for row in H]
    return rank(rows+transformed,len(S))==rank(rows,len(S))
def graph_accept(H,L,S):
    comp=components([[row[i] for i in S] for row in H],len(S))
    return all(len({L[S[i]] for i in block})==1 for block in comp)
def certify_family(H,n,weights=(1,2,3)):
    V=vertices(H,n)
    if not V:return None
    S=tuple(i for i in range(n) if any(v[i]>0 for v in V));p=tuple(sum(v[i] for v in V)/len(V) for i in range(n))
    assert all(p[i]>0 for i in S) and in_kernel(H,p)
    accepted=0; instances=0
    for L in product(map(Q,weights),repeat=n):
        vertex=all(in_kernel(H,bayes(v,L)) for v in V)
        assert vertex==rank_accept(H,L,S)==graph_accept(H,L,S),(H,L,S)
        if vertex:
            assert all(in_kernel(H,bayes(v,tuple(1/x for x in L))) for v in V)
            assert bayes(bayes(p,L),tuple(1/x for x in L))==p
            accepted+=1
        instances+=1
    return instances,accepted,S,len(V)

# Different implementation of combinatorial face classification over n=1..4.
family_stats=[]
for n in range(1,5):
    supports=tuple(frozenset(i for i in range(n) if mask&(1<<i)) for mask in range(1,1<<n))
    totals=closed=convex=faces=0
    for bits in range(1,1<<len(supports)):
        F={S for i,S in enumerate(supports) if bits&(1<<i)};totals+=1
        is_closed=all(T in F for S in F for T in supports if T<=S)
        is_convex=all(S|T in F for S in F for T in F)
        maximal=frozenset().union(*F)
        is_face=F=={T for T in supports if T<=maximal}
        assert (is_closed and is_convex)==is_face
        closed+=is_closed;convex+=is_convex;faces+=is_face
    family_stats.append(dict(n=n,families=totals,closed=closed,convex=convex,faces=faces))
record('support family controls through four states',enumerations=family_stats)

# All ordered pairs of {-1,0,1} rows in dimension 3, plus every such row in dimension 4.
stats=[]
for n,count_rows in ((3,2),(4,1)):
    rowset=tuple(product((-1,0,1),repeat=n));num=feasible=instances=accepted=0;spaces=set();supports=set()
    for H in product(rowset,repeat=count_rows):
        num+=1;result=certify_family(H,n)
        if result is None:continue
        feasible+=1;i,a,S,v=result;instances+=i;accepted+=a;supports.add(S)
        R,P=rref(H,n);spaces.add(tuple(tuple(row) for row in R[:len(P)]))
    stats.append(dict(n=n,rows=count_rows,presentations=num,feasible_presentations=feasible,distinct_row_spaces=len(spaces),likelihood_instances=instances,accepted=accepted,supports=len(supports)))
record('independent vertex rank component and inverse agreement',enumerations=stats,arithmetic='fractions.Fraction; independently implemented Gaussian elimination')

# Nonzero affine right sides, multiple components, forced zeros, redundant rows.
cases=[
 ('full simplex',[],5),
 ('two linked pairs and isolated coordinate',[[1,-2,0,0,0],[0,0,2,-3,0]],5),
 ('forced coordinate plus linked pair',[[0,0,0,1,1],[1,-1,0,0,0]],5),
 ('fixed positive law',[[2,-1,0,0],[3,0,-1,0],[4,0,0,-1]],4),
 ('fixed block masses',[[2,2,-3,-3]],4),
 ('redundant constraints',[[1,-2,0,0],[0,0,1,-3],[2,-4,1,-3],[0,0,0,0]],4),
 ('one state',[[0],[0]],1),
]
case_results=[]
for name,H,n in cases:
    got=certify_family(H,n,weights=(Q(1,2),Q(1),Q(2)));assert got
    instances,accepted,S,vcount=got
    # Arbitrary nonzero b rows: A=H+b1^T gives the same homogenized family.
    b=[Q(k+2,k+3) for k in range(len(H))]
    A=[[Q(x)+z for x in row] for row,z in zip(H,b)]
    assert [[a-z for a in row] for row,z in zip(A,b)]==[[Q(x) for x in row] for row in H]
    for v in vertices(H,n):assert all(dot(row,v)==z for row,z in zip(A,b))
    case_results.append(dict(name=name,support=list(S),vertices=vcount,instances=instances,accepted=accepted,components=[list(c) for c in components([[row[i] for i in S] for row in H],len(S))]))
record('support degenerate redundant and affine representation cases',cases=case_results)

# Pivot choice is induced by coordinate order. Check every order of two n=5 systems.
pivot_cases=[([[1,-2,0,0,0],[0,0,2,-3,0]],5),([[1,1,-2,0,0],[0,1,1,-2,0]],5)]
permutation_count=0;rowop_count=0
for H,n in pivot_cases:
    original={frozenset(block) for block in components(H,n)}
    for perm in permutations(range(n)):
        Hp=[[row[i] for i in perm] for row in H]
        lifted={frozenset(perm[i] for i in block) for block in components(Hp,n)}
        assert lifted==original;permutation_count+=1
    transformed=[H[1],H[0],tuple(2*x-3*y for x,y in zip(H[0],H[1])),(0,)*n]
    assert {frozenset(c) for c in components(transformed,n)}==original;rowop_count+=1
record('intrinsic component partition controls',coordinate_orders=permutation_count,redundant_row_basis_changes=rowop_count)

# Exhaust binary positive channels with entries in {1/4,1/2,3/4}.
H=[[1,-1,0,0],[0,0,1,-1]];n=4;V=vertices(H,n);comp=components(H,n);channel_count=passing=0
for plus in product((Q(1,4),Q(1,2),Q(3,4)),repeat=n):
    minus=tuple(1-x for x in plus); assert all(x>0 for x in plus+minus)
    factored=all(len({plus[i] for i in c})==1 for c in comp)
    preserved=all(in_kernel(H,bayes(v,L)) for v in V for L in (plus,minus))
    assert preserved==factored
    channel_count+=1;passing+=preserved
# Adaptive two-step sequence changes channel according to first outcome.
p=(Q(1,8),Q(1,8),Q(3,8),Q(3,8));first=(Q(3,4),Q(3,4),Q(1,4),Q(1,4));histories=[]
for y,L1 in enumerate((first,tuple(1-x for x in first))):
    nextplus=(Q(2,3),Q(2,3),Q(1,3),Q(1,3)) if y==0 else (Q(1,5),Q(1,5),Q(4,5),Q(4,5))
    for z,L2 in enumerate((nextplus,tuple(1-x for x in nextplus))):
        post=bayes(bayes(p,L1),L2);assert in_kernel(H,post)
        assert post[0]/post[1]==p[0]/p[1] and post[2]/post[3]==p[2]/p[3]
        histories.append({'history':[y,z],'posterior':list(map(str,post))})
record('channel factorization and adaptive odds',binary_channels=channel_count,globally_preserving=passing,adaptive_histories=histories)

# Fixed-block update and exact KKT ratio. Positive r and weights make the
# constrained candidate positive; q_i/r_i is constant per block, hence the
# KL gradient is constant per block. Strict convexity supplies uniqueness.
def project(r,blocks,w):
    out=[Q(0)]*len(r)
    for I,wa in zip(blocks,w):
        z=sum(r[i] for i in I);assert z>0
        for i in I:out[i]=wa*r[i]/z
    return tuple(out)
def U(p,L,blocks,w):return project(bayes(p,L),blocks,w)
blocks=((0,1),(2,3,4));w=(Q(2,5),Q(3,5));p=(Q(1,10),Q(3,10),Q(1,10),Q(1,5),Q(3,10))
L=(Q(1),Q(2),Q(3),Q(4),Q(5));M=(Q(5),Q(4),Q(3),Q(2),Q(1));r=bayes(p,L);q=project(r,blocks,w)
for I,wa in zip(blocks,w):
    assert sum(q[i] for i in I)==wa
    assert len({q[i]/r[i] for i in I})==1
assert U(U(p,M,blocks,w),L,blocks,w)==U(p,tuple(a*b for a,b in zip(L,M)),blocks,w)
assert U(p,(Q(1),)*5,blocks,w)==p
assert U(U(p,L,blocks,w),tuple(1/x for x in L),blocks,w)==p
assert U(p,tuple(13*x for x in L),blocks,w)==U(p,L,blocks,w)
assert U(p,(Q(7),Q(7),Q(2),Q(2),Q(2)),blocks,w)==p
record('KL fixed block stationarity composition inverse and block gauge',projected_report=list(map(str,q)),block_weights=list(map(str,w)))

# Conditional and joint risk accounting from the joint distribution directly.
p=(Q(1,2),Q(1,4),Q(1,4));K=((Q(3,4),Q(1,4),Q(1,4)),(Q(1,4),Q(3,4),Q(3,4)))
blocks=((0,),(1,2));w=(Q(1,2),Q(1,2));posts=[bayes(p,L) for L in K]
def loss(i,q):return sum(((Q(i==j)-x)**2 for j,x in enumerate(q)),Q(0))/2
prior_risk=sum(p[i]*loss(i,p) for i in range(3))
true_risk=sum(p[i]*K[y][i]*loss(i,posts[y]) for i in range(3) for y in range(2))
repair_risk=sum(p[i]*K[y][i]*loss(i,U(p,K[y],blocks,w)) for i in range(3) for y in range(2))
assert (prior_risk,true_risk,repair_risk)==(Q(5,16),Q(17,64),Q(5,16))
assert all(U(p,L,blocks,w)==p for L in K)
assert bayes(posts[0],K[0])==(Q(9,10),Q(1,20),Q(1,20))
# Every length-4 observation string: conventional posterior tracks count;
# repaired state remains exactly fixed, even though composition still holds.
for ys in product(range(2),repeat=4):
    raw=p;repaired=p;combined=(Q(1),)*3
    for y in ys:
        raw=bayes(raw,K[y]);repaired=U(repaired,K[y],blocks,w);combined=tuple(a*b for a,b in zip(combined,K[y]))
    assert raw==bayes(p,combined) and repaired==p==U(p,combined,blocks,w)
record('fixed channel direct joint risk and repeated loss',prior_risk=str(prior_risk),Bayes_risk=str(true_risk),repair_risk=str(repair_risk),regret=str(repair_risk-true_risk),four_observation_histories=16)

# Current-prior membership and inverse use are not global or current-state invariants.
H=[[Q(1,2),-Q(1,2),-Q(1,2)]];L=(Q(1,2),Q(1,4),Q(3,4));Lm=tuple(1-x for x in L)
assert all(in_kernel(H,bayes(p,x)) for x in (L,Lm))
assert not rank_accept(H,L,(0,1,2))
assert bayes(bayes(p,L),L)==(Q(4,9),Q(1,18),Q(1,2))
assert not in_kernel(H,bayes(p,tuple(1/x for x in L)))
# But inverse at the reached posterior is exactly p, as required by Bayes itself.
assert bayes(bayes(p,L),tuple(1/x for x in L))==p
record('current prior all outcomes repeated update and inverse boundary',first_plus=list(map(str,bayes(p,L))),second_plus=list(map(str,bayes(bayes(p,L),L))),inverse_at_original=list(map(str,bayes(p,tuple(1/x for x in L)))))

# Support removal and malformed/empty families are outside Theorem 3's hypotheses.
assert vertices([[1,1]],2)==[]
assert bayes((Q(1,2),Q(1,2)),(Q(1),Q(0)))==(Q(1),Q(0))
try:bayes((Q(1),Q(0)),(Q(0),Q(1)))
except AssertionError:pass
else:raise AssertionError('undefined branch was accepted')
assert bayes((Q(1,2),Q(1,2)),(Q(2),Q(1)))==(Q(2,3),Q(1,3))
record('nonempty positive and equality family boundaries',empty_family_rejected=True,zero_mass_rejected=True,strict_forward_inclusion_inequality_example='p1 >= 1/2 maps onto p1 >= 2/3')

result={'status':'PASS','proof_status':'Exact finite controls only; no Lean or formal-kernel certification','runtime':{'python':sys.version,'platform':platform.platform()},'control_groups':len(checks),'checks':checks}
(HERE/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
