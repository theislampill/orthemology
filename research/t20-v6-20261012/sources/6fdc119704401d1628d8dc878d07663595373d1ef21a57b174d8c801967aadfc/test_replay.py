"""Portable wrapper contract tests; no proof result is inferred from mocks."""
from pathlib import Path
import importlib.util,json,os,tempfile,unittest,hashlib,math,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('batch_replay',ROOT/'replay.py')
replay=importlib.util.module_from_spec(spec);spec.loader.exec_module(replay)

def sha(b):return hashlib.sha256(b).hexdigest()

class WrapperContracts(unittest.TestCase):
    def test_timeout_is_finite_positive_bounded(self):
        for x in [0,-1,float('nan'),float('inf'),601]:self.assertFalse(replay.valid_timeout(x))
        for x in [0.01,30,600]:self.assertTrue(replay.valid_timeout(x))
    def test_canonical_paths_reject_escapes_and_aliases(self):
        for p in ['../x','/x','a/../x','a//x','a/./x','a\\x','']:
            with self.assertRaises(RuntimeError):replay.canonical_relative(p)
        self.assertEqual(str(replay.canonical_relative('science/X.lean')),'science/X.lean')
    def test_existing_and_protected_output_refused(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);source=base/'source';source.mkdir()
            for target in [source,source/'build']:
                with self.assertRaises(RuntimeError):replay.require_fresh_output(target,[source])
            self.assertEqual(replay.require_fresh_output(base/'new',[source]),(base/'new').resolve())
    def test_source_symlink_refused(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);(base/'real').write_text('data');(base/'alias').symlink_to('real')
            with self.assertRaises(RuntimeError):replay.regular_path(base,'alias')
    def test_unlisted_source_file_refused(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);(base/'known').write_text('x');(base/'MANIFEST.json').write_text('{}')
            records=[{'path':'known'}];replay.exact_inventory(base,records,'MANIFEST.json')
            (base/'Foreign.olean').write_bytes(b'poison')
            with self.assertRaises(RuntimeError):replay.exact_inventory(base,records,'MANIFEST.json')
    def test_nested_comments_do_not_hide_real_proof_escape(self):
        tokens=replay.proof_tokens('/- sorry /- axiom -/ -/ theorem t : True := by trivial')
        self.assertNotIn('sorry',tokens);self.assertNotIn('axiom',tokens)
        self.assertIn('sorry',replay.proof_tokens('theorem bad : False := by sorry'))
        with self.assertRaises(RuntimeError):replay.proof_tokens('/- unfinished')
    def test_dependency_byte_tamper_and_extra_file_refused(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);(base/'cache').mkdir();file=base/'cache/A.olean';file.write_bytes(b'exact')
            pin={'roots':['cache'],'entries':[{'path':'cache','kind':'directory'},
                {'path':'cache/A.olean','kind':'file','bytes':5,'sha256':sha(b'exact')}]}
            replay.verify_tree_pin(base,pin)
            file.write_bytes(b'wrong')
            with self.assertRaises(RuntimeError):replay.verify_tree_pin(base,pin)
            file.write_bytes(b'exact');(base/'cache/Extra.olean').write_bytes(b'extra')
            with self.assertRaises(RuntimeError):replay.verify_tree_pin(base,pin)
    def test_only_exact_path_metadata_relocation_is_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);rel='.lake/build/lib/lean/Cache/Hashing.trace';file=base/rel;file.parent.mkdir(parents=True)
            old='/workspace/shared/lean-toolchain-4.19.0/lean-4.19.0-linux/bin/lean'
            known='/known/lean-toolchain-4.19.0/lean-4.19.0-linux/bin/lean'
            launcher=base/'third compiler/bin/lean';launcher.parent.mkdir(parents=True);launcher.write_bytes(b'unit fixture')
            original=('{"log":[{"message":" '+old+' Cache/Hashing.lean --json"}],"depHash":"123"}\n').encode()
            current=original.replace(old.encode(),known.encode())
            entry={'path':rel,'kind':'file','bytes':len(original),'sha256':sha(original)}
            pin={'roots':['.lake/build/lib/lean/Cache'],'entries':[{'path':'.lake/build/lib/lean/Cache','kind':'directory'},entry]}
            relocation={'current_prefix':'/known/','historical_prefix':'/workspace/shared/','files':[{'path':rel,
                'current_sha256':sha(current),'current_bytes':len(current),
                'original_pin_sha256':sha(original),'original_pin_bytes':len(original),'replacement_count':1}]}
            file.write_bytes(original);self.assertEqual(replay.verify_tree_pin(base,pin,relocation,launcher),[])
            file.write_bytes(current)
            with self.assertRaises(RuntimeError):replay.verify_tree_pin(base,pin)
            used=replay.verify_tree_pin(base,pin,relocation,launcher)
            self.assertEqual(used[0]['path'],rel);self.assertEqual(used[0]['mode'],'known_restored_launcher')
            third=original.replace(old.encode(),str(launcher.resolve()).encode());file.write_bytes(third)
            used=replay.verify_tree_pin(base,pin,relocation,launcher)
            self.assertEqual(used[0]['mode'],'supplied_pinned_launcher')
            self.assertEqual(used[0]['raw_sha256'],sha(third))
            for bad in [third+str(launcher.resolve()).encode(),third.replace(b'--json',b'--bad'),third.replace(b'123',b'999')]:
                file.write_bytes(bad)
                with self.assertRaises(RuntimeError):replay.verify_tree_pin(base,pin,relocation,launcher)
    def test_loader_and_lean_environment_are_fully_sanitized(self):
        hostile={'LEAN_PATH':'poison','LEAN_SYSROOT':'poison','LEAN_SRC_PATH':'poison',
            'LD_AUDIT':'poison.so','LD_PRELOAD':'poison.so','LD_LIBRARY_PATH':'poison',
            'LD_DEBUG_OUTPUT':'/elsewhere/out','LD_PROFILE_OUTPUT':'/elsewhere/profile',
            'DYLD_INSERT_LIBRARIES':'poison.so','KEEP_EXPECTED':'yes'}
        before=dict(os.environ)
        try:
            os.environ.update(hostile)
            env=replay.sanitized_env([Path('/isolated/build')],Path('/pinned/mathlib'),{'roots':['cache']})
            self.assertEqual(env['LEAN_PATH'],'/isolated/build'+os.pathsep+'/pinned/mathlib/cache')
            self.assertEqual(env['KEEP_EXPECTED'],'yes')
            for key in hostile:
                if key not in ['LEAN_PATH','KEEP_EXPECTED']:self.assertTrue(key not in env,f'Environment key leaked: {key}')
        finally:os.environ.clear();os.environ.update(before)
    def test_real_version_probe_timeout_is_inconclusive(self):
        with tempfile.TemporaryDirectory() as d:
            result=replay.run_compiler_stage([sys.executable,'-c','import time; time.sleep(0.3)'],
                dict(os.environ),Path(d)/'timeout.log',0.02)
            self.assertTrue(result['timed_out'])
            self.assertEqual(replay.failure_classification(result),'INCONCLUSIVE')
            result=replay.run_compiler_stage([sys.executable,'-c','print("warning: probe")'],
                dict(os.environ),Path(d)/'warning.log',5)
            self.assertFalse(replay.clean_positive_result(result))
            self.assertEqual(replay.failure_classification(result),'FAIL')
    def test_launcher_oserror_is_inconclusive(self):
        with tempfile.TemporaryDirectory() as d:
            result=replay.run_compiler_stage([str(Path(d)/'absent-launcher')],dict(os.environ),Path(d)/'launch.log',1)
            self.assertEqual(replay.failure_classification(result),'INCONCLUSIVE')
            self.assertFalse(replay.clean_positive_result(result))
    def test_failure_removes_new_success_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);(base/'RECEIPT.json').write_text('{"status":"PASS"}')
            replay.record_failure(base,'FAIL',RuntimeError('controlled boundary'),[], 'bound-public-identity')
            self.assertFalse((base/'RECEIPT.json').exists())
            self.assertEqual(json.loads((base/'REPLAY_FAILURE.json').read_text())['status'],'FAIL')
    def test_mixed_resource_or_uppercase_diagnostic_cannot_pass(self):
        for text in ['REPLAY_TIMEOUT despite zero exit','maximum recursion depth reached',
            'WARNING: synthetic diagnostic','ERROR: synthetic diagnostic']:
            result={'timed_out':False,'exit_code':0,'text':text}
            self.assertFalse(replay.clean_positive_result(result),text)
        result={'timed_out':False,'exit_code':0,'text':'REPLAY_TIMEOUT despite zero exit'}
        self.assertEqual(replay.failure_classification(result),'INCONCLUSIVE')
    def test_axiom_audit_refuses_missing_duplicate_or_nonstandard(self):
        good="'A.x' depends on axioms: [propext, Quot.sound]\n"
        self.assertEqual(set(replay.audit_axioms(good,['A.x'])),{'A.x'})
        for text,names in [(good,['A.x','A.y']),(good+good,['A.x']),
            ("'A.x' depends on axioms: [sorryAx]\n",['A.x'])]:
            with self.assertRaises(RuntimeError):replay.audit_axioms(text,names)

if __name__=='__main__':unittest.main()
