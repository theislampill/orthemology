from copy import deepcopy
from dataclasses import asdict, replace
from itertools import product
from unittest.mock import patch
from tests.support import BoundaryCase, validate_model, graph_model, subsets
from tests.fixtures import singleton, bernoulli, separator, recovery, stale
import certificates as reference_certificates
import synthesis as reference_synthesis


class SolverTests(BoundaryCase):
    def api(self):
        api=self.module('efficient')
        for name in ('known_operator','uncertain_operator','descend','solve'):
            self.assertTrue(callable(getattr(api,name,None)),f'missing planned boundary: efficient.{name}')
        return api

    def negative(self): return self.module('negative')

    def test_even_positive_and_odd_exact_negative(self):
        api=self.api(); even=api.solve(singleton()); odd=api.solve(singleton(1))
        self.assertIsInstance(even,reference_certificates.Positive)
        self.assertEqual(odd,reference_certificates.Negative(((0,),(),()),((0,),(),())))
        self.assertEqual(self.negative().check_negative(singleton(1),odd),odd)

    def test_static_switch_separator_full_trace(self):
        api=self.api(); m=validate_model(separator()); body=api.solve(m)
        self.assertEqual(body.k_trace,((0,1),(0,),(0,)))
        self.assertEqual(body.w_trace,((0,1),(),()))
        self.assertEqual(body,reference_synthesis.solve(m))

    def test_memory_numerical_revelation_and_stale_fixtures(self):
        api=self.api()
        for raw in (bernoulli(),recovery(),stale()):
            body=api.solve(raw)
            self.assertIsInstance(body,reference_certificates.Positive)
            self.assertEqual(reference_certificates.check_positive(raw,body),body)
        body=api.solve(bernoulli(True))
        self.assertIsInstance(body,reference_certificates.Negative)
        self.assertEqual(reference_certificates.check_negative(bernoulli(True),body),body)

    def test_routes_keep_shortest_lexicographic_edge_semantics(self):
        result=self.api().solve(stale())
        for routes in result.uncertain_routes:
            self.assertEqual(routes[0].steps,((0,1),))
            self.assertIsNotNone(routes[0].component)
        result=self.api().solve(recovery())
        self.assertEqual(result.uncertain_routes[1][0].reveal,(0,1))

    def test_exact_negative_schema_and_malformed_traces(self):
        api=self.api(); checker=self.negative().check_negative
        m=validate_model(separator()); good=api.solve(m)
        self.assertEqual(checker(m,asdict(good)),good)
        bad_traces=(((),),((),()),((0,1),()),((0,1),(0,),(),()),
            ((0,1),(0,),(0,)),((0,1),(0,),(),(),()),((0,1),(0,1),(),()),
            ((1,0),(),()),((0,0,1),(),()),((0,1),[],()),((False,1),(),()))
        for trace in bad_traces:
            with self.subTest(trace=trace): self.assertIsNone(checker(m,replace(good,w_trace=trace)))
        for body in (None,{},dict(k_trace=good.k_trace,w_trace=good.w_trace,success=True),
                     dict(k_trace=list(good.k_trace),w_trace=good.w_trace)):
            self.assertIsNone(checker(m,body))
        positive_trace=reference_certificates.Negative(((0,),(0,)),((0,),(0,)))
        self.assertIsNone(checker(singleton(),positive_trace))

    def test_negative_rejects_wrong_known_prefix_even_with_same_terminal(self):
        api=self.api(); checker=self.negative().check_negative; m=validate_model(separator())
        good=api.solve(m)
        for trace in (((0,1),(0,1),(0,),(0,)),((0,), (0,)),((0,1),(),())):
            self.assertIsNone(checker(m,replace(good,k_trace=trace)))

    def test_region_domains_remain_strict(self):
        api=self.api(); m=validate_model(bernoulli())
        for region in ({-1},{2},{False}):
            with self.assertRaises(ValueError):api.known_operator(m,region)
            with self.assertRaises(ValueError):api.uncertain_operator(m,region,{0,1})
            with self.assertRaises(ValueError):api.uncertain_operator(m,{0,1},region)

    def test_invalid_models_are_errors_not_negative_answers(self):
        api=self.api(); checker=self.negative().check_negative
        for raw in (None,{},dict(singleton(),initial=False),dict(singleton(),rows=[[[["2/2"]]],[[[1]]]])):
            with self.assertRaises(ValueError):api.solve(raw)
            with self.assertRaises(ValueError):checker(raw,{})

    def test_resource_failure_and_failed_self_validation_propagate(self):
        api=self.api()
        with patch.object(api,'maximal_components',side_effect=MemoryError('execution failed')):
            with self.assertRaises(MemoryError):api.solve(singleton())
            with self.assertRaises(MemoryError):self.negative().check_negative(singleton(),dict(k_trace=((0,),(0,)),w_trace=((0,),(0,))))
        with patch.object(api,'check_positive',return_value=None):
            with self.assertRaises(RuntimeError):api.solve(singleton())
        with patch.object(self.negative(),'check_negative',return_value=None):
            with self.assertRaises(RuntimeError):api.solve(singleton(1))

    def test_descent_invariant_is_checked(self):
        api=self.api(); m=validate_model(singleton())
        calls=iter((frozenset(),frozenset({0})))
        with self.assertRaises(RuntimeError):api.descend(m,lambda _:next(calls))

    def test_no_production_exhaustive_or_reference_negative_calls(self):
        api=self.api(); checker=self.negative().check_negative
        forbidden=AssertionError('exponential reference boundary called')
        with patch('finite.all_components',side_effect=forbidden), \
             patch('synthesis.all_components',side_effect=forbidden), \
             patch('synthesis.solve',side_effect=forbidden), \
             patch('synthesis.known_operator',side_effect=forbidden), \
             patch('synthesis.uncertain_operator',side_effect=forbidden), \
             patch('certificates.check_negative',side_effect=forbidden):
            for raw in (singleton(),singleton(1),separator(),bernoulli(),bernoulli(True),recovery(),stale()):
                body=api.solve(raw)
                if isinstance(body,reference_certificates.Negative):self.assertEqual(checker(raw,body),body)

    def test_every_small_two_state_operator_region_and_signed_body(self):
        api=self.api(); options=([1,0],[0,1],['1/2','1/2']); regions=subsets((0,1)); cases=0
        for rows in product(options,repeat=4):
            for labels in product(range(2),repeat=4):
                m=graph_model([[rows[0]],[rows[1]]],rows1=[[rows[2]],[rows[3]]],
                    priorities=[[[labels[0]],[labels[1]]],[[labels[2]],[labels[3]]]])
                for K in regions:
                    self.assertEqual(api.known_operator(m,K),reference_synthesis.known_operator(m,K))
                    for W in regions:
                        self.assertEqual(api.uncertain_operator(m,K,W),reference_synthesis.uncertain_operator(m,K,W))
                kt=api.descend(m,lambda K:api.known_operator(m,K))
                rt=reference_synthesis.descend(m,lambda K:reference_synthesis.known_operator(m,K))
                self.assertEqual(kt,rt)
                K=frozenset(kt[-1])
                self.assertEqual(api.descend(m,lambda W:api.uncertain_operator(m,K,W)),
                    reference_synthesis.descend(m,lambda W:reference_synthesis.uncertain_operator(m,K,W)))
                result=api.solve(m); expected=reference_synthesis.solve(m)
                self.assertEqual(type(result),type(expected))
                checker=reference_certificates.check_positive if isinstance(result,reference_certificates.Positive) else reference_certificates.check_negative
                self.assertEqual(checker(m,result),result)
                cases+=1
        self.assertEqual(cases,1296)

    def test_frozen_controller_accepts_new_body_and_replays_branches(self):
        api=self.api(); import controller
        m=validate_model(bernoulli()); body=api.solve(m)
        frontier=[((m.initial,),controller.initial_memory(m,body))]
        for _ in range(5):
            following=[]
            for history,memory in frontier:
                a,prepared=controller.choose(m,body,memory,history[-1])
                self.assertEqual(controller.action_for_history(m,body,history),a)
                for receipt in range(m.n_states):
                    following.append((history+(a,receipt),controller.observe(m,body,prepared,history[-1],a,receipt)))
            frontier=following
        self.assertEqual(len(frontier),32)

    def test_controller_timing_and_known1_persistence_unchanged(self):
        self.api(); import controller
        m=validate_model(recovery()); body=self.api().solve(m)
        memory=controller.initial_memory(m,body)
        a,prepared=controller.choose(m,body,memory,0)
        memory=controller.observe(m,body,prepared,0,a,1)
        self.assertEqual((memory.known1,memory.phase,memory.retained),(True,0,None))
        self.assertEqual(memory.uses[0][0],1)
        a,prepared=controller.choose(m,body,memory,1)
        memory=controller.observe(m,body,prepared,1,a,1)
        self.assertTrue(memory.known1)

    def test_raw_history_validation_with_efficient_body(self):
        self.api(); import controller
        m=validate_model(stale()); body=self.api().solve(m)
        for history in ((),(False,),(0,1,1),(0,0),(3,),None):
            with self.assertRaises(ValueError):controller.action_for_history(m,body,history)
