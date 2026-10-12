#!/usr/bin/env python3
"""Independent controls; no imports from author/root checker. Not a universal proof."""
import argparse, json, math
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import quad
from scipy.special import logsumexp

checks=[]
def check(name, ok, evidence=None):
    if not bool(ok):
        raise RuntimeError(f'FAILED: {name}: {evidence}')
    checks.append({'name':name,'passed':True,'evidence':evidence})
def zero(M):
    if isinstance(M,s.MatrixBase): return all(s.simplify(x)==0 for x in M)
    return s.simplify(M)==0

def exact_controls():
    I=s.eye(2); T=s.diag(1,s.Rational(1,2)); A=T.inv()
    B=s.diag(s.Rational(1,2),s.Rational(1,4)); a=s.Rational(1,2)
    c=s.Matrix([1,-2]); m0=s.Matrix([3,-1]); S0=s.ones(2)
    Q=T*(I-B*B); Sd=B*S0*B+Q; md=c+B*(m0-c)
    P=a*Sd.inv()+(1-a)*A; Sr=P.inv(); mr=Sr*(a*Sd.inv()*md+(1-a)*A*c)
    check('rank_one_initial_covariance',S0.det()==0 and S0.rank()==1)
    check('OU_positive_noise',Q[0,0]>0 and Q.det()>0,str(Q))
    check('OU_positive_covariance',Sd[0,0]>0 and Sd.det()>0,str(Sd))
    check('noncommuting_precisions',not zero(Sd.inv()*A-A*Sd.inv()))
    check('reaction_positive_covariance',Sr[0,0]>0 and Sr.det()>0,str(Sr))
    check('reaction_relative_mean_order',zero(mr-c-a*Sr*Sd.inv()*B*(m0-c)),str(mr))
    check('wrong_reordered_mean_rejected',not zero(mr-c-a*Sd.inv()*Sr*B*(m0-c)))
    x=s.Matrix(s.symbols('x0:2')); qquad=lambda m,S:((x-m).T*S.inv()*(x-m))[0]
    diff=s.expand(a*qquad(md,Sd)+(1-a)*qquad(c,T)-qquad(mr,Sr))
    check('normalized_product_completes_square',all(s.diff(diff,v)==0 for v in x),str(diff))
    check('OU_target_fixed',zero(B*T*B+Q-T))
    check('reaction_target_fixed',zero((a*A+(1-a)*A).inv()-T))
    # General off-centred noncommuting Gaussian generator, independently at density level.
    S=s.Matrix([[2,1],[1,3]]); m=s.Matrix([s.Rational(2,3),-1]); P=S.inv(); e=x-m; d=m-c
    score=A*(x-c)-P*e
    trans=s.trace(A-P)-(e.T*P*score)[0]
    q0=s.Rational(1,2)*(((x-c).T*A*(x-c))[0]-(e.T*P*e)[0])
    h0=s.Rational(1,2)*(s.trace(A*S)+(d.T*A*d)[0]-2)
    react=-q0+h0
    Sd_dot=2*I-A*S-S*A; md_dot=-A*d
    Sr_dot=S-S*A*S; mr_dot=-S*A*d
    def tangent(Sdot,mdot):
        return -s.trace(P*Sdot)/2+(e.T*P*Sdot*P*e)[0]/2+(mdot.T*P*e)[0]
    check('OU_full_density_generator',zero(trans-tangent(Sd_dot,md_dot)))
    check('reaction_full_density_generator',zero(react-tangent(Sr_dot,mr_dot)))
    check('combined_full_density_generator',zero(trans+react-tangent(Sd_dot+Sr_dot,md_dot+mr_dot)))
    # Differentiate finite update at zero using exact inverse derivative, retaining order.
    dP=-P-P*Sd_dot*P+A
    dS=-S*dP*S
    dm=-d+dS*P*d-S*P*Sd_dot*P*d-A*d
    check('split_covariance_first_derivative',zero(dS-(Sd_dot+Sr_dot)))
    check('split_mean_first_derivative',zero(dm-(md_dot+mr_dot)))
    # Gaussian entropy derivative against transport Fisher plus reaction log variance.
    Hdot=s.trace(A*(Sd_dot+Sr_dot))/2+(d.T*A*(md_dot+mr_dot))[0]-s.trace(P*(Sd_dot+Sr_dot))/2
    C=A-P; fisher=s.trace(C*S*C)+(d.T*A*A*d)[0]
    variance=s.trace(C*S*C*S)/2+(d.T*A*S*A*d)[0]
    check('Gaussian_entropy_exact_dissipation',zero(Hdot+fisher+variance),str(-Hdot))
    # Exact kernel KL decomposition, no density hypothesis on mixing law.
    ker=s.Rational(1,2)*((d.T*B*A*B*d)[0]-s.trace(B*B)-s.log((I-B*B).det()))
    direct=s.Rational(1,2)*(s.trace(A*Q)+(B*d).dot(A*B*d)-2+s.log(T.det()/Q.det()))
    check('kernel_KL_constant_and_quadratic',zero(ker-direct))
    # Countercontrol separating full projected and stricter fibrewise Gaussian flow.
    b=s.Rational(1); v=s.Rational(11,10); y=s.symbols('y',real=True)
    b_full=-b*(v+2+b*b/3); v_full=(1-v)*(v+2)+2*b*b
    hfull=(1-1/v)*v_full/2+b*b_full*y*y
    bf=-b*(1+v); vf=(1-v)*(v+2)
    hf=(1-1/v)*vf/2+b*bf*y*y
    check('full_projection_fibre_growth_control',zero(hfull-(s.Rational(169,2200)-s.Rational(103,30)*y*y)))
    check('strict_fibrewise_decrease_control',zero(hf-(-b*b*y*y*(1+v)-(v-1)**2*(1/v+s.Rational(1,2)))))
    check('flows_are_different_at_same_state',b_full!=bf and v_full!=vf)


