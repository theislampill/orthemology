#!/usr/bin/env python3
"""Additive portable adapter; never edits or deletes original bindings or scripts."""
import hashlib,json,os,runpy,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUTHOR='cumulative-credal-audit-coupling-20261011'
REVIEW='cumulative-revision-coupling-independent-review-20261011'
CONTROLS='cumulative-credal-root-controls-20261011'
GA='credal-geometric-transport-20261011'
GR='credal-geometric-independent-review-20261011'
GC='credal-geometric-root-controls-20261011'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
 for x in json.loads((ROOT/'DELIVERY_MANIFEST.json').read_text()):
  p=ROOT/x['path']
  if not p.is_file():raise RuntimeError('Missing archived file: '+x['path'])
  if p.stat().st_size!=x['bytes'] or digest(p)!=x['sha256']:raise RuntimeError('Archive mismatch: '+x['path'])
 for x in json.loads((ROOT/'PRESERVATION_MAP.json').read_text()):
  if digest(ROOT/x['preserved'])!=x['sha256']:raise RuntimeError('Original preservation mismatch: '+x['source'])
 for x in json.loads((ROOT/'INHERITED_INPUTS.json').read_text()):
  p=ROOT/x['preserved']
  if not p.is_file():raise RuntimeError('Missing inherited input: '+x['path'])
  if digest(p)!=x['sha256']:raise RuntimeError('Inherited input mismatch: '+x['path'])
 for x in json.loads((ROOT/'payload'/REVIEW/'REVIEW_BINDINGS.json').read_text())['reviewed_files']:
  if digest(ROOT/'payload'/x['path'])!=x['sha256']:raise RuntimeError('Final reviewer binding mismatch: '+x['path'])
 for x in json.loads((ROOT/'payload'/AUTHOR/'AUTHOR_SNAPSHOT.json').read_text()):
  if digest(ROOT/'payload'/AUTHOR/x['file'])!=x['sha256']:raise RuntimeError('Author snapshot mismatch: '+x['file'])
 for name,sha in json.loads((ROOT/'payload'/CONTROLS/'MANIFEST.json').read_text()).items():
  if digest(ROOT/'payload'/CONTROLS/name)!=sha:raise RuntimeError('Root manifest mismatch: '+name)
 for name,sha in json.loads((ROOT/'payload'/GR/'REVIEW_BINDINGS.json').read_text()).items():
  target=ROOT/'payload'/GA/('pre-wording-clarification/'+name if name in ['REPORT.md','AUTHOR_FREEZE.json'] else name)
  if digest(target)!=sha:raise RuntimeError('Historical geometric reviewer binding mismatch: '+name)
 for name,sha in json.loads((ROOT/'payload'/GR/'WORDING_BINDINGS.json').read_text()).items():
  if digest(ROOT/'payload'/GA/name)!=sha:raise RuntimeError('Geometric wording binding mismatch: '+name)
 for x in json.loads((ROOT/'payload'/GA/'AUTHOR_FREEZE.json').read_text())['files']:
  if digest(ROOT/'payload'/GA/x['path'])!=x['sha256']:raise RuntimeError('Geometric author freeze mismatch: '+x['path'])
 for name,sha in json.loads((ROOT/'payload'/GC/'MANIFEST.json').read_text()).items():
  if digest(ROOT/'payload'/GC/name)!=sha:raise RuntimeError('Geometric root binding mismatch: '+name)
 for x in json.loads((ROOT/'payload'/GA/'REPAIR_FREEZE.json').read_text())['files']:
  if digest(ROOT/'payload'/GA/x['path'])!=x['sha256']:raise RuntimeError('Repair author freeze mismatch: '+x['path'])
 for name,sha in json.loads((ROOT/'payload'/GR/'REPAIR_REVIEW_BINDINGS.json').read_text()).items():
  if digest(ROOT/'payload'/GA/name)!=sha:raise RuntimeError('Repair reviewer binding mismatch: '+name)
