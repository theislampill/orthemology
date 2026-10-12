#!/usr/bin/env python3
"""Portable packaging/relationship checks; no source-reading or proof authority."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1];P='t20-next-frontier-20261008/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(rel):return json.loads((R/rel).read_text())
def verify(x):
 p=Path(x['path']);assert not p.is_absolute() and '..' not in p.parts
 p=R/p;assert p.is_file() and not p.is_symlink(),str(p)
 assert sha(p)==x['sha256'],str(p)
 assert p.stat().st_size==x['bytes'],str(p)
def pointer(d,p):
 for k in p.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');d=d[int(k)] if isinstance(d,list) else d[k]
 return d
def declaration(x):
 if x['format']=='text_line':
  line=(R/x['record']).read_text().splitlines()[x['locator']-1]
  m=re.fullmatch(r'([0-9a-f]{64})\s+\*?(.+)',line);assert m
  assert m[1]==x['declared_sha256'] and m[2]==x['declared_path']
 else:
  d=pointer(read(x['record']),x['locator'])
  if x['hash_key']=='value':assert d==x['declared_sha256']
  else:
   assert d[x['hash_key']]==x['declared_sha256']
   assert x['declared_path'] in [d.get(k) for k in ['path','file','name','source','result','source_path','local_pdf']]
   if x['declared_bytes'] is not None:assert d['bytes']==x['declared_bytes']
m=read('MANIFEST.json');assert m['schema']=='t20-checkpoint-file-manifest-v1'
assert sha(R/'MANIFEST.json')==(R/'MANIFEST.sha256').read_text().split()[0]
listed={x['path'] for x in m['files']};assert len(listed)==len(m['files'])==m['file_count']
for x in m['files']:verify(x)
assert not any(p.is_symlink() for p in R.rglob('*'))
assert {p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()}==listed|{'MANIFEST.json','MANIFEST.sha256'}
copies=read('PACKING/SOURCE_COPY_BINDINGS.json')
for x in copies:verify(x);assert x['copied_unchanged']
b=read('PACKING/REVIEW_AND_DEPENDENCY_BINDINGS.json');ext={x['path']:x for x in b['external_dependencies']}
assert len(ext)==len(b['external_dependencies'])
for x in ext.values():
 assert not (R/x['path']).exists() and x['included'] is False and x['verification_failure'] is False
 assert not Path(x['path']).is_absolute() and '..' not in Path(x['path']).parts
 assert len(x['sha256'])==64 and isinstance(x['bytes'],int)
for x in b['explicit_bindings']:
 declaration(x);assert x['sha256']==x['declared_sha256']
 if x['declared_bytes'] is not None:assert x['bytes']==x['declared_bytes']
 if x['included']:verify(x)
 else:assert ext[x['path']]['sha256']==x['sha256'] and ext[x['path']]['bytes']==x['bytes']
 if x['status']=='HISTORICAL_BYTES_MATCH_PRESERVED_DRAFT':assert '/history/' in x['path']
 else:assert x['status']=='CURRENT_BYTES_MATCH'
hist=b['historical_declarations_without_bytes'];assert len(hist)==2
expected_hist={'93876913fbd76931f93b21f0d23ef5697facad754cfba284b3aa48fc75ff06eb':23306,'501311d5f2a86d32724f3c451084b01c01791442bd8442f1900658b375484fa2':472}
assert {x['declared_sha256']:x['declared_bytes'] for x in hist}==expected_hist
for x in hist:
 declaration(x);assert x['status']=='HISTORICAL_DECLARATION_ONLY_BYTES_UNAVAILABLE' and x['not_intentional_source_omission'] and x['not_verified_as_current']
 for y in x['current_path_identities']:verify(y);assert y['sha256']!=x['declared_sha256']
ids=read('COMPONENT_AND_PRIOR_IDENTITIES.json');prior=ids['prior_checkpoints'];archives={x['archive_id']:x for x in ids['all_checked_archives']}
assert len(prior)==13 and [x['checkpoint_number'] for x in prior]==list(range(1,14))
assert all(x['included'] is False for x in prior)
assert prior[8]['sha256']=='81089a1bd1497982bf80310d191a6b1019462bcb922b1f2fffbefc696853f1ef'
assert prior[-1]['sha256']=='18a66948e5ae98915c82f7920a869ef93d4e650432925ad1f35279a222cc6db9'
for x in ext.values():
 for a in x['archive_matches']:
  assert archives[a['archive_id']]['sha256']==a['archive_sha256'] and a['member_sha256']==x['sha256']
idx=read('INCREMENTAL_RESULT_SOURCE_EVIDENCE_DEPENDENCY_MANIFEST.json');assert idx['schema']=='t20-incremental-result-source-evidence-dependency-v2' and idx['checkpoint_ordinal']==14
results={x['id']:x for x in idx['results']};assert len(results)==8
expected={
'necessary-concordance-power':('a2023aa4eff3920745e3a2e3c098c9bf13222db6e30c53bf4a674b4cc1266544','FULL_REPORT_INTERNAL_REVIEW'),
'oneness-return-20261009':('21362330512dff0ef5ca9f48a3b8311ab8b0dd952e97d3ae338af0bc2e118b68','ROOT_READING_AND_SEPARATE_RIVAL_AUDIT_NOT_BLANKET_FINAL_REVIEW'),
'original-rival-warrant-audit-20261009':('46c6db37bf86fbe531f877520c0416afc8a5b709ce09d729482c3ff0cd038454','BOUNDED_AUDIT_NO_SEPARATE_FINAL_REPORT_REVIEW'),
'joint-manifestation-ontology':('080d4c2a1c46835d76fcf86345c6536b84eb7b8278855a0a7b4b99cd7b3258c9','INITIAL_REPORT_INTERNAL_REVIEW_PLUS_FINAL_DELTA_READBACK'),
'modal-psr-bridge':('01dce257466aaa678520fe87d43e2cf08a2bb0f15e36c6020d4c6fd86e7759d6','H_P_LEMMA_ONLY_INTERNAL_REVIEW'),
'particular-reasons-comparison':('fc29f0403f42aec87c48455d7b078b4653dd13736fa7895c65d1060bd77e2080','AUTHOR_REPORT_AND_ROOT_TARGETED_RETURN_NO_SEPARATE_FINAL_REVIEW'),
'complete-overdetermination-audit':('0dc3642ac0c17b614fa87c8b513f6f9008272861693139b26b9c92893c276f08','SEPARATE_BOUNDED_ISSUE_REVIEW_NOT_DIGEST_ACCEPTANCE_OF_FINAL_REPORT'),
'creator-uniqueness-bridge':('c81a634310e6f7696645f02e9ee885215e57f87919c0d965cf4c746e2a5f2408','AUTHOR_REPORT_NO_SEPARATE_FINAL_REVIEW')}
assert set(results)==set(expected)
for k,r in results.items():
 verify(r['author']);assert (r['author']['sha256'],r['internal_review_scope'])==expected[k]
 for x in r['review_records']+r['evidence_records']:verify(x)
 assert r['new_kernel_or_empirical_credit'] is False
r=read(P+'joint-manifestation-ontology-review/FINAL_READBACK.json')
verify(r['final_result']|{'bytes':21513});verify(r['prior_result']|{'bytes':20557});assert not r['blocking_findings'] and r['R1_resolved'] and r['R2_resolved']
assert sha(R/P/'necessary-concordance-power-review/reviewed_RESULT.md')==results['necessary-concordance-power']['author']['sha256']
for x in idx['sources']:verify(x['receipt']);assert x['fresh_credit_from_archive_assembly'] is False
u=idx['unavailable_source_work'];assert u['status']=='ABSTRACT_AND_METADATA_ONLY; FULL_BODY_UNAVAILABLE' and u['no_unanswered_objection_inference'];verify(u['receipt'])
bounds=read('EVIDENCE_BOUNDARIES.json');assert bounds==idx['boundaries']
assert bounds['checkpoint_ordinal']==14 and bounds['T20_status']=='ACTIVE' and bounds['historical_six_hour_active_compliance']=='UNVERIFIED'
for k in ['owner_acceptance','final_integration','closure','new_source_reading_credit','new_lean_execution','new_empirical_verification','prior_science_rerun','prior_archives_mutated']:assert bounds[k] is False
assert bounds['new_research_duration_credit_seconds']==0 and set(bounds['membership_cutoff'])==set(expected)
assert 'epistemic-psr-warrant' in bounds['excluded_active_or_later']
state=idx['root_state'];assert state==bounds['current_root_judgement']
verify(state['latest']);verify(state['historical_positive_judgement']);verify(state['historical_frontier_record'])
assert state['latest']['sha256']=='4f982bebd1c4add817a93a1445407a31374dc9f42d056e987bb14f816f17d9d1'
assert state['historical_positive_judgement']['sha256']=='0df98323e518afcd9f0ad040f27d87b4c12293385def29f741013c4199038eb8'
assert state['latest_status']=='PROVISIONAL_PREFERENCE_ONE_ACTUAL_COMMON_CREATOR_WITH_JUDGEMENT_WITHHELD_ON_UNIVERSAL_EXCLUSION'
assert state['earlier_not_silently_renewed'] and state['no_full_metaphysical_plural_original_countermodel'] and state['no_universal_nonduplication_theorem']
om=read('OMISSIONS_AND_SOURCE_LINKS.json');assert om['omission_is_verification_failure'] is False
for x in om['intentional_source_body_omissions']:assert x['path'] in ext and x['verification_failure'] is False and x['sha256']==ext[x['path']]['sha256']
assert not any(Path(p).suffix.lower() in {'.pdf','.png','.jpg','.html','.zip','.lean','.olean','.ilean','.pyc'} for p in listed)
assert not any('/epistemic-psr-warrant/' in p for p in listed)
assert all(p.startswith('PACKING/') for p in listed if p.endswith('.py'))
assert all(p.endswith('/sources/retrieval-status-gale-pruss-reply-oppy-lca.txt') for p in listed if '/sources/' in p)
print(json.dumps({'status':'PASS','payload_files':len(listed),'unchanged_source_copies':len(copies),'explicit_binding_rows':len(b['explicit_bindings']),'historical_unavailable_revisions':len(hist),'external_provenance_dependencies':len(ext),'prior_numbered_checkpoints':13,'all_prior_archives':len(archives),'result_components':8,'research_or_source_reading_credit':False},indent=2))
