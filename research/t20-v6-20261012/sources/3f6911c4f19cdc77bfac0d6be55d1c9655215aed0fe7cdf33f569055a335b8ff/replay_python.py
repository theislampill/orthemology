#!/usr/bin/env python3
"""Replay unchanged frozen controls in a disposable copy, never original files."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];P='t20-next-frontier-20261008/'
COMMANDS=[
 ('catalogue-author',P+'catalogue-mixture-sampling/exact_controls.py',P+'catalogue-mixture-sampling/results/exact_controls.json'),
 ('catalogue-frozen-author',P+'catalogue-mixture-review/frozen/exact_controls.py',P+'catalogue-mixture-review/frozen/results/exact_controls.json'),
 ('catalogue-independent',P+'catalogue-mixture-review/independent_checks.py',None),
 ('catalogue-receipt',P+'catalogue-mixture-review/verify_receipt.py',None),
 ('reason-author',P+'reason-causation-bridge/model/check_bridge.py',P+'reason-causation-bridge/model/RESULTS.json'),
 ('reason-independent',P+'reason-causation-review/independent_checks.py',None),
 ('reported-statistic-arithmetic',P+'fitrah-warrant-bridge/public-study-reanalysis/recompute_reported_statistics.py',P+'fitrah-warrant-bridge/public-study-reanalysis/arithmetic_results.json'),
]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args();out=Path(args.output).resolve()
 if out==ROOT or ROOT in out.parents:raise SystemExit('Output must be outside the immutable checkpoint.')
 out.mkdir(parents=True,exist_ok=True)
 try:
  import scipy
 except ImportError:raise SystemExit('SciPy is required only for the printed-statistic arithmetic check. See PACKING/requirements-arithmetic.txt; no package is installed automatically.')
 if scipy.__version__!='1.17.0':raise SystemExit('This byte-equality replay pins SciPy 1.17.0; installed '+scipy.__version__+'. See REPLAY.md.')
 records=json.loads((ROOT/'PACKING/SOURCE_COPY_BINDINGS.json').read_text())['files']
 assert all(h(ROOT/r['path'])==r['sha256'] for r in records)
 results=[]
 with tempfile.TemporaryDirectory(prefix='t20-warrant-empirical-replay-') as tmp:
  work=Path(tmp)/'evidence';shutil.copytree(ROOT,work)
  for label,script,output in COMMANDS:
   cmd=[sys.executable,script]
   p=subprocess.run(cmd,cwd=work,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0'),capture_output=True,text=True,timeout=300)
   same=True if output is None else (work/output).read_bytes()==(ROOT/output).read_bytes()
   (out/(label+'.log')).write_text(p.stdout+p.stderr+(('\nFrozen output byte equal: '+str(same)+'\n') if output else ''))
   result={'label':label,'command':cmd,'exit_code':p.returncode,'log':label+'.log'}
   if output:result.update({'output_file':output,'frozen_output_byte_equal':same})
   if label=='reason-independent' and p.returncode==0:
    equal=json.loads(p.stdout)==json.loads((ROOT/P/'reason-causation-review/INDEPENDENT_CHECKS.json').read_text());result['frozen_independent_json_equal']=equal;same &= equal
   results.append(result);print(label,p.returncode,same,flush=True)
 unchanged=all(h(ROOT/r['path'])==r['sha256'] for r in records)
 passed=unchanged and all(r['exit_code']==0 and r.get('frozen_output_byte_equal',True) and r.get('frozen_independent_json_equal',True) for r in results)
 receipt={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'scipy':scipy.__version__,'status':'PASS' if passed else 'FAIL','commands':results,'frozen_sources_unchanged':unchanged,'execution_location':'Disposable copied evidence tree','research_time_credit_seconds':0,'participant_level_data_used':False,'raw_data_reanalysis_or_replication':False,'fresh_lean_replay':False,'inherited_proof_rebuild':False,'scope':['Catalogue: 15 author families (also frozen replay), 5 independent families, receipt verification; these are exact synthetic controls for conditional confidence requirements.','Reason: finite 512-packet/2048-case semantic implementation and independent controls, mutation counterexamples, all 19 payload hashes and 13 exact predecessor bindings; no independent content/warrant/human-cognition verification.','Statistics: printed seven-row t/F-to-p consistency, rounding checks and preserved unaffected significant controls; no participant dataset.','Fresh equality checks compare four generated files byte-for-byte and the reason independent JSON semantically with their frozen versions.'],'skipped':['Inherited Lean imported --trust=0 replay and full dependency rebuild: not portable from this compact set of hash dependencies; original logs remain historical evidence only.','Primary-source acquisition/reading, empirical experiments, unavailable participant-data analysis, and philosophical or historical-duration certification are not performed by this harness.']}
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
