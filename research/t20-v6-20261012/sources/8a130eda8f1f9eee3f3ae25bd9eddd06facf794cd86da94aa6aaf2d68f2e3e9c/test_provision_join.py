"""Contract for a read-only shared semantic adapter, before implementation."""
import unittest
from provision_join import inspect_case, candidate_vs_used

class JoinContract(unittest.TestCase):
    def test_direct_joint_has_witnesses_not_single_cover(self):
        r=inspect_case('coalescence')
        self.assertEqual(r['witness_bearers'], ['A','B'])
        self.assertTrue(r['all_contributions_have_original_resource'])
        self.assertEqual(r['complete_same_bearers'], [])
        self.assertEqual(r['first_joint_events'], ['e'])
    def test_mechanism_moves_first_joint_node(self):
        r=inspect_case('persistent_created_mechanism')
        self.assertEqual(r['first_joint_events'], ['m'])
        self.assertEqual(r['event_roots'], {'e':['A','B'],'m':['A','B']})
        self.assertEqual(r['complete_same_bearers'], [])
    def test_priority_does_not_use_issued_b(self):
        r=inspect_case('priority_A')
        self.assertEqual(r['issued_bearers'], ['A','B'])
        self.assertEqual(r['witness_bearers'], ['A'])
        self.assertEqual(r['complete_same_bearers'], ['A'])
        self.assertEqual(r['first_joint_events'], [])
    def test_candidate_trace_is_not_actual_trace(self):
        r=candidate_vs_used()
        self.assertIn('B',r['candidate_bearers'])
        self.assertNotIn('B',r['actual_bearers'])
        self.assertNotEqual(r['candidate_bearers'],r['actual_bearers'])
    def test_source_mode_classification_not_forced(self):
        r=inspect_case('coalescence')
        self.assertFalse(r['participation_implies_complete'])
        self.assertTrue(r['atomic_incidence_unique_source'])
    def test_shared_effect_is_not_two_created_bearers(self):
        r=inspect_case('coalescence')
        self.assertEqual(r['created_bearer_events'], ['e'])
        self.assertEqual(len(r['actual_contribution_incidences']),2)
    def test_actual_original_requisites_propagate_without_new_root(self):
        r=inspect_case('persistent_created_mechanism')
        self.assertEqual(r['original_requisites'], {'e':['input-A','input-B'],'m':['input-A','input-B']})
        self.assertEqual(r['overlap_witnesses'], [{'effects':['e','m'],'shared':['input-A','input-B']}])
    def test_actual_tokens_stay_rigid(self):
        r=inspect_case('persistent_created_mechanism')
        self.assertTrue(r['actual_contribution_incidences'])
        for c in r['actual_contribution_incidences']:
            self.assertEqual(c['standing_resource'], 'resource-'+c['bearer'])
            self.assertEqual(c['intrinsic_act'], 'act-'+c['bearer'])
if __name__ == '__main__': unittest.main()
