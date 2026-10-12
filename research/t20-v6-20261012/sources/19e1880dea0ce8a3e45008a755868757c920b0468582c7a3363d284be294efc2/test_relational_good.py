import unittest
from relational_good import run,end_satisfied,original_roots
class RelationalTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_created_target_is_not_relabelled(self):
  for row in self.r['finite_families']:self.assertTrue(row['A_solo_constructs_same_created_target'])
 def test_total_end_is_not_reduced_to_created_effect(self):
  for row in self.r['finite_families']:
   self.assertFalse(row['A_solo_attains_relational_good']);self.assertFalse(row['B_solo_attains_relational_good'])
 def test_participation_selects_split_without_equal_share_norm_at_two(self):
  self.assertEqual(self.r['finite_families'][1]['relational_good_profiles'],[(1,1)])
 def test_participation_does_not_always_select_allocation(self):
  self.assertEqual(self.r['finite_families'][2]['relational_good_profiles'],[(1,2),(2,1)])
  self.assertFalse(self.r['continuous_countercontrol']['therefore_positive_participation_alone_selects_unique_allocation'])
 def test_derived_coactor_preserves_two_genuine_act_bearers(self):
  p=self.r['provenance_controls'];self.assertEqual(p['immediate_act_bearers']['derivative'],['A','C']);self.assertEqual(p['original_root_supports']['derivative_coactor'],['A_original'])
 def test_independent_coactor_adds_original_support(self):
  self.assertEqual(self.r['provenance_controls']['original_root_supports']['original_coactor'],['A_original','B_original'])
 def test_actual_actor_identity_not_original_provision_identity(self):
  self.assertFalse(self.r['provenance_controls']['two_actors_equals_two_original_sources'])
if __name__=='__main__':unittest.main(verbosity=2)
