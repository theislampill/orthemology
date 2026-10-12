#!/usr/bin/env python3
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parents[1]

def bounds(q,e):
 return ((q*q-F(1,4))/(e*(1+e)),(F(1,4)-(1-q)**2)/(e*(1-e)))
def good(alpha,q,e):
 return 0<=q<=1 and q*q-F(1,4)-alpha*e*(1+e)<=0 and (1-q)**2-F(1,4)+alpha*e*(1-e)<=0

def beta_integral(i,j,l,u):
 if u<=l:return F(0)
 return sum((F((-1)**k*comb(j,k),i+k+1)*(u**(i+k+1)-l**(i+k+1)) for k in range(j+1)),F(0))
def bad_integral(i,j,l,u,q,e):
 full=beta_integral(i,j,l,u)
 if not 0<=q<=1:return full
 lo,hi=bounds(q,e)
 return full-beta_integral(i,j,max(l,lo),min(u,hi))

interval=likelihood=weighted=endpoint=perstep=mixtures=0
for e in [F(1,8),F(1,4)]:
 R0=(1+e)/(1-e);R1=(1+2*e)*(1-e)/((1-2*e)*(1+e))
 reports=[F(-1),F(0),F(1),F(2)]+[F(1,2)+e*F(k,32) for k in range(33)]
 for a in [1,2,3,4]:
  for n in range(1,25):
   t=min(F(1,4),F(1,n+1))
   assert (1-t)**n>=F(1,3);likelihood+=1
   for q in reports:
    missed=bad_integral(a-1,0,0,t,q,e)
    assert missed>=t**a/(a*R0**a)
    # Transform high endpoint beta=1-alpha; acceptance endpoints reverse.
    if 0<=q<=1:
     lo,hi=bounds(q,e);captured=beta_integral(a-1,0,max(F(0),1-hi),min(t,1-lo))
    else:captured=F(0)
    assert t**a/a-captured>=t**a/(a*R1**a);interval+=2
    # The actual all-zero weighted source mass dominates the rational lower.
    mass=bad_integral(a-1,n,0,t,q,e)
    assert mass>=F(1,3)*t**a/(a*R0**a);weighted+=1

# Piecewise power densities, arbitrary interior atom and endpoint atoms.
# These are not globally Beta laws. All probability calculations are exact.
for a in [1,2,3]:
 for b in [1,2,3]:
  for e in [F(1,8),F(1,4)]:
   eta=F(1,4)
   segs=[(a-1,0,F(0),eta/2,F(1)),(a-1,0,eta/2,eta,F(2)),(0,b-1,1-eta,1-eta/2,F(2)),(0,b-1,1-eta/2,F(1),F(1))]
   atoms=[(F(0),F(1)),(F(1,2),F(3)),(F(1),F(2))]
   Z=sum((w*beta_integral(i,j,l,u) for i,j,l,u,w in segs),F(0))+sum(w for _,w in atoms)
   c=1/Z;R0=(1+e)/(1-e);R1=(1+2*e)*(1-e)/((1-2*e)*(1+e))
   def word_bad(n,k,q):
    v=sum((w*bad_integral(i+k,j+n-k,l,u,q,e) for i,j,l,u,w in segs),F(0))
    v+=sum((w*x**k*(1-x)**(n-k) for x,w in atoms if not good(x,q,e)),F(0))
    return v/Z
   reports=[F(1,2)+e*F(k,16) for k in range(17)]
   for n in range(1,17):
    t=min(eta,F(1,n+1));lower=c*F(1,3)*(t**a/(a*R0**a)+t**b/(b*R1**b))
    # An arbitrary seed mixture cannot beat the two separate prefix minima.
    zmin=min(word_bad(n,0,q) for q in reports);omin=min(word_bad(n,n,q) for q in reports)
    assert zmin+omin>=lower
    mixed=sum((word_bad(n,0,q)+word_bad(n,n,q) for q in reports),F(0))/len(reports)
    assert mixed>=lower;mixtures+=1
    empirical=sum((comb(n,k)*word_bad(n,k,F(1,2)+e*F(k,n)) for k in range(n+1)),F(0))
    assert empirical>=lower and empirical<=1;perstep+=1
    for x in [F(0),F(1)]:
     assert good(x,F(1,2)+e*x,e);endpoint+=1
# Named scope countercontrols.
# A pure interior atom has no asserted positive endpoint-density lower bound.
assert good(F(1,2),F(1,2)+F(1,4)*F(1,2),F(1,4))
# A constant posterior failure floor is false in the presence of an endpoint atom.
posterior_atom=[]
for n in [1,5,20,1000]:
 risk=F(1,99*(n+1)+1)
 assert risk<F(1,100) and risk==F(1,100*(n+1))/(F(99,100)+F(1,100*(n+1)))
 posterior_atom.append(str(risk))
# The missing mass is not always just the lower interval; q0 has l=0.
lo,hi=bounds(F(1,2),F(1,4));assert lo==hi==0 and not lo>=F(1,4)/F(5,3)
# The two endpoint width constants really differ.
e=F(1,4);q=F(1,2)+e-e/32;lo,hi=bounds(q,e)
assert (1-lo)/(1-hi)>(1+e)/(1-e)
# A supplied alpha-dependent exact-mean report erases failure, violating common-policy scope.
for a in range(1,16):assert good(F(a,16),F(1,2)+F(1,4)*F(a,16),F(1,4))
result={'status':'PASS_FRESH_EXACT_DENSITY_CONTROLS','power_interval_missed_mass_checks':interval,'likelihood_checks':likelihood,'weighted_all_zero_checks':weighted,'non_beta_empirical_step_checks':perstep,'seed_mixture_prefix_checks':mixtures,'endpoint_atom_zero_error_checks':endpoint,'countercontrols':{'pure_interior_atom_omits_density_lower_hypothesis':True,'model_parameter_supplied_to_policy_breaks_lower_bound':True,'full_inverse_moment_with_endpoint_atom_not_valid_criterion':True,'posterior_atom_no_constant_conditional_floor':posterior_atom,'lower_interval_alone_insufficient':True,'endpoint_width_constants_not_identical':True},'scope':'Finite exact rational tests support the independent ordinary review; infinite rates and integrability require its proof. The inverse-moment countercontrol is analytic in the review, not a simulated infinity.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(BASE/'CONTROL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
