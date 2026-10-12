"""Seal the final research payload; independent verification is a separate process."""
from pathlib import Path
import hashlib,json,zipfile,datetime,sys,os
R=Path(__file__).resolve().parents[1]
OUT=R.parent/'Orthemology_P02_Measure_Research_Checkpoint_attempt-0002.zip'
def sh(b):return hashlib.sha256(b).hexdigest()
def write(n,d):(R/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def paths():return sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
def row(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)),'bytes':len(b),'sha256':sh(b)}
schema={
 '$schema':'https://json-schema.org/draft/2020-12/schema',
 'type':'object','required':['schema','status','created_utc','canonical_boundary','obligation_statuses','output_hashes','full_exhaustion_certified','kernel_verified','input_predecessor'],
 'properties':{'schema':{'const':'orthemology-p02-attempt2-research-receipt-v1'},'status':{'const':'SUPERSEDING_RESEARCH_CHECKPOINT_NOT_FULL_EXHAUSTION'},
 'created_utc':{'type':'string'},'full_exhaustion_certified':{'const':False},'kernel_verified':{'const':False},
 'canonical_boundary':{'type':'object','required':['main','tree','repository_effects'],
  'properties':{'main':{'const':'03e2604dfcef278b01c60d19b05370fcec4194b6'},'tree':{'const':'3d06e80277ce39286c94307e0f14b215bc94ed83'},'repository_effects':{'const':[]}}},
 'obligation_statuses':{'type':'object','required':['U05','U08','CV-R','CV-C','Q1c']},
 'input_predecessor':{'type':'object','required':['bytes','sha256','zip_members'],
  'properties':{'bytes':{'const':4192393},'sha256':{'const':'365d6e27c953102aba2f1749286ff731e0b1b50bf15c2a4cc9ed576eeb02bfc9'},'zip_members':{'const':693}}},
 'output_hashes':{'type':'array','minItems':1,'items':{'type':'object','required':['path','bytes','sha256'],'properties':{'path':{'type':'string'},'bytes':{'type':'integer','minimum':0},'sha256':{'type':'string','pattern':'^[0-9a-f]{64}$'}}}}}}
write('RECEIPT.schema.json',schema)
excluded={'RECEIPT.json','RECEIPT.json.sha256','CHECKPOINT_MANIFEST.json'}
outputs=[row(p) for p in paths() if str(p.relative_to(R)) not in excluded]
ob=json.loads((R/'OBLIGATION_RESULTS.json').read_text())
receipt={
 'schema':'orthemology-p02-attempt2-research-receipt-v1','status':'SUPERSEDING_RESEARCH_CHECKPOINT_NOT_FULL_EXHAUSTION',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'canonical_boundary':{'main':'03e2604dfcef278b01c60d19b05370fcec4194b6','tree':'3d06e80277ce39286c94307e0f14b215bc94ed83','PR_merged':28,'integration_cells_remaining':0,'repository_effects':[],'identity_scope':'Inherited accepted packet; not a new live remote qualification'},
 'input_predecessor':{'path':'predecessor/Orthemology_P02_Measure_Research_Checkpoint_20260922.zip','bytes':4192393,'sha256':'365d6e27c953102aba2f1749286ff731e0b1b50bf15c2a4cc9ed576eeb02bfc9','zip_members':693,'preserved_byte_for_byte':True},
 'obligation_statuses':{x['id']:x['terminal_status'] for x in ob['results']},
 'research_scope_PASS':['U08','Q1c'],'formal_scope_PASS':[],'full_exhaustion_certified':False,'kernel_verified':False,
 'new_ordinary_results':{'proof_documents':6,'hash_bound_sections':39,'specialist_review':False,'novelty_claim':False},
 'new_executed_research':{'test_methods':31,'research_test_methods':25,'synthetic_audit_gate_test_methods':6,'modes':['normal','optimised'],
  'assertion_failure_mutation_controls':6,'mutant_discovery_errors':0,'codec_byte_fixtures':6,'rational_flow_fixtures':2,'old_censuses_replayed':False},
 'formal_evidence':{'Lean':'4.19.0 / 6caaee842e94','Lake':'5.0.0-6caaee8','Mathlib':'c44e0c8ee63ca166450922a373c7409c5d26b00b',
  'explicit_theorem_candidates':130,'new_candidates':119,'unchanged_predecessor_candidates':11,'modules':15,'compiled_declarations':0,'declaration_type_readbacks':0,'axiom_audits':0,'olean_artifacts':0,
  'host_status':'HOST_EXECUTION_BLOCKED','actual_runner_exit':127,'formal_source_complete':False,'missing_source_pointer':'FORMAL_COVERAGE.json'},
 'source_custody':{'predecessor_hash_binding_checks':2631,'original_selector_checks':5,'source_sha_and_git_blob_checks':539,'accepted_projection_checks':54,'original_strict_wrapper':'GENUINE_FAIL_PRESERVED'},
 'P03_interface':{'path':'P03_CONSUMER_BINDINGS.json','hash_bound_ordinary_bindings':34,'kernel_verified_bindings':0,'other_packet_new_results_assumed':[]},
 'credit_exclusions':['canonical adoption','repository mutation','Integration DAG action','external review','historical recovery','empirical/world authority','publication','licensing decision','novelty'],
 'output_hashes_scope':'All payload files excluding RECEIPT.json, its detached digest and CHECKPOINT_MANIFEST.json; avoids circularity.',
 'output_hashes':outputs,
 'independent_reopen':'Performed after sealing, recorded in external VERIFICATION.json so the archive is not modified after verification.'}
write('RECEIPT.json',receipt)
(R/'RECEIPT.json.sha256').write_text(sh((R/'RECEIPT.json').read_bytes())+'  RECEIPT.json\n')
rows=[row(p) for p in paths() if p.name!='CHECKPOINT_MANIFEST.json']
# Only the root manifest is excluded; no nested file with that basename is present in this layout.
if any(p.name=='CHECKPOINT_MANIFEST.json' and p.parent!=R for p in paths()):raise ValueError('Unexpected nested manifest')
write('CHECKPOINT_MANIFEST.json',{'schema':'orthemology-p02-attempt2-manifest-v1','files':rows,'file_count':len(rows),'self_member':'CHECKPOINT_MANIFEST.json','self_hash_location':'Detached SEAL.json and outer archive digest','all_other_members_listed':True})
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in paths():
  if p.is_symlink():raise ValueError('Symlink payload')
  n=str(p.relative_to(R));info=zipfile.ZipInfo(n,date_time=(2026,9,23,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
  z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
b=OUT.read_bytes();digest=sh(b)
OUT.with_suffix('.zip.sha256').write_text(digest+'  '+OUT.name+'\n')
with zipfile.ZipFile(OUT) as z:members=len(z.infolist());uncompressed=sum(x.file_size for x in z.infolist())
seal={'archive':OUT.name,'bytes':len(b),'sha256':digest,'zip_members':members,'uncompressed_bytes':uncompressed,
 'manifest':row(R/'CHECKPOINT_MANIFEST.json'),'receipt':row(R/'RECEIPT.json'),
 'independent_verification_file':OUT.with_suffix('.VERIFICATION.json').name,'no_signature_or_external_review_claim':True}
OUT.with_suffix('.SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps(seal,indent=2))
