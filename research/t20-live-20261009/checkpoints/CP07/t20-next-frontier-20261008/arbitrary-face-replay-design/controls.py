#!/usr/bin/env python3
"""Proof supplements, not empirical sampling or a global optimization oracle."""
from fractions import Fraction as F
from pathlib import Path
import json
import mpmath as mp

HERE = Path(__file__).resolve().parent


def root_interval(q, k, bits=160):
    lo, hi = F(0), max(F(1), q)
    for _ in range(bits):
        mid = (lo + hi) / 2
        if mid**k <= q:
            lo = mid
        else:
            hi = mid
    assert lo**k <= q <= hi**k
    return lo, hi


def stable(n, u_string, v_string, dps):
    with mp.workdps(dps):
        u, v = mp.mpf(u_string), mp.mpf(v_string)
        if u < v:
            u, v = v, u
        c = mp.mpf(n) / (n + 1)
        # x<=y. Avoid x^c+y^c-z^c subtraction at unequal tiny rates.
        logx, logy = -u/n, -v/n
        b = -mp.expm1(logy)
        h = mp.exp(logx-logy)*b
        term = mp.exp(c*(logy-logx)+mp.log(mp.expm1(c*mp.log1p(h))))
        assert 0 < term < 1
        logS = c*logx + mp.log1p(-term)
        L = (n+1)*logS + u + v
        assert L > 0
        logDelta = -u-v + mp.log(mp.expm1(L))
        logchi = 2*logDelta+u+v-mp.log(-mp.expm1(-u))-mp.log(-mp.expm1(-v))
        chi = mp.exp(logchi)
        a = -mp.expm1(-u/n)
        bb = -mp.expm1(-v/n)
        if max(a, bb) <= mp.mpf('0.5'):
            fu = u*u/mp.expm1(u)
            fv = v*v/mp.expm1(v)
            assert n**4*chi <= 16*mp.e**2*fu*fv*(1+mp.mpf('1e-50'))
        else:
            assert chi <= 4*(mp.mpf(11)/12)**(2*n)*(1+mp.mpf('1e-50'))
        assert n**4*chi <= 32768
        return +chi


