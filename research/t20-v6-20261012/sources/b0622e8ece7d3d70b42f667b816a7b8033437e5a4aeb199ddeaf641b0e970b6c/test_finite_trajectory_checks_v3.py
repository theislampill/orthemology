#!/usr/bin/env python3
"""Independent behavioural specifications for the additive stage-three toy suite."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import importlib
import sys
import unittest

if not __debug__:
    raise SystemExit("Optimised execution is not a verification run.")
try:
    m = importlib.import_module("finite_trajectory_checks_v3")
except ModuleNotFoundError:
    m = None

class FiniteTrajectorySpecification(unittest.TestCase):
    def need(self):
        self.assertIsNotNone(m, "The finite-model implementation has not been written.")
        return m

    def test_global_compatibility_is_not_pairwise_compatibility(self):
        x = self.need()
        allowed = (frozenset("ab"), frozenset("bc"), frozenset("ac"))
        self.assertTrue(all(allowed[i] & allowed[j] for i in range(3) for j in range(i)))
        self.assertEqual(set.intersection(*(set(a) for a in allowed)), set())
        self.assertEqual(x.cover_number(allowed), 2)
        self.assertEqual(x.partition_number(allowed), 2)

    def test_cover_and_good_partition_agree_on_all_four_world_three_candidate_relations(self):
        x = self.need()
        sets = tuple(frozenset(c for c in range(3) if mask & (1 << c)) for mask in range(1, 8))
        count = 0
        for relation in product(sets, repeat=4):
            self.assertEqual(x.cover_number(relation), x.partition_number(relation))
            count += 1
        self.assertEqual(count, 2401)

    def test_probability_rounding_preserves_zero_support_and_declared_error_bound(self):
        x = self.need()
        cases = 0
        for size in range(1, 6):
            for counts in x.compositions(7, size):
                p = tuple(F(c, 7) for c in counts)
                for denominator in range(1, 8):
                    q = x.round_distribution(p, denominator)
                    self.assertEqual(sum(q), 1)
                    self.assertTrue(all(v >= 0 for v in q))
                    self.assertTrue(all(not q[i] for i, v in enumerate(p) if not v))
                    self.assertLessEqual(sum(abs(a-b) for a, b in zip(p, q)), F(size, denominator))
                    cases += 1
        self.assertGreater(cases, 3000)

    def test_grid_regret_bound_on_a_known_mixed_nash_profile(self):
        x = self.need()
        c1, c2 = ((0, 1), (2, 0)), ((1, 0), (0, 2))
        p, q = (F(2, 3), F(1, 3)), (F(1, 3), F(2, 3))
        self.assertEqual(x.cost_regret(c1, p, q, 0), 0)
        self.assertEqual(x.cost_regret(c2, p, q, 1), 0)
        for denominator in range(1, 20):
            r, s = x.round_distribution(p, denominator), x.round_distribution(q, denominator)
            dp, dq = sum(abs(a-b) for a,b in zip(p,r)), sum(abs(a-b) for a,b in zip(q,s))
            self.assertLessEqual(x.cost_regret(c1,r,s,0), 2*dp+4*dq)
            self.assertLessEqual(x.cost_regret(c2,r,s,1), 2*dq+4*dp)

    def test_simultaneous_improvement_cycles_and_asynchronous_improvement_stops(self):
        x = self.need()
        costs = ((1, 0), (0, 1))
        self.assertEqual(x.simultaneous_trace(costs, (0, 0), 4),
                         ((0,0),(1,1),(0,0),(1,1),(0,0)))
        path = x.asynchronous_improvement(costs, (0, 0))
        self.assertEqual(path, ((0,0),(1,0)))
        self.assertTrue(x.is_pure_equilibrium(costs, path[-1]))

    def test_all_small_potential_tables_have_terminating_strict_unilateral_paths(self):
        x = self.need()
        paths = 0
        for cells in product(range(3), repeat=4):
            costs = (cells[:2], cells[2:])
            for start in product(range(2), repeat=2):
                path = x.asynchronous_improvement(costs, start)
                self.assertLessEqual(len(path)-1, 3)
                self.assertEqual(len(set(path)), len(path))
                self.assertTrue(x.is_pure_equilibrium(costs, path[-1]))
                self.assertTrue(all(costs[v[0]][v[1]] < costs[u[0]][u[1]]
                                    for u,v in zip(path,path[1:])))
                paths += 1
        self.assertEqual(paths, 324)

    def test_detection_without_progress_can_stall_before_equilibrium(self):
        x = self.need()
        costs = ((2, 2), (0, 1))
        state = (0, 0)
        for _ in range(8):
            state = x.best_response_step(costs, state, 1)
        self.assertEqual(state, (0,0))
        self.assertFalse(x.is_pure_equilibrium(costs, state))

    def test_logit_detailed_balance_and_stationary_joint_law(self):
        x = self.need()
        costs = ((0,2),(2,1))
        transition = x.logit_transition(costs, (2,2))
        pi = (F(1,2),F(1,8),F(1,8),F(1,4))
        self.assertEqual(x.apply_law(pi,transition), pi)
        self.assertTrue(all(sum(row)==1 for row in transition))
        self.assertTrue(all(pi[i]*transition[i][j]==pi[j]*transition[j][i]
                            for i in range(4) for j in range(4)))
        p,q = x.marginals(pi)
        self.assertEqual(p,(F(5,8),F(3,8)))
        self.assertEqual(q,p)
        self.assertNotEqual(x.product_law(p,q),pi)
        self.assertEqual(x.cost_regret(costs,p,q,0),F(21,64))
        self.assertEqual(x.cost_regret(costs,p,q,1),F(21,64))

    def test_heterogeneous_logit_sensitivity_breaks_reversible_potential_formula(self):
        x = self.need()
        transition = x.logit_transition(((0,2),(2,1)), (2,4))
        cycle = (0,2,3,1,0)
        forward = reverse = F(1)
        for a,b in zip(cycle,cycle[1:]):
            forward *= transition[a][b]
            reverse *= transition[b][a]
        self.assertEqual(forward/reverse,8)

    def test_mixed_equilibrium_is_a_saddle_of_expected_common_cost(self):
        x = self.need()
        c = ((1,0),(0,1))
        p = (F(1,2),F(1,2))
        self.assertEqual(x.cost_regret(c,p,p,0),0)
        self.assertEqual(x.cost_regret(c,p,p,1),0)
        t=F(1,10)
        plus=(F(1,2)+t,F(1,2)-t)
        minus=tuple(reversed(plus))
        self.assertGreater(x.expected_cost(c,plus,plus),F(1,2))
        self.assertLess(x.expected_cost(c,plus,minus),F(1,2))

    def test_sensor_polarity_loss_preserves_ambiguity(self):
        x = self.need()
        fibres = x.calibration_fibres()
        self.assertEqual(fibres[0],frozenset({(0,0),(1,1)}))
        self.assertEqual(fibres[1],frozenset({(0,1),(1,0)}))
        self.assertTrue(all(len({c for c,k in fibre})==2 for fibre in fibres.values()))
        for c,k in product((0,1), repeat=2):
            self.assertEqual((c^k)^k,c)

    def test_per_query_budget_is_not_simultaneous_vector_budget(self):
        x=self.need()
        for size in range(1,7):
            for bits in product((0,1),repeat=size):
                answers=[]
                total=0
                for query in range(size):
                    answer, probes=x.coordinate_query(bits,query)
                    self.assertEqual(probes,1)
                    self.assertEqual(answer,bits[query])
                    answers.append(answer); total+=probes
                self.assertEqual(tuple(answers),bits)
                self.assertEqual(total,size)

    def test_destructive_experiments_need_initial_answer_labels(self):
        x=self.need()
        trans={
            "a":{"p":"t1","q":"t0","r":"t0","t0":"t0","t1":"t1"},
            "b":{"p":"t0","q":"t1","r":"t0","t0":"t0","t1":"t1"},
        }
        obs={"p":"?","q":"?","r":"?","t0":"0","t1":"1"}
        initial=frozenset({("p",0),("q",0),("r",1)})
        result=x.decision_game(initial,tuple(trans),
              lambda a,s:trans[a][s], lambda s:obs[s],
              lambda c,s,label:c==label, (0,1), lambda a,s:True)
        self.assertFalse(result["initial_winning"])
        singleton_merge=frozenset({("t0",0),("t0",1)})
        merged=x.decision_game(singleton_merge,tuple(trans),
              lambda a,s:trans[a][s],lambda s:obs[s],
              lambda c,s,label:c==label,(0,1),lambda a,s:True)
        self.assertFalse(merged["initial_winning"])

    def test_current_execution_resource_is_not_initial_feasibility(self):
        x=self.need()
        def solve(budget):
            initial=frozenset({((0,False,budget),0),((1,False,budget),1)})
            return x.decision_game(
                initial,("probe",),
                lambda a,s:(s[0],True,s[2]-1),
                lambda s:(s[0] if s[1] else "?",s[2]),
                lambda c,s,label:c==label and s[2]>=1,
                (0,1), lambda a,s:s[2]>=1 and not s[1])
        self.assertFalse(solve(1)["initial_winning"])
        good=solve(2)
        self.assertTrue(good["initial_winning"])
        self.assertEqual(good["initial_rank"],1)


    def test_pure_preference_signs_do_not_determine_the_mixed_equilibrium(self):
        x=self.need()
        old=((0,1),(1,0)); new=((0,1),(2,0)); other=((1,0),(0,1))
        half=(F(1,2),F(1,2)); third=(F(1,3),F(2,3))
        def sign(v):
            return (v>0)-(v<0)
        self.assertEqual(tuple(sign(old[1][j]-old[0][j]) for j in (0,1)),
                         tuple(sign(new[1][j]-new[0][j]) for j in (0,1)))
        self.assertEqual(x.cost_regret(old,half,half,0),0)
        self.assertEqual(x.cost_regret(other,half,half,1),0)
        self.assertEqual(x.cost_regret(new,half,half,0),F(1,4))
        self.assertEqual(x.cost_regret(new,half,third,0),0)
        self.assertEqual(x.cost_regret(other,half,third,1),0)

if __name__=="__main__":
    unittest.main(verbosity=2)
