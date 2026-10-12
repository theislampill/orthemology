import sympy as s,json
from pathlib import Path
n,T=s.symbols('n T',positive=True)
m,v=s.symbols('m v',real=True,positive=True)
E=((v+m*m)/T-1+s.log(T/v))/2
I=m*m/T**2+(v-T)**2/(v*T**2)
R=m*m*v/T**2+(v-T)**2/(2*T**2)
D=I+R
Eseq=E.subs({m:n,v:1/n});Dseq=D.subs({m:n,v:1/n})
checks={
'energy_leading':s.limit(Eseq/n**2,n,s.oo)==1/(2*T),
'action_leading':s.limit(Dseq/n**2,n,s.oo)==1/T**2,
'sharp_ratio':s.limit(Dseq/Eseq,n,s.oo)==2/T,
'centred_unit_target_reduction':s.simplify(D.subs({m:0,T:1})-(v-1)**2*(1/v+s.Rational(1,2)))==0,
'mean_shift_unit_variance':s.simplify((D-4*E).subs({T:1,v:1}))==0,
}
b0=s.Rational(1);s0=s.Rational(11,10)
bdot=-b0*(s0+2+b0*b0/3);sdot=(1-s0)*(s0+2)+2*b0*b0
c0=(1-1/s0)*sdot/2;c2=b0*bdot
checks.update({'local_positive_intercept':c0==s.Rational(169,2200),'local_slope':c2==-s.Rational(103,30),'integrated_negative':c0+c2==-s.Rational(22153,6600),'positive_interval_radius_squared':-c0/c2==s.Rational(507,22660)})
if not all(checks.values()):raise RuntimeError(checks)
Path(__file__).with_name('CHECKS.json').write_text(json.dumps({'count':len(checks),'checks':checks,'scope':'Exact supplementary scalar Gaussian computations; analytic derivation and class assumptions in CONTROL.md.'},indent=2)+'\n')
print(len(checks),'PASS')
