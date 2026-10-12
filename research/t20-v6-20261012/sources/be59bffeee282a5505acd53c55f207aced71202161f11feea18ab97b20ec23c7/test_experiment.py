import unittest
from itertools import product
from experiment import run, optimal_profiles, knowledge, undominated, fixedpoints

class SemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()
    def test_unique_end_multiple_allocations(self):
        self.assertEqual(self.r['epistemic']['worlds'],[(0,2),(1,1),(2,0)])
    def test_knowledge_has_information_not_arbitrary_label(self):
        e=self.r['epistemic']
        self.assertTrue(e['prechoice_A_knows_target'])
        self.assertFalse(e['prechoice_A_knows_B_command_1'])
        self.assertTrue(e['postchoice_A_knows_B_command_1'])
        self.assertTrue(e['all_subset_propositions_factive'])
    def test_actual_omniscience_retains_metaphysical_multiplicity(self):
        rows=self.r['epistemic']['omniscient_identity_frame_at_each_world']
        self.assertEqual(len(rows),3)
        self.assertTrue(all(r['knows_own_command'] and r['knows_peer_command'] and r['knows_all_true_subset_propositions'] for r in rows))
    def test_equal_power_does_not_force_equal_intrinsic_roles(self):
        a=self.r['asymmetric_intrinsic_roles']
        self.assertTrue(a['equal_target_capacity'])
        self.assertEqual(a['role_selected_commands'],{'A':'1','B':'2'})
        self.assertEqual(a['whole_outcome'],'3')
        self.assertNotEqual(a['role_selected_commands'],a['same_bearer_after_role_swap'])
    def test_factivity_does_not_select_equilibrium(self):
        self.assertEqual(len(self.r['factive_forecast_choice_solutions']),3)
    def test_forecast_rule_sensitivity(self):
        self.assertEqual(fixedpoints((0,1),lambda b:b,lambda a:a),[(0,0),(1,1)])
        self.assertEqual(fixedpoints((0,1),lambda b:1-b,lambda a:a),[])
        self.assertEqual(fixedpoints((0,1),lambda b:1,lambda a:1),[(1,1)])
    def test_unique_cycle_is_not_well_founded_production(self):
        self.assertEqual(self.r['unique_mutual_ternary_fixedpoint'],[(2,2)])
    def test_anonymity_requires_structural_fixedpoint(self):
        for row in self.r['anonymous_rules']:
            self.assertEqual(len(row['anonymous_fixed_profiles']),int(row['target']%2==0))
            self.assertTrue(row['rational_target_attained'])
    def test_outcome_only_wisdom_is_fiber_invariant(self):
        # Independent universal finite census of all output maps and all rankings
        # on two output values: every same-output pair has the same status.
        for vals in product(range(2),repeat=4):
            F=dict(zip(product(range(2),repeat=2),vals))
            for score in product(range(3),repeat=2):
                top=max(score[y] for y in vals)
                for p,q in product(F,repeat=2):
                    if F[p]==F[q]:self.assertEqual(score[F[p]]==top,score[F[q]]==top)
    def test_weak_dominance_differs_from_strict(self):
        d=self.r['dominance']
        self.assertEqual(d['or_weakly_undominated_full_operational_domain'],[1])
        self.assertEqual(d['or_strictly_undominated_full_operational_domain'],[0,1])
    def test_dominance_changes_with_knowledge_restricted_rivals(self):
        self.assertEqual(self.r['dominance']['or_weakly_undominated_if_peer_known_active'],[0,1])
    def test_additive_symmetric_rule_not_dominance_theorem(self):
        self.assertEqual(self.r['dominance']['additive_weakly_undominated_full_domain'],[0,1,2])
    def test_suppression_retains_exact_command(self):
        a,b=self.r['fixed_command_controls']
        self.assertFalse(a['fixed_A_suffices']);self.assertTrue(b['fixed_A_suffices'])
        self.assertTrue(a['A_has_full_target_constructor'])
    def test_temporal_same_rule_does_not_align_phases(self):
        h=self.r['autonomous_histories']
        self.assertTrue(h['constant_one']['all_biinfinite_histories_concordant'])
        self.assertFalse(h['identity']['all_biinfinite_histories_concordant'])
        self.assertFalse(h['negation']['all_biinfinite_histories_concordant'])
    def test_same_observation_different_productive_dependencies(self):
        d=self.r['dependency_models']
        self.assertEqual(d['independent_intrinsic']['actual'],d['B_receives_A_activation']['actual'])
        self.assertNotEqual(d['independent_intrinsic']['do_A_0_result'],d['B_receives_A_activation']['do_A_0_result'])
    def test_concentration_uses_each_existing_bearer(self):
        self.assertTrue(all(r['same_A_executes_sum'] and r['same_B_executes_sum'] for r in self.r['same_bearer_concentration']))

if __name__=='__main__':unittest.main(verbosity=2)
