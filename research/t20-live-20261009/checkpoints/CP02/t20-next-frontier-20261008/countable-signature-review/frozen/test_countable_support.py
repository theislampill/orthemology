import unittest,random
from itertools import product
from countable_support import *

class CountableSupportTests(unittest.TestCase):
    def test_binary_support_coding_and_fixed_calibration(self):
        for exponent in range(1,65):
            support=decode_support(exponent)
            self.assertEqual(encode_support(support),exponent)
            self.assertEqual(prod((rate(i) for i in support),start=Q(1)),Q(1,4**exponent))
        self.assertEqual(encode_support([0,0,2]),encode_support([0,2]))

    def test_verified_base_four_has_order_witnesses_in_executed_range(self):
        for exponent in range(1,25):
            prime=primitive_prime_witness(exponent)
            self.assertIsNotNone(prime)
            self.assertEqual(order_of_four(prime),exponent)
            self.assertTrue(all(pow(4,k,prime)!=1 for k in range(1,exponent)))

    def test_binary_histograms_decode_without_signature_bound(self):
        for values in product((0,1),repeat=8):
            counts={e:n for e,n in enumerate(values,1) if n}
            self.assertEqual(decode(probability(counts))[0],counts)

    def test_generated_multiplicities_and_high_index_decode(self):
        rng=random.Random(10082026)
        for _ in range(48):
            counts={e:rng.randrange(3) for e in range(1,16)}
            counts={e:n for e,n in counts.items() if n}
            self.assertEqual(decode(probability(counts))[0],counts)
        # No largest-index argument is passed to the decoder.
        for counts in ({16:1},{32:1},{1:3,16:2},{3:5,8:4}):
            self.assertEqual(decode(probability(counts))[0],counts)

    def test_shared_prime_orders_require_descending_elimination(self):
        counts={6:2,3:1,1:4}
        recovered,trace=decode(probability(counts))
        self.assertEqual(recovered,counts)
        steps=trace['steps'];self.assertEqual([s['exponent'] for s in steps],sorted([s['exponent'] for s in steps],reverse=True))
        self.assertEqual(order_of_four(3),1)
        self.assertGreater(valuation(probability({6:2}),3),0)
        self.assertEqual(decode(probability({6:2}))[0],{6:2})
        recovered,trace=decode(Q(255,256))
        self.assertEqual(recovered,{4:1})
        self.assertEqual({step['exponent']:step['count'] for step in trace['steps']},{4:1,2:0,1:0})

    def test_denominator_weight_is_not_the_complete_histogram(self):
        left={1:3};right={3:1}
        self.assertEqual(probability(left).denominator,probability(right).denominator)
        self.assertNotEqual(probability(left),probability(right))
        self.assertNotEqual(decode(probability(left))[0],decode(probability(right))[0])

    def test_base_two_exception_gives_a_real_multiplicative_collision(self):
        left={6:1,1:1};right={2:2,3:1}
        self.assertEqual(probability(left,2),Q(63,128))
        self.assertEqual(probability(left,2),probability(right,2))
        self.assertNotEqual(probability(left,4),probability(right,4))

    def test_nonmodel_rationals_are_rejected(self):
        for q in (Q(0),Q(2),Q(1,2),Q(1,3),Q(7,16),Q(1,4),Q(5,16)):
            with self.assertRaises(ValueError):decode(q)
        self.assertEqual(decode(Q(1))[0],{})

    def test_finite_arbitrary_infinite_profiles_have_an_invisible_guard(self):
        families=[(lambda i:True,),
                  (lambda i:True,lambda i:False,lambda i:i%2==0,lambda i:i%3==1)]
        for n in range(1,9):
            families.append(tuple([lambda i:True]+[lambda i,j=j:bool(i>>j&1) for j in range(n-1)]))
        base=[(frozenset({0}),frozenset(),1)]
        fresh_i,fresh_j,_=hidden_guard_pair(families[0],excluded={0,1,2,3})
        self.assertTrue({fresh_i,fresh_j}.isdisjoint({0,1,2,3}))
        for profiles in families:
            i,j,pattern=hidden_guard_pair(profiles)
            self.assertNotEqual(i,j)
            extra=base+[(frozenset({i}),frozenset({j}),1)]
            for profile in profiles:self.assertEqual(guarded_probability(base,profile),guarded_probability(extra,profile))
            distinguishing=lambda k:k==i
            self.assertNotEqual(guarded_probability(base,distinguishing),guarded_probability(extra,distinguishing))

    def test_adaptive_finite_query_transcript_is_preserved(self):
        base=[(frozenset({0}),frozenset(),1)]
        first,profiles=finite_query_policy(lambda profile:guarded_probability(base,profile))
        i,j,_=hidden_guard_pair(profiles)
        alternative=base+[(frozenset({i}),frozenset({j}),1)]
        second,_=finite_query_policy(lambda profile:guarded_probability(alternative,profile))
        self.assertEqual(first,second)

    def test_unbounded_index_fixed_calibration_has_no_uniform_sampling_margin(self):
        for index in range(1,9):
            x=rate(index)
            baseline=probability({1:1})
            alternate=probability({1:1,1<<index:1})
            self.assertEqual(baseline-alternate,Q(3,4)*x)
            self.assertEqual(x,Q(1,4**(1<<index)))

    def test_nonempty_single_route_indices_already_lose_uniform_sample_margin(self):
        for i in range(1,8):
            left=probability({1<<i:1});right=probability({1<<(i+1):1})
            p=rate(i)
            self.assertEqual(abs(left-right),p-p*p)
            self.assertLess(abs(left-right),p)
            self.assertEqual(left.denominator.bit_length(),2**(i+1)+1)

    def test_greedy_infinite_prefix_has_bounded_digits_and_certified_error(self):
        for target_e in (1,2,4,8):
            counts,partial,records=greedy_infinite_prefix(target_e,target_e+32)
            target=failure(target_e)
            self.assertEqual(probability(counts),partial)
            for record in records:
                e=record['exponent'];q=record['partial_product']
                self.assertLess(failure(e)**5,failure(e-1))
                self.assertTrue(0<=record['digit']<=4)
                self.assertGreater(q,target)
                self.assertLess(q-target,record['error_upper_bound'])
            self.assertTrue(all(e>target_e for e in counts))

    def test_real_convergence_does_not_preserve_prime_valuations(self):
        _,partial,records=greedy_infinite_prefix(1,24)
        target=failure(1)
        self.assertGreater(valuation(partial,3),valuation(target,3))
        self.assertLess(partial-target,Q(1,4**23))
        self.assertNotEqual(partial.denominator,target.denominator)

    def test_second_exact_scope_query_separates_the_infinite_mimic(self):
        target=failure(1)
        self.assertEqual(compare_scope_queries(target,target)['status'],'conditional_finitude_certificate')
        self.assertEqual(compare_scope_queries(target,Q(1))['status'],'finite_candidate_rejected_under_expanded_class')
        self.assertEqual(compare_scope_queries(target,Q(1,2))['status'],'inconsistent_with_unguarded_restriction')
        # Every prefix of the e>=2 mimic has no route contained in decoded {0}.
        counts,partial,_=greedy_infinite_prefix(1,24)
        routes=[(decode_support(e),frozenset(),n) for e,n in counts.items()]
        self.assertEqual(guarded_probability(routes,lambda i:i==0),1)
        # Adding a guarded inside route defeats the expanded equality inference:
        # at all-issued it is blocked; under {0} it supplies exactly target.
        guarded=routes+[(frozenset({0}),frozenset({1}),1)]
        self.assertEqual(guarded_probability(guarded,lambda i:True),partial)
        self.assertEqual(guarded_probability(guarded,lambda i:i==0),target)
        # Full-profile equality with target arises only in the proved infinite limit.

if __name__=='__main__':unittest.main(verbosity=2)
