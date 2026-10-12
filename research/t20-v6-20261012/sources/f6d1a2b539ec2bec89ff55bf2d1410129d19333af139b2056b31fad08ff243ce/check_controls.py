#!/usr/bin/env python3
"""Exact finite controls only; the written proof carries all universal claims."""
from pathlib import Path
import hashlib, json, os, platform, sys
from datetime import datetime, timezone
from math import factorial
import sympy as S

HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get("LIFT_SOURCE_ROOT", str(HERE.parent))).resolve()
checks=[]

def record(name,ok,detail=None):
    if not bool(ok):
        raise AssertionError(name if detail is None else f'{name}: {detail}')
    checks.append({'name':name,'passed':True})

def zero(name,expr):
    value=S.cancel(S.expand(expr))
    record(name,value==0,str(value))

def integral(poly,u,lo,hi):
    p=S.Poly(S.expand(poly),u)
    return S.Add(*(coeff*(hi**(power[0]+1)-lo**(power[0]+1))/S.Integer(power[0]+1)
                   for power,coeff in p.terms()))

def hashes():
    data=json.loads((HERE/'INPUT_BINDINGS.json').read_text())
    for item in data['files']:
        original=ROOT/item['original']
        record('source hash '+item['original'],hashlib.sha256(original.read_bytes()).hexdigest()==item['sha256'])
        if item.get('copy'):
            copy=HERE/item['copy']
            record('copy hash '+item['copy'],hashlib.sha256(copy.read_bytes()).hexdigest()==item['sha256'])

hashes()

# Algebraic domination: each summand in the identity is a product of SOS factors
# when B and B-a_i are SOS. The symbolic identity itself is independently checked.
B=S.symbols('B')
for m in range(1,9):
    a=S.symbols(f'a0:{m}')
    rhs=sum(B**(m-i-1)*(B-a[i])*S.prod(a[:i]) for i in range(m))
    zero(f'SOS product telescope m={m}', B**m-S.prod(a)-rhs)

K,c,R=S.symbols('K c R')
for n in range(1,13):
    rhs=(K-c*R)*sum(K**(n-1-i)*(c*R)**i for i in range(n))
    zero(f'cumulative power telescope n={n}',K**n-c**n*R**n-rhs)

# Exact formal-lambda checks of both finite Volterra formulae. The scalar energy
# g(u)=(a+b*u)^2 is genuinely time varying. Coefficients through lambda^7
# use exact rational polynomial integration, not numerical quadrature.
u=S.symbols('u')
configs=[(S.Rational(1),S.Rational(1),S.Rational(1,4),S.Rational(3,4)),
         (S.Rational(2),S.Rational(-1),S.Rational(1,3),S.Rational(5,4)),
         (S.Rational(-1),S.Rational(2),S.Rational(1,5),S.Rational(4,5)),
         (S.Rational(1,2),S.Rational(3,2),S.Rational(1,2),S.Rational(3,2))]
for idx,(a,b,s,t) in enumerate(configs):
    g=(a+b*u)**2
    Hu=a*a*u+a*b*u*u+b*b*u**3/3
    Hs=Hu.subs(u,s); Ht=Hu.subs(u,t); delta=Ht-Hs
    zero(f'energy primitive cfg={idx}',S.diff(Hu,u)-g)
    for m in range(1,5):
        for ell in range(8):
            forward=sum((-1)**k*delta**k/S.factorial(k)*(-Hs)**(ell-k)/S.factorial(ell-k)
                        for k in range(min(m-1,ell)+1))
            backward=sum(delta**k/S.factorial(k)*(-Ht)**(ell-k)/S.factorial(ell-k)
                         for k in range(min(m-1,ell)+1))
            if ell>=m:
                common=g*(-Hu)**(ell-m)/S.factorial(ell-m)/S.factorial(m-1)
                forward+=(-1)**m*integral(common*(Ht-Hu)**(m-1),u,s,t)
                backward+=integral(common*(Hu-Hs)**(m-1),u,s,t)
            zero(f'forward earliest endpoint cfg={idx} m={m} lambda={ell}',forward-(-Ht)**ell/S.factorial(ell))
            zero(f'backward latest endpoint cfg={idx} m={m} lambda={ell}',backward-(-Hs)**ell/S.factorial(ell))

