from dataclasses import replace
import unittest
from production_contract import *

class ProductionContractTests(unittest.TestCase):
    def test_sound_redundant_certificate_changes_no_actual_production(self):
        rules=(inherited.rule('A-actual','A'),)
        l=execute_program(rules,'AB');e=l.effects[0];law=program_law(rules,e)
        ca=Certificate('A-suffices',e,frozenset('A'))
        cab=Certificate('A-and-B-also-suffice',e,frozenset('AB'))
        self.assertTrue(certificate_valid(ca,law))
        self.assertTrue(certificate_valid(cab,law))
        x=extend_certificates(l,ca);y=extend_certificates(x,cab)
        self.assertEqual(x.effects,y.effects);self.assertEqual(x.births,y.births)
        self.assertEqual(x.operative_routes,y.operative_routes)
        self.assertEqual(x.exhaustive_positive_sources(e),frozenset('A'))
        self.assertEqual(y.exhaustive_positive_sources(e),frozenset('A'))
        self.assertNotEqual(x.cited_sources(e),y.cited_sources(e))
    def test_old_rule_addition_is_new_declared_production_not_proof_weakening(self):
        base=(inherited.rule('A-actual','A'),)
        extra=base+(inherited.rule('new-AB-production','AB'),)
        for profile in inherited.PROFILES:
            self.assertEqual(inherited.run(base,profile).history(),inherited.run(extra,profile).history())
        x=execute_program(base,'AB');y=execute_program(extra,'AB');e=x.effects[0]
        self.assertEqual(x.effects,y.effects)
        self.assertNotEqual(x.operative_routes,y.operative_routes)
        self.assertEqual(x.roots(e),frozenset('A'));self.assertEqual(y.roots(e),frozenset('AB'))
    def test_joint_overdetermined_priority_same_birth_distinct_actual_routes(self):
        ledgers={p:execute_program(inherited.direct_rules(p),'AB') for p in ('coalescence','redundant','priority_A')}
        for l in ledgers.values():self.assertTrue(l.unique_birth_per_effect())
        j,o,p=[ledgers[k] for k in ('coalescence','redundant','priority_A')];e=j.effects[0]
        self.assertEqual(j.effects,o.effects);self.assertEqual(o.effects,p.effects)
        self.assertEqual(j.births,o.births);self.assertEqual(o.births,p.births)
        self.assertEqual(j.source_only_actual_routes(e),frozenset())
        self.assertEqual(o.source_only_actual_routes(e),frozenset('AB'))
        self.assertEqual(p.source_only_actual_routes(e),frozenset('A'))
        self.assertEqual(j.exhaustive_positive_sources(e),frozenset())
        self.assertEqual(o.exhaustive_positive_sources(e),frozenset())
        self.assertEqual(p.exhaustive_positive_sources(e),frozenset('A'))
    def test_multiple_minimal_certificates_do_not_force_exclusive_attribution(self):
        self.assertEqual(set(minimal_true_certificates(abstract_law(EffectID('actual-episode','e'),lambda a,b:a or b))),{frozenset({('A',True)}),frozenset({('B',True)})})
        self.assertEqual(set(minimal_true_certificates(abstract_law(EffectID('actual-episode','e'),lambda a,b:a and b))),{frozenset({('A',True),('B',True)})})
        # Minimality removes redundant premises, not rival sufficient explanations.
    def test_output_sufficiency_does_not_make_a_route_actual(self):
        rules=inherited.direct_rules('priority_A');l=execute_program(rules,'AB');e=l.effects[0]
        cb=Certificate('B-output-sufficiency',e,frozenset('B'))
        self.assertTrue(certificate_valid(cb,program_law(rules,e)))
        self.assertNotIn('B',l.source_only_actual_routes(e))
    def test_absence_guard_not_positive_producer_or_unconditioned_power(self):
        rule=inherited.rule('A-needs-B-absent','A','B')
        l=execute_program((rule,),'A');e=l.effects[0]
        self.assertEqual(l.exhaustive_positive_sources(e),frozenset('A'))
        self.assertEqual(l.guarded_absences(e),frozenset('B'))
        self.assertFalse(inherited.run((rule,),'AB').events)
        self.assertNotIn('B',l.roots(e))
    def test_current_joined_candidate_survives_certificate_enrichment(self):
        for item in reactive_ledgers():
            l=item['ledger'];a=item['actual']
            self.assertTrue(all(a['intentions'].values()));self.assertTrue(all(a['own_activity_ends'].values()))
            self.assertTrue(all(f==a for f in item['forecasts'].values()))
            self.assertTrue(l.unique_birth_per_effect())
            for e in l.effects:
                self.assertEqual(l.roots(e),frozenset('AB'))
                self.assertFalse(l.exhaustive_positive_sources(e))
                enriched=extend_certificates(l,Certificate('record-of-observed-event',e,frozenset('AB')))
                self.assertEqual(l.operative_routes,enriched.operative_routes)
                self.assertEqual(l.roots(e),enriched.roots(e))
    def test_effect_and_birth_ids_have_no_source_component(self):
        l=execute_program(inherited.direct_rules('coalescence'),'AB');e=l.effects[0]
        self.assertEqual(e,EffectID('actual-episode','e'))
        self.assertEqual(l.births,(BirthID(e),))
        self.assertNotIn('A',repr(e));self.assertNotIn('B',repr(e))

    def test_certificates_are_effect_bound_nonvacuous_and_actually_applicable(self):
        rules=(inherited.rule('A-actual','A'),);l=execute_program(rules,'AB');e=l.effects[0];law=program_law(rules,e)
        ca=Certificate('valid',e,frozenset('A'))
        self.assertTrue(certificate_applicable(ca,law,'AB',l))
        self.assertFalse(certificate_valid(replace(ca,conclusion=EffectID('actual-episode','missing')),law))
        self.assertFalse(certificate_valid(replace(ca,negative_facts=frozenset('A')),law))
        self.assertFalse(certificate_valid(replace(ca,positive_facts=frozenset('C')),law))
        self.assertFalse(certificate_applicable(ca,law,'B',execute_program(rules,'B')))
        other=(inherited.rule('joint-only','AB'),)
        # Same event now true, but A alone is not sufficient under the actual other law.
        self.assertFalse(certificate_applicable(ca,law,'AB',execute_program(other,'AB')))
    def test_same_table_same_minimal_certificates_still_different_ground(self):
        modes=('coalescence','redundant','priority_A')
        ls=[execute_program(inherited.direct_rules(p),'AB') for p in modes]
        laws=[program_law(inherited.direct_rules(p),ls[i].effects[0]) for i,p in enumerate(modes)]
        self.assertEqual(laws[0].table,laws[1].table);self.assertEqual(laws[1].table,laws[2].table)
        self.assertEqual(minimal_true_certificates(laws[0]),minimal_true_certificates(laws[1]))
        self.assertEqual(minimal_true_certificates(laws[1]),minimal_true_certificates(laws[2]))
        self.assertNotEqual(ls[0].operative_routes,ls[1].operative_routes)
        self.assertNotEqual(ls[1].roots(ls[1].effects[0]),ls[2].roots(ls[2].effects[0]))
    def test_certificate_erasure_commutes_but_route_cut_discriminates(self):
        base=(inherited.rule('A-actual','A'),);extra=base+(inherited.rule('AB-new-actual','AB'),)
        l=execute_program(base,'AB');e=l.effects[0]
        c=Certificate('weakened',e,frozenset('AB'))
        enriched=extend_certificates(l,c)
        self.assertEqual(erase_certificates(enriched),erase_certificates(l))
        cut_base=execute_program(base,'AB',disabled=('A-actual',))
        cut_extra=execute_program(extra,'AB',disabled=('A-actual',))
        self.assertFalse(cut_base.effects);self.assertTrue(cut_extra.effects)
        self.assertFalse(certificate_valid(c,program_law(base,e,disabled=('A-actual',))))
        self.assertTrue(certificate_valid(c,program_law(extra,e,disabled=('A-actual',))))
    def test_event_state_preserved_separately_from_identity(self):
        x=execute_program((inherited.rule('same-route','A'),),'A')
        changed=inherited.rule('same-route','A',output=inherited.Event('e','different-state'))
        y=execute_program((changed,),'A')
        self.assertEqual(x.effects,y.effects);self.assertEqual(x.births,y.births)
        self.assertNotEqual(x.effect_states,y.effect_states)
        self.assertNotEqual(erase_certificates(x),erase_certificates(y))
    def test_indirect_flattened_derivation_is_not_claimed_actual_route_lineage(self):
        rules=inherited.created_rules('persistent_created_mechanism')
        with self.assertRaises(NotImplementedError):execute_program(rules,'AB')
    def test_actual_route_tensor_contraction_loses_comembership(self):
        j=execute_program(inherited.direct_rules('coalescence'),'AB')
        r=execute_program(inherited.direct_rules('redundant'),'AB')
        tj,tr=operative_tensor(j,2),operative_tensor(r,2)
        self.assertNotEqual(tj,tr)
        self.assertEqual(contract_route_axis(tj),contract_route_axis(tr))
        self.assertEqual((same_route_comembership(tj),same_route_comembership(tr)),(1,0))
        self.assertEqual(j.effects,r.effects);self.assertEqual(j.effect_states,r.effect_states);self.assertEqual(j.births,r.births)
        # Route coordinate permutation leaves the query invariant.
        self.assertEqual(same_route_comembership(tuple(reversed(tr))),same_route_comembership(tr))

    def test_minimal_certificates_retain_nondefault_state(self):
        e=EffectID('actual-episode','e')
        law=abstract_law(e,lambda a,b:a,'other-state')
        self.assertEqual(minimal_true_certificates(law),(frozenset({('A',True)}),))

    def test_indirect_occurrence_refinements_flatten_to_identical_retained_run(self):
        rules,one,two=indirect_occurrence_witness()
        x=project_occurrence_history(rules,'A',one)
        y=project_occurrence_history(rules,'A',two)
        old=inherited.run(rules,'A')
        self.assertEqual(x,old);self.assertEqual(y,old)
        self.assertEqual((len(one),len(two)),(3,4))
        self.assertEqual(sum(o.rule_id=='m-e' for o in one),1)
        self.assertEqual(sum(o.rule_id=='m-e' for o in two),2)
        self.assertEqual(len(old.firing_occurrence_history()),3)
        self.assertEqual(x.history(),y.history())
        self.assertEqual(x.issued,y.issued)
        # Different operative-occurrence counts do not force two event births.
        self.assertEqual(tuple(sorted(x.events)),('e','m'))

    def test_indirect_fixed_lineage_cut_does_not_descend_to_flattened_run(self):
        rules,one,two=indirect_occurrence_witness()
        cutone=prune_occurrence_history(one,('m-left',))
        cuttwo=prune_occurrence_history(two,('m-left',))
        x=project_occurrence_history(rules,'A',cutone)
        y=project_occurrence_history(rules,'A',cuttwo)
        self.assertNotIn('e',x.events);self.assertIn('e',y.events)
        # Rule-disable + closure rescheduling is a distinct continuation.
        rerun=inherited.run(rules,'A',disabled=('A-m-left',))
        self.assertIn('e',rerun.events)

    def test_occurrence_refinement_rejects_duplicate_ids_future_inputs_and_false_roots(self):
        rules,one,two=indirect_occurrence_witness()
        with self.assertRaises(ValueError):project_occurrence_history(rules,'A',one+(one[0],))
        with self.assertRaises(ValueError):project_occurrence_history(rules,'A',(one[2],one[0],one[1]))
        with self.assertRaises(ValueError):project_occurrence_history(rules,'B',one)
        # Equal contents under distinct actual occurrence IDs are permitted.
        fresh=Occurrence('e-left-second','m-e',('m-left',))
        self.assertEqual(project_occurrence_history(rules,'A',one+(fresh,)),project_occurrence_history(rules,'A',one))

if __name__=='__main__':unittest.main(verbosity=2)
