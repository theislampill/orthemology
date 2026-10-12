#!/usr/bin/env python3
"""Exact rational controls for audit/filter transport; no external dependencies."""
from fractions import Fraction as F
from itertools import product
from collections import deque
from pathlib import Path
import hashlib, json, random

ROOT=Path(__file__).resolve().parent
Q=lambda x:F(x)
def mat(A): return tuple(tuple(F(x) for x in row) for row in A)
def eye(n): return mat([[int(i==j) for j in range(n)] for i in range(n)])
def diag(xs): return mat([[x if i==j else 0 for j in range(len(xs))] for i,x in enumerate(xs)])
def transpose(A): return tuple(zip(*A))
def dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))
def mv(A,x): return tuple(dot(a,x) for a in A)
def rm(a,M): return tuple(dot(a,col) for col in transpose(M))
def mm(A,B): return tuple(rm(a,B) for a in A)
def kronvec(a,b): return tuple(x*y for x in a for y in b)
def kron(A,B): return tuple(tuple(x*y for x in ar for y in br) for ar in A for br in B)
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def rref(rows):
    if not rows:return ()
    A=[list(map(F,row)) for row in rows]; k=0
    for j in range(len(A[0])):
        p=next((i for i in range(k,len(A)) if A[i][j]),None)
        if p is None:continue
        A[k],A[p]=A[p],A[k]; t=A[k][j]; A[k]=[x/t for x in A[k]]
        for i in range(len(A)):
            if i!=k and A[i][j]:
                t=A[i][j]; A[i]=[x-t*y for x,y in zip(A[i],A[k])]
        k+=1
        if k==len(A):break
    return tuple(tuple(row) for row in A[:k])
def coords(row,B):
    piv=[next(i for i,x in enumerate(b) if x) for b in B]
    co=tuple(row[i] for i in piv)
    assert tuple(sum((co[j]*B[j][i] for j in range(len(B))),F(0)) for i in range(len(row)))==tuple(row)
    return co

def closure(initial,Ms):
    B=rref(initial); dims=[len(B)]
    while True:
        D=rref(list(B)+[rm(b,M) for M in Ms for b in B])
        if len(D)==len(B):
            assert D==B
            return B,dims
        B=D; dims.append(len(B))

def complete_basis(C,Ms):
    B,dims=closure([(F(1),)*len(C[0])]+list(C),Ms)
    Ts=[tuple(coords(rm(b,M),B) for b in B) for M in Ms]
    assert all(mm(B,M)==mm(T,B) for M,T in zip(Ms,Ts))
    return B,Ts,dims

def posterior(C,r):
    mass=sum(r)
    return None if not mass else tuple(x/mass for x in mv(C,r))
def normal(r):
    z=sum(r); return None if not z else tuple(x/z for x in r)
def words(m,h):
    yield ()
    for k in range(1,h+1):yield from product(range(m),repeat=k)
def run(r,Ms,w):
    for i in w:r=mv(Ms[i],r)
    return r

def support(r):return frozenset(i for i,x in enumerate(r) if x>0)
def supp_step(S,M):return frozenset(i for i,row in enumerate(M) if any(row[j]>0 for j in S))
def feasible_equal(r,s,Ms):
    init=(support(r),support(s)); queue=deque([(init,())]); seen={init}
    while queue:
        (R,S),w=queue.popleft()
        if bool(R)!=bool(S):return False,w,len(seen)
        for i,M in enumerate(Ms):
            pair=(supp_step(R,M),supp_step(S,M))
            if pair not in seen:seen.add(pair);queue.append((pair,w+(i,)))
    return True,None,len(seen)

def posterior_lift(C,Ms):
    n=len(C[0]); u=(F(1),)*n
    D=[sub(kronvec(c,u),kronvec(u,c)) for c in C]
    B,dims=closure(D,[kron(M,M) for M in Ms])
    assert len(B)<=n*(n-1)//2
    for b in B:
        assert all(b[i*n+j]==-b[j*n+i] for i in range(n) for j in range(n))
    return B,dims

def post_equiv(r,s,C,Ms):
    B,dims=posterior_lift(C,Ms)
    eq,w,visited=feasible_equal(r,s,Ms)
    residual=mv(B,kronvec(r,s))
    return eq and not any(residual),dict(lift_dimensions=dims,same_feasible_language=eq,support_witness=w,support_pairs=visited,residual=residual)

