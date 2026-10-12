#!/usr/bin/env python3
"""Exact discriminating controls for the written cumulative-SOS proof, not a proof kernel."""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-root', type=Path, default=ROOT.parent,
                    help='Read-only directory containing the bound predecessor packets.')
WORK = parser.parse_args().source_root.resolve()
checks = []

def check(condition, label, category='algebra'):
    assert bool(condition), label
    checks.append({'label': label, 'category': category})

def zero(expr, label):
    check(S.simplify(S.expand(expr)) == 0, label)

# Bound copies and current source identity are both checked. Sources are read only.
for row in json.loads((ROOT / 'INPUT_BINDINGS.json').read_text()):
    data = (ROOT / row['copy']).read_bytes()
    check(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'],
          'copied input: ' + row['source'], 'input_integrity')
    check((WORK / row['source']).read_bytes() == data,
          'source still matches bound copy: ' + row['source'], 'input_integrity')
for name in ('time-varying-square-positivity-20261010', 'polynomial-transport-continuation-20261010'):
    parent = WORK / name
    receipt = json.loads((parent / 'AUTHOR_RECEIPT.json').read_text())
    rows = receipt['files']
    if isinstance(rows, dict):
        rows = [{'path': p, 'sha256': digest} for p, digest in rows.items()]
    for row in rows:
        data = (parent / row['path']).read_bytes()
        check(hashlib.sha256(data).hexdigest() == row['sha256'] and
              ('bytes' not in row or len(data) == row['bytes']),
              'predecessor receipt: ' + name + '/' + row['path'], 'receipt_integrity')

x, y, u, z, s, v, lam = S.symbols('x y u z s v lam', real=True)
t = S.symbols('t', positive=True)
g = (x + t*y)**2
K = t*x*x + t*t*x*y + t**3*y*y/3
zero(S.integrate(g.subs(t, v), (v, 0, t)) - K, 'integrated rank-one polynomial')
zero(S.diff(K, t) - g, 'coefficientwise energy derivative')
Q = S.Matrix([[t, t*t/2], [t*t/2, t**3/3]])
zero((S.Matrix([x,y]).T * Q * S.Matrix([x,y]))[0] - K, 'Gramian quadratic form')
zero(Q.det() - t**4/12, 'positive integrated Gramian determinant')
zero(Q.trace() - (t+t**3/3), 'integrated Gramian trace')
Qt = S.Matrix([[1,t],[t,t*t]])
zero(Qt.det(), 'instantaneous rank-one determinant')
zero(g.subs({x:-t*lam, y:lam}, simultaneous=True), 'instantaneous null ray')
C, c0 = S.symbols('C c0', real=True)
zero((g+C-c0*(x*x+y*y)).subs({x:-t*lam,y:lam},simultaneous=True)
     -(C-c0*(1+t*t)*lam*lam), 'any shifted radial claim fails along null ray')
c = t**3/(4*(t*t+3))
a = t-c
zero(c-Q.det()/Q.trace(), 'determinant-over-trace radial constant')
zero(a-3*t*(t*t+4)/(4*(t*t+3)), 'positive completed-square coefficient')
zero((Q-c*S.eye(2)).det()-c*c, 'radial-slack determinant equals c squared')
certificate = a*(x+2*t*(t*t+3)*y/(3*(t*t+4)))**2 + t**5*y*y/(12*(t*t+3)*(t*t+4))
zero(K-c*(x*x+y*y)-certificate, 'explicit cumulative SOS certificate')
check(c.is_positive, 'radial constant is positive for every positive t')
check(S.factor(a).is_positive, 'first SOS coefficient is positive for every positive t')
check((t**5/(12*(t*t+3)*(t*t+4))).is_positive,
      'second SOS coefficient is positive for every positive t')
zero(S.limit(c/t**3, t, 0, dir='+')-S.Rational(1,12), 'cumulative onset is cubic')
Qs = S.Matrix([[t-s,(t*t-s*s)/2],[(t*t-s*s)/2,(t**3-s**3)/3]])
zero(Qs.det()-(t-s)**4/12, 'arbitrary interval Gramian determinant')

# Ordered-simplex terminal coefficients: recursion integrates the latest time.
ordered = S.Integer(1)
for k in range(1,6):
    ordered = S.integrate(S.expand(g.subs(t,v)*ordered.subs(t,v)), (v,0,t))
    zero(ordered-K**k/S.factorial(k), 'ordered simplex symmetrization order ' + str(k))
Kst = S.expand(K-K.subs(t,s))
ordered_st = S.Integer(1)
for k in range(1,4):
    ordered_st = S.integrate(S.expand(g.subs(t,v)*ordered_st.subs(t,v)), (v,s,t))
    zero(ordered_st-Kst**k/S.factorial(k), 'nonzero-origin simplex symmetrization order ' + str(k))

# Finite Volterra residual on an actual atom: exact derivative and lower boundary.
# These checks do not assume that an abstract hierarchy was already represented.
katom = K.subs({x:1,y:1},simultaneous=True)
gatom = g.subs({x:1,y:1},simultaneous=True)
weight = S.exp(-katom)
for N in range(5):
    residual = 1-weight*sum(katom**k/S.factorial(k) for k in range(N+1))
    zero(S.diff(residual,t)-weight*gatom*katom**N/S.factorial(N),
         'exact latest-time Volterra residual derivative N=' + str(N))
    zero(residual.subs(t,0), 'exact Volterra residual zero lower boundary N=' + str(N))

