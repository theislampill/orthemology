#!/usr/bin/env python3
"""Small symbolic controls for the action-tail successor; no numerical sampling."""
import argparse, hashlib, json, platform
from pathlib import Path
import sympy as S

BASE=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--output-dir',type=Path,required=True)
p.add_argument('--original-root',type=Path)
a=p.parse_args()
if a.output_dir.exists(): p.error('choose a fresh output directory')
a.output_dir.mkdir(parents=True)
checks=[]
def ok(label,condition):
    assert condition,label
    checks.append(label)
def zero(label,expr):
    expr=S.simplify(expr)
    assert expr==0,(label,expr)
    checks.append(label)
bindings=json.loads((BASE/'INPUT_BINDINGS.json').read_text())
for row in bindings:
    ok('copied binding '+row['original'],hashlib.sha256((BASE/row['copy']).read_bytes()).hexdigest()==row['sha256'])
    if a.original_root:
        ok('original unchanged '+row['original'],hashlib.sha256((a.original_root/row['original']).read_bytes()).hexdigest()==row['sha256'])

h,D,C=S.symbols('h D C',positive=True)
theta=S.symbols('theta',real=True)
zero('action-length power derivative',
     -S.diff(h**(1-theta),h)*(-D)-(1-theta)*h**(-theta)*D)
zero('comparison action-tail primitive',
     S.diff(h**(1-theta)/(S.sqrt(C)*(1-theta)),h)*(-C*h**(2*theta))+S.sqrt(C)*h**theta)
eps,b,gap=S.symbols('eps b gap',nonnegative=True)
u=eps+b; hlow=eps/2-gap
zero('high-region half-gap remainder',u-hlow-u/2-(b/2+gap))
t,h0,beta=S.symbols('t h0 beta',positive=True)
hexp=h0*S.exp(-C*t)
zero('half-exponent comparison',S.diff(hexp,t)+C*hexp)
q=S.symbols('q',positive=True)
zero('algebraic comparison power',S.diff(q**(-1/beta),q)*C*beta+C*q**(-1-1/beta))
zero('algebraic action-tail exponent',
     ((1-theta)/(2*theta-1)).subs(theta,(beta+1)/2)-(1-beta)/(2*beta))

# Exact inherited stationary double-well control: gradient-only coercivity fails.
mass=S.symbols('mass',positive=True)
f0=S.Integer(0);f1=S.Rational(1,4)
mean=mass*f1
variance=(1-mass)*(f0-mean)**2+mass*(f1-mean)**2
zero('double-well mixture mean',mean-mass/4)
zero('double-well mixture variance',variance-mass*(1-mass)/16)
x=S.symbols('x',real=True)
F=(x*x-1)**2/4
ok('double-well both positions critical',all(S.diff(F,x).subs(x,q)==0 for q in (0,1)))

# The log-Pareto energy density and quadratic clock use exact primitives.
y,s=S.symbols('y s',positive=True)
primitive=-1/S.log(y)
rho=1/(y*S.log(y)**2)
zero('log-Pareto density primitive',S.diff(primitive,y)-rho)
zero('log-Pareto probability normalization',S.limit(primitive,y,S.oo)-primitive.subs(y,S.E)-1)
zero('low interval probability one half',primitive.subs(y,S.E**2)-primitive.subs(y,S.E)-S.Rational(1,2))
zero('high interval logarithmic mass',S.log(2/s)-S.log(1/s)-S.log(2))
clock=(1-S.exp(-2*t))/2
zero('quadratic clock derivative',S.diff(clock,t)-S.exp(-2*t))
Y=S.symbols('Y',positive=True)
Ft=Y*S.exp(-2*t)
zero('quadratic accumulated energy',S.diff(clock*Y,t)-Ft)
zero('reaction-length clock cancellation',S.exp(-2*t)/S.diff(clock,t)-1)
c=S.exp(-S.Rational(5,2))*S.log(2)/8
zero('two-interval variance lower constant',
     (S.exp(-S.Rational(1,2))/2)*(S.exp(-2)*S.log(2))/4-c)
divergence_primitive=-S.log(S.log(2/s))
zero('initial-length divergent primitive',S.diff(divergence_primitive,s)-1/(s*S.log(2/s)))
ok('initial-length lower primitive tends to minus infinity',S.limit(divergence_primitive,s,0,dir='+')==-S.oo)

report={'status':'all_exact_controls_passed','python':platform.python_version(),'sympy':S.__version__,
        'check_count':len(checks),'symbolic_control_count':len(checks)-len(bindings)*(2 if a.original_root else 1),
        'copied_input_count':len(bindings),'original_input_count':len(bindings) if a.original_root else 0,
        'scope':'Symbolic control identities and binding checks, not a numerical sampling campaign or formal proof. No closure authority.','checks':checks}
(a.output_dir/'EXACT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'check_count':len(checks),'symbolic_control_count':report['symbolic_control_count']}))
