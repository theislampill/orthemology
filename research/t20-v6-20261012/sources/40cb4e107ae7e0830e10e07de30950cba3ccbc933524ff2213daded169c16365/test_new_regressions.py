"""New P03 tests. Run first against the unchanged source; later against a proposal.
P03-U03-CE01 deletes the roundtrip invariant by allowing one extra container.
P03-U04-CE01 deletes snapshot-before-validation and retains caller-owned mutation.
These are not a replay/relabel of the historical integration controls.
"""
import linecache, os, sys, threading, unittest
sys.path.insert(0, os.environ['P03_SOURCE'])
import boundaries as b
import operational as o

class NewRegressions(unittest.TestCase):
    def test_dump_success_is_inside_load_domain_at_empty_container_boundary(self):
        value=[]
        for _ in range(b.MAX_DEPTH):value=[value]
        self.assertEqual(b.bound_tree(value),b.MAX_DEPTH+1)
        try:raw=b.dump_json(value)
        except b.Rejection:return  # a bounded encoder may refuse before success
        try:decoded=b.load_json(raw)
        except b.Rejection as ex:
            self.fail(f'P03-U03-CE01: dump succeeded ({len(raw)} bytes) but load rejected: {ex}')
        self.assertEqual(decoded,value)

    def test_observation_snapshot_is_validated_before_blocking_on_registry_lock(self):
        engine=o.Engine.standard();values=[0,0];at_lock=threading.Event();errors=[]
        def trace(frame,event,arg):
            if (event=='line' and frame.f_code.co_name=='set_observation'
                and frame.f_globals.get('__name__')=='operational'
                and 'with self._lock:' in linecache.getline(frame.f_code.co_filename,frame.f_lineno)):
                at_lock.set()
            return trace
        def worker():
            sys.settrace(trace)
            try:engine.set_observation('p03',values)
            except BaseException as ex:errors.append(ex)
            finally:sys.settrace(None)
        with engine._lock:  # test-only scheduling; no registry mutation
            t=threading.Thread(target=worker,name='p03-observation-setter');t.start()
            ready=at_lock.wait(2)
            if ready:values[1]='changed-after-validation'
        t.join(2)
        self.assertTrue(ready,'test did not reach the intended scheduling boundary')
        self.assertFalse(t.is_alive(),'test thread did not finish')
        self.assertEqual(errors,[])
        self.assertEqual(engine._observations['p03'],(0,0),
            'P03-U04-CE01: successful setter committed data not covered by its validation')

if __name__=='__main__':unittest.main(verbosity=2)