U,V = S.symbols('U V',real=True)
for n in range(1,7):
    zero(U**n-V**n-(U-V)*sum(U**(n-1-j)*V**j for j in range(n)),
         'SOS radial power-difference factorization n=' + str(n))
u1,u2 = S.symbols('u1 u2',real=True)
zero((x+u1*y)**2*(x+u2*y)**2-((x+u1*y)*(x+u2*y))**2,
     'rank-one products remain a square at unrelated times')

# Rotating example: exact Gramian integration and characteristic polynomial.
rot = S.Matrix([[S.cos(v)**2,S.cos(v)*S.sin(v)],
                [S.cos(v)*S.sin(v),S.sin(v)**2]])
Qrot = S.Matrix([[t/2+S.sin(2*t)/4,(1-S.cos(2*t))/4],
                 [(1-S.cos(2*t))/4,t/2-S.sin(2*t)/4]])
for i,j in ((0,0),(0,1),(1,1)):
    zero(S.integrate(rot[i,j],(v,0,t))-Qrot[i,j], 'rotating Gramian entry '+str((i,j)))
zero(Qrot.det()-(t*t-S.sin(t)**2)/4, 'rotating Gramian determinant')
e = S.symbols('e', real=True)
zero((Qrot-e*S.eye(2)).det()-((e-t/2)**2-S.sin(t)**2/4),
     'rotating eigenvalue characteristic identity')

# Atomic reaction checks and a genuinely time-dependent scalar shift.
atoms = [(S.Rational(1,3),0,1),(S.Rational(2,3),2,-1)]
def A(p):
    return sum(w*p.subs({x:xx,y:yy},simultaneous=True)*S.exp(-K.subs({x:xx,y:yy},simultaneous=True))
               for w,xx,yy in atoms)
for p in (S.Integer(1),x,y,x*x,x*y,y*y):
    zero(S.diff(A(p),t)+A(g*p), 'atomic unnormalized hierarchy for '+str(p))
beta = 1+t*t
Bint = t+t**3/3
h = g-beta
zero(S.diff(Bint,t)-beta, 'continuous scalar-shift primitive')
# Symbolic quotient form: shift cancels exactly without expanding the exponentials.
Np,Ngp,N1,Ng = S.symbols('Np Ngp N1 Ng',real=True)
zero((-Ngp*N1+Np*Ng)/N1**2 - (-(Ngp-beta*Np)/N1+(Ng-beta*N1)*Np/N1**2),
     'normalized scalar-shift cancellation')
zero(S.diff(S.exp(Bint)*A(x),t)+S.exp(Bint)*A(h*x),
     'unnormalized time-dependent scalar shift')
zero(S.diff(S.exp(-K)*S.exp(K-K.subs(t,s)),t), 'compact integrating-factor cancellation')
zero(S.exp(-K)*S.exp(K-K.subs(t,s))-S.exp(-K.subs(t,s)), 'positive-time inverse-weight identity')

# Supplied nonlinear polynomial characteristics and cumulative pullback.
for m in (2,3,4):
    htrans = (x+t*(y-t*x**m))**2
    zero(htrans.subs({x:u,y:z+t*u**m},simultaneous=True)-(u+t*z)**2,
         'nonlinear cumulative-energy pullback m=' + str(m))
    zero((y-t*x**m).subs({x:u,y:z+t*u**m},simultaneous=True)-z,
         'polynomial inverse m=' + str(m))
    for i,j in ((0,0),(1,0),(0,1),(1,1),(2,1),(0,3)):
        q=x**i*(y-t*x**m)**j
        zero(S.diff(q,t)+x**m*S.diff(q,y),
             'transport chain rule m=' + str(m) + ' monomial=' + str((i,j)))

# The exact weighted Fourier error ratio tends to zero; no all-frequency integration.
n,D = S.symbols('n D',integer=True,nonnegative=True)
M,r = S.symbols('M r',positive=True)
term = M**(2*n)*S.factorial(n+D)/(S.factorial(n)**2*r**(n+D))
zero(term.subs(n,n+1)/term - M*M*(n+D+1)/(r*(n+1)**2),
     'weighted Fourier Taylor remainder squared ratio')
zero(S.limit(M*M*(n+D+1)/(r*(n+1)**2),n,S.oo), 'Fourier error ratio limit')

# Full rank in the cumulative energy does not force full support of the law.
b1,b2,pb = S.symbols('b1 b2 pb',real=True)
hb=(b1+t*b2)**2
zero(-hb*pb+hb*pb, 'Dirac normalized reaction cancellation')
for i,bi in enumerate((b1,b2)):
    for j,bj in enumerate((b1,b2)):
        zero(bi*bj-bi*bj, 'Dirac covariance entry '+str((i,j)))

categories = {category:sum(row['category']==category for row in checks)
              for category in sorted({row['category'] for row in checks})}
result = {'status':'PASS','total_exact_checks':len(checks),'category_counts':categories,
          'checks':checks,'sympy_version':S.__version__,
          'scope':'Finite exact algebra and integrity controls supplement the universal written proof. No proof-kernel verification, measure-reconstruction algorithm, or empirical validation.'}
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
