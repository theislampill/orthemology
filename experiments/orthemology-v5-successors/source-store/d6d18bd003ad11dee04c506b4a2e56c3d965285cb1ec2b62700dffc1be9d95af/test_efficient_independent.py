"""Independent pre-source adversarial specification tests."""
import copy
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import sys
import unittest

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
REFERENCE=ROOT/'tranche18/research/hidden-change/reference-v1'
EFFICIENT=ROOT/'tranche18/research/hidden-change/efficient-v1'
sys.path[:0]=[str(EFFICIENT),str(REFERENCE)]
from oracle import (fixture,raw_model,full_pairs,subsets,all_end_components,
                    maximal_allowed,qualifying,target_union)
from model import validate_model
from certificates import Positive,Negative,check_positive,check_negative as original_negative
from mec import maximal_components
from efficient import known_components,uncertain_components,known_operator,uncertain_operator,solve
from negative import check_negative


def verify_components(inp):
    model=validate_model(raw_model(inp))
    all_ends={theta:all_end_components(inp,theta) for theta in (0,1)}
    for allowed in subsets(full_pairs(inp)):
        for theta in (0,1):
            actual=maximal_components(model,theta,allowed)
            assert isinstance(actual,tuple)
            assert actual==tuple(sorted(set(actual)))
            actual_sets=frozenset(frozenset(c) for c in actual)
            assert actual_sets==maximal_allowed(all_ends[theta],allowed),(inp,theta,allowed,actual)
            for c in actual:
                assert c==tuple(sorted(set(c))) and frozenset(c)<=allowed
            for c in all_ends[theta]:
                if c<=allowed: assert any(c<=got for got in actual_sets)
            sources=[target_union((c,)) for c in actual_sets]
            assert all(not (sources[i]&sources[j]) for i in range(len(sources)) for j in range(i))
        for theta,uncertain in ((1,False),(0,True),(1,True)):
            actual=uncertain_components(model,theta,allowed) if uncertain else known_components(model,allowed)
            assert actual==tuple(sorted(set(actual)))
            assert all(frozenset(c)<=allowed and qualifying(inp,theta,frozenset(c),uncertain) for c in actual)
            expected=[c for c in all_ends[theta] if c<=allowed and qualifying(inp,theta,c,uncertain)]
            assert target_union(actual)==target_union(expected),(inp,theta,allowed,actual,expected)
    return model


class ExactComponents(unittest.TestCase):
    def test_empty_singleton_disconnected(self):
        for n in (1,2,3): verify_components(fixture(n))

    def test_two_separate_attained_minima(self):
        inp=fixture(1,3,d=lambda t,s,a:((2,3,1),(3,2,1))[t][a])
        model=verify_components(inp)
        expected=(((0,0),(0,1)),)
        self.assertEqual(uncertain_components(model,0,full_pairs(inp)),expected)
        self.assertEqual(uncertain_components(model,1,full_pairs(inp)),expected)
        self.assertIsInstance(solve(model),Positive)

    def test_good_subcomponent_in_odd_maximal(self):
        inp=fixture(1,2,d=lambda t,s,a:(2,1)[a])
        model=verify_components(inp)
        self.assertEqual(maximal_components(model,1,full_pairs(inp)),(((0,0),(0,1)),))
        self.assertEqual(known_components(model,full_pairs(inp)),(((0,0),),))

    def test_candidate_specific_not_common_closure(self):
        for theta in (0,1):
            inp=fixture(2,p=lambda t,s,a:tuple(Q(y==s) for y in range(2)) if t==theta
                        else (Q(1,2),Q(1,2)),d=lambda t,s,a:2 if t==theta else 1)
            model=verify_components(inp)
            self.assertEqual(uncertain_components(model,theta,frozenset({(0,0)})),(((0,0),),))

    def test_nonrevelation_deletes_whole_pair(self):
        inp=fixture(2,p=lambda t,s,a:tuple(Q(y==s) for y in range(2)) if t==0 else (Q(1,2),Q(1,2)))
        model=verify_components(inp)
        self.assertEqual(uncertain_components(model,1,full_pairs(inp)),())

    def test_escaping_successor_then_recursive_split(self):
        def row(t,s,a):
            targets=({1,2} if a==0 else {0}) if s==0 else ({0} if a==0 else {1}) if s==1 else {2}
            return tuple(Q(int(y in targets),len(targets)) for y in range(3))
        inp=fixture(3,2,p=row)
        model=verify_components(inp)
        self.assertEqual(maximal_components(model,0,full_pairs(inp)),
                         (((0,1),),((1,1),),((2,0),(2,1))))
        # Keeping only the favourable outcome 1 would wrongly return {0,1}.

    def test_row_equality_uses_every_coordinate(self):
        inp=fixture(3,p=lambda t,s,a:(Q(1,3),Q(1,3),Q(1,3)) if t==0 else (Q(1,3),Q(1,6),Q(1,2)),
                    d=lambda t,s,a:t)
        model=verify_components(inp)
        self.assertEqual(target_union(uncertain_components(model,0,full_pairs(inp))),frozenset(range(3)))
        self.assertEqual(uncertain_components(model,1,full_pairs(inp)),())

    def test_same_support_unequal_rows_changes_answer(self):
        for equal in (False,True):
            inp=fixture(2,2,p=lambda t,s,a:(Q(1,2),Q(1,2)) if t==0 or equal else (Q(1,3),Q(2,3)),
                        d=lambda t,s,a:2 if t==a else 1)
            model=verify_components(inp)
            self.assertIsInstance(solve(model),Negative if equal else Positive)

    def test_large_binary_priority_gap(self):
        huge=2**4096
        inp=fixture(1,3,d=lambda t,s,a:((huge,huge+1,1),(huge+1,huge,1))[t][a])
        model=verify_components(inp)
        body=solve(model)
        self.assertIsInstance(body,Positive)
        self.assertIsNotNone(check_positive(model,body))

    def test_static_switch_separator(self):
        inp=fixture(2,p=lambda t,s,a:tuple(Q(y==(1-s if t==0 else s)) for y in range(2)),d=lambda t,s,a:s)
        model=verify_components(inp); body=solve(model)
        self.assertIsInstance(body,Negative)
        self.assertEqual(body.k_trace[-1],(0,)); self.assertEqual(body.w_trace[-1],())
        self.assertIsNotNone(check_negative(model,body))


