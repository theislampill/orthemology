import sympy as s,json
from pathlib import Path
T=s.diag(1,2);W=T.inv();A=s.diag(s.Rational(1,4),s.Rational(1,2));a=s.Rational(1,4)
S=s.Matrix([[2,1],[1,3]]);g=s.Matrix([3,-1]);m=s.Matrix([-1,2]);d=m-g
Q=T*(s.eye(2)-A*A);Sd=A*S*A+Q;md=g+A*d
P=a*Sd.inv()+(1-a)*W;Sr=P.inv();mr=g+Sr*a*Sd.inv()*(md-g)
z=lambda M: all(s.simplify(x)==0 for x in M)
checks={'OU_noise_exact':Q==s.diag(s.Rational(15,16),s.Rational(3,2)),
'OU_covariance_exact':Sd==s.Matrix([[s.Rational(17,16),s.Rational(1,8)],[s.Rational(1,8),s.Rational(9,4)]]),
'OU_mean_exact':md==s.Matrix([2,s.Rational(1,2)]),
'noncommuting_input':not z(S*W-W*S),
'reaction_precision_identity':z(Sr.inv()-P),
'reaction_mean_normal_equation':z(P*(mr-g)-a*Sd.inv()*(md-g)),
'positive_covariance':Sr[0,0]>0 and Sr.det()>0,
'point_mass_noise_strict_positive':Q[0,0]>0 and Q.det()>0}
# Fréchet first derivatives of exact Gaussian updates, no commuting assumption.
D0=2*s.eye(2)-W*S-S*W
Pdot=W-S.inv()-S.inv()*D0*S.inv();Sdot=-S*Pdot*S
mdot=Sdot*S.inv()*d-S*S.inv()*d-S*S.inv()*D0*S.inv()*d-W*d
checks['covariance_generator']=z(Sdot-(D0+S-S*W*S))
checks['mean_generator']=z(mdot+(s.eye(2)+S)*W*d)
if not all(checks.values()):raise RuntimeError(checks)
Path(__file__).with_name('CHECKS.json').write_text(json.dumps({'count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'reaction_covariance':str(Sr),'reaction_mean':str(mr),'scope':'Exact Gaussian parameter identities supplement the all-law proof; no finite representation or exact sampler for arbitrary laws is asserted.'},indent=2)+'\n')
print(len(checks),'PASS',Sr,mr)
