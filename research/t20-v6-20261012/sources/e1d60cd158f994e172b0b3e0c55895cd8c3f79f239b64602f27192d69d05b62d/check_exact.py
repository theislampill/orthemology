"""Exact local algebra controls; the accompanying proof handles all indices and gluing."""
import json
import sympy as s
from pathlib import Path
x,c,n=s.symbols('x c n', positive=True)
t=s.symbols('t', real=True)
X=1/(1-t)
C=s.exp((1-(1-t)**(-3))/3)
checks={}
checks['characteristic']=s.simplify(s.diff(X,t)-X**2)==0
checks['weight']=s.simplify(s.diff(C,t)+X**4*C)==0
checks['source_dual_reaction']=s.simplify((-x**4-2*x)+s.diff(x**2,x)+x**4)==0
D=lambda f:s.expand(x**2*s.diff(f,x)-x**4*c*s.diff(f,c))
checks['general_moving_moment']=s.simplify(D(c*x**n)-(n*c*x**(n+1)-c*x**(n+4)))==0
m=lambda k:(s.Integer(1) if k==0 else s.Integer(0))+c*x**k
q=lambda k:m(k)/(1+c)
for k in range(13):
    checks[f'linear_moment_{k}']=s.simplify(D(m(k))-(k*m(k+1)-m(k+4)))==0
    checks[f'normalized_moment_{k}']=s.simplify(D(q(k))-(k*q(k+1)-q(k+4)+q(4)*q(k)))==0
H=s.Matrix([[m(i+j) for j in range(3)] for i in range(3)])
checks['linear_rank2_minor']=s.simplify(H[:2,:2].det()-c*x**2)==0
checks['linear_rank3_minor_zero']=s.simplify(H.det())==0
checks['normalized_rank2_minor']=s.simplify((H[:2,:2]/(1+c)).det()-c*x**2/(1+c)**2)==0
# Derivatives of exp((1-x^3)/3) P(x) remain of that form.
P=x**7
for r in range(8):
    lhs=s.diff(s.exp((1-x**3)/3)*P,x)*x**2
    Q=s.expand(x**2*s.diff(P,x)-x**4*P)
    checks[f'flatness_polynomial_recursion_{r}']=s.simplify(lhs-s.exp((1-x**3)/3)*Q)==0
    P=Q
RX=1/t
RC=s.exp(-1/(3*t**3))
checks['reverse_characteristic']=s.simplify(s.diff(RX,t)+RX**2)==0
checks['reverse_weight']=s.simplify(s.diff(RC,t)-RX**4*RC)==0
checks['reverse_source_dual_reaction']=s.simplify(x**4+2*x+s.diff(-x**2,x)-x**4)==0
for k in range(13):
    checks[f'reverse_linear_moment_{k}']=s.simplify(-D(m(k))-(-k*m(k+1)+m(k+4)))==0
    checks[f'reverse_normalized_moment_{k}']=s.simplify(-D(q(k))-(-k*q(k+1)+q(k+4)-q(4)*q(k)))==0
checks['all_pass']=all(checks.values())
Path(__file__).with_name('EXACT_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
assert checks['all_pass']
