#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent
def require(v,msg):
 if not v:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def refresh(p):
 rows=[{'path':str(f.relative_to(p)),'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(p.rglob('*')) if f.is_file() and f != p/'MANIFEST.json']
 dump(p/'MANIFEST.json',{'schema':'partial-law-evidence-v1','files':rows})
 return sha(p/'MANIFEST.json')
def main():
 require(sys.flags.optimize==0,'optimized guard driver refused')
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--manifest-sha256',required=True);args=ap.parse_args()
 out=Path(args.out).resolve();require(not out.exists(),'guard output exists');require(not out.is_relative_to(ROOT) and not ROOT.is_relative_to(out),'guard output overlaps packet');out.mkdir(parents=True)
 results=[]
 def run(name,packet=ROOT,digest=args.manifest_sha256,extra=None,flags=None,env=None,verify=True,omit_digest=False,output=None):
  target=output or out/(name+'-output')
  cmd=[sys.executable,*list(flags or []),str(packet/'replay.py')]
  if not omit_digest:cmd+=['--manifest-sha256',digest]
  cmd+=['--out',str(target)]
  if verify:cmd+=['--verify-only']
  if extra:cmd+=extra
  proc=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,text=True)
  log=out/(name+'.log');log.write_text(proc.stdout)
  require(proc.returncode!=0,name+' unexpectedly passed')
  require(not (target/'runs').exists() and not (target/'REPLAY_RECEIPT.json').exists(),name+' executed controls')
  results.append({'name':name,'exit_code':proc.returncode,'rejected':True,'no_controls_executed':True,'log':log.name,'log_sha256':sha(log)})
 def clone(name):
  p=out/(name+'-packet');shutil.copytree(ROOT,p);return p
 run('missing-manifest-argument',omit_digest=True)
 run('wrong-manifest-digest',digest='0'*64)
 p=clone('tampered-file');q=p/'evidence/partial-cumulative-law-persistence-20261010/RESULT.md';q.write_bytes(q.read_bytes()+b'\n');run('tampered-file',packet=p)
 p=clone('missing-file');(p/'SOURCE_ROOT_BINDINGS.json').unlink();run('missing-file',packet=p)
 p=clone('unexpected-file');(p/'unexpected.txt').write_text('not in manifest');run('unexpected-file',packet=p)
 p=clone('unexpected-nested-manifest');(p/'nested').mkdir();(p/'nested/MANIFEST.json').write_text('{}');run('unexpected-nested-manifest',packet=p)
 p=clone('symlink-file');(p/'unexpected-link').symlink_to(p/'README.md');run('symlink-file',packet=p)
 target=out/'existing-output';target.mkdir();(target/'keep').write_text('unchanged');run('reused-output',output=target,verify=False);require((target/'keep').read_text()=='unchanged','existing output mutated')
 run('inside-packet-output',output=ROOT/'forbidden-output',verify=False)
 run('optimized-python',flags=['-O'])
 env=dict(os.environ);env['PYTHONOPTIMIZE']='1';run('optimized-env',env=env)
 run('missing-sympy-runtime',flags=['-S'],verify=False)
 for name,field,value in [('false-scalar-boolean','match',False),('wrong-scalar-digest','expected_sha256','0'*64)]:
  p=clone(name);f=p/'INHERITED_DEPENDENCIES.json';data=json.loads(f.read_text());data['scalar_object_receipt_bindings']['bindings'][0][field]=value;dump(f,data)
  run(name,packet=p,digest=refresh(p))
 p=clone('closure-escalation');f=p/'ACCEPTANCE_BINDINGS.json';data=json.loads(f.read_text());data['closure']=True;dump(f,data);run('closure-escalation',packet=p,digest=refresh(p))
 if (ROOT/'ADDENDA_BINDINGS.json').exists():
  p=clone('addendum-kernel-escalation');f=p/'ADDENDA_BINDINGS.json';data=json.loads(f.read_text());data['analytic_kernel_proof']=True;dump(f,data);run('addendum-kernel-escalation',packet=p,digest=refresh(p))
  p=clone('historical-preimage-substitution');f=p/'ADDENDA_BINDINGS.json';data=json.loads(f.read_text());target=next(v for v in data['programs'] if v.get('overrides'));target['overrides'][0]['packet']='evidence/valid-initial-escape-effectivity-20261010/RESULT.md';dump(f,data);run('historical-preimage-substitution',packet=p,digest=refresh(p))
  p=clone('false-recovery-receipt');f=p/'evidence/valid-initial-escape-effectivity-independent-review-20261010/root-replay-observation/RECOVERY_RECEIPT.json';data=json.loads(f.read_text());data['all_original_manifest_entries_restored_and_verified']=False;dump(f,data);run('false-recovery-receipt',packet=p,digest=refresh(p))
 # Verify the guard driver itself refuses optimization before constructing output.
 extra=out/'optimized-driver-output';proc=subprocess.run([sys.executable,'-O',str(ROOT/'test_guards.py'),'--out',str(extra),'--manifest-sha256',args.manifest_sha256],capture_output=True,text=True)
 require(proc.returncode!=0 and not extra.exists(),'optimized guard driver bypass');log=out/'optimized-guard-driver.log';log.write_text(proc.stdout+proc.stderr);results.append({'name':'optimized-guard-driver','exit_code':proc.returncode,'rejected':True,'no_controls_executed':True,'log':log.name,'log_sha256':sha(log)})
 dump(out/'GUARD_RESULTS.json',{'status':'PASS_FAIL_CLOSED_GUARDS','count':len(results),'tests':results,'scope':'Packaging guard mutations; these are not independent mathematical counterexamples.'})
 print(str(len(results))+' fail-closed guard cases passed.')
if __name__=='__main__':
 try:main()
 except Exception as e:print('REFUSED: '+str(e),file=sys.stderr);sys.exit(1)
