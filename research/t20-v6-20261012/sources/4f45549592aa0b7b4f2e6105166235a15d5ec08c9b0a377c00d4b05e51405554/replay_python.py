#!/usr/bin/env python3
"""Scoped packaging replay in a disposable copy; no research-source edits."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,tempfile,re
ROOT=Path(__file__).resolve().parents[1];P='t20-next-frontier-20261008/'
COMMANDS=[
 ('noise-author-tests',P+'noise-aware-calibration/src/test_robust_masks.py'),
 ('noise-independent-controls',P+'noise-aware-review/independent_noise_controls.py'),
 ('noise-restricted-lower-bound',P+'noise-aware-review/check_lower_bound.py'),
 ('noise-frozen-decoder-crosscheck',P+'noise-aware-review/crosscheck_frozen_decoder.py'),
 ('countable-author-tests',P+'countable-signature-identification/src/test_countable_support.py'),
 ('gcd-author-tests',P+'countable-signature-identification/src/test_gcd_decoder.py'),
 ('oracle-author-tests',P+'countable-signature-identification/src/test_oracle_boundaries.py'),
 ('countable-independent-controls',P+'countable-signature-review/independent_countable_controls.py'),
 ('gcd-independent-controls',P+'countable-signature-review/independent_gcd_decoder.py'),
 ('countable-frozen-decoder-crosscheck',P+'countable-signature-review/crosscheck_frozen_decoders.py'),
 ('arithmetic-boundary-control',P+'countable-signature-review/check_arithmetic_block.py'),
 ('grouped-author-controls',P+'grouped-mixture-identification/exact_controls.py'),
]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);a=parser.parse_args();out=Path(a.output).resolve()
 if out==ROOT or ROOT in out.parents:raise SystemExit('Replay output must be outside this immutable checkpoint.')
 out.mkdir(parents=True,exist_ok=True)
 files=json.loads((ROOT/'PACKING/SOURCE_COPY_BINDINGS.json').read_text())['files']
 assert all(digest(ROOT/r['path'])==r['sha256'] for r in files)
 cmds=list(COMMANDS)
 additions=ROOT/'PACKING/ADDITIONAL_REPLAY_COMMANDS.json'
 if additions.is_file():cmds+=json.loads(additions.read_text())
 records=[]
 with tempfile.TemporaryDirectory(prefix='t20-additional-replay-') as tmp:
  work=Path(tmp)/'evidence';shutil.copytree(ROOT,work)
  for label,script in cmds:
   cmd=[sys.executable,script];p=subprocess.run(cmd,cwd=work,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0'),capture_output=True,text=True,timeout=300)
   (out/(label+'.log')).write_text(p.stdout+p.stderr)
   count=re.search(r'Ran (\d+) tests',p.stderr)
   records.append({'label':label,'command':cmd,'exit_code':p.returncode,'unit_test_count':int(count.group(1)) if count else None,'log':label+'.log'})
   print(label,p.returncode,flush=True)
  for component in ['noise-aware-calibration','countable-signature-identification']:
   label=component+'-export';script=P+component+'/src/export_results.py';cmd=[sys.executable,script]
   p=subprocess.run(cmd,cwd=work,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0'),capture_output=True,text=True,timeout=300)
   same=(work/P/component/'results/RESULTS.json').read_bytes()==(ROOT/P/component/'results/RESULTS.json').read_bytes()
   (out/(label+'.log')).write_text(p.stdout+p.stderr+'\nByte equal to frozen export: '+str(same)+'\n')
   records.append({'label':label,'command':cmd,'exit_code':p.returncode,'frozen_export_byte_equal':same,'log':label+'.log'})
   print(label,p.returncode,same,flush=True)
 unchanged=all(digest(ROOT/r['path'])==r['sha256'] for r in files)
 passed=unchanged and all(x['exit_code']==0 and x.get('frozen_export_byte_equal',True) for x in records)
 receipt={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'status':'PASS' if passed else 'FAIL','commands':records,'frozen_sources_unchanged':unchanged,'disposable_copy':True,'research_time_credit_seconds':0,'fresh_lean_replay':False,'limitations':['Exact rational finite controls do not prove every written arbitrary-k/countable theorem or imported Zsigmondy theorem.','Original full provenance wrappers are not run: they require omitted historical inputs and, for countable, the deliberately omitted original source PDF. The exact standalone test suites and deterministic exports are run.','No primary source reading, empirical sampling, physical model validation, practical-authority adoption, or historical duration certification is performed by this harness.']}
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
