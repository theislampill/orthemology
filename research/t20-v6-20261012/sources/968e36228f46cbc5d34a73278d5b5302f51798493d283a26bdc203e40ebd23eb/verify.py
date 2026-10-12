#!/usr/bin/env python3
"""Bounded exact transport controls, not a proof of the analytic theorems."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, platform
import sympy as S

HERE=Path(__file__).resolve().parent
checks=[]
def check(name, proposition):
    if not bool(proposition):
        raise AssertionError(name)
    checks.append(name)
    print('PASS', name)

# Read-only ancestor byte bindings.
bindings=json.loads((HERE/'INPUT_BINDINGS.json').read_text())
for row in bindings['inputs']:
    b=(HERE/row['snapshot']).read_bytes()
    check('snapshot hash: '+row['path'], hashlib.sha256(b).hexdigest()==row['sha256'])
    check('snapshot byte count: '+row['path'], len(b)==row['bytes'])

m=S.symbols('m0:10', real=True)
def D(expr):
    return S.expand(sum(S.diff(expr,m[j])*(-m[j+1]+m[1]*m[j]) for j in range(1,9)))
V=m[2]-m[1]**2
k3=m[3]-3*m[1]*m[2]+2*m[1]**3
check('mean derivative is minus variance',S.expand(D(m[1])+V)==0)
check('variance derivative is minus third cumulant',S.expand(D(V)+k3)==0)
Fjet=[S.Integer(0),-m[1]]
for k in range(2,8):
    Fjet.append(D(Fjet[-1]))
qjet=[m[1]]
for k in range(1,7):
    qjet.append(D(qjet[-1]))
for k in range(7):
    check('F derivative/mean sign order '+str(k),S.expand(Fjet[k+1]+qjet[k])==0)
check('second log-partition derivative',S.expand(Fjet[2]-V)==0)
check('third log-partition derivative',S.expand(Fjet[3]+k3)==0)
check('inverse mean metric derivative',S.cancel(D(1/V)/(-V)+k3/V**3)==0)
E=S.exp
check('lognormal endpoint variance',S.simplify(V.subs({m[1]:E(S.Rational(1,2)),m[2]:E(2)})-(E(2)-E(1)))==0)

# Legendre and metric chart, keeping the original mean q (not -q).
s,t,qs,qt,Fs,Ft=S.symbols('s t qs qt Fs Ft',real=True)
psis=-s*qs-Fs
psit=-t*qt-Ft
Bdual=S.expand(psis-psit-(-t)*(qs-qt))
KL=(t-s)*qs-Fs+Ft
Bnatural=Ft-Fs-(-qs)*(t-s)
check('KL equals mean-coordinate Bregman with same argument order',S.expand(Bdual-KL)==0)
check('KL reverses the natural-coordinate Bregman arguments',S.expand(Bnatural-KL)==0)
q0=S.symbols('q0',real=True)
check('boundary-to-interior KL orientation',S.expand(KL.subs({s:0,qs:q0,Fs:0})-(Ft+t*q0))==0)
check('interior-to-boundary KL orientation',S.expand(KL.subs({t:0,Ft:0})-(-s*qs-Fs))==0)
check('calibrated mean boundary Bregman is dual potential',S.expand(Bdual.subs({t:0,qt:q0,Ft:0})-psis)==0)
va, vb=S.symbols('va vb', positive=True)
dq=S.symbols('dq',real=True)
check('metric coordinate transformation',S.cancel(va*(dq/(-va))**2-dq**2/va)==0)
check('linear-objective mean natural gradient',S.cancel(-1/(1/va)+va)==0)

# Translation retains original normalizer constants but not in divergences.
u,w,a,c=S.symbols('u w a c',real=True)
F=S.Function('F')
G=lambda x:F(x+a)-c
BG=G(u)-G(w)-S.diff(G(w),w)*(u-w)
BF=F(u+a)-F(w+a)-S.diff(F(w+a),w)*((u+a)-(w+a))
check('normalizer translation preserves Bregman after shift',S.simplify(BG-BF)==0)
check('normalizer additive constant drops from metric',S.diff(G(u),u,2)==S.diff(F(u+a),u,2))
check('uncentered endpoint constant retained',G(-a)==F(0)-c)

# Finite-support analytic positive control: ν=(δ0+δ1)/2.
L=(1+S.exp(-t))/2
Fc=S.log(L)
qc=-S.diff(Fc,t)
Vc=S.diff(Fc,t,2)
check('Bernoulli variance identity',S.simplify(Vc-qc*(1-qc))==0)
check('Bernoulli mean descent',S.simplify(S.diff(qc,t)+Vc)==0)
q=S.symbols('q', positive=True)
psi=q*S.log(2*q)+(1-q)*S.log(2*(1-q))
check('Bernoulli dual metric',S.simplify(S.diff(psi,q,2)-1/(q*(1-q)))==0)
check('Bernoulli calibrated boundary value',S.simplify(psi.subs(q,S.Rational(1,2)))==0)
check('Bernoulli calibrated boundary slope',S.simplify(S.diff(psi,q).subs(q,S.Rational(1,2)))==0)
check('Bernoulli inverse chart',S.simplify(S.diff(psi,q)-(S.log(q)-S.log(1-q)))==0)

# Exact finite polynomial covariance blocks for generic z=exp(1/2)>1.
z=S.symbols('z',positive=True)
for d in range(1,5):
    H=S.Matrix(d+1,d+1,lambda i,j:z**((i+j)**2))
    C=S.Matrix(d,d,lambda i,j:z**((i+j+2)**2)-z**((i+1)**2+(j+1)**2))
    vd=z**(2*sum(i*i for i in range(d+1)))
    for i in range(d+1):
        for j in range(i+1,d+1):
            vd*=z**(2*j)-z**(2*i)
    dh=S.factor(H.det(method='domain-ge'))
    dc=S.factor(C.det(method='domain-ge'))
    check('Vandermonde lognormal moment determinant degree '+str(d),S.expand(dh-vd)==0)
    check('covariance Schur-complement determinant degree '+str(d),S.expand(dc-dh)==0)

# Formal Taylor obstruction is an exact ratio identity; divergence is proved in text.
n=S.symbols('n',integer=True,nonnegative=True)
h=S.symbols('h',positive=True)
term=S.exp(n*n/2)*h**n/S.factorial(n)
check('zero-radius Taylor term ratio',S.simplify(term.subs(n,n+1)/term-h*S.exp(n+S.Rational(1,2))/(n+1))==0)

report={'status':'PASS','checks':len(checks),'check_names':checks,
        'executed_at_utc':datetime.now(timezone.utc).isoformat(),
        'python':platform.python_version(),'sympy':S.__version__,
        'scope':'Exact finite algebraic/source-hash controls only. General analytic claims are ordinary proofs in RESULT.md; no kernel certification.'}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(checks),'exact controls')
print(report['scope'])
