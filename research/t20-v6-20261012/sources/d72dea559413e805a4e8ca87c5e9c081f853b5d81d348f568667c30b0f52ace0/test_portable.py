import unittest,tempfile,pathlib,json,hashlib,sys,zipfile
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
try: import portable_core as p
except ImportError: p=None
class PortableTests(unittest.TestCase):
 def setUp(self): self.assertIsNotNone(p,'portable_core must implement the fail-closed replay primitives')
 def test_manifest_binds_bytes(self):
  with tempfile.TemporaryDirectory() as td:
   r=pathlib.Path(td);(r/'a').write_text('x');m={'files':[{'path':'a','bytes':1,'sha256':hashlib.sha256(b'x').hexdigest()}]}
   self.assertEqual(p.validate_files(r,m),1);(r/'a').write_text('y')
   with self.assertRaises(ValueError):p.validate_files(r,m)
 def test_manifest_rejects_escape_duplicate_and_symlink(self):
  with tempfile.TemporaryDirectory() as td:
   r=pathlib.Path(td);(r/'a').write_text('x');(r/'link').symlink_to(r/'a')
   for path in ['../a','/tmp/a','link']:
    with self.assertRaises(ValueError):p.validate_files(r,{'files':[{'path':path,'bytes':1,'sha256':'x'}]})
   row={'path':'a','bytes':1,'sha256':hashlib.sha256(b'x').hexdigest()}
   with self.assertRaises(ValueError):p.validate_files(r,{'files':[row,row]})
 def test_graph_orders_custom_sources_and_rejects_missing(self):
  sources={'B':'import A\nimport Mathlib.Data.Nat.Basic\ntheorem b : True := True.intro','A':'/- import Evil -/\nimport Std\n'}
  self.assertEqual(p.order_modules(sources,['B']),['A','B'])
  with self.assertRaises(ValueError):p.order_modules({'B':'import Missing\n'},['B'])
  with self.assertRaises(ValueError):p.order_modules({'A':'import B\n','B':'import A\n'},['A'])
 def test_axiom_parser_requires_exact_targets_and_type(self):
  good="T.a : True\n'T.a' does not depend on any axioms\n"
  self.assertEqual(p.parse_audit(good,['T.a']),{'T.a':[]})
  for bad in [good+good,good.replace('T.a :','T.b :'),good.replace('does not depend on any axioms','depends on axioms: [sorryAx]'),good+'error: failed\n']:
   with self.assertRaises(ValueError):p.parse_audit(bad,['T.a'])
 def test_safe_zip_rejects_traversal(self):
  with tempfile.TemporaryDirectory() as td:
   r=pathlib.Path(td);z=r/'bad.zip'
   with zipfile.ZipFile(z,'w') as f:f.writestr('../escape','bad')
   with self.assertRaises(ValueError):p.extract_zip(z,r/'out')

class RunnerTests(unittest.TestCase):
 def test_replay_script_supports_explicit_paths(self):
  import subprocess
  script=pathlib.Path(__file__).resolve().parents[1]/'scripts/replay.py'
  self.assertTrue(script.is_file(),'portable CLI must exist')
  run=subprocess.run([sys.executable,'-B',str(script),'--help'],capture_output=True,text=True)
  self.assertEqual(run.returncode,0)
  for flag in ['--package-root','--out','--lean','--mathlib','--suite']:self.assertIn(flag,run.stdout)

class CanonicalIdentityTests(unittest.TestCase):
 def test_git_snapshot_rejects_wrong_blob_and_tree(self):
  self.assertTrue(hasattr(p,'verify_git_snapshot'),'canonical source verifier must recompute blob and tree identity')
  with tempfile.TemporaryDirectory() as td:
   z=pathlib.Path(td)/'src.zip';b=b'hello\n';blob=hashlib.sha1(b'blob 6\0'+b).hexdigest();raw=b'100644 file\0'+bytes.fromhex(blob);tree=hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
   with zipfile.ZipFile(z,'w') as f:f.writestr('file',b)
   identity={'tree':tree,'git_entries':[{'mode':'100644','type':'blob','git_blob':blob,'path':'file'}]}
   self.assertEqual(p.verify_git_snapshot(z,identity),1)
   identity['tree']='0'*40
   with self.assertRaises(ValueError):p.verify_git_snapshot(z,identity)

class EntryPointTests(unittest.TestCase):
 def test_integrity_and_python_entrypoints(self):
  import subprocess
  root=pathlib.Path(__file__).resolve().parents[1]
  for name in ['verify.py','replay_python.py']:
   script=root/'scripts'/name
   self.assertTrue(script.is_file(),name+' must provide a portable CLI')
   run=subprocess.run([sys.executable,'-B',str(script),'--help'],capture_output=True,text=True)
   self.assertEqual(run.returncode,0)

