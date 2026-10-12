#!/usr/bin/env python3
"""Independent exact symbolic controls; finite examples are not the general proof."""
import json
import sympy as S

checks = []
def check(name, condition):
    ok = bool(condition)
    checks.append({'name': name, 'pass': ok})
    if not ok:
        raise AssertionError(name)

def zero(x):
    return S.simplify(x) == 0

x, y, s, t = S.symbols('x y s t', positive=True)
p, q = S.symbols('p q', real=True)
h1, h2 = S.symbols('h1 h2', real=True)
b = S.Matrix([x, y]); mass=x+y
F=(x*x+y*y)/(2*mass)+mass*mass/2
grad=S.Matrix([S.diff(F,v) for v in (x,y)])
H=S.hessian(F,(x,y))
pv=S.Matrix([p,1-p]); qv=S.Matrix([q,1-q])
sub_sp={x:s*p,y:s*(1-p)}; sub_tq={x:t*q,y:t*(1-q)}
div=F.subs(sub_sp, simultaneous=True)-F.subs(sub_tq, simultaneous=True)-(grad.subs(sub_tq, simultaneous=True).dot(s*pv-t*qv))
check('quadratic divergence split', zero(div-(s*(p-q)**2+(s-t)**2/2)))
check('quadratic canonical a(1)=0', zero(((s*s-s)/2).subs(s,1)))
check('quadratic radial Hessian', all(zero(v) for v in H*b/mass-S.ones(2,1)))
check('quadratic inverse-Hessian radial vector', all(zero(v) for v in H.inv()*S.ones(2,1)-b/mass))
check('quadratic determinant', zero(H.det()-2/mass))
check('quadratic H11 positive formula', zero(H[0,0]-(1+2*y*y/mass**3)))
check('quadratic genuinely nonseparable witness', H[0,1].subs({x:1,y:1}) != 0)

hv=S.Matrix([h1,h2]); sigma=h1+h2; tang=hv-pv*sigma
quad=(hv.T*H.subs(sub_sp,simultaneous=True)*hv)[0]
check('quadratic Hessian quadratic form', zero(quad-tang.dot(tang)/s-sigma*sigma))

losses=[]
field=-(mass-1)*(b/mass)
for ei in (S.Matrix([1,0]),S.Matrix([0,1])):
    Di=S.Rational(1)-F-grad.dot(ei-b)
    dDi=sum(S.diff(Di,v)*field[j] for j,v in enumerate((x,y)))
    check('truth-state derivative '+str(tuple(ei)), zero(dDi+(mass-1)**2))
    Di_sp=Di.subs(sub_sp,simultaneous=True)
    Di_p=Di.subs({x:p,y:1-p},simultaneous=True)
    check('truth-state repair gain '+str(tuple(ei)),zero(Di_sp-Di_p-(s-1)**2/2))
    losses.append(str(S.factor(Di)))

Fdeg=(x*x+y*y)/(2*mass)+(mass-1)**4
Hdeg=S.hessian(Fdeg,(x,y))
check('strict-convex countercontrol radial singularity', zero(Hdeg.det().subs({x:p,y:1-p},simultaneous=True)))
check('strict-convex countercontrol radial kernel', all(zero(v) for v in Hdeg.subs({x:p,y:1-p},simultaneous=True)*pv))
check('strict-convex countercontrol nonzero tangent curvature', zero((S.Matrix([1,-1]).T*Hdeg.subs({x:p,y:1-p},simultaneous=True)*S.Matrix([1,-1]))[0]-2))

# Normalization does not characterize arbitrary convex potentials.
# Euclidean F(b)=||b||^2/2 projects b=(3/5,7/10) onto the interior simplex
# by subtracting 3/20 from both coordinates, not by normalizing.
euclid_b=S.Matrix([S.Rational(3,5),S.Rational(7,10)])
euclid_projection=euclid_b-S.ones(2,1)*(sum(euclid_b)-1)/2
normalize=euclid_b/sum(euclid_b)
check('negative control Euclidean projection differs from normalization', euclid_projection != normalize)
check('negative control projection remains interior', all(v>0 for v in euclid_projection))
check('negative control Euclidean objective is smaller at actual projection', (euclid_projection-euclid_b).dot(euclid_projection-euclid_b)<(normalize-euclid_b).dot(normalize-euclid_b))

# Box-compatible restricted-neutrality and orientation counterexample.
z=x+y/S.Integer(2)-1
bump_active=z**4
bump_grad=S.Matrix([S.diff(bump_active,v) for v in (x,y)])
witness={x:S.Rational(9,10),y:S.Rational(4,5)}
check('box bump witness is active', z.subs(witness)>0)
residual=-(bump_grad[0]-bump_grad[1]).subs(witness)
check('box bump forward normalization stationarity fails',residual==-S.Rational(27,500))
pstar=S.Matrix([S.Rational(9,17)+S.Rational(27,1000),S.Rational(8,17)-S.Rational(27,1000)])
check('box bump true minimizer interior',all(v>0 for v in pstar) and sum(pstar)==1)
full_grad_at_b=(grad+bump_grad).subs(witness)
check('box bump true minimizer stationary',zero((pstar[0]-pstar[1])-(full_grad_at_b[0]-full_grad_at_b[1])))
check('box bump differs from normalization',pstar!=S.Matrix([S.Rational(9,17),S.Rational(8,17)]))
# On Delta, z=(p-1)/2<0 for 0<p<1, so the positive-part bump
# and every derivative relevant to the Bregman expression vanish.
check('simplex bump argument exactly negative',zero(z.subs({x:p,y:1-p},simultaneous=True)-(p-1)/2))
# For b=c*p, c<=1, z=c*(1+p)/2-1<0. This symbolic identity
# supplies the algebra; the inequality follows from 0<p<1 and 0<c<=1.
check('restricted-neutrality bump argument identity',zero(z.subs(sub_sp,simultaneous=True)-(s*(1+p)/2-1)))

# Coordinate-free trace-positive symmetric-matrix example.
w=S.symbols('w', real=True)
Mcoords=S.Matrix([x,y,w])
Fmatrix=(x*x+y*y+2*w*w)/(2*mass)+mass*mass/2
Hmatrix=S.hessian(Fmatrix,(x,y,w))
ell=S.Matrix([1,1,0])
check('matrix trace radial Hessian identity',all(zero(v) for v in Hmatrix*Mcoords/mass-ell))
check('matrix trace inverse-Hessian radial identity',all(zero(v) for v in Hmatrix.inv()*ell-Mcoords/mass))
check('matrix trace Hessian positive at SPD witness',all(v>0 for v in [Hmatrix[:i,:i].det().subs({x:2,y:3,w:S.Rational(1,2)}) for i in (1,2,3)]))

report={'status':'PASS','checks':checks,'check_count':len(checks),
        'symbolic_engine':'sympy '+S.__version__, 'example_losses':losses,
        'limitations':'Exact finite-dimensional example controls; the general theorem is proved in INDEPENDENT_ANALYSIS.md.'}
print(json.dumps(report,indent=2))
