import unittest
from determination_contract import Model, Context, Plan, Determination, derive_means, reason_projection, factors_through, execute_declared, validate_certificate, standing_settings

class DeterminationContractTests(unittest.TestCase):
    def test_target_and_explicit_role_derive_means_without_value_ranking(self):
        for q in range(3):
            for d in range(3):
                ctx=Context(q,d); cert=derive_means(ctx)
                self.assertEqual(cert.plan,Plan((q+2*d)%3,(q-2*d)%3))
                self.assertTrue(validate_certificate(cert))
                self.assertEqual((cert.plan.a-cert.plan.b)%3,d)
                self.assertFalse(cert.establishes_normative_eligibility)
                self.assertFalse(cert.establishes_source_complete_will)

    def test_coarse_end_omits_particularizing_data_without_refuting_every_selector(self):
        contexts=tuple(Context(q,d) for q in range(3) for d in range(3))
        plans={c:derive_means(c).plan for c in contexts}
        self.assertFalse(factors_through(contexts,reason_projection,plans))
        self.assertTrue(factors_through(contexts,lambda c:(c.q,c.role_delta),plans))
        # A q-only policy exists on the explicitly equal-role subdomain.
        diagonal=tuple(c for c in contexts if c.role_delta==0)
        self.assertTrue(factors_through(diagonal,reason_projection,plans))

    def test_role_coordinate_reencodes_fixed_target_choice_without_justifying_it(self):
        for q in range(3):
            forward={d:derive_means(Context(q,d)).plan for d in range(3)}
            backward={(p.a-p.b)%3:p for p in forward.values()}
            self.assertEqual(forward,backward)
            self.assertEqual(len(set(forward.values())),3)
            for d,p in forward.items():
                swapped=derive_means(Context(q,(-d)%3)).plan
                self.assertEqual(swapped,Plan(p.b,p.a))
                self.assertEqual(swapped==p,d==0)

    def test_declared_choice_token_does_not_supply_reason_certificate(self):
        ctx=Context(0,0); cert=derive_means(ctx)
        chosen=Determination(Plan(1,2))
        actual=execute_declared(chosen,goal=0)
        self.assertEqual(actual['events'],Model.Catalogue(('e0','e1')).targets[0])
        self.assertNotEqual(chosen.plan,cert.plan)
        self.assertFalse(chosen.has_independent_justification)
        self.assertFalse(validate_certificate(cert,claimed_plan=chosen.plan))

    def test_same_product_and_standing_power_allow_distinct_declared_exercises(self):
        plans=[derive_means(Context(0,d)).plan for d in range(3)]
        runs=[execute_declared(Determination(p),goal=0) for p in plans]
        self.assertEqual(len(set(plans)),3)
        self.assertEqual(len({r['events'] for r in runs}),1)
        self.assertTrue(all(standing_settings(g)==(0,1,2) for g in ('A','B')))
        self.assertTrue(all(all(not providers for providers in r['entire'].values()) for r in runs))
        self.assertEqual(len({tuple((a.bearer,a.goal,a.setting) for a in r['acts']) for r in runs}),3)

    def test_fixing_declared_determination_does_not_require_other_standing_options(self):
        decree=Determination(derive_means(Context(0,0)).plan)
        first=execute_declared(decree,goal=0); second=execute_declared(decree,goal=0)
        self.assertEqual(first,second)
        alternative=Determination(derive_means(Context(0,1)).plan)
        self.assertNotEqual(decree,alternative)
        self.assertNotEqual(first['acts'],execute_declared(alternative,goal=0)['acts'])
        self.assertEqual(standing_settings('A'),(0,1,2))

    def test_successive_contexts_change_determination_not_standing_repertoire(self):
        # Finite contract illustration only: no model of an infinite past or
        # proof of why the role condition changes between occasions.
        contexts=(Context(0,0),Context(0,1),Context(1,0))
        declarations=tuple(Determination(derive_means(c).plan) for c in contexts)
        before=standing_settings('A')
        runs=[execute_declared(w,goal=c.q) for c,w in zip(contexts,declarations)]
        self.assertEqual(before,standing_settings('A'))
        self.assertEqual([r['events'] for r in runs],[Model.Catalogue(('e0','e1')).targets[c.q] for c in contexts])
        self.assertNotEqual(declarations[0],declarations[1])

if __name__=='__main__':unittest.main(verbosity=2)
