#!/usr/bin/env python3
"""Exact controls plus explicitly numerical tests; not a formal proof or PDE solver."""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as s
import mpmath as mp
import numpy as np
from gaussian_step import gaussian_step

parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', required=True)
parser.add_argument('--original-root')
args = parser.parse_args()
ROOT = Path(__file__).resolve().parent
OUT = Path(args.output_dir).resolve()
OUT.mkdir(parents=True, exist_ok=False)
checks = []


def check(name, condition, detail='', kind='exact'):
    ok = bool(condition)
    checks.append(dict(name=name, passed=ok, kind=kind, detail=str(detail)))
    if not ok:
        raise RuntimeError('FAILED: '+name+': '+str(detail))


def zero(name, expr):
    if isinstance(expr, s.MatrixBase):
        value = expr.applyfunc(s.simplify)
        check(name, value == s.zeros(*value.shape), value)
    else:
        value = s.simplify(expr)
        check(name, value == 0, value)


def spd(name, matrix):
    check(name, matrix == matrix.T and
          all(matrix[:j, :j].det() > 0 for j in range(1, matrix.rows+1)), matrix)


I = s.eye(2)
T = s.diag(1, 2)
U = T.inv()
S = s.Matrix([[2, 1], [1, 3]])
A = s.diag(s.Rational(1, 4), s.Rational(1, 2))
Q = s.diag(s.Rational(15, 16), s.Rational(3, 2))
a = s.Rational(1, 4)
g = s.Matrix([3, -1])
m = s.Matrix([-1, 2])
delta = m-g
SD = A*S*A+Q
dD = A*delta
P = a*SD.inv()+(1-a)*U
SR = P.inv()
dR = SR*a*SD.inv()*dD
zero('OU noise covariance exact', Q-(T-A*T*A))
zero('OU target covariance fixed', A*T*A+Q-T)
check('fixture covariance genuinely noncommutes with target', S*T != T*S)
zero('noncommuting OU covariance fixture', SD-s.Matrix([[s.Rational(17,16),s.Rational(1,8)],[s.Rational(1,8),s.Rational(9,4)]]))
zero('reaction covariance exact rational fixture', SR-s.Matrix([[s.Rational(74,73),s.Rational(2,73)],[s.Rational(2,73),s.Rational(150,73)]]))
zero('reaction mean exact rational fixture', g+dR-s.Matrix([s.Rational(1603,584),-s.Rational(371,584)]))
spd('diffusion covariance positive definite', SD)
spd('reaction covariance positive definite', SR)
wrong_d = a*SD.inv()*SR*dD
check('reordering reaction mean matrices is wrong', s.simplify(wrong_d-dR) != s.zeros(2,1))

x0, x1 = s.symbols('x0 x1', real=True)
x = s.Matrix([x0,x1])
raw_exponent = -a*((x-g-dD).T*SD.inv()*(x-g-dD))[0]/2-(1-a)*((x-g).T*U*(x-g))[0]/2
output_exponent = -((x-g-dR).T*P*(x-g-dR))[0]/2
residual = s.expand(raw_exponent-output_exponent)
zero('reaction whole-density square completion has zero spatial gradient', s.Matrix([s.diff(residual,z) for z in x]))
zero('reaction whole-density precision', -s.hessian(raw_exponent,x)-P)

# Full-density identity for the inherited fibrewise combined generator.
d0,d1 = s.symbols('d0 d1',real=True)
d = s.Matrix([d0,d1])
e = x
K = U-S.inv()
b = U*d
mdot = -(I+S)*b
Sdot = 2*I-U*S-S*U+S-S*U*S
parametric_log_derivative = (-s.trace(S.inv()*Sdot)/2
    +(e.T*S.inv()*mdot)[0]+(e.T*S.inv()*Sdot*S.inv()*e)[0]/2)
transport_density_ratio = s.trace(K)-(e.T*S.inv()*(K*e+b))[0]
reaction_density_ratio = -(b.T*e)[0]-(e.T*K*e)[0]/2+s.trace(K*S)/2
zero('entire Gaussian density combined generator identity',
     parametric_log_derivative-transport_density_ratio-reaction_density_ratio)
zero('Gaussian reaction density normalization derivative',
     -s.trace(S*K)/2+s.trace(K*S)/2)

# First-order subflow jets; inverse differentiation is exact rational algebra.
eps = s.symbols('eps',real=True)
Aj = I-eps*U
SDj = Aj*S*Aj+2*eps*I
dj = Aj*d
Pj = (1-eps)*SDj.inv()+eps*U
SRj = Pj.inv()
dRj = SRj*(1-eps)*SDj.inv()*dj
zero('matrix first-order covariance consistency', SRj.diff(eps).subs(eps,0)-Sdot)
zero('matrix first-order nonzero mean consistency', dRj.diff(eps).subs(eps,0)-mdot)

