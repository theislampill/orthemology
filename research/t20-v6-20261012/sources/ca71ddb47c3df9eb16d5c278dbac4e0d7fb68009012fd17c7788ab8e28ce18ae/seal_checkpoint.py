from pathlib import Path
import datetime,hashlib,json,os,shutil,stat,sys,zipfile
import jsonschema
root=Path('private-locator:1dc82187dd31bb556614');dest=Path('/mnt/data')
name='Orthemology_P02_Measure_Research_Checkpoint_20260922'
archive=dest/(name+'.zip')
for path in [archive,root/'RECEIPT.json',root/'CHECKPOINT_MANIFEST.json']:
 if path.exists():raise SystemExit('Refusing to overwrite sealed output: '+str(path))
sha=lambda b:hashlib.sha256(b).hexdigest()
def row(p):
 b=p.read_bytes();return {'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':sha(b)}
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
shutil.copy2('private-locator:3e78408b6549d8f85ae2',root/'provenance/seal_checkpoint.py')
shutil.copy2('private-locator:d03da2fb7f1512b9747e',root/'provenance/build_metadata.py')
# Local final readback: no claim of native Git or remote status checking.
for p in (root/'proposals').rglob('*'):
 if p.is_file() and '__pycache__' in p.parts:raise SystemExit('Unwanted cache file: '+str(p))
for r in json.loads((root/'provenance/PROPOSAL_IDENTITIES.json').read_text())['files']:
 if row(root/r['path'])!=r:raise SystemExit('Changed proposal '+r['path'])
input_check=json.loads((root/'evidence/INPUT_VERIFICATION.json').read_text())
assert input_check['status']=='PASS' and input_check['binding_checks']==1842 and not input_check['failures']
for group in ['FINAL_TEST_ROOT_NORMAL','FINAL_TEST_ROOT_OPTIMISED','CENSUS_NORMAL','CENSUS_OPTIMISED_REPEAT','HANDOFF_SHELL_SYNTAX']:
 c=json.loads((root/'evidence'/group/'COMMAND.json').read_text());assert c['exit_code']==0
 for stream in ['stdout','stderr']:
  b=(root/'evidence'/group/(stream+'.bin')).read_bytes();assert sha(b)==c[stream+'_sha256'] and len(b)==c[stream+'_bytes']
