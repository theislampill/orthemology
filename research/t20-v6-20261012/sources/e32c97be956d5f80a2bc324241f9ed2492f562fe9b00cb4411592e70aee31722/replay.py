#!/usr/bin/env python3
import argparse,hashlib,json,platform,shutil,subprocess,sys
from pathlib import Path
import sympy
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output).resolve();assert not out.exists(),'Fresh output required'
 root=Path(__file__).resolve().parent;manifest=json.loads((root/'MANIFEST.json').read_text());actual=lambda:{str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p!=root/'MANIFEST.json'};assert actual()==manifest['files']
 ev=root/'evidence';a='moving-objective-order-interface-20261010';r='moving-objective-order-independent-review-20261010'
 receipt=json.loads((ev/r/'REVIEW_RECEIPT.json').read_text());assert sha(ev/a/'RESULT.md')==receipt['author_result_sha256'];assert sha(ev/a/'MANIFEST.json')==receipt['author_manifest_sha256']
 for k,h in receipt['files'].items():assert sha(ev/r/k)==h
 for k,h in json.loads((ev/r/'FROZEN_AUTHOR_INPUTS.json').read_text()).items():assert sha(ev/a/k)==h;assert sha(ev/r/'inputs'/k)==h
 for k,h in json.loads((ev/a/'INPUT_BINDINGS.json').read_text()).items():assert sha(ev/r/'predecessors'/k)==h
 out.mkdir(parents=True);work=out/'work';shutil.copytree(ev,work)
 p=subprocess.run([sys.executable,str(work/r/'check_independent.py')],cwd=work/r,text=True,capture_output=True);(out/'independent.stdout.txt').write_text(p.stdout);(out/'independent.stderr.txt').write_text(p.stderr);assert p.returncode==0,p.stderr
 reports={}
 for name in ['INDEPENDENT_CHECKS.json','AUTHOR_REPLAY.log','inputs/CHECK_RESULTS.json']:
  assert (work/r/name).read_bytes()==(ev/r/name).read_bytes();reports[name]=sha(work/r/name)
 data=json.loads((work/r/'INDEPENDENT_CHECKS.json').read_text());assert data['total']==38 and data['counts']['mathematical']==21
 assert actual()==manifest['files']
 result={'status':'PASS','python':platform.python_version(),'sympy':sympy.__version__,'manifest_sha256':sha(root/'MANIFEST.json'),'author_mathematical_controls':7,'review_total_checks':38,'independent_mathematical_controls':21,'all_three_outputs_byte_identical':True,'output_hashes':reports,'source_byte_exclusions':0,'path_relocations':0,'extracted_packet_unchanged':True,'scope':'Ordinary local moving-objective-order proof and exact controls only. Review38 includes identity/execution/count checks, not38 mathematical controls. No empirical/kernel/source validation, upload/integration/closure.'}
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','author_math':7,'review_total':38,'independent_math':21,'receipt':str(out/'REPLAY_RECEIPT.json')}))
if __name__=='__main__':main()
