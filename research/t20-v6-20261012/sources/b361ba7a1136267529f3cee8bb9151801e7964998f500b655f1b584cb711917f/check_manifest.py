#!/usr/bin/env python3
"""Portable fifteenth checkpoint integrity and exact relationship verification."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1];ROOT='t20-next-frontier-20261008/root-later-operations/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(rel):return json.loads((R/rel).read_text())
def verify(x):
 p=Path(x['path']);assert not p.is_absolute() and '..' not in p.parts
 p=R/p;assert p.is_file() and not p.is_symlink(),str(p)
 assert sha(p)==x['sha256'] and p.stat().st_size==x['bytes'],str(p)
def pointer(d,p):
 for k in p.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');d=d[int(k)] if isinstance(d,list) else d[k]
 return d
def declaration(x):
 if x['format']=='text_line':
  line=(R/x['record']).read_text().splitlines()[x['locator']-1];m=re.fullmatch(r'([0-9a-f]{64})\s+\*?(.+)',line)
  assert m and m[1]==x['declared_sha256'] and m[2]==x['declared_path']
 else:
  d=pointer(read(x['record']),x['locator'])
  if x['format']=='json_value':assert d==x['declared_sha256']
  else:
   assert d[x['hash_key']]==x['declared_sha256']
   if x['format']=='acquisition_html':assert d['name']+'.html'==x['declared_path']
   elif x['format']!='hash_only':assert d[x['path_key']]==x['declared_path']
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
assert len(ext)==len(b['external_dependencies']) and b['historical_declarations_without_bytes']==[]
for x in ext.values():
 assert not (R/x['path']).exists() and x['included'] is False and x['verification_failure'] is False
 assert not Path(x['path']).is_absolute() and '..' not in Path(x['path']).parts
for x in b['explicit_bindings']:
 declaration(x);assert x['sha256']==x['declared_sha256']
 if x['declared_bytes'] is not None:assert x['bytes']==x['declared_bytes']
 if x['included']:verify(x)
 else:assert ext[x['path']]['sha256']==x['sha256'] and ext[x['path']]['bytes']==x['bytes']
 assert x['status'] in ['CURRENT_BYTES_MATCH','EXACT_PRESERVED_HISTORICAL_BYTES']
limits=b['inherited_predecessor_revision_limits'];assert {x['declared_sha256'] for x in limits}=={'93876913fbd76931f93b21f0d23ef5697facad754cfba284b3aa48fc75ff06eb','501311d5f2a86d32724f3c451084b01c01791442bd8442f1900658b375484fa2'}
ids=read('COMPONENT_AND_PRIOR_IDENTITIES.json');prior=ids['prior_checkpoints'];archives={x['archive_id']:x for x in ids['all_checked_archives']}
assert len(prior)==14 and [x['checkpoint_number'] for x in prior]==list(range(1,15))
assert all(x['included'] is False for x in prior)
assert prior[-1]['sha256']=='ca9c0b7b471593dbde65a642c694f2c40b3cd5ea9f81052d7bc0901699a6b31c'
assert ids['direct_predecessor']==prior[-1]
assert len(archives)==25
for x in b['inherited_member_bindings']:
 for a in x['archive_matches']:
  assert archives[a['archive_id']]['sha256']==a['archive_sha256'] and a['member_sha256']==x['sha256'] and a['member_bytes']==x['bytes']
idx=read('INCREMENTAL_RESULT_SOURCE_EVIDENCE_DEPENDENCY_MANIFEST.json');assert idx['checkpoint_ordinal']==15
results={x['id']:x for x in idx['results']}
expected={'epistemic-psr-warrant':'d2a195ebb48d41af23938e1b963180383930371fb6cd90c31900e7e40db14c59','plural-explanation-theorem-audit':'e1a2311dd76a5d18e121a02974de3a28cdccee957d8b120c567e481e129f7e79','particular-explanans-bridge-audit':'7f347b80c097ecb4c71a361b0128ad39fa0fb41ceb6c84374c1e8924b100761c','explanation-bridge-review':'76f6b4f4328bea5750217072ad0ca5e6b35e928d8cd6a9682b2b43b629d52fd1','source-noncirculation-feedback':'5c27711184ba09865011d77573cc8cca8c2195755f443117bf66044fbb209b13'}
assert set(results)==set(expected)
for c,row in results.items():
 verify(row['author']);assert row['author']['sha256']==expected[c]
 for v in row['evidence_records']:verify(v)
 assert row['new_research_credit_from_preservation'] is False
assert results['explanation-bridge-review']['internal_review_scope']=='INTERNAL_REVIEW_NOT_EXTERNAL_VALIDATION'
fa=read('explanation-bridge-review/FINAL_HASH_ACCEPTANCE.json');assert fa['accepted']
assert sha(R/fa['previous_result_path'])==fa['previous_result_sha256']=='3dedbeef25eed122342ae46f82a09e17a36719a52126d3169f3c13125b7d37d6'
assert sha(R/fa['final_result_path'])==fa['final_result_sha256']==expected['particular-explanans-bridge-audit']
assert sha(R/'explanation-bridge-review/REVIEW.md')==fa['original_review_preserved_sha256']
assert sha(R/'explanation-bridge-review/INPUTS.json')==fa['original_input_record_preserved_sha256']
old=(R/fa['previous_result_path']).read_text();new=(R/fa['final_result_path']).read_text()
assert new.replace(fa['only_change']+'\n\n','',1)==old,'Final review delta is not exact'
for x in read('explanation-bridge-review/INPUTS.json')['files']:
 if x['path']=='particular-explanans-bridge-audit/RESULT.md':verify(x|{'path':fa['previous_result_path']})
 else:verify(x)
completion=read('epistemic-psr-warrant/READING_COMPLETION_LEDGER.json')
assert sha(R/'epistemic-psr-warrant/READING_LEDGER.json')==completion['initial_ledger_preserved']['sha256']=='f1d6b069549808b3811b73ab8c2af27f77311a23828dee71d687a2537fdb1787'
root_replay=read(ROOT+'PLURAL_EXPLANATION_ROOT_REPLAY_20261009.json')
assert len(root_replay['checks'])==4
for x in root_replay['checks']:assert sha(R/x['file'])==x['sha256'] and x['exit_code']==0
for row in read('source-noncirculation-feedback/SOURCE_READS.json')['records']:
 for s in row['read_selections']:
  p=R/s['selection_path'];assert sha(p)==s['selection_sha256']
  if (R/row['path']).is_file():
   first,last=s['one_based_physical_lines'];assert p.read_text()==''.join((R/row['path']).read_text().splitlines(keepends=True)[first-1:last])
bounds=read('EVIDENCE_BOUNDARIES.json');assert bounds==idx['boundaries']
assert bounds['checkpoint_ordinal']==15 and bounds['T20_status']=='ACTIVE' and bounds['historical_six_hour_active_compliance']=='UNVERIFIED'
for k in ['owner_acceptance','final_integration','closure','new_source_reading_credit','new_proof_development','historical_proofs_rerun','toolchain_bundled_or_rebuilt','prior_archives_mutated','actual_necessary_being_or_uniqueness_proved']:assert bounds[k] is False
assert bounds['package_qualification_fresh_lean_replays']==4 and bounds['new_research_duration_credit_seconds']==0
assert bounds['internal_review_not_external_validation'] is True and bounds['regular_open_realization']=='WRITTEN_ONLY'
assert bounds['weakened_controls']=='BOTH_TRANSITIVITY_CLAUSES_AND_OUTPUT_DISTRIBUTIVITY_DROPPED'
assert bounds['general_E_parthood_BNF_productive_transports']=='OPEN'
assert bounds['repairs']=='SUFFICIENT_NOT_PROVED_NECESSARY_UNIQUE_OR_WEAKEST; wholly particular constituents required'
state=idx['root_state'];assert state==bounds['current_root_judgement']
for k in ['latest','historical_positive_judgement','historical_frontier_record']:verify(state[k])
assert state['latest']['sha256']=='4f982bebd1c4add817a93a1445407a31374dc9f42d056e987bb14f816f17d9d1'
assert state['latest_status']=='PROVISIONAL_PREFERENCE_ONE_ACTUAL_COMMON_CREATOR_WITH_JUDGEMENT_WITHHELD_ON_UNIVERSAL_EXCLUSION'
assert state['anti_bootstrap_does_not_settle_redundant_originals']
for x in idx['root_receipts']:verify(x)
for x in idx['sources']:
 for f in x.get('scope_records',[]):verify(f)
 if 'witness' in x:verify(x['witness']);assert x['license']=='CC BY 4.0'
om=read('OMISSIONS_AND_SOURCE_LINKS.json');assert om['omission_is_verification_failure'] is False
for x in om['intentional_source_body_omissions']:assert x['path'] in ext and x['sha256']==ext[x['path']]['sha256'] and x['verification_failure'] is False
assert len(om['unavailable_source_bodies'])==3
assert not any(Path(p).suffix.lower() in {'.pdf','.png','.jpg','.html','.zip','.olean','.ilean','.pyc'} for p in listed)
assert [p for p in sorted(listed) if p.startswith('epistemic-psr-warrant/sources/')]==['epistemic-psr-warrant/sources/koons-pruss2020-web-continuous.txt']
assert len([p for p in listed if p.endswith('.lean')])==4
print(json.dumps({'status':'PASS','payload_files':len(listed),'unchanged_source_copies':len(copies),'explicit_binding_rows':len(b['explicit_bindings']),'current_unresolved_historical_revisions':0,'inherited_checkpoint14_revision_limits':2,'external_provenance_dependencies':len(ext),'prior_numbered_checkpoints':14,'all_prior_archives':len(archives),'result_and_review_components':5,'historical_exact_mappings':sum(x['status']=='EXACT_PRESERVED_HISTORICAL_BYTES' for x in b['explicit_bindings']),'research_or_source_reading_credit':False},indent=2))
