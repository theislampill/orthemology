#!/usr/bin/env python3
"""Replay only the three actual portable controls on disposable copies; no path rewriting."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,importlib.metadata,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(p):return {v.relative_to(p).as_posix():sha(v) for v in p.rglob('*') if v.is_file()}
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve()
assert out!=ROOT and ROOT not in out.parents,'Outputs must stay outside frozen inputs'
out.mkdir(parents=True,exist_ok=True);assert not (out/'REPLAY_RECEIPT.json').exists()
plan=json.loads((ROOT/'PACKING/CONTROL_PLAN.json').read_text());before=snapshot(ROOT);checks=[]
with tempfile.TemporaryDirectory(prefix='t20-twelfth-python-') as tmp:
 work=Path(tmp)/'copy';shutil.copytree(ROOT,work)
 for cmd in plan['commands']:
  assert sha(ROOT/cmd['script'])==cmd['script_sha256']
  for rel in cmd['generated_outputs']:(work/rel).unlink(missing_ok=True)
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
  try:
   proc=subprocess.run([sys.executable,str(work/cmd['script'])],cwd=work/cmd['cwd'],env=env,capture_output=True,timeout=1800);stdout,stderr,code=proc.stdout,proc.stderr,proc.returncode
  except subprocess.TimeoutExpired as exc:stdout,stderr,code=exc.stdout or b'',exc.stderr or b'',124
  (out/(cmd['id']+'.stdout.log')).write_bytes(stdout);(out/(cmd['id']+'.stderr.log')).write_bytes(stderr)
  row={'id':cmd['id'],'script':cmd['script'],'script_sha256':cmd['script_sha256'],'exit_code':code,'generated_outputs':[]}
  for rel in cmd['generated_outputs']:
   actual,expected=work/rel,ROOT/rel;row['generated_outputs'].append({'path':rel,'expected_sha256':sha(expected),'actual_sha256':sha(actual) if actual.is_file() else None,'byte_match':actual.is_file() and actual.read_bytes()==expected.read_bytes()})
  row['status']='PASS' if code==0 and all(r['byte_match'] for r in row['generated_outputs']) else 'FAIL';checks.append(row);print(cmd['id'],row['status'],flush=True)
  if row['status']!='PASS':break
unchanged=before==snapshot(ROOT)
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if unchanged and len(checks)==len(plan['commands']) and all(r['status']=='PASS' for r in checks) else 'FAIL','classification':'FRESH_PACKAGING_REPLAY_NOT_NEW_RESEARCH_OR_ACCEPTANCE','python':sys.version,'dependencies':{x:importlib.metadata.version(x) for x in ['mpmath','sympy']},'checks':checks,'preserved_programs_not_replayed':plan['preserved_not_replayed'],'temporary_external_dependencies':[],'frozen_checkpoint_bytes_unchanged':unchanged,'comparison':'Every generated scientific-output byte compared; no ignored timestamp or scientific fields.','source_body_rechecks':False,'modal_diagnostic_replay':False,'empirical_validation':False,'new_kernel_verification':False,'research_duration_credit_seconds':0}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');assert receipt['status']=='PASS',receipt
