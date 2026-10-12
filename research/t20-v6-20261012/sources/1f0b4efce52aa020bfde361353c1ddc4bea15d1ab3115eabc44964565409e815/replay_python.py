#!/usr/bin/env python3
"""Delivery-assurance replay of unchanged bounded controls in disposable copies."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
P='t20-next-frontier-20261008/'
COMMANDS=[
 ('acquisition',P+'structuring-cause-reply/model/check_acquisition.py',None,P+'structuring-cause-reply/results/acquisition.json'),
 ('calibration-frontier',P+'calibration-design-frontier/exact_controls.py',P+'calibration-design-frontier/results/exact_controls.json',None),
 ('crossed-independent',P+'crossed-code-root-review/independent_controls.py',None,P+'crossed-code-root-review/results/EXACT_CONTROLS.json'),
 ('crossed-incorporation',P+'crossed-code-root-review/frontier_incorporation_controls.py',None,P+'crossed-code-root-review/results/FRONTIER_INCORPORATION_CONTROLS.json'),
 ('crossed-symbolic',P+'crossed-code-root-review/symbolic_interior_control.py',None,P+'crossed-code-root-review/results/SYMBOLIC_INTERIOR_CONTROL.json'),
 ('adaptive-count',P+'adaptive-count-review/check_adaptive_count.py',P+'adaptive-count-review/results/INDEPENDENT_CONTROLS.json',None),
 ('multiroot-author',P+'multi-root-adaptive-bound/exact_controls.py',P+'multi-root-adaptive-bound/results/exact_controls.json',None),
 ('multiroot-review',P+'multi-root-adaptive-review/check_multiroot.py',P+'multi-root-adaptive-review/results/INDEPENDENT_CONTROLS.json',None),
 ('global-author',P+'global-calibration-ambiguity/exact_controls.py',P+'global-calibration-ambiguity/results/exact_controls.json',None),
 ('global-efficiency',P+'global-calibration-ambiguity/efficiency_controls.py',P+'global-calibration-ambiguity/results/efficiency_controls.json',None),
 ('global-review',P+'global-calibration-ambiguity-review/independent_controls.py',None,P+'global-calibration-ambiguity-review/independent_controls.json'),
 ('global-efficiency-review',P+'global-calibration-ambiguity-review/appendix_independent_controls.py',None,P+'global-calibration-ambiguity-review/appendix_independent_controls.json'),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():return {str(p.relative_to(ROOT)):sha(p) for p in ROOT.rglob('*') if p.is_file()}
a=argparse.ArgumentParser();a.add_argument('--output',required=True);a.add_argument('--allow-incomplete-stage',action='store_true');args=a.parse_args()
out=Path(args.output).resolve();assert out!=ROOT and ROOT not in out.parents,'Replay logs must be outside the checkpoint'
out.mkdir(parents=True,exist_ok=True)
initial=snapshot();checks=[]
import mpmath,sympy
with tempfile.TemporaryDirectory(prefix='t20-checkpoint-replay-') as temp:
 work=Path(temp)/'copy';shutil.copytree(ROOT,work)
 for name,script,generated,stdout_target in COMMANDS:
  if not (work/script).is_file():
   assert args.allow_incomplete_stage,script
   continue
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
  proc=subprocess.run([sys.executable,script],cwd=work,env=env,capture_output=True,timeout=300)
  (out/(name+'.stdout.log')).write_bytes(proc.stdout);(out/(name+'.stderr.log')).write_bytes(proc.stderr)
  row={'name':name,'command':['python3',script],'script_sha256':sha(ROOT/script),'exit_code':proc.returncode}
  if generated:
   row.update({'generated_path':generated,'expected_sha256':sha(ROOT/generated),'actual_sha256':sha(work/generated),'deterministic_file_byte_match':(ROOT/generated).read_bytes()==(work/generated).read_bytes()})
  if stdout_target:
   row.update({'stdout_target':stdout_target,'expected_sha256':sha(ROOT/stdout_target),'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'stdout_json_semantic_match':json.loads(proc.stdout)==json.loads((ROOT/stdout_target).read_bytes()),'stdout_byte_match':proc.stdout==(ROOT/stdout_target).read_bytes()})
  row['status']='PASS' if proc.returncode==0 and row.get('deterministic_file_byte_match',True) and row.get('stdout_json_semantic_match',True) else 'FAIL'
  checks.append(row);print(name,row['status'],flush=True)
final=snapshot();unchanged=initial==final
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'classification':'DELIVERY_ASSURANCE_NOT_ACTIVE_RESEARCH','python':sys.version,'dependencies':{'mpmath':mpmath.__version__,'sympy':sympy.__version__},'checks':checks,'checkpoint_bytes_unchanged':unchanged,'fresh_Lean_replay_performed':False,'status':'PASS' if unchanged and all(x['status']=='PASS' for x in checks) else 'FAIL'}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert receipt['status']=='PASS',receipt
