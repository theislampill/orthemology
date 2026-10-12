#!/usr/bin/env python3
"""Author controls, not independent review or a formal proof.
Exact fractions and SymPy identities are separated from numerical diagnostics.
No assertions: all checks remain active under Python -O.
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, math, platform
from fractions import Fraction as Q
from pathlib import Path
import sympy as sp
import mpmath as mp

HERE=Path(__file__).resolve().parent
RESULTS=[]
def check(name, condition, detail=None, kind='exact'):
    if not condition: raise RuntimeError('FAILED: '+name+' '+str(detail))
    RESULTS.append({'name':name,'kind':kind,'status':'PASS','detail':detail})

def norm(v):
    s=sum(v)
    if s<=0: raise ValueError('positive total required')
    return [x/s for x in v]

def audit(w,a): return norm([x*y for x,y in zip(w,a)])
def p2(z): return 1+z+z*z/2

def mass_step(w,c,h,alpha=Q(1), rule='p2'):
    if h<0 or any(x<=0 for x in w) or sum(w)!=1: raise ValueError('interior, normalized, forward step required')
    b=min(c)
    a=[1/p2(alpha*h*(v-b)) for v in c]
    return norm([x*y for x,y in zip(w,a)])

def quadratic_internal(x,h): return x*(1-h/2)/(1+h/2)

def quartic_internal(x,h):
    """Finite exact-rational bisection, with certified position error <= h^3/200.
    A root in [-|x|,|x|] guarantees endpoint energy descent even before convergence.
    """
    if h<0: raise ValueError('forward step required')
    if h==0 or x==0: return x, {'bisections':0,'error_bound':Q(0)}
    u=abs(x); lo=Q(-1); hi=Q(1); eps=h**3/100
    def f(z): return z-1+h*u*u*(z**3+z*z+z+1)/4
    count=0
    if not(f(lo)<0 and f(hi)>0): raise RuntimeError('invalid bracket')
    while (hi-lo)*u>eps:
        mid=(lo+hi)/2; v=f(mid); count+=1
        if v==0: lo=hi=mid; break
        if v<0: lo=mid
        else: hi=mid
    z=(lo+hi)/2
    y=u*z if x>0 else -u*z
    if not(abs(y)<=abs(x) and f(lo)<=0<=f(hi)): raise RuntimeError('invalid certificate')
    return y, {'bisections':count,'error_bound':u*(hi-lo)/2}

def singleton_step(w,x,h,potential='quadratic'):
    if potential=='quadratic':
        y=[quadratic_internal(t,h) for t in x]; V=lambda t:t*t/2; certificates=[]
    else:
        pairs=[quartic_internal(t,h) for t in x]
        y=[a for a,b in pairs]; certificates=[b for a,b in pairs]; V=lambda t:t**4/4
    c=[(V(a)+V(b))/2 for a,b in zip(x,y)]
    wp=mass_step(w,c,h)
    return wp,y,certificates

# Genuine nonlinear grouped benchmark: q=log(r/(1-r)); two interacting positions.
# V1=(q^2+(x2-x1)^2)/2, V2=z^2/2, alpha=1.
def sigmoid(q): return 1/(1+mp.exp(-q))
def kappa(q): return 2+2*mp.cosh(q)

def group_internal(y,h):
    q,x1,x2,z=y
    if h==0: return y,mp.mpf('0'),0
    if q==0: s=mp.mpf('0'); count=0
    else:
        sign=1 if q>0 else -1; u=abs(q); lo=mp.mpf('0'); hi=u; count=0
        # s + (h/2) kappa(s) s = q has derivative >= 1 for h>=0.
        # Absolute termination is numerical; exact existence/uniqueness is proved in RESULT.md.
        for count in range(1,600):
            mid=(lo+hi)/2
            fm=mid*(1+h*kappa(mid)/2)-u
            if fm<0: lo=mid
            else: hi=mid
            if hi-lo<min(mp.mpf('1e-65'),h**3*mp.mpf('1e-20')): break
        else: raise RuntimeError('bisection failed')
        s=sign*(lo+hi)/2
    r=sigmoid(s); kap=kappa(s); d=x2-x1
    gam=(1-h*kap/2)/(1+h*kap/2)
    dp=gam*d; dm=(d+dp)/2
    yp=(2*s-q,x1+h*dm/r,x2-h*dm/(1-r),quadratic_internal(z,h))
    # Save equation residual, not only the library's success flag.
    mid=[(a+b)/2 for a,b in zip(y,yp)]
    qm,a,b,zm=mid; dm=b-a; rm=sigmoid(qm)
    field=(-kappa(qm)*qm,dm/rm,-dm/(1-rm),-zm)
    residual=max(abs(v-u-h*f) for u,v,f in zip(y,yp,field))
    return yp,residual,count

def losses(y):
    q,x1,x2,z=y
    return ((q*q+(x2-x1)**2)/2,z*z/2)

def grouped_step(m,y,h,rule='p2',endpoint_only=False):
    yp,residual,it=group_internal(y,h)
    v0=losses(y); v1=losses(yp)
    c=v1 if endpoint_only else tuple((a+b)/2 for a,b in zip(v0,v1))
    base=min(c)
    if rule=='p2': a=[1/p2(h*(v-base)) for v in c]
    elif rule=='exponential': a=[mp.exp(-h*(v-base)) for v in c]
    else: raise ValueError(rule)
    mn=norm([v*b for v,b in zip(m,a)])
    e0=sum(v*b for v,b in zip(m,v0)); e1=sum(v*b for v,b in zip(mn,v1))
    reaction=sum((b-a)*c0 for a,b,c0 in zip(m,mn,c))
    internal=sum((a+b)*(v-u)/2 for a,b,u,v in zip(m,mn,v0,v1))
    return mn,yp,{'residual':residual,'iterations':it,'energy_change':e1-e0,
                  'reaction_term':reaction,'internal_term':internal,
                  'energy_identity_error':abs((e1-e0)-(reaction+internal))}

def reference(t,m,y):
    q0,x10,x20,z0=y
    if q0<=0: raise ValueError('reference uses q0>0')
    # Independent scalar separated-variables quadrature, not the discrete update.
    lower=q0*mp.exp(-kappa(q0)*t); upper=q0*mp.exp(-4*t)
    def elapsed(q): return mp.quad(lambda u:1/(kappa(u)*u),[q,q0])
    lo=lower; hi=upper
    for _ in range(220):
        mid=(lo+hi)/2
        if elapsed(mid)>t: lo=mid
        else: hi=mid
    qt=(lo+hi)/2; C=(x20-x10)/q0; dt=C*qt
    primitive=lambda u:u-mp.log(1+mp.exp(u))
    x1=x10+C*(primitive(q0)-primitive(qt)); x2=x1+dt
    H=lambda u:u*mp.tanh(u/2)/2-mp.log(mp.cosh(u/2))
    I1=(1+C*C)*(H(q0)-H(qt))/2
    I2=z0*z0*(1-mp.exp(-2*t))/4
    mt=norm([m[0]*mp.exp(-I1),m[1]*mp.exp(-I2)])
    return mt,(qt,x1,x2,z0*mp.exp(-t)),abs(elapsed(qt)-t)

def main(out):
    mp.mp.dps=80
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    for rec in json.loads((HERE/'SOURCE_BINDINGS.json').read_text())['readings']:
        actual=hashlib.sha256(Path(rec['path']).read_bytes()).hexdigest()
        check('source unchanged: '+rec['owner'],actual==rec['sha256'])

    # General exact algebraic identities.
    a,b,v,w=sp.symbols('a b v w')
    identity=(b*w-a*v)-((b-a)*(v+w)/2+(a+b)*(w-v)/2)
    check('endpoint-average product identity',sp.expand(identity)==0)
    z1,z2,scale=sp.symbols('z1 z2 scale')
    reciprocal_diff=1/p2(z1)-1/p2(z2)
    check('P2 explicit negative covariance factor',sp.factor(reciprocal_diff+(z1-z2)*(1+(z1+z2)/2)/(p2(z1)*p2(z2)))==0)
    r1,r2=sp.symbols('r1 r2',positive=True); r3=1-r1-r2
    J=sp.diag(r1,r2)-sp.Matrix([r1,r2])*sp.Matrix([[r1,r2]])
    inv=sp.diag(1/r1,1/r2)+sp.ones(2)/r3
    check('three-label Fisher logit inverse',sp.simplify(J*inv-sp.eye(2))==sp.zeros(2))
    h=sp.symbols('h',positive=True)
    gamma=(1-h/2)/(1+h/2)
    check('quadratic midpoint local order and nonzero cubic',sp.series(gamma-sp.exp(-h),h,0,4).removeO()==-h**3/12)
    c=(1+gamma**2)/4
    good=1/(1+p2(h*c))  # w=(1/2,1/2); V2=0
    bad=1/(1+p2(h*gamma**2/2))
    target=1/(1+sp.exp((1-sp.exp(-2*h))/4))
    goodseries=sp.series(good-target,h,0,4).removeO()
    badseries=sp.series(bad-target,h,0,3).removeO()
    check('whole quadratic P2 step local cubic',sp.expand(goodseries)==-sp.Rational(7,192)*h**3,str(goodseries))
    check('post-position loss remains first order',sp.expand(badseries)==h**2/8,str(badseries))
    b0,b1,c10,c11,c20,c21,alpha=sp.symbols('b0 b1 c10 c11 c20 c21 alpha')
    aa=lambda v,d:1/p2(alpha*h*(v+h*d/2-b0-h*b1))
    odds=sp.series(sp.log(aa(c10,c11)/aa(c20,c21)),h,0,3).removeO().expand()
    want=-alpha*h*(c10-c20)-alpha*h*h*(c11-c21)/2
    check('arbitrary baseline cancels through second order',sp.simplify(odds-want)==0)
    q,s,t=sp.symbols('q s t',real=True)
    check('Gonzalez scalar quartic exact chain rule',sp.expand((t-s)*(t**3+t*t*s+t*s*s+s**3)/4-(t**4-s**4)/4)==0)
    vv=sp.symbols('v',real=True)
    check('stationary point can have nonzero large-step root',sp.expand(vv+2*(-vv/2))==0 and -Q(1,2)<0,'phi=-x^2/2, u=0, h=2: every v is a root; v=1 strictly descends. Local branch qualification is required.')

    # A genuinely multidimensional Gonzalez correction, with an actual rational
    # Picard solve under the report's explicit contraction certificate.
    u=[Q(1),Q(1,2)]; hh=Q(1,32); radius=Q(1,2)
    M1,M2,M3,K0,K1=Q(8),Q(12),Q(12),Q(1),Q(0)
    D0=M1+M3*radius**2/24; LD=M2/2+M3*radius/6; qc=hh*(K1*D0/2+K0*LD)
    check('explicit multidimensional contraction certificate',hh*K0*D0<=radius and qc<1,{'Q_h':str(qc),'hK0D0':str(hh*K0*D0),'R':str(radius)})
    def radial_V(v): return sum(x*x for x in v)**2/4
    def radial_D(delta):
        mid=[a+b/2 for a,b in zip(u,delta)]; midsq=sum(a*a for a in mid); md=sum(a*b for a,b in zip(mid,delta))
        return [midsq*a+md*b/4 for a,b in zip(mid,delta)]
    delta=[Q(0),Q(0)]; eps=hh**3/100
    for it in range(1,13):
        dg=radial_D(delta); delta=[-hh*a for a in dg]
        dg=radial_D(delta); rho=[a+hh*b for a,b in zip(delta,dg)]
        res2=sum(a*a for a in rho); dg2=sum(a*a for a in dg)
        if sum(a*a for a in delta)>radius**2: raise RuntimeError('Picard left certified ball')
        if res2<=eps**2 and res2<=(hh/2)**2*dg2: break
    else: raise RuntimeError('certified radial solve failed')
    v=[a+b for a,b in zip(u,delta)]
    check('multidimensional Gonzalez chain identity',sum(a*b for a,b in zip(dg,delta))==radial_V(v)-radial_V(u))
    check('finite rational Picard accuracy and descent certificate',res2<=eps**2 and res2<=(hh/2)**2*dg2 and radial_V(v)<radial_V(u),{'iterations':it,'root_error_bound_at_most':str(eps/(1-qc))})

    # Entirely exact rational states, including finite approximate implicit solve.
    ww=[Q(1,5),Q(3,10),Q(1,2)]; xx=[Q(-2),Q(1,2),Q(3,2)]; audits=[Q(2),Q(1,3),Q(5)]
    for potential in ['quadratic','quartic']:
        hh=Q(1,16)
        wp,yp,cert=singleton_step(ww,xx,hh,potential)
        wa,ya,_=singleton_step(audit(ww,audits),xx,hh,potential)
        V=(lambda x:x*x/2) if potential=='quadratic' else (lambda x:x**4/4)
        check(potential+' exact audit square',wa==audit(wp,audits) and ya==yp)
        check(potential+' strictly positive normalized law',all(x>0 for x in wp) and sum(wp)==1)
        check(potential+' exact whole energy descent',sum(a*V(b) for a,b in zip(wp,yp))<sum(a*V(b) for a,b in zip(ww,xx)))
        for degree in range(7):
            coeff=[Q((j%3)-1,j+1) for j in range(degree+1)]
            pol=lambda x:sum(c*x**j for j,c in enumerate(coeff))
            sq=sum(a*pol(b)**2 for a,b in zip(wp,yp))
            check(potential+' represented-square control degree '+str(degree),sq>=0)
        if potential=='quartic':
            check('finite rational implicit-solve error certificates',all(c['error_bound']<=hh**3/200 for c in cert),{'bisections':[c['bisections'] for c in cert]})
    # A step depending on audited group/atom masses changes positions, defeating covariance.
    w=[Q(1,2),Q(1,2)]; x=[Q(1),Q(0)]; av=[Q(2),Q(1)]
    _,yp,_=singleton_step(w,x,w[0]/2)
    wa=audit(w,av); _,ya,_=singleton_step(wa,x,wa[0]/2)
    check('mass-dependent step audit counterexample',yp!=ya,{'before_audit_position':str(yp[0]),'after_audit_position':str(ya[0])})
    # P2 factor is decreasing and shift invariant if all retained catalogue entries remain.
    cc=[Q(-2),Q(0),Q(5)]; wp=mass_step(ww,cc,Q(7)); wq=mass_step(ww,[c+Q(13) for c in cc],Q(7))
    check('rational mass common-shift gauge',wp==wq)
    # Strong structure does not mean rank preservation or moving-law TV convergence.
    check('midpoint collision at finite step',quadratic_internal(Q(-1),Q(2))==quadratic_internal(Q(1),Q(2))==0)
    check('one Dirac exact and midpoint positions differ',sp.simplify(gamma-sp.exp(-h))!=0,'For every h in (0,2), log(gamma)<-h, so TV=1 between the two Diracs. The strict inequality is proved in the report.')

    # Genuine grouped benchmark: nonlinear conditional weights and moving interacting positions.
    m0=[mp.mpf('.4'),mp.mpf('.6')]; y0=tuple(map(mp.mpf,['.7','-.6','1.4','.9']))
    factors=[mp.mpf('3.2'),mp.mpf('.15')]
    for rule in ['p2','exponential']:
        for hh in map(mp.mpf,['.003125','.05','.5','10']):
            mn,yn,meta=grouped_step(m0,y0,hh,rule)
            ma,ya,other=grouped_step(audit(m0,factors),y0,hh,rule)
            err=max([abs(a-b) for a,b in zip(ma,audit(mn,factors))]+[abs(a-b) for a,b in zip(ya,yn)])
            check('grouped '+rule+' audit '+str(hh),err<mp.mpf('1e-70'),str(err),'numerical')
            check('grouped '+rule+' residual '+str(hh),meta['residual']<mp.mpf('1e-61'),str(meta['residual']),'numerical')
            check('grouped '+rule+' energy '+str(hh),meta['energy_change']<0 and meta['reaction_term']<=mp.mpf('1e-70') and meta['internal_term']<0,{k:mp.nstr(meta[k],12) for k in ['energy_change','reaction_term','internal_term']},'numerical')
            check('grouped '+rule+' positive interior '+str(hh),all(a>0 for a in mn) and 0<sigmoid(yn[0])<1,None,'numerical')
            check('grouped '+rule+' exact-product numerical residual '+str(hh),meta['energy_identity_error']<mp.mpf('1e-70'),str(meta['energy_identity_error']),'numerical')
            if rule=='exponential':
                jeff=sum((a-b)*mp.log(a/b) for a,b in zip(mn,m0))
                check('exponential Jeffreys budget '+str(hh),abs(meta['reaction_term']+jeff/hh)<mp.mpf('1e-70'),None,'numerical')
    T=mp.mpf('.5'); mt,yt,refres=reference(T,m0,y0)
    check('independent separated-variable reference time residual',refres<mp.mpf('1e-60'),str(refres),'numerical')
    convergence=[]
    for rule,endpoint in [('p2',False),('exponential',False),('p2',True)]:
        rows=[]
        for n in [8,16,32,64,128]:
            m=list(m0); y=y0; hh=T/n; max_res=mp.mpf('0'); max_increase=-mp.inf
            for _ in range(n):
                m,y,meta=grouped_step(m,y,hh,rule,endpoint)
                max_res=max(max_res,meta['residual']); max_increase=max(max_increase,meta['energy_change'])
            err=max(abs(a-b) for a,b in zip(list(m)+list(y),list(mt)+list(yt)))
            moment=sum(a*b for a,b in zip([m[0]*sigmoid(y[0]),m[0]*(1-sigmoid(y[0])),m[1]],[y[1],y[2],y[3]]))
            exactmoment=sum(a*b for a,b in zip([mt[0]*sigmoid(yt[0]),mt[0]*(1-sigmoid(yt[0])),mt[1]],[yt[1],yt[2],yt[3]]))
            rows.append({'n':n,'max_coordinate_error':mp.nstr(err,18),'group_mass_error':mp.nstr(abs(m[0]-mt[0]),18),'conditional_weight_error':mp.nstr(abs(sigmoid(y[0])-sigmoid(yt[0])),18),'first_moment_error':mp.nstr(abs(moment-exactmoment),18),'max_nonlinear_residual':mp.nstr(max_res,8),'maximum_step_energy_change':mp.nstr(max_increase,10)})
        errors=[mp.mpf(r['max_coordinate_error']) for r in rows]
        rates=[mp.log(errors[i]/errors[i+1],2) for i in range(len(errors)-1)]
        name=rule+('-endpoint-only-negative-control' if endpoint else '-endpoint-average')
        convergence.append({'method':name,'rows':rows,'observed_orders':[mp.nstr(r,12) for r in rates]})
        if not endpoint: check(name+' observed second order',all(r>mp.mpf('1.85') for r in rates[-2:]),[mp.nstr(r,9) for r in rates],'numerical diagnostic')
        else: check(name+' observed first-order boundary',mp.mpf('.85')<rates[-1]<mp.mpf('1.15'),[mp.nstr(r,9) for r in rates],'numerical diagnostic')
        if not endpoint:
            mass_errors=[mp.mpf(r['group_mass_error']) for r in rows]
            mass_rates=[mp.log(mass_errors[i]/mass_errors[i+1],2) for i in range(len(mass_errors)-1)]
            check(name+' group mass separately second order',all(r>mp.mpf('1.85') for r in mass_rates[-2:]),[mp.nstr(r,9) for r in mass_rates],'numerical diagnostic')
    # A full method can have order two in coordinates/TV on fixed support, but
    # only order one in W2 because mass transfer costs a square root.
    wf=1/(1+mp.e); fixed=[]
    for n in [16,32,64,128,256]:
        wn=1/(1+p2(mp.mpf(1)/n)**n); e=abs(wn-wf)
        fixed.append({'n':n,'weight_error':mp.nstr(e,18),'W2_error':mp.nstr(mp.sqrt(e),18)})
    rates=[mp.log(mp.mpf(fixed[i]['W2_error'])/mp.mpf(fixed[i+1]['W2_error']),2) for i in range(4)]
    check('fixed-support W2 only first order',mp.mpf('.97')<rates[-1]<mp.mpf('1.03'),{'rows':fixed,'observed_W2_orders':[mp.nstr(x,10) for x in rates]},'numerical diagnostic')
    # Full conditional weights moved, not the equal-conditional invariant subfamily.
    check('benchmark all state slots move',abs(yt[0]-y0[0])>.01 and all(abs(a-b)>.01 for a,b in zip(yt[1:],y0[1:])) and abs(mt[0]-m0[0])>.01,{'initial_r':mp.nstr(sigmoid(y0[0]),16),'final_r':mp.nstr(sigmoid(yt[0]),16),'initial_m':mp.nstr(m0[0],16),'final_m':mp.nstr(mt[0],16)},'numerical')
    # Solve root identity derivative, exact bracket uniqueness is in written proof.
    ss=sp.symbols('s',real=True); hh=sp.symbols('h',nonnegative=True)
    derivative=sp.diff(ss*(1+hh*(2+2*sp.cosh(ss))/2),ss)
    check('benchmark scalar solver derivative identity',sp.simplify(derivative-(1+hh*(1+sp.cosh(ss)+ss*sp.sinh(ss))))==0)
    payload={'status':'PASS','started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':platform.python_version(),'sympy':sp.__version__,'mpmath':mp.__version__,'mpmath_decimal_precision':mp.mp.dps,'checks':RESULTS,'convergence':convergence,'reference':{'time':str(T),'m':[mp.nstr(a,30) for a in mt],'state':[mp.nstr(a,30) for a in yt]},'limits':'Author mathematical controls and high-precision diagnostics, not independent review, interval certification of transcendental arithmetic, production integration, or a formal kernel proof.'}
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,indent=2)+'\n')
    print('PASS',len(RESULTS),'checks;',out)
    for row in convergence: print(row['method'],row['observed_orders'])

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True); args=p.parse_args()
    if args.output.exists(): raise SystemExit('Refusing to overwrite existing result')
    main(args.output)