results={}
# The actual finite source model has one fixed verifier V and rereadable observations.
X=list(product(range(2),repeat=4)) # theta, T (0 Good/1 Bad), Y, V
prior=[]
for th,t,y,v in X:
    acc=F(9,10) if t==0 else F(1,2)
    prior.append(F(1,4)*(acc if y==th else 1-acc)*(F(4,5) if v==th else F(1,5)))
prior=tuple(prior); assert sum(prior)==1
C=mat([[int(th==k) for th,t,y,v in X] for k in range(2)])
Y=[diag([int(y==k) for th,t,y,v in X]) for k in range(2)]
As=list(product(range(2),repeat=2))
Ms=[diag([int((t,int(v!=y))==a) for th,t,y,v in X]) for a in As]
B,Ts,dims=complete_basis(C,Ms);assert len(B)==8
Bfull,_,dimsfull=complete_basis(C,Y+Ms);assert len(Bfull)==16
# Natural exact quotient: eight masses of (theta,T,D).
Z=list(product(range(2),repeat=3))
G=mat([[int((th,t,int(v!=y))==z) for th,t,y,v in X] for z in Z])
Ns=[diag([int((t,d)==a) for th,t,d in Z]) for a in As]
assert all(mm(G,M)==mm(N,G) for M,N in zip(Ms,Ns))
assert rref(G)==B
ry=[normal(mv(A,prior)) for A in Y]
assert posterior(C,ry[1])[1]==F(7,10)
full=mv(Ms[3],ry[1]);assert sum(full)==F(1,4) and posterior(C,full)[1]==F(1,5)
results['actual_source_model']={'latent_states':16,'audit_only_closure_dimensions':dims,'report_and_audit_dimensions':dimsfull,'old_target_one':posterior(C,ry[1])[1],'bad_disagree_probability':sum(full),'correct_target_one':posterior(C,full)[1]}

# Condition on Bad and report y; target posterior and all next audit probabilities coincide.
bad=diag([int(t==1) for th,t,y,v in X])
r0,r1=[normal(mv(bad,r)) for r in ry]
assert posterior(C,r0)==posterior(C,r1)==(F(1,2),F(1,2))
assert tuple(sum(mv(M,r0)) for M in Ms)==tuple(sum(mv(M,r1)) for M in Ms)==(F(0),F(0),F(1,2),F(1,2))
assert posterior(C,mv(Ms[3],r0))[1]==F(4,5)
assert posterior(C,mv(Ms[3],r1))[1]==F(1,5)
# Four-state retained quotient (theta,D) on the known-Bad slice.
P=list(product(range(2),repeat=2))
H=mat([[int((th,int(v!=y))==p) for th,t,y,v in X] for p in P])
p0,p1=mv(H,r0),mv(H,r1)
C4=mat([[int(th==k) for th,d in P] for k in range(2)])
D=[diag([int(d==k) for th,d in P]) for k in range(2)]
B4,T4,d4=complete_basis(C4,D); assert len(B4)==4
assert p1==(F(1,10),F(2,5),F(2,5),F(1,10))
eq,details=post_equiv(p0,p1,C4,D); assert not eq and details['same_feasible_language']
# Same fixed audit may be reread; contradictory readings are impossible.
one=mv(D[1],p1);two=mv(D[1],one);wrong=mv(D[0],one)
assert one==two and sum(wrong)==0 and posterior(C4,wrong) is None
results['neutral_history_collision']={'joint_theta_D_after_Y1':p1,'current_target':posterior(C4,p1),'audit_probabilities':[sum(mv(m,p1)) for m in D],'posterior_D1_Y0':posterior(C4,mv(D[1],p0)),'posterior_D1_Y1':posterior(C4,one),'closure_dimensions':d4,'posterior_lift':details,'repeat_same_audit_unchanged':one==two,'contradictory_reread_impossible':sum(wrong)==0}

