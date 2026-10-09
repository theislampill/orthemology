#!/usr/bin/env python3
"""Independent targeted controls; these numerical checks do not prove continua."""
from pathlib import Path
from fractions import Fraction
import json
import math
import mpmath as mp
import sympy as sp

mp.mp.dps = 150
ROOT = Path(__file__).resolve().parent
checks = []

def record(name, ok, detail):
    checks.append(dict(name=name, passed=bool(ok), detail=detail))
    if not ok:
        raise AssertionError(name + ': ' + str(detail))

def s(v):
    return mp.nstr(v, 28)

def law(n, a, b):
    a,b=mp.mpf(a),mp.mpf(b)
    m=n+1; c=mp.mpf(n)/m
    A=(1-a)**n; B=(1-b)**n
    p=[A*B,A*(1-B),(1-A)*B,(1-A)*(1-B)]
    if a in (0,1) or b in (0,1):
        return p,p,mp.mpf(0),mp.mpf(0)
    X=(1-a)**c;Y=(1-b)**c
    S=X+Y-(1-a*b)**c
    delta=S**m-(X*Y)**m
    q=[p[0]+delta,p[1]-delta,p[2]-delta,p[3]+delta]
    chi=delta**2/(A*(1-A)*B*(1-B))
    kl=sum(qi*mp.log(qi/pi) for pi,qi in zip(p,q) if qi)
    return p,q,chi,kl

def f(u):
    return u*u/mp.expm1(u)

