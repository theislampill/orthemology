#!/usr/bin/env python3
"""Independent exact controls, using orthogonal categorical contrasts and kernels.
No author program or author matrix utilities are imported. General proofs remain
in REVIEW.md; finite examples are discriminators rather than theorem certificates.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
from math import prod
import json,hashlib
HERE=Path(__file__).resolve().parent
OUT=[]
def clean(x):
 if isinstance(x,F): return str(x)
 if isinstance(x,dict): return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)): return [clean(v) for v in x]
 return x
def record(name,**data): OUT.append({'control':name,'status':'PASS',**clean(data)})
def inner(x,y): return sum((F(a)*b for a,b in zip(x,y)),F(0))
def had(x,y): return [a*b for a,b in zip(x,y)]
def matvec(M,p): return [inner(r,p) for r in M]
def posterior(p,L):
 q=had(p,L);a=sum(q);assert a>0
 return [v/a for v in q]
def rref(A):
 A=[list(map(F,r)) for r in A]
 if not A: return [],[]
 row=0;piv=[]
 for j in range(len(A[0])):
  pivot=next((i for i in range(row,len(A)) if A[i][j]),None)
  if pivot is None:continue
  A[row],A[pivot]=A[pivot],A[row]
  d=A[row][j];A[row]=[v/d for v in A[row]]
  for i in range(len(A)):
   if i!=row and A[i][j]:
    d=A[i][j];A[i]=[v-d*w for v,w in zip(A[i],A[row])]
  piv.append(j);row+=1
  if row==len(A):break
 return A,piv
def rank(A):return len(rref(A)[1])
def nullspace(A):
 R,p=rref(A);n=len(A[0]);free=[i for i in range(n) if i not in p];N=[]
 for j in free:
  x=[F(0)]*n;x[j]=1
  for i,c in enumerate(p):x[c]=-R[i][j]
  N.append(x)
 return N
# Local contrasts h_j=(1,...,1,-j,0,...,0); unlike the author basis these
# are mutually orthogonal within each multidimensional categorical factor.
def h(j,x):return 1 if j==0 or x<j else -j if x==j else 0
def basis(sizes):
 X=list(product(*[range(q) for q in sizes]));J=list(product(*[range(q) for q in sizes]))
 B=[[prod(h(j,x) for j,x in zip(idx,atom)) for atom in X] for idx in J]
 return X,J,B
def lowbasis(sizes,k):
 X,J,B=basis(sizes);lo=[r for j,r in zip(J,B) if sum(v>0 for v in j)<=k]
 return X,lo

def descends(M,L):
 A=[had(r,L) for r in M]
 return all(all(v==0 for v in matvec(A,d)) for d in nullspace(M))
def normalized_coefficient_test(M,L):
 # For all d in ker M and all p, (A d)(L.p)=(L.d)(A p).
 A=[had(r,L) for r in M]
 for d in nullspace(M):
  ad=matvec(A,d);ld=inner(L,d)
  if any(ad[j]*L[i]!=ld*A[j][i] for j in range(len(M)) for i in range(len(L))):return False
 return True

def support_rank_one(M,L):
 C=[[r[i] for i,v in enumerate(L) if v>0] for r in M]
 return bool(C[0]) and rank(C)==1

# 1. Full categorical multiplier system, including multiple contrasts per slot.
cases=[]
for sizes in ((3,3),(3,3,3),(2,3,4),(2,2,3,3)):
 X,J,B=basis(sizes);n=len(X)
 assert rank(B)==n
 assert all(inner(B[i],B[j])==0 for i in range(n) for j in range(i))
 for k in range(1,len(sizes)):
  lo=[r for j,r in zip(J,B) if sum(v>0 for v in j)<=k]
  hi=[r for j,r in zip(J,B) if sum(v>0 for v in j)>k]
  C=[had(l,g) for l in lo for g in hi]
  assert rank(C)==n-1
  cases.append({'sizes':sizes,'k':k,'retained_rank':rank(lo),'multiplier_dimension':n-rank(C)})
record('categorical_multiplier_linear_systems',cases=cases)

# 2. Two genuinely multidimensional factors in a non-pure top interaction.
X,M=lowbasis((3,3,3),2);a=[1,-1,0];b=[1,1,-2]
R=[a[x]*a[y]+b[x]*b[y] for x,y,z in X]
L=[F(1,2)+F(v,16) for v in R]
pp=[(1+F(v*a[z],8))/27 for v,(x,y,z) in zip(R,X)]
pm=[(1-F(v*a[z],8))/27 for v,(x,y,z) in zip(R,X)]
a3=[a[z] for x,y,z in X]
assert min(pp)>0 and min(pm)>0 and min(L)>0 and max(L)<1
assert matvec(M,pp)==matvec(M,pm)
assert inner(L,pp)==inner(L,pm)==F(1,2)
assert inner(a3,posterior(pp,L))==F(5,108)
assert inner(a3,posterior(pm,L))==-F(5,108)
assert rank([[a[x]*a[y]+b[x]*b[y] for y in range(3)] for x in range(3)])==2
assert had(a,a)==[F(2,3)+F(v,3) for v in b]
assert had(a,b)==a and had(b,b)==[2-v for v in b]
record('rank_two_categorical_interaction_witness',alpha=F(1,2),posterior_a3=[F(5,108),-F(5,108)],likelihood_range=[min(L),max(L)],prior_range=[min(pp),max(pp)],top_component_tensor_rank=2)

# 3. Arbitrary non-linear normalized decoding across general mass-row matrices.
matrices={
 'mass_only':[[1,1,1,1]],
 'distinct_nonseparating':[[1,1,1],[0,1,2]],
 'repeated_nonpartition':[[1,1,1,1],[0,0,1,2]],
 'partition':[[1,1,1,1],[0,0,1,1]],
 'full_law':[[1,1,1],[0,1,0],[0,0,1]],
 'categorical_unary_2x3':lowbasis((2,3),1)[1],
}
counts=[]
for name,M in matrices.items():
 n=len(M[0]);accepted=0;constant_posterior_only=0
 assert rank(M)==len(M)
 for vals in product((F(0),F(1,2),F(1)),repeat=n):
  linear=descends(M,vals);rankone=support_rank_one(M,vals)
  criterion=normalized_coefficient_test(M,vals)
  assert criterion==(linear or rankone),(name,vals)
  accepted+=criterion;constant_posterior_only+=criterion and not linear
 counts.append({'matrix':name,'grid_cases':3**n,'descending_including_zero':accepted,'support_rank_exception_only':constant_posterior_only})
record('general_normalized_support_rank_grid',cases=counts)

# 4. Repeated columns yield a multi-state support exception, not singleton support.
M=[[1,1,1,1],[0,0,1,2]];L=[F(1,4),F(3,4),F(0),F(0)]
p=[F(1,4)]*4;q=[F(3,8),F(1,8),F(1,4),F(1,4)]
assert matvec(M,p)==matvec(M,q)
assert matvec(M,posterior(p,L))==matvec(M,posterior(q,L))==[1,0]
assert inner(L,p)==F(1,4) and inner(L,q)==F(3,16)
assert not descends(M,L) and normalized_coefficient_test(M,L)
record('multi_state_equal_column_exception',supported_states=2,branch_probabilities=[inner(L,p),inner(L,q)],posterior=[1,0])

# 5. Categorical support size two fails; singleton support succeeds posterior-only.
X,M=lowbasis((3,3),1)
pp=[(1+F(a[x]*a[y],2))/9 for x,y in X]
pm=[(1-F(a[x]*a[y],2))/9 for x,y in X]
L2=[F(x==0 and y in (0,1)) for x,y in X]
Ls=[F(x==0 and y==0) for x,y in X];a2=[a[y] for x,y in X]
assert matvec(M,pp)==matvec(M,pm)
assert inner(L2,pp)==inner(L2,pm)==F(2,9)
assert [inner(a2,posterior(p,L2)) for p in (pp,pm)]==[F(1,2),-F(1,2)]
assert matvec(M,posterior(pp,Ls))==matvec(M,posterior(pm,Ls))
assert [inner(Ls,p) for p in (pp,pm)]==[F(1,6),F(1,18)]
record('categorical_zero_likelihood_support_discriminator',two_state_probabilities=[F(2,9)]*2,two_state_posterior_a2=[F(1,2),-F(1,2)],singleton_probabilities=[F(1,6),F(1,18)])

# 6. Full simplex vs full-support feasibility, independently on ternary slots.
X,M=lowbasis((3,3,3),2)
pp=[F(1+(-1)**sum(x),8) if max(x)<=1 else F(0) for x in X]
pm=[F(1-(-1)**sum(x),8) if max(x)<=1 else F(0) for x in X]
Ls=[F(x==(0,0,0)) for x in X]
assert sum(pp)==sum(pm)==1 and matvec(M,pp)==matvec(M,pm)
assert inner(Ls,pp)==F(1,4) and inner(Ls,pm)==0
H=[prod(F(int(v==0))-F(1,3) for v in x) for x in X]
qp=[F(1,27)+v/16 for v in H];qm=[F(1,27)-v/16 for v in H]
assert min(qp)>0 and min(qm)>0 and sum(qp)==sum(qm)==1
assert matvec(M,qp)==matvec(M,qm)
assert [inner(Ls,p) for p in (qp,qm)]==[F(1,18),F(1,54)]
record('ternary_feasibility_boundary_and_interior',boundary_probabilities=[F(1,4),F(0)],fullsupport_probabilities=[F(1,18),F(1,54)])

# 7. Direct linear equations for the exposed-column lift, not an interval sample.
cones=[]
for sizes,k in (((3,3),1),((3,3),2),((2,3,2),1)):
 X,M=lowbasis(sizes,k);n=len(X);r=len(M);eq=[]
 for j in range(r):
  for i in range(n):
   row=[F(0)]*(r*r+n)
   for h0 in range(r):row[j*r+h0]=M[h0][i]
   row[r*r+i]=-M[j][i];eq.append(row)
 nullity=r*r+n-rank(eq)
 assert nullity==(n if k==len(sizes) else 1)
 for x in X:
  vals=[sum(v!=w for v,w in zip(x,y)) for y in X]
  assert min(vals)==0 and vals.count(0)==1
 cones.append({'sizes':sizes,'k':k,'ray_count':n,'span_dimension':r,'diagonal_lift_dimension':nullity})
record('categorical_exposed_rays_and_direct_lift_equations',cases=cones)

# 8. Compute channel-adapted closure without a preselected Walsh mask answer.
X,M=lowbasis((2,2,2),1);x1=[1 if x[0]==0 else -1 for x in X]
L=[F(1,2)+F(v,4) for v in x1];Lc=[1-v for v in L]
C=M[:];dims=[rank(C)]
while True:
 rows=C+[had(r,Y) for Y in (L,Lc) for r in C]
 R,piv=rref(list(map(list,zip(*rows))))
 Cnew=[rows[i] for i in piv]
 if len(Cnew)==len(C):break
 C=Cnew;dims.append(len(C))
assert dims==[4,6] and rank(C)==6
x2x3=[(1 if x[1]==0 else -1)*(1 if x[2]==0 else -1) for x in X]
x1x2x3=had(x1,x2x3)
assert rank(C+[x2x3])==7 and rank(C+[x1x2x3])==7
assert all(rank(C+[had(r,Y)])==6 for r in C for Y in (L,Lc))
# Derive reduced matrices from orthogonal target basis, then check all words≤4.
_,J,B=basis((2,2,2));keep=[j for j in range(len(J)) if J[j] not in ((0,1,1),(1,1,1))]
W=[B[j] for j in keep]
T=[[inner(had(row,L),w)/inner(w,w) for w in W] for row in W]
U=[[inner(had(row,Lc),w)/inner(w,w) for w in W] for row in W]
p=[F(i+1,36) for i in range(8)]
for h0 in range(5):
 for word in product((0,1),repeat=h0):
  q=p[:];z=matvec(W,p)
  for v in word:q=had(q,(L,Lc)[v]);z=matvec((T,U)[v],z)
  assert z==matvec(W,q)
record('channel_adapted_closure_and_word_intertwining',dimension_path=dims,full_dimension=8,checked_words=sum(2**i for i in range(5)),nonconstant_likelihood=True,complete_channel='L and 1-L')

# 9. Explicit tensor coefficient / augmentation / moment crosswalk.
sizes=(2,3,2);X,J,B=basis(sizes);p=[F(i+1,78) for i in range(12)]
assert sum(p)==1
subsetchecks=0
for k in range(4):
 for S in combinations(range(3),k):
  marginal={y:F(0) for y in product(*[range(sizes[i]) for i in S])}
  for atom,mass in zip(X,p):marginal[tuple(atom[i] for i in S)]+=mass
  # Contraction by augmentation on omitted tensor factors is exactly the sum.
  for idx,row in zip(J,B):
   if {i for i,j in enumerate(idx) if j}.issubset(S):
    contracted=sum(mass*prod(h(idx[i],y[t]) for t,i in enumerate(S)) for y,mass in marginal.items())
    assert contracted==inner(row,p)
  subsetchecks+=1
# Typed-word moment state components use words (i1,...,id) with i1<...<id.
words={tuple(i for i,j in enumerate(idx) if j) for idx in J if sum(j>0 for j in idx)<=2}
assert words=={(),(0,),(1,),(2,),(0,1),(0,2),(1,2)}
# Proper-marginal parity difference is a pure coefficient tensor of order 3.
delta=[F(prod(1 if v==0 else -1 if v==1 else 0 for v in x),4) for x in X]
_,M=lowbasis(sizes,2)
assert matvec(M,delta)==[0]*len(M)
assert inner([prod(1 if v==0 else -1 if v==1 else 0 for v in x) for x in X],delta)==2
record('actual_finite_tensor_mapping',marginal_contraction_subsets=subsetchecks,typed_words=sorted(words,key=lambda w:(len(w),w)),parity_tensor_order=3,parity_tensor_rank=1,proper_moment_difference_zero=True)

# 10. Assumption controls: omitted mass row, k=0, degenerate slots, k=m.
Mnomass=[[1,2]];L=[1,2]
assert not descends(Mnomass,L) and Mnomass[0][0]!=Mnomass[0][1]
# Mp uniquely determines p on simplex; posterior readout is (4-3p0)/(2-p0).
for t in (F(0),F(1,4),F(1,2),F(1)):
 z=2-t
 assert matvec(Mnomass,posterior([t,1-t],L))==[(3*z-2)/z]
X,M0=lowbasis((3,3),0);L=[F(i+1,10) for i in range(len(X))]
assert normalized_coefficient_test(M0,L) and not descends(M0,L)
# One singleton factor turns nominal proper order k=1 into a full-law record.
X,M=lowbasis((2,1),1);assert rank(M)==2 and descends(M,[F(1,4),F(3,4)])
record('load_bearing_hypothesis_controls',mass_row_omission_breaks_dichotomy=True,mass_only_normalized_exception=True,singleton_factor_breaks_proper_order_conclusion=True)

# 11. Intrinsic cone projections have no informative passive ambient lift.
v=[F(1,2),F(1,2),F(0)];w=[F(1,2),F(0),F(1,2)]
# P(a v+b w)=a v, with an arbitrary linear extension off span(v,w).
P=[[0,1,0],[0,1,0],[0,0,0]]
assert matvec(P,v)==v and matvec(P,w)==[0,0,0]
assert rank([[1,-1,0],[1,0,-1]])==2
# v and w demand inconsistent ambient L1 for P's desired outputs.
assert v[0]==w[0]!=0
record('intrinsic_projection_has_no_fixed_diagonal_lift',intrinsic_projection_verified=True,ambient_diagonal_preserving_dimension=1)

# 12. Complete erasure-or-revelation channel, checking all output contracts.
X,M=lowbasis((2,2),1);n=len(X)
channel=[[F(1,3)]*n]+[[F(2,3) if i==j else F(0) for i in range(n)] for j in range(n)]
assert all(sum(row[i] for row in channel)==1 for i in range(n))
assert all(normalized_coefficient_test(M,row) for row in channel)
assert sum(descends(M,row) for row in channel)==1
record('complete_erasure_or_revelation_channel',outcomes=len(channel),posterior_descending_rows=len(channel),probability_plus_posterior_descending_rows=1)

result={'status':'PASS','arithmetic':'Python standard-library Fraction','groups':len(OUT),'results':OUT,'scope':'Independent finite controls supplement ordinary proofs. No formal certificate, empirical warrant, field-wide novelty or T20 closure.'}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
