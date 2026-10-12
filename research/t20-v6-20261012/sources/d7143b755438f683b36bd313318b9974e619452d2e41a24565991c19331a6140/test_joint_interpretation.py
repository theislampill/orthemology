import unittest
from joint_interpretation import run
class JointTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run();cls.rows=cls.r['records']
 def test_same_candidate_realizes_own_full_target_ends(self):
  self.assertTrue(all(all(row['joint']['individual_own_activity_ends_satisfied'].values()) and all(row['joint']['exact_intention_satisfied'].values()) for row in self.rows))
 def test_each_remaining_own_end_survives_peer_suppression(self):
  self.assertTrue(all(row['A_own_end_survives'] and row['created_output_equal'] for row in self.rows))
 def test_global_participation_end_is_not_individual_end(self):
  self.assertTrue(all(row['joint']['both_participate_total_end'] and not row['solo_same_A_act']['both_participate_total_end'] for row in self.rows))
 def test_factive_knowledge_covaries_without_command_change(self):
  self.assertTrue(all(row['joint']['knowledge_factive'] and row['solo_same_A_act']['knowledge_factive'] and not row['A_total_knowledge_unchanged'] and row['A_intrinsic_command_and_target_unchanged'] for row in self.rows))
 def test_branch_label_switch_is_not_semantic_condition_failure(self):
  self.assertTrue(all(row['uniform_rule_names_equal'] and row['reencoding_preserves_created_output_support_and_intentions'] for row in self.rows))
 def test_actual_contributors_are_both_roots(self):
  self.assertTrue(all(all(roots==['A','B'] for roots in row['joint']['supports'].values()) for row in self.rows))
 def test_fixed_active_rule_not_preserved(self):
  self.assertTrue(all(not row['actual_rule_equal'] and not row['actual_support_equal'] for row in self.rows))
 def test_CND_is_not_nonvacuous_whole_effect_coverage(self):
  self.assertTrue(all(row['joint']['CND_whole_event'] and not row['joint']['whole_event_entire_coverage'] for row in self.rows))
 def test_primitive_entire_relation_cannot_hide_scope_failure(self):
  self.assertTrue(all(not row['any_attribution_has_CND_coverage_and_exclusive_entire_meaning'] for row in self.rows))
 def test_weak_participation_multiple_event_allocation_failure(self):
  row=next(row for row in self.rows if len(row['target'])==2)
  self.assertEqual(row['weak_participation_cover_count'],7);self.assertEqual(row['exact_command_intention_preserving_cover_count'],1)
 def test_opposed_commands_do_not_get_fake_exact_will_success(self):
  self.assertFalse(any(self.r['opposed_command_control']['exact_intention_satisfied'].values()))
if __name__=='__main__':unittest.main(verbosity=2)
