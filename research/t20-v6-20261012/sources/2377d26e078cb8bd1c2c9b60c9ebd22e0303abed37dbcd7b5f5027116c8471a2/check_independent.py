#!/usr/bin/env python3
"""Independent exact controls; no imports from the author implementation."""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json
import sympy as s

ROOT = Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--output-dir',type=Path)
args=parser.parse_args()
OUT=ROOT if args.output_dir is None else args.output_dir
if args.output_dir is not None:
    if OUT.exists():
        parser.error('explicit output directory must not already exist')
    OUT.mkdir(parents=True)
checks = []

def check(name, condition, detail=None):
    assert bool(condition), name
    checks.append({"name": name, "pass": True, "detail": detail})

def F(x):
    return x**4 / 4

def step(xs, ws, tau):
    assert tau > 0 and all(w > 0 for w in ws) and sum(ws) == 1
    M = max(map(abs, xs))
    assert M == 0 or tau <= 1 / (6 * M**2)
    ys = [x - tau*x**3 for x in xs]
    fs = list(map(F, ys))
    c = min(fs)
    raw = [w/(1+tau*(f-c)) for w, f in zip(ws, fs)]
    total = sum(raw)
    return ys, [v/total for v in raw]

def moment(xs, ws, k):
    return sum(w*x**k for x,w in zip(xs,ws))

def energy(xs, ws):
    return sum(w*F(x) for x,w in zip(xs,ws))

# 1. Symbolic three-dimensional Dirac covariance, arbitrary drift and step.
t = s.symbols('t', real=True)
x = s.Matrix(s.symbols('x0:3', real=True))
b = s.Matrix(s.symbols('b0:3', real=True))
m1 = x+t*b
m2 = x*x.T + t*(x*b.T+b*x.T)
check('dirac_covariance_symbolic_3d', s.simplify(m2-m1*m1.T+t*t*b*b.T)==s.zeros(3))

# 2. A positive-covariance two-atom raw Euler record with a negative square.
y = s.symbols('y')
xs, ws, tau = [s.Rational(-1),s.Rational(2)], [s.Rational(1,3),s.Rational(2,3)], s.Rational(1,100)
E = sum(w*F(v) for v,w in zip(xs,ws))
bs = [-v**3 for v in xs]
As = [1-tau*(F(v)-E) for v in xs]
def raw(poly):
    return s.expand(sum(w*(A*poly.subs(y,v)+tau*bb*s.diff(poly,y).subs(y,v))
                      for v,w,A,bb in zip(xs,ws,As,bs)))
j = 1
ell = (y-xs[0])/(xs[j]-xs[0])
C = (abs(As[j])+1)/(2*tau*bs[j]**2)
q = s.expand(ell**2*(1-(2*s.diff(ell,y).subs(y,xs[j])+C*bs[j])*(y-xs[j])))
check('hermite_values', [q.subs(y,v) for v in xs] == [0,1])
check('hermite_derivatives', [s.diff(q,y).subs(y,v) for v in xs] == [0,-C*bs[j]])
check('hermite_degree_budget', s.degree(q,y)<=3 and s.degree(q*q,y)<=6)
square_value = raw(q*q)
check('negative_square_beyond_covariance', square_value == ws[j]*(As[j]-abs(As[j])-1) and square_value<0,
      {"negative_square":str(square_value),"witness":str(q)})
cov = raw(y*y)-raw(y)**2
check('covariance_alone_misses_multiatom_failure', cov>0,{"covariance":str(cov)})

# Independent multivariate Hermite construction at three noncollinear nodes.
u,v=s.symbols('u v')
points=[(0,0),(1,0),(0,1)]; masses=[s.Rational(1,4),s.Rational(1,2),s.Rational(1,4)]
ell2=u+2*v; jj=2; separating=[ell2.subs({u:a,v:b}) for a,b in points]
card=s.prod((ell2-separating[k])/(separating[jj]-separating[k]) for k in range(3) if k!=jj)
bj=s.Matrix([2,-3]); C2=s.Rational(7,5)
gradcard=s.Matrix([s.diff(card,u),s.diff(card,v)]).subs({u:points[jj][0],v:points[jj][1]})
delta=s.Matrix([u-points[jj][0],v-points[jj][1]])
q2=s.expand(card**2*(1-(2*gradcard+C2*bj).dot(delta)))
for k,(aa,bb) in enumerate(points):
    vals={u:aa,v:bb}
    check(f'multivariate_hermite_value_{k}',q2.subs(vals)==int(k==jj))
    check(f'multivariate_hermite_gradient_{k}',s.Matrix([s.diff(q2,u),s.diff(q2,v)]).subs(vals)==(-C2*bj if k==jj else s.zeros(2,1)))