class MidRunSealTests(unittest.TestCase):
 def test_resealed_manifest_cannot_change_mid_run(self):
  self.assertTrue(hasattr(p,'verify_manifest'),'manifest identity must be stable through a run')
  with tempfile.TemporaryDirectory() as td:
   r=pathlib.Path(td);(r/'data').write_text('a')
   def seal():
    m={'files':[{'path':'data','bytes':1,'sha256':hashlib.sha256((r/'data').read_bytes()).hexdigest()}]};(r/'MASTER_MANIFEST.json').write_text(json.dumps(m));h=p.sha(r/'MASTER_MANIFEST.json');(r/'MASTER_MANIFEST.sha256').write_text(h+'  MASTER_MANIFEST.json\n');return h
   old=seal();self.assertEqual(p.verify_manifest(r),old);(r/'data').write_text('b');seal()
   with self.assertRaises(ValueError):p.verify_manifest(r,old)

class DependencyGraphTests(unittest.TestCase):
 def test_graph_is_bound_to_exact_source_bytes_and_imports(self):
  self.assertTrue(hasattr(p,'verify_source_graph'),'dependency graph must be checked against actual included sources')
  with tempfile.TemporaryDirectory() as td:
   r=pathlib.Path(td);(r/'sources/s').mkdir(parents=True);f=r/'sources/s/A.lean';f.write_text('import Std\n')
   suites=[{'id':'s','source_root':'sources/s','module_order':['A']}]
   graph=[{'suite':'s','module':'A','source':'sources/s/A.lean','sha256':p.sha(f),'imports':['Std']}]
   self.assertEqual(p.verify_source_graph(r,suites,graph),1)
   graph[0]['imports']=['Mathlib']
   with self.assertRaises(ValueError):p.verify_source_graph(r,suites,graph)

class EntrypointCensusTests(unittest.TestCase):
 def test_only_documented_lean_driver_is_shipped(self):
  root=pathlib.Path(__file__).resolve().parents[1]
  self.assertFalse((root/'scripts/replay_lean.py').exists(),'stale MANIFEST.json-based driver must not be shipped as a second entrypoint')

class P03RuntimeEntrypointTests(unittest.TestCase):
 def test_p03_runtime_replay_is_explicit_and_portable(self):
  import subprocess
  script=pathlib.Path(__file__).resolve().parents[1]/'scripts/replay_p03_runtime.py'
  self.assertTrue(script.is_file(),'P03 archived runtime tests need an explicit-path fresh-extraction runner')
  r=subprocess.run([sys.executable,'-B',str(script),'--help'],capture_output=True,text=True)
  self.assertEqual(r.returncode,0);self.assertIn('--out',r.stdout);self.assertIn('--package-root',r.stdout)

class ReplayIsolationTests(unittest.TestCase):
 def test_official_cache_cannot_supply_custom_module(self):
  self.assertTrue(hasattr(p,'reject_custom_shadows'),'custom artifacts must not be available through official caches')
  with tempfile.TemporaryDirectory() as td:
   r=pathlib.Path(td);p.reject_custom_shadows([r],['Local.Module']);(r/'Local').mkdir();(r/'Local/Module.olean').write_bytes(b'old')
   with self.assertRaises(ValueError):p.reject_custom_shadows([r],['Local.Module'])
 def test_executable_fixture_readback_is_exact(self):
  self.assertTrue(hasattr(p,'check_fixture_stdout'),'successful elaboration alone must not certify fixture output')
  self.assertEqual(p.check_fixture_stdout('1\n0\n',['1','0']),['1','0'])
  for text in ['1\n1\n','1\n0\nwarning: x','1\n']:
   with self.assertRaises(ValueError):p.check_fixture_stdout(text,['1','0'])

class PrimedDeclarationTests(unittest.TestCase):
 def test_lean_identifiers_with_apostrophes_are_audited_exactly(self):
  name="P02A2.PRCompiler.comp'_correct";text=name+" : True\n'"+name+"' depends on axioms: [propext]\n"
  self.assertEqual(p.parse_audit(text,[name]),{name:['propext']})
  with self.assertRaises(ValueError):p.parse_audit(text,[name.replace("'",'')])

