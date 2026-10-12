import unittest
from provision_semantics import *

class SemanticsTests(unittest.TestCase):
    def test_all_input_interventions_have_same_complete_created_history(self):
        for s in PROFILES:
            histories={run(direct_rules(p),s).history() for p in ('coalescence','redundant','priority_A','priority_B')}
            self.assertEqual(len(histories),1)
    def test_actual_derivations_differ(self):
        self.assertEqual(run(direct_rules('coalescence'),'AB').productive_roots(),frozenset('AB'))
        self.assertEqual(run(direct_rules('priority_A'),'AB').productive_roots(),frozenset('A'))
    def test_attribution_is_derived_and_respect_matters(self):
        joint=run(direct_rules('coalescence'),'AB')
        redundant=run(direct_rules('redundant'),'AB')
        self.assertEqual(joint.derivation_providers(),frozenset())
        self.assertEqual(redundant.derivation_providers(),frozenset('AB'))
        self.assertEqual(joint.exhaustive_providers(),frozenset())
        self.assertEqual(redundant.exhaustive_providers(),frozenset())
    def test_whole_effect_cnd_not_only_emissions(self):
        # This relation admits an actual whole owner in singleton contexts;
        # the coalescence joint context has no whole owner, explicitly.
        for p in ('coalescence','redundant','priority_A','priority_B'):
            for s in PROFILES:
                self.assertLessEqual(len(run(direct_rules(p),s).exhaustive_providers()),1)
        self.assertEqual(run(direct_rules('coalescence'),'A').exhaustive_providers(),frozenset('A'))
    def test_same_intrinsic_act_retained_but_operative_rule_changes(self):
        both=run(direct_rules('coalescence'),'AB'); solo=run(direct_rules('coalescence'),'A')
        self.assertIs(both.issued[0],solo.issued[0])
        self.assertNotEqual({p.rule for p in both.proofs['e']},{p.rule for p in solo.proofs['e']})
    def test_cut_exposes_primitive_joint_rule(self):
        self.assertEqual(run(direct_rules('coalescence'),'AB',['AB-joint']).history(),())
        self.assertEqual(run(direct_rules('redundant'),'AB',['A-direct']).history(),(('e','exists-at-t'),))
    def test_created_coupler_must_be_counted(self):
        both=run(created_rules('joint_created_mechanism'),'AB')
        solo=run(created_rules('joint_created_mechanism'),'A')
        self.assertNotEqual(both.history(),solo.history())
        self.assertEqual(both.events['e'],solo.events['e'])
        self.assertEqual(both.productive_roots('m'),frozenset('AB'))
    def test_one_root_coupler_no_cycle_but_external_resource_needed(self):
        both=run(created_rules('A_created_mechanism'),'AB')
        self.assertEqual(both.productive_roots('m'),frozenset('A'))
        self.assertEqual(both.productive_roots('e'),frozenset('AB'))
        self.assertNotIn('e',run(created_rules('A_created_mechanism'),'B').events)
    def test_nonidempotent_occurrences_detect_double_firing(self):
        rr=run(direct_rules('redundant'),'AB')
        cc=run(direct_rules('coalescence'),'AB')
        self.assertEqual(len(rr.history()),1)
        self.assertEqual(len(rr.firing_occurrence_history()),2)
        self.assertEqual(len(cc.firing_occurrence_history()),1)
    def test_effects_in_bearer_are_distinct_from_bearer_count(self):
        joint=run(direct_rules('coalescence'),'AB')
        solo=run(direct_rules('coalescence'),'A')
        self.assertEqual(len(joint.history()),1)
        self.assertEqual(len(joint.contribution_relations()),2)
        self.assertEqual(joint.history(),solo.history())
        self.assertNotEqual(joint.causally_enriched_history(),solo.causally_enriched_history())
    def test_every_finite_joint_dag_has_primitive_coalescence(self):
        for n in range(1,5):
            r=shared_grounding_dags(n)
            self.assertEqual(r['joint_terminal_programs'],r['first_joint_node_without_prior_joint_mechanism'])
            self.assertGreater(r['joint_terminal_programs'],0)
    def test_persistent_created_mechanism_relocates_first_joint_node(self):
        rules=created_rules('persistent_created_mechanism')
        both=run(rules,'AB'); solo=run(rules,'A')
        self.assertEqual(both.history(),solo.history())
        self.assertEqual(both.productive_roots('m'),frozenset('AB'))
        self.assertEqual(solo.productive_roots('m'),frozenset('A'))
    def test_all_declared_catalogue_targets_constructible(self):
        report=catalogue_report(4)
        self.assertEqual(report['all_target_sets_tested'],16)
        self.assertEqual(report['full_created_event_set_fixed_solo_failures'],[])
    def test_interpreted_intention_content_changes_output(self):
        a=IntendedAct('A','alpha',frozenset(['e0']))
        a2=IntendedAct('A','alpha2',frozenset(['e1']))
        self.assertNotEqual(execute_intentions([a])[0],execute_intentions([a2])[0])
    def test_complete_exact_intentions_need_admissibility_constraint(self):
        a=IntendedAct('A','alpha',frozenset(['e0']))
        b=IntendedAct('B','beta',frozenset(['e1']))
        self.assertEqual(execute_intentions([a,b])[3],{'A':False,'B':False})
    def test_frozen_interpreted_act_not_same_active_rule(self):
        q=frozenset(['e0','e1'])
        a=IntendedAct('A','alpha',q); b=IntendedAct('B','beta',q)
        joint=execute_intentions([a,b]); solo=execute_intentions([a])
        self.assertEqual(joint[0],solo[0])
        self.assertEqual(joint[3],{'A':True,'B':True})
        self.assertNotEqual(joint[2],solo[2])
    def test_primitive_double_entire_is_not_hiddenly_functional(self):
        rr=primitive_attribution_report()
        double=next(r for r in rr if r['primitive_entire_relation']==['A','B'])
        self.assertFalse(double['whole_effect_CND'])
        self.assertTrue(double['whole_effect_coverage'])
        self.assertFalse(double['entire_solo_meaning_excludes_coproducer'])
    def test_cnd_does_not_smuggle_in_coverage(self):
        rr=primitive_attribution_report()
        empty=next(r for r in rr if r['primitive_entire_relation']==[])
        self.assertTrue(empty['whole_effect_CND'])
        self.assertTrue(empty['entire_solo_meaning_excludes_coproducer'])
        self.assertFalse(empty['whole_effect_coverage'])
    def test_single_primitive_entire_still_excludes_coproduction(self):
        rr=primitive_attribution_report()
        for record in rr:
            if len(record['primitive_entire_relation'])==1:
                self.assertTrue(record['whole_effect_CND'])
                self.assertFalse(record['entire_solo_meaning_excludes_coproducer'])
    def test_actual_nonvacuous_cnd_somewhere_not_cooperative_e(self):
        rules=direct_rules('coalescence')+(rule('A-f','A',output=Event('f','exists-at-t')),)
        actual=run(rules,'AB')
        self.assertEqual(actual.exhaustive_providers('e'),frozenset())
        self.assertEqual(actual.exhaustive_providers('f'),frozenset('A'))
    def test_no_unassigned_spontaneous_output(self):
        for p in ('coalescence','redundant','priority_A','priority_B'):
            self.assertEqual(run(direct_rules(p),()).history(),())
    def test_engine_would_detect_spontaneous_output_if_inserted(self):
        self.assertIn('e',run([rule('bad-spontaneous',())],()).events)
    def test_conservation_extension_restores_distinction(self):
        # Finite physical accounting fixture, not universal metaphysical law.
        def physical(a,b):
            display=min(1,a+b)
            waste=a+b-display
            return (display,waste)
        self.assertEqual(physical(1,1)[0],physical(1,0)[0])
        self.assertNotEqual(physical(1,1),physical(1,0))
        for a,b in product(range(4),repeat=2): self.assertEqual(sum(physical(a,b)),a+b)
    def test_interaction_correction_has_real_negative_weight(self):
        # Bilinear inclusion/exclusion exactly realises the Boolean merge.
        for a,b in product((0,1),repeat=2):
            self.assertEqual(a+b-a*b,int(bool(a or b)))
        self.assertEqual(1+1-1,1)
    def test_all_commutative_monoids_enumerated(self):
        for n in (2,3,4):
            records=monoid_report(n)['records']
            self.assertTrue(records)
            for rec in records:
                if rec['cancellative']: self.assertFalse(rec['absorptions'])
                # Finite monoid fact is tested here, not claimed universal.
                if not rec['absorptions']: self.assertTrue(rec['cancellative'])
    def test_creation_history_not_definitionally_provenance_injective(self):
        self.assertEqual(run(direct_rules('coalescence'),'AB').history(),
                         run(direct_rules('priority_A'),'AB').history())
        self.assertNotEqual(run(direct_rules('coalescence'),'AB').proofs,
                            run(direct_rules('priority_A'),'AB').proofs)
    def test_intrinsic_token_difference_does_not_force_event_difference(self):
        self.assertNotEqual(ACTS['A'],ACTS['B'])
        a=run(direct_rules('coalescence'),'A'); b=run(direct_rules('coalescence'),'B')
        self.assertEqual(a.history(),b.history())
        # Equality here is in the mathematical semantics; no source theorem of
        # cross-world numerical identity is inferred from this equality.

if __name__=='__main__': unittest.main(verbosity=2)
