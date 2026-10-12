import unittest
from intentions import run
class ContentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run();cls.c=cls.r['cases']
 def test_actual_plan_derived_from_known_peer(self):
  c=self.c['actual_whole_end_known_peer_plan'];self.assertTrue(c['means_end_policy_satisfied'] and c['peer_knowledge_factive'] and c['whole_end_satisfied'])
 def test_frozen_total_state_not_admissible_after_suppression(self):
  c=self.c['suppression_freeze_everything'];self.assertFalse(c['peer_knowledge_factive'] or c['output_knowledge_factive'])
 def test_relevant_knowledge_changes_selected_means(self):
  c=self.c['change_knowledge_freeze_used_command'];self.assertTrue(c['peer_knowledge_factive']);self.assertFalse(c['means_end_policy_satisfied'])
 def test_solo_repair_changes_exercise(self):
  c=self.c['replan_preserve_end_change_exercise'];self.assertTrue(c['whole_end_satisfied']);self.assertEqual(c['state']['command'],2)
 def test_through_peer_is_not_repaired_by_same_output(self):
  c=self.c['through_peer_solo_repair'];self.assertTrue(c['whole_end_satisfied']);self.assertFalse(c['through_peer_content_satisfied'])
 def test_factive_accompaniment_does_not_change_productive_scope(self):
  a=self.c['intrinsic_symmetric_plan_actual'];b=self.c['accompaniment_covaries_productive_state_fixed']
  self.assertTrue(b['peer_knowledge_factive'] and b['output_knowledge_factive']);self.assertEqual(a['productive_relevance_scope'],b['productive_relevance_scope']);self.assertEqual(a['state']['command'],b['state']['command']);self.assertFalse(b['whole_end_satisfied'])
 def test_or_relevant_state_survives_with_factive_covariance(self):
  a=self.c['or_accompaniment_actual'];b=self.c['or_accompaniment_covaries_productive_state_fixed']
  self.assertTrue(b['peer_knowledge_factive'] and b['output_knowledge_factive'] and b['whole_end_satisfied']);self.assertEqual(a['state']['command'],b['state']['command'])
 def test_passive_factivity_does_not_mean_productive_sufficiency(self):
  p=self.r['passive_knower_control'];self.assertTrue(p['full_factive_knowing_state_entails_output']);self.assertFalse(p['therefore_entailment_alone_identifies_productive_completion']);self.assertTrue(all(not w['observer_productive_support'] for w in p['worlds']))
if __name__=='__main__':unittest.main(verbosity=2)
