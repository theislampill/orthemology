#!/usr/bin/env python3
"""Exact deterministic controls for uniform skyline baseline moments.

The primary oracle below expands the geometric four-variable query integral
into rational polynomial integrals. It does not use the claimed harmonic
second/cross moment formulas. Finite controls supplement the written proof.
"""
from fractions import Fraction as F
from itertools import permutations
from math import comb, factorial
from pathlib import Path
import json
import mpmath as mp


def harmonic(n, power=1):
    return sum((F(1, j**power) for j in range(1, n+1)), F(0))


def product_polynomial_integral(n, moment=0):
    # Integral (xy)^moment (1-xy)^n dxdy, by finite expansion.
    return sum((F((-1)**j * comb(n, j), (j+moment+1)**2)
                for j in range(n+1)), F(0))


def incomparable_query_integral(n):
    # One orientation: p=(tu,s), q=(t,sv), Jacobian ts,
    # union lower-rectangle area ts(u+v-uv).
    # Inner integral is expanded independently, not replaced by harmonics.
    return sum((F((-1)**j*comb(n,j), (j+2)**2)
                * sum((F((-1)**r*comb(j,r),(r+1)**2)
                       for r in range(j+1)), F(0))
                for j in range(n+1)), F(0))


def exact_controls(n):
    h, h2 = harmonic(n), harmonic(n,2)
    m = n+1
    hm, gm = harmonic(m), harmonic(m,2)
    hp, gp = harmonic(m+1), harmonic(m+1,2)
    u1_geom = product_polynomial_integral(n)
    comp = product_polynomial_integral(n,1)
    inc = incomparable_query_integral(n)
    u2_geom = 2*(comp+inc)
    u2_claim = (hp*hp-gp+2*(hp-1))/((n+1)*(n+2))
    assert u1_geom == hm/m
    assert u2_geom == u2_claim
    assert 2*inc == (hp*hp-gp)/((n+1)*(n+2))
    ku_geom = F(0) if n==0 else n*(product_polynomial_integral(n-1,1)
                                          +2*incomparable_query_integral(n-1))
    ku_claim = (hm*hm-gm+hm-1)/m
    assert ku_geom == ku_claim
    k2 = h*h+h-h2
    cm2 = k2-2*m*ku_geom+m*m*u2_geom
    cn2 = k2-2*n*ku_geom+n*n*u2_geom
    delta = -2*hm/m+F(2,m*m)-(hm*hm-gm-4)/(m+1)-2*(hm+1)/(m+1)**2
    assert cm2 == h+delta
    assert h-m*u1_geom == -F(1,m)
    assert h-n*u1_geom == (hm-1)/m
    assert cm2 >= 0 and cn2 >= 0
    s1 = F(0) if n==0 else n*product_polynomial_integral(n-1,1)
    assert s1 == (hm-1)/m
    assert comp == (hp-1)/(m*(m+1))
    eq = (cm2-h)/(2*m*m)+2*(s1/m-comp)
    eq_claim = delta/(2*m*m)+2*((hm-1)/(m*m*(m+1))-F(1,m*(m+1)**2))
    assert eq == eq_claim
    # Deliberately wrong candidates should fail away from degenerate cases.
    if n >= 1:
        assert u2_geom != 2*inc, 'Omitting comparable pairs escaped control.'
        assert ku_geom != n*2*incomparable_query_integral(n-1), 'Subtracting both comparable orientations escaped control.'
        assert abs(delta) <= 11*hm*hm/m
    return {"n":n, "EU":str(u1_geom), "EU2":str(u2_geom), "EKU":str(ku_geom),
            "EK2":str(k2), "E_compensated_n_squared":str(cn2),
            "E_compensated_m_squared":str(cm2), "E_Q":str(eq),
            "comparable_one_orientation":str(comp),
            "incomparable_one_orientation":str(inc)}


def record_permutation_controls(N):
    sum_k = sum_k2 = sum_fact2 = 0
    for p in permutations(range(N)):
        low = N
        k = 0
        for y in p:
            if y < low:
                low = y
                k += 1
        sum_k += k
        sum_k2 += k*k
        sum_fact2 += k*(k-1)
    h, h2 = harmonic(N), harmonic(N,2)
    assert F(sum_k,factorial(N)) == h
    assert F(sum_k2,factorial(N)) == h*h+h-h2
    assert F(sum_fact2,factorial(N)) == h*h-h2
    return {"N":N,"permutations":factorial(N),"factorial_second_moment":str(F(sum_fact2,factorial(N)))}


def numerical_scaling(n):
    m=mp.mpf(n+1)
    h=mp.digamma(m+1)+mp.euler
    g=mp.zeta(2)-mp.polygamma(1,m+1)
    hn=h-1/m
    delta=-2*h/m+2/m**2-(h*h-g-4)/(m+1)-2*(h+1)/(m+1)**2
    cm2=hn+delta
    eq=delta/(2*m*m)+2*((h-1)/(m*m*(m+1))-1/(m*(m+1)**2))
    return {"n":n,"H_n":mp.nstr(hn,30),"E_Cm_squared":mp.nstr(cm2,30),
            "E_Cm_squared_over_Hn":mp.nstr(cm2/hn,30),
            "E_Q":mp.nstr(eq,30),"E_Q_times_m3_over_Hm2":mp.nstr(eq*m**3/h**2,30)}


def main():
    mp.mp.dps=70
    exact=[exact_controls(n) for n in range(33)]
    records=[record_permutation_controls(N) for N in range(1,9)]
    assert exact[0]["EU2"] == "1"
    assert exact[1]["EU2"] == "11/18"
    assert exact[1]["EKU"] == "3/4"
    assert exact[1]["E_compensated_m_squared"] == "4/9"
    # Independent one-dimensional high-precision quadrature for product moments.
    quadrature=[]
    for n in [0,1,2,5,20]:
        for power in [0,1]:
            value=mp.quad(lambda z: -mp.log(z)*z**power*(1-z)**n,[0,mp.mpf('0.5'),1])
            expected=product_polynomial_integral(n,power)
            target=mp.mpf(expected.numerator)/expected.denominator
            error=abs(value-target)
            assert error < mp.mpf('1e-60')
            quadrature.append({"n":n,"moment":power,"value":mp.nstr(value,40),"absolute_error":mp.nstr(error,6)})
    result={"status":"PASS","exact_geometric_n_range":[0,32],
            "exact_geometric_controls":exact,"record_permutation_controls":records,
            "quadrature_controls":quadrature,
            "numerical_scaling":[numerical_scaling(n) for n in [1,2,10,100,1000,1000000,1000000000000]],
            "negative_controls":["Omitting both comparable contributions rejected for every n=1..32",
                                 "Subtracting both comparable orientations in EKU rejected for every n=1..32"],
            "limits":"Exact rational and deterministic numerical controls, not random data, a formal proof, or a rigorous numerical error certificate."}
    out=Path(__file__).with_name('CONTROL_RESULTS.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: exact geometric controls n=0..32; all permutations N=1..8; 10 product quadratures; 7 scaling controls.')
    for n in [0,1,2,3,8,32]:
        row=exact[n]
        print({k:row[k] for k in ['n','EU2','EKU','E_compensated_m_squared','E_Q']})

if __name__=='__main__':
    main()
