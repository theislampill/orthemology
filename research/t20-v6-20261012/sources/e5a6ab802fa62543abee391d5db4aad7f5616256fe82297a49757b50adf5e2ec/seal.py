from pathlib import Path
import hashlib,json,zipfile,datetime
r=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
controls=json.loads((r/'CONTROLS_RESULT.json').read_text());assert controls['status']=='PASS' and controls['theorem_count']==82 and controls['differential_check_count']==758
fresh=json.loads((r/'receipts/20260930T161345Z/RESULT.json').read_text());assert fresh['status']=='PASS' and len(fresh['sources'])==49 and fresh['origins_unchanged']
for m,rec in fresh['sources'].items():
 assert sha(r/'receipts/20260930T161345Z/sources'/(m.replace('.','/')+'.lean'))==rec['sha256']
 assert sha(Path(rec['origin']))==rec['sha256']
assert (r/'Differential.log').read_text().strip()=='PASS 758 differential checks (82 generated programs)'
exclude={'FILES_MANIFEST.json','SEAL.json','SEAL.json.sha256','DifferentialBatched.lean'}
files=[p for p in sorted(r.rglob('*')) if p.is_file() and p.name not in exclude and not ({'lib','__pycache__','bundle-reopen'} & set(p.relative_to(r).parts)) and p.suffix not in {'.olean','.ilean','.pyc'}]
manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]};(r/'FILES_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
seal={'status':'INDEPENDENT_TECHNICAL_PASS_WITH_EXPLICIT_BOUNDARIES','author_seal_sha256':'271d070be9a69948a8d3f9545de52882eaf4aaa74f5b5e5cdb9004eea261f35a','manifest_sha256':sha(r/'FILES_MANIFEST.json'),'report_sha256':sha(r/'REPORT.md'),'fresh_closure_receipt_sha256':sha(r/'receipts/20260930T161345Z/RESULT.json'),'controls_receipt_sha256':sha(r/'CONTROLS_RESULT.json'),'modules':49,'target_theorems':82,'differential_checks':758,'negative_controls':5,'index_set_membership_proved':False,'full_python_runtime_refinement':False,'canonical_adoption':False,'whole_obligation_closure':False};(r/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');(r/'SEAL.json.sha256').write_text(sha(r/'SEAL.json')+'  SEAL.json\n')
z=r.parent/'Effective_Index_Independent_Audit_20260930.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for p in files+[r/'FILES_MANIFEST.json',r/'SEAL.json',r/'SEAL.json.sha256']:f.write(p,'effective-index-independent-audit/'+str(p.relative_to(r)))
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for e in manifest['files']:
  b=f.read('effective-index-independent-audit/'+e['path']);assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
assert 'lib' not in [Path(x).parts[-2] for x in zipfile.ZipFile(z).namelist() if len(Path(x).parts)>1]
summary={'archive':str(z),'archive_bytes':z.stat().st_size,'archive_sha256':sha(z),'seal':str(r/'SEAL.json'),'seal_sha256':sha(r/'SEAL.json'),'report_sha256':sha(r/'REPORT.md'),'files':len(manifest['files']),'reopened_verified':True};(r.parent/'Effective_Index_Independent_Audit_20260930.seal.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
