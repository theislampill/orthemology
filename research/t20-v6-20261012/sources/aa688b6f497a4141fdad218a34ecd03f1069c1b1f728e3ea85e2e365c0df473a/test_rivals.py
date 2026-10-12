"""Behavioral research controls written before the model implementation."""
import unittest
import rivals as r

class RivalControls(unittest.TestCase):
    def test_custody_does_not_set_purpose(self):
        a, b = r.token_case('attest'), r.token_case('repair')
        self.assertEqual(a.observations['received'], b.observations['received'])
        self.assertEqual(a.observations['transfer'], b.observations['transfer'])
        self.assertTrue(a.target['commission'])
        self.assertFalse(b.target['commission'])
        self.assertNotEqual(a.observations['prior_instruction'], b.observations['prior_instruction'])

    def test_scope_and_falsehood_are_not_erased(self):
        a = r.token_case('attest', fact=False)
        self.assertTrue(a.target['commission'])
        self.assertFalse(a.target['report_true'])
        self.assertFalse(r.token_case('arrival_only').target['commission'])
        self.assertTrue(r.token_case('arrival_only').target['sent'])

    def test_insincerity_cannot_be_read_from_public_undertaking(self):
        a = r.token_case('attest', sincere=True)
        b = r.token_case('attest', sincere=False)
        self.assertEqual(a.observations, b.observations)
        self.assertNotEqual(a.target['sincere'], b.target['sincere'])
        self.assertEqual(a.target['commission'], b.target['commission'])

    def test_fresh_challenge_does_not_set_origin_or_mission(self):
        a, b, c = [r.challenge_case(k,2) for k in ['envoy','maintenance','adaptive_counterfeit']]
        self.assertEqual(a.observations['challenge'], b.observations['challenge'])
        self.assertEqual(a.observations['challenge'], c.observations['challenge'])
        self.assertEqual(a.observations['source_action'], b.observations['source_action'])
        self.assertTrue(a.target['mission'])
        self.assertFalse(b.target['mission'])
        self.assertFalse(c.target['origin'])
        self.assertNotEqual(a.observations['source_action'], c.observations['source_action'])

    def test_authentic_source_response_may_be_appropriated(self):
        a = r.challenge_case('stolen_access',3)
        self.assertTrue(a.target['origin'])
        self.assertFalse(a.target['mission'])
        self.assertEqual(a.observations['challenge'],r.challenge_case('envoy',3).observations['challenge'])

    def test_instruction_does_not_authenticate_this_sign_or_its_delivery(self):
        a=r.challenge_case('envoy',2)
        b=r.challenge_case('aborted_envoy',2)
        c=r.challenge_case('diverted_to_other',2)
        self.assertEqual(a.observations['original_instruction'],b.observations['original_instruction'])
        self.assertEqual(a.observations['original_instruction'],c.observations['original_instruction'])
        self.assertEqual(a.observations['source_action'],c.observations['source_action'])
        self.assertTrue(a.target['mission'])
        self.assertFalse(b.target['mission'])
        self.assertFalse(c.target['mission'])
        self.assertTrue(c.target['origin'])
        self.assertNotEqual(a.observations['dispatch_record'],c.observations['dispatch_record'])

    def test_valid_amendment_allows_independent_replacement(self):
        a = r.institution_case(mutable=True,remove_voter=False,publish=True,appoint_time=4,descent=False)
        self.assertEqual(a.target['holder'],'N')
        self.assertTrue(a.target['amendment'])
        self.assertFalse(a.target['descent'])

    def test_current_votes_and_prior_constitution_matter(self):
        good = r.institution_case()
        entrenched = r.institution_case(mutable=False)
        stale = r.institution_case(remove_voter=True)
        self.assertEqual(good.observations['service'],entrenched.observations['service'])
        self.assertEqual(good.observations['vote_packet'],entrenched.observations['vote_packet'])
        self.assertEqual(good.observations['vote_packet'],stale.observations['vote_packet'])
        self.assertEqual(good.target['holder'],'N')
        self.assertEqual(entrenched.target['holder'],'P')
        self.assertEqual(stale.target['holder'],'P')

    def test_timing_publication_and_outage_are_separate(self):
        self.assertEqual(r.institution_case(publish=False).target['holder'],'P')
        self.assertEqual(r.institution_case(appoint_time=2).target['holder'],'P')
        good = r.institution_case(operational=False)
        self.assertEqual(good.target['holder'],'N')
        self.assertFalse(good.target['operational'])
        causal = r.institution_case(mutable=False,descent=True)
        self.assertTrue(causal.target['descent'])
        self.assertEqual(causal.target['holder'],'P')

    def test_lossy_words_support_different_force_and_truth(self):
        a,b = r.discourse_case('assert','P',0),r.discourse_case('quote','P',0)
        self.assertEqual(a.observations['received'],b.observations['received'])
        self.assertNotEqual(a.target['asserts_p0'],b.target['asserts_p0'])
        c = r.discourse_case('assert','Q',1)
        self.assertEqual(a.observations['received'],c.observations['received'])
        self.assertTrue(a.target['embedded_true'])
        self.assertFalse(c.target['embedded_true'])

    def test_true_report_is_not_endorsement_of_embedded_falsehood(self):
        a = r.discourse_case('report','Q',1)
        self.assertTrue(a.target['outer_true'])
        self.assertFalse(a.target['embedded_true'])
        self.assertFalse(a.target['asserts_p0'])

    def test_no_discriminator_with_corrupted_observation_channels(self):
        a,b = r.token_case('attest'),r.token_case('repair')
        b.observations = a.observations.copy()
        self.assertEqual(r.minimal_discriminators([a,b],'commission'),[])

    def test_computation_finds_required_independent_evidence(self):
        worlds=[r.token_case(k) for k in r.TOKEN_KINDS]
        self.assertIn(('prior_instruction','transfer'),r.minimal_discriminators(worlds,'commission'))
        worlds=[r.discourse_case(k,s,t) for k in ['assert','quote','report'] for s in ['P','Q'] for t in [0,1]]
        self.assertIn(('context_record','full_frame'),r.minimal_discriminators(worlds,'asserts_p0'))

if __name__=='__main__': unittest.main(verbosity=2)
