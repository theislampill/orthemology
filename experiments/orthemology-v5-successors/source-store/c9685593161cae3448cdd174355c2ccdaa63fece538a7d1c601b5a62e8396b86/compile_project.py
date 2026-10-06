#!/usr/bin/env python3
"""New recovered-v1 integration wrapper: source copy compilation, never old objects."""
from pathlib import Path
import argparse,json,hashlib,os,re,subprocess,time

if not __debug__:
 raise SystemExit("OPTIMIZED_PYTHON_UNSUPPORTED: disable -O, -OO and PYTHONOPTIMIZE")

def sha(p):
 digest=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):digest.update(chunk)
 return digest.hexdigest()
def compile_project(package, output, lean, dependency_roots):
 package=Path(package).resolve();output=Path(output).resolve();lean=Path(lean).resolve()
 assert not output.exists(),'Fresh project output must not exist'
 assert package not in output.parents and package!=output,'Outputs must stay outside distributed source'
 locks=json.loads((package/'MATHEMATICAL_SOURCE_LOCK.json').read_text());sources={r['module']:package/r['path'] for r in locks}
 for r in locks:assert sha(package/r['path'])==r['sha256'],'Mathematical source mismatch: '+r['module']
 sources['verification.KernelAudit']=package/'lean/verification/KernelAudit.lean'
 output.mkdir(parents=True);(output/'project').mkdir();(output/'inherited/verification').mkdir(parents=True);(output/'logs').mkdir()
 env=dict(os.environ);env['LEAN_NUM_THREADS']='1';env['LEAN_PATH']=':'.join(map(str,[output/'project',output/'inherited',*map(Path,dependency_roots)]))
 env['PYTHONDONTWRITEBYTECODE']='1';done=set();active=set();records=[]
 def build(m):
  if m in done:return
  assert m not in active,'Import cycle';active.add(m)
  for imp in re.findall(r'^import\s+([\w.]+)',sources[m].read_text(),re.M):
   if imp in sources:build(imp)
  obj=(output/'inherited' if m.startswith('verification.') else output/'project')/(m.replace('.','/')+'.olean');obj.parent.mkdir(parents=True,exist_ok=True)
  begin=time.monotonic();run=subprocess.run([str(lean),'--root='+str(package/'lean'),'-o',str(obj),str(sources[m])],cwd=output,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
  log=output/'logs'/(m+'.log');log.write_text(run.stdout)
  row={'module':m,'exit':run.returncode,'source_sha256':sha(sources[m]),'seconds':round(time.monotonic()-begin,3),'log_sha256':sha(log),'new_object_sha256':sha(obj) if obj.exists() else None};records.append(row);(output/'PROGRESS.json').write_text(json.dumps(records,indent=2)+'\n')
  if run.returncode:print(run.stdout,flush=True);raise RuntimeError('Fresh source compilation failed: '+m)
  print('FRESH_COMPILE_PASS '+m,flush=True);done.add(m);active.remove(m)
 for module in sources:build(module)
 for row in locks:assert sha(package/row['path'])==row['sha256'],'Source changed during build'
 receipt={'status':'PASS','candidate':'new recovered-v1 integration','fresh_mathematical_modules':len(locks),'fresh_inherited_audit_support':1,'project_object_reuse':False,'source_locks_sha256':sha(package/'MATHEMATICAL_SOURCE_LOCK.json'),'lean_binary_sha256':sha(lean),'dependency_source_or_cold_build':False,'dependency_objects':'newly reacquired official pinned cache objects from post-reset recovery','records':records}
 (output/'PROJECT_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('RECOVERED_PROJECT_SOURCE_BUILD_PASS',len(locks),flush=True)
 return receipt
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--package',type=Path,required=True);a.add_argument('--output',type=Path,required=True);a.add_argument('--lean',type=Path,required=True);a.add_argument('--dependencies',type=Path,required=True);args=a.parse_args()
 names=['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib']
 compile_project(args.package,args.output,args.lean,[args.dependencies.resolve()/n/'.lake/build/lib/lean' for n in names])
