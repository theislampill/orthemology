#!/usr/bin/env python3
"""New lane-isolated control/audit orchestration over a bound current source build."""
from pathlib import Path
import argparse,json,os,re,subprocess,sys,time
sys.dont_write_bytecode=True
from package_checks import sha,check_source_locks,coverage_check,constructor_check

def run_controls(package,build,output,lean,dependency_roots):
 package=Path(package).resolve();build=Path(build).resolve();output=Path(output).resolve();lean=Path(lean).resolve()
 assert not output.exists(),'Control output must be new'
 assert output!=package and package not in output.parents,'CONTROL_OUTPUT_INSIDE_SOURCE_REFUSED'
 check_source_locks(package)
 receipt=json.loads((build/'PROJECT_BUILD_RECEIPT.json').read_text());assert receipt['status']=='PASS' and receipt['source_locks_sha256']==sha(package/'MATHEMATICAL_SOURCE_LOCK.json')
 for r in receipt['records']:
  folder='inherited' if r['module'].startswith('verification.') else 'project';p=build/folder/(r['module'].replace('.','/')+'.olean');assert sha(p)==r['new_object_sha256'],'Source-build object changed: '+r['module']
 output.mkdir(parents=True);(output/'logs').mkdir()
 base=[build/'project',build/'inherited',*map(Path,dependency_roots)]
 extras={'inherited':[output/'lanes/inherited'],'unary':[output/'lanes/unary'],'renewal':[output/'lanes/renewal'],'lookahead':[output/'lanes/lookahead',output/'lanes/renewal'],'policy':[output/'lanes/policy'],'integration':[output/'lanes/integration',output/'lanes/unary']}
 records=[]
 def execute(label,p,lane,compiled=None,root=None,negative=None,positive=None,category=None):
  env=dict(os.environ);env['LEAN_PATH']=':'.join(map(str,extras[lane]+base));env['LEAN_NUM_THREADS']='1';env['PYTHONDONTWRITEBYTECODE']='1'
  cmd=[str(lean)]
  if compiled is not None:compiled.parent.mkdir(parents=True,exist_ok=True);cmd+=['--root='+str(root),'-o',str(compiled)]
  cmd.append(str(p));begin=time.monotonic();r=subprocess.run(cmd,cwd=output,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
  log=output/'logs'/(label+'.log');log.write_text(r.stdout)
  if negative is None:ok=r.returncode==0 and 'error:' not in r.stdout and all(re.search(x,r.stdout) for x in positive or [])
  else:
   cleaned=r.stdout
   for regex in negative:cleaned=re.sub(regex,'',cleaned)
   infra=re.search(r'unknown module|unknown constant|unknown identifier|object file.*does not exist|no such file|failed to read file',cleaned,re.I)
   ok=r.returncode!=0 and not infra and all(re.search(x,r.stdout) for x in negative)
  row={'label':label,'path':str(p.relative_to(package)),'lane':lane,'exit':r.returncode,'passed':bool(ok),'expected_rejection_patterns':negative,'expected_success_patterns':positive,'category':category,'seconds':round(time.monotonic()-begin,3),'log_sha256':sha(log)}
  records.append(row);(output/'PROGRESS.json').write_text(json.dumps(records,indent=2)+'\n');print(('CONTROL_PASS ' if ok else 'CONTROL_FAIL ')+label,flush=True)
  if not ok:print(r.stdout,flush=True);raise RuntimeError('Control contract failed: '+label)
 tests=json.loads((package/'CONTROL_MANIFEST.json').read_text())['tests'];supports={(t['lane'],t['module']):t for t in tests if t['role']=='support'};done=set();active=set()
 def support(key):
  if key in done:return
  assert key not in active,'Audit-support cycle';active.add(key);t=supports[key];lane=t['lane'];module=t['module'];p=package/t['path']
  for dep in t['imports']:
   candidates=[(lane,dep)]+([('renewal',dep)] if lane=='lookahead' else [])+[('inherited',dep)]
   for k in candidates:
    if k in supports:support(k);break
  execute('SUPPORT_'+lane+'_'+module,p,lane,compiled=output/'lanes'/lane/(module.replace('.','/')+'.olean'),root=package/'lean' if lane=='inherited' else p.parent,positive=t['expected_patterns'],category=t['category'])
  done.add(key);active.remove(key)
 for k in supports:support(k)
 for i,t in enumerate(tests):
  if t['role']=='support':continue
  execute(str(i)+'_'+t['lane']+'_'+Path(t['path']).stem,package/t['path'],t['lane'],negative=t['expected_patterns'] if t['role']=='negative' else None,positive=t['expected_patterns'] if t['role']=='positive' else None,category=t['category'])
 execute('INTEGRATION_AUDIT_SUPPORT',package/'verification/integration/GlobalProofClosure.lean','integration',compiled=output/'lanes/integration/GlobalProofClosure.olean',root=package/'verification/integration')
 integration_tests=json.loads((package/'INTEGRATION_CONTROL_MANIFEST.json').read_text())['tests']
 for i,t in enumerate(integration_tests):
  assert sha(package/t['path'])==t['sha256'],'New integration control changed'
  execute('INTEGRATION_'+str(i),package/t['path'],'integration',negative=t['expected_patterns'] if t['role']=='negative' else None,positive=t['expected_patterns'] if t['role']=='positive' else None,category=t['category'])
 execute('COMPLETE_PROJECT_INVENTORY',package/'verification/integration/CompleteInventory.lean','integration',positive=['RECOVERED_COMPLETE_PROOF_COVERAGE_PASS'])
 coverage=coverage_check(package,output);constructor=constructor_check(package)
 env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';r=subprocess.run([sys.executable,'-m','unittest','discover','-s','verification','-p','test*.py','-v'],cwd=package/'python-reference',env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (output/'logs/PYTHON_REFERENCE.log').write_text(r.stdout);assert r.returncode==0,r.stdout
 check_source_locks(package)
 result={'status':'PASS','candidate':'new recovered-v1 integration','executed_control_files':len(tests),'new_integration_controls':len(integration_tests),'role_counts':{role:sum(t['role']==role for t in tests) for role in ['support','positive','negative']},'restoration_counts':{status:sum(t.get('recovery_status')==status for t in tests) for status in sorted({t.get('recovery_status','unspecified') for t in tests})},'coverage':coverage,'packaged_constructor_check':constructor,'records':records,'mathematical_build_receipt_sha256':sha(build/'PROJECT_BUILD_RECEIPT.json'),'current_source_build_reused_for_control_stage':True,'historical_pre_reset_objects_used':False,'native_compiler_ffi_verified':False}
 (output/'CONTROL_REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print('RECOVERED_CONTROL_REPLAY_PASS',len(tests),flush=True);return result
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--package',type=Path,default=Path(__file__).resolve().parent);a.add_argument('--build',type=Path,required=True);a.add_argument('--output',type=Path,required=True);a.add_argument('--lean',type=Path,required=True);a.add_argument('--dependencies',type=Path,required=True);x=a.parse_args();names=['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib'];run_controls(x.package,x.build,x.output,x.lean,[x.dependencies.resolve()/n/'.lake/build/lib/lean' for n in names])
