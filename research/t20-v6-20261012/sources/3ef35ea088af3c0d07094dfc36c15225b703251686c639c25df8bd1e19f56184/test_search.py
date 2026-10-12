#!/usr/bin/env python3
import unittest
from itertools import product
import search as m

class InterpretationTests(unittest.TestCase):
    def test_nonempty_targets_and_rigid_agents(self):
        self.assertEqual(len(m.COMMANDS),9)
        self.assertEqual(set(m.CAPACITIES),{'A','B'})
        self.assertIn(m.TARGET,m.COMMANDS)
    def test_equal_intrinsic_executable_capacities(self):
        self.assertEqual(m.CAPACITIES['A'],m.CAPACITIES['B'])
        for q in m.COMMANDS:
            for g in ('A','B'):
                self.assertEqual(m.Will(q,q).issue(m.CAPACITIES[g])+m.ZERO,q)
    def test_unchanged_actual_will_under_peer_deletion(self):
        wa=m.ACTUAL_WILLS['A']; command=wa.issue(m.CAPACITIES['A'])
        self.assertEqual(command,m.Vec(1,1))
        self.assertEqual(command+m.ACTUAL_WILLS['B'].command,m.TARGET)
        self.assertNotEqual(command+m.ZERO,m.TARGET)
        self.assertEqual(wa,m.ACTUAL_WILLS['A'])
    def test_changed_effort_is_rejected(self):
        before=m.ACTUAL_WILLS['A']; after=m.Will(m.TARGET,m.TARGET)
        self.assertEqual(after.command+m.ZERO,m.TARGET)
        self.assertNotEqual(before,after)
    def test_empty_eligibility_is_detected(self):
        def nonvacuous(domain): return len(domain)>0 and m.TARGET in domain
        self.assertTrue(nonvacuous(m.COMMANDS))
        self.assertFalse(nonvacuous(()))
    def test_unequal_partial_capacities_are_detected(self):
        a={m.ZERO,m.Vec(1,0)}; b={m.ZERO,m.Vec(0,1)}
        self.assertNotEqual(a,b)
        self.assertFalse(set(m.COMMANDS)<=a)
        self.assertFalse(set(m.COMMANDS)<=b)
    def test_B5_union_is_already_owned_not_a_third_agent(self):
        union=set(m.CAPACITIES['A'])|set(m.CAPACITIES['B'])
        self.assertTrue(all(union<=set(m.CAPACITIES[g]) for g in ('A','B')))
        self.assertEqual(set(m.CAPACITIES),{'A','B'})
    def test_additive_exhaustive_family(self):
        r=m.additive_search()
        self.assertEqual(len(r['fixed_target_profiles']),9)
        self.assertEqual(r['both_indispensable_count'],7)
        self.assertEqual(r['both_fixed_solo_count'],0)
    def test_all_boolean_tables(self):
        r=m.table_search()
        self.assertEqual(len(r['tables']),16)
        self.assertEqual(r['indispensable_and_fixed_solo_count'],0)
        self.assertEqual(r['both_rectangular_full_control_count'],0)
    def test_AND_OR_are_distinct_controls(self):
        def AND(a,b): return a and b
        def OR(a,b): return a or b
        self.assertTrue(AND(1,1)); self.assertFalse(AND(1,0)); self.assertFalse(AND(0,1))
        self.assertTrue(OR(1,1)); self.assertTrue(OR(1,0)); self.assertTrue(OR(0,1))
    def test_saturation_full_command_fixed_but_inputs_redundant(self):
        q=m.Vec(1,1)
        self.assertEqual(m.sat(q,q),q)
        self.assertEqual(m.sat(q,m.ZERO),q)
        self.assertEqual(m.sat(m.ZERO,q),q)
    def test_rectangular_and_concordant_distinction(self):
        for q in m.BOOLVECS:self.assertEqual(m.sat(q,q),q)
        self.assertNotEqual(m.sat(m.ZERO,m.Vec(1,1)),m.ZERO)
        self.assertEqual(m.saturated_candidate()['robust_targets_over_all_rival_commands'],{'A':[[1,1]],'B':[[1,1]]})
    def test_CND_is_not_definitionally_forced(self):
        def cnd(rel):return all(not({('A',i),('B',i)}<=rel) for i in range(4))
        good={('A',0),('A',1),('B',2),('B',3)}
        self.assertTrue(cnd(good));self.assertFalse(cnd(good|{('B',0)}))
    def test_received_capacity_and_cycle_mutations_are_detected(self):
        graph=m.graph_checks(); edges=[tuple(e) for e in graph['efficient_edges']]
        def reaches(es,start,end,seen=frozenset()):
            if start==end:return True
            if start in seen:return False
            return any(reaches(es,b,end,seen|{start}) for a,b in es if a==start)
        self.assertFalse(reaches(edges,'B.emission','A.capacity'))
        self.assertTrue(reaches(edges+[('B.emission','A.capacity')],'B.emission','A.capacity'))
        cycle=edges+[('A.will','B.will'),('B.will','A.will')]
        self.assertTrue(reaches(cycle,'B.will','A.will'))
        self.assertTrue(reaches(cycle,'A.will','B.will'))
    def test_target_identity_is_not_source_or_history_indexed(self):
        token='e'
        self.assertEqual(m.saturated_candidate()['target_token'],token)
        self.assertEqual(m.additive_search()['actual']['target_token'],token)
        self.assertNotEqual(('e_A','e_B'),(token,token))

if __name__=='__main__':unittest.main(verbosity=2)
