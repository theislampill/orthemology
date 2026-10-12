#!/usr/bin/env python3
"""New attempt2 regression gates; --mode baseline records real predecessor failures."""
from pathlib import Path
import contextlib, inspect, json, os, sys, unittest
MODE='proposal'
if '--mode' in sys.argv:
    i=sys.argv.index('--mode'); MODE=sys.argv[i+1]; del sys.argv[i:i+2]
BASE=Path(os.environ.get('P03_BASE','private-locator:2b638f3fdccf0e1e2e94'))
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'proposal'),str(BASE)]
import boundaries as b
import operational as op
if MODE=='proposal':
    from atomic_engine import AtomicEngine
    from safe_frontend import encode_owned, snapshot_native, export_module_owned
else:
    AtomicEngine=op.Engine
    encode_owned=b.dump_json
HISTORIES=[]

def core(engine):return engine._engine if hasattr(engine,'_engine') else engine

def logical_state(engine):
    e=core(engine)
    return {'epoch':e._epoch,'rules':dict(e._rules),'observations':dict(e._observations),
            'prob_observations':dict(e._prob_observations),'prob_requirements':dict(e._prob_requirements),
            'issued':dict(e._issued),'issuer':e._issuer}

@contextlib.contextmanager
def before_line(fn,needle,exception=None,action=None):
    lines,start=inspect.getsourcelines(fn)
    targets=[start+i for i,line in enumerate(lines) if needle in line]
    if len(targets)!=1:raise RuntimeError(('ambiguous fault point',fn.__name__,needle,targets))
    fired=[];previous=sys.gettrace()
    def trace(frame,event,arg):
        if event=='line' and frame.f_code is fn.__code__ and frame.f_lineno==targets[0] and not fired:
            fired.append({'function':fn.__name__,'line':targets[0],'source':lines[targets[0]-start].strip()})
            if action: action(frame)
            if exception: raise exception('controlled fault at '+fn.__name__)
        return trace
    sys.settrace(trace)
    try:yield fired
    finally:sys.settrace(previous)

