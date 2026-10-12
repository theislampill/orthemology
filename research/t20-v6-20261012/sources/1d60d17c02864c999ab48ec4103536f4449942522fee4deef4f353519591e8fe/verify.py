#!/usr/bin/env python3
"""Bounded exact audit-transport controls plus labelled NumPy replay.

No universal theorem is proved by this finite checker. Run with ordinary or
optimized Python; checks do not depend on removable assert statements.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

import sympy as s

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', type=Path, default=HERE / 'run')
parser.add_argument('--check-originals', action='store_true')
args = parser.parse_args()
checks = []


def check(name, condition, detail='', kind='exact symbolic/rational'):
    good = bool(condition)
    checks.append(dict(name=name, passed=good, detail=str(detail), kind=kind))
    if not good:
        raise RuntimeError('FAILED: ' + name + ': ' + str(detail))


def zero(name, value, detail=''):
    entries = list(value) if isinstance(value, s.MatrixBase) else [value]
    check(name, all(s.simplify(v) == 0 for v in entries), detail)


def norm(v):
    return v / sum(v)


def bayes(v, likelihood):
    return norm(v.multiply_elementwise(likelihood))


def reaction(v, pi, a):
    return norm(s.Matrix([pi[i] * (v[i]/pi[i])**a for i in range(len(v))]))


bindings = json.loads((HERE/'INPUT_BINDINGS.json').read_text())['inputs']
for row in bindings:
    data = (HERE/row['snapshot']).read_bytes()
    check('snapshot hash: ' + row['snapshot'],
          hashlib.sha256(data).hexdigest() == row['sha256'], kind='integrity')
    if args.check_originals:
        path = HERE.parent/row['original']
        check('original unchanged: '+row['original'],
              path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'],
              kind='integrity')

R = s.Rational

# Finite strictly positive invertible-kernel analogue of the law-level proof.
K = s.Matrix([[R(3,4), R(1,4)], [R(1,4), R(3,4)]])
pi = s.Matrix([R(1,2), R(1,2)])
p = s.Matrix([R(1,3), R(2,3)])
L = s.Matrix([1, 2])
a = R(1,2)
check('finite kernel strictly positive', all(v > 0 for v in K))
zero('finite kernel determinant', K.det()-R(1,2))
zero('finite kernel invariant reference', K*pi-pi)
q = K*p
ell = s.Matrix([(K*p.multiply_elementwise(L))[i]/q[i] for i in range(2)])
zero('conditional factor kernel identity', K*bayes(p,L)-bayes(q,ell))
zero('original evidence normalizer', (q.T*ell)[0]-(p.T*L)[0])
phi = reaction(q,pi,a)
out = reaction(K*bayes(p,L),pi,a)
zero('powered conditional factor exactly transports posterior',
     out-bayes(phi,ell.applyfunc(lambda x:x**a)))
zero('reaction inverse on range', reaction(phi,pi,1/a)-q)
zero('full finite law recovered on actual image', K.inv()*reaction(phi,pi,1/a)-p)
check('forgetting reaction exponent changes output',
      any(s.simplify(v) != 0 for v in out-bayes(phi,ell)))
H = sum(phi[i]*ell[i]**a for i in range(2))
Z = (p.T*L)[0]
check('output multiplier normalizer differs from original evidence', s.simplify(H-Z) != 0,
      'H='+str(H)+'; Z='+str(Z))
zero('state-dependent rescaling can preserve evidence normalizer',
     sum(phi[i]*(Z/H)*ell[i]**a for i in range(2))-Z)

e0=s.Matrix([1,0]); e1=s.Matrix([0,1])
zero('Dirac audit fixes its input',bayes(e0,L)-e0)
phi0 = reaction(K*e0,pi,a)
check('Dirac image full support',all(v>0 for v in phi0))
check('naive same-coordinate factor moves Dirac image',
      any(s.simplify(v) != 0 for v in bayes(phi0,L)-phi0))
uniform = pi
phi_mix = reaction(K*uniform,pi,a)
phi_audit_mix = reaction(K*bayes(uniform,L),pi,a)
zero('two point mixture remains uniform before audit',phi_mix-pi)
check('two point audit changes corrected law',
      any(s.simplify(v) != 0 for v in phi_audit_mix-phi_mix))

# Sequential transported factors must use the revised incoming law.
L2=s.Matrix([2,1]); revised=bayes(p,L)
q_revised=K*revised
ell2_new=s.Matrix([(K*revised.multiply_elementwise(L2))[i]/q_revised[i] for i in range(2)])
ell2_old=s.Matrix([(K*p.multiply_elementwise(L2))[i]/q[i] for i in range(2)])
ell12=s.Matrix([(K*p.multiply_elementwise(L.multiply_elementwise(L2)))[i]/q[i]
               for i in range(2)])
zero('updated conditional factor product identity',ell.multiply_elementwise(ell2_new)-ell12)
joint=phi
correct_second=bayes(out,ell2_new.applyfunc(lambda x:x**a))
wrong_second=bayes(out,ell2_old.applyfunc(lambda x:x**a))
zero('successive correct transport recovers constant-product audit',correct_second-joint)
check('reusing old conditional factors breaks posterior',
      any(s.simplify(v) != 0 for v in wrong_second-joint))

# Actual OU mixture witness; no quadrature or floating-point equality claim.
z=s.symbols('z', real=True)
ratio=s.exp(4*z/3)
ell_ou=(1+2*ratio)/(1+ratio)
zero('actual OU likelihood ratio at zero',ell_ou.subs(z,0)-R(3,2))
zero('actual OU likelihood ratio at second point',ell_ou.subs(z,R(3,4)*s.log(2))-R(5,3))
zero('actual OU corrected density-ratio relative change',
     s.sqrt(ell_ou.subs(z,R(3,4)*s.log(2))/ell_ou.subs(z,0))-s.sqrt(R(10,9)))
check('actual OU relative change nontrivial',s.sqrt(R(10,9)) != 1)

# Noncommuting Gaussian exact-real fixture inherited from the split packet.
T=s.diag(1,2); A=s.diag(R(1,4),R(1,2)); Q=s.diag(R(15,16),R(3,2)); a=R(1,4)
S=s.Matrix([[2,1],[1,3]]); g=s.Matrix([3,-1]); m=s.Matrix([-1,2]); theta=s.Matrix([2,-1])
SD=A*S*A+Q
C=(a*SD.inv()+(1-a)*T.inv()).inv()
mp=g+C*a*SD.inv()*A*(m-g)
b=a*SD.inv()*A*S*theta
check('fixture covariance genuinely noncommutes with drift',S*A != A*S)
zero('Gaussian audited input mean shift',
     (g+C*a*SD.inv()*A*(m+S*theta-g))-(mp+C*b))
zero('conditional Gaussian exponential coefficient',
     a*(theta.T*S*A*SD.inv()).T-b)
check('wrong noncommuting coefficient order fails',a*SD.inv()*S*A*theta != b)
zero('fixed covariance multiplier independent of prior mean',
     (g+C*a*SD.inv()*A*(m+s.Matrix([7,5])+S*theta-g))
     -(g+C*a*SD.inv()*A*(m+s.Matrix([7,5])-g))-C*b)
P0=C.inv()-(1-a)*T.inv()
SD_recovered=a*P0.inv()
S_recovered=A.inv()*(SD_recovered-Q)*A.inv()
m_recovered=g+A.inv()*(SD_recovered/a)*C.inv()*(mp-g)
zero('exact inverse recovers diffusion covariance',SD_recovered-SD)
zero('exact inverse recovers incoming covariance',S_recovered-S)
zero('exact inverse recovers incoming mean',m_recovered-m)
x=s.Matrix(s.symbols('x0 x1',real=True))
log_difference=-(x-mp-C*b).dot(C.inv()*(x-mp-C*b))/2+(x-mp).dot(C.inv()*(x-mp))/2-b.dot(x)
zero('Gaussian whole-density tilt identity',s.Matrix([s.diff(log_difference,t) for t in x]))

for name,S0 in [('Dirac',s.zeros(2)),('partial rank',s.Matrix([[1,1],[1,1]]))]:
    SD0=A*S0*A+Q; C0=(a*SD0.inv()+(1-a)*T.inv()).inv()
    b0=a*SD0.inv()*A*S0*theta
    P00=C0.inv()-(1-a)*T.inv()
    zero(name+' inverse recovers singular covariance',A.inv()*(a*P00.inv()-Q)*A.inv()-S0)
    zero(name+' audit-transport mean equality',
         C0*a*SD0.inv()*A*(m+S0*theta-m)-C0*b0)
    check(name+' corrected covariance SPD',C0[0,0]>0 and C0.det()>0)
    if name=='Dirac': zero('Dirac Gaussian output multiplier constant',b0)

# Scalar class restriction and both distinct image guards.
v=s.symbols('v',nonnegative=True)
scalar_b=R(1,2)/(v/R(4)+R(3,4))*R(1,2)*v
zero('scalar tilt coefficient formula',scalar_b-v/(v+3))
zero('scalar covariance one coefficient',scalar_b.subs(v,1)-R(1,4))
zero('scalar covariance four coefficient',scalar_b.subs(v,4)-R(4,7))
check('varying covariance changes required fixed factor',R(1,4)!=R(4,7))

def inverse_scalar(c):
    p0=1/c-R(1,2)
    if p0 <= 0: return 'invalid reaction precision',None
    sd=R(1,2)/p0
    recovered=4*(sd-R(3,4))
    if recovered < 0: return 'invalid input covariance',recovered
    return 'valid',recovered

check('SPD output can fail reaction image',inverse_scalar(s.Integer(3))[0]=='invalid reaction precision')
check('SPD output can fail recovered input image',inverse_scalar(R(1,2))[0]=='invalid input covariance')
check('closed lower covariance boundary is valid Dirac image',inverse_scalar(R(6,7))==('valid',0))
check('open upper covariance endpoint fails',inverse_scalar(s.Integer(2))[0]=='invalid reaction precision')
check('interior scalar covariance image valid',inverse_scalar(s.Integer(1))==('valid',1))

# Parent-supplied two-fibre global/conditional normalizer discriminator.
nu=s.Matrix([R(1,2),R(1,2)]); Zy=s.Matrix([R(1,4),1]); a=R(1,2)
Hy=Zy.applyfunc(lambda x:x**a)
actual_global=bayes(nu,Zy); naive_global=bayes(nu,Hy)
full_factor=s.Matrix([Zy[i]*Hy[i]/Hy[i] for i in range(2)])
zero('joint audit true observed marginal',actual_global-s.Matrix([R(1,5),R(4,5)]))
zero('naive powered joint factor wrong marginal',naive_global-s.Matrix([R(1,3),R(2,3)]))
zero('coarse normalizers repair extended-family joint transport',bayes(nu,full_factor)-actual_global)
check('global audit with nonconstant fibre normalizers leaves fixed marginal domain',actual_global != nu)

# Replay the actual inherited NumPy function, distinguished from symbolic proof.
import numpy as np
spec=importlib.util.spec_from_file_location('inherited_gaussian_step',HERE/'inputs/gaussian_step.py')
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
Sn=np.array(S,dtype=float); Tn=np.array(T,dtype=float); mn=np.array(m,dtype=float).ravel()
gn=np.array(g,dtype=float).ravel(); th=np.array(theta,dtype=float).ravel()
h=float(np.log(4))
base=module.gaussian_step(mn,Sn,gn,Tn,h)
audited=module.gaussian_step(mn+Sn@th,Sn,gn,Tn,h)
bn=base['reaction_exponent']*np.linalg.solve(base['diffusion_covariance'],base['diffusion_matrix']@Sn@th)
mean_error=float(np.max(np.abs(audited['mean']-(base['mean']+base['covariance']@bn))))
cov_error=float(np.max(np.abs(audited['covariance']-base['covariance'])))
check('actual inherited implementation audit transported mean',mean_error<1e-12,
      mean_error,kind='numerical floating-point control')
check('actual inherited implementation audit covariance',cov_error<1e-12,
      cov_error,kind='numerical floating-point control')
check('actual implementation matches exact coefficient',
      float(np.max(np.abs(bn-np.array(b,dtype=float).ravel())))<1e-12,
      kind='numerical floating-point control')

args.output_dir.mkdir(parents=True,exist_ok=True)
result={'status':'PASS','checks':checks,'check_count':len(checks),
        'versions':{'python':sys.version.split()[0],'sympy':s.__version__,'numpy':np.__version__},
        'exact_gaussian_fixture':{'output_covariance':str(C),'output_mean':str(mp),
                                  'transported_exponent':str(b)},
        'limits':['Finite controls supplement written proofs.',
                  'No arbitrary-law finite encoding or inverse stability certificate.',
                  'No protected edit, integration, or T20 closure.']}
(args.output_dir/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS:',len(checks),'checks; results:',args.output_dir/'CONTROL_RESULTS.json')
