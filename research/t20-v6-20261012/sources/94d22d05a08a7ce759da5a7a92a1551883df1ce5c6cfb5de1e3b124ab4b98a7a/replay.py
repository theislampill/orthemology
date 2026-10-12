#!/usr/bin/env python3
import argparse,hashlib,json,platform,shutil,subprocess,sys
from pathlib import Path
import sympy
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output).resolve();assert not out.exists(),'Fresh output required'
 root=Path(__file__).resolve().parent;manifest=json.loads((root/'MANIFEST.json').read_text());actual=lambda:{str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'};assert actual()==manifest['files']
 ev=root/'evidence';a='nonconvex-atomic-limit-classification-20261010';r='nonconvex-limit-classification-independent-review-20261010'
 am=json.loads((ev/a/'FROZEN_MANIFEST.json').read_text())
 for k,h in am['files'].items():assert sha(ev/a/k)==h;assert (ev/a/k).read_bytes()==(ev/r/'author_snapshot'/k).read_bytes()
 for row in json.loads((ev/a/'INPUT_BINDINGS.json').read_text()):assert sha(ev/a/row['copy'])==row['sha256']
 out.mkdir(parents=True);work=out/'work';shutil.copytree(ev,work)
 nested=out/'reviewer-replay';p=subprocess.run([sys.executable,str(work/r/'check_review.py'),'--output-dir',str(nested)],cwd=work/r,text=True,capture_output=True)
 (out/'reviewer.stdout.txt').write_text(p.stdout);(out/'reviewer.stderr.txt').write_text(p.stderr);assert p.returncode==0,p.stderr
 receipt=json.loads((nested/'REPLAY_RECEIPT.json').read_text());assert receipt['status']=='PASS' and receipt['author_portable_check_count']==85 and receipt['independent_control_count']==10
 assert actual()==manifest['files'],'Extracted packet changed'
 result={'status':'PASS','python':platform.python_version(),'sympy':sympy.__version__,'manifest_sha256':sha(root/'MANIFEST.json'),'included_files_verified':len(manifest['files']),'author_checks':85,'independent_checks':10,'full_portable_reports_byte_identical':True,'author_report_sha256':sha(nested/'portable_author/EXACT_CHECKS.json'),'independent_report_sha256':sha(nested/'INDEPENDENT_CONTROLS.json'),'native_review_receipt_sha256':sha(nested/'REPLAY_RECEIPT.json'),'native_review_receipt':receipt,'extracted_packet_unchanged':True,'scope':'Accepted ordinary mathematics; finite exact controls only. No source-byte exclusions needed for these suites; no source content revalidation or kernel rebuild. Historical91 live-original run retained; no upload/integration/closure.'}
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','author':85,'independent':10,'receipt':str(out/'REPLAY_RECEIPT.json')}))
if __name__=='__main__':main()
