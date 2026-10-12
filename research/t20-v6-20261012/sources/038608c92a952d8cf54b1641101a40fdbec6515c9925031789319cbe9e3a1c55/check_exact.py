#!/usr/bin/env python3
"""Exact controls for the limit classification; not a theorem prover.

Uses only symbolic algebra and input hashes. Fresh output directories only.
No network, numerical simulation, predecessor writes, or external state changes.
"""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import sympy as S

BASE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', type=Path, required=True)
parser.add_argument('--original-root', type=Path)
args = parser.parse_args()
if args.output_dir.exists():
    parser.error('output directory already exists; choose a fresh path')
args.output_dir.mkdir(parents=True)
checks = []

def truth(label, value):
    assert value, (label, value)
    checks.append(label)

def zero(label, value):
    value = S.simplify(S.powsimp(value, force=False))
    if value != 0:
        value = S.cancel(S.expand(value))
    assert value == 0, (label, value)
    checks.append(label)

bindings = json.loads((BASE/'INPUT_BINDINGS.json').read_text())
for b in bindings:
    truth('copied input '+b['original'],
          hashlib.sha256((BASE/b['copy']).read_bytes()).hexdigest()==b['sha256'])
    if args.original_root:
        truth('original input unchanged '+b['original'],
              hashlib.sha256((args.original_root/b['original']).read_bytes()).hexdigest()==b['sha256'])

# Classical power-inequality consequences, checked as derivative identities.
h,g,k = S.symbols('h g k', positive=True)
theta = S.symbols('theta', real=True)
zero('length-power derivative',
     -S.diff(h**(1-theta),h)*(-g**2) - (1-theta)*h**(-theta)*g**2)
zero('integrated-gap power derivative',
     -S.diff(h**(2-2*theta),h)*(-g**2) - (2-2*theta)*h**(1-2*theta)*g**2)
zero('integrated-gap comparison equality',
     S.diff(h**(2-2*theta)/(k**2*(2-2*theta)),h)*(-k**2*h**(2*theta))+h)
zero('power-rate exceeds integrability threshold',
     1/(2*theta-1)-1-(2-2*theta)/(2*theta-1))
t,h0,b = S.symbols('t h0 b', positive=True)
hexp = h0*S.exp(-k**2*t)
zero('half-exponent exponential comparison', S.diff(hexp,t)+k**2*hexp)
# b=2theta-1>0; substitute a positive auxiliary denominator before simplification.
v = S.symbols('v', positive=True)
H = v**(-1/b)
zero('algebraic comparison derivative',
     S.diff(H,v)*k**2*b + k**2*v**(-1-1/b))

# Exact monomial family. Identities in a positive spatial coordinate apply
# to both signs by symmetry; zero is the stationary branch.
x,z,m = S.symbols('x z m', positive=True)
Fm=x**(2*m)/(2*m)
zero('monomial gradient',S.diff(Fm,x)-x**(2*m-1))
zero('monomial tail primitive all positive integer m',
     S.diff(x**2/(4*m),x)*(-x**(2*m-1))+Fm)
zero('monomial exponent convention',
     1/(2*((2*m-1)/(2*m))-1)-m/(m-1))
for n in (2,3,5):
    D=1+(2*n-2)*z**(2*n-2)*t
    X=z*D**(-S.Rational(1,2*n-2))
    # Reduce both terms to the same positive base without numerical evaluation.
    zero(f'monomial m={n} trajectory',S.diff(X,t)+X**(2*n-1))
    zero(f'monomial m={n} initial value',X.subs(t,0)-z)
    zero(f'monomial m={n} tail derivative',
         S.diff(X**2/(4*n),t)+X**(2*n)/(2*n))
    zero(f'monomial m={n} total excess',
         (X**2/(4*n)).subs(t,0)-z**2/(4*n))
    zero(f'monomial m={n} endpoint',S.limit(X,t,S.oo))
Xq=z*S.exp(-t)
Kq=z**2*(1-S.exp(-2*t))/4
zero('quadratic trajectory',S.diff(Xq,t)+Xq)
zero('quadratic accumulated energy',S.diff(Kq,t)-Xq**2/2)
zero('quadratic excess integral',S.limit(Kq,t,S.oo)-z**2/4)

# Exact general normalization for three labels with arbitrary time energies.
K=[S.Function(f'K{i}')(t) for i in range(3)]
f=S.symbols('f0:3', real=True)
a=S.symbols('a0:3', positive=True)
Z=sum(a[i]*S.exp(-K[i]) for i in range(3))
w=[a[i]*S.exp(-K[i])/Z for i in range(3)]
E=sum(w[i]*f[i] for i in range(3))
subs={S.diff(K[i],t):f[i] for i in range(3)}
zero('normalization sums to one',sum(w)-1)
for i in range(3):
    zero(f'replicator coordinate {i}',S.diff(w[i],t).subs(subs)+w[i]*(f[i]-E))
zero('log normalizer derivative',-S.diff(S.log(Z),t).subs(subs)-E)

# Two equal-energy winners and an exponential loser: exact limiting prefactors.
alpha=S.symbols('alpha0:3', positive=True)
delta=S.symbols('delta', positive=True)
D=alpha[0]+alpha[1]+alpha[2]*S.exp(-delta*t)
A=alpha[0]+alpha[1]
for i in (0,1):
    zero(f'winning weight {i} exact limit',S.limit(alpha[i]/D,t,S.oo)-alpha[i]/A)
losing_weight=alpha[2]*S.exp(-delta*t)/D
zero('losing weight exact prefactor',
     S.limit(S.exp(delta*t)*losing_weight,t,S.oo)-alpha[2]/A)
