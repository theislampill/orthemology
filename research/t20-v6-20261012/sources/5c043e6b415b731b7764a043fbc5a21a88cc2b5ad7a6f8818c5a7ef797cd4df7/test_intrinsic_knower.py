import unittest
from intrinsic_knower import run,forecast_from_intrinsic_reasons,powerset
class KnowerTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_foreknowledge_is_derived_without_reading_execution(self):
  self.assertTrue(all(w['factive'] and not w['choice_peer_execution_input'] for w in self.r['worlds']))
 def test_intrinsic_reason_context_yields_complete_knowledge(self):
  self.assertTrue(all(w['all_subset_propositions_known_iff_true'] for w in self.r['complete_knowledge_checks']))
 def test_same_standing_knowing_tokens_persist(self):
  worlds=self.r['worlds'];self.assertTrue(all(w['standing_knowledge']==worlds[0]['standing_knowledge'] for w in worlds))
 def test_nonreceipt_is_typed_and_mutation_sensitive(self):
  self.assertTrue(all(self.r['original_nonreceipt_represented'].values()));self.assertTrue(self.r['foreign_donation_negative_control_detected'])
 def test_truth_relation_is_not_covert_efficient_arrow(self):
  self.assertNotIn(['B_act','K_A'],self.r['relation_types']['efficient_productive'])
 def test_frozen_normal_forecast_does_not_survive_policy_violation(self):
  self.assertFalse(self.r['suppression_control']['fixed_predicted_content_factive'])
if __name__=='__main__':unittest.main(verbosity=2)
