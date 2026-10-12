#!/usr/bin/env python3
"""Independent exact controls for the nonautonomous proof's delicate algebra."""
from pathlib import Path
from fractions import Fraction
import hashlib,json
import sympy as S
ROOT=Path(__file__).resolve().parent
checks=[]
def check(ok,name):
    assert bool(ok),name
    checks.append(name)
def eq(a,b,name): check(S.simplify(a-b)==0,name)

for row in json.loads((ROOT/'author-snapshot/INPUT_BINDINGS.json').read_text()):
    original=(ROOT.parent/row['source']).read_bytes()
    copied=(ROOT/'author-snapshot'/row['copy']).read_bytes()
    check(original==copied,'unchanged bytes: '+row['source'])
    check(hashlib.sha256(original).hexdigest()==row['sha256'],'unchanged hash: '+row['source'])

# Full backwards partial-sum inequality, beyond checking only its last term.
v,delta,c=S.symbols('v delta c',positive=True)
f=sum((j+1)*v**j for j in range(6))
for N in range(6):
    partial=sum((c*delta)**j*(S.diff(f,v,j).subs(v,0)/c**j)/S.factorial(j)
                for j in range(N+1))
    difference=S.Poly(S.expand(f.subs(v,delta)-partial),delta)
    check(all(coefficient>=0 for coefficient in difference.all_coeffs()),
          'full positive backward sum N='+str(N))

# A truly changing quartic objective, rather than a scalar multiple of one energy.
x,y,t,s,H=S.symbols('x y t s H',real=True)
R=x*x+y*y
h=(x-t)**2+(y+t)**2+(x*y-t)**2
g=h+2*H*H
slack=(x-2*t)**2/2+(y+2*t)**2/2+(x*y-t)**2+2*(H*H-t*t)
eq(g-R/2,slack,'moving quartic SOS radial identity')
for time in [S.Rational(0),S.Rational(1,10),S.Rational(1,5)]:
    check((2*(H*H-t*t)).subs({H:S.Rational(1,5),t:time})>=0,
          'window scalar SOS remainder t='+str(time))
U=S.integrate(g,(t,0,t))
eq(S.diff(U,t),g,'integrated quartic energy')
points=[(-1,0),(0,1),(1,-1)]
weights=[S.Rational(1,6),S.Rational(1,3),S.Rational(1,2)]
def at(p,point): return S.sympify(p).subs({x:point[0],y:point[1]},simultaneous=True)
def A(p): return sum(w*at(p,point)*S.exp(-at(U,point)) for w,point in zip(weights,points))
for n in range(3):
    eq(-S.diff(A(R**n),t)-A(R**(n+1))/2,A(R**n*slack),
       'first derivative radial slack n='+str(n))
for p in [x,y,x*y,x*x-y]:
    eq(S.diff(A(p),t),-A(g*p),'changing quartic signed hierarchy '+str(p))

# The integrating factor is checked pointwise; compact support is a proof premise.
factor=S.exp(U-U.subs(t,s))
eq(S.exp(-U)*factor,S.exp(-U.subs(t,s)),'two-time factor identity')
eq(S.diff(S.exp(-U)*factor,t),0,'factor product has zero derivative')

# Exact weighted Fourier-tail ratio tends to zero with arbitrary fixed degree.
n,D=S.symbols('n D',integer=True,nonnegative=True)
M,r=S.symbols('M r',positive=True)
squared_ratio=M*M*(n+D+1)/(r*(n+1)**2)
eq(S.limit(squared_ratio,n,S.oo),0,'weighted Fourier remainder ratio limit')

# C0 energy coefficients need not give any second time derivative of the path.
left=S.Rational(3,2)*t-t*t/2
right=S.Rational(1,4)+t/2+t*t/2
eq(left.subs(t,S.Rational(1,2)),right.subs(t,S.Rational(1,2)),
   'integrated nonsmooth coefficient is continuous')
eq(S.diff(left,t).subs(t,S.Rational(1,2)),S.diff(right,t).subs(t,S.Rational(1,2)),
   'integrated nonsmooth coefficient is C1')
check(S.diff(left,t,2)!=S.diff(right,t,2),'second time derivative is not required')

# Rational calculation independent of SymPy for the shifted sign countercontrol.
time=Fraction(1,10);C=Fraction(1,25)
for atom,wanted in [(Fraction(-1),Fraction(-51,80)),(Fraction(0),Fraction(-79,400))]:
    energy=(atom-time)**2+C
    derivative=-2*(atom-time)
    coefficient=energy**2-derivative
    check(coefficient==wanted and coefficient<0,'negative shifted coefficient at '+str(atom))

out={'status':'PASS','total_exact_checks':len(checks),'checks':checks,
     'sympy_version':S.__version__,'scope':'Finite exact controls supplement the universal proof review.'}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
