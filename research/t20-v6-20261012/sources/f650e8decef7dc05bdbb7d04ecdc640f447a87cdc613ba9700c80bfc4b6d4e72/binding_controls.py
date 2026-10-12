#!/usr/bin/env python3
"""Expected rejections of rehashed but misbound packing metadata; inputs untouched."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
cases=['wrong_author_review_pair','wrong_review_file','wrong_external_digest','missing_external_dependency','wrong_receipt_binding','omitted_stage_acceptance'];rows=[]
with tempfile.TemporaryDirectory(prefix='t20-eleventh-bindings-negative-') as tmp:
 for case in cases:
  work=Path(tmp)/case;shutil.copytree(ROOT,work)
  path=work/'PACKING/REVIEW_AND_DEPENDENCY_BINDINGS.json';b=json.loads(path.read_text())
  if case=='wrong_author_review_pair':b['accepted_results'][0]['author']=b['accepted_results'][1]['author']
  elif case=='wrong_review_file':b['accepted_results'][0]['review']=b['accepted_results'][1]['review']
  elif case=='wrong_external_digest':b['external_predecessor_bindings'][0]['sha256']='0'*64
  elif case=='missing_external_dependency':b['external_predecessor_bindings'].pop(0)
  elif case=='wrong_receipt_binding':b['accepted_results'][0]['binding_record']=b['accepted_results'][3]['binding_record']
  elif case=='omitted_stage_acceptance':b['accepted_results'].pop()
  dump(path,b)
  # Rehash top inventory, so rejection tests declared relationships, not a stale top hash.
  manifest_path=work/'MANIFEST.json';manifest=json.loads(manifest_path.read_text())
  for r in manifest['files']:
   if r['path']=='PACKING/REVIEW_AND_DEPENDENCY_BINDINGS.json':r.update({'sha256':sha(path),'bytes':path.stat().st_size})
  dump(manifest_path,manifest);(work/'MANIFEST.sha256').write_text(sha(manifest_path)+'  MANIFEST.json\n')
  run=subprocess.run([sys.executable,str(work/'PACKING/check_manifest.py')],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0'),capture_output=True,text=True)
  rows.append({'case':case,'status':'PASS_EXPECTED_REJECTION' if run.returncode!=0 else 'FAIL_UNEXPECTED_ACCEPTANCE','exit_code':run.returncode,'diagnostic':run.stderr.strip().splitlines()[-1] if run.stderr.strip() else '', 'top_manifest_rehashed_for_test':True})
report={'status':'PASS' if all(r['status']=='PASS_EXPECTED_REJECTION' for r in rows) else 'FAIL','controls':rows,'scope':'Exact result/review/dependency relationship guards in disposable metadata copies; not a mathematical theorem verifier.'}
print(json.dumps(report,indent=2));assert report['status']=='PASS'
