"""Wrapper boundary tests; no theorem source is changed by this test suite."""
from pathlib import Path
import importlib.util,json,os,sys,tempfile,unittest,shutil,subprocess
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('shared_root_replay',HERE/'replay.py')
replay=importlib.util.module_from_spec(spec);spec.loader.exec_module(replay)
class BoundaryTests(unittest.TestCase):
 def api(self,name):
  fn=getattr(replay,name,None);self.assertTrue(callable(fn),'missing required wrapper API: '+name);return fn
 def test_existing_output_untouched(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'out';p.mkdir();(p/'sentinel').write_text('unchanged')
   with self.assertRaises(RuntimeError): replay.require_fresh_output(p,[])
   self.assertEqual((p/'sentinel').read_text(),'unchanged')
 def test_protected_and_symlinked_output(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/'input';root.mkdir();link=Path(d)/'link';link.symlink_to(root,target_is_directory=True)
   for out in [root/'new',link/'new']:
    with self.assertRaises(RuntimeError):replay.require_fresh_output(out,[root])
    self.assertFalse(out.exists())
 def test_manifest_paths_fail_closed(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'ok').write_text('x');(root/'link').symlink_to(root/'ok')
   for name in ['../ok','/ok','./ok','a/../ok','link']:
    with self.assertRaises(RuntimeError):replay.regular_path(root,name)
 def test_extra_empty_directory_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'PUBLIC_MANIFEST.json').write_text('{}');(root/'extra').mkdir()
   with self.assertRaises(RuntimeError):replay.exact_inventory(root,[],'PUBLIC_MANIFEST.json')
 def test_corrupt_file_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/'x';p.write_text('a');r={'path':'x','bytes':1,'sha256':replay.digest(p)};p.write_text('b')
   with self.assertRaises(RuntimeError):replay.verify_record(root,r)
 def test_nested_token_audit(self):
  text=replay.proof_tokens('/- sorry /- unsafe -/ admit -/\ndef s := "axiom"\n-- native_decide\ntheorem ok : True := by trivial')
  self.assertNotRegex(text,r'\b(sorry|admit|axiom|unsafe|native_decide)\b')
  self.assertIn('sorry',replay.proof_tokens('theorem no : False := by sorry'))
 def test_mutant_requires_intended_diagnostic(self):
  classify=self.api('classify_mutant')
  self.assertEqual(classify(1,'error: type mismatch expected budget',False,['type mismatch','expected budget']),'REJECTED_AS_EXPECTED')
  self.assertEqual(classify(1,'error: unrelated',False,['type mismatch']),'UNCLASSIFIED_FAILURE')
  self.assertEqual(classify(0,'',False,['type mismatch']),'UNEXPECTED_SUCCESS')
 def test_mutant_resource_failure_is_inconclusive(self):
  classify=self.api('classify_mutant')
  for text in ['error: maximum recursion depth has been reached','error: maximum number of heartbeats','error: unknown module prefix','out of memory']:
   self.assertEqual(classify(1,text,False,['error:']),'RESOURCE_OR_INFRASTRUCTURE_INCONCLUSIVE')
  self.assertEqual(classify(None,'partial intended error',True,['intended error']),'RESOURCE_OR_INFRASTRUCTURE_INCONCLUSIVE')
 def test_timeout_preserves_diagnostics(self):
  run=self.api('run_compiler_stage')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'log';r=run([sys.executable,'-u','-c','import time;print("partial",flush=True);time.sleep(2)'],dict(os.environ),p,.15)
   self.assertTrue(r['timed_out']);self.assertIsNone(r['exit_code']);self.assertIn('partial',p.read_text());self.assertIn('REPLAY_TIMEOUT',p.read_text())
 def test_dependency_inventory_and_bytes(self):
  verify=self.api('verify_tree_pin')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'lib').mkdir();(p/'lib/x').write_text('original')
   pin={'roots':['lib'],'entries':[{'path':'lib','kind':'directory'},{'path':'lib/x','kind':'file','bytes':8,'sha256':replay.digest(p/'lib/x')}]}
   verify(p,pin);(p/'lib/x').write_text('modified')
   with self.assertRaises(RuntimeError):verify(p,pin)
   (p/'lib/x').write_text('original');(p/'lib/extra').write_text('x')
   with self.assertRaises(RuntimeError):verify(p,pin)
 def test_dependency_symlink_escape_rejected(self):
  verify=self.api('verify_tree_pin')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'root';p.mkdir();(p/'escape').symlink_to(Path(d)/'outside')
   with self.assertRaises(RuntimeError):verify(p,{'roots':[''],'entries':[{'path':'escape','kind':'symlink','target':'../outside'}]})
 def test_timeout_bounds_reject_nan(self):
  valid=self.api('valid_timeout')
  for t in [0,-1,float('nan'),float('inf'),601]:self.assertFalse(valid(t))
  self.assertTrue(valid(.1));self.assertTrue(valid(600))
 def test_mutant_patterns_match_frozen_diagnostics(self):
  for name,(_,patterns) in replay.MUTANTS.items():
   path=HERE/'historical/typed-v1/controls/mutants'/name/'EXPECTED_FAILURE.log'
   self.assertEqual(replay.classify_mutant(1,path.read_text(),False,patterns),'REJECTED_AS_EXPECTED')
 def test_independent_cache_pin_cannot_be_rebound(self):
  with tempfile.TemporaryDirectory() as d:
   copied=Path(d)/'packet';shutil.copytree(HERE,copied);pin=copied/'dependencies/MATHLIB_CACHE_PIN.json';pin.write_text('{}')
   public=json.loads((copied/'PUBLIC_MANIFEST.json').read_text())
   for rec in public['files']:
    if rec['path']=='dependencies/MATHLIB_CACHE_PIN.json':rec.update(bytes=2,sha256=replay.digest(pin))
   (copied/'PUBLIC_MANIFEST.json').write_text(json.dumps(public));old=replay.ROOT
   try:
    replay.ROOT=copied
    with self.assertRaisesRegex(RuntimeError,'Pinned input changed'):replay.verify_checkpoint()
   finally:replay.ROOT=old
 def test_failed_dependency_check_writes_failure_only(self):
  with tempfile.TemporaryDirectory() as d:
   base=Path(d);out=base/'new-output'
   r=subprocess.run([sys.executable,str(HERE/'replay.py'),'--lean-root',str(base/'missing-lean'),
     '--mathlib',str(base/'missing-mathlib'),'--output',str(out)],capture_output=True,text=True,
     env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=30)
   self.assertNotEqual(r.returncode,0);self.assertTrue((out/'REPLAY_FAILURE.json').is_file())
   self.assertFalse((out/'RECEIPT.json').exists());receipt=json.loads((out/'REPLAY_FAILURE.json').read_text())
   self.assertEqual(receipt['status'],'FAIL');self.assertTrue(receipt['no_success_receipt'])
 def test_unlisted_file_in_whole_packet_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   copied=Path(d)/'packet';shutil.copytree(HERE,copied);(copied/'unlisted').write_text('x');old=replay.ROOT
   try:
    replay.ROOT=copied
    with self.assertRaisesRegex(RuntimeError,'inventory mismatch'):replay.verify_checkpoint()
   finally:replay.ROOT=old
 def actual_reviewer_lint(self):
  text=(HERE/'historical/wrapper-v1/ReviewerControls.log').read_text()
  oldpath=text.split(':66:44: warning:',1)[0]
  source=HERE/'review/ReviewerControls.lean'
  return source,text.replace(oldpath,str(source))
 def test_exact_historical_lint_is_allowed(self):
  check=self.api('positive_diagnostics_ok');source,text=self.actual_reviewer_lint()
  self.assertTrue(check('ReviewerControls',replay.digest(source),text,source))
 def test_lint_exception_rejects_wrong_stage_or_hash(self):
  check=self.api('positive_diagnostics_ok');source,text=self.actual_reviewer_lint()
  self.assertFalse(check('AliasModel',replay.digest(source),text,source))
  self.assertFalse(check('ReviewerControls','0'*64,text,source))
 def test_lint_exception_rejects_other_diagnostics(self):
  check=self.api('positive_diagnostics_ok');source,text=self.actual_reviewer_lint()
  for extra in ['warning: another warning','error: bad','sorryAx']:
   self.assertFalse(check('ReviewerControls',replay.digest(source),text+'\n'+extra,source))
  self.assertFalse(check('ReviewerControls',replay.digest(source),text.replace("simp at quorum","simp at other"),source))
 def test_lint_exception_requires_exact_occurrence_counts(self):
  check=self.api('positive_diagnostics_ok');source,text=self.actual_reviewer_lint()
  self.assertFalse(check('ReviewerControls',replay.digest(source),text+text,source))
  self.assertFalse(check('ReviewerControls',replay.digest(source),'',source))
if __name__=='__main__':unittest.main()
