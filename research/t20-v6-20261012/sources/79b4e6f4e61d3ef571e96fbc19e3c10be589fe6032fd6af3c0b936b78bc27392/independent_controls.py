from fractions import Fraction as F
import math,json
from pathlib import Path
import sympy as s
checks=[]
def check(name,c):
    assert c,name
    checks.append(name)
def eq(name,a,b): check(name,s.simplify(a-b)==0)
t=s.symbols('t',real=True)
z=s.symbols('z',positive=True)
# Independent direct t-parameterized signed three-atom model.
w=[F(1,2),F(1,3),F(1,6)]; e=[-1,0,1]
a=[s.Rational(v.numerator,v.denominator)*s.exp(-t*h) for v,h in zip(w,e)]
Z=sum(a); W=[v/Z for v in a]
for k in range(8):
    obs=sum(Wi*h**k for Wi,h in zip(W,e))
    nxt=sum(Wi*h**(k+1) for Wi,h in zip(W,e))
    mean=sum(Wi*h for Wi,h in zip(W,e))
    eq(f'atomic normalized hierarchy {k}',s.diff(obs,t),-nxt+mean*obs)
for i,v in enumerate([s.Rational(12,17),s.Rational(4,17),s.Rational(1,17)]): eq(f'log2 weight {i}',W[i].subs(t,s.log(2)),v)
for n in range(50): check(f'odd factorial interpolation {n}',F((2*n+2),(2*n+1))<=2)
# Gaussian negative quadratic: all even moments, direct hierarchy at finite degrees.
G=(1-2*t)**(-s.Rational(1,2))
eq('Gaussian logarithmic derivative',s.diff(s.log(G),t),1/(1-2*t))
for n in range(10):
    mn=s.factorial2(2*n-1)/(1-2*t)**n if n else s.Integer(1)
    nextm=s.factorial2(2*n+1)/(1-2*t)**(n+1)
    eq(f'Gaussian normalized recurrence {n}',s.diff(mn,t),nextm-mn/(1-2*t))
check('Gaussian second moment diverges',s.limit(1/(1-2*t),t,s.Rational(1,2),dir='-')==s.oo)
check('Gaussian normalizer diverges',s.limit(G,t,s.Rational(1,2),dir='-')==s.oo)
# Null square on support, polarization, nonlinear support energies, switches.
x,y=s.symbols('x y',real=True); atoms=[(0,1),(s.Rational(1,2),s.Rational(1,2)),(1,0)]
check('null polynomial on support',all((x+y-1).subs({x:xx,y:yy})==0 for xx,yy in atoms))
eq('polarization',(x+1)**2/4-(x-1)**2/4,x)
check('nonlinear signed energies',[(x**3-3*y).subs({x:xx,y:yy}) for xx,yy in atoms]==[-3,-s.Rational(11,8),1])
end=[s.Rational(v.numerator,v.denominator)*s.Rational(3,2)**h for v,h in zip(w,e)]
check('signed reverse switch endpoint',[s.simplify(v/sum(end)) for v in end]==[s.Rational(4,11),s.Rational(4,11),s.Rational(3,11)])
# Gaussian signed linear: polynomial moments of N(-t,1).
def gl(n):
    return sum(s.factorial(n)*(-t)**(n-2*k)/(2**k*s.factorial(k)*s.factorial(n-2*k)) for k in range(n//2+1))
for n in range(13): eq(f'Gaussian signed linear recurrence {n}',s.diff(gl(n),t),-gl(n+1)-t*gl(n))
# Explicit failed positivity and unbounded geometric horizon countercontrols.
u=s.symbols('u',positive=True)
flat=1-s.exp(-1/u)/2
eq('flat negative square',s.diff(flat,u,2).subs(u,s.Rational(1,4)),-64*s.exp(-4))
eq('geometric energy mean',-z*s.diff(1/(2-z),z)/(1/(2-z)),-z/(2-z))
for n in range(10): eq(f'lognormal sine moment cancellation {n}',s.sin(2*s.pi*n),0)
result={'status':'PASS','count':len(checks),'checks':checks,'scope':'Independent finite exact controls; universal proof separately audited.'}
Path(__file__).with_name('INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS',len(checks))
