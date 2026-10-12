#!/usr/bin/env python3
"""Independently authored focused algebra controls; no author checker imported.

These are polynomial identities and exact finite-dimensional controls, not a
proof of the general LSI, entropy chain rule, or PDE existence/uniqueness.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as S

p = argparse.ArgumentParser()
p.add_argument('--output', default=None)
args = p.parse_args()
checks = []

def zero(name, expression):
    residual = S.factor(S.expand(expression))
    checks.append({'name': name, 'pass': residual == 0, 'residual': str(residual)})
    if residual != 0:
        raise RuntimeError(f'{name}: {residual}')

def truth(name, condition, evidence):
    ok = bool(condition)
    checks.append({'name': name, 'pass': ok, 'evidence': str(evidence)})
    if not ok:
        raise RuntimeError(f'{name}: {evidence}')

y, e, a, delta, c = S.symbols('y e a delta c', real=True)
b = a + delta

# Under the current law, Y is standard normal and e has quartic density.
# Integration by parts: M_(n+4)=(n+1) M_n - M_(n+2).
quartic_moments = {0: S.Integer(1), 1: S.Integer(0), 2: c, 3: S.Integer(0)}
for n in range(13):
    quartic_moments[n+4] = S.expand((n+1)*quartic_moments[n]-quartic_moments[n+2])

def Ee(poly):
    return S.expand(sum(coef*quartic_moments[k[0]]
                        for k, coef in S.Poly(S.expand(poly), e).terms()))

def Ey(poly):
    return S.expand(sum(coef*(S.factorial2(k[0]-1) if k[0] % 2 == 0 else 0)
                        for k, coef in S.Poly(S.expand(poly), y).terms()))

def E(poly):
    return Ey(Ee(poly))

def dy(poly):
    # Derivative at fixed z, not at fixed innovation e=z-b*y.
    return S.diff(poly, y)-b*S.diff(poly, e)

def dz(poly):
    return S.diff(poly, e)

def V(u):
    return u*u/2 + u**4/4

q = S.expand(V(e+delta*y)-V(e))
h = Ee(q)
m = Ee(dy(q))
A = 1+3*c
H2, H4 = y*y-1, y**4-6*y*y+3
R2 = A*delta**2/2+3*delta**4/2-a*(A*delta+3*delta**3)
R4 = delta**4/4-a*delta**3
phi = R2*H2/3+R4*H4/5
g = S.expand(q-phi)

zero('quartic fourth moment', quartic_moments[4]-(1-c))
zero('quartic sixth moment', quartic_moments[6]-(4*c-1))
zero('conditional entropy h', h-(A*delta**2*y*y/2+delta**4*y**4/4))
zero('conditional observed score m', m+a*(A*delta*y+delta**3*y**3))
zero('multiplier centered', Ey(phi))
rhs = S.expand(y*m-S.diff(m,y)+h-Ey(h))
coarseKphi = -S.diff(phi,y,2)+y*S.diff(phi,y)+phi
zero('weak multiplier strong polynomial equation', coarseKphi-rhs)

# Full fine-law differential operator computed independently from log(mu).
score_y, score_z = -y+b*(e+e**3), -(e+e**3)
def Kdensity(f):
    return S.expand(-dy(dy(f))-dz(dz(f))
                    -score_y*dy(f)-score_z*dz(f)+f-E(f))

Kg = Kdensity(g)
zero('full projected density tangent marginal vanishes', Ee(Kg))
zero('full projected density tangent total mass vanishes', E(Kg))
I = E(dz(q)**2)
zero('translated-quartic latent coercivity remainder',
     I-2*E(q)-((9-6*c)*delta**2+(S.Rational(9,2)+45*c)*delta**4+15*delta**6))
conditional_variance = E(q*q)-Ey(h*h)
observed_gradient = E((dy(q)-S.diff(phi,y))**2)
coarse_variance = Ey((h-phi)**2)-Ey(h-phi)**2
D = E(dy(g)**2+dz(g)**2+g*g)-E(g)**2
zero('four-term exact dissipation decomposition',
     D-I-conditional_variance-observed_gradient-coarse_variance)
zero('latent Fisher survives the multiplier', E(dz(g)**2)-I)
Bqg = E(dy(q)*dy(g)+dz(q)*dz(g)+q*g)-E(q)*E(g)
zero('projected duality in gradient form', Bqg-D)
zero('full density entropy pairing', E(q*Kg)-D)
zero('projection orthogonality',
     E(dy(g)*S.diff(phi,y)+g*phi)-E(g)*Ey(phi))

# Negative control: deleting the correlated-target score term leaves drift.
wrong_phi = (A*delta**2/2+3*delta**4/2)*H2/3+delta**4*H4/20
wrong_drift = Ee(Kdensity(q-wrong_phi))
zero('wrong multiplier residual equals missing score flux',
     wrong_drift-(y*m-S.diff(m,y)))
truth('wrong multiplier concretely fails',
      S.expand(wrong_drift.subs({a:1,delta:1})).coeff(y,4) == -1,
      S.factor(wrong_drift.subs({a:1,delta:1})))

# A general coarse log-ratio is annihilated by the projection. The Gaussian
# marginal mismatch below supplies an actual normalised-target instance.
L = S.symbols('L', real=True)
ell = -L*y+L*L/2  # log(N(0,1)/N(L,1))
q_total = q+ell
phi_total = phi+ell-Ey(ell)
zero('incompatible marginal leaves identical projected fields',
     q_total-phi_total-g-Ey(ell))
zero('incompatible marginal total entropy residual', E(q_total)-E(q)-L*L/2)

# Independent Gaussian innovation derivation for sharpness including reaction.
n, T, s, M, w = S.symbols('n T s M w', positive=True)
qg = S.log(T/s)/2-w*w/(2*s)+(M+w)**2/(2*T)
def Ew(poly):
    return S.expand(sum(coef*(S.factorial2(k[0]-1)*s**(k[0]//2)
                             if k[0] % 2 == 0 else 0)
                        for k,coef in S.Poly(S.expand(poly),w).terms()))
Eg = (s+M*M)/(2*T)-S.Rational(1,2)+S.log(T/s)/2
Ig = M*M/T**2+(s-T)**2/(s*T**2)
Vg = M*M*s/T**2+(s-T)**2/(2*T**2)
zero('Gaussian entropy', Ew(qg)-Eg)
zero('Gaussian Fisher', Ew(S.diff(qg,w)**2)-Ig)
zero('Gaussian reaction variance', Ew(qg*qg)-Ew(qg)**2-Vg)
zero('fixed target entropy leading coefficient',
     S.limit(Eg.subs({M:n,s:1/n})/n**2,n,S.oo)-1/(2*T))
zero('fixed target full dissipation leading coefficient',
     S.limit((Ig+Vg).subs({M:n,s:1/n})/n**2,n,S.oo)-1/T**2)
zero('fixed target sharp full dissipation over entropy',
     S.limit(((Ig+Vg)/Eg).subs({M:n,s:1/n}),n,S.oo)-2/T)

# Per-fibre increase at an admissible state of the inherited exact flow.
beta, variance = S.symbols('beta variance', positive=True)
edot = ((1-1/variance)*((1-variance)*(variance+2)+2*beta**2)/2
        -beta**2*(variance+2+beta**2/3)*y*y)
edot0 = S.expand(edot.subs({beta:1,variance:S.Rational(11,10)}))
zero('per-fibre derivative exact', edot0-(S.Rational(169,2200)-S.Rational(103,30)*y*y))
truth('per-fibre derivative positive near zero', edot0.subs(y,0)>0, edot0)
truth('integrated derivative negative', Ey(edot0)<0, Ey(edot0))

# Logistic constants reduce to elementary series integrals on (0,1).
# These identities evaluate the transformed integrands only, not Gaussian
# quadrature or an unproved universal functional inequality.
u = S.symbols('u', positive=True)
zero('logistic Fisher envelope integral', S.integrate(1-u,(u,0,1))-S.Rational(1,2))
zero('logistic entropy envelope series', S.summation(1/n**2,(n,1,S.oo))-S.pi**2/6)
zero('logistic variance envelope series', S.summation(2/n**3,(n,1,S.oo))-2*S.zeta(3))

summary = {
    'status': 'PASS',
    'independence': 'Separately written from report formulas; no author checker imported or read.',
    'scope': 'Exact symbolic identities and controls only; no PDE, LSI, existence, or empirical proof.',
    'sympy_version': S.__version__,
    'check_count': len(checks),
    'checks': checks,
    'derived_quartic_fisher': str(S.factor(I)),
    'derived_quartic_entropy': str(S.factor(E(q))),
    'quartic_moments_used': {str(k):str(v) for k,v in quartic_moments.items()},
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
text = json.dumps(summary,indent=2)+'\n'
if args.output:
    Path(args.output).write_text(text)
print(text)