def main():
    # Exact identity, independently obtained by summing the four cells.
    A,B,D=sp.symbols('A B D', nonzero=True)
    cells=[A*B,A*(1-B),(1-A)*B,(1-A)*(1-B)]
    residual=sp.factor(sum(D*D/pi for pi in cells)-D*D/(A*(1-A)*B*(1-B)))
    record('symbolic_four_cell_chi_identity',residual==0,str(residual))

    # Exact positive rational Sibuya coefficients, with a rigorous residual
    # interval for the bounded PGF. Decimal evaluations only locate the known
    # algebraic transform inside these rational enclosures.
    mixture=[]
    for nc in (1,2,10):
        c=Fraction(nc,nc+1); p=c; coeff=[]
        for k in range(1,101):
            coeff.append(p)
            p=p*Fraction(k-c,k+1)
        tail=1-sum(coeff)
        ok=all(x>0 for x in coeff) and tail>0
        maximum=mp.mpf(0)
        for z in (Fraction(1,3),Fraction(2,5),Fraction(2,15)):
            partial=sum(pk*z**k for k,pk in enumerate(coeff,1))
            error=tail*z**101
            conv=lambda x:mp.mpf(x.numerator)/x.denominator
            exact=1-(1-conv(z))**conv(c)
            ok=ok and conv(partial)<=exact<=conv(partial+error)
            maximum=max(maximum,conv(error))
        mixture.append(dict(n=nc,tail_mass=s(conv(tail)),maximum_pgf_error_bound=s(maximum)))
        record('bounded_sibuya_pgf_'+str(nc),ok,mixture[-1])

    # All-rate and intermediate envelopes on intentionally asymmetric grids.
    # Keep values safely above the chosen numerical precision floor.
    grid=[mp.mpf('1e-30'),mp.mpf('1e-12'),mp.mpf('1e-5'),mp.mpf('.01'),mp.mpf('.17'),mp.mpf('.5'),mp.mpf('.50001'),mp.mpf('.9'),1-mp.mpf('1e-12'),1-mp.mpf('1e-30')]
    count=0; largest_scaled=mp.mpf(0); min_cell=mp.mpf(1)
    max_ratios={k:mp.mpf(0) for k in ('central','tail','mixture_covariance','comparison')}
    for n in (1,2,3,10,24,100,1000):
        m=n+1;c=mp.mpf(n)/m
        for a in grid:
            for b in grid:
                p,q,chi,kl=law(n,a,b)
                # Tiny KL can lose absolute accuracy through cancellation.
                tol=mp.mpf('1e-130')
                ok=min(q)>0 and abs(sum(q)-1)<tol and abs(q[0]+q[1]-(1-a)**n)<tol
                ok=ok and chi<=mp.mpf(32768)/n**4 and kl<=chi+tol and kl>=-tol
                record_detail=False
                if not ok:
                    record('interior_grid_failure',False,dict(n=n,a=s(a),b=s(b),chi=s(chi),kl=s(kl),minimum_cell=s(min(q))))
                count+=1;largest_scaled=max(largest_scaled,n**4*chi);min_cell=min(min_cell,min(q))
                X=(1-a)**c;Y=(1-b)**c;S=X+Y-(1-a*b)**c;g=S-X*Y
                var_bound=2*(1-c)*mp.sqrt(X*Y*a*b)
                max_ratios['mixture_covariance']=max(max_ratios['mixture_covariance'],g/var_bound)
                half_bound=X+Y-mp.sqrt(X*X+Y*Y-X*X*Y*Y)
                max_ratios['comparison']=max(max_ratios['comparison'],S/half_bound)
                if a<=mp.mpf('.5') and b<=mp.mpf('.5'):
                    u=-n*mp.log1p(-a);v=-n*mp.log1p(-b)
                    ratio=n**4*chi/(16*mp.e**2*f(u)*f(v))
                    max_ratios['central']=max(max_ratios['central'],ratio)
                else:
                    # Compare at the root level to avoid a tiny-probability
                    # underflow masking the tail contraction.
                    ratio=(S/mp.sqrt(X*Y))/(mp.mpf(11)/12)
                    max_ratios['tail']=max(max_ratios['tail'],ratio)
    record('asymmetric_interior_grid',True,dict(count=count,max_scaled_chi=s(largest_scaled),min_cell=s(min_cell)))
    record('all_intermediate_envelopes',all(v<=1+mp.mpf('1e-120') for v in max_ratios.values()),{k:s(v) for k,v in max_ratios.items()})

    literal=0
    for n in (1,2,10,100):
        for a,b in ((0,'.2'),(1,'.2'),('.2',0),('.2',1),(0,0),(0,1),(1,0),(1,1)):
            p,q,chi,kl=law(n,a,b)
            record('literal_boundary_'+str(literal),p==q and chi==kl==0,dict(n=n,a=str(a),b=str(b)))
            literal+=1
    high=[]
    for n in (1,2,5,20):
        c=mp.mpf(n)/(n+1);target=(2-2**c)**(2*(n+1))
        eps=mp.mpf('1e-45')
        chi=law(n,1-eps,1-eps)[2]
        rel=abs(chi/target-1)
        high.append(dict(n=n,limit=s(target),relative_error=s(rel)))
    record('high_rate_interior_limit',all(mp.mpf(d['relative_error'])<mp.mpf('1e-20') for d in high),high)

    # Compact and escaping designs. No finite grid is used as a global proof.
    ustar=mp.findroot(lambda u:2*(-mp.expm1(-u))-u,(1,2))
    optimum=f(ustar)**2; old=f(mp.mpf(1)/3)**2
    record('asymptotic_constants',abs(ustar-mp.mpf('1.5936242600400400923'))<mp.mpf('1e-19') and abs(optimum-mp.mpf('.4193990202224225571'))<mp.mpf('1e-19'),dict(ustar=s(ustar),optimum=s(optimum),old=s(old),ratio=s(optimum/old)))
    local=[]
    for n in (100,1000,10000,100000):
        errs=[]; klerrs=[]
        for u in (mp.mpf('.1'),mp.mpf('.8'),ustar,mp.mpf('4')):
            for v in (mp.mpf('.2'),ustar,mp.mpf('3')):
                a=-mp.expm1(-u/n);b=-mp.expm1(-v/n)
                p,q,chi,kl=law(n,a,b)
                errs.append(abs(n**4*chi/(f(u)*f(v))-1))
                klerrs.append(abs(n**4*kl/(f(u)*f(v)/2)-1))
        a=-mp.expm1(-ustar/n);chi=law(n,a,a)[2];kl=law(n,a,a)[3]
        local.append(dict(n=n,max_relative_grid_error=s(max(errs)),max_relative_kl_grid_error=s(max(klerrs)),scaled_at_star=s(n**4*chi),scaled_kl_at_star=s(n**4*kl),kl_over_chi=s(kl/chi)))
    record('compact_asymptotics',mp.mpf(local[-1]['max_relative_grid_error'])<mp.mpf('.0001') and mp.mpf(local[-1]['max_relative_kl_grid_error'])<mp.mpf('.0001') and abs(mp.mpf(local[-1]['kl_over_chi'])-mp.mpf('.5'))<mp.mpf('1e-8'),local)
    escaping=[]
    for n in (100,1000,10000):
        cases={'u_down':(mp.mpf(1)/n,ustar),'u_up':(mp.sqrt(n),ustar),'both_asymmetric':(mp.mpf(1)/n,mp.sqrt(n)),'central_edge':(n*mp.log(2),ustar),'outside_central':(-n*mp.log(mp.mpf('.25')),ustar)}
        row={'n':n}
        for name,(u,v) in cases.items():
            _,_,chi,kl=law(n,-mp.expm1(-u/n),-mp.expm1(-v/n))
            row[name]=s(n**4*chi)
            row[name+'_kl']=s(n**4*kl)
        escaping.append(row)
    record('escaping_design_evaluations',all(mp.mpf(escaping[-1][k])<mp.mpf('.0001') for k in escaping[-1] if k!='n'),escaping)

    # A finite-history randomized common policy. Rates depend on earlier
    # outcomes, pair outcomes are atomic, and fresh endpoints remain equal.
    n=3
    leaves=[]; ledger=mp.mpf(0); expected_pairs=mp.mpf(0)
    def traverse(depth,hist,w0,w1,cost):
        nonlocal ledger,expected_pairs
        if depth==3:
            reject=sum(hist)%2==1
            leaves.append((w0,w1,cost,reject));return
        # Exact common randomization into a rate pair or a fresh endpoint.
        z=sum(hist)
        pair_rates=[(mp.mpf('.2'),mp.mpf('.7')),(mp.mpf('.001'),mp.mpf('.4')),(0,mp.mpf('.8')),(mp.mpf('.8'),mp.mpf('.05'))]
        a,b=pair_rates[z%4]
        p,q,chi,kl=law(n,a,b)
        ledger+=w1*mp.mpf('.7')*kl
        expected_pairs+=w1*mp.mpf('.7')
        for k,(pi,qi) in enumerate(zip(p,q)):
            if pi or qi:
                traverse(depth+1,hist+(k,),w0*mp.mpf('.7')*pi,w1*mp.mpf('.7')*qi,cost+1)
        fresh=(1-mp.mpf('.2')*mp.mpf('.3'))**n
        for k,pi in enumerate((fresh,1-fresh)):
            traverse(depth+1,hist+(k+4,),w0*mp.mpf('.3')*pi,w1*mp.mpf('.3')*pi,cost)
    traverse(0,(),mp.mpf(1),mp.mpf(1),0)
    direct=sum(w1*mp.log(w1/w0) for w0,w1,_,_ in leaves if w1)
    e_cost=sum(w1*cost for _,w1,cost,_ in leaves)
    r0=sum(w0 for w0,_,_,r in leaves if r);r1=sum(w1 for _,w1,_,r in leaves if r)
    binary=r1*mp.log(r1/r0)+(1-r1)*mp.log((1-r1)/(1-r0))
    record('adaptive_finite_prefix',abs(direct-ledger)<mp.mpf('1e-130') and abs(e_cost-expected_pairs)<mp.mpf('1e-130') and binary<=direct and direct<=mp.mpf(32768)/n**4*e_cost,dict(leaves=len(leaves),direct_kl=s(direct),conditional_kl_sum=s(ledger),expected_pairs=s(e_cost),binary_kl=s(binary)))

    # Deliberate invalid-method controls retained, not counted as theorem
    # failures. Naive subtraction loses a small positive dependence signal.
    failed=[]
    for nf in (1000000,100000000):
        af=1-math.exp(-float(ustar)/nf);cf=nf/(nf+1)
        xf=1-af;Sf=xf**cf+xf**cf-(1-af*af)**cf
        df=Sf**(nf+1)-(xf*xf)**nf
        pref=(xf**nf)**2*(1-xf**nf)**2
        naive=nf**4*df*df/pref
        a=-mp.expm1(-ustar/nf);good=nf**4*law(nf,a,a)[2]
        failed.append(dict(name='binary64_direct_subtraction',n=nf,naive_scaled_chi=naive,high_precision_scaled_chi=s(good),relative_error=s(abs(mp.mpf(naive)/good-1)),expected='This method is not accepted as a proof or accurate tail computation.'))
    wrong_boundary=dict(name='boundary_continuity_assumption',literal=0,interior_limit=s((2-mp.sqrt(2))**4),expected='Strictly positive interior limit contradicts boundary continuity.')
    failed.append(wrong_boundary)
    out=dict(precision_decimal_digits=mp.mp.dps,checks=checks,retained_failed_methods=failed,scope='Finite numerical controls and symbolic cell identity only. Analytic review supplies continuum, tail, and stopping arguments.')
    (ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(passed=len(checks),failed_theorem_checks=0,retained_failed_methods=failed),indent=2))

if __name__=='__main__':
    try:
        main()
    except BaseException as exc:
        (ROOT/'CONTROL_FAILURE.json').write_text(json.dumps(dict(error=repr(exc),completed_checks=checks),indent=2)+'\n')
        raise
