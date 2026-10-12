from pathlib import Path
import importlib.util,json,os,stat,sys,tempfile,unittest,zipfile
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('review_replay',Path(__file__).with_name('replay_review.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
class CompanionContracts(unittest.TestCase):
    def test_safe_zip_extract_and_existing_destination(self):
        with tempfile.TemporaryDirectory() as d:
            b=Path(d);z=b/'source.zip'
            with zipfile.ZipFile(z,'w') as f:f.writestr(r.SOURCE_FOLDER+'/x.txt','exact')
            root=r.safe_extract(z,b/'out');self.assertEqual((root/'x.txt').read_text(),'exact')
            with self.assertRaises(RuntimeError):r.safe_extract(z,b/'out')
    def test_traversal_wrong_root_and_symlink_refused_before_writes(self):
        with tempfile.TemporaryDirectory() as d:
            b=Path(d)
            for k,name in enumerate(['../escape','Other/x',r.SOURCE_FOLDER+'/../escape',r.SOURCE_FOLDER+'\\x']):
                z=b/f'{k}.zip'
                with zipfile.ZipFile(z,'w') as f:f.writestr(name,'bad')
                out=b/f'out{k}'
                with self.assertRaises(RuntimeError):r.safe_extract(z,out)
                self.assertFalse(out.exists())
            z=b/'link.zip';info=zipfile.ZipInfo(r.SOURCE_FOLDER+'/link');info.create_system=3;info.external_attr=(stat.S_IFLNK|0o777)<<16
            with zipfile.ZipFile(z,'w') as f:f.writestr(info,'/elsewhere')
            with self.assertRaises(RuntimeError):r.safe_extract(z,b/'linkout')
    def test_protected_output_refused(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source=root/'source';source.mkdir()
            with self.assertRaises(RuntimeError):r.fresh_output(source/'child',[source])
    def test_real_source_process_timeout_stops_group(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            result=r.run_source_command([sys.executable,'-c','import time; time.sleep(1)'],dict(os.environ),root/'log',0.03,root)
            self.assertTrue(result['timed_out']);self.assertIsNone(result['exit_code'])
            self.assertIn('REPLAY_TIMEOUT',result['text'])
    def test_bound_child_inconclusive_status_is_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            def record(status,identity):
                (root/'REPLAY_FAILURE.json').write_text(json.dumps({'status':status,
                    'public_manifest_sha256':identity,'no_success_receipt':True}))
            self.assertEqual(r.propagated_source_failure(root,'FAIL'),'FAIL')
            record('INCONCLUSIVE',r.SOURCE_PUBLIC_SHA)
            self.assertEqual(r.propagated_source_failure(root,'FAIL'),'INCONCLUSIVE')
            record('FAIL',r.SOURCE_PUBLIC_SHA)
            self.assertEqual(r.propagated_source_failure(root,'INCONCLUSIVE'),'FAIL')
            record('INCONCLUSIVE','wrong-binding')
            self.assertEqual(r.propagated_source_failure(root,'FAIL'),'FAIL')
if __name__=='__main__':unittest.main()