def lp_gauss(x,m,v): return -0.5*(math.log(2*math.pi*v)+(x-m)**2/v)
def numeric_controls():
    weights=np.array([.2,.5,.3]); atoms=np.array([-3.,.7,2.]); h=.3; T=1.7; c=-.4
    B=math.exp(-h/T); Q=T*(1-B*B); means=c+B*(atoms-c); a=math.exp(-h)
    lp=lambda x:float(logsumexp(np.log(weights)-.5*(np.log(2*math.pi*Q)+(x-means)**2/Q)))
    lg=lambda x:lp_gauss(x,c,T)
    integ=lambda f:quad(f,-np.inf,np.inf,epsabs=2e-10,epsrel=2e-10,limit=250)[0]
    H=integ(lambda x:math.exp(lp(x))*(lp(x)-lg(x)))
    bound=.5*(B*B/T*np.dot(weights,(atoms-c)**2)-B*B-math.log(1-B*B))
    check('atomic_mixture_KL_below_kernel_bound',H<=bound+1e-9,{'H':H,'bound':bound})
    check('OU_density_probability',abs(integ(lambda x:math.exp(lp(x)))-1)<1e-9)
    lunn=lambda x:a*lp(x)+(1-a)*lg(x)
    Z=integ(lambda x:math.exp(lunn(x)))
    lr=lambda x:lunn(x)-math.log(Z)
    Hr=integ(lambda x:math.exp(lr(x))*(lr(x)-lg(x)))
    check('reaction_normalization_between_zero_one',0<Z<=1,{'Z':Z})
    check('reaction_probability',abs(integ(lambda x:math.exp(lr(x)))-1)<1e-9)
    check('atomic_smoothed_reaction_entropy_descent',0<=Hr<=H+1e-9,{'before':H,'after':Hr})
    M=integ(lambda x:math.exp(lr(x))*(x-c)**2/T)
    check('entropy_to_relative_moment_bound',M<=4*Hr+2*math.log(2)+1e-9,{'moment':M,'bound':4*Hr+2*math.log(2)})
    K=integ(lambda x:math.exp(lp(x))*(lp(x)-lr(x)))
    check('forward_reaction_KL_identity',abs(K-((1-a)*H+math.log(Z)))<1e-9)
    check('forward_reaction_KL_upper_bound',-1e-10<=K<=(1-a)*H+1e-9)
    # Pure reaction must retain zero support; finite model checks exact mechanism.
    p=np.array([.25,.25,.25,.25]); r=np.array([.25,.75,0.,0.]); f=r/p
    last=float('inf'); hs=[]
    for theta in [1.,.8,.5,.1,.001]:
        powf=np.power(f,theta); z=float(np.dot(p,powf)); rr=p*powf/z
        HH=float(np.dot(rr[:2],np.log(rr[:2]/p[:2])))
        hs.append(HH)
        if not (rr[2]==rr[3]==0 and HH<=last+1e-14 and z>0 and z<=1+1e-14):
            raise RuntimeError('finite reaction control')
        last=HH
    check('zero_support_preserved_and_entropy_descends',True,hs)
    check('zero_support_reaction_limit_not_full_target',abs(hs[-1]-math.log(2))<2e-6)
    theta=.55; fpos=f[:2]; w=p[:2]*fpos**theta; zz=w.sum(); rr=w/zz
    logs=np.log(fpos); var=np.dot(rr,logs**2)-np.dot(rr,logs)**2
    def HH(t):
        ww=p[:2]*fpos**t; zz=ww.sum(); rr=ww/zz
        return t*np.dot(rr,np.log(fpos))-math.log(zz)
    eps=1e-5
    check('reaction_H_derivative_theta_variance',abs((HH(theta+eps)-HH(theta-eps))/(2*eps)-theta*var)<1e-9)
    # Singular point input: shrinking-step entrance only, not finite-time Trotter.
    rows=[]
    for n in [5,10,15,20]:
        t=2.**(-n); B=math.exp(-t); aa=math.exp(-t); ss=-math.expm1(-2*t); md=2*B
        sr=1/(aa/ss+1-aa); mr=aa*md/ss*sr
        HD=.5*(ss+md*md-1-math.log(ss))
        kl=.5*(ss/sr+(md-mr)**2/sr-1+math.log(sr/ss))
        rows.append({'h':t,'reaction_KL':kl,'upper_bound':(1-aa)*HD,'mean':mr,'variance':sr})
        if not (-1e-12<=kl<=(1-aa)*HD+1e-10): raise RuntimeError('entrance bound')
    check('singular_entrance_reaction_difference_bound',True,rows)
    check('singular_entrance_mean_variance_approach_input',abs(rows[-1]['mean']-2)<3e-6 and rows[-1]['variance']<3e-6)
    check('singular_entrance_bound_tends_zero_on_sequence',rows[-1]['upper_bound']<rows[0]['upper_bound']/1000)
    # Absolute-continuous mixture: OU and full split inherit correct LSI constant.
    vs=np.array([.4,.9,2.]); lp0=lambda x:float(logsumexp(np.log(weights)-.5*(np.log(2*math.pi*vs)+(x-atoms)**2/vs)))
    BB=math.exp(-h/T); vv=BB*BB*vs+T*(1-BB*BB); mm=c+BB*(atoms-c)
    lpd=lambda x:float(logsumexp(np.log(weights)-.5*(np.log(2*math.pi*vv)+(x-mm)**2/vv)))
    H0=integ(lambda x:math.exp(lp0(x))*(lp0(x)-lg(x)))
    HD=integ(lambda x:math.exp(lpd(x))*(lpd(x)-lg(x)))
    aa=math.exp(-h); lpow=lambda x:aa*lpd(x)+(1-aa)*lg(x); ZZ=integ(lambda x:math.exp(lpow(x)))
    HP=integ(lambda x:math.exp(lpow(x))/ZZ*(lpow(x)-math.log(ZZ)-lg(x)))
    check('nonGaussian_OU_LSI_contraction_control',HD<=math.exp(-2*h/T)*H0+1e-9,{'H0':H0,'HD':HD,'factor':math.exp(-2*h/T)})
    check('nonGaussian_split_contraction_control',HP<=HD+1e-9 and HP<=math.exp(-2*h/T)*H0+1e-9,{'H0':H0,'HD':HD,'HP':HP})

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True); args=parser.parse_args()
    exact_controls(); numeric_controls()
    out={'status':'PASS','count':len(checks),'limits':'Named exact algebra and numerical examples only; not a universal proof, PDE limit, or computability theorem.','checks':checks}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(f'PASS {len(checks)} independent controls')
