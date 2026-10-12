#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,zipfile,datetime
r=Path(__file__).resolve().parent; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=Path((r/'LATEST_REPLAY.txt').read_text().strip()); controls=Path((r/'LATEST_CONTROLS.txt').read_text().strip());d=json.loads(receipt.read_text());c=json.loads(controls.read_text());a=json.loads((r/'SEAL_RECONCILIATION.json').read_text());assert d['status']==c['status']==a['status']=='PASS';assert a['all_53_custom_sources_match_archive'];assert d['origins_unchanged'] and c['origins_unchanged']
files=[p for p in sorted(r.rglob('*')) if p.is_file() and p.suffix not in ['.olean','.ilean','.pyc'] and 'lib' not in p.relative_to(r).parts and '__pycache__' not in p.relative_to(r).parts and p.name not in ['INDEPENDENT_SEAL.json','Atomic_Membership_Independent_Audit_20260930.zip','ARCHIVE_SEAL.json']]
seal={'status':'INDEPENDENT_PASS_QUALIFIED_SCOPE','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'subject_archive_sha256':a['author_archive_sha256'],'subject_seal_sha256':a['author_archive_seal_sha256'],'fresh_custom_modules':len(d['sources']),'author_target_count':len(d['targets']),'review_control_theorem_count':c['control_theorem_count'],'runtime_differential_checks':c['differential_check_count'],'exact_rational_checks':c['exact_rational_check_count'],'negative_controls':c['negative_control_count'],'ordinary_uniform_computability_argument':'independently accepted','uniform_mathlib_computable_certificate':False,'canonical_adoption':False,'whole_obligation_closure':False,'build_receipt_sha256':sha(receipt),'control_receipt_sha256':sha(controls),'files':[{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]}
(r/'INDEPENDENT_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
z=r/'Atomic_Membership_Independent_Audit_20260930.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as out:
 for p in files+[r/'INDEPENDENT_SEAL.json']:out.write(p,str(p.relative_to(r)))
with zipfile.ZipFile(z) as inp:
 assert len(inp.namelist())==len(set(inp.namelist()))
 for f in seal['files']:
  b=inp.read(f['path']);assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
archive={'archive':str(z),'bytes':z.stat().st_size,'sha256':sha(z),'members':len(files)+1,'independent_seal_sha256':sha(r/'INDEPENDENT_SEAL.json')};(r/'ARCHIVE_SEAL.json').write_text(json.dumps(archive,indent=2)+'\n');print(json.dumps(archive))