def run():
    report = {"scope": "Exact rational interval controls and high-precision formula checks; no empirical samples, no exhaustive rate search"}
    exact_cases = 0
    ps = [F(1,10), F(1,2), F(3,4), F(9,10), F(99,100), F(999,1000)]
    for n in [1,2,3,5,10]:
        m, c = n+1, F(n,n+1)
        for p in ps:
            for q in ps:
                x, y = p**m, q**m
                X, Y = p**n, q**n
                a, b = 1-x, 1-y
                A, B = x**n, y**n
                z = x+y-x*y
                zl, zu = root_interval(z**n,m)
                sl, su = X+Y-zu, X+Y-zl
                gl, gu = sl-X*Y, su-X*Y
                assert gl > 0
                integral_upper = c*(1-c)*a*b*X*Y/(x*y)
                assert gu <= integral_upper
                assert gu*gu <= 4*(1-c)**2*X*Y*a*b
                # Comparison with c=1/2, raised to integer powers exactly.
                W = X*X+Y*Y-X*X*Y*Y
                assert z**(2*n) >= W**m
                if max(a,b) > F(1,2):
                    assert su*su <= F(121,144)*X*Y
                dl, du = sl**m-A*B, su**m-A*B
                assert dl > 0
                chi_upper = du*du/(A*(1-A)*B*(1-B))
                assert chi_upper*n**4 < 32768
                exact_cases += 1
    report["rational_algebraic_pair_cases"] = exact_cases

    series_cases = 0
    for c in [F(1,2),F(2,3),F(5,6),F(10,11)]:
        masses, p = [], c
        for k in range(1,65):
            assert p > 0
            masses.append(p)
            p *= F(k-c,k+1)
        total = sum(masses)
        assert 0 < total < 1
        for a in [F(1,10),F(1,2),F(9,10)]:
            hl, hu = root_interval((1-a)**c.numerator,c.denominator,bits=400)
            approx = sum(pk*a**(k+1) for k,pk in enumerate(masses))
            # H_c(a)=1-(1-a)^c, with remaining probability-mass tail bound.
            assert approx <= 1-hu
            assert 1-hl <= approx+(1-total)*a**65
            series_cases += 1
    report["positive_series_enclosure_cases"] = series_cases

    boundary_cases = 0
    for n in [1,2,10,100]:
        for r in [F(0),F(1,3),F(1)]:
            for a,b in [(F(0),r),(F(1),r),(r,F(0)),(r,F(1))]:
                A,B=(1-a)**n,(1-b)**n
                if a==0: J=B
                elif b==0: J=A
                else: J=F(0)
                assert J == A*B
                assert sum([J,A-J,B-J,1-A-B+J])==1
                boundary_cases += 1
    report["literal_boundary_equal_law_cases"] = boundary_cases

    def exp_interval(t, terms=40):
        s, term = F(1), F(1)
        for k in range(1,terms+1):
            term *= t/k
            s += term
        nxt=term*t/(terms+1)
        return s, s+nxt/(1-t/F(terms+2))
    ul, uu = F(159362,100000), F(159363,100000)
    elo,ehi=exp_interval(ul)
    assert (2-ul)*elo-2 > 0
    elo,ehi=exp_interval(uu)
    assert (2-uu)*ehi-2 < 0
    report["certified_u_star_bracket"]=[str(ul),str(uu)]
    report["certified_limit_constant_bracket"]=[str((uu*(2-uu))**2),str((ul*(2-ul))**2)]

    identity_cases=0
    for A in [F(1,10),F(1,3),F(1,2),F(9,10)]:
        for B in [F(1,7),F(1,2),F(4,5)]:
            D=A*(1-A)*B*(1-B)/2
            p0=[A*B,A*(1-B),(1-A)*B,(1-A)*(1-B)]
            p1=[p+d for p,d in zip(p0,[D,-D,-D,D])]
            assert all(p>0 for p in p1)
            assert sum((q-p)**2/p for p,q in zip(p0,p1))==D*D/(A*(1-A)*B*(1-B))
            identity_cases+=1
    report["exact_four_cell_identity_cases"]=identity_cases

    mp.mp.dps=80
    grid=[mp.nstr(mp.power(10,mp.mpf(k)/2),70) for k in range(-8,9)]
    scan=[]
    checks=0
    for n in [1,2,5,10,50,1000]:
        best=(mp.mpf(0),None,None)
        for u in grid:
            for v in grid:
                ch80=stable(n,u,v,80)
                ch160=stable(n,u,v,160)
                assert abs(ch80/ch160-1)<mp.mpf('1e-50')
                checks += 1
                if ch160>best[0]:best=(ch160,u,v)
        scan.append({"n":n,"largest_grid_n4_chi":mp.nstr(n**4*best[0],30),"u":best[1],"v":best[2]})
    # Asymmetric and tiny-rate cases outside a modest plotted grid.
    for n in [1,10,1000,1000000]:
        for u,v in [('1000000','0.000000000001'),('0.000000000001','1'),('1000','1'),('1.59362426004','1.59362426004')]:
            a=stable(n,u,v,80);b=stable(n,u,v,160)
            assert abs(a/b-1)<mp.mpf('1e-45')
            checks+=1
    report["high_precision_80_160_agreement_cases"]=checks
    report["exploratory_log_grid_only"]=scan
    # Preserve a genuine cancellation failure of the naive direct formula.
    with mp.workdps(80):
        x,y=mp.exp(-1000),mp.exp(-1)
        direct=mp.sqrt(x)+mp.sqrt(y)-mp.sqrt(x+y-x*y)
        stable_chi=stable(1,'1000','1',160)
        assert direct==0 and stable_chi>0
        report["negative_naive_80_digit_control"]={"n":1,"u":1000,"v":1,"naive_S":"0","stable_positive_chi":mp.nstr(stable_chi,30)}
    ustar=mp.findroot(lambda u:u-2*(-mp.expm1(-u)),mp.mpf('1.6'))
    f=lambda u:u*u/mp.expm1(u)
    report["asymptotic_characterization_evaluations"]={"u_star":mp.nstr(ustar,50),"constant":mp.nstr(f(ustar)**2,50),"old_t_constant":mp.nstr(f(mp.mpf(1)/3)**2,50),"information_ratio":mp.nstr((f(ustar)/f(mp.mpf(1)/3))**2,50)}
    report["fixed_u_star_convergence"]=[{"n":n,"n4_chi":mp.nstr(n**4*stable(n,str(ustar),str(ustar),160),35)} for n in [10,100,1000,10000,1000000]]
    kl_checks=[]
    for n in [10,100,1000,10000,1000000]:
        with mp.workdps(160):
            u=mp.mpf(str(ustar)); x=mp.exp(-u/n);c=mp.mpf(n)/(n+1)
            A=mp.exp(-u);S=2*x**c-(2*x-x*x)**c;D=S**(n+1)-A*A
            ps=[A*A,A*(1-A),A*(1-A),(1-A)**2]
            rs=[d/p for d,p in zip([D,-D,-D,D],ps)]
            kl=sum(p*((1+r)*mp.log1p(r)-r) for p,r in zip(ps,rs))
            chi=D*D/(A*A*(1-A)**2)
            assert 0<kl<chi
            assert abs(chi/stable(n,str(u),str(u),160)-1)<mp.mpf('1e-100')
            kl_checks.append({"n":n,"n4_kl":mp.nstr(n**4*kl,35),"kl_over_chi":mp.nstr(kl/chi,35)})
    report["fixed_u_star_kl_convergence"]=kl_checks
    report["status"]="PASS"
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__=="__main__":run()