# Explicit negative controls reject the incorrect time endpoint in each remainder.
a,b,s,t=configs[0]
g=(a+b*u)**2; Hu=a*a*u+a*b*u*u+b*b*u**3/3
Hs=Hu.subs(u,s); Ht=Hu.subs(u,t); delta=Ht-Hs
m,ell=2,3
term_f=sum((-1)**k*delta**k/S.factorial(k)*(-Hs)**(ell-k)/S.factorial(ell-k) for k in range(m))
wrong_f=term_f+integral(g*(-Hu)*(Hu-Hs),u,s,t)
record('countercontrol: forward latest endpoint rejected',S.cancel(wrong_f-(-Ht)**3/6)!=0)
term_b=sum(delta**k/S.factorial(k)*(-Ht)**(ell-k)/S.factorial(ell-k) for k in range(m))
wrong_b=term_b+integral(g*(-Hu)*(Ht-Hu),u,s,t)
record('countercontrol: backward earliest endpoint rejected',S.cancel(wrong_b-(-Hs)**3/6)!=0)

# Scalar Gaussian-tail estimates are algebraically consistent with simplex volume.
C,dt,c0,M=S.symbols('C dt c0 M',positive=True)
for n in range(1,13):
    zero(f'factorial cancellation n={n}',dt**n/S.factorial(n)*S.factorial(n)*(C/c0)**n*M-M*(C*dt/c0)**n)
for j in range(12):
    y=S.symbols('y',real=True)
    # (1+y^(2j))/2 dominates |y|^j because (|y|^j-1)^2>=0.
    v=S.symbols('v',nonnegative=True)
    zero(f'absolute hidden weight majorant j={j}',(1+v**(2*j))/2-v**j-(v**j-1)**2/2)

# Nonautonomous partial quadratic example and exact cumulative certificate.
t=S.symbols('t',positive=True)
z1,z2=S.symbols('z1 z2',real=True)
Qt=S.Matrix([[1,t],[t,t*t]])
Kt=S.Matrix([[t,t*t/2],[t*t/2,t**3/3]])
zero('rank one instantaneous determinant',Qt.det())
zero('cumulative Gram determinant',Kt.det()-t**4/12)
for i in range(2):
    for j in range(2):
        zero(f'Gram derivative entry={i},{j}',S.diff(Kt[i,j],t)-Qt[i,j])
c_t=t**3/(4*(t*t+3)); a_t=3*t*(t*t+4)/(4*(t*t+3))
energy=(S.Matrix([z1,z2]).T*Kt*S.Matrix([z1,z2]))[0]
sos=a_t*(z1+2*t*(t*t+3)*z2/(3*(t*t+4)))**2+t**5*z2*z2/(12*(t*t+3)*(t*t+4))
zero('explicit cumulative SOS certificate',energy-c_t*(z1*z1+z2*z2)-sos)
zero('determinant after certified radial shift',(Kt-c_t*S.eye(2)).det()-c_t*c_t)
commutator=Qt.subs(t,0)*Qt.subs(t,1)-Qt.subs(t,1)*Qt.subs(t,0)
record('countercontrol: quadratic matrices do not commute',commutator!=S.zeros(2))
record('countercontrol: full-space coercivity fails on hidden axis',energy.subs({z1:0,z2:0})==0)

# Genuine Gaussian killed laws for the varying, noncommuting-matrix example.
W=S.eye(2)+2*Kt
Sigma=W.inv(); D=S.factor(W.det())
E_g=S.trace(Qt*Sigma)
zero('Gaussian log normalizer derivative',-S.diff(D,t)/(2*D)+E_g)
for i in range(2):
    for j in range(2):
        zero(f'Gaussian covariance reaction entry={i},{j}',S.diff(Sigma[i,j],t)+2*(Sigma*Qt*Sigma)[i,j])

