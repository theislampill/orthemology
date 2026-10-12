#!/usr/bin/env python3
"""Replay only the five declared tenth-checkpoint controls in disposable copies."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,importlib.metadata,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():return {p.relative_to(ROOT).as_posix():sha(p) for p in ROOT.rglob('*') if p.is_file()}
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
out=Path(args.output).resolve()
assert out!=ROOT and ROOT not in out.parents,'Outputs must stay outside frozen inputs'
out.mkdir(parents=True,exist_ok=True)
assert not (out/'REPLAY_RECEIPT.json').exists(),'Refuse to overwrite an existing receipt'
plan=json.loads((ROOT/'PACKING/CONTROL_PLAN.json').read_text());before=snapshot();checks=[]
with tempfile.TemporaryDirectory(prefix='t20-tenth-python-') as tmp:
    work=Path(tmp)/'copy';shutil.copytree(ROOT,work)
    for cmd in plan['commands']:
        assert sha(ROOT/cmd['script'])==cmd['script_sha256']
        for rel in cmd['generated_outputs']:(work/rel).unlink(missing_ok=True)
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
        try:
            proc=subprocess.run([sys.executable,str(work/cmd['script'])],cwd=work/cmd['cwd'],env=env,capture_output=True,timeout=900)
            stdout,stderr,code=proc.stdout,proc.stderr,proc.returncode
        except subprocess.TimeoutExpired as exc:stdout,stderr,code=exc.stdout or b'',exc.stderr or b'',124
        (out/(cmd['id']+'.stdout.log')).write_bytes(stdout)
        (out/(cmd['id']+'.stderr.log')).write_bytes(stderr)
        row={'id':cmd['id'],'script':cmd['script'],'script_sha256':cmd['script_sha256'],'exit_code':code,'generated_outputs':[]}
        for rel in cmd['generated_outputs']:
            actual,expected=work/rel,ROOT/rel
            row['generated_outputs'].append({'path':rel,'expected_sha256':sha(expected),'actual_sha256':sha(actual) if actual.is_file() else None,'byte_match':actual.is_file() and actual.read_bytes()==expected.read_bytes()})
        if cmd.get('stdout_target'):
            expected=ROOT/cmd['stdout_target']
            row.update({'stdout_target':cmd['stdout_target'],'expected_sha256':sha(expected),'actual_stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stdout_byte_match':stdout==expected.read_bytes()})
        row['status']='PASS' if code==0 and all(r['byte_match'] for r in row['generated_outputs']) and row.get('stdout_byte_match',True) else 'FAIL'
        checks.append(row);print(cmd['id'],row['status'],flush=True)
unchanged=before==snapshot()
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if unchanged and all(r['status']=='PASS' for r in checks) else 'FAIL','classification':'FRESH_PACKAGING_REPLAY_NOT_NEW_RESEARCH_OR_ACCEPTANCE','python':sys.version,'dependencies':{x:importlib.metadata.version(x) for x in ['numpy','mpmath']},'checks':checks,'frozen_checkpoint_bytes_unchanged':unchanged,'comparison':'Exact bytes; no ignored fields','proof_by_finite_scan':False,'empirical_validation':False,'new_kernel_verification':False,'research_duration_credit_seconds':0}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert receipt['status']=='PASS',receipt
