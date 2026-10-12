#!/usr/bin/env python3
"""Finite checks for continuation-complete orthing representations.

Exact arithmetic verifies the certificates; scipy is only a proposal engine for
small linear-program witnesses. This is not a proof-assistant development.
Run: python verify_frontier.py
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json, random
import numpy as np
import sympy as sp
from scipy.optimize import linprog

OUT=Path(__file__).resolve().parent
RESULTS={}
def require(p: bool, msg: str):
    if not p: raise AssertionError(msg)
def frac(x): return F(float(x)).limit_denominator(1000000)
def dot(x,y): return sum((a*b for a,b in zip(x,y)), F(0))
def rank_rows(rows):
    if not rows: return []
    M=sp.Matrix(rows)
    piv=(M.T).rref()[1]
    return [tuple(F(v) for v in rows[i]) for i in piv]

def sharp_defect():
    rng=random.Random(813071)
    count=0; positive=0
    for n in range(2,9):
        for rep in range(15):
            k=rng.randrange(1,min(n,4)+1)
            rows=[[F(1)]*n]+[[F(rng.randrange(-2,3)) for _ in range(n)] for _ in range(k-1)]
            f=[F(rng.randrange(-4,5)) for _ in range(n)]
            A=np.array(rows,float); q=np.array(f,float)
            # Minimise t subject to |f-Phi^T a| <= t.
            c=np.r_[np.zeros(k),1.]
            Aub=np.vstack([np.column_stack([-A.T,-np.ones(n)]), np.column_stack([A.T,-np.ones(n)])])
            bub=np.r_[-q,q]
            sol=linprog(c,A_ub=Aub,b_ub=bub,bounds=[(None,None)]*k+[(0,None)],method='highs')
            require(sol.success,'primal LP failed')
            a=list(map(frac,sol.x[:-1])); t=frac(sol.x[-1])
            require(all(abs(f[j]-sum(a[i]*rows[i][j] for i in range(k)))<=t for j in range(n)), 'rational primal certificate invalid')
            # Maximise half the separation of two indistinguishable laws.
            E=np.column_stack([A,-A]); E=np.vstack([E,np.r_[np.ones(n),np.zeros(n)],np.r_[np.zeros(n),np.ones(n)]])
            rhs=np.r_[np.zeros(k),1.,1.]
            dual=linprog(np.r_[-q,q]/2,A_eq=E,b_eq=rhs,bounds=[(0,None)]*(2*n),method='highs')
            require(dual.success,'dual pair LP failed')
            mu=list(map(frac,dual.x[:n])); nu=list(map(frac,dual.x[n:]))
            require(sum(mu)==1 and sum(nu)==1 and min(mu+nu)>=0,'rational law invalid')
            require(all(dot(row,mu)==dot(row,nu) for row in rows),'moment equality failed')
            require((dot(f,mu)-dot(f,nu))/2==t,'exact primal/dual gap')
            count+=1; positive+=bool(t)
    RESULTS['sharp_defect_rational_certificates']={'cases':count,'positive_defects':positive,'status':'PASS'}

def local_update_growth():
    ncases=0; pullbacks=0; ranks=0
    records=[]
    for n in range(2,10):
        masks={0}|{1<<i for i in range(n)}
        for h in range(n):
            expected={s for s in range(1<<n) if s.bit_count()<=min(n,h+1)}
            require(masks==expected,f'horizon support mismatch n={n} h={h}')
            d=sum(comb(n,j) for j in range(min(n,h+1)+1))
            require(len(masks)==d,'dimension mismatch')
            records.append({'n':n,'h':h,'observable_rank':d,'min_continuous_coordinates':d-1})
            ncases+=1
            nxt=set(masks)
            for s in masks:
                for i in range(n):
                    for j in range(n):
                        if i==j: continue
                        out=s^(1<<j) if s&(1<<i) else s
                        nxt.add(out)
                        if n<=5:
                            for bits in range(1<<n):
                                z=[-1 if bits&(1<<q) else 1 for q in range(n)]
                                zz=z.copy(); zz[i]=z[i]*z[j]
                                lhs=np.prod([zz[q] for q in range(n) if s&(1<<q)],dtype=int)
                                rhs=np.prod([z[q] for q in range(n) if out&(1<<q)],dtype=int)
                                require(lhs==rhs,'pointwise pullback failed');pullbacks+=1
            masks=nxt
        if n<=7:
            W=np.array([[(-1)**((s&x).bit_count()) for x in range(1<<n)] for s in range(1<<n)],dtype=np.int64)
            require(np.array_equal(W@W.T,(1<<n)*np.eye(1<<n,dtype=np.int64)),'Walsh orthogonality failed')
            ranks+=1
    (OUT/'horizon_dimensions.json').write_text(json.dumps(records,indent=2)+'\n')
    RESULTS['pair_update_horizon_growth']={'horizon_cases':ncases,'pointwise_pullbacks':pullbacks,'full_Walsh_orthogonality_cases':ranks,'status':'PASS'}

def parity_future():
    checks=0; trajectories=0
    for n in range(2,10):
        mus=[]
        for sign in [1,-1]:
            mus.append([F(1,1<<(n-1)) if (-1)**(x.bit_count())==sign else F(0) for x in range(1<<n)])
        for mask in range((1<<n)-1):
            f=[F((-1)**((mask&x).bit_count())) for x in range(1<<n)]
            require(dot(f,mus[0])==dot(f,mus[1]),'proper-moment separation')
            checks+=1
        vals=[]
        for x in range(1<<n):
            z=[-1 if x&(1<<i) else 1 for i in range(n)]
            for j in range(1,n): z[0]*=z[j]
            require(z[0]==(-1)**x.bit_count(),'forward parity chain failed')
            vals.append(F((1-z[0])//2)); trajectories+=1
        require(dot(vals,mus[0])==0 and dot(vals,mus[1])==1,'maximal outcome separation failed')
    RESULTS['future_parity_witnesses']={'matched_moment_cases':checks,'pointwise_forward_trajectories':trajectories,'status':'PASS'}

def instrument_closure():
    # Four latent states, action-dependent deterministic update, then noisy
    # binary observation; instruments are exact sub-stochastic matrices.
    n=4
    updates=[[0,1,2,3],[0,2,1,3],[1,0,3,2]]
    obs=[F(1,4),F(1,2),F(3,4),F(1)]
    mats=[]
    for update in updates:
        for o in [0,1]:
            K=[[F(0)]*n for _ in range(n)]
            for x,j in enumerate(update): K[x][j]=obs[j] if o else 1-obs[j]
            mats.append(K)
    def apply(K,f):return tuple(dot(row,f) for row in K)
    rows=rank_rows([[F(1)]*n,[F(0),F(0),F(1),F(1)]])
    dims=[len(rows)]
    while True:
        new=rank_rows(rows+[apply(K,f) for K in mats for f in rows])
        if len(new)==len(rows):break
        rows=new;dims.append(len(rows))
    B=sp.Matrix(rows)
    require(len(rows)==4,'instrument example did not expose full dimension')
    d=0; post=0
    for K in mats:
        KM=sp.Matrix(K)
        R=B*KM.T*B.inv()
        require(R*B==B*KM.T,'closure matrix failed')
        for den in range(1,6):
            for a in range(den+1):
                mu=sp.Matrix([sp.Rational(a,den),sp.Rational(den-a,den),0,0])
                actual=KM.T*mu
                represented=R*B*mu
                require(represented==B*actual,'unnormalised feature update failed');d+=1
                mass=sum(actual)
                if mass>0:
                    require(represented/mass==B*(actual/mass),'conditional update failed');post+=1
    RESULTS['feedback_instrument_completion']={'dimension_chain':dims,'exact_updates':d,'positive_mass_posterior_checks':post,'status':'PASS'}

def direct_advantages():
    rng=random.Random(819)
    count=0
    # Certify that a direct advantage bound eta gives eta, not two eta, in
    # regret transfer, while same-opponent payoff shifts preserve all gains.
    grid=[F(0),F(1,4),F(1,2),F(3,4),F(1)]
    for trial in range(20):
        U=[[F(rng.randrange(-3,4)) for _ in range(4)] for _ in range(2)]
        V=[[u+F(rng.randrange(-2,3),4) for u in row] for row in U]
        for p,q in product(grid,repeat=2):
            probs=[(1-p)*(1-q),(1-p)*q,p*(1-q),p*q]
            for i in [0,1]:
                allD=[];allE=[]
                for b in [0,1]:
                    D=[];E=[]
                    for s1,s2 in product([0,1],repeat=2):
                        index=2*s1+s2
                        dest=(2*b+s2) if i==0 else (2*s1+b)
                        D.append(U[i][dest]-U[i][index]);E.append(V[i][dest]-V[i][index])
                    allD.append(D);allE.append(E)
                eta=max(abs(a-b) for A,B in zip(allD,allE) for a,b in zip(A,B))
                reg=max(dot(probs,D) for D in allD)
                regV=max(dot(probs,D) for D in allE)
                require(reg<=regV+eta,'direct advantage transport failed');count+=1
    RESULTS['direct_advantage_regret_transport']={'exact_cases':count,'status':'PASS'}

def mixed_safety():
    rects=0; safe=0; products_checked=0; nash=0
    for n in range(2,8):
        # Supports {-1}, {+1}, {-1,+1}; parity +1 is feasible.
        for choices in product([(-1,),(1,),(-1,1)],repeat=n):
            feasible=all(np.prod(a)==1 for a in product(*choices))
            singleton=all(len(c)==1 for c in choices)
            require(not feasible or singleton,'safe non-singleton parity rectangle')
            rects+=1; safe+=feasible
        for p in product([F(1,4),F(1,2),F(3,4)],repeat=n):
            bias=np.prod([1-2*q for q in p])
            fail=(1-bias)/2
            bound=(1-F(1,2)**n)/2
            require(fail>=bound,'exploration safety lower bound');products_checked+=1
        # All-on penalty family with c=1, M=2^(n-1), p=1/2.
        M=F(2**(n-1));p=F(1,2)
        require(1-M*p**(n-1)==0,'symmetric indifference failed')
        pure=[]
        for s in product([0,1],repeat=n):
            U=[F(si)-M*int(all(s)) for si in s]
            eq=True
            for i in range(n):
                alt=list(s);alt[i]=1-alt[i]
                gain=F(alt[i])-M*int(all(alt))-U[i]
                if gain>0:eq=False
            if eq:pure.append(s)
        require(len(pure)==n and all(sum(s)==n-1 for s in pure),'pure equilibrium characterisation failed')
        require(p**n>0,'finite penalty falsely eliminated risk');nash+=1
    RESULTS['mixed_safety_and_coordination']={'rectangles_checked':rects,'safe_rectangles':safe,'exploration_profiles_checked':products_checked,'penalty_game_families':nash,'status':'PASS'}

def approximate_dimension_bound():
    rng=random.Random(44277)
    cases=0; lp_checks=0
    for n in range(2,6):
        N=1<<n
        for h in range(n):
            masks=[s for s in range(1,N) if s.bit_count()<=h+1]
            m=len(masks)
            for d in sorted({0,1,min(3,m),m}):
                rows=[[F(1)]*N]
                while len(rows)<d+1:
                    v=[F(rng.randrange(-3,4)) for _ in range(N)]
                    new=rank_rows(rows+[v])
                    if len(new)>len(rows): rows=new
                A=sp.Matrix(rows)
                P=A.T*(A*A.T).inv()*A
                residuals=[]
                for mask in masks:
                    v=sp.Matrix([[(-1)**((mask&x).bit_count()) for x in range(N)]])
                    r=(v*(sp.eye(N)-P)*v.T)[0]/N
                    require(r>=0,'negative projected squared norm')
                    residuals.append(r)
                require(sum(residuals)>=m-d,'Bessel/trace lower bound failed')
                cases+=1
                # Independently check one worst L2 residual against an L-infinity LP.
                j=max(range(m),key=lambda j:residuals[j]); mask=masks[j]
                target=np.array([(-1)**((mask&x).bit_count()) for x in range(N)],float)
                AA=np.array(rows,float)
                sol=linprog(np.r_[np.zeros(d+1),1.],
                    A_ub=np.vstack([np.column_stack([-AA.T,-np.ones(N)]),np.column_stack([AA.T,-np.ones(N)])]),
                    b_ub=np.r_[-target,target],bounds=[(None,None)]*(d+1)+[(0,None)],method='highs')
                require(sol.success,'projection LP failed')
                coeff=list(map(frac,sol.x[:-1]))
                # Solver coefficients are proposals only. Recompute their exact
                # sup error: rounded coefficients need not attain the solver's
                # separately rounded optimal t. This is an upper certificate,
                # not an asserted exact optimum (group 1 checks optimum duality).
                t=max(abs(F(int(target[x]))-sum(coeff[i]*rows[i][x] for i in range(d+1))) for x in range(N))
                require(t*t>=residuals[j], 'sup norm below L2 residual')
                lp_checks+=1
    RESULTS['approximate_memory_lower_bound']={'rational_projection_cases':cases,'rational_LP_upper_certificate_checks':lp_checks,'status':'PASS'}

def parity_strategic_obstruction():
    c=F(1,2); grid=[F(i,8) for i in range(9)]; checks=0
    all_ne=[]
    for B in [0,1]:
        U=[[F(int(si==B))+c*int(s1==s2) for s1,s2 in product([0,1],repeat=2) for si in [(s1,s2)[i]]] for i in [0,1]]
        ne=[]
        for s1,s2 in product([0,1],repeat=2):
            ix=2*s1+s2
            if all(U[i][(2*(1-s1)+s2) if i==0 else (2*s1+1-s2)]<=U[i][ix] for i in [0,1]):ne.append((s1,s2))
        require(ne==[(B,B)],'unique truth-aligned equilibrium failed');all_ne.append(ne)
    for p,q in product(grid,repeat=2):
        probs=[(1-p)*(1-q),(1-p)*q,p*(1-q),p*q]
        for i in [0,1]:
            regrets=[]
            for B in [0,1]:
                gain=[]
                for s1,s2 in product([0,1],repeat=2):
                    before=[s1,s2]; after=before.copy();after[i]=B
                    u0=F(int(before[i]==B))+c*int(before[0]==before[1])
                    u1=F(1)+c*int(after[0]==after[1])
                    gain.append(u1-u0)
                regrets.append(dot(probs,gain))
            require(max(regrets)>=(1-c)/2,'two-law strategic regret bound failed'); checks+=1
    RESULTS['parity_strategic_obstruction']={'pure_game_cases':2,'mixed_profile_player_cases':checks,'status':'PASS'}

def mean_flow_and_memory():
    # Exact scalar stand-ins test the algebra; no fluid PDE is numerically solved.
    t,r,eps,a,b,c,y0=sp.symbols('t r eps a b c y0',positive=True)
    x=sp.symbols('x',real=True)
    require(sp.expand(b*x*(c*x*x)-b*c*x**3)==0,'effective cubic mismatch')
    m=[F(1,2),F(1,2)];v=[F(-1),F(1)]
    require(dot(m,[q*q for q in v])-dot(m,v)**2==1,'quadratic covariance defect failed')
    # For x(t)=t, verify the exact convolution solves eps*y'=-y+c*t^2.
    y=sp.exp(-t/eps)*y0+c/eps*sp.integrate(sp.exp(-(t-r)/eps)*r*r,(r,0,t))
    require(sp.simplify(eps*sp.diff(y,t)+y-c*t*t)==0,'eliminated memory ODE identity failed')
    require(sp.simplify(y.subs(t,0)-y0)==0,'eliminated memory initial condition failed')
    # x'=y, y'=0: compare exact trajectories from the same projected x(0).
    histories=[sp.Integer(1)*t,sp.Integer(-1)*t]
    require(histories[0].subs(t,0)==histories[1].subs(t,0),'initial fibre equality failed')
    require(sp.diff(histories[0],t)!=sp.diff(histories[1],t),'projected update closed falsely')
    RESULTS['reduction_structural_controls']={'exact_controls':5,'status':'PASS'}

def main():
    for fn in [sharp_defect,local_update_growth,parity_future,instrument_closure,direct_advantages,mixed_safety,approximate_dimension_bound,parity_strategic_obstruction,mean_flow_and_memory]:fn()
    payload={'status':'PASS','test_groups':len(RESULTS),'arithmetic':'Fraction / symbolic exact checks; LP witnesses proposed by HiGHS and then checked as rationals','groups':RESULTS,'nonclaims':['not Lean verified','not an empirical experiment','no repository or meniscus promotion','the continuous-encoder dimension theorem is proved on paper, not by finite enumeration']}
    (OUT/'verification.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(payload,indent=2))
if __name__=='__main__':main()
