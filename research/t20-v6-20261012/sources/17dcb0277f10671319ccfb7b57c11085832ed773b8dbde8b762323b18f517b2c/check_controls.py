"""Independent, finite exact controls. These do not prove the universal theorem."""
import hashlib
import json
from pathlib import Path
import sympy as S

ROOT = Path('private-locator:8f24556a330b05a11a95')
OUT = Path(__file__).resolve().parent
EXPECTED = {
    'partial-cumulative-law-persistence-20261010/RESULT.md': 'cf9b6626b24329f8dd27d2ff2d78027ea4e222f45a6b7621209aa4d39b840fe3',
    'partial-cumulative-one-hidden-lift-20261010/GENERAL_SOS_BRIDGE.md': '9f20a6b0125b98a659d87b0a3758630b4e3ded99ba376e1bf4fbcc31d49765db',
    'cumulative-square-positivity-20261010/RESULT.md': 'a530a5341497e3416345a7ec325e986a7e54f2c254954f80fd32f1f596e6244f',
    'partial-quadratic-rank-classification-20261010/sources/putinar-schmudgen-0810.0840v1.pdf': '9e551b5856cdf1065f1170641bed91a1d0f40c1d19368c9187f0c3d16661ac94',
}
checks = []

def check(name, condition):
    assert condition, name
    checks.append(name)

def zero(name, expr):
    check(name, S.simplify(S.expand(expr)) == 0)

for relative, expected in EXPECTED.items():
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    check('source binding: ' + relative, actual == expected)

h, b = S.symbols('h b', real=True)
zero('polarization represents h', ((h+1)**2-(h-1)**2)/4-h)
zero('Gaussian variation constant', ((h+1)**2+(h-1)**2)/4-(1+h*h)/2)
zero('square polarization represents b squared', ((b*b+1)**2-(b*b-1)**2)/4-b*b)

z, y1, y2 = S.symbols('z y1 y2', real=True)
t, s, u, v = S.symbols('t s u v', real=True)
g = z**4 + t**2*z**2
K = t*z**4 + t**3*z**2/3
zero('higher-degree schedule primitive', S.diff(K,t)-g)
zero('higher-degree cumulative certificate', K-t**3*z**2/3-t*z**4)
W = S.exp(K.subs(t,s)-K)
zero('weight evolution at every z', S.diff(W,t)+g*W)
zero('integrating-factor cancellation', S.diff(S.exp(K-K.subs(t,s)),t)-g*S.exp(K-K.subs(t,s)))
zero('weight cocycle', (K.subs(t,s)-K.subs(t,u))+(K.subs(t,u)-K.subs(t,v))-(K.subs(t,s)-K.subs(t,v)))

n, D = S.symbols('n D', integer=True, nonnegative=True)
zero('squared factorial-remainder ratio', S.factorial(n+D+1)/S.factorial(n+D)/(n+1)**2-(n+D+1)/(n+1)**2)

atoms = [(0,1,-2,S.Rational(1,5)),(1,2,3,S.Rational(1,3)),(-2,-1,4,S.Rational(7,15))]
check('atomic weights sum to one', sum(w for _,_,_,w in atoms) == 1)
def A(p):
    return sum(w*p.subs({z:zi,y1:ai,y2:bi})*S.exp(-K.subs(z,zi)) for zi,ai,bi,w in atoms)
p = (1+z*y1-y2**2)**2
zero('joint mixed-square unnormalized hierarchy', S.diff(A(p),t)+A(g*p))
Z = A(S.Integer(1))
zero('atomic normalizer equation', S.diff(Z,t)+A(g))
zero('atomic normalized mixed hierarchy', S.diff(A(p)/Z,t)+A(g*p)/Z-A(g)*A(p)/Z**2)
for i,(zi,ai,bi,w) in enumerate(atoms):
    rho = w*S.exp(-K.subs({t:s,z:zi}))/Z.subs(t,s)
    zero(f'atomic fibre inverse {i}', Z.subs(t,s)*S.exp(K.subs({t:s,z:zi}))*rho-w)

degenerate_atoms = [(S.Integer(0),S.Integer(1),S.Integer(-1),S.Rational(1,2)),
                    (S.Integer(2),S.Integer(3),S.Integer(-3),S.Rational(1,2))]
zero('zero-mass hidden-square example', sum(w*(ai+bi)**2 for zi,ai,bi,w in degenerate_atoms))
zero('zero-mass example controlled moment', sum(w*zi**5*(ai+bi)**2 for zi,ai,bi,w in degenerate_atoms))
check('signed cancellation needs separate square control', S.Rational(1,2)*1+S.Rational(1,2)*(-1)==0 and S.Rational(1,2)*1**2+S.Rational(1,2)*(-1)**2==1)

z1,z2 = S.symbols('z1 z2', real=True)
radial_gap = S.Poly((z1*z1+z2*z2)**3-z1*z1*z2**4,z1,z2)
check('mixed monomial square radial majorant control', all(c>=0 and all(e%2==0 for e in powers) for powers,c in radial_gap.terms()))

result = {'kind':'finite exact supporting controls, not a proof by sampling',
          'sympy_version':S.__version__, 'passed':len(checks), 'failed':0,
          'checks':checks, 'source_bindings':EXPECTED}
(OUT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':len(checks),'failed':0,'result_file':str(OUT/'CONTROL_RESULTS.json')}))