# Singular inputs are never inverted before OU.
for label, initial in [('zero',s.zeros(2)),('rank_one',s.ones(2))]:
    smoothed = A*initial*A+Q
    reacted = (a*smoothed.inv()+(1-a)*U).inv()
    spd(label+' input diffusion regularizes',smoothed)
    spd(label+' input reaction remains nondegenerate',reacted)
    check(label+' input covariance was singular',initial.det()==0)

alpha,beta = s.symbols('alpha beta',positive=True)
precision1 = alpha*S.inv()+(1-alpha)*U
precision2 = beta*precision1+(1-beta)*U
zero('Gaussian reaction semigroup precision', precision2-(alpha*beta*S.inv()+(1-alpha*beta)*U))
eta1 = alpha*S.inv()*d
zero('Gaussian reaction semigroup natural mean', beta*eta1-alpha*beta*S.inv()*d)

# Scalar exact full h dependence, including the singular fixture.
ss,tt,dd,hh = s.symbols('ss tt dd hh',positive=True)
ascalar = s.exp(-hh)
Ascalar = s.exp(-hh/tt)
sdscalar = Ascalar**2*ss+tt*(1-Ascalar**2)
srscalar = 1/(ascalar/sdscalar+(1-ascalar)/tt)
drscalar = srscalar*ascalar/sdscalar*Ascalar*dd
zero('scalar exact covariance derivative',s.diff(srscalar,hh).subs(hh,0)-(2-2*ss/tt+ss-ss**2/tt))
zero('scalar exact mean derivative',s.diff(drscalar,hh).subs(hh,0)+(1+ss)*dd/tt)
zero('scalar singular covariance output',srscalar.subs({ss:0,tt:1,hh:s.log(2)})-s.Rational(6,7))
zero('scalar singular mean output',drscalar.subs({ss:0,tt:1,dd:3,hh:s.log(2)})-s.Rational(6,7))

# A non-affine supplied target mean still updates its residual feature vector.
y,b0,b1 = s.symbols('y b0 b1',real=True)
target_y = y**2
initial_delta_y = b0+b1*y
coef = s.simplify((drscalar/dd).subs({ss:s.Rational(3,2),tt:1,hh:s.log(2)}))
updated_y = target_y+coef*initial_delta_y
zero('dependent mean residual finite-feature closure',updated_y-(target_y+(coef*b0)+(coef*b1)*y))

# Raw Euler of the diffusion moment hierarchy is not an entire-law update.
tau = s.symbols('tau',positive=True)
euler_m2,euler_m4 = 2*tau,s.Integer(0)
zero('OU Dirac Euler square-positivity defect',euler_m4-euler_m2**2+4*tau**2)
check('OU Dirac Euler positivity defect is strict',-4*tau**2<0)
actual_var = 1-s.exp(-2*tau)
zero('exact OU fourth moment gives nonnegative square variance',3*actual_var**2-actual_var**2-2*actual_var**2)

# Power of a total mixture differs from powering its components.
z = s.symbols('z',real=True)
zero('mixture square-completion envelope',(-s.Rational(1,2)*(z*z+s.Integer(1))/(2*s.Rational(3,4))-(1-s.Rational(1,2))*z*z/2).coeff(z,2)+s.Rational(7,12))
zero('mixture fourth log derivative non-Gaussian',s.diff(s.log(s.cosh(4*z/3))/2,z,4).subs(z,0)+s.Rational(256,81))
check('density-power and componentwise-power are not proportional',
      s.simplify(s.diff(s.sqrt(s.cosh(2*z))/s.cosh(z),z,2).subs(z,0)) != 0)

# Finite-support density control of zero-set preservation and KL monotonicity.
mp.mp.dps=60
target = [mp.mpf(1)/5,mp.mpf(3)/10,mp.mpf(1)/2]
f = [mp.mpf(0),mp.mpf(2),mp.mpf(4)/5]
def escort(vals, aa):
    zz=sum(p*(v**aa) for p,v in zip(target,vals))
    return [v**aa/zz for v in vals],zz
def entropy(vals):
    return sum(p*v*mp.log(v) for p,v in zip(target,vals) if v)
fhalf,zhalf=escort(f,mp.mpf(1)/2)
fquarter,zquarter=escort(f,mp.mpf(1)/4)
check('reaction normalizer positive and at most one',0<zhalf<=1,str(zhalf),'numerical high precision')
check('reaction zero support remains zero',fhalf[0]==0,'','numerical high precision')
check('reaction entropy decreases at consecutive positive times',entropy(fquarter)<entropy(fhalf)<entropy(f),'','numerical high precision')
fcomposed,_=escort(fhalf,mp.mpf(1)/2)
check('reaction full discrete-density semigroup',max(abs(u-v) for u,v in zip(fcomposed,fquarter))<mp.mpf('1e-55'),'','numerical high precision')
fixed=[mp.mpf(0),mp.mpf(5)/4,mp.mpf(5)/4]
fixed_after,_=escort(fixed,mp.mpf(1)/3)
check('zero-support reaction positive-KL fixed state',max(abs(u-v) for u,v in zip(fixed,fixed_after))<mp.mpf('1e-55') and entropy(fixed)>0,'','numerical high precision')

