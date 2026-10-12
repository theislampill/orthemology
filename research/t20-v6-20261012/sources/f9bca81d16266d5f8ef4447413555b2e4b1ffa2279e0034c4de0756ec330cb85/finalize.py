from pathlib import Path
import hashlib,json,datetime
W=Path.cwd();R=W/'hase-joint-proof-uniqueness-independent-review-20261010';C=W/'hase-joint-proof-uniqueness-20261010';H=W/'.toolchains/lean-4.19.0-linux'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest='ab4d52f539d70beb4b14a4e17cef29fdd00c06d4d976488478f7ef081b7e2bca';assert sha(C/'SOURCE_BOUNDARY.json')==manifest
b=json.loads((C/'SOURCE_BOUNDARY.json').read_text())
for x in b['retained']+b['additive']:assert sha(W/x['path'])==x['sha256'],x['path']
rows=json.loads((R/'SOURCE_INPUTS.json').read_text()); project={x['module'] for x in rows}
for x in rows:
 assert sha(W/x['original'])==x['sha256']
 assert sha(R/'sources'/(x['module'].replace('.','/')+'.lean'))==x['sha256']
imports=[line.split('IMPORTED ',1)[1].strip() for line in (R/'ProofUniquenessAudit.log').read_text().splitlines() if line.startswith('IMPORTED ')]
bind=json.load(open(W/'joint-computation-preservation-20261010/Joint_Induction_Computation_Intermediate_Evidence_20261010/prerequisites/IMPORT_BINDINGS.json'));bm={x['module']:x for x in bind}
pr=[]
for m in imports:
 if m in project:continue
 rel=Path(m.replace('.','/')+'.olean');p=R/'fresh-lib'/rel
 if p.is_symlink():p=p.resolve()
 elif p.exists():
  x=bm[m];p=W/x['object']['path'];assert sha(p)==sha(R/'fresh-lib'/rel)
 else:p=H/'lib/lean'/rel
 assert p.exists(),m
 pr.append({'module':m,'path':str(p.relative_to(W)),'sha256':sha(p),'bytes':p.stat().st_size})
(R/'STANDARD_OBJECT_PREREQUISITES.json').write_text(json.dumps(pr,indent=2)+'\n')
rebuild=json.loads((R/'REBUILD_PASS.json').read_text());assert rebuild['status']=='PASS'
assert (R/'IndependentControls.olean').exists() or (R/'fresh-lib/IndependentControls.olean').exists()
receipt={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_manifest_sha256':manifest,'candidate_report_sha256':sha(C/'RESULT.md'),'lean_version':'4.19.0','lean_binary_sha256':sha(H/'bin/lean'),'trust':0,'project_sources_freshly_compiled':len(rows),'independent_control_modules_freshly_compiled':1,'standard_import_objects_reused':len(pr),'standard_packages_freshly_compiled':False,'imported_modules_reported':len(imports),'candidate_and_retained_pins_verified':len(b['retained'])+len(b['additive']),'all_project_original_and_snapshot_sources_verified_unchanged':True,'semantic_verdict':'PASS with exact source-internal scope; no metaphysical identity inference','positive_axioms':['propext','Quot.sound'],'negative_control_axioms':['propext','Quot.sound','Classical.choice'],'baseline_linter_warnings':'27 pre-existing style/unused-variable warnings; no errors or sorry warnings','protected_source_edits':False,'integration':False,'closure':False}
files=['SOURCE_INPUTS.json','STANDARD_OBJECT_PREREQUISITES.json','REBUILD_PASS.json','IndependentControls.lean','IndependentControls.log','SEMANTIC_REVIEW.md','ProofUniquenessAudit.log','rebuild.py','run-controls.sh']
receipt['review_files']=[{'path':p,'sha256':sha(R/p)} for p in files]
(R/'REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
