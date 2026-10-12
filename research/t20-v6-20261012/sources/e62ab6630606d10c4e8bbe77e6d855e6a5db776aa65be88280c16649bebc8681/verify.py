#!/usr/bin/env python3
"""Portable exact and numerical controls; not a proof of PDE well-posedness."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import sympy as S
import mpmath as mp

P = argparse.ArgumentParser()
P.add_argument('--output-dir', default='author-run')
P.add_argument('--original-root')
args = P.parse_args()
ROOT = Path(__file__).resolve().parent
OUT = Path(args.output_dir)
if not OUT.is_absolute():
    OUT = ROOT / OUT
OUT.mkdir(parents=True, exist_ok=True)
checks = []

def check(name, condition, detail='', kind='exact'):
    passed = bool(condition)
    checks.append(dict(name=name, passed=passed, kind=kind, detail=str(detail)))
    if not passed:
        raise RuntimeError('FAILED: ' + name + ': ' + str(detail))

def zero(name, expr):
    result = S.simplify(expr)
    check(name, result == 0, result)

y, e, c = S.symbols('y e c', real=True)
a, b = S.Rational(1, 2), S.Integer(1)
d = b-a
A = 1+3*c

def V(x):
    return x*x/2+x**4/4

emom = {0:S.Integer(1), 1:0, 2:c, 3:0, 4:1-c,
        5:0, 6:4*c-1, 7:0, 8:6-9*c}

def cond(poly):
    p = S.Poly(S.expand(poly), e)
    return S.expand(sum(coef*emom[n] for (n,),coef in p.terms()))

def ey(poly):
    p = S.Poly(S.expand(poly), y)
    return S.expand(sum(coef*(S.factorial2(n-1) if n else 1)
                        for (n,),coef in p.terms() if n % 2 == 0))

def expectation(poly):
    return S.expand(ey(cond(poly)))

def variance(poly):
    return S.expand(expectation(poly**2)-expectation(poly)**2)

def dy(poly):
    # e=z-b*y: spatial y differentiation must hold z, not e, fixed.
    return S.diff(poly,y)-b*S.diff(poly,e)

q = S.expand(V(e+d*y)-V(e))
h = A*d*d*y*y/2+d**4*y**4/4
m = -a*(A*d*y+d**3*y**3)
H2, H4 = y*y-1, y**4-6*y*y+3
R2 = A*d*d/2+3*d**4/2-a*(A*d+3*d**3)
R4 = d**4/4-a*d**3
phi = S.expand(R2*H2/3+R4*H4/5)
L = lambda f: -S.diff(f,y,2)+y*S.diff(f,y)+f
rhs = y*m-S.diff(m,y)+h-ey(h)
zero('quartic conditional entropy', cond(q)-h)
zero('quartic conditional observed score', cond(dy(q))-m)
zero('quartic multiplier centered', ey(phi))
zero('quartic full observed-flux multiplier equation', L(phi)-rhs)
zero('Hermite two eigenvalue', L(H2)-3*H2)
zero('Hermite four eigenvalue', L(H4)-5*H4)
wrong_phi = (A*d*d/2+3*d**4/2)*H2/3+d**4*H4/20
zero('wrong multiplier residual is omitted flux',
     rhs-L(wrong_phi)-(y*m-S.diff(m,y)))
check('omitted observed flux is genuinely nonzero', S.expand(y*m-S.diff(m,y)) != 0)
f = q-phi
E = expectation(q)
Iz = expectation(S.diff(q,e)**2)
Vf = expectation(q*q)-ey(h*h)
D = expectation(dy(f)**2+S.diff(f,e)**2)+variance(f)
remainder = expectation((dy(q)-S.diff(phi,y))**2)+ey((h-phi)**2)-ey(h-phi)**2
zero('exact conditional dissipation decomposition', D-Iz-Vf-remainder)
Bqphi = expectation(dy(q)*S.diff(phi,y)) + expectation(q*phi)-expectation(q)*ey(phi)
Bphiphi = ey(S.diff(phi,y)**2+phi**2)-ey(phi)**2
zero('full projection orthogonality', Bqphi-Bphiphi)
Bqf = expectation(dy(q)*dy(f)+S.diff(q,e)*S.diff(f,e))+expectation(q*f)-expectation(q)*expectation(f)
zero('entropy chain pairing equals minimum action', Bqf-D)
zero('coarse drift vanishes', -rhs+L(phi))
zero('quartic target curvature certificate', S.diff(V(e),e,2)-(1+3*e*e))

mp.mp.dps = 60
Z = mp.quad(lambda x:mp.exp(-x*x/2-x**4/4),[-mp.inf,0,mp.inf])
mom = lambda n: mp.quad(lambda x:x**n*mp.exp(-x*x/2-x**4/4),[-mp.inf,0,mp.inf])/Z
cv = mom(2)
check('quartic integration-by-parts fourth moment', abs(mom(4)-(1-cv))<mp.mpf('1e-50'), kind='numerical high precision')
check('quartic integration-by-parts sixth moment', abs(mom(6)-(4*cv-1))<mp.mpf('1e-50'), kind='numerical high precision')
num = lambda x: mp.mpf(str(S.N(x.subs(c,S.Float(str(cv),65)),60)))
check('non-Gaussian correlated state has positive entropy', num(E)>0, num(E), 'numerical high precision')
check('non-Gaussian latent LSI control', num(Iz)>=2*num(E), num(Iz)-2*num(E), 'numerical high precision')
check('non-Gaussian full control with reaction', num(D)>=2*num(E), num(D)-2*num(E), 'numerical high precision')
check('non-Gaussian exact remainder nonnegative', num(remainder)>0, num(remainder), 'numerical high precision')

M, s, T, x = S.symbols('M s T x',positive=True)
xi = S.symbols('xi',real=True)
qg = S.log(T/s)/2+(xi+M)**2/(2*T)-xi**2/(2*s)

def eg(poly):
    p = S.Poly(S.expand(poly), xi)
    return S.expand(sum(coef*(S.factorial2(n-1)*s**(S.Rational(n,2)) if n else 1)
                        for (n,),coef in p.terms() if n % 2 == 0))

Eg = ((s+M*M)/T-1+S.log(T/s))/2
Ig = M*M/T**2+(s-T)**2/(s*T**2)
Vg = M*M*s/T**2+(s-T)**2/(2*T**2)
zero('Gaussian entropy including nonzero mean', eg(qg)-Eg)
zero('Gaussian Fisher including nonzero mean', eg(S.diff(qg,xi)**2)-Ig)
zero('Gaussian reaction variance including nonzero mean', eg(qg*qg)-eg(qg)**2-Vg)
limit = S.limit(((Ig+Vg)/Eg).subs(s,1/M), M,S.oo)
zero('fixed-target all-law sharpness limit',limit-2/T)
check('centred-subclass constant fails for general states',
      ((Ig+Vg)-6*Eg).subs({T:1,M:10,s:S.Rational(1,10)}).evalf()<0)

bb, ss = S.symbols('bb ss',real=True)
hh=(ss-1-S.log(ss)+bb*bb*y*y)/2
bprime=-bb*(ss+2+bb*bb/3)
sprime=(1-ss)*(ss+2)+2*bb*bb
hdot=(S.diff(hh,bb)*bprime+S.diff(hh,ss)*sprime).subs({bb:1,ss:S.Rational(11,10)})
zero('per-fibre increase exact polynomial', hdot-(S.Rational(169,2200)-S.Rational(103,30)*y*y))
check('per-fibre entropy rises near observed zero', hdot.subs(y,0)>0)
check('whole entropy nevertheless falls', ey(hdot)<0,ey(hdot))
restricted_hdot=S.diff(hh,bb)*(-(1+ss)*bb)+S.diff(hh,ss)*((1-ss)*(ss+2))
zero('inherited fibrewise alternative decreases each conditional entropy',
     restricted_hdot+bb*bb*y*y*(1+ss)+(ss-1)**2*(1/ss+S.Rational(1,2)))

# Derive the incompatible-marginal score from the two joint log densities.
log_current = -((y-1)**2+e**2)/2
log_target = -(y**2+e**2)/2
q_wrong_target = S.expand(log_current-log_target)
phi_wrong_target = y-1
ey_shift = lambda f: ey(S.expand(f.subs(y,y+1)))
zero('incompatible marginal multiplier is centered',ey_shift(phi_wrong_target))
zero('incompatible marginal coarse weak equation',
     -S.diff(phi_wrong_target,y,2)+(y-1)*S.diff(phi_wrong_target,y)+phi_wrong_target
     -((y-1)*S.diff(q_wrong_target,y)+q_wrong_target-ey_shift(q_wrong_target)))
remaining_score = q_wrong_target-phi_wrong_target
zero('incompatible marginal projected transport vanishes',S.diff(remaining_score,y))
zero('incompatible marginal projected reaction vanishes',remaining_score-ey_shift(remaining_score))
zero('incompatible marginal positive total KL floor',ey_shift(q_wrong_target)-S.Rational(1,2))

# Logistic change of variables turns the claimed integrals into integrable
# functions on (0,1); exact constants are independently checked numerically.
j1=mp.quad(lambda u:1-u,[0,1])
j2=mp.quad(lambda u:-mp.log(u)/(1-u),[0,mp.mpf('.5'),1])
j3=mp.quad(lambda u:mp.log(u)**2/(1-u),[0,mp.mpf('.5'),1])
check('logistic Fisher integral',abs(j1-mp.mpf('.5'))<mp.mpf('1e-50'),kind='numerical high precision')
check('logistic entropy integral',abs(j2-mp.zeta(2))<mp.mpf('1e-50'),kind='numerical high precision')
check('logistic reaction integral',abs(j3-2*mp.zeta(3))<mp.mpf('1e-50'),kind='numerical high precision')
zero('bounded-entropy reaction-sensitive obstruction limit',S.limit((1+4*S.zeta(3))/S.sqrt(2*S.pi*T),T,S.oo))

for row in json.loads((ROOT/'INPUT_BINDINGS.json').read_text()):
    data=(ROOT/row['snapshot']).read_bytes()
    check('input snapshot '+row['original'],hashlib.sha256(data).hexdigest()==row['sha256'],kind='integrity')
    if args.original_root:
        original=Path(args.original_root)/row['original']
        check('original '+row['original'],hashlib.sha256(original.read_bytes()).hexdigest()==row['sha256'],kind='integrity')

result=dict(status='PASS',count=len(checks),checks=checks,
    non_gaussian_control=dict(a=str(a),b=str(b),second_moment=str(cv),
       entropy=str(num(E)),latent_fisher=str(num(Iz)),conditional_reaction=str(num(Vf)),
       full_dissipation=str(num(D)),remainder=str(num(remainder)),
       exact_entropy=str(E),exact_dissipation=str(S.factor(D))),
    scope='Controls supplement ordinary proofs; no PDE existence/uniqueness, general chain rule, LSI proof, independent review or programme closure claimed.')
(OUT/'CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status='PASS',count=len(checks),output=str(OUT/'CHECKS.json'))))
