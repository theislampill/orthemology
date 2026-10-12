"""Exact finite and rational tests. They assert no real-world metaphysical model."""
import unittest
from fractions import Fraction as F
from itertools import product
from diagnostics import (
    bayes_uncaused, posterior_interval, validate_law, exchangeable,
    covariance, bernoulli_mixture, fixed_heads_law, uniform_beta_word,
    minimal_supports, common_requisite_check, rotating_witness_model,
    restricted_explanation_model, audit_boolean_explanation_model,
    hierarchy_examples, semantic_transfer,
)


class ProbabilityTests(unittest.TestCase):
    def test_bayes_requires_type_likelihood(self):
        self.assertEqual(bayes_uncaused(F(1,1000),F(1,100),F(1,1000)), F(1,101))
    def test_worst_case_is_not_bayes_identity(self):
        self.assertEqual(bayes_uncaused(F(1,1000),F(1,100),F(1)), F(10,11))
    def test_bayes_zero_type_likelihood(self):
        self.assertEqual(bayes_uncaused(F(1,1000),F(1,100),F(0)), F(0))
    def test_bayes_illegal_joint_mass(self):
        with self.assertRaises(ValueError): bayes_uncaused(F(3,4),F(1,2),F(1,2))
    def test_bayes_empty_event(self):
        with self.assertRaises(ValueError): bayes_uncaused(F(0),F(0),F(0))
    def test_likelihood_interval_can_inform(self):
        lo,hi=posterior_interval(F(99,100),F(1,2),F(0),F(1))
        self.assertEqual((lo,hi),(F(99,101),F(1)))
    def test_interval_monotonicity(self):
        a=posterior_interval(F(1,2),F(1,4),F(0),F(1))
        b=posterior_interval(F(1,2),F(1,4),F(1,8),F(1,2))
        self.assertLessEqual(a[0],b[0]); self.assertGreaterEqual(a[1],b[1])
    def test_interval_invalid(self):
        with self.assertRaises(ValueError): posterior_interval(F(1,2),F(1,2),F(3,4),F(1,4))
    def test_nonexchangeable_coherent_law(self):
        law={(0,0):F(1,8),(0,1):F(1,8),(1,0):F(3,8),(1,1):F(3,8)}
        self.assertEqual(validate_law(law),2); self.assertFalse(exchangeable(law))
    def test_exchangeable_not_iid_mixture(self):
        law=fixed_heads_law(2,1)
        self.assertTrue(exchangeable(law)); self.assertEqual(covariance(law),F(-1,4))
    def test_iid_mixture_covariance(self):
        law=bernoulli_mixture(2,[(F(1,2),F(1,4)),(F(1,2),F(3,4))])
        self.assertTrue(exchangeable(law));self.assertEqual(covariance(law),F(1,16))
    def test_covariance_nonnegative_grid(self):
        for p,q,w in product([F(i,4) for i in range(5)],repeat=3):
            self.assertGreaterEqual(covariance(bernoulli_mixture(2,[(w,p),(1-w,q)])),0)
    def test_beta_word_probabilities(self):
        self.assertEqual(uniform_beta_word(2,1),F(1,6))
        self.assertEqual(uniform_beta_word(2,0),F(1,3))
    def test_beta_consistency(self):
        for n in range(1,9):
            for k in range(n+1):
                self.assertEqual(uniform_beta_word(n,k),uniform_beta_word(n+1,k)+uniform_beta_word(n+1,k+1))
    def test_urn_normalization(self):
        for n in range(1,7):
            for k in range(n+1): self.assertEqual(sum(fixed_heads_law(n,k).values()),1)
    def test_invalid_law_negative(self):
        with self.assertRaises(ValueError): validate_law({(0,):F(-1),(1,):F(2)})
    def test_invalid_law_mass(self):
        with self.assertRaises(ValueError): validate_law({(0,):F(1,2)})
    def test_invalid_mixture(self):
        with self.assertRaises(ValueError): bernoulli_mixture(2,[(F(1,2),F(1,2))])

