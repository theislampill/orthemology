#!/usr/bin/env python3
"""Exact replay/finite-grid controls, not empirical sampling or a copula search proof."""
from fractions import Fraction as F
from itertools import product
from collections import Counter,defaultdict
from pathlib import Path
import json

counts=Counter()
def check(x,family):
    assert x,family
    counts[family]+=1

def prod(xs):
    a=F(1)
    for x in xs:a*=x
    return a

def pmul(p,q):
    r=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):r[i+j]+=a*b
    return r

def peval(p,x):
    v=F(0)
    for c in reversed(p):v=v*x+c
    return v

def pder(p):return [i*p[i] for i in range(1,len(p))]

def perturbation(coords):
    p=[F(0),F(1),F(-1)]
    for a in coords:
        if 0<a<1:p=pmul(p,[-a,F(1)])
    d=pder(p); M=sum(abs(v) for v in d)
    return p,d,M

def cell(C,a0,a1,b0,b1):return C(a1,b1)-C(a0,b1)-C(a1,b0)+C(a0,b0)

# Formal coefficient arithmetic: no derivative of unknown joint law occurs here.
for n,m in product(range(1,17),repeat=2):
    c=F(n,m); u1=c;u2=c*(1-c)/2
    linear=-2*m*u1
    quadratic=-2*m*u2+n-2*m*u1*u1
    check(linear==-2*n,'replay_log_linear_coefficient')
    check(quadratic==-n*c,'replay_log_quadratic_coefficient')
    check((quadratic==-n)==(m==n),'second_order_count_rigidity')
    check((n*(1-c)>0)==(m>n),'second_order_discrepancy_sign')

# Probability-only estimates used in the nonsmooth argument.
for vals in product([F(i,16) for i in range(9)],repeat=3):
    Q=prod(1-d for d in vals)
    for d in vals:check(d<=1-Q,'each_joint_bounded_by_total_hit')
    # Union/product remainder bounded by sum of pair products.
    s=sum(vals)
    check(0<=s-(1-Q)<=sum(vals[i]*vals[j] for i in range(3) for j in range(i+1,3)),
          'product_to_sum_quadratic_remainder')

# Exhaustive exact pointwise AM-GM rigidity diagnostics in valid Bernoulli tables.
rigidity=[]
settings=[(F(1,2),F(1,2),16,4),(F(1,3),F(2,3),36,3),(F(1,4),F(1,4),16,3)]
for a,b,den,maxn in settings:
    options=[F(k,den) for k in range(den+1) if max(F(0),a+b-1)<=F(k,den)<=min(a,b)]
    for n in range(1,maxn+1):
        accepted=[]
        for ds in product(options,repeat=n):
            q=prod(1-d for d in ds);j=prod(1-a-b+d for d in ds)
            match=(q==(1-a*b)**n and j==((1-a)*(1-b))**n)
            check(not match or all(d==a*b for d in ds),'pointwise_two_product_rigidity')
            if match:accepted.append(ds)
        check(accepted==[(a*b,)*n],'pointwise_unique_grid_solution')
        rigidity.append({'a':str(a),'b':str(b),'n':n,'table_candidates':len(options)**n,'solutions':len(accepted)})

# Genuine smooth positive-density non-independent copula invisible on a finite grid.
grid=[F(i,4) for i in range(5)]
p,dp,M=perturbation(grid);q,dq,N=perturbation(grid)
eps=1/(2*M*N)
base=lambda a,b:a*b
C=lambda a,b:a*b+eps*peval(p,a)*peval(q,b)
check(eps*M*N==F(1,2),'global_density_lower_bound_certificate')
for x in grid:
    check(peval(p,x)==0 and peval(q,x)==0,'perturbation_grid_zeros')
for a,b in product(grid,repeat=2):
    check(C(a,b)==a*b,'copula_CDF_grid_match')
for a,b in product([F(i,32) for i in range(33)],repeat=2):
    density=1+eps*peval(dp,a)*peval(dq,b)
    check(density>=F(1,2),'density_grid_diagnostic')
    check(C(a,0)==0 and C(0,b)==0 and C(a,1)==a and C(1,b)==b,'uniform_margins_and_grounding')
for a0,a1 in zip(grid,grid[1:]):
    for b0,b1 in zip(grid,grid[1:]):
        check(cell(C,a0,a1,b0,b1)==(a1-a0)*(b1-b0),'all_threshold_grid_cells_equal')
off=(F(1,8),F(3,8));delta=C(*off)-base(*off)
check(delta!=0,'off_grid_nonindependence')

