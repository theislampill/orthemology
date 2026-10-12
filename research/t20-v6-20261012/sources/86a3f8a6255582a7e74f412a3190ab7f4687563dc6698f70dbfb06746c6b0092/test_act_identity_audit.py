"""Read-only identity probes. No imported model/source is changed."""
from pathlib import Path
import importlib.util
import sys
import unittest

FRONTIER=Path(__file__).resolve().parents[3]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

reactive=load('audited_reactive', FRONTIER/'sovereignty-choice-semantics/reactive-context-extension/src/reactive_context.py')
union=load('audited_union',FRONTIER/'provision-identity/src/provision_semantics.py')

class NumericalActScopeAudit(unittest.TestCase):
    def test_reactive_role_handle_collides_across_different_exercises(self):
        original=reactive.Original('A')
        first=original.issue(0,0)
        adapted=original.issue(0,2)
        other_goal=original.issue(1,0)
        self.assertNotEqual(first,adapted)
        self.assertNotEqual(first,other_goal)
        self.assertEqual(first.token,adapted.token)
        self.assertEqual(first.token,other_goal.token)
        self.assertEqual(first.setting,other_goal.setting)
        self.assertNotEqual(first.goal,other_goal.goal)
        # A distinct bearer still has a distinct handle within an actual run.
        self.assertNotEqual(first.token,reactive.Original('B').issue(0,0).token)

    def test_reactive_suppression_reuses_record_but_equal_clone_is_indistinguishable_extensionally(self):
        c=reactive.Catalogue(('e0','e1'))
        a=reactive.Original('A').issue(0,0)
        b=reactive.Original('B').issue(0,0)
        clone=reactive.Original('A').issue(0,0)
        self.assertEqual(a,clone)
        self.assertIsNot(a,clone)
        joint=reactive.execute(c,a,b)
        solo_reused=reactive.execute(c,a,None)
        solo_cloned=reactive.execute(c,clone,None)
        self.assertIs(joint['acts'][0],a)
        self.assertIs(solo_reused['acts'][0],a)
        self.assertIsNot(solo_cloned['acts'][0],a)
        self.assertEqual(solo_reused,solo_cloned)
        self.assertEqual(joint['events'],solo_reused['events'])
        # The complete executed productive records are nevertheless different.
        self.assertNotEqual(joint['proofs'],solo_reused['proofs'])
        self.assertNotEqual(joint['supports'],solo_reused['supports'])

    def test_forecast_equality_is_representational_not_python_object_identity(self):
        c=reactive.Catalogue(('e0','e1'))
        predicted=reactive.forecast(c,0)
        a=reactive.Original('A').issue(0,0); b=reactive.Original('B').issue(0,0)
        actual=reactive.execute(c,a,b)
        self.assertEqual(predicted,actual)
        for forecast_act,actual_act in zip(predicted['acts'],actual['acts']):
            self.assertEqual(forecast_act,actual_act)
            self.assertIsNot(forecast_act,actual_act)
        # This does NOT make the forecast false: a representation need not be
        # numerically identical with the act it represents. It limits identity
        # conclusions one may draw from the equality check.

    def test_union_token_metadata_does_not_determine_production_or_act_numerical_identity(self):
        q=frozenset(('e0',)); r=frozenset(('e1',))
        a=union.IntendedAct('A','fixed-A',q)
        changed=union.IntendedAct('A','fixed-A',r)
        clone=union.IntendedAct('A','fixed-A',q)
        renamed=union.IntendedAct('A','different-occurrence-label',q)
        b=union.IntendedAct('B','fixed-B',q)
        self.assertEqual(a.token,changed.token)
        self.assertNotEqual(a,changed)
        self.assertEqual(a,clone)
        self.assertIsNot(a,clone)
        self.assertNotEqual(a,renamed)
        self.assertEqual(union.execute_intentions([a,b]),union.execute_intentions([clone,b]))
        self.assertEqual(union.execute_intentions([a,b]),union.execute_intentions([renamed,b]))
        self.assertEqual(union.execute_intentions([a])[0],union.execute_intentions([a,b])[0])
        self.assertNotEqual(union.execute_intentions([a])[1],union.execute_intentions([a,b])[1])

    def test_invocation_scoping_disambiguates_records_without_asserting_counterpart_identity(self):
        c=reactive.Catalogue(('e0','e1'))
        worlds=reactive.epistemic_model(c)['worlds']
        unscoped={act.token for w in worlds for act in w['actual']['acts']}
        scoped={(w['context'],act.token) for w in worlds for act in w['actual']['acts']}
        self.assertEqual(len(unscoped),2)
        self.assertEqual(len(scoped),6)
        for w in worlds:
            actual=w['actual']
            expected={(w['context'],act.token) for act in actual['acts']}
            for proof in actual['proofs'].values():
                self.assertEqual({(w['context'],token) for token in proof['intrinsic_inputs']},expected)
        # Six are occurrence-record handles in alternative contexts, not six
        # independently established metaphysical acts in one actual world.
        # A cross-context numerical-identity/counterpart relation is still free.

if __name__=='__main__':unittest.main(verbosity=2)
