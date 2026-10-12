#!/usr/bin/env python3
"""Run only the declared seventh-checkpoint controls in disposable scratch."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():return {p.relative_to(ROOT).as_posix():sha(p) for p in ROOT.rglob('*') if p.is_file()}
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
out=Path(args.output).resolve();assert out!=ROOT and ROOT not in out.parents,'Use an output directory outside the checkpoint'
out.mkdir(parents=True,exist_ok=True)
plan=json.loads((ROOT/'PACKING/CONTROL_PLAN.json').read_text());before=snapshot();checks=[]
with tempfile.TemporaryDirectory(prefix='t20-seventh-controls-') as temp:
 work=Path(temp)/'copy';shutil.copytree(ROOT,work)
 for cmd in plan['commands']:
  assert sha(ROOT/cmd['script'])==cmd['script_sha256']
  for rel in cmd['generated_outputs']:(work/rel).unlink(missing_ok=True)
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
  env.pop('PRIOR_BINDING_BASE',None)
  try:
   proc=subprocess.run([sys.executable,cmd['script']],cwd=work,env=env,capture_output=True,timeout=900)
   stdout,stderr,code=proc.stdout,proc.stderr,proc.returncode
  except subprocess.TimeoutExpired as e:stdout,stderr,code=e.stdout or b'',e.stderr or b'',124
  (out/(cmd['id']+'.stdout.log')).write_bytes(stdout);(out/(cmd['id']+'.stderr.log')).write_bytes(stderr)
  row={'id':cmd['id'],'command':['python3',cmd['script']],'script_sha256':cmd['script_sha256'],'exit_code':code,'generated_outputs':[]}
  for rel in cmd['generated_outputs']:
   actual,expected=work/rel,ROOT/rel
   row['generated_outputs'].append({'path':rel,'expected_sha256':sha(expected),'actual_sha256':sha(actual) if actual.is_file() else None,'byte_match':actual.is_file() and actual.read_bytes()==expected.read_bytes()})
  if cmd['stdout_target']:
   expected=ROOT/cmd['stdout_target'];row.update({'stdout_target':cmd['stdout_target'],'expected_stdout_sha256':sha(expected),'actual_stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stdout_byte_match':stdout==expected.read_bytes()})
  row['status']='PASS' if code==0 and all(x['byte_match'] for x in row['generated_outputs']) and row.get('stdout_byte_match',True) else 'FAIL'
  checks.append(row);print(cmd['id'],row['status'],flush=True)
unchanged=before==snapshot()
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'classification':'DELIVERY_ASSURANCE_ONLY_NO_RESEARCH_TIME_OR_OWNER_ACCEPTANCE','python':sys.version,'checks':checks,'checkpoint_bytes_unchanged':unchanged,'no_new_Lean_or_kernel_verification':True,'historical_research_reintegration':False,'whole_proof_machine_verification':False,'empirical_validation':False,'status':'PASS' if unchanged and all(x['status']=='PASS' for x in checks) else 'FAIL'}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert receipt['status']=='PASS',receipt