class RecordedReplayTests(unittest.TestCase):
 def test_recorded_replay_binds_source_logs_and_exact_targets(self):
  self.assertTrue(hasattr(p,'verify_replay_evidence'),'retained logs must bind exact current sources and targets')
  with tempfile.TemporaryDirectory() as td:
   r=pathlib.Path(td);(r/'sources/s').mkdir(parents=True);source=r/'sources/s/A.lean';source.write_text('namespace T\ntheorem a : True := True.intro\nend T\n');logs=r/'logs/s';logs.mkdir(parents=True)
   rows=[]
   for name,text in [('A',''),('PortableAudit_t',"T.a : True\n'T.a' does not depend on any axioms\n")]:
    (logs/(name+'.stdout')).write_text(text);(logs/(name+'.stderr')).write_text('');rows.append({'module':name,'exit_code':0,'olean_sha256':'0'*64,'stdout_sha256':p.sha(logs/(name+'.stdout')),'stderr_sha256':p.sha(logs/(name+'.stderr'))})
   rec={'status':'PASS','manifest_sha256':'f'*64,'suites':[{'id':'s','status':'FRESH_CUSTOM_SOURCE_BUILD_AND_TYPE_AXIOM_READBACK_PASS','sources':{'A.lean':{'sha256':p.sha(source),'bytes':source.stat().st_size}},'modules':rows,'claim_sets':{'t':{'target_count':1,'declarations':{'T.a':[]}}}}]}
   p.write_json(r/'result.json',rec);entries=[{'receipt':'result.json','sha256':p.sha(r/'result.json'),'log_root':'logs','input_snapshot_manifest_sha256':'f'*64}];suites=[{'id':'s','source_root':'sources/s','module_order':['A'],'targets':{'t':['T.a']}}]
   self.assertEqual(p.verify_replay_evidence(r,entries,suites)['status'],'RECORDED_REPLAY_SOURCE_LOG_TARGET_BINDINGS_PASS')
   source.write_text('changed')
   with self.assertRaises(ValueError):p.verify_replay_evidence(r,entries,suites)

class ReplayMetadataTests(unittest.TestCase):
 def test_snapshot_and_fixture_metadata_cannot_drift(self):
  with tempfile.TemporaryDirectory() as td:
   r=pathlib.Path(td);(r/'sources/s').mkdir(parents=True);f=r/'sources/s/A.lean';f.write_text('theorem a : True := True.intro\n');logs=r/'logs/s';logs.mkdir(parents=True);rows=[]
   for name,text in [('A','1\n'),('PortableAudit_t',"a : True\n'a' does not depend on any axioms\n")]:
    (logs/(name+'.stdout')).write_text(text);(logs/(name+'.stderr')).write_text('');rows.append({'module':name,'exit_code':0,'olean_sha256':'0'*64,'stdout_sha256':p.sha(logs/(name+'.stdout')),'stderr_sha256':p.sha(logs/(name+'.stderr'))})
   rows[0]['fixture_output']=['1'];rec={'status':'PASS','manifest_sha256':'f'*64,'suites':[{'id':'s','status':'FRESH_CUSTOM_SOURCE_BUILD_AND_TYPE_AXIOM_READBACK_PASS','sources':{'A.lean':{'sha256':p.sha(f),'bytes':f.stat().st_size}},'modules':rows,'claim_sets':{'t':{'target_count':1,'declarations':{'a':[]}}}}]};p.write_json(r/'result.json',rec)
   entries=[{'receipt':'result.json','sha256':p.sha(r/'result.json'),'log_root':'logs','input_snapshot_manifest_sha256':'f'*64}];suites=[{'id':'s','source_root':'sources/s','module_order':['A'],'targets':{'t':['a']},'stdout_expectations':{'A':['1']}}]
   p.verify_replay_evidence(r,entries,suites)
   with self.subTest('input snapshot'):
    entries[0]['input_snapshot_manifest_sha256']='a'*64
    with self.assertRaises(ValueError):p.verify_replay_evidence(r,entries,suites)
   entries[0]['input_snapshot_manifest_sha256']='f'*64
   with self.subTest('fixture output'):
    suites[0]['stdout_expectations']['A']=['0']
    with self.assertRaises(ValueError):p.verify_replay_evidence(r,entries,suites)
   suites[0]['stdout_expectations']['A']=['1'];rows[0]['fixture_output']=['0'];p.write_json(r/'result.json',rec);entries[0]['sha256']=p.sha(r/'result.json')
   with self.subTest('recorded fixture metadata'):
    with self.assertRaises(ValueError):p.verify_replay_evidence(r,entries,suites)

class CommitIdentityTests(unittest.TestCase):
 def test_canonical_commit_object_binds_named_tree(self):
  self.assertTrue(hasattr(p,'verify_commit_identity'),'canonical commit-to-tree link must be independently hashable')
  tree='1'*40;raw=('tree '+tree+'\n\nSnapshot\n').encode();commit=hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  self.assertTrue(p.verify_commit_identity(raw,commit,tree))
  with self.assertRaises(ValueError):p.verify_commit_identity(raw+b'x',commit,tree)
  with self.assertRaises(ValueError):p.verify_commit_identity(raw,commit,'2'*40)

if __name__=='__main__':unittest.main()