zero('equal-energy limiting ratio',(alpha[0]/A)/(alpha[1]/A)-alpha[0]/alpha[1])
zero('merging two coincident winners',alpha[0]/A+alpha[1]/A-1)
B,u,ai=S.symbols('B u ai', positive=True)
zero('winner error exact algebra',
     ai*(1+u)/(A+B)-ai/A-ai*(A*u-B)/(A*(A+B)))

# Double-well: variable v=exp(-2t), so d/dt=-2v d/dv.
D=z**2+(1-z**2)*v
X=z/S.sqrt(D)
zero('double-well denominator convex combination',D-((1-v)*z**2+v))
zero('double-well flow',-2*v*S.diff(X,v)-X*(1-X**2))
zero('double-well initial value',X.subs(v,1)-z)
zero('double-well positive endpoint',S.limit(X,v,0,dir='+')-1)
U=z**2/D
J=(U-1-S.log(U))/8
zero('double-well tail derivative',-2*v*S.diff(J,v)+(U-1)**2/4)
zero('double-well total excess',J.subs(v,1)-(z**2-1-S.log(z**2))/8)
zero('double-well tail endpoint',S.limit(J,v,0,dir='+'))
I2=(S.Integer(3)-S.log(4))/8
zero('double-well stationary label excess',(z**2-1-S.log(z**2)).subs(z,1)/8)
zero('double-well moving label excess',(z**2-1-S.log(z**2)).subs(z,2)/8-I2)
zero('double-well biased winner normalization',
     S.Rational(1,2)/(S.Rational(1,2)+S.exp(-I2)/2)-1/(1+S.exp(-I2)))

# Exact unequal-well and stable-saddle controls.
x,y=S.symbols('x y', real=True)
Fu=x**4/4-x**3/3-x**2
zero('unequal-well gradient factor',S.diff(Fu,x)-x*(x-2)*(x+1))
for q,c,Hess in [(-1,-S.Rational(5,12),3),(2,-S.Rational(8,3),6),(0,0,-2)]:
    zero(f'unequal-well critical point {q}',S.diff(Fu,x).subs(x,q))
    zero(f'unequal-well value {q}',Fu.subs(x,q)-c)
    zero(f'unequal-well Hessian {q}',S.diff(Fu,x,2).subs(x,q)-Hess)
zero('unequal-well energy gap',Fu.subs(x,-1)-Fu.subs(x,2)-S.Rational(9,4))
u=S.symbols('u',positive=True)
zero('left basin velocity below minus one',-S.diff(Fu,x).subs(x,-1-u)-u*(u+1)*(u+3))
zero('left basin velocity between minus one and zero',
     -S.diff(Fu,x).subs(x,-1+u)+u*(1-u)*(3-u))
Fs=(x**2-1)**2/4+y**2/2
zero('saddle invariant first coordinate',S.diff(Fs,x).subs(x,0))
zero('saddle trajectory second coordinate',S.diff(z*S.exp(-t),t)+z*S.exp(-t))
zero('saddle trajectory energy',Fs.subs({x:0,y:z*S.exp(-t)})-(S.Rational(1,4)+z**2*S.exp(-2*t)/2))
zero('saddle excess tail',S.diff(z**2*S.exp(-2*t)/4,t)+z**2*S.exp(-2*t)/2)
truth('saddle Hessian indefinite',S.hessian(Fs,(x,y)).subs({x:0,y:0})==S.diag(-1,1))

# Pure extinction with stationary atoms; explicit absent-basin sensitivity.
am,ap,a0=S.symbols('am ap a0', positive=True)
den=am+ap+a0*S.exp(-t/4)
wm,wp,w0=am/den,ap/den,a0*S.exp(-t/4)/den
Est=w0/4
for name,wi,fi in [('minus',wm,0),('plus',wp,0),('zero',w0,S.Rational(1,4))]:
    zero('stationary-position reaction '+name,S.diff(wi,t)+wi*(fi-Est))
zero('extinction losing prefactor',S.limit(S.exp(t/4)*w0,t,S.oo)-a0/(am+ap))
eps=S.symbols('eps', positive=True)
v_eps=eps/(eps+(1-eps)*S.exp(-delta*t))
zero('absent-basin fixed-time epsilon limit',S.limit(v_eps,eps,0,dir='+'))
zero('absent-basin long-time limit',S.limit(v_eps,t,S.oo)-1)
zero('absent-basin half-mass crossover',
     v_eps.subs(S.exp(-delta*t),eps/(1-eps))-S.Rational(1,2))
zero('absent-basin replicator logistic',S.diff(v_eps,t)-delta*v_eps*(1-v_eps))

# A continuum of critical endpoints: check polynomial circle constraints.
circle=x*x+y*y-1
Fc=circle**2/4
zero('circle critical x factor',S.diff(Fc,x)-x*circle)
zero('circle critical y factor',S.diff(Fc,y)-y*circle)
zero('circle energy zero modulo circle',S.rem(Fc,circle,x))

# The positive-time polynomial/exponential bound has an exact derivative.
N,t0,u=S.symbols('N t0 u',positive=True)
Q=(1+u)**N*S.exp(-t0*u)
zero('regularizing envelope derivative',S.diff(Q,u)-Q*(N/(1+u)-t0))
zero('regularizing envelope critical point',
     (N/(1+u)-t0).subs(u,N/t0-1))

report={'status':'all_exact_controls_passed','python':platform.python_version(),
        'sympy':S.__version__,'check_count':len(checks),
        'copied_input_count':len(bindings),
        'original_input_count':len(bindings) if args.original_root else 0,
        'scope':'Executed symbolic controls and input hashes only; no numerical simulation, independent review, formal-kernel proof, protected edit, integration, or closure.',
        'checks':checks}
(args.output_dir/'EXACT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'check_count':len(checks),'report':str(args.output_dir/'EXACT_CHECKS.json')}))
