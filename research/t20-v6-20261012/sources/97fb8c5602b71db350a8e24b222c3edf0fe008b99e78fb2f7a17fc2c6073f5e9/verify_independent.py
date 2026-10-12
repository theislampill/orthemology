"""Finite exact controls supplementary to the ordinary independent proof.

These checks do not establish halting undecidability, infinite divergence,
general Type-2 termination, or a formal-kernel theorem.
"""
from fractions import Fraction as F
from math import comb, factorial
import json

groups = []

def check(name, body):
    count = body()
    groups.append({"group": name, "checks": count, "passed": True})

def geometric_ratios():
    count = 0
    for r in range(41):
        K = max(1, 2*r)
        first = F(factorial(r+K), factorial(K) * 2**K)
        tail = F(0)
        for k in range(K, K+80):
            assert F(r+k+1, 2*(k+1)) <= F(3, 4)
            tail += F(factorial(r+k), factorial(k) * 2**k)
            assert tail <= 4*first
            count += 2
    return count

def finite_stronger_family():
    # a=log(2) makes all finite exponential weights exactly rational.
    count = 0
    for j in range(2, 65):
        damp = F(1, 2**j)
        D = F(j-1, j) + damp/j
        p = damp/(j*D)
        Z = (1-p) + p*2**j
        assert F(1, 2) <= D <= 1
        assert Z == 1/D and 1 <= Z <= 2
        assert Z-1 <= F(1, j-1)
        assert p*2**j/Z == F(1, j)
        assert (1-p)/Z == F(j-1, j)
        count += 5
        for r in range(1, 12):
            assert p*j**r <= 2*j**(r-1)*damp
            assert p*2**j*j**r/Z == j**(r-1)
            count += 2
    return count

def finite_event_model():
    count = 0
    for mask in range(128):
        weights = []
        for e in range(7):
            if mask & (1 << e):
                t = e*e+1
                pair = (e+t)*(e+t+1)//2+t
                j = pair+1
                assert j >= t and j >= 1
                weights.append((F(1, 4**(e+1)), j))
                count += 1
        P = sum((w/F(2**j) for w,j in weights), F(0))
        alpha = sum((w for w,j in weights), F(0))
        p0 = 1-P
        Z = p0+alpha
        assert p0 >= F(2, 3)
        assert 1 <= Z <= F(4, 3)
        assert p0/(p0/Z) == Z
        count += 3
    for e in range(50):
        w = F(1, 4**(e+1))
        exact_later_total = w/3
        threshold = 2*w/3
        assert exact_later_total+w/12 < threshold < w-w/12
        count += 1
    return count

def tilt_composition():
    law = {0: F(1,2), 1: F(1,3), 3: F(1,6)}
    def tilt(p, k):
        weighted = {x: mass*F(2)**(-k*x) for x,mass in p.items()}
        Z = sum(weighted.values())
        return {x: mass/Z for x,mass in weighted.items()}, Z
    count = 0
    for i in range(-5,6):
        for j in range(-5,6):
            p1,z1 = tilt(law,i)
            p2,z2 = tilt(p1,j)
            direct,z = tilt(law,i+j)
            assert p2 == direct and z1*z2 == z
            assert sum(p2.values()) == 1
            count += 2
    return count

def quotient_error():
    count = 0
    for n in [F(0), F(1,7), F(5,3), F(30)]:
        K = max(F(1), n)
        for z in [F(1,19), F(2,3), F(5)]:
            D = z/2
            eta = D/8
            for sn in [-1,1]:
                for sz in [-1,1]:
                    nhat,zhat = n+sn*eta,z+sz*eta
                    actual = abs(nhat/zhat-n/z)
                    assert zhat >= D/2
                    assert actual <= 2*eta/D+2*K*eta/D**2
                    count += 2
    return count

def bernstein_variance():
    count = 0
    for N in range(1,26):
        for l in range(8):
            p = F(l,7)
            probs = [F(comb(N,k))*p**k*(1-p)**(N-k) for k in range(N+1)]
            variance = sum((mass*(F(k,N)-p)**2 for k,mass in enumerate(probs)),F(0))
            assert sum(probs) == 1
            assert variance == p*(1-p)/N <= F(1,4*N)
            count += 2
    return count

for name,body in [
    ("unnormalized factorial-tail ratio and partial-tail majorant",geometric_ratios),
    ("finite-support endpoint family exact normalization and moments",finite_stronger_family),
    ("finite event models and halting-digit separation gap",finite_event_model),
    ("finite exact normalized-tilt composition",tilt_composition),
    ("normalized quotient-error bound",quotient_error),
    ("Bernstein binomial-variance control",bernstein_variance),
]:
    check(name,body)

print(json.dumps({"status":"PASS","groups":groups,"total_finite_checks":sum(g["checks"] for g in groups),"limit":"Supplementary finite rational checks; no kernel or noncomputability certification."},indent=2))