# Different experiment: each repeated D comes from a fresh conditionally independent verifier.
Fstates=list(product(range(2),repeat=2)) # theta,Y
rho=F(3,5)
fresh=[diag([(1+(-1)**(th+y+d)*rho)/2 for th,y in Fstates]) for d in range(2)]
Cf=mat([[int(th==k) for th,y in Fstates] for k in range(2)])
rf=tuple(F(int(y==1),2) for th,y in Fstates)
Bf,Tf,df=complete_basis(Cf,fresh);assert len(Bf)==4
fresh1=run(rf,fresh,(1,));fresh2=run(rf,fresh,(1,1))
assert posterior(Cf,fresh1)[1]==F(1,5) and posterior(Cf,fresh2)[1]==F(1,17)
_,_,neutral_dims=complete_basis(Cf,[diag([F(1,2)]*4)]*2);assert neutral_dims==[2]
results['fixed_vs_fresh_audit']={'fresh_dimensions':df,'zero_rho_dimensions':neutral_dims,'one_fresh_target_one':posterior(Cf,fresh1)[1],'two_fresh_target_one':posterior(Cf,fresh2)[1],'fixed_reread_target_one':posterior(C4,two)[1]}

# Binary target and source are independent in both starting laws. Source-only
# likelihoods preserve the same nondegenerate target forever, but event rates differ.
f=(F(1,4),F(3,4),F(1,4),F(3,4))
source_only=[diag(f),diag([1-x for x in f])]
Ct=mat([[1,1,0,0],[0,0,1,1]])
a=(F(3,8),F(1,8),F(3,8),F(1,8));b=(F(1,8),F(3,8),F(1,8),F(3,8))
eq,details=post_equiv(a,b,Ct,source_only);assert eq
Br,Tr,dr=complete_basis(Ct,source_only);assert mv(Br,a)!=mv(Br,b)
assert sum(mv(source_only[0],a))==F(3,8) and sum(mv(source_only[0],b))==F(5,8)
for w in words(2,6):assert posterior(Ct,run(a,source_only,w))==posterior(Ct,run(b,source_only,w))==(F(1,2),F(1,2))
results['posterior_only_strictness']={'equivalent':eq,'details':details,'full_predictive_dimensions':dr,'event_probabilities':[sum(mv(source_only[0],a)),sum(mv(source_only[0],b))]}

# Tensor cross-products alone silently pass a feasible-versus-impossible mismatch.
selectors=[diag([1,0,1,0]),diag([0,1,0,1])]
a=(F(1),F(0),F(0),F(0));b=(F(0),F(1),F(0),F(0))
K,kdims=posterior_lift(Ct,selectors)
assert not any(mv(K,kronvec(a,b)))
eq,details=post_equiv(a,b,Ct,selectors);assert not eq and not details['same_feasible_language']
w=details['support_witness'];assert bool(sum(run(a,selectors,w)))!=bool(sum(run(b,selectors,w)))
results['zero_branch_guard']={'bilinear_test_alone_passes':True,'guarded_equivalence':eq,'details':details}

# Complete binary fixed-audit quotient: signature versus paired tensor test.
raws=set()
for v in product(range(3),repeat=4):
    if sum(v):raws.add(normal(tuple(F(x) for x in v)))
K,_=posterior_lift(C4,D)
def signature(v):
    return (posterior(C4,v),posterior(C4,mv(D[0],v)),posterior(C4,mv(D[1],v)))
classification_pairs=0;collapsed_distinct=0
for x,y in product(raws,repeat=2):
    lifted=feasible_equal(x,y,D)[0] and not any(mv(K,kronvec(x,y)))
    assert lifted==(signature(x)==signature(y))
    if lifted and x!=y:
        assert signature(x)[1]==signature(x)[2]==signature(x)[0]
        collapsed_distinct+=1
    for v in (x,y):
        t=sum(mv(D[1],v));q=posterior(C4,v)[1]
        if 0<t<1:
            q0=posterior(C4,mv(D[0],v))[1];q1=posterior(C4,mv(D[1],v))[1]
            if q0!=q1:assert t==(q-q0)/(q1-q0)
            else:assert q==q0
    classification_pairs+=1
results['fixed_audit_posterior_quotient']={'distinct_normalized_laws':len(raws),'ordered_pairs':classification_pairs,'equivalent_distinct_ordered_pairs':collapsed_distinct,'classes':len(set(signature(v) for v in raws))}

# The admissible cone cannot be replaced by the ambient coordinate space.
Walsh=mat([[1]*4,[(-1)**th for th,d in P],[(-1)**d for th,d in P],[(-1)**(th+d) for th,d in P]])
zbad=(F(1),F(0),F(0),F(2))
signed=tuple(x/4 for x in mv(transpose(Walsh),zbad))
assert any(x<0 for x in signed) and sum(signed)==1
badq=posterior(C4,mv(D[0],signed));assert badq[1]==F(-1,2)
results['cone_guard']={'invalid_moments':zbad,'reconstructed_signed_law':signed,'invalid_posterior':badq}