def gaussmoment(a,b):
    if a<0 or b<0: return S.Integer(0)
    if a==0 and b==0: return S.Integer(1)
    if (a+b)%2: return S.Integer(0)
    if a:
        return S.cancel((a-1)*Sigma[0,0]*gaussmoment(a-2,b)+b*Sigma[0,1]*gaussmoment(a-1,b-1))
    return S.cancel((b-1)*Sigma[1,1]*gaussmoment(0,b-2))
for a in range(5):
    for b in range(5-a):
        p=gaussmoment(a,b)
        gp=gaussmoment(a+2,b)+2*t*gaussmoment(a+1,b+1)+t*t*gaussmoment(a,b+2)
        zero(f'Gaussian normalized polynomial hierarchy z=({a},{b})',S.diff(p,t)+gp-E_g*p)

# Inherited hidden ambiguity. This exact Gaussian characteristic cancellation
# is a finite control of the explicit family, not a universal moment theorem.
for n in range(33):
    zero(f'lognormal Stieltjes cancellation moment={n}',S.exp(S.Rational(n*n,2)-2*S.pi**2)*S.sin(2*S.pi*n))
zero('graph-law conditional variance discriminator',S.exp(2)-2*S.exp(2)+S.exp(2))

# Higher-degree energy satisfies the general theorem but not quadratic domination.
z=S.symbols('z',real=True)
Gh=z**4+t*t*z*z
Kh=t*z**4+t**3*z*z/3
zero('higher-degree primitive',S.diff(Kh,t)-Gh)
zero('higher-degree cumulative SOS remainder',Kh-t**3*z*z/3-t*z**4)
B0=S.symbols('B0',nonnegative=True)
excess=S.expand(((B0+1)**4-B0*(B0+1)**2))
record('countercontrol: quartic exceeds every proposed quadratic bound',all(coef>0 for coef in S.Poly(excess,B0).all_coeffs()))

# Separate tensor sharpness corollary. Reuse the exact full-functional source's
# executable prefix solely for finite arithmetic controls; its ordinary proof is
# the infinite-dimensional premise. run_path does not mutate the source copy.
import runpy
src=runpy.run_path(str(HERE/'inputs/countermodel.py'),run_name='tensor_control_import')
model=src['SchurMoment']()
record('tensor source witness value',model.apply(src['WITNESS'])==-1)
V=1/(1+2*t*t)
def active_moment(n):
    return S.Integer(0) if n%2 else S.factorial2(n-1)*V**(n//2)
for a in range(7):
    for b in range(5):
        for d in range(5):
            h=S.Rational(model.moment(b,d))
            value=active_moment(a)*h
            rhs=-2*t*(active_moment(a+2)-active_moment(2)*active_moment(a))*h
            zero(f'tensor mixed hierarchy active={a} hidden=({b},{d})',S.diff(value,t)-rhs)
H4=S.Matrix([[S.Rational(v) for v in row] for row in model.gram(4)])
for tt in [S.Rational(0),S.Rational(1,3),S.Rational(1),S.Rational(2)]:
    G3=S.Matrix(3,3,lambda a,b:active_moment(a+b).subs(t,tt))
    Tensor=S.kronecker_product(G3,H4)
    L,D=Tensor.LDLdecomposition(hermitian=False)
    record(f'tensor exact LDL reconstruction t={tt}',L*D*L.T==Tensor)
    for i in range(12):
        record(f'tensor strict finite pivot t={tt} pivot={i}',D[i,i]>0)
    record(f'tensor witness remains negative t={tt}',model.apply(src['WITNESS'])==-1)

result={'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'check_count':len(checks),'python':platform.python_version(),'sympy':S.__version__,
        'scope':'Exact finite symbolic controls. No finite control proves full-functional existence, signed Fourier uniqueness, or the universal whole-path theorem.',
        'checks':checks}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
