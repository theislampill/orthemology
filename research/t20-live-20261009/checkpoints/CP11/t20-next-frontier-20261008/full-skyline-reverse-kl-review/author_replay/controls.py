#!/usr/bin/env python3
"""Deterministic diagnostics only; no sampling, fitting, or interval certification."""
import itertools
import json
import math
import platform
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp

mp.mp.dps = 110
ROOT = Path(__file__).resolve().parent


def mm(q):
    if isinstance(q, F):
        return mp.mpf(q.numerator) / q.denominator
    return mp.mpf(q)


def out(x):
    return mp.nstr(x, 45)


def ceil_log2(n):
    return (n - 1).bit_length()


def geometry(s):
    x = [p[0] for p in s] + [F(1)]
    y = [p[1] for p in s]
    u = x[0] + sum((x[i + 1] - x[i]) * y[i] for i in range(len(s)))
    m1 = (x[0] ** 2 + sum((x[i + 1] ** 2 - x[i] ** 2) * y[i] ** 2 for i in range(len(s)))) / 4
    return u, m1


def height(s, a):
    return min([y for x, y in s if x <= a] + [F(1)])


def exact_log_likelihood(s, m):
    n = m - 1
    k = len(s)
    c = mp.mpf(n) / m
    d0 = mm(1 - geometry(s)[0])
    dc = mp.mpf(0)
    for i, (xx, yy) in enumerate(s):
        a, y = mm(xx), mm(yy)
        b = mm(s[i + 1][0]) if i + 1 < k else mp.mpf(1)
        dc += (1-a)**c - (1-b)**c + (1-b*y)**c - (1-a*y)**c
    logs = [mp.log(c) + (c-2)*mp.log1p(-mm(x*y)) + mp.log1p(-c*mm(x*y)) for x,y in s]
    ell = mp.log(mp.mpf(m)/(m-k)) + sum(logs) + (m-k)*mp.log(dc) - (n-k)*mp.log(d0)
    return ell, d0, dc


checks = {}
# Exact rational R_m distributions, factorial moments and fourth-moment envelopes.
record_rows = []
probs = [F(1)]
h = F(0)
for m in range(1, 65):
    p = F(1, m)
    probs = [((probs[k] * (1-p)) if k < len(probs) else 0) + ((probs[k-1]*p) if k else 0) for k in range(len(probs)+1)]
    h += p
    assert sum(probs) == 1
    e4 = sum(prob * k**4 for k, prob in enumerate(probs))
    envelope = h**4 + 6*h**3 + 7*h**2 + h
    assert e4 <= envelope
    for r in range(1, 5):
        ef = sum(prob * math.prod(range(k-r+1, k+1)) if k >= r else F(0) for k,prob in enumerate(probs))
        assert ef <= h**r
    mgf = sum(mm(prob)*mp.exp(k) for k,prob in enumerate(probs))
    assert mp.log(mgf) <= (mp.e-1)*mm(h) + mp.mpf('1e-100')
    if m in [1,2,4,8,16,32,64]:
        record_rows.append({'m':m, 'E_R4':str(e4), 'fourth_envelope':str(envelope), 'mgf_log':out(mp.log(mgf))})
checks['record_exact_rational'] = {'sizes_checked':64, 'rows':record_rows}

# For T_a=na h(a), its exact fourth moment follows by integrating its exact
# polynomial tail: 4*n^4*int_0^a u^3(1-u)^n du. The atom at h=1 is included.
height_rows = []
height_count = 0
for n in range(1, 33):
    for a in [F(1,2),F(1,4),F(1,8),F(1,32),F(3,4)]:
        integral = sum(F((-1)**r * math.comb(n,r), r+4) * a**(r+4) for r in range(n+1))
        moment = 4*n**4*integral
        assert 0 <= moment <= 24
        height_count += 1
        if n in [1,2,8,32] and a == F(1,2):
            height_rows.append({'n':n, 'a':str(a), 'exact_E_T4':str(moment), 'decimal':out(mm(moment))})
        for frac in [F(0),F(1,8),F(1,2),F(7,8)]:
            t = n*a*frac
            tail = (1-t/n)**n
            assert mm(tail) <= mp.exp(-mm(t)) + mp.mpf('1e-100')
            b = t / (n*a)
            c = mp.mpf(n)/(n+1)
            joe_no_hit = ((1-mm(a*b))**c)**(n+1)
            assert abs(joe_no_hit-mm(tail)) < mp.mpf('1e-100')
checks['height_exact_rational'] = {'cases_checked':height_count, 'rows':height_rows}

# Fixed deterministic skylines, including high-area boundary cases and small
# dyadic staircases. Hidden routes are placed at one deterministic dominated
# point when checking the global bound; this is not a random sample.
configurations = []
for m in [2,3,4,8,16,64,256,1024,4096,2**20]:
    configurations.extend([
        (m, [(F(1,4),F(1,3))], 'one_point'),
        (m, [(F(1)-F(1,10**12),F(1,2))], 'boundary_12'),
        (m, [(F(1)-F(1,10**60),F(1,2))], 'boundary_60'),
    ])
    k = min(m-1, max(1, (m.bit_length()-1)))
    configurations.append((m,[(F(2)**(i-k-1),F(2)**(-i)) for i in range(1,k+1)],'dyadic_staircase'))
    for k in sorted({1,min(2,m-1),min(4,m-1),min(8,m-1)}):
        s = [(F(i,4*m),F(k+1-i,4*m)) for i in range(1,k+1)]
        configurations.append((m,s,'small_corner'))

