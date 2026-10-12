import unittest
from causal_transfer import Model, modified_causes, run

class TransferTests(unittest.TestCase):
    def test_or_is_one_conjunctive_modified_cause(self):
        self.assertEqual(modified_causes(Model('parallel'), (1,1)), [('A','B')])
    def test_preemption_is_asymmetric(self):
        self.assertEqual(modified_causes(Model('left'), (1,1)), [('A',)])
        self.assertEqual(modified_causes(Model('right'), (1,1)), [('B',)])
    def test_and_control(self):
        self.assertEqual(modified_causes(Model('and'), (1,1)), [('A',),('B',)])
    def test_concordant_laws_need_two_disallowed_queries(self):
        r=run()['concordant_identification']
        self.assertEqual(r['compatible_with_concordant_data'],4)
        self.assertEqual(r['minimal_identifying_extra_query_sets'],[[[0,1],[1,0]]])
        self.assertTrue(r['all_required_extra_queries_outside_admitted_diagonal'])
    def test_signature_and_all_interventions(self):
        r=run()
        self.assertEqual(r['root_output_intervention_comparisons'],108)
        self.assertTrue(r['all_three_output_tables_equal'])
        self.assertFalse(r['conjunctive_negative_control_equal'])
        self.assertFalse(r['route_predicate_fibre_constant'])
        self.assertTrue(r['fine_intervention_breaks_coarse_empty_mapping'])

if __name__=='__main__': unittest.main()
