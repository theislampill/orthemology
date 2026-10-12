from fractions import Fraction as Q
from math import factorial
import json
checks = 0

def check(p):
    global checks
    assert p
    checks += 1

# Exact finite-law shadow: independently compute normalization, hierarchy,
# positive-time untwisting, and two successive updates on integer support.
for n in range(1, 8):
    weights = [Q(j+1, (n+1)*(n+2)//2) for j in range(n+1)]
    for z in [Q(1,2), Q(2,3), Q(3,4)]:
        a = [sum((weights[j] * z**j * j**r for j in range(n+1)), Q(0)) for r in range(12)]
        m = [v/a[0] for v in a]
        check(m[0] == 1)
        check(all(v >= 0 for v in m))
        for r in range(11):
            quotient_derivative = (-a[r+1]*a[0]+a[r]*a[1])/a[0]**2
            check(quotient_derivative == -m[r+1]+m[1]*m[r])
        tilted = [weights[j]*z**j/a[0] for j in range(n+1)]
        recovered_mass = sum(tilted[j]*z**(-j) for j in range(n+1))
        recovered = [tilted[j]*z**(-j)/recovered_mass for j in range(n+1)]
        check(recovered == weights)
        for w in [Q(1,3),Q(3,5)]:
            den = sum(tilted[j]*w**j for j in range(n+1))
            composed = [tilted[j]*w**j/den for j in range(n+1)]
            directden = sum(weights[j]*(z*w)**j for j in range(n+1))
            direct = [weights[j]*(z*w)**j/directden for j in range(n+1)]
            check(composed == direct)
# Flat control a0=1-exp(-1/t): a2=exp(-1/t)*(2*t-1)/t**4.
# Its sign is exact without needing approximate exponential evaluation.
for k in range(3,103):
    t = Q(1,k)
    check((2*t-1)/t**4 < 0)
# Linear control m1=1/(T-t), m2=0 violates variance positivity,
# including at initial time: it is not a valid initial moment record.
for T in range(1,20):
    for p in range(4):
        t=Q(T*p,4)
        m1=1/(T-t)
        check(0-m1*m1 < 0)
# The determinate boundary example has zero-radius origin Laplace series.
# Successive coefficient ratio is exactly (2n+3)(2n+2)/(n+1).
for n in range(30):
    lhs=Q(factorial(2*n+3),factorial(n+1))/Q(factorial(2*n+1),factorial(n))
    check(lhs==Q((2*n+3)*(2*n+2),n+1))
print(json.dumps({'status':'PASS','exact_checks':checks,'scope':'Finite controls only; not a proof of the infinite classification.'},indent=2))
