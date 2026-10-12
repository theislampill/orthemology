import sympy as s,json
from pathlib import Path
u=s.symbols('u',positive=True)
t=s.symbols('t',positive=True)
e=s.exp(3*t);v=2*(e-1)/(2*e+1)
D=s.factor(s.Rational(1,2)*(1-1/v)**2*v*(v+2))
checks={
'initial_variance':s.limit(v,t,0,dir='+')==0,
'variance_ODE':s.simplify(s.diff(v,t)-(v+2)*(1-v))==0,
'initial_inflow':s.limit(v/t,t,0,dir='+')==2,
'limit_target':s.limit(v,t,s.oo)==1,
'dissipation_identity':s.simplify(s.diff((v-1-s.log(v))/2,t)+D)==0,
'one_missing_direction_pole':s.limit(t*D,t,0,dir='+')==s.Rational(1,2),
'quadratic_clock_action_density':s.limit(4*u*u*D.subs(t,u*u),u,0,dir='+')==2,
}
# r missing axes contribute additively; all other axes stay at target variance 1.
for r in (1,2,3,5):
 checks[f'rank_{r}_det_prefactor']=s.limit((v/t)**r,t,0,dir='+')==2**r
 checks[f'rank_{r}_action_pole']=s.limit(t*r*D,t,0,dir='+')==s.Rational(r,2)
if not all(checks.values()):raise RuntimeError(checks)
Path(__file__).with_name('CHECKS.json').write_text(json.dumps({'count':len(checks),'checks':checks,'scope':'Exact isotropic target witness with B=0, S diagonal with r zero initial variances and remaining variances one. Positivity uses exp(3t)>1 for t>0. Finite symbolic checks supplement general proof; no novelty or kernel claim.'},indent=2)+'\n')
print(len(checks),'PASS')
