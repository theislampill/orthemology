import unittest
from domain_contract import context,ordinary_domain,diagnostic_domain,policy_conforms,success_domain,outcome,shifted_outcome,profile_key

class DomainContractTests(unittest.TestCase):
    def test_ordinary_domain_is_policy_generated_and_has_success_without_entire_provision(self):
        for q in range(3):
            ctx=context(q); profiles=ordinary_domain(ctx)
            self.assertEqual(len(profiles),1)
            p=profiles[0]
            self.assertTrue(policy_conforms(ctx,p))
            actual=ctx['model'].execute(ctx['catalogue'],*p)
            self.assertEqual(actual,ctx['forecast'])
            self.assertEqual(actual['events'],ctx['target'])
            self.assertTrue(all(actual['intentions'].values()))
            self.assertTrue(all(not providers for providers in actual['entire'].values()))

    def test_full_compatible_domain_is_larger_than_policy_or_output_success_domain(self):
        for q in range(3):
            ctx=context(q); full=diagnostic_domain(ctx)
            self.assertEqual(len(full),16)
            success=success_domain(ctx,full,outcome)
            self.assertEqual(len(success),5)
            self.assertEqual(sum(policy_conforms(ctx,p) for p in full),1)
            self.assertEqual(sum(all(a is not None for a in p) for p in success),3)
            self.assertEqual(sum(ctx['model'].execute(ctx['catalogue'],*p)==ctx['forecast'] for p in success),1)

    def test_suppression_preserves_A_record_but_overrides_policy_and_frozen_forecast(self):
        for q in range(3):
            ctx=context(q); normal=ordinary_domain(ctx)
            self.assertEqual(len(normal),1)
            a,b=normal[0]; suppressed=(a,None)
            actual=ctx['model'].execute(ctx['catalogue'],*suppressed)
            self.assertIs(actual['acts'][0],a)
            self.assertEqual(actual['events'],ctx['target'])
            self.assertTrue(actual['intentions']['A'])
            self.assertFalse(policy_conforms(ctx,suppressed))
            self.assertNotEqual(actual,ctx['forecast'])
            self.assertTrue(all(s==frozenset(('A',)) for s in actual['supports'].values()))
            self.assertNotEqual(actual['supports'],ctx['forecast']['supports'])

    def test_policy_domain_does_not_move_to_hide_failure_when_output_function_changes(self):
        for q in range(3):
            ctx=context(q); ordinary=ordinary_domain(ctx)
            self.assertEqual(len(ordinary),1)
            keys_before=tuple(profile_key(p) for p in ordinary)
            self.assertTrue(all(outcome(ctx,p)==ctx['target'] for p in ordinary))
            self.assertTrue(all(shifted_outcome(ctx,p)!=ctx['target'] for p in ordinary))
            self.assertEqual(keys_before,tuple(profile_key(p) for p in ordinary_domain(ctx)))

    def test_success_filtered_domain_moves_with_law_and_does_not_warrant_admissibility(self):
        for q in range(3):
            ctx=context(q); full=diagnostic_domain(ctx)
            self.assertEqual(len(full),16)
            before=success_domain(ctx,full,outcome)
            after=success_domain(ctx,full,shifted_outcome)
            self.assertEqual(len(before),5); self.assertEqual(len(after),5)
            self.assertNotEqual({profile_key(p) for p in before},{profile_key(p) for p in after})
            self.assertTrue(all(outcome(ctx,p)==ctx['target'] for p in before))
            self.assertTrue(all(shifted_outcome(ctx,p)==ctx['target'] for p in after))
            self.assertTrue(any(not policy_conforms(ctx,p) for p in before))
            self.assertFalse(any(policy_conforms(ctx,p) for p in after))

if __name__=='__main__':unittest.main(verbosity=2)
