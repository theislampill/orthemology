#!/usr/bin/env python3
import argparse,hashlib,json,platform,shutil,subprocess,sys
from pathlib import Path
import sympy
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output).resolve();assert not out.exists(),'Fresh output required'
 root=Path(__file__).resolve().parent;manifest=json.loads((root/'MANIFEST.json').read_text());actual=lambda:{str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'};assert actual()==manifest['files']
 ev=root/'evidence';a='asymptotic-gibbs-transport-20261010';r='asymptotic-gibbs-transport-independent-review-20261010';ancestor='nonconvex-atomic-limit-classification-20261010/RESULT.md'
 accepted=json.loads((ev/r/'REVIEW_RECEIPT.json').read_text());assert sha(ev/a/'AUTHOR_MANIFEST.json')==accepted['reviewed_author_manifest_sha256']
 for k,h in json.loads((ev/a/'AUTHOR_MANIFEST.json').read_text())['files'].items():assert sha(ev/a/k)==h
 for k,h in accepted['files'].items():assert sha(ev/r/k)==h
 original_binding=json.loads((ev/a/'INPUT_BINDING.json').read_text());assert sha(ev/ancestor)==original_binding['sha256']==accepted['ancestor_result_sha256']
 assert (ev/a/'INPUT_BINDING.json').read_bytes()==(ev/r/'inputs/INPUT_BINDING.json').read_bytes()
 out.mkdir(parents=True);work=out/'work';shutil.copytree(ev,work)
 binding=dict(original_binding);binding['path']=str(work/ancestor);newbytes=(json.dumps(binding,indent=2)+'\n').encode()
 for target in [work/a/'INPUT_BINDING.json',work/r/'inputs/INPUT_BINDING.json']:target.write_bytes(newbytes)
 oldhash=sha(ev/a/'INPUT_BINDING.json');newhash=sha(work/a/'INPUT_BINDING.json');script=work/r/'check_independent.py';original_script=(ev/r/'check_independent.py').read_bytes();assert original_script.count(oldhash.encode())==1
 derivative=original_script.replace(oldhash.encode(),newhash.encode(),1);script.write_bytes(derivative);assert script.read_bytes()==original_script.replace(oldhash.encode(),newhash.encode(),1)
 assert sha(work/ancestor)==accepted['ancestor_result_sha256']
 for target in [work/a/'AUTHOR_MANIFEST.json',work/r/'inputs/AUTHOR_MANIFEST.json']:assert sha(target)==accepted['reviewed_author_manifest_sha256']
 p=subprocess.run([sys.executable,str(script)],cwd=script.parent,text=True,capture_output=True)
 (out/'independent.stdout.txt').write_text(p.stdout);(out/'independent.stderr.txt').write_text(p.stderr);assert p.returncode==0,p.stderr
 comparisons={}
 for rel in ['INDEPENDENT_CHECKS.json','AUTHOR_REPLAY.log','inputs/EXACT_CHECKS.json']:
  assert (work/r/rel).read_bytes()==(ev/r/rel).read_bytes(),rel;comparisons[rel]=sha(work/r/rel)
 report=json.loads((work/r/'INDEPENDENT_CHECKS.json').read_text());assert report['independent_checks_total']==41 and report['counts_by_category']['symbolic']==29
 relocation={'original_binding_sha256':oldhash,'relocated_binding_sha256':newhash,'original_ancestor_path':original_binding['path'],'working_ancestor_path':binding['path'],'ancestor_content_sha256':sha(work/ancestor),'original_independent_checker_sha256':hashlib.sha256(original_script).hexdigest(),'working_independent_checker_sha256':sha(script),'allowed_transformations':['Author working binding path field relocated','Review snapshot working binding replaced with identical relocated bytes','One expected binding-hash literal substituted in working independent checker'],'original_manifests_unchanged':True,'mathematical_code_unchanged':True,'output_byte_comparisons':comparisons}
 (out/'RELOCATION_RECEIPT.json').write_text(json.dumps(relocation,indent=2)+'\n');assert actual()==manifest['files'],'Extracted evidence changed'
 result={'status':'PASS','python':platform.python_version(),'sympy':sympy.__version__,'manifest_sha256':sha(root/'MANIFEST.json'),'included_files_verified':len(manifest['files']),'author_algebra_controls':7,'author_ancestor_hash_controls':1,'independent_checks':41,'independent_mathematical_controls':29,'all_three_outputs_byte_identical':True,'relocation_receipt_sha256':sha(out/'RELOCATION_RECEIPT.json'),'relocation':relocation,'extracted_original_evidence_unchanged':True,'scope':'Explicitly reviewed working-copy portability relocation only. Ordinary entropy/measure proof and classical dependencies not kernel-verified. No external source bytes, upload, integration, owner acceptance or closure.'}
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','independent':41,'author_algebra':7,'receipt':str(out/'REPLAY_RECEIPT.json')}))
if __name__=='__main__':main()
