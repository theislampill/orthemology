from dataclasses import asdict
from unittest.mock import patch
from tests.support import BoundaryCase
from tests.fixtures import singleton, separator, bernoulli, recovery, stale, bernoulli_body

class SynthesisTests(BoundaryCase):
    def setUp(self):
        self.model=self.module('model');self.cert=self.module('certificates');self.api=self.module('synthesis');self.finite=self.module('finite')
    def m(self,raw): return self.model.validate_model(raw)
    def test_even_positive_and_odd_negative(self):
        even=self.m(singleton()); odd=self.m(singleton(1))
        self.assertIsInstance(self.api.solve(even),self.cert.Positive)
        result=self.api.solve(odd);self.assertIsInstance(result,self.cert.Negative)
        self.assertEqual(result.k_trace,((0,),(),()));self.assertEqual(result.w_trace,((0,),(),()))
    def test_minimal_static_switch_separator(self):
        m=self.m(separator());result=self.api.solve(m)
        self.assertIsInstance(result,self.cert.Negative)
        self.assertEqual(result.k_trace,((0,1),(0,),(0,)))
        self.assertEqual(result.w_trace,((0,1),(),()))
        self.assertEqual(self.api.known_operator(m,{0,1}),frozenset({0}))
        self.assertEqual(self.api.uncertain_operator(m,{0},{0,1}),frozenset())
    def test_numerical_control_and_positive_returns_check(self):
        for raw in (bernoulli(),recovery(),stale()):
            m=self.m(raw);result=self.api.solve(m)
            with self.subTest(raw=raw):
                self.assertIsInstance(result,self.cert.Positive);self.assertEqual(self.cert.check_positive(m,result),result)
        m=self.m(bernoulli(True));result=self.api.solve(m)
        self.assertIsInstance(result,self.cert.Negative);self.assertEqual(self.cert.check_negative(m,result),result)
    def test_safe_sets_all_components_and_region_domains(self):
        m=self.m(bernoulli())
        self.assertEqual(self.finite.safe_known(m,{0}),())
        self.assertEqual(self.finite.safe_uncertain(m,set(),{0,1}),((0,0),(0,1),(1,0),(1,1)))
        self.assertEqual(self.finite.all_components(m,0,((0,0),(0,1),(1,0),(1,1)),True),(((0,0),(1,0)),))
        for region in ({-1},{2},{False}):
            with self.subTest(region=region):
                with self.assertRaises(ValueError):self.api.known_operator(m,region)
    def test_bfs_shortest_lex_route(self):
        m=self.m(stale()); result=self.api.solve(m)
        for routes in result.uncertain_routes:
            self.assertEqual(routes[0].steps,((0,1),));self.assertEqual(routes[0].component,0)
    def test_no_terminal_only_or_wrong_start_negative(self):
        m=self.m(singleton(1))
        for trace in (((),),((),()),((0,),())):
            body=dict(k_trace=trace,w_trace=((0,),(),()))
            with self.subTest(trace=trace):self.assertIsNone(self.cert.check_negative(m,body))
    def test_wrong_intermediate_premature_or_repeated_trace_rejected(self):
        m=self.m(separator()); good=self.api.solve(m)
        for w in (((0,1),(0,),(),()),((0,1),(0,),(0,)),((0,1),(0,),(),(),()),((0,1),(0,1),(0,),(),())):
            with self.subTest(w=w):self.assertIsNone(self.cert.check_negative(m,dict(k_trace=good.k_trace,w_trace=w)))
    def test_negative_exclusion_and_canonical_syntax(self):
        m=self.m(singleton());body=dict(k_trace=((0,),(0,)),w_trace=((0,),(0,)))
        self.assertIsNone(self.cert.check_negative(m,body))
        for body in (None,dict(k_trace=(),w_trace=()),dict(k_trace=([0],(),()),w_trace=((0,),(),())),
                     dict(k_trace=((False,),(),()),w_trace=((0,),(),())),dict(k_trace=((0,),(),()),w_trace=((0,),(),()),success=True)):
            with self.subTest(body=body):self.assertIsNone(self.cert.check_negative(self.m(singleton(1)),body))
    def test_checkers_never_call_solve(self):
        m=self.m(singleton(1));negative=self.api.solve(m)
        with patch('synthesis.solve',side_effect=AssertionError('validator called solve')):
            self.assertIsNotNone(self.cert.check_negative(m,negative))
            self.assertIsNotNone(self.cert.check_positive(self.m(bernoulli()),bernoulli_body()))
    def test_resource_exhaustion_is_not_negative(self):
        with patch('synthesis.all_components',side_effect=MemoryError('bounded execution failed')):
            with self.assertRaises(MemoryError):self.api.solve(self.m(singleton()))