check('multivariate_hermite_degree',s.Poly(q2,u,v).total_degree()<=5)

# 3. Zero-drift raw Euler can work, and its large-step failure is weight loss.
g = (y*y-1)**2
zs = [s.Integer(0),s.Integer(1)]
check('stationary_support_for_selection_control', all(s.diff(g,y).subs(y,z)==0 for z in zs))
check('zero_drift_small_step_positive', all(1-s.Rational(1,2)*(g.subs(y,z)-s.Rational(1,2))>0 for z in zs))
check('zero_drift_large_step_negative_weight', 1-3*(g.subs(y,0)-s.Rational(1,2))<0)

# 4. Independent rational algorithm checks, including the exact bound endpoint.
samples = [([-2,-1,0,1,2],[Q(1,5)]*5),
           ([Q(-3,2),Q(1,3),Q(5,4)],[Q(1,6),Q(1,3),Q(1,2)]),
           ([0,0],[Q(1,4),Q(3,4)]),
           ([-1,-1,2],[Q(1,6),Q(1,3),Q(1,2)])]
for index,(xs0,ws0) in enumerate(samples):
    xs0=list(map(Q,xs0)); ws0=list(map(Q,ws0))
    M=max(map(abs,xs0)); tau0=Q(7) if M==0 else 1/(6*M*M)
    ys,vs=step(xs0,ws0,tau0)
    check(f'rational_state_{index}', all(isinstance(z,Q) for z in ys+vs))
    check(f'positive_normalized_{index}', all(v>0 for v in vs) and sum(vs)==1)
    check(f'interval_invariant_{index}', all(abs(z)<=M for z in ys))
    check(f'energy_descent_{index}',energy(ys,vs)<=energy(xs0,ws0))
    check(f'no_new_collisions_{index}',len(set(ys))==len(set(xs0)))
    if M>0:
        check(f'guard_strict_lipschitz_{index}',tau0*3*M*M==Q(1,2))
    for a in range(len(xs0)):
        for c in range(a+1,len(xs0)):
            check(f'pair_lower_bound_{index}_{a}_{c}',abs(ys[a]-ys[c])>=Q(1,2)*abs(xs0[a]-xs0[c]))
    for coefs in [[Q(1),Q(-2),Q(1)],[Q(-3),Q(2),Q(0),Q(4)]]:
        p2=sum(v*sum(c*z**k for k,c in enumerate(coefs))**2 for z,v in zip(ys,vs))
        mm=sum(a*b*moment(ys,vs,i+j) for i,a in enumerate(coefs) for j,b in enumerate(coefs))
        check(f'square_moment_{index}_{len(coefs)}',p2==mm and mm>=0)

# Repeat steps to check bounded support, positivity, strict descent, fixed rank.
xs0, ws0 = [Q(-2),Q(-1,3),Q(1),Q(3,2)], [Q(1,10),Q(1,5),Q(3,10),Q(2,5)]
tau0=Q(1,24)
for index in range(4):
    ys,vs=step(xs0,ws0,tau0)
    check(f'iterated_step_{index}',energy(ys,vs)<energy(xs0,ws0) and len(set(ys))==4 and sum(vs)==1)
    xs0,ws0=ys,vs

# Aggregation/splitting invariance, exact rational equality.
ys,vs=step([Q(-1),Q(-1),Q(2)],[Q(1,6),Q(1,3),Q(1,2)],Q(1,24))
merged_y,merged_v=step([Q(-1),Q(2)],[Q(1,2),Q(1,2)],Q(1,24))
check('duplicate_aggregation_invariance',ys[0]==ys[1]==merged_y[0] and ys[2]==merged_y[1] and vs[0]+vs[1]==merged_v[0] and vs[2]==merged_v[1])
check('duplicate_internal_ratio_preserved',vs[0]/vs[1]==Q(1,2))

