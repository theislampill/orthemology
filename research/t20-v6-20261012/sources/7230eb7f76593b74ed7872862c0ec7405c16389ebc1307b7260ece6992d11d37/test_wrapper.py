"""Mutation-sensitive tests for the portable replay boundary; no Lean needed."""
from pathlib import Path
import hashlib, importlib.util, json, os, subprocess, sys, tempfile, unittest
BASE=Path(__file__).resolve().parents[1]
WRAPPER=(BASE/'replay.py') if (BASE/'replay.py').exists() else BASE/'stage'/'Orthemic_Signed_Controller_Service_v1'/'replay.py'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

class WrapperBoundaryTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue(WRAPPER.exists(), 'Portable replay wrapper is not implemented')
  spec=importlib.util.spec_from_file_location('signed_replay',WRAPPER)
  self.m=importlib.util.module_from_spec(spec); spec.loader.exec_module(self.m)
  self.tmp=tempfile.TemporaryDirectory(prefix='signed wrapper test ')
  self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name)/'packet'; self.root.mkdir()
  (self.root/'replay.py').write_text('# trusted entrypoint\n')
  (self.root/'src').mkdir(); (self.root/'src'/'A.lean').write_text('def a := 1\n')
  self.rows=[{'path':'src/A.lean','sha256':sha(self.root/'src/A.lean'),'bytes':11}]
  self.pin=self.write_manifest()
 def write_manifest(self):
  p=self.root/'PACKAGE_MANIFEST.json';p.write_text(json.dumps({'format':1,'files':self.rows}))
  return sha(p)
 def verify(self):return self.m.verify_package(self.root,self.pin)
 def test_clean_exact_census_passes(self):self.assertEqual(len(self.verify()['files']),1)
 def test_absent_manifest_fails_closed(self):
  (self.root/'PACKAGE_MANIFEST.json').unlink()
  with self.assertRaisesRegex(RuntimeError,'manifest'):self.verify()
 def test_changed_manifest_fails_closed(self):
  (self.root/'PACKAGE_MANIFEST.json').write_text('{}')
  with self.assertRaisesRegex(RuntimeError,'manifest'):self.verify()
 def test_changed_source_fails_closed(self):
  (self.root/'src/A.lean').write_text('def a := 2\n')
  with self.assertRaisesRegex(RuntimeError,'changed'):self.verify()
 def test_unexpected_source_fails_closed(self):
  (self.root/'src/B.lean').write_text('def b := 1\n')
  with self.assertRaisesRegex(RuntimeError,'census'):self.verify()
 def test_unexpected_binary_fails_closed(self):
  (self.root/'src/A.olean').write_bytes(b'not allowed')
  with self.assertRaisesRegex(RuntimeError,'census'):self.verify()
 def test_symlink_file_fails_closed(self):
  (self.root/'src/A.lean').unlink();(self.root/'src/A.lean').symlink_to('/tmp/no-source')
  with self.assertRaisesRegex(RuntimeError,'symlink'):self.verify()
 def test_symlink_directory_fails_closed(self):
  (self.root/'extra').symlink_to(self.root/'src',target_is_directory=True)
  with self.assertRaisesRegex(RuntimeError,'symlink'):self.verify()
 def test_path_escape_fails_closed(self):
  self.rows[0]['path']='../A.lean';self.pin=self.write_manifest()
  with self.assertRaisesRegex(RuntimeError,'path'):self.verify()
 def test_absolute_path_fails_closed(self):
  self.rows[0]['path']='/tmp/A.lean';self.pin=self.write_manifest()
  with self.assertRaisesRegex(RuntimeError,'path'):self.verify()
 def test_duplicate_row_fails_closed(self):
  self.rows.append(self.rows[0].copy());self.pin=self.write_manifest()
  with self.assertRaisesRegex(RuntimeError,'duplicate'):self.verify()
 def test_existing_output_refused(self):
  out=Path(self.tmp.name)/'exists';out.mkdir()
  with self.assertRaisesRegex(RuntimeError,'absent'):self.m.validate_output(out,[self.root])
 def test_protected_output_refused(self):
  with self.assertRaisesRegex(RuntimeError,'protected'):self.m.validate_output(self.root/'out',[self.root])
 def test_symlink_output_parent_refused(self):
  link=Path(self.tmp.name)/'alias';link.symlink_to(self.root,target_is_directory=True)
  with self.assertRaisesRegex(RuntimeError,'protected'):self.m.validate_output(link/'out',[self.root])
 def test_external_absent_output_accepted(self):
  out=Path(self.tmp.name)/'fresh';self.assertEqual(self.m.validate_output(out,[self.root]),out)
 def test_environment_ignores_caller_lean_path(self):
  env=self.m.clean_env([Path('/fresh new'),Path('/deps')],{'LEAN_PATH':'/evil','LEAN_SRC_PATH':'/evil','PYTHONPATH':'/evil','LEAN_NUM_THREADS':'99','X':'keep'})
  self.assertEqual(env['LEAN_PATH'],'/fresh new:/deps');self.assertNotIn('LEAN_SRC_PATH',env);self.assertNotIn('PYTHONPATH',env);self.assertEqual(env['LEAN_NUM_THREADS'],'1');self.assertEqual(env['X'],'keep')
 def test_native_guard_failure_accepted(self):
  self.m.check_outcome(1,1,'x.lean:2:0: error: expression\n  !mutant [0]\ndid not evaluate to `true`\n')
 def test_typos_do_not_count_as_mutation_detection(self):
  for txt in ['error: unknown identifier\ndid not evaluate to `true`','error: failed to synthesize\ndid not evaluate to `true`','error: expression\ndid not evaluate to `true`\nx.lean:4:0: error: unknown module prefix']:
   with self.subTest(txt=txt),self.assertRaises(RuntimeError):self.m.check_outcome(1,1,txt)
 def test_multiple_guard_failures_do_not_count_as_one_fault(self):
  with self.assertRaises(RuntimeError):self.m.check_outcome(1,1,'error: expression\ndid not evaluate to `true`\nerror: expression\ndid not evaluate to `true`')
 def test_timeout_does_not_count_as_mutation_detection(self):
  with self.assertRaisesRegex(RuntimeError,'wall'):self.m.check_outcome(None,1,'WALL_CLOCK_LIMIT')
 def test_sorry_success_refused(self):
  with self.assertRaisesRegex(RuntimeError,'sorry'):self.m.check_outcome(0,0,"warning: declaration uses 'sorry'")
 def test_nonstandard_axiom_refused(self):
  with self.assertRaisesRegex(RuntimeError,'axiom'):self.m.check_outcome(0,0,'foo depends on axioms: [propext, injected]')
 def test_optimized_python_refused(self):
  p=subprocess.run([sys.executable,'-O',str(WRAPPER),'--verify-only'],capture_output=True,text=True)
  self.assertNotEqual(p.returncode,0);self.assertIn('Optimized Python',p.stderr+p.stdout)

if __name__=='__main__':unittest.main(verbosity=2)
