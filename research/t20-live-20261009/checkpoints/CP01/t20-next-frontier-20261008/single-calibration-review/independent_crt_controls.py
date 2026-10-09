"""Independent CRT-existence controls; separate from the author's implementation.

Construction here uses incremental CRT and the independently proposed exponent
pattern subsequently shared with the author: inside P use k-1 copies of +1 and
one -(k-1), outside P use +k. The author now uses this pattern too.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import random
import unittest

HERE = Path(__file__).resolve().parent
METRICS = {}


def prime(n):
    return n >= 2 and all(n % d for d in range(2,int(n**0.5)+1))


def factor_distinct(n):
    factors = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            factors.append(d)
            while n%d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def generator(q):
    if q == 2:
        return 1
    return next(g for g in range(2,q) if all(pow(g,(q-1)//p,q) != 1 for p in factor_distinct(q-1)))


def exponents(roots,mask):
    inside = [i for i in range(roots) if mask>>i&1]
    k = len(inside)
    result = [k]*roots
    for i in inside[:-1]:
        result[i] = 1
    result[inside[-1]] = -(k-1)
    return tuple(result)


def incremental_crt(residues,moduli):
    value, modulus = 0, 1
    for residue,q in zip(residues,moduli):
        step = ((residue-value)*pow(modulus,-1,q)) % q
        value += modulus*step
        modulus *= q
    return value,modulus


def construct(roots):
    masks = tuple(range(1,1<<roots))
    moduli = []
    candidate = roots*roots+2
    for _ in masks:
        while not prime(candidate):
            candidate += 1
        moduli.append(candidate)
        candidate += 1
    residues = [[pow(generator(q),a%(q-1),q) for a in exponents(roots,mask)] for mask,q in zip(masks,moduli)]
    numerators = []
    for i in range(roots):
        value, modulus = incremental_crt([row[i] for row in residues],moduli)
        numerators.append(value)
    denominator = modulus+1
    return tuple(F(b,denominator) for b in numerators),tuple(moduli),tuple(numerators),denominator


def failure(mask,rates):
    survival = F(1)
    for i,rate in enumerate(rates):
        if mask>>i&1:
            survival *= rate
    return 1-survival


def valuation(value,p):
    count = 0
    for number,sign in ((value.numerator,1),(value.denominator,-1)):
        while number%p == 0:
            count += sign
            number //= p
    return count


class IndependentCRTReview(unittest.TestCase):
    def test_zero_subset_sum_is_exactly_empty_and_designated_support(self):
        checked = 0
        for roots in range(1,9):
            for target in range(1,1<<roots):
                powers = exponents(roots,target)
                zero_masks = {mask for mask in range(1<<roots) if sum(powers[i] for i in range(roots) if mask>>i&1) == 0}
                self.assertEqual(zero_masks,{0,target})
                self.assertLess(max(abs(sum(powers[i] for i in range(roots) if mask>>i&1)) for mask in range(1<<roots)), roots*roots+1)
                checked += 1
        METRICS['zero_sum_support_patterns'] = checked

    def test_calibrations_have_strict_rates_and_private_diagonal(self):
        checked = 0
        details = {}
        for roots in range(1,7):
            rates,primes,numerators,denominator = construct(roots)
            self.assertTrue(all(0 < x < 1 for x in rates))
            self.assertTrue(all(1 <= b < denominator-1 for b in numerators))
            factors = {mask:failure(mask,rates) for mask in range(1,1<<roots)}
            diagonal = []
            for target,p in enumerate(primes,1):
                self.assertEqual(denominator%p,1)
                for support,factor in factors.items():
                    self.assertEqual(valuation(factor,p)>0,support==target)
                    checked += 1
                diagonal.append(valuation(factors[target],p))
            details[str(roots)] = {'calibration_denominator_bits':denominator.bit_length(),'support_count':len(primes),'minimum_diagonal':min(diagonal),'maximum_diagonal':max(diagonal),'primes':list(primes)}
        METRICS['private_prime_entries'] = checked
        METRICS['calibrations'] = details

    def test_exact_single_readout_recovers_integer_histograms(self):
        rng = random.Random(202610080730)
        checked = 0
        for roots in range(1,6):
            rates,primes,_,_ = construct(roots)
            factors = {mask:failure(mask,rates) for mask in range(1,1<<roots)}
            diagonals = {mask:valuation(factors[mask],p) for mask,p in enumerate(primes,1)}
            for _ in range(12):
                counts = {mask:rng.randrange(4) for mask in factors}
                q = F(1)
                for mask,count in counts.items():
                    q *= factors[mask]**count
                recovered = {}
                for mask,p in enumerate(primes,1):
                    v = valuation(q,p)
                    self.assertEqual(v%diagonals[mask],0)
                    recovered[mask] = v//diagonals[mask]
                self.assertEqual(recovered,counts)
                checked += 1
        METRICS['single_readout_reconstructions'] = checked

    def test_single_root_edge_case(self):
        rates,primes,numerators,denominator = construct(1)
        self.assertEqual(numerators,(1,))
        self.assertEqual(rates,(F(1,primes[0]+1),))
        self.assertEqual(valuation(1-rates[0],primes[0]),1)


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(IndependentCRTReview))
    (HERE/'INDEPENDENT_CRT_METRICS.json').write_text(json.dumps(METRICS,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
