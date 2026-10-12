"""Tests of research claims, written before implementation.

Each assertion is vulnerable to a concrete mutation: collapse roots into ultimate-goal
labels; confuse actual and expected recognition; discard ties; remove residual value;
call ordinary channel/menu probes separating; or count one crossover observation as
universal identification.
"""
import unittest
import recovery

class RecoveryClaims(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = recovery.run_experiment()

    def test_standard_interventions_do_not_identify_mixed_intention(self):
        self.assertEqual(self.r.get('standard_decisions_checked'), 112)
        self.assertIs(self.r.get('standard_pairs_same_unique_actions'), True)
        self.assertIs(self.r.get('target_pair_differs_in_intended_answer'), True)

    def test_end_means_and_material_roots_are_distinct(self):
        self.assertEqual(self.r.get('intended_answer_by_recipe'), {
            'indication_end': True, 'belief_end': True,
            'gratitude_through_belief': True, 'material_only': False,
            'mixed_indication_material': True})

    def test_hostility_does_not_cancel_indication(self):
        self.assertIs(self.r.get('hostility_indication_preserved'), True)
        self.assertIs(self.r.get('hostile_recipient_accepts'), False)

    def test_failed_decoding_does_not_cancel_attempt(self):
        self.assertIs(self.r.get('failed_decoding_intended_answer'), True)
        self.assertIs(self.r.get('failed_decoding_actual_recognition'), False)

    def test_exact_matched_crossover_requires_two_single_action_observations(self):
        self.assertEqual(self.r.get('matched_crossover_minimal_probe_count'), 2)
        self.assertIs(self.r.get('matched_crossover_identifies_restricted_class'), True)
        self.assertIs(self.r.get('each_single_probe_has_opposite_intention_collision'), True)

    def test_latent_beliefs_and_unmatched_values_break_crossover(self):
        self.assertIs(self.r.get('hidden_channel_belief_collision'), True)
        self.assertIs(self.r.get('private_action_value_collision'), True)

    def test_ties_are_possibility_compatible_without_intention_certification(self):
        self.assertEqual(self.r.get('tie_actions'), ['keep', 'mantle'])
        self.assertEqual(self.r.get('tie_intention_values'), [False, True])
        self.assertIs(self.r.get('observed_mantle_possibility_compatible'), True)

    def test_no_public_adoption_or_truth_classifier_is_supplied(self):
        self.assertIs(self.r.get('public_adoption_computed'), False)
        self.assertIs(self.r.get('commission_truth_in_planning'), False)

    def test_positive_appraisal_without_goal_commitment_is_not_intention(self):
        self.assertIs(self.r.get('uncommitted_positive_appraisal_intends_answer'), False)
        self.assertIs(self.r.get('uncommitted_appraisal_still_positive'), True)

    def test_commitment_changes_post_failure_retry_when_cost_is_low_enough(self):
        self.assertEqual(self.r.get('post_failure_retry_actions'), {
            'committed_mixed': 'retry', 'material_only': 'keep',
            'uncommitted_appraisal': 'keep'})

    def test_both_structural_policies_extend_to_the_old_calibrations(self):
        self.assertEqual(self.r.get('old_calibration_actions'), {
            'material_only': ['keep', 'reject', 'mantle', 'mantle'],
            'committed_mixed': ['keep', 'reject', 'mantle', 'mantle']})

    def test_finite_negative_retries_leave_positive_goal_values(self):
        self.assertIs(self.r.get('finite_retry_nondetection_has_positive_witness'), True)
        self.assertIs(self.r.get('positive_cost_floor_retains_positive_witness'), True)
        self.assertIs(self.r.get('tested_positive_values_eventually_retry_on_geometric_costs'), True)

if __name__ == '__main__': unittest.main()
