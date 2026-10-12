#!/usr/bin/env python3
"""Packing-only replay in a disposable copy; never writes the frozen evidence.

Standard library, Python 3.12 used. This is a new packaging harness, not a
research theorem or an alternate implementation of any scientific result.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,tempfile,re
ROOT=Path(__file__).resolve().parents[1]
P='t20-next-frontier-20261008/'
COMMANDS=[
 ('nonabsorption-diagnostic',P+'nonabsorption/diagnostic/response_diagnostic.py'),
 ('wise-determination-author-tests',P+'wise-determination/src/test_determination_contract.py'),
 ('eligibility-dependency-audit',P+'eligibility-review/src/dependency_audit.py'),
 ('two-root-author-tests',P+'productive-identifiability/src/test_identifiability.py'),
 ('general-root-author-tests',P+'productive-identifiability/general-roots/src/test_design_rank.py'),
 ('crt-author-tests',P+'single-calibration-design/src/test_crt_calibration.py'),
 ('two-root-independent-review-v2',P+'identification-review/independent_controls_v2.py'),
 ('general-root-independent-review',P+'identification-review/general_rank_controls.py'),
 ('crt-independent-review',P+'single-calibration-review/independent_crt_controls.py'),
 ('crt-constructor-crosscheck',P+'single-calibration-review/crosscheck_frozen_constructor.py'),
 ('crt-isolated-evidence-verifier',P+'single-calibration-design/src/verify_evidence.py'),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
 args=parser.parse_args();out=Path(args.output).resolve()
 if out==ROOT or ROOT in out.parents:raise SystemExit('Output must be outside the immutable checkpoint directory.')
 out.mkdir(parents=True,exist_ok=True)
 source_records=json.loads((ROOT/'PACKING/SOURCE_COPY_BINDINGS.json').read_text())['files']
 before={r['path']:sha(ROOT/r['path']) for r in source_records}
 assert all(before[r['path']]==r['sha256'] for r in source_records)
 results=[]
 with tempfile.TemporaryDirectory(prefix='t20-checkpoint-scoped-replay-') as tmp:
  isolated=Path(tmp)/'evidence';shutil.copytree(ROOT,isolated)
  for label,script in COMMANDS:
   cmd=[sys.executable,script]
   p=subprocess.run(cmd,cwd=isolated,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,timeout=300)
   (out/(label+'.log')).write_text(p.stdout+p.stderr)
   count=re.search(r'Ran (\d+) tests',p.stderr)
   results.append({'label':label,'command':cmd,'exit_code':p.returncode,'unit_test_count':int(count.group(1)) if count else None,'log':label+'.log'})
   print(label,p.returncode,flush=True)
  # Export deterministic research data in the disposable copy and compare it
  # byte-for-byte with the frozen result. No evidence file is overwritten.
  for component in ['productive-identifiability','single-calibration-design']:
   label=component+'-deterministic-export';script=P+component+'/src/export_results.py'
   cmd=[sys.executable,script];p=subprocess.run(cmd,cwd=isolated,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,timeout=300)
   equal=(isolated/P/component/'results/RESULTS.json').read_bytes()==(ROOT/P/component/'results/RESULTS.json').read_bytes()
   (out/(label+'.log')).write_text(p.stdout+p.stderr+'\nFrozen output byte-equal: '+str(equal)+'\n')
   results.append({'label':label,'command':cmd,'exit_code':p.returncode,'frozen_output_byte_equal':equal,'log':label+'.log'})
   print(label,p.returncode,equal,flush=True)
 unchanged=all(sha(ROOT/r['path'])==before[r['path']] for r in source_records)
 passed=unchanged and all(r['exit_code']==0 and r.get('frozen_output_byte_equal',True) for r in results)
 receipt={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'result':'PASS' if passed else 'FAIL','commands':results,'frozen_sources_unchanged':unchanged,'isolated_from_original_workspace':True,'research_time_credit_seconds':0,'limitations':['No fresh Lean kernel or mutation replay is performed by this Python harness. Existing frozen author and independent receipts are included.','No source-interpretation, source authentication, source eligibility or metaphysical validation is established by these checks.','The full productive-identifiability/src/verify_evidence.py provenance wrapper is not portable in this compact checkpoint because deliberately omitted historical and primary-text inputs are hashed before it runs. Its 20+8 tests and deterministic export are replayed directly here.','wise-determination/review/transport_probe.py contains a hard-coded original workspace path and is preserved with its original results, not replayed by this portable harness.','Historical review v1 and development failures are preserved as dated evidence, not silently recertified as the current stage.']}
 (out/'PYTHON_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
