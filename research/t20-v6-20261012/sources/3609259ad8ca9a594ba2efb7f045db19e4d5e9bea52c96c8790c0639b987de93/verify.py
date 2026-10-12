#!/usr/bin/env python3
"""Exact controls for the ordinary proof in RESULT.md; not a formal theorem proof."""
import sympy as S

Q = S.Rational
x1, x2, y1, y2 = S.symbols('x1 x2 y1 y2', positive=True)
h1, h2, z, tau = S.symbols('h1 h2 z tau', real=True)
x = S.Matrix([x1, x2])
y = S.Matrix([y1, y2])
one = S.ones(2, 1)
s, t = sum(x), sum(y)
p, q = x / s, y / t
F0 = x.dot(x) / (2*s) + s*s/2
checks = []

def eq(name, actual, expected):
    if isinstance(actual, S.MatrixBase):
        residual = (actual-expected).applyfunc(S.simplify)
        assert residual == S.zeros(*actual.shape), (name, residual)
    else:
        residual = S.simplify(actual-expected)
        assert residual == 0, (name, residual)
    checks.append(name)
    print('PASS', name)

def at(expr, point):
    return expr.subs(dict(zip(x, point)), simultaneous=True)

def grad(expr):
    return S.Matrix([S.diff(expr, v) for v in x])

def div(expr, first, second):
    return S.simplify(at(expr, first)-at(expr, second)
                      -at(grad(expr), second).dot(first-second))

def brier(first, second):
    return (first-second).dot(first-second)/2

def risk(law, report):
    return S.simplify(sum(law[i]*brier(S.eye(2)[:, i], report)
                          for i in range(2)))

G0 = grad(F0)
H0 = S.hessian(F0, x)
eq('quadratic ambient gradient', G0, p + (s-p.dot(p)/2)*one)
eq('quadratic radial Hessian identity H p = 1', H0*p, one)
h = S.Matrix([h1, h2]); mass_h = sum(h); tangent_h = h-p*mass_h
eq('quadratic Hessian exact quadratic form', (h.T*H0*h)[0],
   tangent_h.dot(tangent_h)/s + mass_h**2)
eq('quadratic exact two-argument divergence', div(F0, x, y),
   s*brier(p, q) + (s-t)**2/2)
eq('quadratic forward KKT normal gradient difference',
   at(G0, p)-G0, (1-s)*one)

b = S.Matrix([Q(3,8), Q(1,8)])
p0 = S.Matrix([Q(3,4), Q(1,4)])
q_euclidean = S.Matrix([Q(5,8), Q(3,8)])
eq('concrete nonseparable Hessian', at(H0, b),
   S.Matrix([[Q(5,4),Q(1,4)],[Q(1,4),Q(13,4)]]))
assert at(H0[0,1],b) != 0
checks.append('mixed ambient Hessian entry is nonzero')
print('PASS mixed ambient Hessian entry is nonzero')
for i in range(2):
    ei = S.eye(2)[:, i]
    eq(f'coherent Brier equality for outcome {i+1}', div(F0,ei,p0), brier(ei,p0))
    eq(f'perspective statewise repair credit for outcome {i+1}',
       div(F0,ei,b)-div(F0,ei,p0),Q(1,8))
eq('null-channel Bayes implementation regret', brier(p0,p0),0)
eq('coherent prior expected Brier loss', risk(p0,p0),Q(3,16))
eq('old Euclidean-repair expected Brier loss', risk(p0,q_euclidean),Q(13,64))
eq('old Euclidean-repair null regret', risk(p0,q_euclidean)-risk(p0,p0),Q(1,64))
Fe = x.dot(x)/2
Fnew = x.dot(x)/(2*s)+(s-1)**2/2
eq('new and old ambient potentials agree on simplex',at(Fnew,p),at(Fe,p))
eq('new gauge differs affinely from baseline',Fnew-F0,-s+S.Rational(1,2))
eq('new gauge has identical baseline divergence',div(Fnew,x,y),div(F0,x,y))
eq('old Euclidean projection exact KKT',
   at(grad(Fe),q_euclidean)-at(grad(Fe),b),Q(1,4)*one)
assert q_euclidean != p0

# Nonquadratic coherent potential with strictly positive tangent Hessian:
# f(p)=||p||^2/2+(p1-p2)^4/4; a(s)=(s^2-1)/2.
f_nonquad = p.dot(p)/2 + (p[0]-p[1])**4/4
Fn = s*f_nonquad + (s*s-1)/2
Gn = grad(Fn); Hn = S.hessian(Fn,x)
eq('nonquadratic forward KKT normal gradient difference', at(Gn,p)-Gn,(1-s)*one)
eq('nonquadratic radial Hessian identity', Hn*p,one)
y0 = S.Matrix([Q(2,5),Q(3,5)])
b0 = S.Matrix([Q(3,8),Q(1,8)])
px, py = b0/sum(b0), y0/sum(y0)
f_intr = x.dot(x)/2+(x[0]-x[1])**4/4
eq('nonquadratic exact divergence split', div(Fn,b0,y0),
   sum(b0)*div(f_intr,px,py)+(sum(b0)-sum(y0))**2/2)
# Direct affine-simplex Hessian: d² f(z,1-z)/dz² = 2 + 12(2z-1)².
eq('nonquadratic positive tangent Hessian',
   S.diff(at(f_intr,S.Matrix([z,1-z])),z,2),2+12*(2*z-1)**2)