assert (root/'evidence/finite-normal/mealy_3state.jsonl').read_bytes()==(root/'evidence/finite-optimised/mealy_3state.jsonl').read_bytes()
results=json.loads((root/'OBLIGATION_RESULTS.json').read_text())['results']
for r in results:
 assert r['obligation_status']=='PARTIAL' and not r['kernel_credit']
 assert row(root/r['statement_and_proof_file']['path'])==r['statement_and_proof_file']
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':['schema','status','main_commit','main_tree','research_executed','repository_modified','kernel_verified','obligation_ids','obligation_statuses','output_hashes'],'properties':{'schema':{'const':'orthemology-p02-research-checkpoint-v1'},'status':{'const':'PARTIAL_RESEARCH_CHECKPOINT'},'main_commit':{'const':'03e2604dfcef278b01c60d19b05370fcec4194b6'},'main_tree':{'const':'3d06e80277ce39286c94307e0f14b215bc94ed83'},'research_executed':{'const':True},'repository_modified':{'const':False},'kernel_verified':{'const':False},'obligation_ids':{'type':'array','uniqueItems':True,'minItems':5,'maxItems':5,'items':{'enum':['U05','U08','CV-R','CV-C','Q1c']}},'obligation_statuses':{'type':'object'},'output_hashes':{'type':'array','items':{'type':'object','required':['path','bytes','sha256'],'properties':{'path':{'type':'string'},'bytes':{'type':'integer','minimum':0},'sha256':{'type':'string','pattern':'^[a-f0-9]{64}$'}},'additionalProperties':False}}},'additionalProperties':True}
write(root/'RECEIPT.schema.json',schema)
files=[row(p) for p in sorted(root.rglob('*')) if p.is_file()]
receipt={'schema':'orthemology-p02-research-checkpoint-v1','status':'PARTIAL_RESEARCH_CHECKPOINT','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'main_commit':'03e2604dfcef278b01c60d19b05370fcec4194b6','main_tree':'3d06e80277ce39286c94307e0f14b215bc94ed83','PR_merged':28,'integration_cells_remaining':0,'main_identity_scope':'Inherited accepted packet; no fresh remote or full native tree requalification.','research_executed':True,'repository_modified':False,'kernel_verified':False,'obligation_ids':['U05','U08','CV-R','CV-C','Q1c'],'obligation_statuses':{r['id']:'PARTIAL' for r in results},'new_ordinary_work':'Supplied for review at exact stated hypotheses; no external-review or adoption credit.','new_finite_execution':{'test_methods_per_mode':14,'modes':['normal','optimised'],'mealy_machines_per_census':46656,'state_probability_Bellman_checks_per_census':139968,'proper_marginal_equalities':498,'projected_cell_checks':9324,'mixture_pair_profiles':83,'repeat_outputs_byte_identical':True},'new_formal_evidence':{'candidate_theorem_targets':11,'checked_theorem_targets':0,'observed_declaration_types':0,'observed_axiom_readbacks':0,'new_olean_artifacts':0,'runtime':'Lean/Lake/Elan unavailable; attempted acquisition did not produce a compiler.','Lean_target':'4.19.0 / 6caaee842e94','Lake_target':'5.0.0-6caaee8','Mathlib_target':'c44e0c8ee63ca166450922a373c7409c5d26b00b','later_commands_executed':False},'original_strict_wrapper':'FAIL_PRESERVED_SEPARATE_FROM_MAPPED_NATIVE','source_status_changes':[],'new_canonical_definitions_adopted':[],'other_packet_new_results_consumed':[],'owner_adoption_credit':'NONE','external_review_credit':'NONE','empirical_world_authority_credit':'NONE','historical_recovery_credit':'NONE','novelty_claim':'NONE','publication_or_contact':'NONE','source_files':539,'accepted_projection_bindings':54,'input_identity':{'path':'inputs/Orthemology_Pro_P02_Measure_CV_R_C.zip','bytes':1809066,'sha256':'70630d5b703fb3262e123b8424c19580e95bf604db3e9eb5d364653c333fdf13','members':620,'binding_checks':1842,'exact_selector_checks':5},'receipt_schema_note':'The unchanged input handoff schema fixes research_executed=false. This execution receipt uses a distinct schema.','verification_protocol':'All payload member hashes are in CHECKPOINT_MANIFEST.json; its own member hash is in the detached seal. A fresh independent reopen report is external so it does not alter the archive being verified.','independent_reopen_status':'RECORDED_AFTER_SEAL_IN_EXTERNAL_VERIFICATION_REPORT','output_hashes_scope':'All files present before this receipt, excluding this receipt, its detached digest and the final manifest to avoid circular hashing.','output_hashes':files}
jsonschema.Draft202012Validator.check_schema(schema);jsonschema.Draft202012Validator(schema).validate(receipt)
write(root/'RECEIPT.json',receipt)
(root/'RECEIPT.json.sha256').write_text(sha((root/'RECEIPT.json').read_bytes())+'  RECEIPT.json\n')
rows=[row(p) for p in sorted(root.rglob('*')) if p.is_file()]
write(root/'CHECKPOINT_MANIFEST.json',{'schema':'orthemology-p02-payload-manifest-v1','files':rows,'file_count':len(rows),'self_member':'CHECKPOINT_MANIFEST.json','self_hash_location':'detached SEAL.json, also bound by the outer archive digest','all_other_members_listed':True})
allfiles=sorted(p for p in root.rglob('*') if p.is_file())
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9,allowZip64=True) as z:
 for p in allfiles:
  info=zipfile.ZipInfo(p.relative_to(root).as_posix(),(2026,9,22,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16
  z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
b=archive.read_bytes();seal={'schema':'orthemology-p02-detached-seal-v1','archive':archive.name,'zip_bytes':len(b),'zip_sha256':sha(b),'zip_members':len(allfiles),'uncompressed_bytes':sum(p.stat().st_size for p in allfiles),'manifest_sha256':sha((root/'CHECKPOINT_MANIFEST.json').read_bytes()),'receipt_sha256':sha((root/'RECEIPT.json').read_bytes()),'manifested_files':len(rows),'receipt_schema_validated':True,'status':'SEALED_AWAITING_INDEPENDENT_REOPEN'}
write(dest/(name+'.SEAL.json'),seal)
(dest/(name+'.zip.sha256')).write_text(seal['zip_sha256']+'  '+archive.name+'\n')
shutil.copy2(root/'REPORT.md',dest/(name+'.REPORT.md'))
print(json.dumps(seal,indent=2))
