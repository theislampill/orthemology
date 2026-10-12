from fractions import Fraction as F
from math import comb,factorial
from pathlib import Path
import json,hashlib

def beta_cdf(a,b,x):
 total=sum(F((-1)**j*comb(b-1,j),a+j)*x**(a+j) for j in range(b))
 norm=F(factorial(a-1)*factorial(b-1),factorial(a+b-1))
 return total/norm

def rising_ratio(a,b,n):
 out=F(1)
 for i in range(n):out*=F(b+i,a+b+i)
 return out

def main():
 geometry=0;posterior=0;moments=0
 for e in [F(1,100),F(1,8),F(1,4)]:
  R0=(1+e)/(1-e);R1=(1+2*e)*(1-e)/((1-2*e)*(1+e))
  for j in range(101):
   q=F(1,2)+e*F(j,100);t=F(1,2)+e-q
   lo=(q*q-F(1,4))/(e*(1+e));hi=(F(1,4)-(1-q)**2)/(e*(1-e))
   lo1=t*(1-2*e+t)/(e*(1-e));hi1=t*(1+2*e-t)/(e*(1+e))
   assert hi<=R0*lo and hi1<=R1*lo1;geometry+=1
   for a,b in [(1,1),(1,2),(2,1),(2,2),(3,4)]:
    for n in [1,2,5,10]:
     L=max(F(0),lo);U=min(F(1),hi)
     mass=beta_cdf(a,b+n,U)-beta_cdf(a,b+n,L) if L<=U else F(0)
     L1=max(F(0),lo1);U1=min(F(1),hi1)
     mass1=beta_cdf(b,a+n,U1)-beta_cdf(b,a+n,L1) if L1<=U1 else F(0)
     assert 0<=mass<=1-R0**(-a) and 0<=mass1<=1-R1**(-b);posterior+=1
 for a,b in [(F(1,2),F(1,2)),(F(1),F(1)),(F(2),F(2)),(F(3,2),F(5,2))]:
  for n in range(1,31):
   m0=rising_ratio(a,b,n);m1=rising_ratio(b,a,n)
   assert 0<m0<=1 and 0<m1<=1
   if a==b==1:assert m0==m1==F(1,n+1)
   moments+=1
 assert F(3,5)+F(5,9)==F(52,45)
 out={'status':'PASS','geometry_cases':geometry,'exact_integer_shape_posterior_cases':posterior,'rational_shape_moment_cases':moments,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite corroboration only; Beta-prior iff is an ordinary integral proof'}
 Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