likelihoods = [S.Matrix([Q(4,5),Q(1,5)]),S.Matrix([Q(1,5),Q(4,5)])]
posteriors = [S.Matrix([Q(12,13),Q(1,13)]),S.Matrix([Q(3,7),Q(4,7)])]
masses = [Q(13,20),Q(7,20)]
post_risk = 0; information = 0; mean_posterior = S.zeros(2,1)
for i,(L,Qp,m) in enumerate(zip(likelihoods,posteriors,masses)):
    raw = p0.multiply_elementwise(L)
    eq(f'informative channel {i+1} outcome mass',sum(raw),m)
    eq(f'informative channel {i+1} exact posterior',raw/sum(raw),Qp)
    eq(f'informative channel {i+1} projection KKT',
       at(G0,Qp)-at(G0,raw),(1-m)*one)
    post_risk += m*risk(Qp,Qp)
    information += m*brier(Qp,p0)
    mean_posterior += m*Qp
eq('posterior barycenter equals prior',mean_posterior,p0)
eq('informative-channel expected posterior Brier loss',post_risk,Q(12,91))
eq('informative-channel learning gain',risk(p0,p0)-post_risk,Q(81,1456))
eq('informative-channel exact information identity',information,Q(81,1456))

# Global convex C3 bump: positive-part affine fourth power. At the selected
# active point it equals the polynomial below; at simplex/subprobability points
# it and its first derivative are zero. The universal sign argument is in RESULT.
u = 2*x1+x2-2
active_bump = u**4
bad_b = S.Matrix([Q(3,4),Q(3,4)])
bad_p = S.Matrix([Q(1,2),Q(1,2)])
eq('counterexample is strictly inside active halfspace',at(u,bad_b),Q(1,4))
eq('counterexample perturbation gradient',at(grad(active_bump),bad_b),
   S.Matrix([Q(1,8),Q(1,16)]))
eq('bump affine argument on simplex',at(u,S.Matrix([z,1-z])),z-1)
# At bad_p, u=-1/2, so the actual positive-part bump gradient is zero.
assert at(u,bad_p) < 0
residual = at(G0,bad_p)-at(G0,bad_b)-at(grad(active_bump),bad_b)
eq('forward normalization KKT fails with exact residual',residual[0]-residual[1],-Q(1,16))
assert residual[0] != residual[1]
bad_projection = S.Matrix([Q(17,32),Q(15,32)])
true_residual = at(G0,bad_projection)-at(G0,bad_b)-at(grad(active_bump),bad_b)
eq('counterexample actual forward projection exact KKT',true_residual[0]-true_residual[1],0)
assert bad_projection != bad_p and at(u,bad_projection) < 0
# Reverse objective changes by bump(b), a constant in the simplex argument.
r = S.Matrix([z,1-z])
reverse0 = div(F0,x,r)
eq('baseline reverse objective exact derivative',S.diff(reverse0,z),2*s*(z-p[0]))
eq('baseline reverse objective positive second derivative',S.diff(reverse0,z,2),2*s)
# For a rational whole null ray, u(cp)=c(1+p1)-2 <=0 when 0<c<=1.
c = S.symbols('c',positive=True)
eq('null-ray affine bump argument',at(u,c*p0),Q(7,4)*c-2)
for c0 in [Q(1,10),Q(1,2),Q(1)]:
    raw = c0*p0
    assert at(u,raw) < 0
    eq(f'attenuation counterexample agrees with normalization at c={c0}',
       at(G0,p0)-at(G0,raw),(1-c0)*one)

# Degenerate radial choices distinguish strict convexity from invertibility.
F_pure = x.dot(x)/(2*s)
eq('pure perspective Hessian has radial null vector',S.hessian(F_pure,x)*p,S.zeros(2,1))
F_degenerate = x.dot(x)/(2*s)+(s-1)**4
Hd = S.hessian(F_degenerate,x)
eq('strictly convex degenerate example radial Hessian',Hd*p,12*(s-1)**2*one)
eq('strictly convex degenerate example singular on simplex',at(Hd,p0).det(),0)
eq('degenerate radial endpoint divergence',div(F_degenerate,p0,b),Q(3,16))
error0 = S.symbols('error0',positive=True)
s_path_degenerate = 1+S.sqrt(error0**2-tau/6)
eq('degenerate flow reaches singular mass at finite time',
   S.simplify(s_path_degenerate.subs(tau,6*error0**2)),1)

# Exact quadratic global flow and statewise derivative, checked symbolically.
s0 = S.symbols('s0',positive=True)
mass_path = 1+(s0-1)*S.exp(-tau)
b_path = mass_path*p0
velocity = S.diff(b_path,tau)
eq('quadratic explicit radial flow satisfies vector field',
   velocity,-(mass_path-1)*at(H0,b_path).inv()*one)
for i in range(2):
    score_path = div(F0,S.eye(2)[:,i],b_path)
    eq(f'quadratic flow exact score derivative outcome {i+1}',
       S.diff(score_path,tau),-(mass_path-1)**2)
eq('quadratic flow initial mass',mass_path.subs(tau,0),s0)
eq('quadratic flow asymptotic normalized endpoint',S.limit(mass_path,tau,S.oo),1)
eq('quadratic integrated repair credit',
   S.integrate((mass_path-1)**2,(tau,0,S.oo)),(s0-1)**2/2)

print(f'\nALL {len(checks)} EXACT CONTROLS PASSED (SymPy {S.__version__})')
print('Finite controls and symbolic examples do not certify the general written theorem.')