skyline_rows = []
local_count = 0
max_ratio = mp.mpf(0)
for m,s,label in configurations:
    n=m-1
    k=len(s)
    assert all(0<x<1 and 0<y<1 for x,y in s)
    assert all(s[i][0]<s[i+1][0] and s[i][1]>s[i+1][1] for i in range(k-1))
    u,m1=geometry(s)
    j=ceil_log2(n)
    dyadic_upper=1+sum(n*F(1,2**(r+1))*height(s,F(1,2**(r+1))) for r in range(j))
    assert n*u <= dyadic_upper
    ell,d0,dc=exact_log_likelihood(s,m)
    assert d0>0 and dc>0
    a=F(k,m)
    z=mm(a+u)
    lead=(mm(k-m*u)**2-k)/(2*m*m) + 2*(sum(mm(x*y) for x,y in s)/m-mm(m1))
    if a<=F(1,2) and u<=F(1,2):
        assert abs(ell-lead) <= 40*z**3+mp.mpf('1e-90')
    if a+u<=F(1,2):
        local_count += 1
        assert abs(ell) <= 23*z*z+mp.mpf('1e-90')
        max_ratio=max(max_ratio,abs(ell)/(z*z))
    hidden_x=(F(1)+max(x for x,y in s))/2
    hidden_y=(F(1)+max(y for x,y in s))/2
    w=sum(-mp.log1p(-mm(x))-mp.log1p(-mm(y)) for x,y in s)
    w+=(n-k)*(-mp.log1p(-mm(hidden_x))-mp.log1p(-mm(hidden_y)))
    assert abs(ell)<=2*m*(1+w)
    if label in ['dyadic_staircase','boundary_60']:
        skyline_rows.append({'m':m,'k':k,'label':label,'U':str(u),'log_L':out(ell),'local_window':bool(a+u<=F(1,2))})
checks['fixed_skyline_geometry_likelihood'] = {'configurations_checked':len(configurations),'local_checks':local_count,'largest_observed_logL_over_z2':out(max_ratio),'rows':skyline_rows}

# Illustrate the eventual-window conditions; this does not substitute for the
# analytic O(log^2(m))/m proof.
window_rows=[]
for n in [10,100,1000,10000,20000,100000,1000000,10**12]:
    m=n+1
    j=ceil_log2(n)
    h=mp.harmonic(m)
    t=20*mp.log(m)
    b=mp.e*h+t+mp.mpf(m)/n*(1+j*t)
    beta=mp.mpf(j+1)*mp.mpf(m)**(-20)
    window_rows.append({'n':n,'B_over_m':out(b/m),'23_B_over_m_squared':out(23*(b/m)**2),'tail_bound_4m2sqrtbeta_plus_2beta':out(4*m*m*mp.sqrt(beta)+2*beta),'conditions_satisfied':bool(b/m<=mp.mpf('0.5') and 23*(b/m)**2<=1)})
assert window_rows[-1]['conditions_satisfied']
checks['eventual_window'] = window_rows

# Exact mass correction and direction in a finite deterministic analogue.
q0=[F(2,5),F(3,5),F(0)]
q1=[F(3,10),F(1,2),F(1,5)]
d=sum(mm(q0[i])*mp.log(mm(q0[i])/mm(q1[i])) for i in range(2))
phi=sum(mm(q0[i])*(-mp.log(mm(q1[i])/mm(q0[i]))+mm(q1[i])/mm(q0[i])-1) for i in range(2))
p=mm(q1[2])
assert abs(d-(phi+p))<mp.mpf('1e-100')
assert abs(d-(phi-p))>mp.mpf('0.3')

# Stop when outcome 0 is observed or at cap=5. Finite terminal words make the
# full KL and both expected costs independently enumerable.
cap=5
leaves=[]
def enumerate_words(word,prob0,prob1):
    if word and (word[-1]==0 or len(word)==cap):
        leaves.append((word,prob0,prob1))
        return
    for i in range(3):
        enumerate_words(word+(i,),prob0*q0[i],prob1*q1[i])
enumerate_words((),F(1),F(1))
assert sum(p0 for word,p0,p1 in leaves)==1
assert sum(p1 for word,p0,p1 in leaves)==1
n0=sum(len(word)*p0 for word,p0,p1 in leaves)
n1=sum(len(word)*p1 for word,p0,p1 in leaves)
terminal_kl=sum(mm(p0)*mp.log(mm(p0)/mm(p1)) for word,p0,p1 in leaves if p0)
assert abs(terminal_kl-d*mm(n0))<mp.mpf('1e-98')
assert abs(terminal_kl-d*mm(n1))>mp.mpf('1e-3')
checks['mass_correction_and_reverse_stopping']={'per_reveal_reverse_kl':out(d),'E_phi':out(phi),'singular_mass':out(p),'E0_N':str(n0),'E1_N':str(n1),'terminal_reverse_kl':out(terminal_kl),'D_times_E0_N':out(d*mm(n0)),'D_times_E1_N_wrong_orientation':out(d*mm(n1)),'terminal_words':len(leaves)}

payload={'status':'PASS','assurance':'Deterministic exact rational and high-precision arithmetic diagnostics; not empirical or interval-certified proof.','python':platform.python_version(),'mpmath':mp.__version__,'precision_digits':mp.mp.dps,'checks':checks}
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps({'status':'PASS','record_sizes':64,'height_cases':height_count,'skyline_cases':len(configurations),'local_cases':local_count,'stopping_words':len(leaves),'output':'CONTROL_RESULTS.json'},indent=2))
