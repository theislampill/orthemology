"""Exact finite corroboration of the ordinary endpoint-density corollary.

Uses only the Python standard library. This is not an all-real or kernel proof.
"""
from fractions import Fraction as F
from math import comb, factorial, isqrt
from pathlib import Path
import hashlib
import json

COUNTS = {}
def checked(name, condition):
    assert condition, name
    COUNTS[name] = COUNTS.get(name, 0) + 1

def interval(q, e):
    return ((q*q-F(1,4))/(e*(1+e)),
            (F(1,4)-(1-q)**2)/(e*(1-e)))

def accepted(alpha, q, e):
    return q*q-F(1,4)-alpha*e*(1+e) <= 0 and (1-q)**2-F(1,4)+alpha*e*(1-e) <= 0

def pow_int_integral(s, lo, hi):
    return (hi**s-lo**s)/s if hi > lo else F(0)

def missing(s, R, t, lo, hi):
    clipped_lo = min(t, max(F(0), lo))
    clipped_hi = min(t, max(F(0), hi))
    return t**s/s - pow_int_integral(s, clipped_lo, clipped_hi)

def exact_root(x, degree):
    def root(n):
        lo, hi = 0, n+1
        while hi-lo > 1:
            mid = (lo+hi)//2
            if mid**degree <= n:
                lo = mid
            else:
                hi = mid
        assert lo**degree == n
        return lo
    return F(root(x.numerator), root(x.denominator))

def rational_power(x, numerator, denominator):
    return exact_root(x, denominator)**numerator

def bern_power_integral(power, k, n, lo, hi):
    """Integral alpha^(power-1) alpha^k (1-alpha)^(n-k)."""
    if hi <= lo:
        return F(0)
    return sum(F((-1)**j*comb(n-k, j))*pow_int_integral(power+k+j, lo, hi)
               for j in range(n-k+1))

class Prior:
    def __init__(self, a, b, delta, left_weight, right_weight, tilt_left, tilt_right, atoms):
        self.a, self.b, self.delta = a, b, delta
        self.c, self.d = tilt_left, tilt_right
        self.K0 = left_weight/(delta**a*(F(1,a)+tilt_left/F(a+1)))
        self.K1 = right_weight/(delta**b*(F(1,b)+tilt_right/F(b+1)))
        self.atoms = atoms
        checked('prior_normalization', left_weight+right_weight+sum(atoms.values()) == 1)
        checked('positive_tail_bounds', self.K0 > 0 and self.K1 > 0 and delta < F(1,2))

    def joint_interval(self, k, n, lo=F(0), hi=F(1)):
        # Tail measures have no atoms; closed clipping changes no tail integrals.
        l0, u0 = max(F(0), lo), min(self.delta, hi)
        val = self.K0*(bern_power_integral(self.a, k, n, l0, u0)
                + self.c/self.delta*bern_power_integral(self.a+1, k, n, l0, u0))
        l1, u1 = max(F(0), 1-hi), min(self.delta, 1-lo)
        val += self.K1*(bern_power_integral(self.b, n-k, n, l1, u1)
                + self.d/self.delta*bern_power_integral(self.b+1, n-k, n, l1, u1))
        val += sum(weight*x**k*(1-x)**(n-k) for x, weight in self.atoms.items()
                   if lo <= x <= hi)
        return val

    def joint_failure(self, k, n, q, e):
        mass = self.joint_interval(k, n)
        if F(1,2) <= q <= F(1,2)+e:
            lo, hi = interval(q,e)
            return mass-self.joint_interval(k,n,lo,hi)
        return mass

    def empirical_risk(self, n, e):
        return sum(comb(n,k)*self.joint_failure(k,n,F(1,2)+e*F(k,n),e)
                   for k in range(n+1))

    def lower(self, n, e, side):
        # Replace exp(-1) by the weaker rational 1/4.
        R = (1+e)/(1-e) if side == 0 else (1+2*e)*(1-e)/((1-2*e)*(1+e))
        s, K = (self.a,self.K0) if side == 0 else (self.b,self.K1)
        return F(1,4)*K*R**(-s)*(self.delta/F(n+1))**s/s


