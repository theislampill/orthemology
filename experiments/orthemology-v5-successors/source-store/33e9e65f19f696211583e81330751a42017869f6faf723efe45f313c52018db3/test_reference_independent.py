"""Adversarial API tests authored from the public contract before source read."""

import copy
import dataclasses
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
REFERENCE = HERE.parents[1] / 'research' / 'hidden-change' / 'reference-v1'
sys.path.insert(0, str(REFERENCE))
from model import validate_model
from finite import component, reachable
from certificates import check_positive, check_negative, Positive, Negative
from synthesis import solve, known_operator, uncertain_operator
from controller import initial_memory, choose, observe, action_for_history, threshold, rejection
from oracle import Input, raw_model, regions, good_component


def fixture(n=1, a=1, p=None, d=None, menus=None, initial=0):
    p = p or (lambda t, s, act: tuple(Q(y == s) for y in range(n)))
    d = d or (lambda t, s, act: 0)
    m = Input(n, a, initial, menus or tuple(tuple(range(a)) for _ in range(n)),
              tuple(tuple(tuple(tuple(p(t, s, act)) for act in range(a))
                          for s in range(n)) for t in (0, 1)),
              tuple(tuple(tuple(d(t, s, act) for act in range(a))
                          for s in range(n)) for t in (0, 1)))
    return m


def numerical(equal=False):
    return fixture(2, 2,
                   p=lambda t,s,a: (Q(1,2),Q(1,2)) if t == 0 or equal
                                   else (Q(1,3),Q(2,3)),
                   d=lambda t,s,a: 2 if t == a else 1)


def reveal_fixture():
    return fixture(2, 1,
                   p=lambda t,s,a: (Q(1),Q(0)) if t == 0 and s == 0
                                   else (Q(0),Q(1)),
                   d=lambda t,s,a: 1 if t == 1 and s == 0 else 0)


def checked(raw):
    model = validate_model(raw_model(raw))
    body = solve(model)
    assert isinstance(body, Positive)
    assert check_positive(model, body) is not None
    return model, body


def empty_k_body():
    route = dict(source=0, steps=(), component=0, reveal=None)
    return dict(K=(), W=(0,), D1=(), D=((0,0),), known_components=(),
                uncertain_components=((((0,0),),), (((0,0),),)),
                known_routes=(), uncertain_routes=((route,), (copy.deepcopy(route),)))


class ModelBoundary(unittest.TestCase):
    def test_exact_fraction_roundtrip(self):
        m = validate_model(raw_model(numerical()))
        self.assertIsInstance(m.rows[1][0][0][0], Q)
        self.assertEqual(m.rows[1][0][0][0], Q(1,3))

    def test_malformed_models(self):
        base = raw_model(fixture())
        mutations = []
        for key, value in [('n_states', True), ('n_states', 0), ('n_actions', False),
                           ('initial', -1), ('initial', True), ('initial', 1),
                           ('menus', ((),)), ('menus', ((True,),)),
                           ('priorities', (((False,),), ((0,),))),
                           ('priorities', (((-1,),), ((0,),))),
                           ('rows', ((((0.0,),),), (((1,),),))),
                           ('rows', (((('1/0',),),), (((1,),),))),
                           ('rows', (((('2/2',),),), (((1,),),))),
                           ('rows', ((((0,),),), (((1,),),)))]:
            raw = copy.deepcopy(base)
            raw[key] = value
            mutations.append(raw)
        extra = copy.deepcopy(base); extra['winning'] = True; mutations.append(extra)
        for index, raw in enumerate(mutations):
            with self.subTest(index=index), self.assertRaises(ValueError):
                validate_model(raw)

    def test_unavailable_action_rows_are_validated(self):
        raw = raw_model(fixture(1,2,menus=((0,),)))
        raw['rows'][1][0][1] = ['-1']
        with self.assertRaises(ValueError):
            validate_model(raw)


