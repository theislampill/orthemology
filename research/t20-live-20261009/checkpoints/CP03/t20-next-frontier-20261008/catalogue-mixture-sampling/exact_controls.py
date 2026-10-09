#!/usr/bin/env python3
"""Finite exact rational controls, not empirical trials or a general proof."""
from fractions import Fraction as F
from math import comb, prod
import json
from pathlib import Path


def trim(a):
    while len(a)>1 and a[-1]==0: a.pop()
    return a

def add(a,b):
    c=[F(0)]*max(len(a),len(b))
    for k,v in enumerate(a): c[k]+=v
    for k,v in enumerate(b): c[k]+=v
    return trim(c)

def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return trim(c)

def scale(a,t): return trim([x*t for x in a])
def val(a,x): return sum(c*x**r for r,c in enumerate(a))
def deriv(a): return trim([r*a[r] for r in range(1,len(a))] or [F(0)])
def falling(n,r): return prod(range(n-r+1,n+1)) if r<=n else 0

def lagrange(z,i):
    p=[F(1)]
    for j,t in enumerate(z):
        if j!=i: p=scale(mul(p,[-t,F(1)]),1/(z[i]-t))
    return p

def bernstein_poly(R,s):
    p=[F(0)]*s+[F(comb(R,s))]
    for _ in range(R-s): p=mul(p,[F(1),F(-1)])
    return p

def contrasts(a,R):
    return [sum(a[r]*F(falling(s,r),falling(R,r)) for r in range(R+1)) for s in range(R+1)]

def pmf(z,R): return [F(comb(R,s))*z**s*(1-z)**(R-s) for s in range(R+1)]
def mixpmf(z,w,R): return [sum(wj*pj[s] for wj,pj in zip(w,[pmf(t,R) for t in z])) for s in range(R+1)]
def expect(b,p): return sum(x*y for x,y in zip(b,p))
def code(H): return prod((1-F(1,4**e))**n for e,n in H.items())
def ports(e): return [i for i in range(e.bit_length()) if (e>>i)&1]
def actual_code(H,rates): return prod((1-prod(rates[i] for i in ports(e)))**n for e,n in H.items())
def port_beta(H,eps): return min(F(1),sum(n*sum(eps.get(i,F(0)) for i in ports(e)) for e,n in H.items()))
def ss(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,list): return [ss(v) for v in x]
    if isinstance(x,dict): return {str(k):ss(v) for k,v in x.items()}
    return x

records=[]
def passed(name,detail):
    records.append({'control':name,'detail':ss(detail)})
    print('PASS:',name)

catalogues=[
 ('one', [{}], [F(1)]),
 ('two', [{},{1:1}], [F(1,3),F(2,3)]),
 ('three', [{},{1:1},{1:2}], [F(1,3),F(0),F(2,3)]),
 ('four_mixed_routes', [{1:1},{2:1},{1:1,2:1},{3:1}], [F(1,10),F(2,10),F(3,10),F(4,10)]),
 ('five_multiplicities',[{1:j} for j in range(5)],[F(1,5)]*5),
]
for name,H,w in catalogues:
    z=list(map(code,H)); N=len(z); R=N-1
    assert len(set(z))==N and sum(w)==1
    rows=[]; ps=[]
    for i in range(N):
        a=lagrange(z,i); b=contrasts(a,R)
        assert [val(a,t) for t in z]==[F(i==j) for j in range(N)]
        reconstructed=[F(0)]
        for s,c in enumerate(b): reconstructed=add(reconstructed,scale(bernstein_poly(R,s),c))
        assert reconstructed==trim(a[:])
        assert expect(b,mixpmf(z,w,R))==w[i]
        for t in [F(0),F(1,17),F(1,2),F(16,17),F(1)]+z:
            assert expect(b,pmf(t,R))==val(a,t)
        B=max(b)-min(b)
        C=sum(abs(c) for c in a[1:])
        assert B<=C
        if R:
            dd=[R*(b[s+1]-b[s]) for s in range(R)]
            dp=[F(0)]
            for s,c in enumerate(dd): dp=add(dp,scale(bernstein_poly(R-1,s),c))
            assert dp==deriv(a)
            D=max(map(abs,dd))
        else: D=F(0)
        rows.append({'i':i,'a':a,'b':b,'B':B,'C_monomial':C,'D_Bernstein':D})
        ps.append(a)
    assert all(sum(rows[i]['b'][s] for i in range(N))==1 for s in range(R+1))
    if N==1: assert rows[0]['B']==rows[0]['D_Bernstein']==0 and rows[0]['b']==[1]
    passed('catalogue_'+name,{'histograms':H,'z':z,'weights':w,'R':R,'rows':rows})

# Small deterministic calibration perturbations on actual two-port histograms.
H=[{1:1},{2:1},{1:1,2:1},{3:1}]
z=list(map(code,H)); w=[F(1,10),F(2,10),F(3,10),F(4,10)]
rates={0:F(251,1000),1:F(63,1000)}
eps={0:abs(rates[0]-F(1,4)),1:abs(rates[1]-F(1,16))}
actual=[actual_code(h,rates) for h in H]
betas=[port_beta(h,eps) for h in H]; beta=max(betas)
assert all(abs(t-u)<=b for t,u,b in zip(z,actual,betas))
rows=[]
for i in range(4):
    a=lagrange(z,i); b=contrasts(a,3); D=3*max(abs(b[s+1]-b[s]) for s in range(3))
    population=expect(b,mixpmf(actual,w,3)); floor=D*beta
    assert abs(population-w[i])<=D*sum(wj*bj for wj,bj in zip(w,betas))<=floor
    rows.append({'i':i,'population':population,'bias':population-w[i],'D':D,'floor':floor})
