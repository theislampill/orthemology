import unittest
from unittest.mock import patch
from joint_end import Model, make_context
from selection_probe import participation_options, policy_domain, evaluate_profile

class SelectionProbeTests(unittest.TestCase):
    def test_three_way_participation_reason_control(self):
        for q in range(3):
            ctx=make_context(q,'joint')
            product=participation_options(ctx,'A','product')
            own=participation_options(ctx,'A','own')
            joint=participation_options(ctx,'A','joint')
            self.assertEqual(len(product),4)
            self.assertEqual(len(own),3)
            self.assertEqual(own,joint)
            self.assertIn(None,product)
            self.assertNotIn(None,joint)
            self.assertEqual({a.setting for a in joint},set(ctx['originals']['A'].repertoire))

    def test_full_domain_constructed_without_calling_interpreter(self):
        ctx=make_context(0,'joint')
        with patch.object(Model,'execute',side_effect=AssertionError('Outcome consultation')):
            domain=policy_domain(ctx,'joint',use_inherited_means=False)
            selected=policy_domain(ctx,'joint',use_inherited_means=True)
        self.assertEqual(len(domain),9)
        self.assertEqual(len(selected),1)

    def test_relation_requirement_without_means_does_not_filter_for_success(self):
        for q in range(3):
            ctx=make_context(q,'joint')
            domain=policy_domain(ctx,'joint',use_inherited_means=False)
            outcomes=[evaluate_profile(ctx,p,'joint') for p in domain]
            self.assertTrue(all(o['goal_directed_coproduction'] for o in outcomes))
            self.assertEqual(sum(o['stated_end_satisfied'] for o in outcomes),3)
            self.assertEqual(sum(not o['stated_end_satisfied'] for o in outcomes),6)

    def test_inherited_means_selects_same_policy_for_own_and_joint(self):
        for q in range(3):
            ctx=make_context(q,'joint')
            own=policy_domain(ctx,'own',use_inherited_means=True)
            joint=policy_domain(ctx,'joint',use_inherited_means=True)
            product=policy_domain(ctx,'product',use_inherited_means=True)
            self.assertEqual(own,joint)
            self.assertEqual(len(joint),1)
            self.assertEqual(len(product),4)
            self.assertTrue(evaluate_profile(ctx,joint[0],'joint')['stated_end_satisfied'])
            self.assertFalse(any(evaluate_profile(ctx,joint[0],'joint')['base']['entire'].values()))
            self.assertEqual(sum(evaluate_profile(ctx,p,'product')['stated_end_satisfied'] for p in product),3)

    def test_local_joint_selection_does_not_command_peer(self):
        ctx=make_context(0,'joint')
        a,b=policy_domain(ctx,'joint',use_inherited_means=True)[0]
        before=participation_options(ctx,'A','joint')
        cut=evaluate_profile(ctx,(a,None),'joint')
        self.assertEqual(before,participation_options(ctx,'A','joint'))
        self.assertTrue(cut['product_satisfied'])
        self.assertFalse(cut['stated_end_satisfied'])
        self.assertIs(cut['base']['acts'][0],a)
        self.assertNotIn((a,None),policy_domain(ctx,'joint',use_inherited_means=True))

    def test_concentration_preserves_external_work_not_two_participant_end(self):
        for q in range(3):
            ctx=make_context(q,'joint'); original=ctx['originals']['A']
            a,b=policy_domain(ctx,'joint',use_inherited_means=True)[0]
            pair=evaluate_profile(ctx,(a,b),'joint'); solo=evaluate_profile(ctx,(a,None),'joint')
            self.assertIs(ctx['originals']['A'],original)
            self.assertEqual(pair['base']['events'],solo['base']['events'])
            self.assertEqual(solo['base']['events'],ctx['catalogue'].targets[q])
            self.assertTrue(all(providers==frozenset(('A',)) for providers in solo['base']['entire'].values()))
            self.assertFalse(solo['stated_end_satisfied'])
            self.assertTrue(pair['stated_end_satisfied'])

if __name__=='__main__':unittest.main(verbosity=2)