class FiniteBoundary(unittest.TestCase):
    def test_row_comparison_checks_every_receipt(self):
        inp=fixture(3,p=lambda t,s,a:(Q(1,3),Q(1,3),Q(1,3)) if t==0
                                   else (Q(1,3),Q(1,6),Q(1,2)),
                    d=lambda t,s,a:t)
        m=validate_model(raw_model(inp)); pairs=((0,0),(1,0),(2,0))
        self.assertEqual(m.rows[0][0][0][0],m.rows[1][0][0][0])
        self.assertTrue(component(m,0,pairs,uncertain=True))
        self.assertFalse(component(m,1,pairs,uncertain=True))

    def test_support_is_not_numerical_equality(self):
        inp = numerical()
        m = validate_model(raw_model(inp))
        pairs = ((0,0),(1,0))
        self.assertTrue(good_component(inp, 0, frozenset(pairs), True))
        self.assertTrue(component(m, 0, pairs, uncertain=True))
        self.assertFalse(component(validate_model(raw_model(numerical(True))),0,pairs,uncertain=True))
        self.assertIsInstance(solve(m), Positive)
        self.assertIsInstance(solve(validate_model(raw_model(numerical(True)))), Negative)

    def test_nonmaximal_and_used_priorities(self):
        m = validate_model(raw_model(fixture(1,2,d=lambda t,s,a: 2 if a == 0 else 1)))
        self.assertTrue(component(m,1,((0,0),)))
        self.assertFalse(component(m,1,((0,0),(0,1))))
        self.assertTrue(component(m,0,((0,0),),uncertain=True))
        self.assertIsInstance(solve(m), Positive)

    def test_disconnected_and_nonclosed_reject(self):
        m = validate_model(raw_model(fixture(2)))
        self.assertFalse(component(m,1,((0,0),(1,0))))
        m = validate_model(raw_model(fixture(2,p=lambda t,s,a:(Q(1,2),Q(1,2)))))
        self.assertFalse(component(m,1,((0,0),)))
        self.assertTrue(component(m,1,((0,0),(1,0))))

    def test_candidate_revelation_disqualifies_component(self):
        m = validate_model(raw_model(reveal_fixture()))
        self.assertFalse(component(m,1,((0,0),(1,0)),uncertain=True))
        self.assertEqual(reachable(m,0,((0,0),(1,0)),1,compatible_only=True),frozenset({0}))

    def test_separator(self):
        inp = fixture(2, p=lambda t,s,a: tuple(Q(y == (1-s if t == 0 else s)) for y in range(2)),
                      d=lambda t,s,a:s)
        self.assertEqual(regions(inp),(frozenset({0}),frozenset()))
        m = validate_model(raw_model(inp)); body = solve(m)
        self.assertIsInstance(body,Negative)
        self.assertEqual(body.k_trace[-1],(0,))
        self.assertEqual(body.w_trace[-1],())
        self.assertIsNotNone(check_negative(m,body))


class PositiveBodyBoundary(unittest.TestCase):
    def setUp(self):
        self.m = validate_model(raw_model(fixture()))
        self.b = empty_k_body()

    def test_valid_body_empty_k_zero_length_route(self):
        self.assertIsNotNone(check_positive(self.m,self.b))

    def test_strict_body_syntax(self):
        mutations = []
        for key,value in [('K',[]), ('W',(0,0)), ('W',(True,)), ('W',()),
                          ('D',((0,0),(0,0))), ('D',((0,1),)),
                          ('D1',((0,0),)), ('known_routes',(dict(source=0,steps=(),component=0,reveal=None),)),
                          ('uncertain_routes',((),self.b['uncertain_routes'][1])),
                          ('uncertain_components',((),self.b['uncertain_components'][1]))]:
            b = copy.deepcopy(self.b); b[key]=value; mutations.append(b)
        b=copy.deepcopy(self.b); b['winning']=True; mutations.append(b)
        for i,b in enumerate(mutations):
            with self.subTest(index=i):
                self.assertIsNone(check_positive(self.m,b))

    def test_malformed_route_fields(self):
        mutations=[]
        for key,value in [('source',True),('source',1),('steps',((0,0),)),
                          ('steps',[]),('component',True),('component',1),
                          ('component',None),('reveal',(0,0)),('extra',True)]:
            b=copy.deepcopy(self.b); b['uncertain_routes'][0][0][key]=value; mutations.append(b)
        b=copy.deepcopy(self.b); b['uncertain_routes']=(b['uncertain_routes'][0]*2,b['uncertain_routes'][1]); mutations.append(b)
        for i,b in enumerate(mutations):
            with self.subTest(index=i):
                self.assertIsNone(check_positive(self.m,b))

    def test_omitted_positive_successor(self):
        m=validate_model(raw_model(fixture(2,p=lambda t,s,a:(Q(1,2),Q(1,2)))))
        self.assertIsNone(check_positive(m,self.b))

    def test_reveal_requires_k(self):
        m,b=checked(reveal_fixture())
        raw=dataclasses.asdict(b); raw['K']=(); raw['D1']=(); raw['known_components']=(); raw['known_routes']=()
        self.assertIsNone(check_positive(m,raw))

    def test_checker_does_not_consult_solver(self):
        import synthesis
        old=synthesis.solve
        try:
            synthesis.solve=lambda *args: (_ for _ in ()).throw(AssertionError('checker called solver'))
            self.assertIsNotNone(check_positive(self.m,self.b))
        finally:
            synthesis.solve=old


