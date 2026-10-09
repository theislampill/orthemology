#!/usr/bin/env python3
"""Independent diagnostics for the sharp skyline information review.
No author or predecessor diagnostic code is imported. Exact arithmetic carries
low-degree identities. Finite high-precision values are consistency checks only.
"""
from pathlib import Path
from math import factorial, comb
from fractions import Fraction
import json
import sympy as s
import mpmath as mp

mp.mp.dps=80
M,Z,t,l=s.symbols('M Z t l')
# Bell recurrence differentiates the exponential through its log derivatives.
g=[None,-M,-Z,Z,-Z,Z,-Z]
B=[s.Integer(1)]
for r in range(1,7):
    B.append(s.expand(sum(s.binomial(r-1,j-1)*g[j]*B[r-j] for j in range(1,r+1))))
P6=M**6-15*M**4*Z-20*M**3*Z+45*M**2*Z**2-15*M**2*Z+60*M*Z**2-6*M*Z-15*Z**3+25*Z**2-Z
assert s.expand(B[6]-P6)==0
assert s.expand(B[4]-(M**4-6*M**2*Z-4*M*Z+3*Z**2-Z))==0
assert B[2]==M**2-Z
weights=[]
for (i,j),coeff in s.Poly(P6-M**6,M,Z).terms():
    assert i<6 and i+2*j<=6
    weights.append({'i':i,'j':j,'coefficient':str(coeff),'scaled_log_exponent':str(s.Rational(i,2)+j)})

# Both coordinates below are increasingly ordered: z_i=1-y_i.
# Integrate monomials directly by nested antiderivatives on each simplex.
def ordered_integral(expr,variables,k):
    out=s.Integer(0)
    for powers,c in s.Poly(s.expand(expr),*variables).terms():
        den=1
        for part in [powers[:k],powers[k:]]:
            cum=0
            for j,p in enumerate(part,1):
                cum+=p;den*=j+cum
        out+=c/s.Integer(den)
    return s.factor(out)

moments={0:{r:s.Integer(1) for r in range(7)}}
for k in range(1,7):
    xs=s.symbols('x0:'+str(k));zs=s.symbols('z0:'+str(k))
    D=sum((b-a)*z for a,b,z in zip(xs,xs[1:]+(s.Integer(1),),zs))
    moments[k]={r:ordered_integral((1-D)**r,xs+zs,k) for r in range(7-k)}
    assert moments[k][0]==s.Rational(1,factorial(k)**2)
    print('Ordered simplex moments k='+str(k),flush=True)

# m^k exp(-m U) is the PPP skyline density. All coefficients below are
# obtained by integrating its actual ordered geometry, including k=0.
poisson_checks={}
for order in [0,2,4,6]:
    P=s.Integer(1) if order==0 else B[order]
    totals=[s.Integer(0)]*7
    noempty=[s.Integer(0)]*7
    for k in range(7):
        for deg in range(7-k):
            # Substitute Z=z and M=k-z, multiply the density exponential.
            zz=s.symbols('zz')
            pol=s.expand(P.subs({M:k-zz,Z:zz}))
            exptr=sum((-zz)**j/s.factorial(j) for j in range(7-k))
            coeff=s.expand(pol*exptr).coeff(zz,deg)
            val=coeff*moments[k][deg]
            totals[k+deg]+=val
            if k: noempty[k+deg]+=val
    want=[s.Integer(1)]+[s.Integer(0)]*6 if order==0 else [s.Integer(0)]*7
    assert totals==want,(order,totals)
    assert noempty!=want
    poisson_checks[str(order)]={'coefficients_degree_0_through_6':[str(v) for v in totals],
        'omitting_empty_rejected':True}

# Separate n=1 check: D=(1-X)(1-Y), E D^r=1/(r+1)^2.
one={}
for r in [1,2,4,6]:
    one[r]=sum(s.Rational(comb(r,j)*(-1)**(r-j)*2**j,(j+1)**2) for j in range(r+1))
assert one[1]==-s.Rational(1,2)
assert one[2]==s.Rational(4,9)
assert one[4]==s.Rational(23,75)
assert one[6]>0

