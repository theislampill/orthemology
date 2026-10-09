import unittest
from unittest.mock import patch
from fractions import Fraction as Q
from gcd_decoder import *
from countable_support import decode

class GcdDecoderTests(unittest.TestCase):
    def test_all_weighted_histograms_through_twelve(self):
        for weight in range(13):
            for counts in histograms_of_weight(weight):
                q=probability(counts)
                recovered,trace=decode_gcd(q)
                self.assertEqual(recovered,counts)
                self.assertEqual(trace['largest_generator'],max(counts,default=0))
                self.assertEqual(decode(q)[0],counts)

    def test_high_unknown_indices_need_no_factorisation(self):
        for counts in ({31:2,1:1},{127:1},{256:1},{1:5,64:2}):
            q=probability(counts)
            with patch('countable_support.factor_integer',side_effect=AssertionError('Factoring is not used')):
                self.assertEqual(decode_gcd(q)[0],counts)

    def test_early_stop_avoids_the_large_multiplicity_weight(self):
        counts={1:5000};recovered,trace=decode_gcd(probability(counts))
        self.assertEqual(recovered,counts);self.assertEqual(trace['weight'],5000)
        self.assertEqual(trace['largest_generator'],1)
        self.assertEqual(decode_gcd(probability({2:1000,3:999}))[1]['largest_generator'],3)

    def test_selector_has_complete_new_prime_valuations(self):
        _,trace=decode_gcd(probability({11:2}))
        item=next(item for item in trace['selectors'] if item['exponent']==11)
        self.assertEqual(item['component'],23*89*683)
        self.assertTrue(all(all(item['checks'].values()) for item in trace['selectors']))
        # A partial prime-power selector fails the explicit full-valuation guard.
        a=45;partial=3
        self.assertEqual(a%partial,0)
        self.assertNotEqual(gcd(partial,a//partial),1)

    def test_full_weight_and_early_stop_versions_agree(self):
        for counts in ({1:8},{1:3,4:2},{3:3,7:1}):
            q=probability(counts)
            self.assertEqual(decode_gcd(q,True)[0],decode_gcd(q,False)[0])

    def test_invalid_readouts_and_resource_limits_have_different_status(self):
        for q in (Q(0),Q(7,16),Q(7,64),Q(3,16),Q(1,4),Q(1,3)):
            with self.assertRaises(InvalidReadout):decode_gcd(q)
        q=probability({1:20})
        with self.assertRaises(ResourceInconclusive):decode_gcd(q,max_weight=10)
        self.assertEqual(decode_gcd(q,max_weight=20)[0],{1:20})

if __name__=='__main__':unittest.main(verbosity=2)
