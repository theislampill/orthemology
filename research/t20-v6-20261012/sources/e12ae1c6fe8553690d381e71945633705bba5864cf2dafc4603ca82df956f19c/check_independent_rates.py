#!/usr/bin/env python3
"""Exact finite countercontrols for an ordinary all-real rate theorem.
Uses a binomial-tail CDF, unlike the author's alternating integral expansion.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb,factorial
from itertools import product
import json,hashlib
BASE=Path(__file__).resolve().parents[1]
def beta(a,b):return F(factorial(a-1)*factorial(b-1),factorial(a+b-1))
def cdf(a,b,x):
 N=a+b-1
 return sum(F(comb(N,j))*x**j*(1-x)**(N-j) for j in range(a,N+1))
def interval(q,e):return (q*q-F(1,4))/(e*(1+e)),(F(1,4)-(1-q)**2)/(e*(1-e))
def accepted(alpha,e,q):return q*q-F(1,4)-alpha*e*(1+e)<=0 and (1-q)**2-F(1,4)+alpha*e*(1-e)<=0

def moment(a,b,n,ones=False):
 x=F(1)
 for j in range(n):x*=((a if ones else b)+j)/(a+b+j)
 return x
counts={'radius_cases':0,'bernstein_coefficient_cases':0,'moment_majorants':0,'posterior_report_lower_cases':0,'integrated_empirical_risks':0,'exact_lower_rate_cases':0,'integer_tail_identities':0,'fractional_shape_moment_cases':0,'uniform_argmax_square_identities':0}
for e in [F(1,100),F(1,7),F(1,4)]:
 for a0 in [F(j,37) for j in range(1,37)]:
  v=a0*(1-a0);r=v*e/4;coef=r*r/(2*(v+r/3))
  assert coef==v*e*e/(32*(1+e/12)) and coef>=v*e*e/33;counts['bernstein_coefficient_cases']+=1
  for h in [a0-r,a0,a0+r]:assert accepted(a0,e,F(1,2)+e*h);counts['radius_cases']+=1
  for k in range(2,33):
   absolute_moment=a0*(1-a0)**k+(1-a0)*a0**k
   assert absolute_moment<=v and factorial(k)>=2*3**(k-2);counts['moment_majorants']+=1
 for a,b in [(1,1),(1,3),(3,1),(2,2),(2,3),(3,2)]:
  R0=(1+e)/(1-e);R1=(1+2*e)*(1-e)/((1-2*e)*(1+e))
  for n in range(1,13):
   for j in range(25):
    q=F(1,2)+e*F(j,24);lo,hi=interval(q,e)
    assert 0<=lo<=hi<=1
    s0=cdf(a,b+n,hi)-cdf(a,b+n,lo)
    s1=cdf(a+n,b,hi)-cdf(a+n,b,lo)
    assert s0<=1-R0**(-a) and s1<=1-R1**(-b)
    counts['posterior_report_lower_cases']+=2
   risk=F(0);masssum=F(0)
   for k in range(n+1):
    q=F(1,2)+e*F(k,n);lo,hi=interval(q,e)
    mass=F(comb(n,k))*beta(a+k,b+n-k)/beta(a,b);masssum+=mass
    risk+=mass*(1-cdf(a+k,b+n-k,hi)+cdf(a+k,b+n-k,lo))
   assert masssum==1
   M0=moment(F(a),F(b),n);M1=moment(F(a),F(b),n,True)
   assert risk>=R0**(-a)*M0+R1**(-b)*M1
   # e^(-1)>1/3 gives a rational weakening of the displayed lower constants.
   c0=F(1,3)*min(F(1),F(2)**(1-b))/(a*beta(a,b)*2**a)
   c1=F(1,3)*min(F(1),F(2)**(1-a))/(b*beta(a,b)*2**b)
   assert M0>=c0/F(n)**a and M1>=c1/F(n)**b;counts['exact_lower_rate_cases']+=2
   # The all-real upper constant is rational at integer shapes.
   t=e*e/66
   upper=2/beta(a,b)*(max(F(1),F(2)**(1-b))*factorial(a-1)/(t*n)**a+max(F(1),F(2)**(1-a))*factorial(b-1)/(t*n)**b)
   assert risk<=upper;counts['integrated_empirical_risks']+=1
# The uniform-prior, zero-observation argmax is exact, not a grid estimate.
e=F(1,4);qstar=F(1,2)+e/2;maximum=e/(2*(1-e*e))
for j in range(65):
 x=e*F(j,64);lo,hi=interval(F(1,2)+x,e)
 assert maximum-(hi-lo)==2*(x-e/2)**2/(e*(1-e*e));counts['uniform_argmax_square_identities']+=1
assert maximum==F(2,15) and 1-maximum==F(13,15)
# The empirical action at n=1 is always an endpoint report and fails a.s.
# Ignoring the receipt and using qstar already improves it, refuting exact
# Bayes optimality while leaving order optimality untouched.
empirical_n1=F(1);constant_n1=1-maximum;assert constant_n1<empirical_n1
# The two extreme histories are disjoint only for n>=1. At n0 this forged
# combined lower bound exceeds1 under the uniform prior.
R0=F(5,3);R1=F(9,5);assert R0**(-1)+R1**(-1)==F(52,45)>1
# CDF scaling itself cannot drop the nonnegative complementary exponent.
# Beta(1,1/2) has F(x)=1-sqrt(1-x). At z=1,R=5/3,
# F(z/R)<R^-1 F(z), equivalently sqrt(2/5)>2/5.
assert F(2,5)>F(2,5)**2
# Exact telescoping prior tails: a=2,b=3 distinguishes both endpoint powers.
for N in range(1,41):
 for M in [N+1,N+7,N+40]:
  m0=sum(moment(F(2),F(3),n) for n in range(N+1,M+1))
  m1=sum(moment(F(2),F(3),n,True) for n in range(N+1,M+1))
  assert m0==F(12,N+4)-F(12,M+4)
  assert m1==F(12,(N+3)*(N+4))-F(12,(M+3)*(M+4));counts['integer_tail_identities']+=2
# Rational noninteger Beta shapes still have exact moment recurrences.
for n in range(10,101):
 x=moment(F(1,2),F(2),n);y=moment(F(1,2),F(2),2*n)
 assert F(2,5)<(y/x)**2<F(3,5)
 assert x==moment(F(2),F(1,2),n,True);counts['fractional_shape_moment_cases']+=1
# A fixed latent parameter mixed once is not a fresh iid averaged source.
assert moment(F(1),F(1),2)==F(1,3)!=F(1,2)**2
# A deterministic posterior-conditioned continuation differs from the
# unconditional fixed-cutoff tail: uniform prior, history01 =>Beta(2,2).
assert beta(2,2)/beta(1,1)==F(1,6)
assert 2*beta(2,2)/beta(1,1)==F(1,3)
assert beta(1,2)/beta(2,2)+beta(2,1)/beta(2,2)==6
# Clock controls: repeated prefixes do not create observations; geometric
# sample counts make the extreme-prefix series summable under uniform prior.
for J in range(1,31):
 assert sum(F(1,2**j) for j in range(1,J+1))==1-F(1,2**J)
 assert sum(F(1,2**j+1) for j in range(1,J+1))<=1
for n in range(1,41):assert moment(F(1),F(1),n)==F(1,n+1)
result={'status':'PASS_FRESH_INDEPENDENT_FINITE_BETA_RATE_CONTROLS',**counts,'uniform_initial_bayes_report':'5/8','uniform_initial_success':'2/15','empirical_n1_failure':'1','constant_report_n1_failure':'13/15','zero_index_double_count_counterexample':'52/45 > 1','fixed_mixture_not_iid_counterexample':'P(00)=1/3, whereas iid fair gives1/4','posterior_tail_counterexample':'Uniform prior after01 is Beta(2,2), with inverse moment6; unconditional deterministic-cutoff tail is still infinite.','clock_scope':'Nondecreasing deterministic positive sample counts; no adaptive stopping or erasure of required reports.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite corroboration and countercontrols; all-real concentration, universal rate/argmax statements and infinite series conclusions are ordinary proofs.'}
(BASE/'evidence/INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
