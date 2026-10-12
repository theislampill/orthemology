"""Exact finite corroboration for the ordinary Beta-rate theorem; not a proof."""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib,json

def beta(a,b):
 return F(factorial(a-1)*factorial(b-1),factorial(a+b-1))

def cdf(a,b,x):
 return sum(F((-1)**j*comb(b-1,j),a+j)*x**(a+j) for j in range(b))/beta(a,b)

def interval(q,e):
 return ((q*q-F(1,4))/(e*(1+e)),(F(1,4)-(1-q)**2)/(e*(1-e)))

def main():
 geometry=0;radius=0;coefficient=0;posterior=0;extreme=0;prefix_clock=0
 eps=[F(1,100),F(1,8),F(1,4)]
 for e in eps:
  for j in range(1,40):
   a=F(j,40);v=a*(1-a);r=v*e/4
   exponent=r*r/(2*(v+r/3))
   assert exponent==v*e*e/(32*(1+e/12)) and exponent>=v*e*e/33;coefficient+=1
   for h in [a-r,a,a+r]:
    q=F(1,2)+e*h
    d0=q*q-F(1,4)-a*e*(1+e)
    d1=(1-q)**2-F(1,4)+a*e*(1-e)
    assert d0<0 and d1<0;radius+=1
   for n in range(1,13):
    for k in range(n+1):
     h=F(k,n);q=F(1,2)+e*h
     d0=q*q-F(1,4)-a*e*(1+e)
     d1=(1-q)**2-F(1,4)+a*e*(1-e)
     if d0>0 or d1>0:assert abs(h-a)>r
     prefix_clock+=1
  for n in range(1,17):
   for k in range(n+1):
    lo,hi=interval(F(1,2)+e*F(k,n),e)
    assert 0<=lo<=hi<=1;geometry+=1
   for a,b in [(1,1),(1,2),(2,1),(2,2),(2,4),(4,3)]:
    fail=F(0);total=F(0)
    for k in range(n+1):
     lo,hi=interval(F(1,2)+e*F(k,n),e)
     mass=comb(n,k)*beta(a+k,b+n-k)/beta(a,b)
     success=cdf(a+k,b+n-k,hi)-cdf(a+k,b+n-k,lo)
     assert 0<=success<=1
     total+=mass;fail+=mass*(1-success)
    assert total==1 and 0<=fail<=1
    R0=(1+e)/(1-e);R1=(1+2*e)*(1-e)/((1-2*e)*(1+e))
    m0=beta(a,b+n)/beta(a,b);m1=beta(a+n,b)/beta(a,b)
    assert fail>=R0**(-a)*m0+R1**(-b)*m1
    # A rational weakening of exp(-1) to 1/4 makes a finite check exact.
    lower0=F(1,4)*min(F(1),F(2)**(1-b))/(a*beta(a,b)*(n+1)**a)
    lower1=F(1,4)*min(F(1),F(2)**(1-a))/(b*beta(a,b)*(n+1)**b)
    assert m0>=lower0 and m1>=lower1
    posterior+=1;extreme+=2
    if a==b==1 and e==F(1,4):
     assert fail>=F(52,45)*F(1,n+1)
 for k in range(2,101):
  assert factorial(k)>=2*3**(k-2)
 out={'status':'PASS','report_interval_cases':geometry,'repair_radius_cases':radius,'exponent_constant_cases':coefficient,'fixed_parameter_prefix_checks':prefix_clock,'exact_integrated_empirical_risks':posterior,'extreme_moment_lower_checks':extreme,'factorial_coefficient_checks':99,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite corroboration; all-real concentration, rate and argmax-existence results are ordinary mathematical proofs'}
 Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
