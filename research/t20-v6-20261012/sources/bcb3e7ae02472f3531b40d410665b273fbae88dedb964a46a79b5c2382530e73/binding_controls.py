#!/usr/bin/env python3
"""Bounded resealed negative tests for result, review, provenance and scope bindings."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cases=['result_digest','old_review_rebound_to_final','obsolete_root_judgement','missing_external_binding','omission_as_failure','erased_inherited_historical_gap','wrong_prior_seal','regular_open_promoted']
rows=[]
with tempfile.TemporaryDirectory(prefix='t20-fifteenth-binding-') as t:
 for case in cases:
  r=Path(t)/case;shutil.copytree(R,r)
  p=r/'INCREMENTAL_RESULT_SOURCE_EVIDENCE_DEPENDENCY_MANIFEST.json';d=read(p)
  if case=='result_digest':d['results'][0]['author']['sha256']='0'*64
  elif case=='obsolete_root_judgement':
   d['root_state']['latest']=d['root_state']['historical_positive_judgement'];d['boundaries']['current_root_judgement']=d['root_state'];bounds=read(r/'EVIDENCE_BOUNDARIES.json');bounds['current_root_judgement']=d['root_state'];dump(r/'EVIDENCE_BOUNDARIES.json',bounds)
  elif case=='regular_open_promoted':
   d['boundaries']['regular_open_realization']='KERNEL_CHECKED';bounds=read(r/'EVIDENCE_BOUNDARIES.json');bounds['regular_open_realization']='KERNEL_CHECKED';dump(r/'EVIDENCE_BOUNDARIES.json',bounds)
  elif case=='wrong_prior_seal':p=r/'COMPONENT_AND_PRIOR_IDENTITIES.json';d=read(p);d['prior_checkpoints'][-1]['sha256']='0'*64
  else:
   p=r/'PACKING/REVIEW_AND_DEPENDENCY_BINDINGS.json';d=read(p)
   if case=='old_review_rebound_to_final':
    row=next(x for x in d['explicit_bindings'] if x['record']=='explanation-bridge-review/INPUTS.json' and x['declared_path']=='particular-explanans-bridge-audit/RESULT.md');row['path']=row['declared_path'];row['sha256']='7f347b80c097ecb4c71a361b0128ad39fa0fb41ceb6c84374c1e8924b100761c';row['bytes']=14810
   elif case=='missing_external_binding':d['external_dependencies'].pop(0)
   elif case=='omission_as_failure':d['external_dependencies'][0]['verification_failure']=True
   elif case=='erased_inherited_historical_gap':d['inherited_predecessor_revision_limits'].pop()
  dump(p,d);m=read(r/'MANIFEST.json')
  for x in m['files']:q=r/x['path'];x['bytes']=q.stat().st_size;x['sha256']=sha(q)
  dump(r/'MANIFEST.json',m);(r/'MANIFEST.sha256').write_text(sha(r/'MANIFEST.json')+'  MANIFEST.json\n')
  proc=subprocess.run([sys.executable,'-B',str(r/'PACKING/check_manifest.py')],capture_output=True,text=True,timeout=60)
  assert proc.returncode!=0,(case,'UNEXPECTED_ACCEPTANCE')
  rows.append({'case':case,'status':'PASS_EXPECTED_REJECTION','manifest_resealed':True,'returncode':proc.returncode,'diagnostic_tail':proc.stderr.splitlines()[-1]})
print(json.dumps({'status':'PASS','controls':rows,'scope':'Packaging relationships only; no independent source, mathematical or metaphysical validation.'},indent=2))
