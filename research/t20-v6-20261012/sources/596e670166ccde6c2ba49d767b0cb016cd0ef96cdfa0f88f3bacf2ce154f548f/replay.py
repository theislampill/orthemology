#!/usr/bin/env python3
import argparse,hashlib,json,platform,shutil,subprocess,sys
from pathlib import Path
import sympy
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
 root=Path(__file__).resolve().parent;out=Path(args.output).resolve()
 assert not out.exists(),'Fresh output required'
 manifest=json.loads((root/'MANIFEST.json').read_text())
 actual=lambda:{str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
 assert actual()==manifest['files']
 ev=root/'evidence';a='radial-quartic-gradient-reverse-lift-20261010';r='radial-quartic-gradient-independent-review-20261010'
 excluded=json.loads((root/'EXCLUDED_SOURCE_BINDINGS.json').read_text())['files']
 verified=[];omitted=[]
 def bindings(source,mapping,prefix=''):
  for name,h in mapping.items():
   target=str(Path(prefix)/name);p=ev/target
   if p.is_file():assert sha(p)==h,(source,target);verified.append({'source':source,'target':target,'sha256':h})
   else:
    matches=[k for k in excluded if target.endswith(k)]
    assert len(matches)==1 and excluded[matches[0]]==h,(source,target)
    omitted.append({'source':source,'target':target,'sha256':h,'status':'excluded_not_revalidated'})
 receipt=json.loads((ev/r/'REVIEW_RECEIPT.json').read_text())
 bindings(r+'/REVIEW_RECEIPT.json',receipt['files'],r)
 snap=json.loads((ev/r/'AUTHOR_SNAPSHOT_BINDINGS.json').read_text())
 bindings(r+'/AUTHOR_SNAPSHOT_BINDINGS.json',snap['frozen_files'],a)
 bindings(r+'/AUTHOR_SNAPSHOT_BINDINGS.json',snap['source_files'])
 assert sha(ev/a/'AUTHOR_RECEIPT.json')==snap['receipt_sha256']
 author_receipt=json.loads((ev/a/'AUTHOR_RECEIPT.json').read_text())
 bindings(a+'/AUTHOR_RECEIPT.json',author_receipt['files'],a)
 full=json.loads((ev/a/'INPUT_BINDINGS.json').read_text());bindings(a+'/INPUT_BINDINGS.json',full)
 out.mkdir(parents=True);work=out/'work';shutil.copytree(ev,work)
 included={k:v for k,v in full.items() if k not in excluded}
 assert len(full)==8 and len(included)==6 and len(excluded)==2
 (work/a/'INPUT_BINDINGS.json').write_text(json.dumps(included,indent=2)+'\n')
 def run(name,cmd,cwd):
  p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
  (out/(name+'.stdout.txt')).write_text(p.stdout);(out/(name+'.stderr.txt')).write_text(p.stderr)
  assert p.returncode==0,(name,p.returncode,p.stderr)
 run('author_included_scope',[sys.executable,str(work/a/'check_exact.py')],work/a)
 original=json.loads((ev/a/'EXACT_CHECKS.json').read_text())
 removed=['input preserved: '+k for k in excluded]
 assert all(x in original['checks'] for x in removed)
 projection=dict(original);projection['checks']=[x for x in original['checks'] if x not in removed];projection['exact_check_count']=len(projection['checks'])
 expected=(json.dumps(projection,indent=2)+'\n').encode();assert projection['exact_check_count']==134
 (out/'EXPECTED_AUTHOR_INCLUDED_SCOPE.json').write_bytes(expected)
 assert (work/a/'EXACT_CHECKS.json').read_bytes()==expected
 independent=out/'INDEPENDENT_RESULTS.json'
 run('independent',[sys.executable,str(work/r/'check_independent.py'),'--output',str(independent)],work/r)
 assert independent.read_bytes()==(ev/r/'INDEPENDENT_RESULTS.json').read_bytes()
 assert json.loads(independent.read_text())['count']==106
 assert actual()==manifest['files'],'Extracted evidence changed'
 result={'status':'PASS','python':platform.python_version(),'sympy':sympy.__version__,'manifest_sha256':sha(root/'MANIFEST.json'),'included_files_verified':len(manifest['files']),'author_original_count':136,'author_offline_count':134,'author_algebra_controls':128,'author_included_antecedent_hashes':6,'author_excluded_source_hash_checks':removed,'author_generated_sha256':sha(work/a/'EXACT_CHECKS.json'),'author_exact_projection_match':True,'author_script_unchanged':sha(work/a/'check_exact.py')==sha(ev/a/'check_exact.py'),'independent_count':106,'independent_mutation_rejections':7,'independent_report_sha256':sha(independent),'independent_report_byte_identical':True,'included_bindings_verified':verified,'excluded_bindings_not_verified':omitted,'extracted_evidence_unchanged':True,'scope':'Ordinary mathematical evidence plus finite exact algebra. Two source-content hash checks deliberately excluded, not passed. No modern source validation, kernel build, numerical guarantee, integration or closure.'}
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'status':'PASS','author_offline_count':134,'independent_count':106,'receipt':str(out/'REPLAY_RECEIPT.json')}))
if __name__=='__main__':main()
