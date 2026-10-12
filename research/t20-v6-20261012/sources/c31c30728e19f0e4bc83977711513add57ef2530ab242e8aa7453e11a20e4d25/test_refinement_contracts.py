"""Proposal-boundary tests, not universal proofs or integration requalification."""
import copy, json, os, sys, unittest
sys.path.insert(0,os.environ['P03_SOURCE'])
import boundaries as b
import operational as op


def state(e):
    """Complete logical engine state at a quiescent call boundary (not scheduler state)."""
    return (e._issuer,copy.deepcopy(e._rules),copy.deepcopy(e._observations),
            copy.deepcopy(e._issued),e._epoch,copy.deepcopy(e._prob_observations),
            copy.deepcopy(e._prob_requirements))


def model():
    return {'space':'tagged-uniform-intervals','law':'fixed-base-law',
            'weights':[[1,2],[1,2]],'view':[0,0],'events':'full-measurable'}


class BoundaryContract(unittest.TestCase):
    def test_scalar_at_depth_limit_remains_supported(self):
        x=0
        for _ in range(b.MAX_DEPTH):x=[x]
        self.assertEqual(b.load_json(b.dump_json(x)),x)

    def test_empty_container_at_last_allowed_json_level(self):
        x=[]
        for _ in range(b.MAX_DEPTH-1):x=[x]
        self.assertEqual(b.load_json(b.dump_json(x)),x)

    def test_encode_canonicalisation_is_a_value_quotient_not_byte_identity(self):
        x={'z':(1,True,None),'a':'é'}
        raw=b.dump_json(x)
        self.assertEqual(b.load_json(raw),{'a':'é','z':[1,True,None]})
        self.assertEqual(b.dump_json(b.load_json(raw)),raw)

    def test_integer_and_unicode_boundaries(self):
        for x in [-(2**256-1),2**256-1,False,'\U0001f642'*4096]:
            with self.subTest(kind=type(x).__name__):self.assertEqual(b.load_json(b.dump_json(x)),x)
        for x in [2**256,-2**256,'\ud800']:
            with self.subTest(rejected=type(x).__name__):
                with self.assertRaises(b.Rejection):b.dump_json(x)

    def test_parser_refusals_are_not_semantic_falsity(self):
        for raw in [b'{"x":1,"x":2}',b'1.0',b'NaN',b'\xff',b'{',b'1e0']:
            with self.subTest(raw=raw):
                with self.assertRaises(b.Rejection):b.load_json(raw)

    def test_decoder_success_does_not_promise_encoder_budget_success(self):
        x=['é'*4096]*30
        raw=json.dumps(x,ensure_ascii=False,separators=(',',':')).encode()
        self.assertLess(len(raw),b.MAX_BYTES)
        decoded=b.load_json(raw)
        with self.assertRaisesRegex(b.Rejection,'output bytes'):b.dump_json(decoded)

    def test_cycles_refused_without_mutating_caller_data(self):
        x=[];x.append(x)
        with self.assertRaises(b.Rejection):b.dump_json(x)
        self.assertIs(x[0],x)


class CompleteStateContract(unittest.TestCase):
    def test_observation_capture_preserves_positive_and_negative_boundaries(self):
        e=op.Engine.standard()
        for i,x in enumerate([[0],[0]*4096,(3,2,1)]):
            e.set_observation(str(i),x)
            self.assertEqual(e._observations[str(i)],tuple(x))
        for x in [[],[0]*4097,[True],[-1],[2**256],['0']]:
            before=state(e)
            with self.assertRaises(b.Rejection):e.set_observation('bad',x)
            self.assertEqual(state(e),before)

    def test_rejections_preserve_all_seven_logical_state_components(self):
        e=op.Engine.standard();lic=e.admit({'op':'primitive','name':'succ'})
        calls=[
            lambda:e.admit_json(b'{"op":"id","op":"copy","type":"nat"}'),
            lambda:e.admit({'op':'unknown'}),
            lambda:e.dispatch(lic,True),
            lambda:e.dispatch(lic,2**256-1),
            lambda:e.dispatch(op.Licence('0'*48,object()),0),
            lambda:e.revise_rule('schema',False),
            lambda:e.set_observation('bad',[-1]),
            lambda:e.remove_observation('missing'),
            lambda:e.set_probability_observation('bad',{}),
            lambda:e.refine_probability_observation('missing',model()),
            lambda:e.coarsen_probability_observation('missing',model()),
            lambda:e.require_probability('primitive:succ','missing',[0,1]),
            lambda:e.remove_probability_requirement('primitive:succ'),
            lambda:e.project(limit=0),
        ]
        for i,call in enumerate(calls):
            with self.subTest(branch=i):
                before=state(e)
                with self.assertRaises(b.Rejection):call()
                self.assertEqual(state(e),before)
                self.assertFalse(e._lock._is_owned())

    def test_absence_readset_and_exact_requirement_revision_delta(self):
        e=op.Engine.standard();e.set_probability_observation('signal',model())
        lic=e.admit({'op':'primitive','name':'succ'})
        self.assertEqual(dict(e._issued[lic.ticket].bindings),
          {'schema':(0,True),'primitive:succ':(0,True),'need:primitive:succ':(0,True)})
        before=state(e);e.require_probability('primitive:succ','signal',[0,1]);after=state(e)
        self.assertIs(before[0],after[0]);self.assertEqual(after[4],before[4]+1)
        self.assertEqual(after[2:4],before[2:4]);self.assertEqual(after[5],before[5])
        self.assertEqual(after[1],{**before[1],'need:primitive:succ':(1,True)})
        self.assertEqual(after[6],{'primitive:succ':('signal',(0,1))})
        self.assertFalse(e.describe(lic)['current'])
        e.remove_probability_requirement('primitive:succ')
        self.assertEqual(e._stamp('need:primitive:succ'),(2,True))
        self.assertFalse(e.describe(lic)['current'])
        self.assertEqual(e.dispatch(e.revalidate(lic),5),6)

    def test_observation_mutation_delta_and_ticket_persistence(self):
        e=op.Engine.standard();lic=e.admit({'op':'primitive','name':'succ'})
        before=state(e);e.set_observation('v',[0,1]);after=state(e)
        self.assertEqual(after[1],{**before[1],'vocabulary':(1,True),'obs:v':(0,True)})
        self.assertEqual(after[2],{'v':(0,1)})
        self.assertEqual(after[3],before[3]);self.assertEqual(after[5:],before[5:])
        self.assertEqual(after[4],before[4]+1)
        self.assertTrue(e.describe(lic)['current'])
        e.remove_observation('v')
        self.assertEqual(e._stamp('obs:v'),(1,False))
        self.assertEqual(e._stamp('vocabulary'),(2,True))
        self.assertEqual(e._issued[lic.ticket],before[3][lic.ticket])

    def test_dispatch_does_not_mutate_registry_or_alias_output(self):
        e=op.Engine.standard();lic=e.admit({'op':'copy','type':['pair','nat','nat']})
        before=state(e);x=[1,2];y=e.dispatch(lic,x);y[0][0]=99
        self.assertEqual(x,[1,2]);self.assertEqual(y[1],[1,2]);self.assertEqual(state(e),before)

if __name__=='__main__':unittest.main(verbosity=2)
