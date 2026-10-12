#!/usr/bin/env python3
"""Replay declared ninth-checkpoint controls in disposable copies, never frozen inputs."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,importlib.metadata
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def equivalent(actual,expected,ignored):
 if not ignored:return actual==expected
 a=json.loads(actual);b=json.loads(expected)
 for key in ignored:a.pop(key,None);b.pop(key,None)
 return a==b
def snapshot():return {p.relative_to(ROOT).as_posix():sha(p) for p in ROOT.rglob('*') if p.is_file()}
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
out=Path(a.output).resolve();assert out!=ROOT and ROOT not in out.parents,'Output must be outside the frozen checkpoint'
out.mkdir(parents=True,exist_ok=True)
assert not (out/'REPLAY_RECEIPT.json').exists(),'Refuse to overwrite an existing receipt'
plan=json.loads((ROOT/'PACKING/CONTROL_PLAN.json').read_text());before=snapshot();checks=[]
with tempfile.TemporaryDirectory(prefix='t20-ninth-python-') as tmp:
 work=Path(tmp)/'copy';shutil.copytree(ROOT,work)
 for cmd in plan['commands']:
  assert sha(ROOT/cmd['script'])==cmd['script_sha256']
  for rel in cmd['generated_outputs']:(work/rel).unlink(missing_ok=True)
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
  try:
   run=subprocess.run([sys.executable,str(work/cmd['script'])],cwd=work/cmd['cwd'],env=env,capture_output=True,timeout=900)
   stdout,stderr,code=run.stdout,run.stderr,run.returncode
  except subprocess.TimeoutExpired as e:stdout,stderr,code=e.stdout or b'',e.stderr or b'',124
  (out/(cmd['id']+'.stdout.log')).write_bytes(stdout);(out/(cmd['id']+'.stderr.log')).write_bytes(stderr)
  row={'id':cmd['id'],'script':cmd['script'],'script_sha256':cmd['script_sha256'],'exit_code':code,'generated_outputs':[]}
  for rel in cmd['generated_outputs']:
   actual,expected=work/rel,ROOT/rel
   row['generated_outputs'].append({'path':rel,'expected_sha256':sha(expected),'actual_sha256':sha(actual) if actual.is_file() else None,'byte_match':actual.is_file() and actual.read_bytes()==expected.read_bytes(),'declared_comparison_match':actual.is_file() and equivalent(actual.read_bytes(),expected.read_bytes(),cmd.get('json_ignore_keys',[])),'ignored_json_timestamp_keys':cmd.get('json_ignore_keys',[])})
  if cmd.get('stdout_target'):
   expected=ROOT/cmd['stdout_target'];row.update({'stdout_target':cmd['stdout_target'],'expected_sha256':sha(expected),'actual_stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stdout_byte_match':stdout==expected.read_bytes(),'stdout_declared_comparison_match':equivalent(stdout,expected.read_bytes(),cmd.get('json_ignore_keys',[])),'ignored_json_timestamp_keys':cmd.get('json_ignore_keys',[])})
  row['status']='PASS' if code==0 and all(r['declared_comparison_match'] for r in row['generated_outputs']) and row.get('stdout_declared_comparison_match',True) else 'FAIL'
  checks.append(row);print(cmd['id'],row['status'],flush=True)
unchanged=before==snapshot()
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if unchanged and all(r['status']=='PASS' for r in checks) else 'FAIL','classification':'FRESH_PACKAGING_REPLAY_NOT_NEW_RESEARCH_OR_ACCEPTANCE','python':sys.version,'dependencies':{name:importlib.metadata.version(name) for name in ['mpmath','sympy','numpy','scipy']},'checks':checks,'frozen_checkpoint_bytes_unchanged':unchanged,'proof_by_finite_scan':False,'empirical_validation':False,'whole_project_kernel_verification':False,'research_duration_credit_seconds':0}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert receipt['status']=='PASS',receipt
