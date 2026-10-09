#!/usr/bin/env python3
"""Reviewer-derived exact controls; does not import or execute author code.

Independent methods: nonnegative power-series mixture certificates, factored
rectangle polynomials, explicit uniform rational converse witnesses, and
integer power identities. Finite checks supplement the proofs in REVIEW.md.
"""
from fractions import Fraction as Q
from pathlib import Path
from collections import Counter
from itertools import combinations, product
import json

checks = Counter()
def verify(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] += 1

def mixture_weights(c, terms):
    w = c
    out = []
    for k in range(1, terms + 1):
        out.append(w)
        w = w * (k - c) / (k + 1)
    return out

cs = [Q(1,7), Q(2,7), Q(3,5), Q(4,5), Q(1)]
grid = [Q(0), Q(1,5), Q(2,5), Q(4,5), Q(1)]
mixture_records = []
for c in cs:
    weights = mixture_weights(c, 24)
    for k, w in enumerate(weights, 1):
        verify('nonnegative_mixture_coefficient', w >= 0)
        verify('strict_mixture_coefficient_unless_independence', w > 0 if c < 1 else w == (1 if k == 1 else 0))
    mass = sum(weights)
    verify('partial_mixture_total_mass', 0 < mass <= 1)
    for a, b in product(grid[1:-1], repeat=2):
        cells = [Q(0), Q(0), Q(0), Q(0)]
        for k, w in enumerate(weights, 1):
            ak, bk = a**k, b**k
            for index, term in enumerate((ak*bk, ak*(1-bk), (1-ak)*bk, (1-ak)*(1-bk))):
                cells[index] += w * term
        for cell in cells:
            verify('positive_independent_mixture_cell_lower_bound', cell > 0)
        verify('mixture_cells_exact_total', sum(cells) == mass)
        verify('mixture_A_marginal_exact', cells[0]+cells[1] == sum(w*a**k for k,w in enumerate(weights,1)))
        verify('mixture_B_marginal_exact', cells[0]+cells[2] == sum(w*b**k for k,w in enumerate(weights,1)))
    smallest = None
    for (a0,a1),(b0,b1) in product(combinations(grid,2), repeat=2):
        lower = sum(w*(a1**k-a0**k)*(b1**k-b0**k) for k,w in enumerate(weights,1))
        verify('positive_rectangle_mixture_lower_bound', lower > 0)
        smallest = lower if smallest is None else min(smallest,lower)
    mixture_records.append({'c':str(c),'terms':24,'partial_total':str(mass),'smallest_rectangle_lower_bound':str(smallest)})

# Independent polynomial factorization of every c=2 rectangle.
def surface2(a,b):
    return 2*a*b-a*a*b*b
def difference2(a0,a1,b0,b1):
    return surface2(a1,b1)-surface2(a0,b1)-surface2(a1,b0)+surface2(a0,b0)
def factor2(a0,a1,b0,b1):
    return (a1-a0)*(b1-b0)*(2-(a0+a1)*(b0+b1))
rgrid = [Q(i,8) for i in range(9)]
for (a0,a1),(b0,b1) in product(combinations(rgrid,2), repeat=2):
    verify('c2_exact_rectangle_factorization', difference2(a0,a1,b0,b1)==factor2(a0,a1,b0,b1))
verify('c2_upper_rectangle',factor2(Q(3,4),Q(1),Q(3,4),Q(1))==Q(-17,256))
verify('c2_interior_rectangle',factor2(Q(3,4),Q(7,8),Q(3,4),Q(7,8))==Q(-41,4096))
verify('c2_lower_rectangle',factor2(Q(0),Q(1,2),Q(0),Q(1,2))==Q(7,16))
j=surface2(Q(3,4),Q(3,4)); u=surface2(Q(3,4),Q(1))
verify('c2_exact_invalid_table',(j,u-j,u-j,1-2*u+j)==tuple(Q(x,256) for x in (207,33,33,-17)))

