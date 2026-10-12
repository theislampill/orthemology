import unittest
import implicit_attestation as i

class ImplicitAttestationControls(unittest.TestCase):
    def test_nonconventional_positive_has_no_rule_or_endorsement_words(self):
        w=i.positive_case()
        self.assertEqual(w['action'],'send_mantle')
        self.assertTrue(w['intended_positive_claim'])
        self.assertEqual(w['prior_credential_rules'],[])
        self.assertEqual(w['source_endorsement_utterances'],[])
        self.assertFalse(w['communicative_goal_removed_still_sends'])

    def test_same_visible_transfer_can_have_other_purposes(self):
        cases=i.purpose_rivals()
        self.assertEqual(cases['positive']['action'],cases['maintenance']['action'])
        self.assertEqual(cases['positive']['action'],cases['courtesy']['action'])
        self.assertFalse(cases['maintenance']['intended_positive_claim'])
        self.assertFalse(cases['courtesy']['intended_positive_claim'])
        self.assertTrue(cases['appropriation']['token_reaches_E'])
        self.assertFalse(cases['appropriation']['source_voluntary_transfer'])

    def test_contextual_interventions_discriminate_reasons(self):
        t=i.intervention_table()
        self.assertEqual(t['positive']['remove_question'],'keep')
        self.assertEqual(t['maintenance']['remove_question'],'send_mantle')
        self.assertEqual(t['maintenance']['remove_practical_need'],'keep')
        self.assertEqual(t['courtesy']['remove_practical_need'],'keep')
        self.assertEqual(t['question_courtesy']['remove_question'],'keep')
        self.assertEqual(t['question_courtesy']['known_false_claim'],'send_mantle')
        self.assertEqual(t['positive']['known_false_claim'],'reject_claim')

    def test_separate_choice_episodes_constrain_policy_without_an_intent_observation(self):
        result=i.calibration_result()
        self.assertGreater(result['initial_policies'],result['surviving_policies'])
        self.assertGreater(result['surviving_policies'],0)
        self.assertTrue(result['all_regular_survivors_select_communicative_plan'])
        self.assertTrue(result['selective_courtesy_matches_calibration_and_target_action'])
        self.assertFalse(result['selective_courtesy_intends_positive_claim'])

    def test_communicative_intention_is_not_truth(self):
        cases=i.false_claim_controls()
        self.assertTrue(cases['mistaken']['intended_positive_claim'])
        self.assertFalse(cases['mistaken']['commission_claim_true'])
        self.assertTrue(cases['deceptive']['intended_positive_claim'])
        self.assertFalse(cases['deceptive']['commission_claim_true'])

    def test_equal_reason_scores_preserve_intention_ambiguity(self):
        w=i.execute(i.Policy(communicate=4,repair=4),i.Situation(repair_needed=True))
        self.assertEqual(w['action'],'send_mantle')
        self.assertIsNone(w['intended_positive_claim'])

    def test_defeasible_weights_do_not_become_empirical_certainty(self):
        rows=i.defeasible_sensitivity()
        self.assertEqual(rows[0]['conditional_purpose_probability'],'999/1000')
        self.assertEqual(rows[-1]['conditional_purpose_probability'],'1/2')
        self.assertTrue(all(r['strong_rival_retained'] for r in rows))

if __name__=='__main__':unittest.main(verbosity=2)
