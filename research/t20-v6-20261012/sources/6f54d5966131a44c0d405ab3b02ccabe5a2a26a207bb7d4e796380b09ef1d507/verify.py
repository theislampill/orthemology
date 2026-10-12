#!/usr/bin/env python3
"""Small exact controls; the general statements are proved in RESULT.md."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def rank(rows):
    a=[list(map(Q,row)) for row in rows]
    if not a: return 0
    m,n=len(a),len(a[0]); r=0
    for c in range(n):
        j=next((j for j in range(r,m) if a[j][c]),None)
        if j is None: continue
        a[r],a[j]=a[j],a[r]
        q=a[r][c]; a[r]=[v/q for v in a[r]]
        for j in range(r+1,m):
            q=a[j][c]
            if q: a[j]=[x-q*y for x,y in zip(a[j],a[r])]
        r+=1
        if r==m: break
    return r

def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q(0))
def mv(a,v): return [dot(row,v) for row in a]
def times(a,b): return [x*y for x,y in zip(a,b)]
def norm(p):
    s=sum(p)
    assert s>0
    return [x/s for x in p]
def bayes(p,L): return norm(times(p,L))
def chi(mask,x):
    y=1
    for i,v in enumerate(x):
        if mask>>i&1: y*=v
    return y

def walsh(m,k):
    X=list(product((1,-1),repeat=m))
    masks=[s for s in range(1<<m) if s.bit_count()<=k]
    return X,masks,[[chi(s,x) for x in X] for s in masks]

def qstr(x):
    if isinstance(x,Q): return str(x)
    if isinstance(x,dict): return {str(k):qstr(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [qstr(v) for v in x]
    return x

out=[]
def record(name,**data): out.append({'control':name,'status':'PASS',**qstr(data)})

bindings=json.loads((HERE/'INPUT_BINDINGS.json').read_text())
for item in bindings['local_inputs']:
    b=(ROOT/item['path']).read_bytes()
    assert len(b)==item['bytes'],item['path']
    assert hashlib.sha256(b).hexdigest()==item['sha256'],item['path']
record('inherited_input_hashes',count=len(bindings['local_inputs']))

counts=[]
for m in (2,3,4):
    X,_,W=walsh(m,m); n=len(X)
    for i,row in enumerate(W):
        for j,row2 in enumerate(W): assert dot(row,row2)==(n if i==j else 0)
    for k in range(1,m):
        _,low,M=walsh(m,k)
        high=[s for s in range(n) if s.bit_count()>k]
        constraints=[[chi(t,x)*chi(u,x) for x in X] for t in low for u in high]
        assert rank(constraints)==n-1
        counts.append({'m':m,'k':k,'moment_rank':rank(M),'multiplier_dimension':n-rank(constraints)})
record('walsh_basis_and_multiplier_ranks',cases=counts)

sizes=(2,3,2); X=list(product(*[range(q) for q in sizes]))
all_indices=list(product(*[range(q) for q in sizes]))
def categorical_row(idx):
    vals=[]
    for x in X:
        z=1
        for i,j in enumerate(idx):
            if j: z*=int(x[i]==j-1)-int(x[i]==sizes[i]-1)
        vals.append(z)
    return vals
rows={idx:categorical_row(idx) for idx in all_indices}
assert rank(list(rows.values()))==12
cases=[]
for k in (1,2):
    low=[idx for idx in all_indices if sum(j!=0 for j in idx)<=k]
    high=[idx for idx in all_indices if sum(j!=0 for j in idx)>k]
    assert all(dot(rows[i],rows[j])==0 for i in low for j in high)
    constraints=[times(rows[i],rows[j]) for i in low for j in high]
    assert rank(constraints)==11
    cases.append({'k':k,'retained_dimension':rank([rows[i] for i in low]),'multiplier_dimension':12-rank(constraints)})
record('categorical_2_by_3_by_2_extension',cases=cases)

X,masks,M=walsh(2,1)
pp=[Q(1,4)*(1+Q(1,2)*chi(3,x)) for x in X]
pm=[Q(1,4)*(1-Q(1,2)*chi(3,x)) for x in X]
L=[(1+Q(1,2)*x[0])/2 for x in X]
assert mv(M,pp)==mv(M,pm)==[1,0,0]
assert dot(L,pp)==dot(L,pm)==Q(1,2)
postp=mv(M,bayes(pp,L)); postm=mv(M,bayes(pm,L))
assert postp==[1,Q(1,2),Q(1,4)]
assert postm==[1,Q(1,2),-Q(1,4)]
record('positive_likelihood_same_probability_different_retained_posterior',prior_plus=pp,prior_minus=pm,branch_probability=Q(1,2),posterior_plus=postp,posterior_minus=postm)

X3,masks3,M3=walsh(3,2)
p3p=[Q(1,8)*(1+Q(1,2)*chi(7,x)) for x in X3]
p3m=[Q(1,8)*(1-Q(1,2)*chi(7,x)) for x in X3]
L3=[(1+Q(1,2)*x[0])/2 for x in X3]
assert mv(M3,p3p)==mv(M3,p3m)
assert dot(L3,p3p)==dot(L3,p3m)==Q(1,2)
post3p=mv(M3,bayes(p3p,L3)); post3m=mv(M3,bayes(p3m,L3))
assert post3p[masks3.index(6)]==Q(1,4)
assert post3m[masks3.index(6)]==-Q(1,4)
record('proper_order_two_missing_triple',posterior_23_plus=Q(1,4),posterior_23_minus=-Q(1,4))

Lhigh=[(1+Q(1,2)*chi(3,x))/2 for x in X]
assert dot(Lhigh,pp)==Q(5,8) and dot(Lhigh,pm)==Q(3,8)
record('hidden_high_degree_branch_probability',probability_plus=dot(Lhigh,pp),probability_minus=dot(Lhigh,pm))

Lsingle=[Q(1),Q(0),Q(0),Q(0)]
assert mv(M,bayes(pp,Lsingle))==mv(M,bayes(pm,Lsingle))==[1,1,1]
assert dot(Lsingle,pp)==Q(3,8) and dot(Lsingle,pm)==Q(1,8)
pboundaryp=[Q(1,4)*(1+chi(3,x)) for x in X]
pboundarym=[Q(1,4)*(1-chi(3,x)) for x in X]
assert mv(M,pboundaryp)==mv(M,pboundarym)
assert dot(Lsingle,pboundaryp)==Q(1,2) and dot(Lsingle,pboundarym)==0
record('singleton_posterior_exception_and_feasibility_boundary',fullsupport_probabilities=[Q(3,8),Q(1,8)],boundary_probabilities=[Q(1,2),Q(0)],retained_posterior=[1,1,1])

accepted=[]
d=[1,-1,-1,1]
for vals in product((Q(0),Q(1,2),Q(1)),repeat=4):
    a=mv(M,times(vals,d)); b=dot(vals,d)
    # Exact coefficient condition from a alpha(p)=b M D_L p.
    criterion=all(a[j]*vals[i]==b*M[j][i]*vals[i] for j in range(3) for i in range(4))
    classified=(len(set(vals))==1 or sum(v>0 for v in vals)==1)
    assert criterion==classified
    if criterion: accepted.append(vals)
assert len(accepted)==11
Mmass=[[1,1,1,1]]
assert mv(Mmass,bayes(pp,L))==mv(Mmass,bayes(pm,L))==[1]
Mrepeat=[[1,1,1],[0,0,1]]; Lrepeat=[Q(1,4),Q(3,4),Q(0)]
p=[Q(1,4),Q(1,4),Q(1,2)]; q=[Q(3,8),Q(1,8),Q(1,2)]
assert mv(Mrepeat,p)==mv(Mrepeat,q)
assert mv(Mrepeat,bayes(p,Lrepeat))==mv(Mrepeat,bayes(q,Lrepeat))==[1,0]
assert dot(Lrepeat,p)==Q(1,4) and dot(Lrepeat,q)==Q(3,16)
record('normalized_support_rank_dichotomy_controls',likelihood_grid_cases=81,descending_including_zero=11,repeated_column_probabilities=[Q(1,4),Q(3,16)],mass_only_rank=1)

mu1=Q(1,3); mu2=-Q(1,5); a=Q(1,2)
pind=[(1+mu1*x[0])*(1+mu2*x[1])/4 for x in X]
assert sum(pind)==1
assert mv(M,bayes(pind,L))==[1,Q(5,7),-Q(1,5)]
assert dot(L,pind)==Q(7,12)
Vselect=[0,1]
assert all((s^t) in Vselect for s in Vselect for t in Vselect)
record('restricted_product_and_selected_subalgebra',initial_means=[mu1,mu2],posterior_means=[Q(5,7),-Q(1,5)],branch_probability=Q(7,12))

r=[Q(1,4)]*4
A=[[r[i]*L[j] for j in range(4)] for i in range(4)]
oldA=mv(A,pp); assert norm(oldA)==r
MA=[[dot(row,[A[i][j] for i in range(4)]) for j in range(4)] for row in M]
assert MA==[L,[0]*4,[0]*4]
record('state_changing_reset_not_passive',retained_posterior=mv(M,r),matrix_rank=rank(A))

initial={0,1,2,4}; closure=set(initial)
while True:
    new=closure|{s^1 for s in closure}
    if new==closure: break
    closure=new
assert closure=={0,1,2,3,4,5} and len(closure)==6
assert {6,7}.isdisjoint(closure)
record('channel_adapted_six_dimensional_closure',initial_masks=sorted(initial),closure_masks=sorted(closure),missing_unneeded_masks=[6,7])

cone_cases=[]
for m,k in ((2,1),(3,1),(3,2),(3,3)):
    XX,ms,MM=walsh(m,k); n=len(XX); rr=len(MM)
    assert rank(MM)==rr
    for x in XX:
        exposed=[m-sum(a*b for a,b in zip(x,y)) for y in XX]
        assert sum(v==0 for v in exposed)==1 and all(v>=0 for v in exposed)
    # Solve all linear maps satisfying T M=M diag(L), in unknowns T and L.
    eq=[]
    for j in range(rr):
        for x in range(n):
            row=[Q(0)]*(rr*rr+n)
            for a in range(rr): row[j*rr+a]=MM[a][x]
            row[rr*rr+x]=-MM[j][x]
            eq.append(row)
    nullity=rr*rr+n-rank(eq)
    assert nullity==(n if k==m else 1)
    if k==m:
        for i in range(n):
            for j in range(n):
                assert sum(MM[a][i]*MM[a][j] for a in range(n))==(n if i==j else 0)
    cone_cases.append({'m':m,'k':k,'lift_space_dimension':nullity,'ray_count':n,'cone_span_dimension':rr})
record('exposed_rays_and_exact_diagonal_lift_spaces',cases=cone_cases)

v=[Q(1,2),Q(1,2),Q(0)]; w=[Q(1,2),Q(0),Q(1,2)]
# Each intrinsic vector a*v+b*w with a,b>=0 splits uniquely into these two parts.
assert rank([v,w])==2
# D_L v and D_L w obey p1=p2+p3 exactly when L1=L2 and L1=L3.
constraints=[[1,-1,0],[1,0,-1]]
assert rank(constraints)==2
record('intrinsic_feasible_cone_does_not_supply_diagonal_lift',intrinsic_component_count=2,ambient_diagonal_dimension=3-rank(constraints))

result={'status':'PASS','exact_arithmetic':'Python standard-library Fraction','groups':len(out),'results':out,'scope':'Finite controls supplement ordinary general proofs; no formal-kernel certification.'}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
