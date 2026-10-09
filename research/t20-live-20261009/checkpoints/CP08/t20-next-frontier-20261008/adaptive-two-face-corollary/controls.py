#!/usr/bin/env python3
"""Exact algebraic controls; artificial rational channels are labeled as such."""
from fractions import Fraction as F
import json
import mpmath as mp

def chi(p,q):
    assert set(q)<=set(p)
    return sum((q[k]-v)**2/v for k,v in p.items() if v)

def main():
    counts=0
    for A in [F(1,5),F(1,2),F(4,5)]:
        Bs=[F(1,4),F(3,5),F(9,10)]
        Ds=[min(A*(1-B),(1-A)*B)/2 for B in Bs]
        ds=[D*D/(A*(1-A)*B*(1-B)) for B,D in zip(Bs,Ds)]
        # Branch kernels include deterministic, random, and aborting policies.
        mus=[[F(1),F(0),F(0),F(0)], [F(0),F(1),F(0),F(0)],
             [F(1,3),F(1,3),F(1,3),F(0)], [F(1,4),F(1,4),F(1,4),F(1,4)],
             [F(0),F(0),F(0),F(1)]]
        for mu0 in mus:
            for mu1 in mus:
                p,q={},{}
                for X,px,mu in [(0,1-A,mu0),(1,A,mu1)]:
                    for j,w in enumerate(mu):
                        if not w: continue
                        if j==3:
                            p[X,j,None]=q[X,j,None]=px*w
                            continue
                        B,D=Bs[j],Ds[j]
                        B1=B+(D/A if X else -D/(1-A))
                        for Y in [0,1]:
                            p[X,j,Y]=px*w*(B if Y else 1-B)
                            q[X,j,Y]=px*w*(B1 if Y else 1-B1)
                assert sum(p.values())==sum(q.values())==1
                expected=(1-A)*sum(w*d for w,d in zip(mu1,ds))+A*sum(w*d for w,d in zip(mu0,ds))
                assert chi(p,q)==expected<=max(ds)
                counts+=1
    # These rational tables check the algebra, not actual Joe thresholds.
    # Actual Joe conditional identity and screening limit, high precision only.
    mp.mp.dps=100
    actual=[]
    for n in [1,2,5,10,100]:
        c=mp.mpf(n)/(n+1)
        a=-mp.expm1(-mp.mpf('1.3')/n);A=(1-a)**n
        vals=[]
        for v in ['0.7','2.1']:
            b=-mp.expm1(-mp.mpf(v)/n);B=(1-b)**n
            S=(1-a)**c+(1-b)**c-(1-a*b)**c
            D=S**(n+1)-A*B
            d=D*D/(A*(1-A)*B*(1-B))
            vals.append((B,D,d))
        adaptive=A*(vals[1][1]/A)**2/(vals[1][0]*(1-vals[1][0]))+(1-A)*(vals[0][1]/(1-A))**2/(vals[0][0]*(1-vals[0][0]))
        expected=(1-A)*vals[1][2]+A*vals[0][2]
        assert abs(adaptive-expected)<mp.mpf('1e-90')
        assert adaptive<=max(z[2] for z in vals)
        actual.append({'n':n,'n4_adaptive_chi':mp.nstr(n**4*adaptive,25)})
    screening=[]
    for n in [1,2,5,10]:
        c=mp.mpf(n)/(n+1);y=mp.power(2,-mp.mpf(1)/n)
        # Logarithmic stable S with x<<y; avoids direct cancellation.
        x=mp.power(10,-10*(n+1))
        term=mp.exp(c*(mp.log(y)-mp.log(x)))*mp.expm1(c*mp.log1p(x*(1-y)/y))
        ratio=mp.exp((n+1)*mp.log1p(-term))
        assert mp.mpf('0.75')<ratio<1
        screening.append({'n':n,'Joe_selected_absence':mp.nstr(ratio,25),'reference_selected_absence':'0.5','expected_first_probes_per_completion_log10':10*n*(n+1)})
    print(json.dumps({'status':'PASS','exact_rational_channel_cases':counts,'rational_scope':'Algebraic proxies, not claims that these rational tables are the Joe model','actual_Joe_checks':actual,'free_screening_negative_controls':screening,'scope':'Proof supplements only; no samples or global optimization'},indent=2))

if __name__=='__main__':main()
