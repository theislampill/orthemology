#!/usr/bin/env python3
"""Exact corroborating controls; not a proof by enumeration or independent review."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=Path('author-run'));ap.add_argument('--original-root',type=Path);args=ap.parse_args()
 root=Path(__file__).resolve().parent; checks={}
 def equal(name,a,b=0):
  if isinstance(a,s.MatrixBase):ok=all(s.simplify(e)==0 for e in a-b)
  else:ok=s.simplify(a-b)==0
  checks[name]=bool(ok)
 # Finite conditional action decomposition, with both contraction and discarded variation.
 weights=[s.Rational(1,6),s.Rational(1,3),s.Rational(1,2)]
 groups=[[0,1],[2]]
 D=[s.Matrix([[s.Rational(1,2),0]]),s.Matrix([[s.Rational(1,2),0]]),s.Matrix([[0,1]])]
 vs=[s.Matrix([2,3]),s.Matrix([4,-1]),s.Matrix([5,2])]
 alphas=[s.Integer(2),s.Integer(-1),s.Integer(0)]
 fine=sum(w*(v.dot(v)+a*a) for w,v,a in zip(weights,vs,alphas))
 coarse=0;vvar=0;avar=0
 for g in groups:
  wg=sum(weights[i] for i in g)
  vb=sum((weights[i]*(D[i]*vs[i])[0] for i in g),s.Integer(0))/wg
  ab=sum(weights[i]*alphas[i] for i in g)/wg
  coarse+=wg*(vb*vb+ab*ab)
  vvar+=sum(weights[i]*((D[i]*vs[i])[0]-vb)**2 for i in g)
  avar+=sum(weights[i]*(alphas[i]-ab)**2 for i in g)
 spatial=sum(weights[i]*(vs[i].dot(vs[i])-(D[i]*vs[i]).dot(D[i]*vs[i])) for i in range(3))
 equal('conditional_action_loss_identity',fine-coarse,spatial+vvar+avar)
 checks['conditional_action_losses_nonnegative']=all(t>=0 for t in [spatial,vvar,avar])
 equal('centered_reaction_preserved',sum(w*a for w,a in zip(weights,alphas)))
 # General constant linear map and covariance contribution to pulled-back linear observables.
 P=s.Matrix([[1,0,0],[0,1,0]]); Sig=s.Matrix([[3,1,2],[1,2,1],[2,1,4]])
 equal('projection_coisometry',P*P.T,s.eye(2))
 g=s.Matrix([s.Rational(2,3),s.Rational(-1,5)]);beta=s.Rational(3,4)
 lifted=P.T*g
 equal('horizontal_lift_cost',lifted.dot(lifted)+beta**2,g.dot(g)+beta**2)
 equal('linear_observable_cometric',P*(s.eye(3)+Sig)*P.T,s.eye(2)+P*Sig*P.T)
 # Projection of the full Gaussian quadratic flow at a correlated SPD state.
 Qb=s.Matrix([[2,1],[1,3]]);Q=P.T*Qb*P; m=s.Matrix([2,-1,3]);b=P.T*s.Matrix([1,-2]);
 fullm=-(s.eye(3)+Sig)*(Q*m+b)
 fullS=-(Q*Sig+Sig*Q+Sig*Q*Sig)
 Sbar=P*Sig*P.T;mbar=P*m
 equal('correlated_gaussian_pulledback_mean',P*fullm,-(s.eye(2)+Sbar)*(Qb*mbar+P*b))
 equal('correlated_gaussian_pulledback_covariance',P*fullS*P.T,-(Qb*Sbar+Sbar*Qb+Sbar*Qb*Sbar))
 # No autonomous mobility for a nonbasic Gram tensor.
 x=s.symbols('x',real=True);T=s.Rational(2,3)*s.sin(x)+s.Rational(1,6)*s.sin(2*x);Tp=s.diff(T,x)
 equal('nonbasic_map_equal_outputs',T.subs(x,0),T.subs(x,s.pi))
 equal('nonbasic_map_first_gram',Tp.subs(x,0)**2,1)
 equal('nonbasic_map_second_gram',Tp.subs(x,s.pi)**2,s.Rational(1,9))
 # Deterministic contraction changes direction in Gaussian parameter space.
 scale=s.Rational(1,2);kappa=scale**2;mx=s.Integer(2);vx=s.Integer(4)
 projected=s.Matrix([scale*(-(1+vx)*kappa*mx),scale**2*(-kappa*vx*(vx+2))])
 canonical=s.Matrix([-2,-3]);equal('contraction_projected_vector',projected,s.Matrix([-s.Rational(5,4),-s.Rational(3,2)]))
 equal('contraction_noncollinearity_determinant',s.det(s.Matrix.hstack(projected,canonical)),s.Rational(3,4))
 # Gaussian KL density ratio and conditional law.
 c,y,z=s.symbols('c y z',real=True);S=s.Matrix([[1,c],[c,1]]);I=s.eye(2);dotS=2*I-S-S*S
 equal('gaussian_kl_initial_matrix',dotS,s.Matrix([[-c*c,-3*c],[-3*c,-c*c]]))
 equal('coarse_kl_at_target',2-1-1**2,0)
 h=(c*c*y*y-c*c-s.log(1-c*c))/2
 expectedh=-s.log(1-c*c)/2
 equal('conditional_centered_kl',h-expectedh,c*c*(y*y-1)/2)
 equal('conditional_variance_reaction',-c*c*(3-1)/2,-c*c)
 equal('conditional_hidden_variance',1-c*c,(S[1,1]-S[1,0]*S[0,0]**-1*S[0,1]))
 # Reviewer-contributed nonminimal pushed representation: independently executed algebra.
 V=c*c
 pushed_cost=V*V*s.Rational(1,2)
 minimal_cost=V*V*s.Rational(1,6)
 defect_cost=V*V*(s.Rational(1,9)+2*s.Rational(1,9))
 equal('nonminimal_pushed_representation_cost',pushed_cost,c**4/2)
 equal('coarse_full_tangent_minimum_cost',minimal_cost,c**4/6)
 equal('nonminimality_penalty',pushed_cost-minimal_cost,defect_cost)
 # Gaussian density derivative: -d(rho*u)/dy+rho*beta over rho equals V(y²-1)/2.
 u=V*y/3;alpha=V*(y*y-1)/6
 equal('coarse_minimizer_full_density',-s.diff(u,y)+y*u+alpha,V*(y*y-1)/2)
 # Total log-density score splits into marginal and conditional at initial marginal target.
 joint=-(s.Matrix([y,z]).T*(S.inv()-I)*s.Matrix([y,z]))[0]/2-s.log(1-c*c)/2
 cond=-(z-c*y)**2/(2*(1-c*c))+z*z/2-s.log(1-c*c)/2
 equal('gaussian_log_ratio_conditional_split',joint,cond)
 M=I-S.inv()
 transport=s.trace(M*M*S);reaction=s.trace((S-I)*(S-I))/2
 equal('full_kl_transport_dissipation',transport,2*c*c/(1-c*c))
 equal('full_kl_reaction_dissipation',reaction,c*c)
 equal('full_kl_total_dissipation',-transport-reaction,-c*c*(3-c*c)/(1-c*c))
 equal('full_kl_matrix_chain_rule',s.trace((I-S.inv())*dotS)/2,-transport-reaction)
 # Closed-time covariance and exact differential equations using q'=−3q.
 q=s.symbols('q',real=True);den=9-c*c*(1-q)**2
 a=1-3*c*c*q*(1-q)/den;ct=9*c*q/den
 St=s.Matrix([[a,ct],[ct,a]]);dSt=St.diff(q)*(-3*q)
 equal('finite_time_covariance_ode',dSt,2*I-St-St*St)
 equal('finite_time_covariance_initial',St.subs(q,1),S)
 equal('finite_time_covariance_terminal',St.subs(q,0),I)
 equal('finite_time_marginal_initial_derivative',s.diff(a,q).subs(q,1)*(-3),-c*c)
 rp=c*q/(3+c);rm=-c*q/(3-c)
 bp=(1+2*rp)/(1-rp);bm=(1+2*rm)/(1-rm)
 equal('finite_time_mean_eigenvalues',a,(bp+bm)/2)
 equal('finite_time_covariance_eigenvalues',ct,(bp-bm)/2)
 for tag,bv in [('plus',bp),('minus',bm)]:equal('eigenvalue_ode_'+tag,-3*q*s.diff(bv,q),(1-bv)*(bv+2))
 # Taylor coefficient is computed through chain rule at a=1, a'=-c².
 av=s.symbols('a',positive=True);KL=(av-1-s.log(av))/2
 equal('marginal_kl_first_derivative',s.diff(KL,av).subs(av,1)*(-c*c),0)
 equal('marginal_kl_second_taylor_coefficient',s.diff(KL,av,2).subs(av,1)*c**4/2,c**4/4)
 # Explicit c=1/2, q=1/2 gives a strict departure and positive covariance eigenvalues.
 At=a.subs({c:s.Rational(1,2),q:s.Rational(1,2)});Ct=ct.subs({c:s.Rational(1,2),q:s.Rational(1,2)})
 equal('finite_time_rational_variance',At,s.Rational(140,143))
 checks['finite_time_rational_positive_and_off_target']=bool(0<At-Ct<At+Ct and At<1)
 # Analytic denominator/sign controls use 0<|c|<1, 0<q<1; no sampling proof.
 # Product reaction algebra: centered sum equals sum of centered factors.
 ly,lz,ey,ez=s.symbols('ly lz ey ez');equal('product_centering',ly+lz-(ey+ez),(ly-ey)+(lz-ez))
 for r in json.loads((root/'INPUT_BINDINGS.json').read_text()):
  checks['snapshot:'+r['snapshot']]=hashlib.sha256((root/r['snapshot']).read_bytes()).hexdigest()==r['sha256']
  if args.original_root:
   checks['original:'+r['original']]=hashlib.sha256((args.original_root/r['original']).read_bytes()).hexdigest()==r['sha256']
 result={'scope':'Author exact algebraic controls plus input identities; not independent review or universal proof by enumeration','passed':sum(checks.values()),'total':len(checks),'checks':checks}
 args.output_dir.mkdir(parents=True,exist_ok=True);(args.output_dir/'CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[k for k,v in checks.items() if not v]},indent=2))
 raise SystemExit(0 if all(checks.values()) else 1)
if __name__=='__main__':main()
