import sympy as s, json
x,y,t=s.symbols('x y t',real=True)
points=[(-2,1),(0,-1),(3,2)]
lam=[a+2*b for a,b in points]
# Choose a genuinely separating projection; x+2y collides at first two? values 0,-2,7 distinct.
ell=x+2*y
checks={}
for j,(a,b) in enumerate(points):
    q=s.prod((ell-lam[k])/(lam[j]-lam[k]) for k in range(3) if k!=j)
    for i,z in enumerate([x,y]):
        p=(z-points[j][i])*q**2
        for k,pt in enumerate(points):
            ev={x:pt[0],y:pt[1]}
            assert s.simplify(p.subs(ev))==0
            for l,zz in enumerate([x,y]):
                assert s.simplify(s.diff(p,zz).subs(ev))==int(k==j and i==l)
checks['frozen_hermite_jets']='passed 18 values and 36 derivative checks'
weights=[s.Rational(1,6),s.Rational(1,3),s.Rational(1,2)]
V=s.Matrix([[z**k for z in lam] for k in range(3)])
B=V*s.diag(*weights)*V.T
assert B.det()>0
for coord in range(2):
    m=s.Matrix([sum(weights[j]*points[j][coord]*lam[j]**k for j in range(3)) for k in range(3)])
    recovered=s.diag(*[1/w for w in weights])*V.inv()*m
    assert list(recovered)==[pt[coord] for pt in points]
checks['projection_recovery']={'vandermonde_determinant':str(V.det()),'hankel_determinant':str(B.det())}
# Signed, changing-direction, nonlinear polynomial energy.
h=t*x+(t*t-1)*y+t*x*y
E=[s.integrate(h.subs({x:a,y:b}),(t,0,t)) for a,b in points]
u=[weights[j]*s.exp(-E[j]) for j in range(3)]
Z=sum(u)
hv=[h.subs({x:a,y:b}) for a,b in points]
for j in range(3):
    assert s.simplify(s.diff(u[j],t)+hv[j]*u[j])==0
# Unnormalized identity + quotient rule proves normalized hierarchy for all fixed test values.
checks['signed_polynomial_energy_reaction']='all atomic unnormalized ODEs pass exact symbolic differentiation'
# Gaussian finite truncations have finite rank while ranks increase indefinitely.
def moment(k):
    return s.Integer(0) if k%2 else s.factorial2(k-1) if k else s.Integer(1)
ranks=[]
for n in range(5):
    G=s.Matrix([[moment(i+j) for j in range(n+1)] for i in range(n+1)])
    assert G.det()>0
    ranks.append(G.rank())
checks['truncation_does_not_bound_full_rank']={'gaussian_ranks_n0_to_n4':ranks}
f=t*t
assert s.simplify(s.diff(f,t)**2-4*f)==0
checks['square_root_null_escape_control']='f=t^2 satisfies (f prime)^2=4f yet leaves zero; not a hierarchy counterexample'
print(json.dumps({'status':'pass','checks':checks},indent=2))
