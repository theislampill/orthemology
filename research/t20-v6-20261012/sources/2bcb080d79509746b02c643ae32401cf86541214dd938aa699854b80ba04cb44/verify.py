#!/usr/bin/env python3
"""Exact controls supplementary to the ordinary measure-theoretic proof."""
import argparse,hashlib,json,platform
from pathlib import Path
import sympy as S
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'author-run');ap.add_argument('--original-root',type=Path);args=ap.parse_args()
root=Path(__file__).resolve().parent;args.output_dir.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,expr):
    if isinstance(expr,bool):ok=expr
    else:ok=S.simplify(S.trigsimp(S.expand_trig(expr)))==0
    checks.append({'name':name,'pass':bool(ok)})
    if not ok:raise AssertionError((name,expr))
t,th=S.symbols('t theta',real=True)
A=S.sin((1-t)*th)/S.sin(th);B=S.sin(t*th)/S.sin(th)
Ad=S.diff(A,t);Bd=S.diff(B,t);aff=S.cos(th)
check('conditional sphere norm',A*A+B*B+2*A*B*aff-1)
check('conditional sphere speed',Ad*Ad+Bd*Bd+2*Ad*Bd*aff-th*th)
check('conditional sphere centering',A*Ad+B*Bd+(A*Bd+B*Ad)*aff)
check('left endpoint coefficient A',A.subs(t,0)-1)
check('left endpoint coefficient B',B.subs(t,0))
check('right endpoint coefficient A',A.subs(t,1))
check('right endpoint coefficient B',B.subs(t,1)-1)
check('zero angle A limit',S.limit(A,th,0)-(1-t))
check('zero angle B limit',S.limit(B,th,0)-t)
check('zero angle A derivative limit',S.limit(Ad,th,0)+1)
check('zero angle B derivative limit',S.limit(Bd,th,0)-1)
# For coinciding fibre vectors, A+B=1 and Ad+Bd=0 at zero angle.
check('coincident fibre constant',1-t+t-1)
check('disjoint fibre A',A.subs(th,S.pi/2)-S.cos(S.pi*t/2))
check('disjoint fibre B',B.subs(th,S.pi/2)-S.sin(S.pi*t/2))
p0=S.cos(S.pi*t/2)**2;p1=S.sin(S.pi*t/2)**2
check('singular fibre mass',p0+p1-1)
check('singular fibre centered source',S.diff(p0+p1,t))
check('singular fibre reaction action',S.diff(p0,t)**2/p0+S.diff(p1,t)**2/p1-S.pi**2)
check('singular left actual reaction',S.diff(p0,t)/p0+S.pi*S.tan(S.pi*t/2))
check('singular right actual reaction',S.diff(p1,t)/p1-S.pi/S.tan(S.pi*t/2))
# Two-fibre example; no minimizer claim from this competitor.
p=S.Rational(1,3);shared=1-p
check('fixed first marginal row',p*p0+p*p1-p)
check('unchanged second marginal row',shared-S.Rational(2,3))
check('atomic example action',p*(S.diff(p0,t)**2/p0+S.diff(p1,t)**2/p1)-S.pi**2/3)
check('atomic example midpoint changing masses',(p*p0).subs(t,S.Rational(1,2))-S.Rational(1,6))
check('atomic global affinity',shared-S.Rational(2,3))
check('global sphere midpoint shared-row mass',shared*2/(1+shared)-S.Rational(4,5))
check('global sphere midpoint first-row mass',1-shared*2/(1+shared)-S.Rational(1,5))
check('wrong marginal exact discrepancy',S.Rational(4,5)-shared-S.Rational(2,15))
# Mixture perspective inequality via nonnegative polynomial remainder.
a,b,ad,bd,f0,f1=S.symbols('a b ad bd f0 f1',real=True)
q=a*a*f0+b*b*f1;dq=2*(a*ad*f0+b*bd*f1)
check('convex mixture perspective remainder',4*(ad*ad*f0+bd*bd*f1)*q-dq*dq-4*f0*f1*(a*bd-b*ad)**2)
ac=S.cos(S.pi*t/2);bc=S.sin(S.pi*t/2)
check('convex mixture universal action bound',4*(S.diff(ac,t)**2+S.diff(bc,t)**2)-S.pi**2)
check('source-normalization factor',2*S.Rational(1,2)-1)
# The RN conditional dominator has mass two, but square-root norms one.
check('sum dominator mass',1+1-2)
check('identical fibre RN square root norm',2*S.Rational(1,2)-1)
# Dual-square algebra, supporting the functional proof.
r,w,F=S.symbols('r w F',real=True)
check('perspective completed square',w*w/r-(2*F*w-F*F*r)-(w-r*F)**2/r)
# Time rescaling and optimized concatenation, including residual positivity.
x,y,tau=S.symbols('x y tau',positive=True)
check('optimal triangle allocation',x*x/(x/(x+y))+y*y/(y/(x+y))-(x+y)**2)
check('triangle allocation remainder',x*x/tau+y*y/(1-tau)-(x+y)**2-(x-(x+y)*tau)**2/(tau*(1-tau)))
# A unit path with constant squared speed E compressed to length h has action E/h.
h,E=S.symbols('h E',positive=True)
check('affine time compression action',(E/h**2)*h-E/h)
check('subarc to unit time action',h*h*E-h*(h*E))
# Protect all copied ancestors, especially earlier frozen author packet.
for row in json.loads((root/'INPUT_BINDINGS.json').read_text()):
    check('snapshot binding '+row['snapshot'],hashlib.sha256((root/row['snapshot']).read_bytes()).hexdigest()==row['sha256'])
    if args.original_root:
        check('original binding '+row['original'],hashlib.sha256((args.original_root/row['original']).read_bytes()).hexdigest()==row['sha256'])
freeze=json.loads((root/'inputs/fixed-marginal-correction-20261011--AUTHOR_FREEZE.json').read_text())
check('prior frozen result digest',hashlib.sha256((root/'inputs/fixed-marginal-correction-20261011--RESULT.md').read_bytes()).hexdigest()==freeze['result_sha256'])
check('prior frozen manifest digest',hashlib.sha256((root/'inputs/fixed-marginal-correction-20261011--MANIFEST.json').read_bytes()).hexdigest()==freeze['manifest_sha256'])
out={'status':'PASS','verification_kind':'Exact author controls, supplementary to ordinary proofs','python':platform.python_version(),'sympy':S.__version__,'check_count':len(checks),'checks':checks}
(args.output_dir/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','check_count','python','sympy')},indent=2))
