#!/usr/bin/env python3
"""Deterministic exact controls; standard library only, no empirical samples."""
from fractions import Fraction as F
from itertools import product, permutations
from math import comb, factorial
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
results = {}

def record(name, data):
    results[name] = data
    print('PASS', name)

def response(j,a,b):
    return [a,b,a+b-a*b,a*b][j]

def joint(p,q,h=None):
    if h is None: h=p*q
    return {(0,0):1-p-q+h,(0,1):q-h,(1,0):p-h,(1,1):h}

def clean(p): return {k:v for k,v in p.items() if v}
def add(p,q):
    z=dict(p)
    for k,v in q.items():z[k]=z.get(k,F(0))+v
    return clean(z)
def neg(p):return {k:-v for k,v in p.items()}
def sub(p,q):return add(p,neg(q))
def mul(p,q):
    z={}
    for (i,j),v in p.items():
        for (k,l),w in q.items():z[i+k,j+l]=z.get((i+k,j+l),F(0))+v*w
    return clean(z)
def scale(p,c):return clean({k:v*c for k,v in p.items()})
def det(m):
    z={}
    for p in permutations(range(len(m))):
        inv=sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
        term={(0,0):F((-1)**inv)}
        for i,k in enumerate(p):term=mul(term,m[i][k])
        z=add(z,term)
    return z

one={(0,0):F(1)}; a={(1,0):F(1)}; b={(0,1):F(1)}
c=sub(add(a,b),mul(a,b));d=mul(a,b)
assert not sub(add(a,b),add(c,d))
record('one_trial_polynomial_identity',True)

rows=[]
for p,q in [(a,b),(b,a),(c,c),(d,d)]:
    rows.append([mul(sub(one,p),sub(one,q)),mul(sub(one,p),q),mul(p,sub(one,q)),mul(p,q)])
rhs=mul(mul(sub(a,b),sub(add(a,b),scale(mul(a,b),2))),add(mul(sub(a,b),sub(a,b)),scale(mul(mul(a,b),mul(sub(one,a),sub(one,b))),2)))
assert det(rows)==rhs
record('swapped_interior_determinant_polynomial',{'terms':len(rhs),'identity':True})
assert add(rows[0][1],rows[0][2])==add(rows[1][1],rows[1][2])
assert rows[0][0]==rows[1][0] and rows[0][3]==rows[1][3]
record('count_compression_loses_A_B',True)

codes=[(1,0),(0,1),(1,1),(0,0)]
corner_laws=[joint(response(j,F(1),F(0)),response(j,F(0),F(1))) for j in range(4)]
assert all(law[codes[j]]==1 for j,law in enumerate(corner_laws))
record('exact_corner_code_bijection',[list(c) for c in codes])

eta=F(1,48); checks=0; max_error=F(0)
for a1,b1,a2,b2 in product([1-eta,F(1)],[F(0),eta],[F(0),eta],[1-eta,F(1)]):
    for j in range(4):
        p,q=response(j,a1,b1),response(j,a2,b2)
        for h in [max(F(0),p+q-1),min(p,q)]:
            law=joint(p,q,h)
            assert min(law.values())>=0 and sum(law.values())==1
            err=1-law[codes[j]]
            assert err<=2*eta
            max_error=max(max_error,err);checks+=1
record('extreme_frechet_couplings',{'cases':checks,'eta':eta,'largest_error':max_error})

sharp={(1,0):1-2*eta,(0,0):eta,(1,1):eta,(0,1):F(0)}
assert sum(v for (x,y),v in sharp.items() if x)==1-eta
assert sum(v for (x,y),v in sharp.items() if y)==eta
assert 1-sharp[(1,0)]==2*eta>2*eta-eta*eta
record('union_bound_sharp_product_bound_rejected',sharp)

eps=F(1,16)
world0=joint(response(0,1,0),response(0,eps,1))
world1={word:(1-eps)*corner_laws[0][word]+eps*corner_laws[2][word] for word in codes}
assert world0==world1
record('physical_calibration_support_confounding',{'epsilon':eps,'common_law':world0})

for wm in [F(1,2),F(1,3),F(1,4),F(1,10),F(1,100)]:
    beta=wm/8
    assert (1-beta)*wm>=7*wm/8
assert F(9,112)>F(1,16)
record('support_floor_and_chernoff_constants',True)

