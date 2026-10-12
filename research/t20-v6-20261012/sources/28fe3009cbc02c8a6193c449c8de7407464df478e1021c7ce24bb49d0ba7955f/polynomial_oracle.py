#!/usr/bin/env python3
"""Independent audit oracles: exact symbolic identities and Fraction instances.
No floating point, no calls to author test helpers, no theorem-generating claim.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import json
import sympy as S

HERE=Path(__file__).resolve().parents[1]

def psi(t): return t*t/2+4*t**4
def dp(t): return t+16*t**3
def div(v,t): return psi(v)-psi(t)-dp(t)*(v-t)
def losses(v,c,K=100):
    return (sum((x-y)**2 for x,y in zip(v,c))/2,
            div(v[0],c[0])+div(v[1],c[1])+Q(K,2)*((v[2]-c[2])**2+(v[3]-c[3])**2))
TRUTHS=[(Q(0),Q(0),Q(0),Q(0)),(Q(0),Q(0),Q(1),Q(0)),
        (Q(0),Q(0),Q(0),Q(1)),(Q(1),Q(1),Q(1),Q(1))]

def params(s,z,w,h,K=100):
    h1,h2,hz,hw=h; m=(h1+h2)/2;e=(h1-h2)**2/4;r=1+48*s*s;T=z+w
    g=96*e*s*s/(T*(K-r));b=(48*e*s-K*g)/r
    theta=96*K*s*s*(T-2*s)/(r*T*(K-r))
    return m,e,r,T,g,b,theta

def polynomial_coefficients(s,h,b,g,a):
    h1,h2,hz,hw=h;m=(h1+h2)/2;d2=1+144*s*s-96*a*s;d3=48*s-16*a
    return [d3*(h1**3+h2**3-2*m**3)-2*d2*m*b-100*g*(hz+hw),
            12*(h1**4+h2**4-2*m**4)-d2*b*b-6*d3*m*m*b-100*g*g,
            -6*d3*m*b*b-96*m**3*b,-2*d3*b**3-144*m*m*b*b,-96*m*b**3,-24*b**4]

def explicit_delta(s,z,w,h):
    h1,h2,hz,hw=h;m,e,r,T,g,b,theta=params(s,z,w,h)
    M=abs(-b*(h1+h2)-g*(hz+hw))+abs(-b*b-g*g)
    M+=sum(abs(c) for a in [0,1] for c in polynomial_coefficients(s,h,b,g,a))
    bary0=[1+s-z-w,z-s,w-s,s]
    linear=[m-hz-hw,hz-m,hw-m,m];quad=[b-2*g,g-b,g-b,b]
    L=sum(map(abs,linear+quad));p0=min(s,1-s,z,1-z,w,1-w);H=1+sum(map(abs,h))
    delta=min(Q(1),e*(1-theta)/(2*(M+1)),min(bary0)/(2*(L+1)),p0/(2*H))
    assert delta>0
    return delta

def candidate(s,z,w,h,eps,K=100,gamma_sign=1):
    m,e,r,T,g,b,theta=params(s,z,w,h,K);g*=gamma_sign
    q=s+eps*m+eps*eps*b
    return (q,q,z+eps*h[2]+eps*eps*g,w+eps*h[3]+eps*eps*g)

def baseline(s,z,w,h,eps):return tuple(x+eps*y for x,y in zip((s,s,z,w),h))
def bary(c):return (1+c[0]-c[2]-c[3],c[2]-c[0],c[3]-c[0],c[0])
def certify_case(s,z,w,h,eps):
    B=baseline(s,z,w,h,eps);C=candidate(s,z,w,h,eps)
    assert all(0<x<1 for x in B)
    assert all(x>0 for x in bary(C))
    assert sum(bary(C))==1
    assert tuple(sum(bary(C)[i]*TRUTHS[i][j] for i in range(4)) for j in range(4))==C
    gains=[]
    for v in TRUTHS:
        lb=losses(v,B);lc=losses(v,C);gain=tuple(a-b for a,b in zip(lb,lc))
        assert all(x>0 for x in gain)
        gains.extend(gain)
    return min(gains)

def symbolic_checks():
    s,t,e,T,eps=S.symbols('s t e T eps');h1,h2,hz,hw,b,g,a,l,u=S.symbols('h1 h2 hz hw b g a l u')
    r=1+48*s*s
    P=(1+s)*r*(100-r)-9600*s*s*(1-s)
    expected=-2304*s**5-2304*s**4+14304*s**3-4896*s*s+99*s+99
    assert S.expand(P-expected)==0
    all_bern=[]
    for j in range(8):
        poly=S.Poly(S.expand(P.subs(s,(j+t)/8)),t)
        power=[poly.nth(k) for k in range(6)]
        bern=[sum(power[k]*S.Rational(comb(i,k),comb(5,k)) for k in range(i+1)) for i in range(6)]
        assert all(v>=S.Rational(132,5) for v in bern)
        reconstruction=sum(bern[i]*comb(5,i)*t**i*(1-t)**(5-i) for i in range(6))
        assert S.expand(reconstruction-poly.as_expr())==0
        all_bern.append([str(x) for x in bern])
    m=(h1+h2)/2;v=(h1-h2)**2/4
    B=(s+eps*h1,s+eps*h2,t+eps*hz,u+eps*hw)
    C=(s+eps*m+eps*eps*b,s+eps*m+eps*eps*b,t+eps*hz+eps*eps*g,u+eps*hw+eps*eps*g)
    truth=(a,a,l,e)
    remg=-b*(h1+h2)-g*(hz+hw)-eps*(b*b+g*g)
    remf=sum(c*eps**j for j,c in enumerate(polynomial_coefficients(s,(h1,h2,hz,hw),b,g,a)))
    gainG=losses(truth,B)[0]-losses(truth,C)[0]
    gainF=losses(truth,B)[1]-losses(truth,C)[1]
    assert S.expand(gainG-eps**2*(v-2*(s-a)*b+(l+e-t-u)*g+eps*remg))==0
    assert S.expand(gainF-eps**2*(r*v+(s-a)*(96*s*v-2*r*b)+100*(l+e-t-u)*g+eps*remf))==0
    gg=96*e*s*s/(T*(100-r));bb=(48*e*s-100*gg)/r;theta=9600*s*s*(T-2*s)/(r*T*(100-r));margin=e*(1-theta)
    leading=[]
    for a0,j in [(0,0),(0,1),(1,2)]:
        LG=e-2*(s-a0)*bb+(j-T)*gg
        LF=r*e+(s-a0)*(96*s*e-2*r*bb)+100*(j-T)*gg
        gtarget=margin+(gg if j==1 else (96*e*s*(T-2*s)/(r*T) if j==2 else 0))
        ftarget=r*margin+(100*gg if j==1 else 0)
        assert S.cancel(LG-gtarget)==0;assert S.cancel(LF-ftarget)==0
        leading.append([str(S.factor(LG)),str(S.factor(LF))])
    envelope=S.Rational(1,4)+eps/2+13*eps**2/24
    baseA=((S.Rational(1,4)+eps)**2+S.Rational(1,4)**2)/2
    tailP=28561*eps**6+105456*eps**5+128440*eps**4+41184*eps**3-246864*eps**2-63360*eps+3456
    assert S.expand(envelope**2-baseA-eps**2*(169*eps**2+312*eps+12)/576)==0
    assert S.expand(2*div(S.Integer(1),envelope)-div(S.Integer(1),S.Rational(1,4)+eps)-div(S.Integer(1),S.Rational(1,4))-eps**2*tailP/13824)==0
    return {'bernstein_coefficients':all_bern,'minimum_bernstein_coefficient':str(min(S.Rational(x) for row in all_bern for x in row)), 'leading_formulas':leading,'exact_identity_count':19}

def controls():
    out={}
    s=Q(1,4);z=w=Q(3,5);h=(Q(1),Q(0),Q(0),Q(0));eps=Q(1,100000)
    B=baseline(s,z,w,h,eps)
    C=candidate(s,z,w,h,eps,gamma_sign=-1)
    bad=[losses(v,B)[1]-losses(v,C)[1] for v in TRUTHS]
    assert min(bad)<0;out['flipped_gamma']={'rejected':True,'minimum_gain':str(min(bad))}
    C=candidate(s,z,w,h,eps,K=10)
    bad=[losses(v,B,10)[k]-losses(v,C,10)[k] for v in TRUTHS for k in (0,1)]
    assert min(bad)<0;out['free_curvature_10']={'rejected':True,'minimum_gain':str(min(bad))}
    tangent=(Q(1),Q(1),Q(0),Q(0));C=candidate(s,z,w,tangent,eps);B=baseline(s,z,w,tangent,eps)
    assert C==B;out['dropped_transverse']={'rejected':True,'all_gains':'0'}
    B=baseline(Q(0),Q(1,4),Q(1,4),(Q(1),Q(-1),Q(0),Q(0)),eps)
    assert min(B)<0;out['closed_hull_boundary']={'rejected':True,'baseline_coordinate':str(B[1])}
    # Unbounded scale is not implied by an existential local theorem.
    C=candidate(s,z,w,h,Q(1));B=baseline(s,z,w,h,Q(1))
    assert any(x<=0 for x in bary(C)) or any(losses(v,B)[k]<=losses(v,C)[k] for v in TRUTHS for k in (0,1))
    out['dropped_small_scale']={'rejected':True}
    assert div(Q(1),Q(1,4))!=div(Q(1,4),Q(1))
    out['reversed_Bregman_orientation']={'rejected':True,'forward':str(div(Q(1),Q(1,4))),'reversed':str(div(Q(1,4),Q(1)))}
    # Enlarging the isolated theorem's epsilon range to 1 makes even all-state weak failure false.
    eps1=Q(1);q=Q(1,2);isoB=(Q(1,4)+eps1,Q(1,4))
    for a in [Q(0),Q(1)]:
        assert (q-a)**2 <= sum((t-a)**2 for t in isoB)/2
        assert 2*div(a,q) <= sum(div(a,t) for t in isoB)
    out['isolated_scale_to_1']={'rejected':True,'epsilon':'1','coherent_common_repair':'1/2','baseline':['5/4','1/4']}
    return out

def main():
    symbolic=symbolic_checks();records=[]
    dirs=[(1,0,0,0),(-1,0,0,0),(0,1,3,-2),(100,99,-100,120),(1,-1,1000,-1000),(Q(1,1000),0,1,-1)]
    contexts=[]
    for weights in product([1,2,4],repeat=4):
        den=sum(weights);a=[Q(x,den) for x in weights]
        contexts.append((a[3],a[1]+a[3],a[2]+a[3]))
    for k in [3,6,12]:
        for small in range(4):
            a=[Q(1,3)]*4;a[small]=Q(1,10**k);a=[x/sum(a) for x in a]
            contexts.append((a[3],a[1]+a[3],a[2]+a[3]))
    for s,z,w in contexts:
        for raw in dirs:
            h=tuple(Q(x) for x in raw);delta=explicit_delta(s,z,w,h)
            eps=delta*Q(999,1000);gain=certify_case(s,z,w,h,eps)
            records.append({'context':[str(s),str(z),str(w)],'direction':list(map(str,h)), 'delta':str(delta),'epsilon':str(eps),'minimum_gain':str(gain)})
    result={'status':'PASS','symbolic':symbolic,'exact_context_count':len(contexts),'direction_count':len(dirs),'case_count':len(records),'truth_score_comparisons':8*len(records),'controls':controls(),'cases':records}
    (HERE/'evidence'/'EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['cases','symbolic']},indent=2))
if __name__=='__main__':main()