passed('port_error_and_calibration_bias',{'rates':rates,'epsilon':eps,'nominal':z,'actual':actual,'beta_j':betas,'beta':beta,'rows':rows})
assert port_beta({3:100},{0:F(1,10),1:F(1,10)})==1
passed('port_error_cap_one',{'raw_sum':20,'capped_beta':1})

# N=2: exact calibration-floor success, strict-boundary failure, and wrong support.
z=[F(1),F(3,4)]; R=1; w=[F(0),F(1)]; threshold=F(1,2)
for rate,label in [(F(7,32),'small_bias'),(F(1,8),'boundary'),(F(1,16),'wrong_support')]:
    actual=[F(1),1-rate]; beta=abs(rate-F(1,4)); D=F(4)
    estimate=[expect(contrasts(lagrange(z,i),R),mixpmf(actual,w,R)) for i in range(2)]
    selected=[i for i,v in enumerate(estimate) if v>threshold]
    assert max(abs(v-t) for v,t in zip(estimate,w))==D*beta
    if label=='small_bias': assert selected==[1] and D*beta<threshold
    if label=='boundary': assert estimate==[F(1,2),F(1,2)] and selected==[] and D*beta==threshold
    if label=='wrong_support': assert estimate==[F(3,4),F(1,4)] and selected==[0] and D*beta>threshold
    passed('calibration_'+label,{'actual_port_rate':rate,'estimate_limit':estimate,'beta':beta,'floor':D*beta,'selected':selected})

# Exhaustive finite sample law, without drawing any samples.
n=4; actual_z=F(3,4); distribution=pmf(actual_z,n)
B=F(4); t=F(1)
tail=sum(p for k,p in enumerate(distribution) if abs((4-F(4*k,n))-1)>=t)
# Hoeffding bound is 2 exp(-1/2); here >1 is loose but legitimate; exact tail retained.
assert tail==F(37,64)
passed('finite_sample_exact_tail_no_simulation',{'n':n,'t':t,'exact_tail':tail,'hoeffding_expression':'2 exp(-1/2), intentionally loose'})

# A concrete support-success sample-size certificate using log(40)<4.
# e^4 > sum_{k=0}^5 4^k/k! > 40, proved with exact rational arithmetic.
from math import factorial
assert sum(F(4**k,factorial(k)) for k in range(6))>40
n=256; B=F(4); beta=F(1,32); floor=4*beta; margin=F(1,2)-floor
# B sqrt(log40/(2n)) < B sqrt(4/(2n)) < margin.
assert B*B*F(4,2*n)<margin*margin
passed('finite_sample_support_certificate',{'delta':F(1,10),'n':n,'B':B,'floor':floor,'margin':margin,'log_upper':4})

# Three-label illustrative budget, certified without floating logarithms.
assert sum(F(5**k,factorial(k)) for k in range(8))>120
n=40000; B=F(50,3); D=F(100,3); beta=F(1,1000); floor=D*beta
margin=F(1,6)-floor
assert floor==F(1,30) and margin==F(2,15)
assert B*B*F(5,2*n)==F(5,288)<margin*margin
assert max(port_beta(h,{0:F(1,2000)}) for h in [{},{1:1},{1:2}])==beta
passed('three_label_disclosed_budget',{'delta':F(1,20),'groups':n,'repeats_per_group':2,'endpoints':80000,'positive_weight_floor':F(1,3),'code_error':beta,'sufficient_port_error':F(1,2000),'worst_B':B,'worst_D':D,'calibration_floor':floor,'remaining_margin':margin,'log120_upper':5})

# Unknown-label separation persists after a fresh rare route is added everywhere.
z=[F(3,4),F(9,16)]; w=[F(1,2),F(1,2)]; gamma=F(1,8); R=3
obstructions=[]
for port in [1,2,3,4]:
    E=2**port; eta=F(1,4**E); shifted=[t*(1-eta) for t in z]
    assert min(abs(shifted[i]-shifted[j]) for i in range(2) for j in range(i))>=gamma
    baseH=[{1:1},{1:2}]; newH=[{**h,E:1} for h in baseH]
    assert list(map(code,newH))==shifted
    assert all(h!=g for h in baseH for g in newH)
    p=mixpmf(z,w,R); q=mixpmf(shifted,w,R)
    tv=sum(abs(a-b) for a,b in zip(p,q))/2
    assert F(0)<tv<=R*eta
    obstructions.append({'new_port':port,'eta':eta,'shifted_z':shifted,'exact_count_TV':tv,'coupling_bound':R*eta})
passed('separated_unknown_labels',{'original_z':z,'gamma':gamma,'weights':w,'R':R,'cases':obstructions})

# Same latent component shared by all groups: the nominal weight estimator does
# not concentrate around population mixture weights as n grows.
z=[F(1),F(3,4)]; w=[F(1,2),F(1,2)]; mean=sum(a*b for a,b in zip(z,w))
varlatent=sum(p*(x-mean)**2 for p,x in zip(w,z))
assert varlatent==F(1,64)
assert 16*varlatent==F(1,4)
passed('cross_group_dependence_obstruction',{'endpoint_covariance_between_groups':varlatent,'asymptotic_contrast_variance':16*varlatent})

out=Path(__file__).parent/'results'/'exact_controls.json'
out.write_text(json.dumps(records,indent=2)+'\n')
print(f'{len(records)} exact rational control families passed. No empirical samples generated.')