def child(script,mode):
 # Exact lookup only. All inherited bytes are archive-owned, even if the old
 # workspace happens to exist. No missing binding is removed or bypassed.
 entries=json.loads((ROOT/'INHERITED_INPUTS.json').read_text())
 mapping={x['path']:ROOT/x['preserved'] for x in entries}
 # Also allow the same inherited path in workspace-relative spelling.
 for x in entries:
  mapping[x['preserved'].split('/',1)[1]]=ROOT/x['preserved']
  if not Path(x['path']).is_absolute():mapping[str(Path(script).resolve().parent.parent/x['path'])]=ROOT/x['preserved']
 original=Path.read_bytes
 def mapped(path):
  key=str(path)
  if key in mapping:return original(mapping[key])
  return original(path)
 Path.read_bytes=mapped
 if mode=='preserve':
  from assertion_preserving_runner import compile_preserving
  p=Path(script).resolve()
  exec(compile_preserving(p.read_text(),str(p)),{'__name__':'__main__','__file__':str(p),'__builtins__':__builtins__})
 else:runpy.run_path(script,run_name='__main__')
def run():
 verify(); results=[]
 with tempfile.TemporaryDirectory(prefix='credal-portable-') as tmp:
  work=Path(tmp)
  for label,name,script,optimized,preserve in [('author-normal',AUTHOR,'verify.py',False,False),('author-optimized-adapter',AUTHOR,'verify.py',True,True),('review-normal',REVIEW,'check.py',False,False),('review-optimized-adapter',REVIEW,'check.py',True,True),('root-normal',CONTROLS,'check.py',False,False),('root-optimized',CONTROLS,'check.py',True,False),('geometric-author-normal',GA,'verify.py',False,False),('geometric-author-optimized',GA,'verify.py',True,False),('geometric-review-normal',GR,'independent_controls.py',False,False),('geometric-review-optimized',GR,'independent_controls.py',True,False),('geometric-root-normal',GC,'check.py',False,False),('geometric-root-optimized',GC,'check.py',True,False),('repair-author-normal',GA,'verify_repair.py',False,False),('repair-author-optimized',GA,'verify_repair.py',True,False),('repair-review-normal',GR,'belief_controls.py',False,False),('repair-review-optimized',GR,'belief_controls.py',True,False)]:
   dest=work/label;shutil.copytree(ROOT/'payload'/name,dest)
   cmd=[sys.executable]+(['-O'] if optimized else [])+[str(ROOT/'replay.py'),'--child',str(dest/script),'preserve' if preserve else 'normal']
   proc=subprocess.run(cmd,cwd=dest,text=True,capture_output=True)
   if proc.returncode:raise RuntimeError(label+' failed:\n'+proc.stdout+proc.stderr)
   output_name={'verify.py':'CONTROL_RESULTS.json' if name==AUTHOR else 'CHECKS.json','check.py':'CONTROL_RESULTS.json' if name==REVIEW else None,'independent_controls.py':'INDEPENDENT_CONTROLS.json','verify_repair.py':'REPAIR_CHECKS.json','belief_controls.py':'BELIEF_CONTROLS.json'}[script]
   if output_name and digest(dest/output_name)!=digest(ROOT/'payload'/name/output_name):raise RuntimeError(label+' regenerated result hash mismatch')
   results.append({'label':label,'status':'PASS','stdout':proc.stdout,'stderr':proc.stderr,'regenerated_result':output_name,'regenerated_result_matches':True if output_name else None})
  for opt in [False,True]:
   cmd=[sys.executable]+(['-O'] if opt else [])+[str(ROOT/'assertion_preserving_runner.py'),'--self-test']
   proc=subprocess.run(cmd,text=True,capture_output=True)
   if proc.returncode:raise RuntimeError('Assertion sentinel failed')
   results.append({'label':'adapter-sentinel-'+('optimized' if opt else 'normal'),'status':'PASS','stdout':proc.stdout})
 verify()
 import sympy
 print(json.dumps({'status':'PASS','python':sys.version,'sympy':sympy.__version__,'inherited_bindings':len(json.loads((ROOT/'INHERITED_INPUTS.json').read_text())),'original_packets':6,'raw_optimized_author_or_reviewer_credit':False,'checks':results},indent=2))
if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='--child':child(sys.argv[2],sys.argv[3])
 elif len(sys.argv)>1 and sys.argv[1]=='--verify-only':verify();print('PASS: manifest, preservation and inherited input hashes')
 else:run()
