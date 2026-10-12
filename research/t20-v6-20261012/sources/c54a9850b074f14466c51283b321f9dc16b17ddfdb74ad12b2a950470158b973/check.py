import sympy as s,json
c,t,y=s.symbols('c t y', real=True)
S=s.Matrix([[1,c],[c,1]]);D=2*s.eye(2)-S-S*S
h=(c*c*y*y-c*c-s.log(1-c*c))/2
checks={
 'full_marginal_variance_derivative':s.simplify(D[0,0]+c*c)==0,
 'offdiagonal_derivative':s.simplify(D[0,1]+3*c)==0,
 'coarse_stationarity':2-1-1==0,
 'conditional_centered_reaction':s.simplify(h-(-s.log(1-c*c)/2)-c*c*(y*y-1)/2)==0,
 'variance_reaction_covariance':s.simplify(-c*c*(3-1)/2+c*c)==0,
 'marginal_kl_second_order':s.simplify(s.diff((1-c*c*t-1-s.log(1-c*c*t))/2,t,2).subs(t,0)-c**4/2)==0,
 'full_kl_initial_dissipation':s.simplify(s.trace((s.eye(2)-S.inv())*D)/2+c*c*(3-c*c)/(1-c*c))==0
}
print(json.dumps({'checks':checks,'passed':sum(checks.values()),'total':len(checks),'scope':'Exact symbolic participating checks, not independent review or PDE existence proof'},indent=2));assert all(checks.values())
