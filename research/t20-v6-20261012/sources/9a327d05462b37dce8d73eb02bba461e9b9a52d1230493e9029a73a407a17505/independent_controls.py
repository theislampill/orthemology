from fractions import Fraction as Q
from pathlib import Path
import importlib.util,sys,json
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'received-authorial-synthesis-20261011/extracted/Orthemology_T20_111min_Recovered_Authored_Work_20261010'
sys.path.insert(0,str(p))
from research.contracts import tilt,replicator,audit_tangent,rational_weight_step
spec=importlib.util.spec_from_file_location('inherited', ROOT/'gradient-discretization-fidelity-20261010/check_exact.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
results={}
# Use actual inherited implementation, preserving origin labels by distinct positions.
w=[Q(1,3),Q(2,3)]; x=[Q(-1),Q(2)]; r={0:Q(2),1:Q(1,3)}; h=Q(1,24)
def B(w):return list(tilt(dict(enumerate(w)),r).values())
a=m.quartic_rational_step(w,x,h); b=m.quartic_rational_step(B(w),x,h)
assert a['positions_after']==b['positions_after']
assert B(a['weights_after'])==b['weights_after']
results['actual_inherited_quartic_commutation']={'positions':a['positions_after'],'weights_both_orders':b['weights_after']}
# n=1: identity action, identically zero weight field, unchanged rational weight.
one={0:Q(1)}
assert replicator(one,{0:Q(7)})=={0:0}
assert audit_tangent(one,{0:Q(9)},{0:0})=={0:0}
assert rational_weight_step(one,{0:Q(-4)},Q(12))==one
results['n1']='PASS'
# Full-audit covariance is stronger than nonlinear target-only quotient descent.
w={0:Q(1,2),1:Q(1,2)}; r={0:Q(1),1:Q(2)}
def nonlinear(w):return replicator(w,{0:-2*w[0],1:0})
left=audit_tangent(w,r,nonlinear(w));right=nonlinear(tilt(w,r))
assert left[0]==Q(-2,9) and right[0]==Q(-4,27)
results['nonlinear_fixed_objective_does_not_commute']={'pushed_field':left,'field_at_audited':right}
# Adaptive weight-dependent step destroys otherwise positive descending repair.
V={0:Q(1),1:Q(0)}
def adaptive(w):return rational_weight_step(w,V,w[0])
left=tilt(adaptive(w),r);right=adaptive(tilt(w,r))
assert left!=right
results['weight_dependent_step_countercontrol']={'step_then_audit':left,'audit_then_step':right}
# Alpha scale: use alpha*h to recover the stated metric's weight velocity.
import sympy as S
h,a,p=S.symbols('h a p', positive=True)
f0=1/(1+a*h);z=p*f0+(1-p);out=p*f0/z
assert S.simplify(S.diff(out,h).subs(h,0)+a*p*(1-p))==0
results['alpha_rescaling']='PASS: denominator 1+alpha*h*(V_i-min V)'
print(json.dumps(results,indent=2,default=str))
