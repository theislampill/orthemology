from pathlib import Path
import json
from itertools import product
import sympy as s
x,y,z=s.symbols('x y z', real=True)
def lam(p):
    def m(e):
        if e==(0,0,0): return s.Integer(1)
        if sorted(e)==[0,0,2]: return s.Integer(4)
        if sorted(e)==[0,0,4]: return s.Integer(50)
        if sorted(e)==[0,2,2]: return s.Integer(1)
        if e==(1,1,1): return s.Rational(3,2)
        return s.Integer(0)
    return s.expand(sum(c*m(e) for e,c in s.Poly(s.expand(p),x,y,z).terms()))
mons=[1,x,y,z,x*x,x*y,x*z,y*y,y*z,z*z]
M=s.Matrix([[lam(u*v) for v in mons] for u in mons])
L,D=M.LDLdecomposition(hermitian=False)
assert all(d>0 for d in D.diagonal())
assert L*D*L.T==M
F=1-4*x*y*z+x*x*y*y+x*x*z*z+y*y*z*z
assert lam(F)==-2
assert lam((x**3-x)**2)==-96
# Two actual identities suffice to prove global nonnegativity without AM-GM:
# F+4xyz = 1+A+B+C >= 4|xyz|, using repeated two-term square bounds.
# Check the standard degree-eight certificate F*(1+...)? No extra asserted identity.
coeffs=s.symbols('a0:10',real=True)
p=sum(a*m for a,m in zip(coeffs,mons))
a=s.Matrix(coeffs)
assert s.expand(lam(p*p)-(a.T*M*a)[0])==0
out={'independent_exact_LDL':True,'LDL_diagonal':[str(d) for d in D.diagonal()],
     'universal_symbolic_10_coefficient_square_identity':True,'witness_lambda':'-2',
     'degree_3_square_counterexample':'-96','scope':'independent symbolic supplement, not kernel proof'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
