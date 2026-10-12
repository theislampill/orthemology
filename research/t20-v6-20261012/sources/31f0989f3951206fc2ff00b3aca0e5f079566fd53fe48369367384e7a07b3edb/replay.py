from pathlib import Path
import ast,hashlib,json,subprocess,sys,tempfile,shutil
R=Path(__file__).resolve().parent;P=R/'payload';A='literal-shift-implementation-audit-20261011';V='literal-shift-independent-review-20261011'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,m):
 if not c:raise RuntimeError(m)
def verify():
 for x in json.loads((R/'MANIFEST.json').read_text()):
  p=R/x['path'];require(p.is_file(),'Missing file '+x['path']);require(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'Manifest mismatch '+x['path'])
 for x in json.loads((R/'PRESERVATION_MAP.json').read_text()):require(sha(R/x['preserved'])==x['sha256'],'Original mismatch '+x['source'])
 for path,h in json.loads((P/A/'BINDINGS.json').read_text())['files'].items():require(sha(P/path)==h,'Author binding mismatch '+path)
 for path,h in json.loads((P/V/'MANIFEST.json').read_text())['files'].items():require(sha(P/V/path)==h,'Review manifest mismatch '+path)
 for path,h in json.loads((P/A/'historical-normal-only/BINDINGS.json').read_text())['files'].items():
  p=P/path
  if path.startswith(A+'/') and Path(path).name in ['check_literal.py','REPORT.md','RESULTS.json','replay.log']:p=P/A/'historical-normal-only'/Path(path).name
  require(sha(p)==h,'Historical binding mismatch '+path)
 basic=P/'basic-recognition-live-input-check-20261011'
 for x in json.loads((basic/'INPUT_BINDINGS.json').read_text())['inputs']:require(sha(basic/x['copy_path'])==x['sha256'],'Basic-recognition snapshot mismatch')
 require(sha(P/A/'check_literal.py')==sha(P/V/'check_literal.py'),'Author/reviewer harness copies differ')
 require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((P/A/'check_literal.py').read_text()))),'Current harness has stripped asserts')
def replay():
 verify();runs=[]
 with tempfile.TemporaryDirectory(prefix='literal-audit-') as tmp:
  w=Path(tmp)/'payload';shutil.copytree(P,w);script=w/A/'check_literal.py'
  for opt in [False,True]:
   cmd=[sys.executable]+(['-O'] if opt else [])+[str(script)]
   p=subprocess.run(cmd,cwd=w,text=True,capture_output=True);require(p.returncode==0,'Audit failed '+p.stderr)
   result=json.loads(p.stdout);require(result==json.loads((P/A/'RESULTS.json').read_text()),'Results differ from frozen author/reviewer evidence')
   require(sum(result['counts'].values())==97456 and len(result['negative_controls'])==5,'Wrong case/control count')
   runs.append({'optimized':opt,'status':'PASS','result':result,'identical_author_and_reviewer_harness_hash':sha(script)})
   p=subprocess.run(cmd+['--false-check'],cwd=w,text=True,capture_output=True);require(p.returncode!=0 and 'deliberate false-check control' in p.stderr,'Explicit false guard failed to reject')
   runs.append({'optimized':opt,'test':'explicit false guard','returncode':p.returncode,'last_error':p.stderr.splitlines()[-1]})
  test=w/'user-checkpoints/extracted/P02/tests/test_new_research.py'
  p=subprocess.run([sys.executable,'-B',str(test)],cwd=w,text=True,capture_output=True);require(p.returncode==0,'Inherited tests failed '+p.stdout+p.stderr)
  runs.append({'test':'inherited test_new_research.py','returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 verify();print(json.dumps({'status':'PASS','python':sys.version,'runs':runs,'review_replay_scope':'The author and reviewer harnesses are byte-identical; the common current source is replayed once per mode. This is not a new independent implementation.','compiler_repaired':False,'universal_or_infinite_law_proof':False},indent=2))
if __name__=='__main__':
 if '--verify-only' in sys.argv:verify();print('PASS: original identities, current/historical bindings, basic snapshots and explicit guards')
 else:replay()
