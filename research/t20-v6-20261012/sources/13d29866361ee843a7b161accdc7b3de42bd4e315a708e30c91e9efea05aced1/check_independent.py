"""Separate exact controls; replay writes only inside this independent review."""
from pathlib import Path
import ast, hashlib, json, subprocess, sys
import sympy as s
ROOT=Path(__file__).resolve().parent
AUTHOR=ROOT.parent/'moving-objective-order-interface-20261010'
checks=[]
def check(name,condition,category='mathematical'):
    if condition is not True and condition != s.true: raise AssertionError((name,condition))
    checks.append({'name':name,'category':category,'status':'PASS'})
def eq(name,value):check(name,s.simplify(s.expand(value))==0)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
expected=json.loads((ROOT/'FROZEN_AUTHOR_INPUTS.json').read_text())
for name,h in expected.items():
    check('author_current_hash_'+name,digest(AUTHOR/name)==h,'author_hash')
    check('author_snapshot_hash_'+name,digest(ROOT/'inputs'/name)==h,'snapshot_hash')
for rel,h in json.loads((ROOT/'inputs'/'INPUT_BINDINGS.json').read_text()).items():
    check('bound_predecessor_copy_'+rel,digest(ROOT/'predecessors'/rel)==h,'ancestor_hash')
proc=subprocess.run([sys.executable,str(ROOT/'inputs'/'check.py')],capture_output=True,text=True)
(ROOT/'AUTHOR_REPLAY.log').write_text(proc.stdout+proc.stderr)
check('author_replay_exit_zero',proc.returncode==0,'execution')
replayed=json.loads(proc.stdout)
check('author_replay_results_match_frozen',digest(ROOT/'inputs'/'CHECK_RESULTS.json')==expected['CHECK_RESULTS.json'],'execution')
tree=ast.parse((ROOT/'inputs'/'check.py').read_text())
calls=[node for node in tree.body if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call)
       and isinstance(node.value.func,ast.Name) and node.value.func.id=='check']
check('author_has_seven_executed_distinct_named_controls',len(calls)==7 and replayed['count']==7 and len(set(replayed['checks']))==7,'count_audit')

x,y,z,t,a,q=s.symbols('x y z t a q',real=True)
coords=(x,y,z)
p=s.Function('p')(*coords);F=s.Function('F')(*coords);G=s.Function('G')(*coords)
def B(f,v):return -sum(s.diff(f,u)*s.diff(v,u) for u in coords)-f*v
C=sum(sum(s.diff(G,u,v)*s.diff(F,v)-s.diff(F,u,v)*s.diff(G,v) for v in coords)*s.diff(p,u) for u in coords)
eq('arbitrary_three_dimensional_gradient_commutator',B(F,B(G,p))-B(G,B(F,p))-C)
eq('three_dimensional_commutator_annihilates_one',B(F,B(G,s.Integer(1)))-B(G,B(F,s.Integer(1))))
eq('observable_order_reversal_changes_bracket_sign',B(G,B(F,p))-B(F,B(G,p))+C)
c,d=s.symbols('c d')
eq('constant_energy_gauge_leaves_commutator_unchanged',B(F+c,B(G+d,p))-B(G+d,B(F+c,p))-C)
eq('pure_multiplication_commutes',(-F)*((-G)*p)-(-G)*((-F)*p))

# Independently chosen velocity/killing fields have the usual nonzero scalar bracket.
u=s.Function('u')(x);v=s.Function('v')(x);h=s.Function('h')(x);k=s.Function('k')(x);f=s.Function('f')(x)
U=lambda w:u*s.diff(w,x)-h*w
V=lambda w:v*s.diff(w,x)-k*w
expected_generic=(u*s.diff(v,x)-v*s.diff(u,x))*s.diff(f,x)+(-u*s.diff(k,x)+v*s.diff(h,x))*f
eq('general_drift_killing_commutator_formula',U(V(f))-V(U(f))-expected_generic)
BF=lambda w:-x*s.diff(w,x)-x*x*w/2
C1=lambda w:a*s.diff(w,x)
eq('higher_commutator_transport_and_reaction',BF(C1(f))-C1(BF(f))-a*s.diff(f,x)-a*x*f)
eq('higher_commutator_does_not_annihilate_one',BF(C1(s.Integer(1)))-C1(BF(s.Integer(1)))-a*x)