class CausalTests(unittest.TestCase):
    def test_or_two_minimal_supports(self):
        self.assertEqual(minimal_supports(2,[0,1,1,1]),[(0,),(1,)])
    def test_and_one_joint_support(self):
        self.assertEqual(minimal_supports(2,[0,0,0,1]),[(0,1)])
    def test_projection_one_support(self):
        self.assertEqual(minimal_supports(2,[0,1,0,1]),[(0,)])
    def test_constant_true_empty_support(self):
        self.assertEqual(minimal_supports(2,[1,1,1,1]),[()])
    def test_constant_false_no_support(self):
        self.assertEqual(minimal_supports(2,[0,0,0,0]),[])
    def test_xor_rejected(self):
        with self.assertRaises(ValueError): minimal_supports(2,[0,1,1,0])
    def test_background_must_be_kept(self):
        # E=(A or B) and L: bit0=A, bit1=B, bit2=L.
        table=[bool((s&1 or s&2) and s&4) for s in range(8)]
        self.assertEqual(minimal_supports(3,table),[(0,2),(1,2)])
    def test_bad_table(self):
        with self.assertRaises(ValueError): minimal_supports(2,[0,1])

class ModalTests(unittest.TestCase):
    def test_common_requisite_theorem_exhaustive(self):
        for worlds in product(list(product([False,True],repeat=3)),repeat=3):
            result=common_requisite_check(worlds)
            self.assertTrue(result['implication_valid'])
    def test_common_requisite_no_contingent_instance(self):
        result=common_requisite_check([(1,0,1),(0,1,1)])
        self.assertTrue(result['premises']);self.assertTrue(result['r_necessary'])
    def test_bad_recombination_breaks_premise(self):
        result=common_requisite_check([(1,0,1),(0,1,0)])
        self.assertFalse(result['premises'])
    def test_rotating_truthmaker_witness(self):
        r=rotating_witness_model()
        self.assertTrue(r['ns_prime']);self.assertTrue(r['p_implies_r']);self.assertTrue(r['n0_implies_r'])
        self.assertFalse(r['same_negative_witness_everywhere']);self.assertTrue(r['r_contingent'])
        self.assertTrue(r['removed_r_world_has_another_negative_witness'])

class ExplanationTests(unittest.TestCase):
    def test_restricted_reverse_part_gap(self):
        r=restricted_explanation_model()
        self.assertTrue(r['restricted_package']);self.assertTrue(r['outside_target'])
        self.assertTrue(r['target_part_of_explainer']);self.assertFalse(r['reverse_externality'])
    def test_boolean_totality_locality(self):
        r=audit_boolean_explanation_model()
        self.assertEqual(r['facts'],15);self.assertEqual(r['nonempty_pluralities'],32767)
        self.assertEqual(r['total_explainers'],[1]);self.assertEqual(r['local_explainers'],[1,2,4])
        self.assertTrue(all(r['axioms'].values()))
    def test_upward_padding_breaks_nec(self):
        r=audit_boolean_explanation_model(padded=True)
        self.assertFalse(r['axioms']['no_extended_circles'])
        self.assertFalse(r['axioms']['total_explainer_unique'])
    def test_two_level_knowledge_not_automatic(self):
        r=hierarchy_examples()
        self.assertTrue(r['first_order_known']);self.assertFalse(r['knows_that_knows'])
        self.assertTrue(r['reflexive']);self.assertFalse(r['transitive'])
    def test_attributes_not_fact_parts(self):
        r=semantic_transfer('fact_atomicity_to_attribute_identity')
        self.assertTrue(r['antecedent']);self.assertFalse(r['conclusion']);self.assertFalse(r['bridge_supplied'])
    def test_unknown_transfer_rejected(self):
        with self.assertRaises(ValueError): semantic_transfer('prove_god')

if __name__=='__main__': unittest.main()