class ExactNegative(unittest.TestCase):
    def test_body_syntax_and_trace_bounds(self):
        model=validate_model(raw_model(fixture(d=lambda t,s,a:3)))
        body=solve(model); self.assertIsInstance(body,Negative)
        self.assertEqual(body.k_trace,((0,),(),()))
        self.assertEqual(body.w_trace,((0,),(),()))
        self.assertEqual(len(body.k_trace),model.n_states+2)
        self.assertIsNotNone(check_negative(model,body))
        traces=[None,(),((),),((0,),),((0,),()),((0,),(0,)),((0,),(),(),()),
                ((True,),(),()),((0,0),(),()),((1,),(),()),[(0,),(),()],
                ((0,),(0,),(),()),((0,),(),(0,),()),((),(),())]
        bad_bodies=[None,{},dict(k_trace=body.k_trace),
                    dict(k_trace=body.k_trace,w_trace=body.w_trace,success=False)]
        for field in ('k_trace','w_trace'):
            for trace in traces:
                raw=dict(k_trace=body.k_trace,w_trace=body.w_trace);raw[field]=trace
                bad_bodies.append(raw)
        for raw in bad_bodies:
            with self.subTest(raw=raw):
                self.assertIsNone(original_negative(model,raw))
                self.assertIsNone(check_negative(model,raw))
        # A valid start/fixed point still fails when the initial state is included.
        winning=validate_model(raw_model(fixture()))
        for raw in (dict(k_trace=((0,),(0,)),w_trace=((0,),(0,))),
                    dict(k_trace=((),()),w_trace=((),())),
                    dict(k_trace=((0,),(),()),w_trace=((0,),(),()))):
            self.assertIsNone(check_negative(winning,raw))
            self.assertIsNone(original_negative(winning,raw))

    def test_long_strict_descent_chain(self):
        # Internal states can initially reach the good state with positive probability.
        # Removing the bad sink then removes one newly unsafe action per step.
        def row(t,s,a):
            targets={s} if s in (0,4) else {s-1,s+1}
            return tuple(Q(int(y in targets),len(targets)) for y in range(5))
        inp=fixture(5,p=row,d=lambda t,s,a:1 if s==4 else 0,initial=1)
        model=validate_model(raw_model(inp)); body=solve(model)
        self.assertIsInstance(body,Negative)
        self.assertIsNotNone(check_negative(model,body))
        self.assertIsNotNone(original_negative(model,body))
        self.assertEqual(len(body.k_trace),model.n_states+1)
        for trace in (body.k_trace,body.w_trace):
            self.assertLessEqual(len(trace),model.n_states+2)
            self.assertEqual(trace[0],tuple(range(5)))
            self.assertEqual(trace[-1],trace[-2])
            for left,right in zip(trace[:-2],trace[1:-1]): self.assertTrue(set(right)<set(left))


if __name__=='__main__': unittest.main(verbosity=2)