# Intermediate projective normalization cancels even when second-stage factors differ.
m1,m2,u1,u2,v1,v2,p1,p2=s.symbols('m1 m2 u1 u2 v1 v2 p1 p2',positive=True)
Z=m1*u1+m2*u2
sequential=((m1*u1/Z)*v1*p1+(m2*u2/Z)*v2*p2)/((m1*u1/Z)*v1+(m2*u2/Z)*v2)
one=((m1*u1)*v1*p1+(m2*u2)*v2*p2)/((m1*u1)*v1+(m2*u2)*v2)
eq('intermediate_projective_normalization_cancels',sequential-one)
n0,n1,n2,n3,j,d1,d2,d3,e3=s.symbols('n0 n1 n2 n3 j d1 d2 d3 e3')
A=(n0+t*n1+t*t*(n2+j)+t**3*n3)/(1+t*d1+t*t*d2+t**3*d3)
D=(n0+t*n1+t*t*n2)/(1+t*d1+t*t*d2+t**3*e3)
eq('unequal_third_order_denominators_leave_second_coefficient',s.diff(A-D,t,2).subs(t,0)/2-j)

ff=lambda w:q*w
gg=lambda w:q*w+a*(1-q)
eq('physical_F_then_G_observable_composition',gg(ff(z))-(q*q*z+a*(1-q)))
eq('physical_G_then_F_observable_composition',ff(gg(z))-(q*q*z+a*q*(1-q)))
eq('physical_order_sign_exact',gg(ff(z))-ff(gg(z))-a*(1-q)**2)
eq('physical_order_second_time_coefficient',s.limit((gg(ff(z))-ff(gg(z))).subs(q,s.exp(-t))/t**2,t,0)-a)

# Exact integrated killing for the same global shifted-quadratic flows.
KF=lambda w:(1-q*q)*w*w/4
KG=lambda w:(1-q*q)*(w-a)**2/4
KFG=lambda w:KF(w)+KG(ff(w))
KGF=lambda w:KG(w)+KF(gg(w))
eq('single_stage_quadratic_integrated_killing',s.integrate(z*z*s.exp(-2*t)/2,(t,0,s.symbols('T',positive=True)))-(1-s.exp(-2*s.symbols('T',positive=True)))*z*z/4)
eq('exact_protocol_killing_difference',KFG(z)-KGF(z)+a*(2*z-a)*(q-1)**3*(q+1)/4)
eq('first_nonzero_killing_difference_third_order',s.limit((KFG(z)-KGF(z)).subs(q,s.exp(-t))/t**3,t,0)-a*(2*z-a)/2)

# A genuine compact two-atom law includes nontrivial normalization and reweighting.
# a=1, mu=(delta_0+2 delta_2)/3, observable p(x)=x^2.
weights=[s.Rational(1,3),s.Rational(2,3)]
points=[0,2]
kfg=[KFG(w).subs(a,1) for w in points]
kgf=[KGF(w).subs(a,1) for w in points]
zfg=[gg(ff(w)).subs(a,1) for w in points]
zgf=[ff(gg(w)).subs(a,1) for w in points]
Dfg=sum(m*s.exp(-k) for m,k in zip(weights,kfg))
Dgf=sum(m*s.exp(-k) for m,k in zip(weights,kgf))
Nfg=sum(m*s.exp(-k)*w*w for m,k,w in zip(weights,kfg,zfg))
Ngf=sum(m*s.exp(-k)*w*w for m,k,w in zip(weights,kgf,zgf))
check('actual_protocol_masses_match_through_second_order',all(s.simplify(s.diff(Dfg-Dgf,q,n).subs(q,1))==0 for n in range(3)))
eq('actual_two_atom_normalized_observable_bracket',s.diff(Nfg/Dfg-Ngf/Dgf,q,2).subs(q,1)/2-s.Rational(8,3))
Pfg=weights[1]*s.exp(-kfg[1])/Dfg
Pgf=weights[1]*s.exp(-kgf[1])/Dgf
check('actual_label_weights_match_through_second_order',all(s.simplify(s.diff(Pfg-Pgf,q,n).subs(q,1))==0 for n in range(3)))
# q-1=-t+O(t^2), so the cubic q-coefficient reverses sign in t.
eq('actual_label_reweighting_returns_at_third_order',-s.diff(Pfg-Pgf,q,3).subs(q,1)/6+s.Rational(4,9))

out={'status':'PASS','total':len(checks),
     'counts':{cat:sum(c['category']==cat for c in checks) for cat in sorted({c['category'] for c in checks})},
     'checks':checks,'scope':'Independent exact controls and hash checks complement the written proof; no kernel or empirical validation.'}
(ROOT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