# Full fixed-threshold transcript law on the finite command panel.
commands=list(product(grid[1:],repeat=2))
def route_transcript_distribution(cop):
    d=defaultdict(F)
    for a0,a1 in zip(grid,grid[1:]):
        for b0,b1 in zip(grid,grid[1:]):
            x,y=(a0+a1)/2,(b0+b1)/2
            mask=sum(1<<k for k,(a,b) in enumerate(commands) if x<=a and y<=b)
            d[mask]+=cell(cop,a0,a1,b0,b1)
    return dict(d)
def combine(d,e):
    r=defaultdict(F)
    for mask,pv in d.items():
        for mask2,qv in e.items():r[mask|mask2]+=pv*qv
    return dict(r)
r0,r1=route_transcript_distribution(base),route_transcript_distribution(C)
check(r0==r1,'single_route_full_panel_transcript_equal')
d0=d1={0:F(1)}; transcript_sizes=[]
for n in range(1,5):
    d0=combine(d0,r0);d1=combine(d1,r1)
    check(d0==d1,'multi_route_full_panel_transcript_equal')
    check(sum(d0.values())==1,'full_panel_transcript_total_mass')
    transcript_sizes.append({'n':n,'possible_response_words':len(d0)})

# Exact high-command count alias. All three held-threshold bits match.
t=F(3,4);u=v=F(1,2);D=[F(1,2),F(1,8)]
check((1-u)**2==1-t and (1-v)**2==1-t,'high_panel_face_alias')
check(prod(1-d for d in D)==1-t*t==F(7,16),'high_panel_fresh_alias')
check(prod(1-u-v+d for d in D)==(1-t)**2==F(1,16),'high_panel_paired_alias')
first={(1,1):F(1,2),(0,0):F(1,2)}
second={(1,1):F(1,8),(1,0):F(3,8),(0,1):F(3,8),(0,0):F(1,8)}
alt=defaultdict(F)
for (A,B),pa in first.items():
    for (AA,BB),pb in second.items():
        bits=(int(A or AA),int(B or BB),int((A and B) or (AA and BB)))
        alt[bits]+=pa*pb
expected={(0,0,0):F(1,16),(1,0,0):F(3,16),(0,1,0):F(3,16),(1,1,1):F(9,16)}
check(dict(alt)==expected,'high_panel_entire_three_bit_replay_alias')

# Joe n=1,m=2 midpoint: exact rational radical certificate.
# J=11/4-sqrt(6); 2449/1000 < sqrt(6) < 49/20.
lo,hi=F(2449,1000),F(49,20)
check(lo*lo<6<hi*hi,'Joe_sqrt6_rational_bracket')
Jlo,Jhi=F(11,4)-hi,F(11,4)-lo
check(Jlo>F(1,4) and Jhi<F(1,2),'Joe_replay_strict_separation')
check(F(5,2)**2>6,'Joe_exact_gap_sign')
Q=F(3,4);face=F(1,2)
check(face*face==F(1,4),'fresh_threshold_faces_erase_separation')
check(Q!=Q*Q and Q==F(3,4),'same_command_replay_is_one_bit')

# Baseline paired laws are valid for multiple counts and rates.
for n,a,b in product(range(1,6),[F(i,8) for i in range(1,8)],[F(i,8) for i in range(1,8)]):
    A=(1-a)**n; B=(1-b)**n;J=((1-a)*(1-b))**n
    table=(J,A-J,B-J,1-A-B+J)
    check(all(p>=0 for p in table) and sum(table)==1,'baseline_paired_law_valid')
    check(J==A*B,'baseline_face_pair_independence')

out={'status':'PASS','arithmetic':'Python Fraction only; analytic radical comparisons through squared rationals',
     'assertions':sum(counts.values()),'families':dict(counts),'pointwise_grid_audits':rigidity,
     'perturbed_copula':{'grid':[str(x) for x in grid],'f_coefficients':[str(x) for x in p],
       'g_coefficients':[str(x) for x in q],'derivative_bounds':[str(M),str(N)],'epsilon':str(eps),
       'certified_density_lower_bound':'1/2','off_grid_point':[str(x) for x in off],'off_grid_difference':str(delta)},
     'transcript_sizes':transcript_sizes,'high_panel_three_bit_law':{str(k):str(v) for k,v in expected.items()},
     'Joe_midpoint_paired_interval':[str(Jlo),str(Jhi)],
     'scope':'No finite global copula certification, no universal finite count impossibility, no physical replay validation.'}
HERE=Path(__file__).resolve().parent
(HERE/'results'/'exact_controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','assertions','families']},indent=2))
