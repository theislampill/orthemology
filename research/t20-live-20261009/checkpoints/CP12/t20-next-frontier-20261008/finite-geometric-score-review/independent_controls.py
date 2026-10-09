#!/usr/bin/env python3
"""Independent finite geometric-score diagnostics. Imports no author code."""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from math import factorial
from collections import Counter
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent

def H(n,r=1): return sum((F(1,k**r) for k in range(1,n+1)),F(0))
def ceil(q): return -((-q.numerator)//q.denominator)
def baseline(n):
    m=n+1; a=H(m); g=H(m,2)
    return -2*a/m+F(2,m*m)-(a*a-g-4)/(m+1)-2*(a+1)/(m+1)**2

def mul(p,q):
    z={}
    for a,x in p.items():
        for b,y in q.items():
            e=tuple(u+v for u,v in zip(a,b)); z[e]=z.get(e,0)+x*y
    return {e:c for e,c in z.items() if c}
def dpoly(k):
    # D = 1 - x_1 - y_k + sum x_i y_i - sum x_(i+1)y_i.
    p={(0,)*(2*k):1}
    def term(coef,*inds):
        e=[0]*(2*k)
        for i in inds:e[i]+=1
        e=tuple(e);p[e]=p.get(e,0)+coef
    term(-1,0);term(-1,2*k-1)
    for i in range(k):term(1,i,k+i)
    for i in range(k-1):term(-1,i+1,k+i)
    return p

def ordered_integral(p,k):
    ans=F(0)
    for e,coef in p.items():
        den=1; s=0
        for i in range(k):s+=e[i];den*=i+1+s
        s=0
        for i in range(k):s+=e[2*k-1-i];den*=i+1+s
        ans+=F(coef,den)
    return ans

def direct_score_moments(n):
    # Ordered-simplex skyline density (n)_k D^(n-k), separately integrated.
    m=n+1;norm=F(0);mean=F(0);second=F(0)
    for k in range(1,n+1):
        dp=dpoly(k); p={(0,)*(2*k):1}; ints=[]
        for r in range(n-k+5):
            ints.append(ordered_integral(p,k));p=mul(p,dp)
        factor=F(factorial(n),factorial(n-k)); base=n-k
        norm+=factor*ints[base]
        jc=[(k-m)**2-k,2*m*(k-m),m*m]
        mean+=factor*sum((jc[j]*ints[base+j] for j in range(3)),F(0))
        sq=[0]*5
        for i in range(3):
            for j in range(3):sq[i+j]+=jc[i]*jc[j]
        second+=factor*sum((sq[j]*ints[base+j] for j in range(5)),F(0))
    return norm,mean,second

def mins(points):
    return sorted(p for p in set(points) if not any(q!=p and q[0]<=p[0] and q[1]<=p[1] for q in set(points)))

def extract(points,L):
    calls=0
    def oracle(a,b):
        nonlocal calls
        calls+=1
        return any(x<=a and y<=b for x,y in points)
    def first(hi,test):
        lo=-1
        while hi-lo>1:
            mid=(lo+hi)//2
            if test(mid):hi=mid
            else:lo=mid
        return hi
    b=L;corners=[]
    while b>=0 and oracle(L,b):
        a=first(L,lambda x:oracle(x,b))
        y=first(b,lambda y:oracle(a,y))
        corners.append((a,y));b=y-1
    return corners,calls

def corner_area(corners,L):
    if not corners:return F(1)
    s=corners[0][0]*L
    for i,(x,y) in enumerate(corners):
        nx=corners[i+1][0] if i+1<len(corners) else L
        s+=(nx-x)*y
    return F(s,L*L)

def cell_area(points,L):
    return F(sum(not any(x<=a and y<=b for x,y in points) for a in range(L) for b in range(L)),L*L)

def area(points):
    if not points:return F(1)
    xs=sorted(set([F(0),F(1)]+[x for x,y in points])); ans=F(0)
    for a,b in zip(xs,xs[1:]):
        ys=[y for x,y in points if x<=a]
        ans+=(b-a)*(min(ys) if ys else F(1))
    return ans

def score(k,u,m):return (k-m*u)**2-k

def grid_root(n,A):
    p,q=A.numerator,A.denominator;m=n+1
    target=p**m;scale=q**m
    lo=0;hi=1
    while hi**n*scale<target:hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**n*scale>=target:hi=mid
        else:lo=mid
    assert hi**n*scale>=target
    assert hi==1 or (hi-1)**n*scale<target
    return hi

results={'status':'PASS','independence':'No imports from author or predecessor control code. Exact rational arithmetic except printed explanatory decimal ratios.'}
rows=[]
for n in range(1,7):
    norm,b,s=direct_score_moments(n)
    assert norm==1 and b==baseline(n) and s>=b*b
    rows.append({'n':n,'normalization':str(norm),'mean_J':str(b),'second_J':str(s),'variance_J':str(s-b*b)})
assert rows[0]['mean_J']=='-5/9'
results['direct_ordered_skyline_integrals']=rows

exhaust=[]
for L in range(1,5):
    grid=list(product(range(L+1),repeat=2));count=0;maxcalls=0
    d=L.bit_length() # ceil(log2(L+1))
    for N in range(5):
        for pp in combinations_with_replacement(grid,N):
            ss,calls=extract(pp,L);k=len(ss);m=max(1,N)
            assert ss==mins(pp)
            assert corner_area(ss,L)==cell_area(pp,L)
            assert score(k,corner_area(ss,L),m)==score(len(mins(pp)),cell_area(pp,L),m)
            assert calls<=1+k*(1+2*d)
            assert all(0<=x<=L and 0<=y<=L for x,y in ss)
            count+=1;maxcalls=max(maxcalls,calls)
    exhaust.append({'L':L,'multisets':count,'max_queries':maxcalls})
results['exhaustive_grid_extraction_area_score']=exhaust

fine=[(F(x,4),F(y,4)) for x,y in product(range(5),repeat=2)]
counts=0;good=0;loss=None;signs={};worst=F(0)
for N in range(5):
    m=max(1,N)
    for pp in combinations_with_replacement(fine,N):
        uq=area(pp);k=len(mins(pp))
        for L in (1,2,3):
            qq=[(ceil(L*x),ceil(L*y)) for x,y in pp]; ss,_=extract(qq,L);kl=len(ss); ul=corner_area(ss,L)
            assert kl<=k and 0<=ul-uq<=F(2*N,L)
            c=all(len(set(q[j] for q in qq))==N for j in (0,1))
            if c:
                assert kl==k
                err=score(kl,ul,m)-score(k,uq,m)
                assert abs(err)<=F(4*m**3,L)
                good+=1;worst=max(worst,abs(err)*L/F(4*m**3))
                if err and ('positive' if err>0 else 'negative') not in signs:
                    signs['positive' if err>0 else 'negative']={'points':str(pp),'L':L,'m':m,'error':str(err)}
            elif kl<k and loss is None:loss={'points':str(pp),'L':L,'K':k,'K_L':kl}
            counts+=1
assert len(signs)==2 and loss
results['rounding_checks']={'cases':counts,'collision_free_cases':good,'maximum_fraction_of_stated_score_bound':str(worst),'both_error_signs':signs,'strict_count_loss':loss}

# Exact baseline finite-grid laws, with each ordered list given mass L^(-2n).
# These are coarse-grid diagnostics, not assertions that the eventual test is valid here.
grid_laws=[]
for n in (1,2,3):
    m=n+1
    for L in range(1,6):
        atoms=list(product(range(1,L+1),repeat=2));mass=F(0);ej=F(0);et=F(0);ek=F(0);bad=F(0)
        for pp in combinations_with_replacement(atoms,n):
            ways=factorial(n)
            for v in Counter(pp).values():ways//=factorial(v)
            prob=F(ways,L**(2*n));ss,t=extract(pp,L);k=len(ss)
            mass+=prob;ej+=prob*score(k,corner_area(ss,L),m);et+=prob*t;ek+=prob*k
            if any(len(set(p[j] for p in pp))<n for j in (0,1)):bad+=prob
        assert mass==1 and ek<=H(n)
        assert et<=1+(1+2*L.bit_length())*H(n)
        assert bad<=F(m*(m-1),L)
        grid_laws.append({'n':n,'L':L,'mean_grid_score':str(ej),'grid_mean_minus_exact_mean':str(ej-baseline(n)),
                          'expected_queries':str(et),'mean_grid_count':str(ek),'collision_probability':str(bad)})
results['exact_uniform_finite_grid_laws']=grid_laws

# Both rounding signs occur for the protocol's m=3 bound even without collisions.
fixed_m_signs={}
for D,L,pp in ((16,8,[(F(1,16),F(1,16))]),(4,2,[(F(1,4),F(1,4))])):
    qq=[(ceil(L*x),ceil(L*y)) for x,y in pp]
    err=score(len(mins(qq)),corner_area(mins(qq),L),3)-score(len(mins(pp)),area(pp),3)
    assert err
    fixed_m_signs['positive' if err>0 else 'negative']=str(err)
assert set(fixed_m_signs)=={'positive','negative'}
results['both_rounding_signs_at_m3']=fixed_m_signs

budgets=[]
for n in (2,3,5,10,20,100):
    m=n+1;h=H(n)
    for alpha,eta in ((F(1,20),F(1,20)),(F(1,10),F(1,5)),(F(1,3),F(1,6))):
        R=ceil(192*m**4/(alpha*h*h));La=ceil(32*m**5/(h*h));A=m*(m-1)*R/eta;Lc=grid_root(n,A);L=max(La,Lc)
        e=h*h/(8*m*m);d=h*h/(4*m*m);delta_min=h*h/(2*m*m)
        assert F(4*m**3,L)<=e
        assert d-e==e and delta_min-d-e==e
        assert 3*h*h/(R*e*e)<=alpha
        p,q=A.numerator,A.denominator
        assert L**n*q**m>=p**m
        budgets.append({'n':n,'alpha':str(alpha),'eta':str(eta),'R':R,'L':L,'L_area':La,'L_collision':Lc})
results['exact_budget_cases']=budgets

center=[]
for n in (1,2,3,10,100,1000):
    b=baseline(n);h=H(n);gap=h*h/(n+1)**2
    center.append({'n':n,'baseline_mean':str(b) if n<=10 else float(b),'absolute_baseline_over_asymptotic_signal':float(abs(b)/gap)})
results['nonzero_centering_negative_control']=center

# Full-law change of measure must include an alternative-only point.
p0=[F(1,2),F(1,2)];p1common=[F(1,4),F(1,2)];js=[F(2),F(-1)];ps=F(1,4);j_s=F(3)
true_gap=sum(p*j for p,j in zip(p1common,js))+ps*j_s-sum(p*j for p,j in zip(p0,js))
common_gap=sum((q-p)*j for p,q,j in zip(p0,p1common,js))
assert true_gap==common_gap+ps*j_s and true_gap!=common_gap
results['singular_omission_negative_control']={'true_gap':str(true_gap),'common_only_gap':str(common_gap),'omitted_singular_term':str(ps*j_s)}
# Insufficient area resolution cannot establish the advertised e bound.
n=10;m=11;h=H(n);badL=ceil(16*m**5/(h*h));e=h*h/(8*m*m)
assert F(4*m**3,badL)>e
results['half_area_budget_rejected']=True
results['scope']={'eventual_cutoff_certified':False,'fixed_confidence_only':True,'formal_kernel':False,'empirical_experiment':False,'historical_floor':'UNVERIFIED'}
(OUT/'CONTROL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
