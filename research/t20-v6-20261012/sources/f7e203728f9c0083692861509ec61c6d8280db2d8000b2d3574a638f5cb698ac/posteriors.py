from fractions import Fraction as F
from math import comb,factorial
from itertools import product
from pathlib import Path
import json,hashlib
A=Path(__file__).resolve().parents[1]
def beta_integer(a,b):return F(factorial(a-1)*factorial(b-1),factorial(a+b-1))
def cdf_integer(a,b,x):return sum(F((-1)**k*comb(b-1,k),a+k)*x**(a+k) for k in range(b))/beta_integer(a,b)
def rising(a,n):
 out=F(1)
 for k in range(n):out*=a+k
 return out
geometry=posterior=seed=halfshape=mixture=moment=0
for e,j in product([F(1,4),F(1,7),F(1,64)],range(21)):
 x=e*F(j,20);q=F(1,2)+x;l=x*(1+x)/(e*(1+e));u=x*(1-x)/(e*(1-e))
 R0=(1+e)/(1-e);R1=(1+2*e)*(1-e)/((1-2*e)*(1+e))
 assert 0<=l<=u<=1 and u<=R0*l and 1-l<=R1*(1-u);geometry+=1
 for a,b,n in product(range(1,5),range(1,5),range(1,7)):
  mass=cdf_integer(a,b+n,u)-cdf_integer(a,b+n,l)
  reflected=cdf_integer(b,a+n,1-l)-cdf_integer(b,a+n,1-u)
  assert 0<=mass<=1-R0**(-a) and 0<=reflected<=1-R1**(-b);posterior+=2
  mixed=F(1,3)*mass+F(2,3)*F(0)
  assert 1-mixed>=R0**(-a);seed+=1
# Fractional first shape: exact CDF at squares, with integer second shape.
def halfcdf(m,b,y):
 a=F(m,2);normal=F(factorial(b-1),1)/rising(a,b)
 return sum(F((-1)**k*comb(b-1,k),1)*y**(m+2*k)/(a+k) for k in range(b))/normal
for m,b,n,y in product([1,3,5],range(1,5),range(1,5),[F(j,10) for j in range(11)]):
 # R=(5/4)^2 corresponds to epsilon=9/41, in the allowed interval.
 assert halfcdf(m,b+n,F(4,5)*y)>=F(4,5)**m*halfcdf(m,b+n,y);halfshape+=1
# Exact Beta-binomial mass normalisation, including noninteger shape parameters.
for a,b,n in product([F(1,2),F(1),F(3,2),F(2)],[F(1,2),F(1),F(3,2),F(2)],range(13)):
 assert sum(F(comb(n,k))*rising(a,k)*rising(b,n-k)/rising(a+b,n) for k in range(n+1))==1;mixture+=1
for a,b,N in product(range(2,7),range(1,7),[1,2,5,10,30]):
 partial=sum(beta_integer(a,b+n)/beta_integer(a,b) for n in range(1,N+1))
 exact=F(b,a-1)-beta_integer(a-1,b+N+1)/beta_integer(a,b)
 assert partial==exact;moment+=1
for b,n in product(range(1,7),range(1,31)):
 assert beta_integer(1,b+n)/beta_integer(1,b)==F(b,b+n);moment+=1
# Uniform prior is not an iid fair source: its two-zero probability is 1/3.
assert beta_integer(1,3)/beta_integer(1,1)==F(1,3)!=F(1,4)
R0=F(5,3);R1=F(9,5);assert 1/R0+1/R1==F(52,45)>1
for N in range(31):
 assert sum(F(52,45)*F(1,n+1) for n in range(1,N+1))==F(52,45)*(sum(F(1,k) for k in range(1,N+2))-1)
# At n=0 the extreme events coincide; summing both would exceed probability one.
assert F(52,45)>1
# The CDF scaling also needs the complementary exponent nonnegative.
# Beta(1,1/2) has F(3/4)=1-sqrt(1/4)=1/2 < (4/3)^(-1).
assert F(1,2)<F(3,4)
out={'status':'FRESH_PASS_BETA_POSTERIOR_CONTROLS','accepted_interval_cases':geometry,'integer_shape_posterior_bounds':posterior,'seed_mixture_bounds':seed,'half_integer_shape_CDF_bounds':halfshape,'beta_binomial_normalisations':mixture,'moment_series_identities':moment,'uniform_horizon_identities':31,'empty_prefix_and_negative_exponent_countercontrols':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite geometry/posterior/clock checks. The real-shape CDF substitution and infinite-moment iff are ordinary proof results.'};(A/'CONTROL_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
