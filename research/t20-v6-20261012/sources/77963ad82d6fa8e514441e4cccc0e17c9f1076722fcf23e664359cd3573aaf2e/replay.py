#!/usr/bin/env python3
import argparse,hashlib,json,platform,shutil,subprocess,sys
from pathlib import Path
import sympy
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output).resolve();assert not out.exists(),'Fresh output required'
 root=Path(__file__).resolve().parent;manifest=json.loads((root/'MANIFEST.json').read_text());actual=lambda:{str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'};assert actual()==manifest['files']
 ev=root/'evidence';a='full-law-gradient-action-tail-20261010';r='full-law-gradient-action-tail-independent-review-20261010'
 am=json.loads((ev/a/'FROZEN_MANIFEST.json').read_text())
 for k,h in am['files'].items():assert sha(ev/a/k)==h;assert (ev/a/k).read_bytes()==(ev/r/'author_snapshot'/k).read_bytes()
 for row in json.loads((ev/a/'INPUT_BINDINGS.json').read_text()):assert sha(ev/a/row['copy'])==row['sha256']
 out.mkdir(parents=True);work=out/'work';shutil.copytree(ev,work);nested=out/'reviewer-replay'
 p=subprocess.run([sys.executable,str(work/r/'check_review.py'),'--output-dir',str(nested)],cwd=work/r,text=True,capture_output=True)
 (out/'reviewer.stdout.txt').write_text(p.stdout);(out/'reviewer.stderr.txt').write_text(p.stderr);assert p.returncode==0,p.stderr
 summary=json.loads(p.stdout);assert summary['independent_control_count']==29 and summary['portable_author_check_count']==25
 author=nested/'portable-author-replay/EXACT_CHECKS.json';independent=nested/'INDEPENDENT_CONTROLS.json'
 assert author.read_bytes()==(ev/a/'portable-author-run/EXACT_CHECKS.json').read_bytes();assert independent.read_bytes()==(ev/r/'initial-run/INDEPENDENT_CONTROLS.json').read_bytes()
 assert actual()==manifest['files'],'Extracted packet changed'
 result={'status':'PASS','python':platform.python_version(),'sympy':sympy.__version__,'manifest_sha256':sha(root/'MANIFEST.json'),'included_files_verified':len(manifest['files']),'author_portable_checks':25,'independent_controls':29,'both_generated_reports_byte_identical':True,'author_report_sha256':sha(author),'independent_report_sha256':sha(independent),'original_review_summary':summary,'source_byte_exclusions':0,'path_relocations':0,'extracted_packet_unchanged':True,'scope':'Portable integrity and finite exact controls only. Separate original-aware31 run is not claimed here. Ordinary action-tail/initial-energy qualifications retained; no source-content/kernel proof, upload/integration/closure.'}
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','author':25,'independent':29,'receipt':str(out/'REPLAY_RECEIPT.json')}))
if __name__=='__main__':main()
