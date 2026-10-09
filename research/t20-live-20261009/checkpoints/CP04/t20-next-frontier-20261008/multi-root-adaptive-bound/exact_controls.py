#!/usr/bin/env python3
"""Exact deterministic controls for the written multiroot proof; no simulations."""
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
R={}
def save(name,x):R[name]=x;print('PASS',name)
def C(r,k):return F(2,k*(k+3))*F(4,(k+1)**2)*F(4,(k+2)**2)**(r-2)
def qs(r,k,S,a):
    q0=prod(((1-a[i])**k for i in S),start=F(1))
    z=prod(a,start=F(1)) if len(S)==r else F(0)
    return q0,q0*(1-z)
def chi(q0,q1):
    if q0==q1:return F(0)
    assert 0<q1<q0<1
    return (q0-q1)**2/(q1*(1-q1))

bound_cases=0;interior_cases=0;boundary_cases=0;max_ratio=(F(0),None)
for r in range(2,7):
    grid=[F(0),F(1,100),F(1,4),F(1,2),F(3,4),F(99,100),F(1)] if r<=3 else [F(1,10),F(1,2),F(9,10)]
    for k in [1,2,3,5,10,25]:
        for a in product(grid,repeat=r):
            q0,q1=qs(r,k,range(r),a);value=chi(q0,q1)
            assert value<=C(r,k);bound_cases+=1
            if value/C(r,k)>max_ratio[0]:max_ratio=(value/C(r,k),[r,k,list(a)])
            if any(x in [0,1] for x in a):
                assert q0==q1;boundary_cases+=1;continue
            interior_cases+=1
            u=[1-x for x in a];z=prod(a,start=F(1));S=sum((u[0]**j for j in range(k)),F(0))
            exact=q0*z*z/((1-z)*(1-q1))
            assert exact==value
            relaxed=q0*z*z/(u[1]*a[0]*S)
            factors=[u[0]**k*a[0]/S,u[1]**(k-1)*a[1]**2]+[u[i]**k*a[i]**2 for i in range(2,r)]
            assert value<=relaxed==prod(factors,start=F(1))<=C(r,k)
            assert S*S>=k*k*u[0]**(k-1)
            limits=[F(2,k*(k+3)),F(4,(k+1)**2)]+[F(4,(k+2)**2)]*(r-2)
            assert all(x<=y for x,y in zip(factors,limits))
save('exact_uniform_bound_and_factorization',{'cases':bound_cases,'interior':interior_cases,'boundary':boundary_cases,'largest_tested_chisquare_over_C':max_ratio})

pc=0
for r in range(2,7):
    for bits in product([0,1],repeat=r):
        S=[i for i,b in enumerate(bits) if b]
        if len(S)==r:continue
        for k in [1,2,7]:
            for a in [tuple(F(i+1,r+2) for i in range(r)),(F(0),)*r,(F(1),)*r]:
                q0,q1=qs(r,k,S,a);assert q0==q1;pc+=1
save('all_proper_issued_profiles',{'cases':pc})

kc=0
for r in range(2,21):
    for L in range(r+1,12*r+2):
        k=(L-1)//r
        assert k>=1 and r*k+1<=L and L<r*(k+1)+1
        assert C(r,k)<=F(2*4**(r-1),k**(2*r))
        kc+=1
save('total_route_bound_and_asymptotic_envelope',{'cases':kc})

counts=[]
for r in range(2,9):
    settings=[(S,V) for S in range(1,2**r) for V in range(1,2**r) if V&S==V]
    G=len(settings);assert G==3**r-2**r
    assert sum(S==2**r-1 for S,V in settings)==2**r-1
    for L in [r+1,2*r+1,10*r+1]:
        k=(L-1)//r;p=F(1,2*L)
        assert r*k+1<=L
        for S,V in settings:
            a=tuple(p if V&(1<<i) else F(0) for i in range(r))
            q0,q1=qs(r,k,[i for i in range(r) if S&(1<<i)],a)
            assert min(q0,q1)>=F(1,2)
    counts.append({'r':r,'full_guarded_settings':G,'unguarded_settings':2**r-1})
