#!/usr/bin/env python3
"""Independent certified Cauchy-input controls for the finite-panel appendix.

The recovery path only sees intervals for raw masked Q, not exact isolated Z.
All arithmetic is Fraction/integer; exact fixtures are used only by the mock
population oracle and final checks. No author implementation is imported.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import prod
import json

HERE = Path(__file__).resolve().parent
statistics = {'oracle_calls': 0, 'sign_decisions': 0, 'largest_bits_used': 0}


def model_q(counts, rates, mask):
    ans = F(1)
    for s, n in counts.items():
        if n and s & mask == s:
            ans *= (1-prod((p for i,p in enumerate(rates) if s >> i & 1), start=F(1)))**n
    return ans


def probability_interval(value, bits, style):
    statistics['oracle_calls'] += 1
    if value == 1:  # Q(0)=1 is known; other exact ones may also be supplied exactly.
        return F(1), F(1)
    scale = 2**bits
    floor = value.numerator * scale // value.denominator
    if style == 0:
        lo, hi = F(floor,scale), F(floor+1,scale)
    else:
        lo, hi = F(floor-1,scale), F(floor+2,scale)
    lo, hi = max(F(0),lo), min(F(1),hi)
    assert lo <= value <= hi
    return lo, hi


def isolate_interval(raw_masks, bits, style):
    lo = hi = F(1)
    for sign, value in raw_masks:
        lower, upper = probability_interval(value, bits, style)
        if sign == 1:
            lo, hi = lo*lower, hi*upper
        else:
            if lower == 0:
                return None  # Refine the raw denominator's oracle.
            lo, hi = lo/upper, hi/lower
    # The declared model supplies 0<Z<=1, independently of approximate data.
    return max(F(0),lo), min(F(1),hi)


def root_bracket(value, degree, bits):
    lo, hi = F(0), F(1)
    for _ in range(bits):
        mid = (lo+hi)/2
        if mid**degree <= value:
            lo = mid
        else:
            hi = mid
    assert lo**degree <= value <= hi**degree
    return lo, hi


def p_interval(z_bounds, cut_k, bits):
    zlo, zhi = z_bounds
    degree = 2*cut_k+1
    lower_root = root_bracket(zlo*zlo, degree, bits)[0]
    upper_root = root_bracket(zhi*zhi, degree, bits)[1]
    return 1-upper_root, 1-lower_root


def determinant_interval(raw, cut_k, bits, style):
    entries = []
    for masks in raw:
        z = isolate_interval(masks,bits,style)
        if z is None:
            return None
        entries.append(p_interval(z,cut_k,bits))
    aa, bb, cc, dd = entries
    lower = aa[0]*dd[0]-bb[1]*cc[1]
    upper = aa[1]*dd[1]-bb[0]*cc[0]
    return lower, upper


def sign(raw, cut_k, style):
    bits = 8
    while bits <= 512:  # Diagnostic cap, not a uniform theorem bound.
        interval = determinant_interval(raw,cut_k,bits,style)
        if interval is not None:
            lo, hi = interval
            if lo > 0 or hi < 0:
                statistics['sign_decisions'] += 1
                statistics['largest_bits_used'] = max(statistics['largest_bits_used'],bits)
                return 1 if lo > 0 else -1
        bits *= 2
    raise AssertionError('This finite diagnostic did not separate before its test cap.')


def make_raw_panel(n, roots):
    support = (1 << roots)-1
    counts = {s:(s%3)+1 for s in range(1,support)}
    counts[support] = n
    raw = []
    for a,b in product([F(1,5),F(3,5)],[F(1,7),F(4,7)]):
        rates = [a,b]+[F(2,5)]*(roots-2)
        masks=[]
        for t in range(support+1):
            parity = (roots-t.bit_count())%2
            masks.append((-1 if parity else 1,model_q(counts,rates,t)))
        raw.append(masks)
    return raw


def recover(raw,style):
    upper = 1
    while sign(raw,upper,style) < 0:
        upper *= 2
    lower = 1
    while lower < upper:
        middle = (lower+upper)//2
        if sign(raw,middle,style)>0:
            upper = middle
        else:
            lower = middle+1
    return lower


def main():
    cases=0
    for n,roots,style in product(range(1,11),[2,3],[0,1]):
        raw = make_raw_panel(n,roots)
        assert recover(raw,style) == n
        assert sign(raw,n-1,style) == -1
        assert sign(raw,n,style) == 1
        cases+=1
    zero_checks=0
    for roots,style,bits,k in product([2,3],[0,1],[16,32,64],[0,1,3]):
        bounds = determinant_interval(make_raw_panel(0,roots),k,bits,style)
        assert bounds is not None and bounds[0] <= 0 <= bounds[1]
        zero_checks+=1
    factor_checks=0
    for a1,a2,b1,b2,K in [
        (F(1,5),F(3,5),F(1,7),F(4,7),F(1)),
        (F(1,9),F(4,9),F(1,8),F(5,8),F(2,5)),
        (F(1,101),F(2,101),F(1,103),F(2,103),F(1,107))]:
        h=lambda x: 1-(1-x)**2
        determinant=h(K*a1*b1)*h(K*a2*b2)-h(K*a1*b2)*h(K*a2*b1)
        exact=-2*K**3*a1*a2*b1*b2*(a2-a1)*(b2-b1)
        assert determinant == exact < 0
        factor_checks+=1
    result={'status':'PASS','arithmetic':'Exact rational input intervals and integer-power root brackets',
            'recovered_positive_count_cases':cases,
            'zero_support_intervals_contain_zero':zero_checks,
            'c2_exact_determinant_factorizations':factor_checks,
            'statistics':statistics,
            'scope':'Finite tests include approximate raw-mask Q propagation, not a uniform precision or sample theorem.'}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    (HERE/'INDEPENDENT_PANEL_CONTROLS.json').write_text(text)
    print(text,end='')


if __name__=='__main__': main()
