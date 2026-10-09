#!/usr/bin/env python3
"""Exact deterministic theorem controls and a finite-grid witness. No sampling."""
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, comb, factorial, lcm, prod
from functools import reduce
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent;out={}
def save(n,x):out[n]=x;print('PASS',n)
def ceil(q):return (q.numerator+q.denominator-1)//q.denominator
def floor(q):return q.numerator//q.denominator
def target(J):
    P=[j for j in J if j]
    return (tuple(j//reduce(gcd,P) for j in P) if P else (),0 in J)
def atoms(J,t):return [t**j for j in J]
def haus(A,B):return max(max(min(abs(a-b) for b in B) for a in A),max(min(abs(a-b) for a in A) for b in B))
def moments(J,w,t,R):return [sum((z*t**(r*j) for j,z in zip(J,w)),F(0)) for r in range(R+1)]
def gapnorm(a,b):return max(abs(x-y) for x,y in zip(a,b))
def params(M,C,w,alpha=None):
    eps=F(1,32*M*M);A=(32*M)**(C-1);B=C*(16*M)**(C-1)
    if alpha is not None:eps=min(eps,alpha/(2*B))
    D=(w/2)*eps**(2*C)/4**C;tau=D/8
    if alpha is not None:tau=min(tau,alpha/(6*A))
    Q=ceil(4*C/tau)
    return eps,D,tau,Q,A,B
def grid_round(M,C,w,J,weights,t,alpha=None):
    eps,D,tau,Q,A,B=params(M,C,w,alpha)
    ints=[floor(p*Q) for p in weights[:-1]];ints.append(Q-sum(ints))
    ww=[F(n,Q) for n in ints]
    low=1-F(3,2*M);h=floor((t-low)*M*Q);tt=low+F(h,M*Q)
    assert 0<=h<=Q and all(z>=w/2 for z in ww) and sum(ww)==1
    assert low<=tt<=1-F(1,2*M) and 0<=t-tt<=F(1,M*Q)
    assert sum(abs(a-b) for a,b in zip(weights,ww))<=F(2*C,Q)
    mm=moments(J,weights,t,2*C);gg=moments(J,ww,tt,2*C)
    assert gapnorm(mm,gg)<=F(4*C,Q)<=tau
    return {'M':M,'C':C,'w':w,'support':J,'true_weights':weights,'true_t':t,'epsilon':eps,'Delta':D,'tau':tau,'Q':Q,'weight_numerators':ints,'grid_weights':ww,'grid_t_index':h,'grid_t':tt,'max_moment_error':gapnorm(mm,gg),'grid_moments':gg,'true_moments':mm}
def mul(p,q):
    z=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):z[i+j]+=a*b
    return z
def evalpoly(p,z):return sum((v*z**i for i,v in enumerate(p)),F(0))
def countlaw(q,w,R):return [sum((p*comb(R,s)*z**s*(1-z)**(R-s) for z,p in zip(q,w)),F(0)) for s in range(R+1)]

geometry=0
for M in list(range(3,81))+[100,200]:
    low=1-F(3,2*M);high=1-F(1,2*M)
    for t in [low,(low+high)/2,high]:
        q=[t**j for j in range(M+1)]
        assert min(q)>=F(1,8)
        assert min(q[j]-q[j+1] for j in range(M))>=F(1,16*M)
        assert q[0]==1 and q[1]<=1-F(1,2*M);geometry+=1
save('uniform_atom_floor_gap_and_zero_margin',geometry)

pairchecks=0;different=0
for M in range(3,8):
    T=[1-F(3,2*M),1-F(1,M),1-F(1,2*M)]
    worlds=[(J,t,atoms(J,t)) for s in [1,2] for J in combinations(range(M+1),s) for t in T]
    for W,Z in combinations(worlds,2):
        J,t,A=W;L,s,B=Z;h=haus(A,B);eps=F(1,32*M*M)
        if target(J)!=target(L):assert h>=eps;different+=1
        if h<eps:
            assert len(A)==len(B) and target(J)==target(L)
            assert max(abs(a-b) for a,b in zip(A,B))<=h
        pairchecks+=1
save('primitive_target_hausdorff_controls',{'pairs':pairchecks,'different_targets':different})

polychecks=0
for M in [3,4,6,10]:
    C=2;w=F(1,4);eps,D,tau,Q,AA,BB=params(M,C,w)
    J=[0,1];L=[M-1,M];wa=[F(2,5),F(3,5)];wb=[F(1,3),F(2,3)]
    for t,s in product([1-F(3,2*M),1-F(1,M),1-F(1,2*M)],repeat=2):
        A=atoms(J,t);B=atoms(L,s);h=haus(A,B)
        assert h>=eps
        ma=moments(J,wa,t,2*C);mb=moments(L,wb,s,2*C)
        candidates=[(a,wa[i],A,B,ma,mb,wa,wb) for i,a in enumerate(A) if min(abs(a-b) for b in B)>=eps]
        if not candidates:
            candidates=[(a,wb[i],B,A,mb,ma,wb,wa) for i,a in enumerate(B) if min(abs(a-b) for b in A)>=eps]
        a,wt,X,Y,mx,my,wx,wy=candidates[0]
        p=[F(1)]
        for b in Y:p=mul(p,[b*b,-2*b,F(1)])
        assert sum(abs(z) for z in p)<=4**C
        ex=sum((z*evalpoly(p,q) for z,q in zip(wx,X)),F(0))
        ey=sum((z*evalpoly(p,q) for z,q in zip(wy,Y)),F(0))
        assert ey==0 and ex>=wt*eps**(2*len(Y))>=w/2*eps**(2*C)
        assert ex-ey==sum(p[r]*(mx[r]-my[r]) for r in range(len(p)))
        assert gapnorm(mx[1:],my[1:])>=D;polychecks+=1
save('nonnegative_annihilator_moment_margin',polychecks)

fc=0
for R in [2,4,6,8]:
    for q in [F(1,8),F(1,4),F(2,3),F(1)]:
        law=countlaw([q],[F(1)],R)
        for r in range(1,R+1):
            vals=[F(factorial(s)//factorial(s-r),factorial(R)//factorial(R-r)) if s>=r else F(0) for s in range(R+1)]
            assert min(vals)>=0 and max(vals)<=1
            assert sum(p*v for p,v in zip(law,vals))==q**r;fc+=1
save('factorial_moment_identities',fc)

rounding=[]
for M,C in product([3,5,10,20],[1,2,3]):
    w=F(1,2*C*C)
    for size in range(1,C+1):
        J=list(range(size)) if size>1 else [M]
        weights=[F(i+1,size*(size+1)//2) for i in range(size)]
        low=1-F(3,2*M)
        for z in [F(1,7),F(2,5),F(3,4)]:
            row=grid_round(M,C,w,J,weights,low+z/M)
            assert row['Delta']==w/F(2**(12*C+1)*M**(4*C))
            rounding.append({'M':M,'C':C,'size':size,'Q':row['Q'],'error':row['max_moment_error'],'tau':row['tau']})
save('exact_finite_grid_rounding_with_relaxed_weight_floor',{'cases':len(rounding),'rows':rounding})

# One complete exact grid witness, with synthetic aggregate frequencies only.
row=grid_round(3,2,F(1,4),[1,3],[F(2,7),F(5,7)],F(7,10))
R=4;law=countlaw(atoms(row['support'],row['true_t']),row['true_weights'],R)
delta=F(1,20);B=0
while 2**B<4*row['C']/delta:B+=1
n_budget=ceil(32*row['Delta']**-2*B)
den=reduce(lcm,[z.denominator for z in law],1)
n=ceil(F(n_budget,den))*den
counts=[int(n*z) for z in law];assert sum(counts)==n
empirical=[]
for r in range(1,R+1):
    empirical.append(sum(F(cnt,n)*F(factorial(s)//factorial(s-r),factorial(R)//factorial(R-r)) for s,cnt in enumerate(counts) if s>=r))
assert empirical==row['true_moments'][1:]
assert gapnorm(empirical,row['grid_moments'][1:])<=2*row['tau']
assert target(row['support'])==((1,3),False)
assert 2*n*row['tau']**2>=B and 2**B>=4*row['C']/delta
witness=dict(row,kind='Synthetic exact count-frequency witness; no samples drawn and no exhaustive grid search run',delta=delta,log_upper_integer=B,sufficient_budget=n_budget,synthetic_group_total=n,synthetic_count_frequencies=counts,empirical_moments=empirical,passes_acceptance_radius=True,primitive_target=[1,3],zero_present=False)
save('complete_synthetic_finite_grid_witness',{'Q':row['Q'],'nonzero_weight_rounding':row['grid_weights']!=row['true_weights'],'nonzero_rate_rounding':row['grid_t']!=row['true_t'],'candidate_residual':row['max_moment_error'],'acceptance_radius':2*row['tau']})

wc=0
for M,C in product([3,6,12],[1,2,3]):
    w=F(1,2*C*C);alpha=F(1,10);J=list(range(C));weights=[F(1,C)]*C
    t=1-F(1,M);row=grid_round(M,C,w,J,weights,t,alpha)
    eps,D,tau,Q,A,B=params(M,C,w,alpha);q=atoms(J,t)
    assert 3*A*tau+B*eps<=alpha
    for i,a in enumerate(q):
        p=[F(1)];den=F(1)
        for j,b in enumerate(q):
            if i!=j:p=mul(p,[-b,F(1)]);den*=a-b
        p=[v/den for v in p]
        assert sum(abs(v) for v in p)<=A
        assert F(len(q)-1,1)/abs(den)<=B
        assert all(evalpoly(p,b)==int(i==j) for j,b in enumerate(q))
    assert max(abs(a-b) for a,b in zip(weights,row['grid_weights']))<=alpha
    wc+=1
save('separate_weight_budget_and_lagrange_certificates',wc)

nc=0
for M in range(3,41):
    u=1-F(1,3*M);aa=1-u**3;bb=1-u*u
    assert F(1,2*M)<=aa<=F(3,2*M) and F(1,2*M)<=bb<=F(3,2*M)
    assert [u**3,u**6]==[u**3,(u*u)**3]
    assert target([1,2])!=target([1,3]);nc+=1
save('component_specific_calibration_counterfeit_inside_window',nc)

for M in range(3,41):
    t=1-F(1,M);s=(t+t*t)/2;aa=1-s
    assert aa==F(3,2*M)-F(1,2*M*M)
    assert F(1,2*M)<=aa<=F(3,2*M)
    assert (t*t+t**4)/2-s*s==(t-t*t)**2/4>0
save('fresh_resampling_counterfeit_inside_window',38)

q=F(2,3);eps=F(1,100);base=countlaw([q],[F(1)],2);alt=countlaw([q,F(1)],[1-eps,eps],2)
for n in [1,2,3]:
    tv=sum(abs(prod(base[s] for s in seq)-prod(alt[s] for s in seq)) for seq in product(range(3),repeat=n))/2
    assert tv<=n*eps
save('rare_zero_mass_obstruction',True)

unbounded=[];t=F(3,4);R=4
for k in [4,10,20,50]:
    base=countlaw([t**k],[F(1)],R)
    mixed=countlaw([t**k,t**(k+1)],[F(1,2),F(1,2)],R)
    tv=sum(abs(a-b) for a,b in zip(base,mixed))/2
    bound=R*(1-t)*t**k/2
    assert tv<=bound and target([k])!=target([k,k+1])
    unbounded.append({'count':k,'group_TV':tv,'coupling_bound':bound})
save('fixed_rate_unbounded_count_primitive_obstruction',unbounded)

for M in range(3,81):
    eta=F(1,2*M)*(1-F(1,M))**(M-1)
    assert eta<F(1,2*M)
save('inherited_absolute_ambiguity_radius_fits_window',78)

bc=0
for M,C,w,delta in product([3,10],[1,2,3],[F(1,4),F(1,10)],[F(1,2),F(1,20),F(1,1000)]):
    ep,D,tau,Q,A,B=params(M,C,w);b=0
    while 2**b<4*C/delta:b+=1
    n=ceil(F(b,1)/(2*tau*tau))
    assert 2**b>=4*C/delta and 2*n*tau*tau>=b
    assert n==ceil(32*D**-2*b);bc+=1
save('rational_budget_selection',bc)

def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v) for v in x]
    return x
(HERE/'results').mkdir(exist_ok=True)
(HERE/'results'/'exact_controls.json').write_text(json.dumps(enc({'families_passed':len(out),'controls':out}),indent=2)+'\n')
(HERE/'results'/'GRID_WITNESS.json').write_text(json.dumps(enc(witness),indent=2)+'\n')
print('ALL',len(out),'EXACT CONTROL FAMILIES PASS')
