#!/usr/bin/env python3
import argparse,hashlib,json,platform,shutil,subprocess,sys
from pathlib import Path
import sympy
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output).resolve();assert not out.exists(),'Fresh output required'
 root=Path(__file__).resolve().parent;manifest=json.loads((root/'MANIFEST.json').read_text());actual=lambda:{str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p!=root/'MANIFEST.json'};assert actual()==manifest['files'];out.mkdir(parents=True);work=out/'work';shutil.copytree(root/'evidence',work)
 a=work/'pointwise-coercive-gradient-escape-20261011';r=work/'pointwise-coercive-gradient-escape-independent-review-20261011';nested=out/'reviewer-replay'
 for name,command in [('verify_before',[sys.executable,str(r/'verify_review.py'),'--author-dir',str(a)]),('replay',[sys.executable,str(r/'replay_review.py'),'--author-dir',str(a),'--output-dir',str(nested)]),('verify_after',[sys.executable,str(r/'verify_review.py'),'--author-dir',str(a)])]:
  p=subprocess.run(command,cwd=r,text=True,capture_output=True);(out/(name+'.stdout.txt')).write_text(p.stdout);(out/(name+'.stderr.txt')).write_text(p.stderr);assert p.returncode==0,(name,p.stderr)
 ar=nested/'author/EXACT_CHECKS.json';ir=nested/'independent/INDEPENDENT_RESULTS.json';assert ar.read_bytes()==(a/'EXACT_CHECKS.json').read_bytes();assert ir.read_bytes()==(r/'INDEPENDENT_RESULTS.json').read_bytes()
 data=json.loads((nested/'REPLAY_RESULTS.json').read_text());assert data['status']=='PASS' and data['author_checks']==43 and data['independent_checks']==50;assert actual()==manifest['files']
 result={'status':'PASS','python':platform.python_version(),'sympy':sympy.__version__,'manifest_sha256':sha(root/'MANIFEST.json'),'author_checks':43,'independent_checks':50,'both_reports_byte_identical':True,'author_report_sha256':sha(ar),'independent_report_sha256':sha(ir),'native_review_receipt':data,'source_byte_exclusions':0,'relocations':0,'extracted_packet_unchanged':True,'scope':'Accepted changing-gradient escape discriminator. Frozen-time coercivity is not common-energy continuation control; the positive theorem remains unchanged. General C1 guard exclusion is written Gronwall proof, not finite SOS search. No kernel/source-content proof, upload/integration/closure.'}
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','author':43,'independent':50,'receipt':str(out/'REPLAY_RECEIPT.json')}))
if __name__=='__main__':main()