# Radical certification at c=1/2 using squared rational brackets only.
s2lo,s2hi,s3lo,s3hi=Q(7,5),Q(10,7),Q(12,7),Q(7,4)
verify('sqrt2_bracket',s2lo*s2lo<2<s2hi*s2hi)
verify('sqrt3_bracket',s3lo*s3lo<3<s3hi*s3hi)
verify('c_half_p11_positive',1-s3hi/2>0)
verify('c_half_p10_p01_positive',(s3lo-s2hi)/2>0)
verify('c_half_p00_positive',s2lo-s3hi/2>0)
verify('c_half_covariance_positive',s2lo-s3hi/2-Q(1,2)>0)
verify('c_half_endpoint_square',Q(3,4)==1-Q(1,2)*Q(1,2))

# Distinct rational witness selection, no root interval routine.
transport = []
for n in range(1,17):
    for m in range(n,17):
        c=Q(n,m); p,q=c.numerator,c.denominator
        t=Q(2,3); z=1-t**q; a=(1+z)/2; b=z/a; J=1-t**p
        verify('transport_commands_interior',0<a<1 and 0<b<1)
        verify('transport_joint_defining_power',(1-J)**q==(1-a*b)**p)
        verify('transport_endpoint_exact',(1-J)**m==(1-a*b)**n)
        transport.append({'n':n,'m':m,'a':str(a),'b':str(b),'J':str(J),'Q':str((1-J)**m)})

# All m<n have the single explicit choice epsilon=1/(2n).
# Bernoulli: (1-1/(4n))^n >= 3/4 > 1/2, hence
# (2-epsilon)^n > 2^(n-1) >= 2^m. No unknown copula enters.
converse=[]
for n in range(2,61):
    epsilon=Q(1,2*n)
    verify('uniform_epsilon_Bernoulli_lower_bound',(1-Q(1,4*n))**n>=Q(3,4))
    for m in range(1,n):
        lhs=(2-epsilon)**n
        verify('homogeneous_negative_table_power_certificate',lhs>2**m)
        target=(epsilon*(2-epsilon))**n
        upper=2**m*epsilon**n
        verify('heterogeneous_product_bound_contradiction',target>upper)
        converse.append({'n':n,'m':m,'epsilon':str(epsilon),'target_over_bound':str(target/upper)})

# Joe product-form algebra after naming x=(1-u)^theta, y=(1-v)^theta.
for x,y in product(rgrid,repeat=2):
    verify('Joe_inside_expression',1-(1-x)*(1-y)==x+y-x*y)
    verify('Joe_independence_boundary',1-(x+y-x*y)==(1-x)*(1-y))

# Semantic controls concern different probability laws/assumptions.
a,b=Q(2,5),Q(3,7)
verify('shared_AB_duplicates_collapse',(1-a*b)!=(1-a*b)**2)
verify('shared_A_absorbs_AB',(1-a)!=(1-a)*(1-a*b))
crossA=lambda a,b:a*(2-a*b)/(2-b)
crossB=lambda b:b*(2-b)
verify('cross_talk_retains_product_joint',crossA(a,b)*crossB(b)==surface2(a,b))
verify('cross_talk_changes_A_with_B',crossA(a,Q(1,3))!=crossA(a,Q(2,3)))
verify('route_dependence_breaks_product_bound',Q(1,4)>Q(1,4)**2)
# Unequal exponents on margins still fit the two endpoint products; they
# destroy the shared-marginal per-route bound. This is not a full model.
eps=Q(1,4)
verify('occurrence_specific_margins_not_forced_equal',eps*eps**2==eps**3 and eps!=eps**2)
verify('unequal_margin_bound_no_longer_excludes_target',(eps+eps**2)**2>(eps*(2-eps))**3)

out={'status':'PASS','assertions':sum(checks.values()),'families':dict(checks),
     'arithmetic':'Exact integers and Fraction arithmetic only; no simulations or floating-point tests.',
     'mixture_controls':mixture_records,'transport_witnesses':transport,'converse_witnesses':converse,
     'scope':'Independent finite controls supplement general proofs in REVIEW.md. The replay is separate supplementary evidence.'}
dest=Path(__file__).resolve().parent/'results'/'independent_controls.json'
dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','assertions','families']},indent=2))
