import unittest,random
from itertools import product
from math import gcd,prod
from crt_calibration import *

class CalibrationTests(unittest.TestCase):
    def test_linear_integer_selectors_have_exactly_one_nonempty_zero_subset(self):
        for r in range(1,7):
            universe=(1<<r)-1
            for selected in subsets(universe,True):
                exponents=selector_exponents(r,selected)
                for queried in subsets(universe):
                    value=sum(e for i,e in enumerate(exponents) if queried>>i&1)
                    self.assertLessEqual(abs(value),r*r)
                    self.assertEqual(value==0,queried in (0,selected))

    def test_private_residues_select_only_their_own_support(self):
        for r in range(1,5):
            cal=construct(r)
            for selected,(prime,g,row) in enumerate(zip(cal.private_primes,cal.primitive_roots,cal.residue_rows),1):
                self.assertTrue(is_prime(prime));self.assertGreater(prime-1,r*r)
                self.assertEqual(len({pow(g,k,prime) for k in range(prime-1)}),prime-1)
                for queried in subsets(cal.universe,True):
                    value=prod(x for i,x in enumerate(row) if queried>>i&1)%prime
                    self.assertEqual(value==1,queried==selected)

    def test_crt_representatives_give_strictly_interior_rates(self):
        for r in range(1,5):
            cal=construct(r);modulus=prod(cal.private_primes)
            self.assertEqual(cal.denominator,modulus+1)
            for i,b in enumerate(cal.numerators):
                self.assertGreater(b,0);self.assertLess(b,modulus)
                self.assertTrue(0<cal.rates[i]<1)
                for q,row in zip(cal.private_primes,cal.residue_rows):
                    self.assertEqual(b%q,row[i]);self.assertEqual(cal.denominator%q,1)
                    self.assertEqual(gcd(cal.denominator,q),1)

    def test_private_valuation_matrix_is_positive_diagonal(self):
        for r in range(1,5):
            cal=construct(r)
            for p,q in enumerate(cal.private_primes,1):
                for s in subsets(cal.universe,True):
                    value=valuation(cal.failure(s),q)
                    self.assertEqual(value>0,p==s)
                    if p!=s:self.assertEqual(value,0)

    def test_all_binary_support_models_through_three_roots_decode(self):
        for r in range(1,4):
            cal=construct(r)
            for vector in product((0,1),repeat=cal.universe):
                counts={p:n for p,n in zip(subsets(cal.universe,True),vector) if n}
                self.assertEqual(cal.decode(cal.probability(counts)),counts)

    def test_unknown_multiplicity_and_large_counts_decode_without_full_factoring(self):
        rng=random.Random(71008)
        for r in range(1,5):
            cal=construct(r)
            for _ in range(16):
                counts={p:rng.randrange(5) for p in subsets(cal.universe,True)}
                counts={p:n for p,n in counts.items() if n}
                self.assertEqual(cal.decode(cal.probability(counts)),counts)
            large={cal.universe:200}
            self.assertEqual(cal.decode(cal.probability(large)),large)

    def test_general_guarded_counts_decode_from_one_calibration_all_profiles(self):
        rng=random.Random(888)
        for r in range(1,5):
            cal=construct(r)
            for _ in range(8):
                counts={(p,n):rng.randrange(3) for p in subsets(cal.universe,True) for n in subsets(cal.universe^p)}
                counts={key:n for key,n in counts.items() if n}
                self.assertEqual(recover_guarded(cal,guarded_panel(cal,counts)),counts)

    def test_every_issued_profile_still_has_an_invisible_omission_route(self):
        for r in range(1,5):
            cal=construct(r);base={(1<<i,0):1 for i in range(r)}
            for omitted in subsets(cal.universe,True):
                alternate=dict(base);key=(omitted,cal.universe^omitted)
                alternate[key]=alternate.get(key,0)+1
                before=guarded_panel(cal,base);after=guarded_panel(cal,alternate)
                for queried in subsets(cal.universe,True):
                    self.assertEqual(before[queried]==after[queried],queried!=omitted)

    def test_known_count_bound_gives_common_rational_grid(self):
        for r in range(1,4):
            cal=construct(r);bound=2
            candidates=[{}]+[{p:1} for p in subsets(cal.universe,True)]
            candidates += [{p:2} for p in subsets(cal.universe,True)]
            candidates += [{p:1,s:1} for p in subsets(cal.universe,True) for s in subsets(cal.universe,True) if p<s]
            values=[cal.probability(counts) for counts in candidates]
            self.assertEqual(len(values),len(set(values)))
            self.assertTrue(all((q*cal.denominator**(r*bound)).denominator==1 for q in values))

    def test_invalid_readouts_are_not_certified_by_private_primes_alone(self):
        cal=construct(2)
        with self.assertRaises(ValueError):cal.decode(Q(0))
        extra_prime=next_primes(max(cal.private_primes),1)[0]
        with self.assertRaises(ValueError):cal.decode(Q(1,extra_prime))
        with self.assertRaises(ValueError):construct(0)

    def test_decoder_divides_by_nonunit_private_valuation(self):
        cal=construct(6)
        support=next(p for p,d in enumerate(cal.diagonal(),1) if d>1)
        coefficient=cal.diagonal()[support-1]
        self.assertGreater(coefficient,1)
        readout=cal.probability({support:3})
        self.assertEqual(valuation(readout,cal.private_primes[support-1]),3*coefficient)
        self.assertEqual(cal.decode(readout),{support:3})

if __name__=='__main__':unittest.main(verbosity=2)
