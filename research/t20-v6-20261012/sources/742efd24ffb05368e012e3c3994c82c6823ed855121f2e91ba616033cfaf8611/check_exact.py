from pathlib import Path
import json
import sympy as s
x,y,z,t,a,T=s.symbols('x y z t a T', real=True)
X=(x,y,z)
exponents=[(i,j,k) for n in range(5) for i in range(n+1) for j in range(n-i+1) for k in [n-i-j]]
assert len(exponents)==35

def mon(alpha):
    return s.prod(v**n for v,n in zip(X,alpha))
def moment(alpha):
    if alpha==(0,0,0): return s.Integer(1)
    if sorted(alpha)==[0,0,2]: return s.Integer(4)
    if sorted(alpha)==[0,0,4]: return s.Integer(50)
    if sorted(alpha)==[0,2,2]: return s.Integer(1)
    if alpha==(1,1,1): return s.Rational(3,2)
    return s.Integer(0)
def evaluate(p, scale=1):
    poly=s.Poly(s.expand(p),*X)
    assert poly.total_degree()<=4
    return s.expand(sum(c*moment(alpha)*scale**sum(alpha) for alpha,c in poly.terms()))
def lap(p): return s.expand(sum(s.diff(p,v,2) for v in X))
def heat(p,time):
    out=s.Integer(0); d=p; k=0
    while d!=0:
        out+=time**k*d/s.factorial(k)
        d=lap(d); k+=1
    return s.expand(out)
basis=[1,x*x,y*y,z*z,x,y*z,y,x*z,z,x*y]
M=s.Matrix([[evaluate(u*v) for v in basis] for u in basis])
E=s.Matrix([[1,4,4,4],[4,50,1,1],[4,1,50,1],[4,1,1,50]])
O=s.Matrix([[4,s.Rational(3,2)],[s.Rational(3,2),1]])
assert M==s.diag(E,O,O,O)
Schur=E[1:,1:]-E[1:,0:1]*E[0:1,1:]
assert Schur==49*s.eye(3)-15*s.ones(3)
assert Schur.eigenvals()=={s.Integer(4):1,s.Integer(49):2}
assert O.det()==s.Rational(7,4)
minors=[s.factor(M[:k,:k].det()) for k in range(1,11)]
assert all(v>0 for v in minors)
F=1-4*x*y*z+x*x*y*y+x*x*z*z+y*y*z*z
assert evaluate(F)==-2
assert evaluate(heat(F,t))==-2+48*t+12*t*t
Fa=F.subs({x:x/a,y:y/a,z:z/a},simultaneous=True)
assert s.simplify(evaluate(heat(Fa,t),a)-(-2+48*t/a**2+12*t*t/a**4))==0
assert (-2+48*t+12*t*t).subs(t,s.Rational(1,100))==s.Rational(-3797,2500)
for alpha in exponents:
    p=mon(alpha)
    assert s.expand(heat(heat(p,T),-T)-p)==0
    assert s.simplify(evaluate(heat(heat(p,-T),T),a)-evaluate(p,a))==0
# Concrete a=10,T=1: preserve every degree<=4 moment of L=Lambda_a o P_T.
concrete={','.join(map(str,alpha)):str(evaluate(heat(mon(alpha),1),10)) for alpha in exponents}
witness=s.expand(Fa.subs(a,10))
assert evaluate(heat(witness,1),10)==s.Rational(-3797,2500)
negative_control=M.copy(); negative_control[0,0]=-1
assert negative_control[:1,:1].det()<0
result={'status':'PASS_EXACT_RATIONAL_AND_SYMBOLIC_DIAGNOSTIC','scope':'ternary polynomial degree<=4 only; no full functional extension claimed','moment_basis_size':35,'square_Gram_dimension':10,'Gram_block_identity':True,'even_Schur_eigenvalues':{'4':1,'49':2},'odd_block_determinant':'7/4','all_leading_principal_minors':[str(v) for v in minors],'initial_nonnegative_witness_value':'-2','scaled_heat_witness':'-2+48*t/a^2+12*t^2/a^4','whole_window_bound_for_t_over_a_squared_at_most_1_over_100':'-3797/2500','heat_inverse_all_35_basis_vectors':True,'concrete_parameters':{'a':10,'T':1},'concrete_witness':str(witness),'concrete_witness_value':'-3797/2500','concrete_L_moments':concrete,'negative_mass_control_rejected':True,'Lean_verified':False}
out=Path(__file__).with_name('EXACT_RESULTS.json');out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='concrete_L_moments'},indent=2))