# Non-Gaussian output from a singular two-atom law: no Gaussian moment closure.
sm = mp.mpf(3)/4
def logcosh(u):
    v=abs(u)
    return v+mp.log1p(mp.exp(-2*v))-mp.log(2)
def logpi(u): return -mp.log(2*mp.pi)/2-u*u/2
def logd(u): return -mp.log(2*mp.pi*sm)/2-(u*u+1)/(2*sm)+logcosh(u/sm)
def qd(u): return logd(u)-logpi(u)
quad=lambda fun:mp.quad(fun,[-mp.inf,-2,0,2,mp.inf])
HD=quad(lambda u:mp.exp(logd(u))*qd(u))
Z=quad(lambda u:mp.exp((logd(u)+logpi(u))/2))
def logr(u):return (logd(u)+logpi(u))/2-mp.log(Z)
HR=quad(lambda u:mp.exp(logr(u))*(logr(u)-logpi(u)))
cross=quad(lambda u:mp.exp(logd(u))*(logd(u)-logr(u)))
bound=(-mp.mpf(1)/4-mp.log(mp.mpf(3)/4))/2+mp.mpf(1)/2
check('singular mixture diffusion finite entropy bound',0<HD<bound,str(HD)+' <= '+str(bound),'numerical high precision')
check('singular mixture reaction probability normalization',abs(quad(lambda u:mp.exp(logr(u)))-1)<mp.mpf('1e-50'),'','numerical high precision')
check('singular mixture reaction entropy descent',0<HR<HD,str(HR)+' < '+str(HD),'numerical high precision')
check('cross KL exact entrance identity',abs(cross-(HD/2+mp.log(Z)))<mp.mpf('1e-50'),str(cross),'numerical high precision')
check('cross KL entrance upper bound',0<cross<HD/2,'','numerical high precision')
moment=quad(lambda u:u*u*mp.exp(logr(u)))
check('entropy-to-moment reaction bound',moment<4*HR+2*mp.log(2),str(moment),'numerical high precision')

def gaussian_kl(mm,cc,gg,tt):
    dim=len(mm)
    dd=np.asarray(mm)-np.asarray(gg)
    return float((np.trace(np.linalg.solve(tt,cc))+dd@np.linalg.solve(tt,dd)-dim
                  +np.linalg.slogdet(tt)[1]-np.linalg.slogdet(cc)[1])/2)

target_np=np.array([[1.,0.],[0.,2.]])
mean_np=np.array([-1.,2.]); g_np=np.array([3.,-1.]); cov_np=np.array([[2.,1.],[1.,3.]])
h=np.log(4.)
initial_e=gaussian_kl(mean_np,cov_np,g_np,target_np)
out=gaussian_step(mean_np,cov_np,g_np,target_np,h)
ed=gaussian_kl(out['diffusion_mean'],out['diffusion_covariance'],g_np,target_np)
er=gaussian_kl(out['mean'],out['covariance'],g_np,target_np)
check('finite implementation OU entropy contraction',ed<=np.exp(-h)*initial_e+1e-13,ed,'numerical floating point')
check('finite implementation reaction entropy descent',er<=ed+1e-13,er,'numerical floating point')
check('finite implementation rational mean fixture',np.max(abs(out['mean']-np.array([1603/584,-371/584])))<1e-13,'','numerical floating point')
check('finite implementation rational covariance fixture',np.max(abs(out['covariance']-np.array([[74/73,2/73],[2/73,150/73]])))<1e-13,'','numerical floating point')

prev=initial_e
for j in range(6):
    out=gaussian_step(mean_np,cov_np,g_np,target_np,.2)
    new=gaussian_kl(out['mean'],out['covariance'],g_np,target_np)
    check('finite Gaussian iteration '+str(j+1)+' contracts KL',new<=np.exp(-.2)*prev+1e-12,new,'numerical floating point')
    mean_np=out['mean']; cov_np=out['covariance']; prev=new

for item in json.loads((ROOT/'INPUT_BINDINGS.json').read_text()):
    copied=ROOT/item['snapshot']
    check('snapshot hash '+item['snapshot'],hashlib.sha256(copied.read_bytes()).hexdigest()==item['sha256'])
    if args.original_root:
        original=Path(args.original_root)/item['original']
        check('original unchanged '+item['original'],hashlib.sha256(original.read_bytes()).hexdigest()==item['sha256'])

payload={'status':'PASS','check_count':len(checks),'checks':checks,
         'scope':'Exact algebraic and explicitly numerical controls supplement the written ordinary proofs; no general PDE existence, novelty, formal-kernel, or closure claim.'}
(OUT/'CHECKS.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
print('PASS:',len(checks),'controls; results in',OUT/'CHECKS.json')
