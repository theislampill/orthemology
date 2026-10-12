#!/usr/bin/env python3
"""Independent exact controls for the Gaussian entropy transfer.

These finite symbolic controls corroborate, and do not prove, the all-dimension
ODE/compactness statements assessed in REVIEW.md. No author module is imported.
"""
import argparse
import json
from pathlib import Path
import sympy as s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    checks = []

    def zero(name, expression):
        terms = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
        residuals = [s.factor(v) for v in terms]
        assert all(v == 0 for v in residuals), (name, residuals)
        checks.append({'name': name, 'result': 'PASS', 'kind': 'exact-symbolic'})

    def truth(name, value):
        assert value, name
        checks.append({'name': name, 'result': 'PASS', 'kind': 'exact-rational'})

    c11, c12, c22 = s.symbols('c11 c12 c22')
    t11, t12, t22 = s.symbols('t11 t12 t22')
    q11, q12, q22 = s.symbols('q11 q12 q22')
    alpha, beta, eps = s.symbols('alpha beta epsilon', nonnegative=True)
    x1, x2, a1, a2, e1, e2 = s.symbols('x1 x2 a1 a2 e1 e2')
    Sigma = s.Matrix([[c11, c12], [c12, c22]])
    S = s.Matrix([[t11, t12], [t12, t22]])
    Q = s.Matrix([[q11, q12], [q12, q22]])
    P = Sigma.inv()
    I = s.eye(2)
    x = s.Matrix([x1, x2])
    a = s.Matrix([a1, a2])
    e = s.Matrix([e1, e2])

    def scalar(v):
        return v[0]

    def L(C, A, al=1, be=1):
        return 2*al*(A*C + C*A) + 2*be*C*A*C

    def gaussian_score(h, B):
        return scalar(h.T*P*x) + (scalar(x.T*P*B*P*x)-s.trace(P*B))/2

    def positive_operator_score(v, A, al=1, be=1):
        f = scalar(v.T*x)+scalar(x.T*A*x)-s.trace(A*Sigma)
        return -2*al*s.trace(A)+al*scalar((P*x).T*(v+2*A*x))+be*f

    h = (alpha*I+beta*Sigma)*a
    B = L(Sigma,S,alpha,beta)
    zero('full_density_weighted_cometric_d2', gaussian_score(h,B)-positive_operator_score(a,S,alpha,beta))
    action = alpha*(scalar(a.T*a)+4*s.trace(S*S*Sigma)) + beta*(scalar(a.T*Sigma*a)+2*s.trace(S*Sigma*S*Sigma))
    zero('weighted_action_frobenius_pairing_d2', action-scalar(a.T*h)-s.trace(S*B))
    zero('accepted_unit_covariance_operator', L(Sigma,S)-2*(S*Sigma+Sigma*S+Sigma*S*Sigma))
    mass=s.Symbol('mass',positive=True)
    mass_action=mass*(alpha*(scalar((a/mass).T*(a/mass))+4*s.trace((S/mass)*(S/mass)*Sigma))+beta*(scalar((a/mass).T*Sigma*(a/mass))+2*s.trace((S/mass)*Sigma*(S/mass)*Sigma)))
    zero('nonunit_mass_shape_inverse_scaling', mass_action-scalar(a.T*h)/mass-s.trace(S*B)/mass)

    l1,l2,b11,b12,b22=s.symbols('l1 l2 b11 b12 b22', positive=True)
    Cdiag=s.diag(l1,l2)
    target=s.Matrix([[b11,b12],[b12,b22]])
    inverse=s.Matrix(2,2,lambda i,j:target[i,j]/(2*(alpha*([l1,l2][i]+[l1,l2][j])+beta*[l1,l2][i]*[l1,l2][j])))
    c2=b11**2/(4*alpha*l1+2*beta*l1**2)+b22**2/(4*alpha*l2+2*beta*l2**2)+b12**2/(alpha*(l1+l2)+beta*l1*l2)
    zero('diagonal_basis_inverse', L(Cdiag,inverse,alpha,beta)-target)
    zero('off_diagonal_frobenius_factor', s.trace(target*inverse)-c2)
    zero('one_dimensional_metric', 4*alpha*l1+2*beta*l1**2-2*l1*(2*alpha+beta*l1))

    dSigma = 2*eps*I+eps*Sigma-Q*Sigma-Sigma*Q-Sigma*Q*Sigma
    dm = -(I+Sigma)*Q*e
    Seps=(Q-eps*P)/2
    J=scalar(e.T*Q*e)/2+s.trace(Q*Sigma)/2-eps*s.log(Sigma.det())/2
    directional=sum(s.diff(J,c)*b for c,b in [(c11,t11),(c12,t12),(c22,t22)])
    zero('entropy_covariance_differential_frobenius',directional-s.trace(Seps*S))
    zero('entropy_full_density_tangency_d2', gaussian_score(dm,dSigma)+positive_operator_score(Q*e,Seps))
    zero('entropy_negative_gradient_covariance', dSigma+L(Sigma,Seps))
    zero('entropy_negative_gradient_mean', dm+(I+Sigma)*Q*e)
    dJ = scalar((Q*e).T*dm)+s.trace(Seps*dSigma)
    dissipation=scalar((Q*e).T*(I+Sigma)*(Q*e))+s.trace(Seps*L(Sigma,Seps))
    zero('exact_energy_dissipation_d2', dJ+dissipation)
    zero('entropy_contribution', dSigma-dSigma.subs(eps,0)-eps*(2*I+Sigma))
    equilibrium=eps*Q.inv()
    zero('positive_temperature_covariance_equilibrium',2*eps*I+eps*equilibrium-Q*equilibrium-equilibrium*Q-equilibrium*Q*equilibrium)
    zero('source_time_scaling', eps*(2*I-(Q/eps)*Sigma-Sigma*(Q/eps)+Sigma-Sigma*(Q/eps)*Sigma)-dSigma)
    zero('zero_temperature_precision_ode', -P*dSigma.subs(eps,0)*P-(P*Q+Q*P+Q))

    d11,d12,d22=s.symbols('d11 d12 d22')
    Delta=s.Matrix([[d11,d12],[d12,d22]])
    Sigma0=Sigma-Delta
    f0=lambda C:-Q*C-C*Q-C*Q*C
    rhs=-Q*Delta-Delta*Q-Delta*Q*Sigma-Sigma0*Q*Delta+eps*(2*I+Sigma)
    zero('noncommuting_covariance_difference_identity',dSigma-f0(Sigma0)-rhs)
    z=s.Matrix(s.symbols('z1 z2'))
    zero('noncommuting_mean_difference_identity',-(I+Sigma)*Q*(e+z)+(I+Sigma0)*Q*e-(-(I+Sigma)*Q*z-Delta*Q*e))

    lam,u,v,w=s.symbols('lambda u v w')
    C3=s.Matrix([[lam,0,0],[0,u,v],[0,v,w]])
    q13,q23,q33=s.symbols('q13 q23 q33')
    Q3=s.Matrix([[q11,q12,q13],[q12,q22,q23],[q13,q23,q33]])
    F3=2*eps*s.eye(3)+eps*C3-Q3*C3-C3*Q3-C3*Q3*C3
    zero('arbitrary_eigendirection_rayleigh_identity_d3',F3[0,0]-(2+lam)*(eps-lam*q11))

    M,R,r,A,L,t=s.symbols('M R r A L t',positive=True)
    totalL=r*(2*(1+M)+R)
    zero('gronwall_delta_coefficient',totalL-(2*r*(1+M)+r*R))
    truth('gronwall_mean_coefficient_dominated',s.simplify(totalL-r*(1+M)).is_positive)
    bound=eps*A*(s.exp(L*t)-1)/L
    zero('explicit_gronwall_majorant_equation',s.diff(bound,t)-L*bound-eps*A)
    zero('explicit_gronwall_initial_condition',bound.subs(t,0))
    zero('explicit_gronwall_zero_epsilon',bound.subs(eps,0))

    Cn=s.Matrix([[2,1],[1,3]])
    Qn=s.Matrix([[3,1],[1,1]])
    truth('test_covariance_spd',Cn[0,0]>0 and Cn.det()>0)
    truth('test_precision_spd',Qn[0,0]>0 and Qn.det()>0)
    truth('noncommuting_example_is_noncommuting',Qn*Cn != Cn*Qn)
    good=-Qn*Cn-Cn*Qn-Cn*Qn*Cn
    wrong=-2*Cn*Qn-Cn*Qn*Cn
    truth('correct_covariance_velocity_symmetric',good==good.T)
    truth('commuting_shortcut_rejected',wrong!=good and wrong!=wrong.T)

    xx=s.Symbol('x',real=True)
    rho=s.exp(-xx**2/2)/s.sqrt(2*s.pi)
    wrong_pde=s.diff(s.diff(rho,xx)+rho*(-xx),xx)/rho
    correct_pde=s.diff(s.diff(rho,xx)-rho*(-xx),xx)/rho
    zero('operator_target_stationarity',correct_pde)
    zero('printed_plus_sign_target_residual',wrong_pde-2*(xx**2-1))
    truth('printed_plus_sign_is_nonstationary',s.simplify(wrong_pde)!=0)

    result={'status':'PASS','count':len(checks),'sympy_version':s.__version__,'checks':checks,
        'noncommuting_witness':{'Sigma':str(Cn),'Q':str(Qn),'correct_velocity':str(good),'incorrect_shortcut':str(wrong)},
        'scope':'Finite exact algebraic controls only. All-dimension norm bounds, positivity, global existence, and convergence are assessed by the independent proof review.'}
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','count':len(checks),'output':args.output}))


if __name__=='__main__':
    main()
