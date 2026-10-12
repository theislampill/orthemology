import unittest
from joint_end import Model, End, make_context, ordinary_choices, execute, forecast, satisfies, active_solutions, source_comparison, shifted_product

class ValuedCooperationTests(unittest.TestCase):
    def test_richer_end_is_declared_before_ordinary_choice_and_factive_forecast(self):
        for q in range(3):
            ctx=make_context(q,'joint')
            choices=ordinary_choices(ctx)
            self.assertEqual(len(choices),2)
            self.assertTrue(all(c.end.kind=='joint' for c in choices))
            predicted=forecast(ctx)
            actual=execute(ctx,choices)
            self.assertEqual(predicted,actual)
            self.assertTrue(all(actual['full_end_satisfied'].values()))
            self.assertTrue(all(not p for p in actual['base']['entire'].values()))
            self.assertEqual(actual['base']['events'],ctx['catalogue'].targets[q])

    def test_richer_joint_goal_does_not_select_unique_coactive_plan(self):
        for q in range(3):
            ctx=make_context(q,'joint')
            plans=active_solutions(ctx)
            self.assertEqual(len(plans),3)
            self.assertTrue(all(all(execute(ctx,p)['full_end_satisfied'].values()) for p in plans))
            expected=ordinary_choices(ctx)
            self.assertEqual(sum(p==expected for p in plans),1)

    def test_frozen_richer_end_loses_peer_while_product_and_standing_repertoire_survive(self):
        for q in range(3):
            ctx=make_context(q,'joint'); a,b=ordinary_choices(ctx)
            prior=ctx['originals']['A'].repertoire
            cut=execute(ctx,(a,))
            self.assertIs(cut['choices'][0],a)
            self.assertEqual(cut['base']['events'],ctx['catalogue'].targets[q])
            self.assertTrue(cut['base']['own_activity_ends']['A'])
            self.assertFalse(cut['full_end_satisfied']['A'])
            self.assertFalse(cut['policy_conforms'])
            self.assertNotEqual(cut,forecast(ctx))
            self.assertEqual(ctx['originals']['A'].repertoire,prior)

    def test_revising_end_repairs_solo_goal_but_not_same_complete_intention(self):
        ctx=make_context(0,'joint'); a,b=ordinary_choices(ctx)
        revised=a.with_end(End(0,'own','A','B_original'))
        self.assertIs(revised.exercise,a.exercise)
        self.assertNotEqual(revised.end,a.end)
        self.assertTrue(execute(ctx,(revised,))['full_end_satisfied']['A'])
        self.assertFalse(execute(ctx,(a,))['full_end_satisfied']['A'])

    def test_product_or_belief_about_peer_does_not_supply_actual_relation(self):
        ctx=make_context(0,'joint'); a,b=ordinary_choices(ctx)
        cut=execute(ctx,(a,))
        cut['reported_peer_present']=True
        cut['reported_joint_success']=True
        self.assertFalse(satisfies(a.end,cut))
        self.assertTrue(satisfies(End(0,'own','A','B_original'),cut))
        self.assertNotEqual(forecast(ctx)['base']['acts'],cut['base']['acts'])

    def test_shared_intended_project_differs_from_accidental_equal_output(self):
        ctx=make_context(0,'joint'); a,b=ordinary_choices(ctx)
        changed_b=b.with_product_intention(1)
        actual=execute(ctx,(a,changed_b))
        self.assertEqual(actual['base']['events'],ctx['catalogue'].targets[0])
        self.assertEqual(actual['base']['supports'],execute(ctx,(a,b))['base']['supports'])
        self.assertFalse(actual['full_end_satisfied']['A'])
        self.assertFalse(actual['policy_conforms'])

    def test_domain_is_not_success_filter_when_observed_product_is_perturbed(self):
        ctx=make_context(0,'joint'); before=ordinary_choices(ctx)
        actual=execute(ctx,before,product_transform=shifted_product)
        self.assertEqual(before,ordinary_choices(ctx))
        self.assertTrue(actual['joint_relation'])
        self.assertFalse(any(actual['full_end_satisfied'].values()))

    def test_peer_originality_and_designated_identity_are_additional_contents(self):
        r=source_comparison(0)
        self.assertTrue(r['plural']['generic_joint_end'])
        self.assertTrue(r['derived']['generic_joint_end'])
        self.assertTrue(r['plural']['original_peer_end'])
        self.assertFalse(r['derived']['original_peer_end'])
        self.assertTrue(r['plural']['designated_B_end'])
        self.assertFalse(r['derived']['designated_B_end'])
        self.assertEqual(r['plural']['original_roots'],frozenset(('A_original','B_original')))
        self.assertEqual(r['derived']['original_roots'],frozenset(('A_original',)))

    def test_created_peer_comparison_retains_extra_created_requisites(self):
        r=source_comparison(0)
        self.assertEqual(r['plural']['local_product'],r['derived']['local_product'])
        self.assertNotEqual(r['plural']['created_inventory'],r['derived']['created_inventory'])
        self.assertTrue({'C_created','C_power','C_will','C_act'} <= r['derived']['created_inventory'])
        self.assertTrue(r['derived']['local_product'] < r['derived']['created_inventory'])

    def test_baseline_original_resources_do_not_become_created_peer_resources(self):
        ctx=make_context(0,'joint'); result=execute(ctx,ordinary_choices(ctx))
        self.assertEqual(result['source_roots'],frozenset(('A_original','B_original')))
        self.assertFalse(any(target in {'A_P','A_K','B_P','B_K'} for _,target in result['efficient_edges']))
        self.assertTrue(result['structural_nonreceipt'])

if __name__=='__main__':unittest.main(verbosity=2)