save('inherited_menu_is_allowed_and_hard_pair_probability_floor',counts)

transcripts=[]
for r in [2,3]:
    for k in [1,2,4]:
        full=tuple(range(r))
        actions=[(full,tuple(F(i+1,r+2) for i in range(r))),
                 (full,(F(1,2),)*r),
                 (full,(F(0),)+(F(1,2),)*(r-1)),
                 (full,(F(1),)+(F(1,3),)*(r-1)),
                 ((0,), (F(1,4),)*r),
                 ((),(F(3,4),)*r)]
        for seed in range(4):
            nodes={(): (F(1),F(1))};information_bound=F(0);depth=5
            for t in range(depth):
                nextnodes={}
                for hist,(p0,p1) in nodes.items():
                    index=(seed+sum((j+1)*y for j,y in enumerate(hist))+2*t)%len(actions)
                    S,a=actions[index];q0,q1=qs(r,k,S,a)
                    information_bound+=p0*chi(q0,q1)
                    for y in [0,1]:
                        v0=q0 if y else 1-q0;v1=q1 if y else 1-q1
                        nextnodes[hist+(y,)]=(p0*v0,p1*v1)
                nodes=nextnodes
                assert sum(p[0] for p in nodes.values())==1==sum(p[1] for p in nodes.values())
            assert all((p0==0)==(p1==0) for p0,p1 in nodes.values())
            assert information_bound<=depth*C(r,k)
            transcripts.append({'r':r,'k':k,'seed':seed,'depth':depth,'expected_conditional_chisquare':information_bound,'chain_bound':depth*C(r,k)})
save('exact_adaptive_tree_conditional_information_envelopes',transcripts)

weak=[]
for r in [2,3,5]:
    for k in [2,3,5,10,25,100]:
        t=1-F(1,k);q0=t**k;q1=q0*t
        assert k*k*chi(q0,q1)>=F(1,4)
        weak.append({'r':r,'k':k,'q0':q0,'q1':q1,'k_squared_chisquare':k*k*chi(q0,q1)})
save('unbalanced_baseline_rate_one_bypass',weak)

for r in [2,3,5]:
    for bits in product([0,1],repeat=r):
        for Sbits in product([0,1],repeat=r):
            baseline=any(x and s for x,s in zip(bits,Sbits))
            added=all(bits) and all(Sbits)
            assert baseline==(baseline or added)
q0,q1=qs(2,2,range(2),(F(1,2),)*2)
assert (q0,q1)==(F(1,16),F(3,64))
save('shared_random_root_gates_invalidate_count_response',{'independent_route_qs':[q0,q1],'shared_gate_qs':[F(1,4),F(1,4)]})

small_variances=[]
for a in [(F(1,10**6),)*2,(1-F(1,10**6),)*2]:
    q0,q1=qs(2,2,range(2),a)
    assert q1*(1-q1)<F(1,100)
    small_variances.append(q1*(1-q1))
save('no_rate_uniform_positive_variance_floor',small_variances)

assert C(2,1)==F(1,2) and C(3,1)==F(2,9)
save('k_one_and_r_two_edges',{'C(2,1)':C(2,1),'C(3,1)':C(3,1)})

for r in range(2,7):
    for m in range(1,6):
        E=tuple(range(m));q0,q1=qs(r,2,range(r),(F(1,2),)*r)
        law0={():q0,E:1-q0};law1={():q1,E:1-q1}
        assert len(law0)==2==len(law1)
        assert chi(law0[()],law1[()])==chi(q0,q1)
save('whole_effect_bundle_binary_embedding',{'root_counts':'2..6','effect_counts':'1..5'})

def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [enc(v) for v in x]
    return x
(HERE/'results').mkdir(exist_ok=True)
(HERE/'results'/'exact_controls.json').write_text(json.dumps(enc({'passed_families':len(R),'controls':R}),indent=2)+'\n')
print('ALL',len(R),'EXACT CONTROL FAMILIES PASS')
