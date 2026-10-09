#!/usr/bin/env python3
"""Independent finite controls. These are not general proofs or empirical data."""
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import mpmath as mp

mp.mp.dps = 100
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def mm(q):
    if isinstance(q, F):
        return mp.mpf(q.numerator) / q.denominator
    return mp.mpf(q)

def kl(u, v):
    u, v = mm(u), mm(v)
    if u == v:
        return mp.mpf(0)
    if v == 0 or v == 1:
        return mp.inf
    return (u * mp.log(u / v) if u else 0) + ((1-u) * mp.log((1-u)/(1-v)) if u != 1 else 0)

metrics = {'kind': 'deterministic exact-rational and high-precision numerical controls, not general proofs'}

# Exact rational inequality and AM-GM consequences, including extreme endpoints.
ns = list(range(1, 121)) + [127, 128, 255, 256, 511, 1000, 4096]
ts = {F(a, b) for b in [2, 3, 5, 7, 10, 16, 31, 64, 100] for a in range(1, b)}
ts |= {F(1, 10**e) for e in [3, 6, 12, 30]}
ts |= {1-F(1, 10**e) for e in [3, 6, 12, 30]}
exact_count = 0
for n in ns:
    for t in sorted(ts):
        a, b = t.numerator, t.denominator
        S = (b**(n+1)-a**(n+1))//(b-a)
        assert n*(n+1)*a**(n-1)*(b-a) <= 2*S
        assert S*S >= (n+1)**2 * a**n * b**n
        exact_count += 1
metrics['exact_uniform_envelope_and_amgm_cases'] = exact_count

# Independently recalculate the chi-square algebra with actual rational Bernoulli means.
algebra_cases = 0
for n in [1, 2, 3, 7, 20, 100]:
    for t in [F(1, 1000), F(1, 7), F(1, 2), F(9, 10), F(999, 1000)]:
        u, v = t**n, t**(n+1)
        chi = (u-v)**2/(v*(1-v))
        expression = t**(n-1)*(1-t)/sum((t**j for j in range(n+1)), F(0))
        assert chi == expression
        assert kl(u,v) <= mm(chi) + mp.mpf('1e-95')
        algebra_cases += 1
metrics['exact_chi_square_identity_cases'] = algebra_cases

# Numerical attack on actual KL, beyond rational control grids. Stable q=1-p treatment.
num_count = 0
max_ratio = (mp.mpf(0), None)
for n in [1, 2, 3, 4, 7, 10, 30, 100, 1000, 10**6]:
    for lam in [mp.mpf(10)**(mp.mpf(k)/10) for k in range(-70, 41)]:
        # t=exp(-lam/n); use survival and complement independently for stability.
        tlog = -lam/n
        u, v = mp.exp(n*tlog), mp.exp((n+1)*tlog)
        cu, cv = -mp.expm1(n*tlog), -mp.expm1((n+1)*tlog)
        kval = -u*tlog + cu*mp.log(cu/cv)
        assert kval >= -mp.mpf('1e-92')
        bound = mp.mpf(2)/(n*(n+1))
        assert kval <= bound + mp.mpf('1e-92')
        ratio = kval/bound
        if ratio > max_ratio[0]: max_ratio = (ratio, [n, str(lam)])
        num_count += 1
metrics['high_precision_actual_kl_cases'] = num_count
metrics['max_observed_kl_over_bound'] = {'ratio':str(max_ratio[0]), 'n_lambda':max_ratio[1]}

# Exact rational min-gap, telescoping bias, and constants.
gap_cases = 0
for K in list(range(2, 251)) + [1000, 4096]:
    t = F(K-1, K)
    mingap = t**(K-1)/K
    assert mingap > F(1, 3*K)
    if K <= 50:
        for j in range(K+1):
            eta=F(1, 12*K*K)
            for actual_x in [F(1,K)-eta,F(1,K)+eta]:
                assert abs((1-actual_x)**j-t**j) <= K*eta
                assert K*eta + F(1,12*K) < mingap/2
    gap_cases += 1
metrics['exact_fixed_rate_gap_K_cases'] = gap_cases