class NegativeBodyBoundary(unittest.TestCase):
    def test_arbitrary_fixed_point_is_not_greatest(self):
        m=validate_model(raw_model(fixture()))
        self.assertEqual(known_operator(m,frozenset()),frozenset())
        self.assertEqual(uncertain_operator(m,frozenset(),frozenset()),frozenset())
        self.assertIsNone(check_negative(m,dict(k_trace=((),()),w_trace=((),()))))
        self.assertIsNone(check_negative(m,dict(k_trace=((0,),(),()),w_trace=((0,),(),()))))

    def test_exact_negative_and_malformed_traces(self):
        m=validate_model(raw_model(fixture(d=lambda t,s,a:3)))
        body=solve(m); self.assertIsInstance(body,Negative)
        self.assertIsNotNone(check_negative(m,body))
        for trace in [(), ((),), ((0,),), ((0,),()), ((0,),(0,)),
                      ((0,),(),(),()), ((True,),(),()), ((0,0),(),()), [((0,),(),())]]:
            with self.subTest(trace=trace):
                self.assertIsNone(check_negative(m,dict(k_trace=trace,w_trace=body.w_trace)))


class ControllerBoundary(unittest.TestCase):
    def test_component_exit_and_rejection_increment_only_once(self):
        inp=fixture(2,p=lambda t,s,a:(Q(1,2),Q(1,2)) if t==0
                                  else tuple(Q(y==s) for y in range(2)))
        m,b=checked(inp)
        base=dataclasses.replace(initial_memory(m,b),phase=1)
        action,prepared=choose(m,b,base,0)
        self.assertIsNotNone(prepared.retained)
        # theta1 expects state0 forever; this compatible exit also rejects it.
        prepared=dataclasses.replace(prepared,departures=(1,0),uses=((1,),(0,)),
            receipts=(((0,1),),((0,0),)))
        updated=observe(m,b,prepared,0,action,1)
        self.assertEqual(updated.phase,2)
        self.assertFalse(updated.known1)
        self.assertIsNone(updated.retained)

    def test_impossible_after_known1_enters_persistent_fallback(self):
        inp=fixture(2,p=lambda t,s,a:tuple(Q(y==(1-s if t==0 else s)) for y in range(2)))
        m,b=checked(inp); base=initial_memory(m,b)
        action,prepared=choose(m,b,base,0)
        known=observe(m,b,prepared,0,action,0) # P0-zero, P1-positive.
        self.assertTrue(known.known1)
        action,prepared=choose(m,b,known,0)
        fallback=observe(m,b,prepared,0,action,1) # P1-zero after revelation.
        self.assertTrue(fallback.fallback)
        action,prepared=choose(m,b,fallback,1)
        again=observe(m,b,prepared,1,action,0)
        self.assertTrue(again.fallback)

    def test_strict_gate_and_exact_threshold(self):
        m,b=checked(numerical()); base=initial_memory(m,b)
        self.assertEqual(threshold(m),Q(1,12))
        def counters(phase,total,first):
            return dataclasses.replace(base,phase=phase,
                departures=(total,0),uses=((total,0),(0,0)),
                receipts=(((first,total-first),(0,0)),((0,0),(0,0))))
        self.assertFalse(rejection(m,counters(12,12,0)))  # N == r: strict gate closed.
        self.assertTrue(rejection(m,counters(12,13,0)))   # N == r+1: gate open.
        self.assertTrue(rejection(m,counters(0,12,5)))    # discrepancy exactly delta.
        self.assertFalse(rejection(m,counters(0,13,6)))  # strictly smaller discrepancy.
        self.assertFalse(rejection(m,base))               # no division by zero.
        same,b_same=checked(fixture())
        self.assertEqual(threshold(same),Q(1))

    def test_stale_counts_do_not_permanently_eliminate_candidate(self):
        m,b=checked(numerical()); base=initial_memory(m,b)
        stale=dataclasses.replace(base,phase=12,departures=(12,0),
            uses=((12,0),(0,0)),receipts=(((0,12),(0,0)),((0,0),(0,0))))
        # A finite stale pair has an arbitrarily poor estimate, but cannot
        # reject the current true phase after the phase gate reaches its count.
        self.assertFalse(rejection(m,stale))
        action,prepared=choose(m,b,stale,1)
        updated=observe(m,b,prepared,1,action,0)
        self.assertFalse(updated.known1)
        self.assertEqual(updated.phase,12) # Both finite counts fail the strict gate.
        action,prepared=choose(m,b,base,0)
        updated=observe(m,b,prepared,0,action,0)
        self.assertEqual(updated.phase,1)  # Early theta0 rejection re-enters theta1.
        action,prepared=choose(m,b,updated,0)
        self.assertEqual(action,1)         # Candidate1's component remains available.

    def test_known1_revelation_precedence_and_permanence(self):
        m,b=checked(reveal_fixture()); memory=initial_memory(m,b)
        action,prepared=choose(m,b,memory,0)
        memory=observe(m,b,prepared,0,action,1)
        self.assertTrue(memory.known1)
        self.assertEqual(memory.phase,0)
        self.assertEqual(memory.departures[0],1)
        for _ in range(3):
            action,prepared=choose(m,b,memory,1)
            memory=observe(m,b,prepared,1,action,1)
            self.assertTrue(memory.known1)
            self.assertEqual(memory.phase,0)

    def test_p1_zero_does_not_announce_known1(self):
        inp=fixture(2,p=lambda t,s,a:tuple(Q(y == (1-s if t == 0 else s)) for y in range(2)))
        m,b=checked(inp); memory=initial_memory(m,b)
        action,prepared=choose(m,b,memory,0)
        memory=observe(m,b,prepared,0,action,1)
        self.assertFalse(memory.known1)
        self.assertFalse(memory.fallback)

    def test_all_bounded_histories_lawful(self):
        m,b=checked(numerical()); total=0
        for depth in range(4):
            for history in product(range(2),repeat=2*depth+1):
                action=action_for_history(m,b,history)
                self.assertIn(action,m.menus[history[-1]])
                total+=1
        self.assertEqual(total,170)

    def test_history_validation(self):
        m,b=checked(numerical())
        for history in [(),(0,0),(True,),(2,),(0,True,1),(0,-1,1),(0,2,1),(0,0,2),'0']:
            with self.subTest(history=history),self.assertRaises(ValueError):
                action_for_history(m,b,history)

    def test_replay_matches_incremental_on_all_receipt_words(self):
        m,b=checked(numerical())
        for receipts in product(range(2),repeat=5):
            memory=initial_memory(m,b); state=m.initial; history=[state]
            for receipt in receipts:
                action,prepared=choose(m,b,memory,state)
                self.assertEqual(action,action_for_history(m,b,history))
                memory=observe(m,b,prepared,state,action,receipt)
                history.extend((action,receipt)); state=receipt
            action,_=choose(m,b,memory,state)
            self.assertEqual(action,action_for_history(m,b,history))


if __name__=='__main__':
    unittest.main(verbosity=2)
