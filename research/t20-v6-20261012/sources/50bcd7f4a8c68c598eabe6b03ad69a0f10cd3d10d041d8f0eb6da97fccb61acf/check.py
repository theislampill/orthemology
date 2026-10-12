import sympy as S,json
b=S.symbols('b', real=True);s=S.symbols('s', positive=True)
M=S.Matrix([[1,b],[b,s+b*b]]);I=S.eye(2);A=(I-M.inv())/2;P=S.diag(b*b/6,0)
def K(X):return 2*(X*M+M*X+M*X*M)
U=-K(A);V=-K(A-P)
Db=-b*(s+2+b*b/3);Ds=(1-s)*(s+2)+2*b*b
Dfull=S.trace(A*K(A));Dcon=S.trace((A-P)*K(A-P));Dfib=b*b*(1+s)+(s-1)**2*(1/s+S.Rational(1,2))
J=(s+b*b-1-S.log(s))/2
checks={
 'unconstrained_covariance':all(S.simplify(x)==0 for x in U-(2*I-M-M*M)),
 'fixed_marginal':S.simplify(V[0,0])==0,
 'cross_velocity':S.simplify(V[0,1]-Db)==0,
 'conditional_variance_velocity':S.simplify(V[1,1]-2*b*Db-Ds)==0,
 'horizontal_cost':S.simplify(Dfull-Dcon-b**4/6)==0,
 'fibrewise_gap':S.simplify(Dcon-Dfib-b*b/s-b**4/3)==0,
 'conditional_KL_dissipation':S.simplify(S.diff(J,b)*Db+S.diff(J,s)*Ds+Dcon)==0,
 'stationary_target':Db.subs(b,0)==0 and Ds.subs({b:0,s:1})==0
}
print(json.dumps({'checks':checks,'passed':sum(checks.values()),'total':len(checks),'symbolic_full_dissipation':str(S.factor(Dfull)),'symbolic_constrained_dissipation':str(S.factor(Dcon)),'scope':'Root participating exact algebra, no independent acceptance or global proof'},indent=2));assert all(checks.values())