cal_cases=0
for K in list(range(2, 251)) + [1000, 1000000, 10**12]:
    t = 1-mp.mpf(1)/K
    L = -mp.log(t)
    d = t*mp.expm1(L/K)
    xp = 1-t-d
    assert 0 < xp < 1/mp.mpf(K)
    assert mp.mpf(1)/(2*K*K) <= d <= mp.mpf(2)/(K*K)
    assert abs((K-1)*mp.log(t) - K*mp.log1p(-xp)) < mp.mpf('1e-80')
    cal_cases += 1
metrics['high_precision_calibration_identity_and_floor_cases'] = cal_cases

# Full adaptive transcript enumeration. Seed is included so the randomization channel
# is visibly identical under both counts; endpoints 0/1 occur on positive-mass paths.
def transcript_law(count, n, horizon, policy):
    paths = {(seed, ()): F(1,2) for seed in [0,1]}
    boundary_used=set()
    rate_menu = [F(0),F(1),F(1,n+1),F(1,2),F(1,10),F(9,10),F(1,(n+1)**2)]
    for h in range(horizon):
        nxt=defaultdict(F)
        for (seed, hist), mass in paths.items():
            bits=tuple(y for x,y in hist)
            if policy==0:
                idx = (seed+3*h+sum((i+1)*y for i,y in enumerate(bits)))%len(rate_menu)
            elif policy==1:
                idx = (2+seed+sum(bits))%len(rate_menu)
            else:
                idx = (2 if h==0 else (4 if bits[-1] else 5))
            x=rate_menu[idx]
            if x in (0,1): boundary_used.add(int(x))
            q=(1-x)**count
            for y,prob in [(1,q),(0,1-q)]:
                if prob: nxt[(seed,hist+((x,y),))]+=mass*prob
        paths=nxt
    assert sum(paths.values(),F(0))==1
    return paths,boundary_used

adaptive_cases=0
boundary_seen=set()
for n in [1,2,3,10]:
    for horizon in [1,2,4,6]:
        for policy in range(3):
            p,bd=transcript_law(n,n,horizon,policy)
            q,_=transcript_law(n+1,n,horizon,policy)
            boundary_seen |= bd
            assert set(p)==set(q)
            divergence=sum((mm(v)*mp.log(mm(v/q[k])) for k,v in p.items()),mp.mpf(0))
            assert divergence <= mp.mpf(2)*horizon/(n*(n+1))+mp.mpf('1e-90')
            # Independent prefix-law chain-rule computation.
            chain=mp.mpf(0)
            for h in range(horizon):
                prefixes,bd=transcript_law(n,n,h,policy)
                for (seed,hist),mass in prefixes.items():
                    bits=tuple(y for x,y in hist)
                    menu=[F(0),F(1),F(1,n+1),F(1,2),F(1,10),F(9,10),F(1,(n+1)**2)]
                    if policy==0: idx=(seed+3*h+sum((i+1)*y for i,y in enumerate(bits)))%len(menu)
                    elif policy==1: idx=(2+seed+sum(bits))%len(menu)
                    else: idx=(2 if h==0 else (4 if bits[-1] else 5))
                    t=1-menu[idx]
                    chain += mm(mass)*kl(t**n,t**(n+1))
            assert abs(divergence-chain)<mp.mpf('1e-88')
            adaptive_cases += 1
assert boundary_seen == {0,1}
metrics['adaptive_exact_probability_transcript_cases']=adaptive_cases
metrics['adaptive_boundary_rates_exercised']=sorted(boundary_seen)

# Check confidence simplification and exact exponent coefficients.
for delta in [mp.mpf(1)/4,mp.mpf(1)/10,mp.mpf('1e-6'),mp.mpf('1e-30')]:
    b=(1-2*delta)*mp.log((1-delta)/delta)
    assert b >= mp.log(1/(2*delta))/2
assert 2*F(1,6)**2 == F(1,18)
assert 2*F(1,12)**2 == F(1,72)
metrics['confidence_and_hoeffding_constants']='PASS'
metrics['K_2_boundary']={'max_hard_pair_per_trial_bound':1,'nominal_t':'1/2','ambiguity_d':'sqrt(1/2)-1/2','empty_count_mean':1}
metrics['result']='PASS'
print(json.dumps(metrics,indent=2))
(HERE/'results'/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(metrics,indent=2)+'\n')
