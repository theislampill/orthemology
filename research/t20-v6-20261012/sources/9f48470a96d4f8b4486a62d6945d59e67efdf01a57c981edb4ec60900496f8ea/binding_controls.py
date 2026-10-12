#!/usr/bin/env python3
"""Reseal disposable metadata corruptions; binding checks must still reject."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cases=['accepted_result_digest','removed_external_dependency','declared_binding_digest','ninth_authority_digest','wrong_review_link','note_promoted_to_proof']
rows=[]
with tempfile.TemporaryDirectory(prefix='t20-thirteenth-binding-') as t:
 for case in cases:
  r=Path(t)/case;shutil.copytree(ROOT,r)
  if case in ['accepted_result_digest','wrong_review_link','note_promoted_to_proof']:
   p=r/'INCREMENTAL_RESULT_SOURCE_EVIDENCE_DEPENDENCY_MANIFEST.json';d=read(p)
   if case=='accepted_result_digest':d['results'][0]['author']['sha256']='0'*64
   if case=='wrong_review_link':d['results'][0]['review']=d['results'][1]['review']
   if case=='note_promoted_to_proof':d['separately_classified_notes'][0]['classification']='NEW_PROOF'
  elif case=='ninth_authority_digest':
   p=r/'COMPONENT_AND_PRIOR_IDENTITIES.json';d=read(p);d['prior_checkpoints'][8]['sha256']='0'*64
  else:
   p=r/'PACKING/REVIEW_AND_DEPENDENCY_BINDINGS.json';d=read(p)
   if case=='removed_external_dependency':d['external_retained_dependencies'].pop(0)
   else:d['explicit_path_hash_rows'][0]['sha256']='0'*64
  dump(p,d)
  m=read(r/'MANIFEST.json')
  for row in m['files']:
   q=r/row['path'];row['bytes']=q.stat().st_size;row['sha256']=sha(q)
  dump(r/'MANIFEST.json',m);(r/'MANIFEST.sha256').write_text(sha(r/'MANIFEST.json')+'  MANIFEST.json\n')
  p=subprocess.run([sys.executable,'-B',str(r/'PACKING/check_manifest.py')],capture_output=True,text=True)
  assert p.returncode!=0,(case,'unexpected acceptance')
  rows.append({'case':case,'status':'PASS_EXPECTED_REJECTION','manifest_resealed_before_test':True,'returncode':p.returncode,'diagnostic_tail':p.stderr.splitlines()[-1]})
print(json.dumps({'status':'PASS','controls':rows,'scope':'Disposable metadata relationship controls, not research or source-reading validation.'},indent=2))