# 5. Necessity of step/domain restrictions, not a blanket Euler prohibition.
check('unguarded_quartic_collision',Q(1)-Q(1)*Q(1)**3==0)
check('unguarded_quartic_energy_increase',F(Q(1)-Q(3)*Q(1)**3)>F(Q(1)))
check('wrong_quartic_normalization_breaks_guard',Q(1)-4*Q(1,7)==Q(1,2)-4*Q(1,7)*Q(1,2)**3 and Q(1,7)<Q(1,6))
check('quadratic_tauL_one_collapses',s.expand(y-s.diff(y*y/2,y))==0)
check('quadratic_tauL_two_not_strict_descent',s.expand((y-2*s.diff(y*y/2,y))**2-y*y)==0)
xa,xb=Q(1),Q(21,20)
ta,tb=Q(1,12),Q(3200,27783)
check('different_guarded_unrecorded_steps_not_injective',
      ta<=1/(6*xa*xa) and tb<=1/(6*xb*xb) and xa-ta*xa**3==xb-tb*xb**3==Q(11,12),
      {"inputs":[str(xa),str(xb)],"steps":[str(ta),str(tb)],"same_output":"11/12"})

# A continuous stationary state is a fixed split-step state, not a minimum.
nonconvex=(u*u-1)**2+(v*v-1)**2
fixed_nodes=[{u:0,v:1},{u:0,v:-1}]
check('stationary_nonminimum_zero_gradients',all(s.diff(nonconvex,z).subs(pt)==0 for pt in fixed_nodes for z in [u,v]))
check('stationary_nonminimum_equal_energies',all(nonconvex.subs(pt)==1 for pt in fixed_nodes))
check('stationary_nonminimum_nearby_lower_energy',nonconvex.subs({u:s.Rational(1,2),v:1})==s.Rational(9,16)<1)

# 6. First-order rational consistency; c may be any common offset.
a,c,f0,f1,g0,g1=s.symbols('a c f0 f1 g0 g1')
f0t=f0+t*g0; f1t=f1+t*g1
r0=a/(1+t*(f0t-c)); r1=(1-a)/(1+t*(f1t-c))
v0=r0/(r0+r1)
target=-a*(f0-(a*f0+(1-a)*f1))
check('weight_first_order_offset_cancels',s.simplify(s.diff(v0,t).subs(t,0)-target)==0)

# Whole-step derivative on polynomial moments for a three-atom rational input.
cx=[s.Rational(-1),s.Integer(0),s.Integer(2)]; cw=[s.Rational(1,4),s.Rational(1,2),s.Rational(1,4)]
cy=[z-t*z**3 for z in cx]; cf=[F(z) for z in cy]
cr=[w/(1+t*f) for w,f in zip(cw,cf)]; cz=sum(cr)
ce=sum(w*F(z) for z,w in zip(cx,cw))
for n in range(7):
    rebuilt=sum(w*z**n for w,z in zip(cr,cy))/cz
    expected=sum(w*(-(n*z**(n+2) if n else 0)-(F(z)-ce)*z**n) for z,w in zip(cx,cw))
    check(f'whole_step_first_order_moment_{n}',s.simplify(s.diff(rebuilt,t).subs(t,0)-expected)==0)
# Actual tied energies at x=0,1 for F=x^4-x^3; minimum switches at t=0.
ft=(1-t)**4-(1-t)**3
for label,ct in [('left_branch',s.Integer(0)),('right_branch',ft)]:
    z0=a/(1-t*ct); z1=(1-a)/(1+t*(ft-ct))
    vt=z0/(z0+z1)
    check('nondifferentiable_min_'+label,s.simplify(s.diff(vt,t).subs(t,0))==0)

# 7. Covariance identity proves monotone rational reweighting.
w0=s.symbols('w0')
f0,f1,c,t=s.symbols('f0 f1 c t')
h0=1/(1+t*(f0-c)); h1=1/(1+t*(f1-c)); Z=w0*h0+(1-w0)*h1
change=(w0*h0*f0+(1-w0)*h1*f1)/Z-(w0*f0+(1-w0)*f1)
pair=w0*(1-w0)*(h0-h1)*(f0-f1)/Z
check('reweighting_covariance_identity',s.factor(change-pair)==0)
check('rational_factor_difference',s.factor(h0-h1+t*(f0-f1)/((1+t*(f0-c))*(1+t*(f1-c))))==0)

report={"scope":"Independent exact controls, not universal-proof enumeration or formal-kernel verification", "pass":True,"count":len(checks),"checks":checks,"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'INDEPENDENT_EXACT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({"pass":True,"count":len(checks),"negative_square":str(square_value),"positive_covariance":str(cov)},indent=2))