def main():
    eps = [F(1,100),F(1,8),F(1,4)]
    for e in eps:
        R0=(1+e)/(1-e)
        R1=(1+2*e)*(1-e)/((1-2*e)*(1+e))
        for j in range(41):
            q=F(1,2)+e*F(j,40)
            lo,hi=interval(q,e)
            checked('accepted_interval_geometry', 0 <= lo <= hi <= 1 and hi <= R0*lo
                    and 1-lo <= R1*(1-hi))
            for n in [1,2,5,20]:
                t=F(1,4*(n+1))
                for s in [1,2,3,5]:
                    checked('integer_missing_power', missing(s,R0,t,lo,hi) >= R0**(-s)*t**s/s)
                    checked('integer_missing_power', missing(s,R1,t,1-hi,1-lo) >= R1**(-s)*t**s/s)
            for alpha in [F(0),lo,hi,F(1)]:
                checked('closed_interval_acceptance', accepted(alpha,q,e) == (lo <= alpha <= hi))
        for n in [1,2,10]:
            for alpha in [F(0), F(1)]:
                checked('endpoint_exact_after_receipt', accepted(alpha,F(1,2)+e*alpha,e))
        for alpha in [F(j,20) for j in range(21)]:
            checked('always_wrong_policy', not accepted(alpha,F(2),e))
            checked('correlated_seed_countercontrol', accepted(alpha,F(1,2)+e*alpha,e))

    # Fractional-shape controls use coordinates with exact rational powers.
    for numerator,denominator in [(1,2),(2,3),(3,2)]:
        s=F(numerator,denominator)
        R=F(6,5)**denominator
        for ti in [2,5,8]:
            t=F(ti,10)**denominator
            for li in range(13):
                for ui in range(li,13):
                    lo=F(li,10)**denominator
                    hi=F(ui,10)**denominator
                    if hi > R*lo:
                        continue
                    l,h=min(t,lo),min(t,hi)
                    excluded=(rational_power(t,numerator,denominator)
                              -rational_power(h,numerator,denominator)
                              +rational_power(l,numerator,denominator))/s
                    bound=rational_power(F(1,R),numerator,denominator)*rational_power(t,numerator,denominator)/s
                    checked('fractional_missing_power', excluded >= bound)

    for delta in [F(1,10),F(1,4),F(2,5)]:
        for n in range(1,101):
            checked('extreme_prefix_likelihood', (1-delta/F(n+1))**n >= F(1,4))
        for j in range(101):
            alpha=F(j,100)
            if 0 <= alpha <= delta:
                checked('endpoint_variance_lower', alpha*(1-alpha) >= (1-delta)*alpha)
            if delta <= alpha <= 1-delta:
                checked('interior_variance_lower', alpha*(1-alpha) >= delta*(1-delta))

    # Nonconjugate piecewise tilted power densities, plus five possible atoms.
    for a,b in [(1,1),(1,3),(2,2),(3,1),(3,4)]:
        for delta in [F(1,4),F(1,3)]:
            for tilt in [F(0),F(2)]:
                atoms={F(0):F(1,10),F(1):F(1,20),delta:F(1,20),1-delta:F(1,20),F(1,2):F(1,4)}
                prior=Prior(a,b,delta,F(1,4),F(1,4),tilt,F(1),atoms)
                for e in eps:
                    for n in range(1,13):
                        total=sum(comb(n,k)*prior.joint_interval(k,n) for k in range(n+1))
                        checked('mixed_prefix_mass_normalization', total == 1)
                        risk=prior.empirical_risk(n,e)
                        lower=prior.lower(n,e,0)+prior.lower(n,e,1)
                        checked('nonconjugate_empirical_integrated_risk', lower <= risk <= 1)
                        for side,k in [(0,0),(1,n)]:
                            failures=[]
                            for j in [0,1,3,7,10]:
                                q=F(1,2)+e*F(j,10)
                                fail=prior.joint_failure(k,n,q,e)
                                checked('unnormalized_report_lower', fail >= prior.lower(n,e,side))
                                failures.append(fail)
                            seed_mix=sum(weight*fail for weight,fail in zip([F(1,10),F(1,5),F(3,10),F(1,4),F(3,20)],failures))
                            checked('independent_seed_mixture_lower', seed_mix >= prior.lower(n,e,side))

    # Finite-stage Cantor approximants inside the compact interior: each is
    # a valid singular (atomic) interior measure. No limit theorem is inferred.
    for depth in range(1,7):
        points=[sum(F(2*((word>>j)&1),3**(j+1)) for j in range(depth)) for word in range(2**depth)]
        delta=F(1,4)
        atoms={delta+(1-2*delta)*x:F(1,2**(depth+1)) for x in points}
        prior=Prior(2,3,delta,F(1,4),F(1,4),F(1),F(2),atoms)
        for n in range(1,7):
            risk=prior.empirical_risk(n,F(1,4))
            checked('cantor_approximant_mixed_risks', prior.lower(n,F(1,4),0)+prior.lower(n,F(1,4),1) <= risk <= 1)

    # Invalid conditional-posterior transplant in the presence of an atom.
    e=F(1,4)
    for n in [1,2,10,100]:
        conditional=F(1,n+1)/(99+F(1,n+1))
        checked('endpoint_atom_posterior_countercontrol', conditional < ((1+e)/(1-e))**(-1))
    checked('empty_prefix_double_count_countercontrol', F(3,5)+F(5,9) > 1)
    checked('pure_endpoint_zero_cost_countercontrol', all(accepted(alpha,F(1,2)+e*alpha,e) for alpha in [F(0),F(1)]))
    # Half Beta(2,2) has density 3 alpha(1-alpha): its interior inverse
    # moment equals integral_0^1 3 d alpha = 3. The other half is at zero.
    checked('endpoint_inverse_moment_countercontrol', F(1,2)*F(6) == 3)
    # Uniform density dominates alpha^(a-1) for a>=1, so a lower-only
    # condition cannot establish a fast exponent or a finite budget.
    for a in [2,3,5]:
        for j in range(1,100):
            checked('lower_density_only_countercontrol', F(j,100)**(a-1) <= 1)
    # Repeated bounded schedules retain a strictly positive per-report rate.
    for a,b in [(1,1),(2,3),(5,2)]:
        for n in [1,3,20]:
            m=min(a,b)
            checked('deterministic_clock_power_equivalence', F(1,n**m) <= F(1,n**a)+F(1,n**b) <= F(2,n**m))

    result={'status':'PASS','checks':COUNTS,'total_checks':sum(COUNTS.values()),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'Exact rational finite corroboration and shortcut countercontrols; ordinary theorem has separate all-real and measure-theoretic proof'}
    dest=Path(__file__).with_name('RESULT.json')
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