# Exact randomized controls validate algebra/normalisation and tensor identities.
rng=random.Random(20261010);counts={'models':0,'predictive_updates':0,'word_pair_checks':0,'tensor_pair_checks':0}
for n in range(2,5):
  for trial in range(12):
    # One two-outcome instrument, with jointly column-stochastic transition weights.
    raw=[[[rng.randrange(4) for j in range(n)] for i in range(n)] for k in range(2)]
    den=[sum(raw[k][i][j] for k in range(2) for i in range(n)) for j in range(n)]
    for j,d in enumerate(den):
      if not d:raw[0][0][j]=1;den[j]=1
    mats=[mat([[F(raw[k][i][j],den[j]) for j in range(n)] for i in range(n)]) for k in range(2)]
    CC=mat([[int(i%2==k) for i in range(n)] for k in range(2)])
    B,T,dim=complete_basis(CC,mats);L=[coords(c,B) for c in CC];mass=coords((F(1),)*n,B)
    K,kd=posterior_lift(CC,mats)
    x=normal(tuple(F(rng.randrange(1,6)) for _ in range(n)))
    y=normal(tuple(F(rng.randrange(1,6)) for _ in range(n)))
    assert feasible_equal(x,y,mats)[0]
    for w in words(2,n*(n-1)//2):
      xx,yy=run(x,mats,w),run(y,mats,w)
      zx=mv(B,x)
      for k in w:zx=mv(T[k],zx)
      assert zx==mv(B,xx)
      assert dot(mass,zx)==sum(xx)
      if sum(xx):assert tuple(dot(l,zx)/dot(mass,zx) for l in L)==posterior(CC,xx)
      for c in CC:
        dd=sub(kronvec(c,(F(1),)*n),kronvec((F(1),)*n,c))
        assert dot(dd,kronvec(xx,yy))==dot(c,xx)*sum(yy)-sum(xx)*dot(c,yy)
      counts['predictive_updates']+=len(w);counts['word_pair_checks']+=1
    liftzero=not any(mv(K,kronvec(x,y)))
    direct=all(posterior(CC,run(x,mats,w))==posterior(CC,run(y,mats,w)) for w in words(2,n*(n-1)//2))
    assert liftzero==direct
    # Projective equality, including absolute-mass distinction.
    assert post_equiv(x,tuple(3*v for v in x),CC,mats)[0]
    counts['models']+=1;counts['tensor_pair_checks']+=1
results['exact_seeded_controls']=counts

# Boundary support cases for all deterministic two-state, two-letter partial maps.
support_count=0
partial=[]
for outputs in product((-1,0,1),repeat=2):
    partial.append(mat([[int(outputs[j]==i) for j in range(2)] for i in range(2)]))
rs=[(F(1),F(0)),(F(0),F(1)),(F(1,2),F(1,2))]
for mats in product(partial,repeat=2):
  for x,y in product(rs,repeat=2):
    equal,w,visited=feasible_equal(x,y,mats)
    assert visited<=16
    if not equal:assert bool(sum(run(x,mats,w)))!=bool(sum(run(y,mats,w)))
    # Direct breadth-first matrix products with normalized live-state distributions.
    seen=set();queue=deque([(x,y)]); direct=True
    while queue:
      xx,yy=queue.popleft()
      if (xx,yy) in seen:continue
      seen.add((xx,yy))
      if bool(sum(xx))!=bool(sum(yy)):direct=False;break
      for M in mats:
        Xx,Yy=mv(M,xx),mv(M,yy)
        queue.append((normal(Xx) or (F(0),F(0)),normal(Yy) or (F(0),F(0))))
    assert equal==direct
    support_count+=1
results['support_language_controls']=support_count

binding=json.loads((ROOT/'INPUT_BINDINGS.json').read_text())
for item in binding['inputs']:
    data=(ROOT.parent/item['path']).read_bytes()
    assert hashlib.sha256(data).hexdigest()==item['sha256']
results['inherited_inputs_unchanged']=len(binding['inputs'])

def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,tuple):return [encode(y) for y in x]
    if isinstance(x,list):return [encode(y) for y in x]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    return x
text=json.dumps(encode(results),indent=2)+'\n'
(ROOT/'CONTROL_RESULTS.json').write_text(text)
print(text)
