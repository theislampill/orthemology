from pathlib import Path
import importlib.util,json,os,subprocess,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('route_context',ROOT/'tools/context.py');ctx=importlib.util.module_from_spec(spec);spec.loader.exec_module(ctx)
class SafetyTests(unittest.TestCase):
 def run_script(self,name,*args):
  return subprocess.run([sys.executable,'-E','-S','-B',str(ROOT/'tools'/name),*map(str,args)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 def test_existing_work_refused(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);sentinel=p/'KEEP';sentinel.write_text('unchanged')
   r=self.run_script('prepare.py','--work',p,'--toolchain',p/'missing')
   self.assertNotEqual(r.returncode,0);self.assertIn('must be absent',r.stdout);self.assertEqual(sentinel.read_text(),'unchanged')
 def test_unsupported_path_refused(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'work space';r=self.run_script('prepare.py','--work',p,'--toolchain',Path(tmp)/'missing')
   self.assertNotEqual(r.returncode,0);self.assertIn('without whitespace or colons',r.stdout);self.assertFalse(p.exists())
 def test_wrong_toolchain_refused_before_work(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);work=p/'absent';r=self.run_script('prepare.py','--work',work,'--toolchain',p/'missing')
   self.assertNotEqual(r.returncode,0);self.assertFalse(work.exists())
 def test_no_arbitrary_build_target(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=self.run_script('run_build.py','--work',tmp,'unapproved')
   self.assertNotEqual(r.returncode,0);self.assertIn('invalid choice',r.stdout)
 def test_altered_original_refused(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);original=p/'original';original.mkdir();(original/'MANIFEST.json').write_text('{}');derived=p/'SOURCE_BUILD_bad'
   r=self.run_script('derive_package.py','--work',p/'work','--original-package',original,'--derived-package',derived)
   self.assertNotEqual(r.returncode,0);self.assertFalse(derived.exists());self.assertEqual((original/'MANIFEST.json').read_text(),'{}')
 def test_clean_environment(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/'environment.json').write_text(json.dumps({'LEAN_PATH':'','LEAN_SRC_PATH':'','LEAN_NUM_THREADS':'2'}))
   keys={'LEAN_SYSROOT':'poison','LEAN_PATH':'poison','LEAN_ARBITRARY':'poison','LD_LIBRARY_PATH':'poison','LD_PRELOAD':'poison','PYTHONPATH':'poison','LAKE_HOME':'poison'}
   old={k:os.environ.get(k) for k in keys}
   try:
    os.environ.update(keys);env=ctx.isolated_environment(p)
    self.assertEqual(env['LEAN_PATH'],'');self.assertEqual(env['LEAN_NUM_THREADS'],'2')
    for k in set(keys)-{'LEAN_PATH'}:self.assertNotIn(k,env)
   finally:
    for k,v in old.items():
     if v is None:os.environ.pop(k,None)
     else:os.environ[k]=v
 def test_replaced_build_log_refused_before_acceptance(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/'evidence').mkdir();(p/'config.json').write_text(json.dumps({'toolchain':str(p/'toolchain')}))
   (p/'evidence/DEPENDENCY_COLD_BUILD.json').write_text(json.dumps({'status':'PASS','exit_code':0,'log_sha256':'0'*64}))
   (p/'evidence/DEPENDENCY_COLD_BUILD.log').write_text('substituted build log')
   r=self.run_script('verify_cold_build.py','--work',p)
   self.assertNotEqual(r.returncode,0);self.assertIn('Build log changed after its originating execution receipt',r.stdout)
   self.assertFalse((p/'evidence/COLD_DEPENDENCY_BUILD_RECEIPT.json').exists())
 def test_final_binder_exact_manifest_only_delta(self):
  bind=json.loads((ROOT/'FINAL_BASE_BINDING.json').read_text())
  old=(ROOT/'tools/derive_package.py').read_text();new=(ROOT/'tools/derive_final_package.py').read_text()
  self.assertEqual(old.count(bind['retained_v3_manifest_sha256']),1)
  self.assertEqual(new,old.replace(bind['retained_v3_manifest_sha256'],bind['consumer_manifest_sha256']))
 def test_optimisation_rejected(self):
  r=subprocess.run([sys.executable,'-E','-S','-O',str(ROOT/'tools/prepare.py'),'--help'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  self.assertNotEqual(r.returncode,0);self.assertIn('Assertions must be enabled',r.stdout)
if __name__=='__main__':unittest.main(verbosity=2)
