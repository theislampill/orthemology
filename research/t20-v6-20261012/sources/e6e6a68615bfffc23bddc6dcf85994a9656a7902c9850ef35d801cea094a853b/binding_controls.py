#!/usr/bin/env python3
"""Small resealed relationship-negative checks; not scientific controls."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cases=['result_digest','broadened_H_P_review','obsolete_root_judgement','missing_external_binding','omission_as_failure','erased_historical_gap','wrong_prior_seal','unavailable_reply_claimed_read','fresh_kernel_credit']
rows=[]
with tempfile.TemporaryDirectory(prefix='t20-fourteenth-binding-') as t:
 for case in cases:
  r=Path(t)/case;shutil.copytree(R,r)
  p=r/'INCREMENTAL_RESULT_SOURCE_EVIDENCE_DEPENDENCY_MANIFEST.json';d=read(p)
  if case=='result_digest':d['results'][0]['author']['sha256']='0'*64
  elif case=='broadened_H_P_review':next(x for x in d['results'] if x['id']=='modal-psr-bridge')['internal_review_scope']='FULL_REPORT_INTERNAL_REVIEW'
  elif case=='obsolete_root_judgement':d['root_state']['latest']=d['root_state']['historical_positive_judgement']
  elif case=='unavailable_reply_claimed_read':d['unavailable_source_work']['status']='FULL_BODY_READ'
  elif case=='fresh_kernel_credit':d['boundaries']['new_lean_execution']=True
  elif case=='wrong_prior_seal':p=r/'COMPONENT_AND_PRIOR_IDENTITIES.json';d=read(p);d['prior_checkpoints'][-1]['sha256']='0'*64
  else:
   p=r/'PACKING/REVIEW_AND_DEPENDENCY_BINDINGS.json';d=read(p)
   if case=='missing_external_binding':d['external_dependencies'].pop(0)
   elif case=='omission_as_failure':d['external_dependencies'][0]['verification_failure']=True
   elif case=='erased_historical_gap':d['historical_declarations_without_bytes'].pop()
  dump(p,d);m=read(r/'MANIFEST.json')
  for x in m['files']:q=r/x['path'];x['bytes']=q.stat().st_size;x['sha256']=sha(q)
  dump(r/'MANIFEST.json',m);(r/'MANIFEST.sha256').write_text(sha(r/'MANIFEST.json')+'  MANIFEST.json\n')
  proc=subprocess.run([sys.executable,'-B',str(r/'PACKING/check_manifest.py')],capture_output=True,text=True)
  assert proc.returncode!=0,(case,'UNEXPECTED_ACCEPTANCE')
  rows.append({'case':case,'status':'PASS_EXPECTED_REJECTION','manifest_resealed':True,'returncode':proc.returncode,'diagnostic_tail':proc.stderr.splitlines()[-1]})
print(json.dumps({'status':'PASS','controls':rows,'scope':'Packaging relationship guards only, not independent source or metaphysical assessment.'},indent=2))