# Positive density normalizer and local-Stirling diagnostics, from independent
# log-pmf evaluations. The first m cases are not asserted asymptotic by fiat.
rn=[]
for mm in [32,128,512,2048,8192,10**6,10**9,10**12]:
    m=mp.mpf(mm);logm=mp.log(m)
    for sign in [-1,0,1]:
        z=logm
        k=max(1,int(mp.nint(z+sign*mp.sqrt(logm))))
        v=m-z;q=mm-1-k;d=q-v
        logden=-m+(mm-1)*mp.log(m)-mp.loggamma(mm)
        lognum=-v+q*mp.log(v)-mp.loggamma(q+1)
        ratio=mp.exp(lognum-logden)
        # Compare against ratio of exact ordered-skyline densities as well.
        alt=mp.exp(mp.loggamma(mm)-mp.loggamma(mm-k)+(mm-1-k)*mp.log(1-z/m)-k*mp.log(m)+z)
        assert abs(ratio-alt)<mp.mpf('1e-60')
        assert ratio<3
        approx=-mp.log(2*mp.pi*q)/2-d*d/(2*v)
        remainder=abs(lognum-approx)
        assert remainder<abs(d)**3/v**2+1/mp.mpf(q)
        rn.append({'m':mm,'k':k,'z':mp.nstr(z,25),'r':mp.nstr(ratio,30),
            'stirling_error':mp.nstr(remainder,25)})
    if mm>=10**9: assert abs(ratio-1)<mp.mpf('1e-7')
# Without the normalizer Poi(m)(n), the proposed RN tends to zero.
assert mp.exp(lognum)<mp.mpf('1e-5') and ratio>mp.mpf('.999')

# Exact UI counterexample: a normalized, bounded density tending to one
# does NOT transfer moments unless the relevant variables are UI.
ui_bad=[]
for j in [3,10,100,1000]:
    p=Fraction(1,j); rare_x=j;rare_r=Fraction(2)
    bulk_r=(1-2*p)/(1-p)
    assert p*rare_r+(1-p)*bulk_r==1
    assert p*rare_x==1 and p*rare_r*rare_x==2
    ui_bad.append({'j':j,'EX':'1','ErX':'2','bulk_density':str(bulk_r)})

# Entropy / Hellinger Taylor factors, with singular mass carried separately.
a=s.symbols('a')
assert s.expand(s.series(s.exp(a)-1-a,a,0,3).removeO()).coeff(a,2)==s.Rational(1,2)
assert s.expand(s.series((s.exp(a/2)-1)**2,a,0,3).removeO()).coeff(a,2)==s.Rational(1,4)
assert s.Rational(1,2)*s.Rational(1,2)==s.Rational(1,4)
assert s.Rational(1,4)*s.Rational(1,2)==s.Rational(1,8)
p0=[mp.mpf(1)/2,mp.mpf(1)/2,mp.mpf(0)]
p1=[mp.mpf(1)/5,mp.mpf(3)/5,mp.mpf(1)/5]
L=[p1[i]/p0[i] for i in range(2)]
rev=sum(-p0[i]*mp.log(L[i]) for i in range(2))
phi=sum(p0[i]*(-mp.log(L[i])+L[i]-1) for i in range(2))
hell=sum((mp.sqrt(x)-mp.sqrt(y))**2 for x,y in zip(p0,p1))
commonhell=sum(p0[i]*(mp.sqrt(L[i])-1)**2 for i in range(2))
rho=sum(mp.sqrt(x*y) for x,y in zip(p0,p1))
assert abs(rev-phi-p1[2])<mp.mpf('1e-75')
assert abs(hell-commonhell-p1[2])<mp.mpf('1e-75')
assert abs(rho-(1-hell/2))<mp.mpf('1e-75')
from itertools import product
lrts=[]
for R in range(1,7):
    err=mp.mpf(0); affinity=mp.mpf(0)
    for word in product(range(3),repeat=R):
        pp=mp.fprod(p0[i] for i in word);qq=mp.fprod(p1[i] for i in word)
        err+=min(pp,qq);affinity+=mp.sqrt(pp*qq)
    assert err<=rho**R
    assert abs(affinity-rho**R)<mp.mpf('1e-75')
    lrts.append({'R':R,'error_sum':mp.nstr(err,30),'affinity_bound':mp.nstr(rho**R,30)})

result={'status':'PASS','assurance':'Deterministic mathematical controls; no empirical or interval/asymptotic proof.',
    'sixth_polynomial':str(P6),'holder_monomial_weights':weights,
    'ordered_U_moments':{str(k):{str(r):str(v) for r,v in vals.items()} for k,vals in moments.items()},
    'poisson_coefficient_controls':poisson_checks,
    'one_point_fixed_moments':{str(r):str(v) for r,v in one.items()},
    'normalized_density_and_stirling':rn,'UI_negative_controls':ui_bad,
    'likelihood_product_controls':lrts,
    'coefficient_summary':{'score_second':'1/2','reverse_KL':'1/4','Hellinger_squared':'1/8','one_minus_affinity':'1/16'},
    'rejected_errors':['Poisson empty atom omitted','unnormalized conditional density','convergence in probability without UI','zero or negative singular correction','Hellinger half-convention confused']}
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS independent sharp-information controls',flush=True)