x=F(211,48)
exp_lower=sum(x**k/F(factorial(k)) for k in range(32))
assert exp_lower>80
record('211_group_budget_exact_exponential_certificate',{'n':211,'w':'1/3','delta':'1/20','positive_taylor_terms':32,'exp_lower_gt_80':True})

def rank(m):
    a=[[F(x) for x in row] for row in m];r=0
    for c in range(len(a[0])):
        k=next((i for i in range(r,len(a)) if a[i][c]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r
z=[F(3,4),F(15,16),F(45,64),F(63,64)]
count2=[[comb(2,s)*q**s*(1-q)**(2-s) for q in z] for s in range(3)]
count3=[[comb(3,s)*q**s*(1-q)**(3-s) for q in z] for s in range(4)]
assert rank(count2)==3 and rank(count3)==4
record('fixed_base4_panel_ranks',{'two_repeat':3,'three_repeat':4})

def polymul(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,v in enumerate(p):
        for j,w in enumerate(q):out[i+j]+=v*w
    return out
Bs=[];contrasts=[]
for i in range(4):
    p=[F(1)]
    for j in range(4):
        if j!=i:p=polymul(p,[-z[j]/(z[i]-z[j]),1/(z[i]-z[j])])
    bs=[sum(p[r]*F(factorial(s)//factorial(s-r),factorial(3)//factorial(3-r)) for r in range(s+1)) for s in range(4)]
    assert all(sum(bs[s]*count3[s][j] for s in range(4))==(i==j) for j in range(4))
    Bs.append(max(bs)-min(bs));contrasts.append(bs)
assert Bs==[F(368),F(1584,5),F(34432,135),F(5504,27)]
record('same_catalogue_base4_exact_contrasts',{'ranges':Bs,'contrasts':contrasts,'claim':'conditioning control only; not minimax comparison'})

def count_hist(a,b):return [a,1-(1-a)**2,1-(1-a)*(1-a*b)]
assert all(len(set(count_hist(F(a),F(b))))==1 for a,b in product([0,1],repeat=2))
assert count_hist(F(1,2),F(1,2))==[F(1,2),F(3,4),F(5,8)]
record('corner_multiplicity_absorption_failure',{'interior':count_hist(F(1,2),F(1,2))})

count=0
for n in range(1,61):
    for k in range(1,100):
        t=F(k,100)
        chi=t**(n-1)*(1-t)/sum(t**j for j in range(n+1))
        assert chi<=F(2,n*(n+1));count+=1
record('uniform_count_chisquare_exact_grid',{'checks':count,'scope':'finite checks of written all-rate proof'})

for K in range(2,101):
    t=1-F(1,K)
    assert t**(K-1)>F(1,3)
    gaps=[t**j/K for j in range(K)]
    assert min(gaps)>F(1,3*K)
record('count_design_exact_minimum_gaps',{'K':list(range(2,101))})

confounds=[]
for K in range(2,13):
    s=1-F(1,K*K); t=s**K;tp=s**(K-1)
    assert t**(K-1)==tp**K and tp>t
    confounds.append({'K':K,'nominal_x':1-t,'other_x':1-tp,'difference':tp-t})
record('rational_count_calibration_confounding',confounds)

w=F(1,4);N=6
p0={seq:F(seq==(0,)*N) for seq in product([0,1],repeat=N)}
p1={seq:w**sum(seq)*(1-w)**(N-sum(seq)) for seq in p0}
overlap=sum(min(p0[s],p1[s]) for s in p0)
assert overlap==(1-w)**N
record('rare_label_oracle_overlap',{'w':w,'n':N,'overlap':overlap})

fresh=[]
for pair in [(0,1),(2,3)]:
    p=sum(response(j,1,0) for j in pair)/F(2)
    q=sum(response(j,0,1) for j in pair)/F(2)
    fresh.append(joint(p,q))
assert fresh[0]==fresh[1]=={word:F(1,4) for word in codes}
record('fresh_resampling_erases_crossed_identity',fresh[0])

def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    return x
(HERE/'results').mkdir(exist_ok=True)
(HERE/'results'/'exact_controls.json').write_text(json.dumps(encode({'passed_families':len(results),'results':results}),indent=2)+'\n')
print('ALL',len(results),'EXACT CONTROL FAMILIES PASS')
