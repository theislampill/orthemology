import json
from pathlib import Path
import sympy as S
b,beta=S.symbols('b beta',real=True);s,tau=S.symbols('s tau',positive=True)
C=S.Matrix([[1,b],[b,b*b+s]]);Q=S.Matrix([[1+beta**2/tau,-beta/tau],[-beta/tau,1/tau]]);D=S.diag(1,0)
k=(b-beta)*(b-3*beta)/(6*tau)
def V(k): return 2*S.eye(2)+C-Q*C-C*Q-C*Q*C+2*k*(D*C+C*D+C*D*C)
M=S.Matrix([[1+2*s+b*b/3,-2*b*s],[-2*b*s,2*s*(s+2+2*b*b)]]);grad=S.Matrix([(b-beta)/tau,(1/tau-1/s)/2]);v=-M*grad
checks={
 'corrected_entire_y_covariance':S.factor(V(k)[0,0])==0,
 'regression_mobility':S.factor(V(k)[0,1]-v[0])==0,
 'conditional_variance_mobility':S.factor(V(k)[1,1]-2*b*V(k)[0,1]-v[1])==0,
 'blind_product_transfer_leak':S.factor(V((b-beta)**2/(6*tau))[0,0]-2*beta*(b-beta)/tau)==0,
 'target_stationary':all(S.simplify(z.subs({b:beta,s:tau}))==0 for z in v),
 'correlation_creation':S.simplify(v[0].subs({b:0,s:tau})-beta*(1+2*tau)/tau)==0,
 'product_recovery':S.factor(v[0].subs({beta:0,tau:1})+b*(s+2+b*b/3))==0,
 'initial_conditional_variance':S.simplify(v[1].subs({b:0,s:tau}))==0
}
if not all(checks.values()): raise RuntimeError(checks)
result={'status':'PASS','scope':'Participating exact algebra, not independent review or PDE existence','checks':checks,'count':len(checks)}
print(json.dumps(result,indent=2))