class Frontier(unittest.TestCase):
    def test_failed_revision_is_atomic(self):
        e=AtomicEngine.standard();e.set_observation('v',[0,0])
        lic=e.admit({'op':'edge','size':2,'source':0,'target':1})
        before=logical_state(e)
        with self.assertRaises(MemoryError):
            with before_line(op.Engine.set_observation,"for key in ['vocabulary'",MemoryError) as fired:
                e.set_observation('v',[0,1])
        after=logical_state(e)
        HISTORIES.append({'id':'P03-A2-CE-HOST-REVISION','mode':MODE,'fault':fired,
            'before_observations':before['observations'],'after_observations':after['observations'],
            'before_rules':before['rules'],'after_rules':after['rules'],
            'old_licence_current':e.describe(lic)['current'],'dispatch_result':e.dispatch(lic,0),
            'logical_state_unchanged':before==after})
        self.assertEqual(before,after,'failed revision exposed a partial state')
    def test_successful_encode_always_decodes(self):
        x={'v':0}
        with before_line(b.dump_json,'encoder=json.JSONEncoder',action=lambda frame:x.__setitem__('v',1.25)) as fired:
            try:raw=encode_owned(x); refusal=None
            except b.Rejection as ex:raw=None;refusal=str(ex)
        problem=None;decoded=None
        if raw is not None:
            try:decoded=b.load_json(raw)
            except b.Rejection as ex:problem=str(ex)
        HISTORIES.append({'id':'P03-A2-CE-MUTABLE-ENCODE','mode':MODE,'mutation':fired,
             'caller_after':x,'returned_bytes':raw.decode() if raw else None,
             'decode_error':problem,'encoder_refusal':refusal,'decoded':decoded})
        self.assertIsNone(problem,'encoder returned bytes rejected by its decoder')
    def test_no_effect_on_issued_record_construction_failure(self):
        e=AtomicEngine.standard();before=logical_state(e)
        with self.assertRaises(MemoryError):
            with before_line(op.Engine.admit_json,'return Licence(',MemoryError):
                e.admit({'op':'primitive','name':'succ'})
        self.assertEqual(before,logical_state(e))
    def test_aba_versions_do_not_revive_old_licence(self):
        e=AtomicEngine.standard();lic=e.admit({'op':'primitive','name':'succ'})
        e.revise_rule('primitive:succ',False);e.revise_rule('primitive:succ',True)
        self.assertFalse(e.describe(lic)['current'])
        with self.assertRaises(b.Rejection):e.dispatch(lic,1)
        fresh=e.revalidate(lic);self.assertEqual(e.dispatch(fresh,1),2)
        self.assertNotEqual(lic.ticket,fresh.ticket)
    def test_failed_dispatch_does_not_change_registry(self):
        e=AtomicEngine.standard();lic=e.admit({'op':'primitive','name':'succ'});before=logical_state(e)
        with self.assertRaises(b.Rejection):e.dispatch(lic,2**256-1)
        self.assertEqual(before,logical_state(e));self.assertTrue(e.describe(lic)['current'])
    def test_output_is_not_registry_alias(self):
        e=AtomicEngine.standard();lic=e.admit({'op':'copy','type':'nat'});out=e.dispatch(lic,3)
        out.append(8);self.assertEqual(e.dispatch(lic,3),[3,3])
        desc=e.describe(lic);desc['bindings'].clear();self.assertTrue(e.describe(lic)['bindings'])
    def test_owned_snapshot_breaks_nested_aliases(self):
        shared=[1];x={'x':shared,'y':shared};v=snapshot_native(x)
        shared[0]=2
        self.assertEqual(b.load_json(encode_owned(v)),{'x':[1],'y':[1]})
    def test_snapshot_rejects_cycles_and_subclasses(self):
        a=[];a.append(a)
        class Evil(list):
            def __iter__(self):raise AssertionError('foreign iterator executed')
        for value in [a,Evil([1]),{'a':object()},1.5,{'bad':float('nan')}]:
            with self.assertRaises(b.Rejection):snapshot_native(value)
    def test_snapshot_rejects_invalid_strings_and_integers(self):
        for value in ['\ud800','x'*4097,2**256,{-1:'not a string key'}]:
            with self.assertRaises(b.Rejection):snapshot_native(value)
    def test_snapshot_preserves_scalars_and_tuple_json_normalisation(self):
        x={'v':(None,False,True,0,-1,'é','"\\[]')}
        self.assertEqual(b.load_json(encode_owned(x)),{'v':[None,False,True,0,-1,'é','"\\[]']})
    def test_module_capture_rejects_arbitrary_iterable_rows(self):
        proof=b.dump_json({'rule':'i','A':['bottom']})
        with self.assertRaises(b.Rejection):export_module_owned([iter(('a',proof))])
        text=export_module_owned([('a',proof)])
        self.assertIn('def aCertificate : Cert',text)
    def test_export_capture_checks_the_same_count_it_traverses(self):
        # A double len() read can validate one row, then traverse an arbitrary
        # number added by a caller. The bounded entry must never read >16 rows.
        raw=b.dump_json({'rule':'i','A':['bottom']});examples=[('a',raw)]
        lines,start=inspect.getsourcelines(export_module_owned)
        count_line=next(start+i for i,x in enumerate(lines) if 'count = len(examples)' in x)
        read_line=next(start+i for i,x in enumerate(lines) if 'row = get_outer(examples, i)' in x)
        mutated=False;reads=[];previous=sys.gettrace()
        def trace(frame,event,arg):
            nonlocal mutated
            if event=='line' and frame.f_code is export_module_owned.__code__:
                if frame.f_lineno==count_line and not mutated:
                    mutated=True;examples.extend((f'x{i}',raw) for i in range(16))
                if frame.f_lineno==read_line:reads.append(frame.f_locals['i'])
            return trace
        sys.settrace(trace)
        try:
            try:export_module_owned(examples)
            except b.Rejection:pass
        finally:sys.settrace(previous)
        self.assertTrue(mutated)
        self.assertLessEqual(len(reads),16,'validated length was not the traversed length')
    def test_public_reentrancy_cannot_erase_nested_success(self):
        e=AtomicEngine.standard();nested=[]
        def reenter(frame):
            try:e.revise_rule('primitive:succ',False);nested.append('success')
            except b.Rejection:nested.append('refused')
        with before_line(AtomicEngine._call,'self._engine = private',action=reenter):
            e.set_observation('v',[0,0])
        current=core(e)._rules['primitive:succ'][1]
        self.assertFalse(nested==['success'] and current,
                         'successful nested disable was overwritten by stale outer clone')
        self.assertEqual(nested,['refused'])
        self.assertEqual(core(e)._observations['v'],(0,0))
    def test_postcommit_cancellation_is_not_rollback(self):
        e=AtomicEngine.standard();before=logical_state(e)
        with self.assertRaises(KeyboardInterrupt):
            with before_line(AtomicEngine._call,'return result',KeyboardInterrupt):
                e.set_observation('v',[0,0])
        self.assertNotEqual(before,logical_state(e))
        self.assertEqual(core(e)._observations['v'],(0,0))
        # This is a completed publication with an interrupted response, not a
        # certificate that the caller observed a successful return.
        lic=e.admit({'op':'primitive','name':'succ'})
        self.assertEqual(e.dispatch(lic,1),2)
    def test_refusal_does_not_mean_logical_bottom(self):
        e=AtomicEngine.standard();before=logical_state(e)
        with self.assertRaises(b.Rejection):e.admit({'op':'compose','first':{'op':'primitive','name':'not'},'second':{'op':'primitive','name':'succ'}})
        self.assertEqual(before,logical_state(e))

if __name__=='__main__':
    program=unittest.main(exit=False,verbosity=2)
    dest=os.environ.get('P03_HISTORY_OUT')
    if dest:Path(dest).write_text(json.dumps(HISTORIES,indent=2)+'\n')
    raise SystemExit(0 if program.result.wasSuccessful() else 1)
