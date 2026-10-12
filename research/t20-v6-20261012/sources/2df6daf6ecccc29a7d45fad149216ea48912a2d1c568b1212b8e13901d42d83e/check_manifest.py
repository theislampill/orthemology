#!/usr/bin/env python3
"""Portable hash, inventory and declared-binding checker. No metaphysical authority."""
from pathlib import Path
import hashlib,json,posixpath
R=Path(__file__).resolve().parents[1]; P='t20-next-frontier-20261008/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((R/p).read_text())
def verify(x):
 p=Path(x['path']);assert not p.is_absolute() and '..' not in p.parts
 p=R/p;assert p.is_file() and not p.is_symlink(),str(p)
 assert sha(p)==x['sha256'],str(p)
 if 'bytes' in x:assert p.stat().st_size==x['bytes']
def pointer(obj,p):
 for k in p.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');obj=obj[int(k)] if isinstance(obj,list) else obj[k]
 return obj
m=read('MANIFEST.json');assert sha(R/'MANIFEST.json')==(R/'MANIFEST.sha256').read_text().split()[0]
listed={x['path'] for x in m['files']};assert len(listed)==len(m['files'])==m['file_count']
for x in m['files']:verify(x)
assert not any(p.is_symlink() for p in R.rglob('*'))
actual={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()}
assert actual==listed|{'MANIFEST.json','MANIFEST.sha256'}
for x in read('PACKING/SOURCE_COPY_BINDINGS.json'):verify(x)
b=read('PACKING/REVIEW_AND_DEPENDENCY_BINDINGS.json');ext={x['path']:x for x in b['external_retained_dependencies']}
assert len(ext)==len(b['external_retained_dependencies'])
for x in ext.values():assert not (R/x['path']).exists() and x['included'] is False
for x in b['explicit_path_hash_rows']:
 obj=pointer(read(x['record']),x['json_pointer'])
 if isinstance(obj,str):assert obj==x['sha256']
 else:
  assert obj['sha256']==x['sha256']
  if 'bytes' in obj:assert obj['bytes']==x['bytes']
  raw=obj.get('path',obj.get('source_path',obj.get('local_pdf')))
  if raw is not None:assert raw==x['declared_path']
 target=x['path'];raw=x['declared_path']
 norm=raw.removeprefix('private-locator:45fe10b770ecaeaedfcf')
 candidates={posixpath.normpath(norm),posixpath.normpath(posixpath.dirname(x['record'])+'/'+norm),posixpath.normpath(P+norm)}
 assert target in candidates,(target,raw)
 if x['included']:verify(x)
 else:assert ext[target]['sha256']==x['sha256'] and ext[target]['bytes']==x['bytes']
prior=read('COMPONENT_AND_PRIOR_IDENTITIES.json')['prior_checkpoints']
assert len(prior)==12 and [x['checkpoint_number'] for x in prior]==list(range(1,13))
assert all(x['included'] is False for x in prior)
assert prior[8]['sha256']=='81089a1bd1497982bf80310d191a6b1019462bcb922b1f2fffbefc696853f1ef'
assert prior[-1]['sha256']=='8f2d12eaf5219a8b84df921ab2e917580ebf10f7a724079bde60587fa78c1801'
for x in ext.values():
 for a in x['archive_matches']:
  q=prior[a['checkpoint_number']-1];assert a['archive_sha256']==q['sha256']
  assert a['archive_member'].endswith('/'+x['path'])
idx=read('INCREMENTAL_RESULT_SOURCE_EVIDENCE_DEPENDENCY_MANIFEST.json');assert idx['checkpoint_ordinal']==13
assert len(idx['results'])==6
for r in idx['results']:
 for k in ['author','review','acceptance_record']:verify(r[k])
 for k in ['source_and_input_records','separate_review_records']:
  for x in r[k]:verify(x)
 text='\n'.join((R/x['path']).read_text() for x in r['separate_review_records'] if Path(x['path']).suffix in {'.md','.json'})
 assert r['author']['sha256'] in text
byid={r['id']:r for r in idx['results']}
expected_stages={'modal-identity-transport','modal-grounding-source','wise-determination-continuation','collective-explanation-adequacy','de-se-sovereignty','de-se-perfection-sources'}
assert set(byid)==expected_stages
for stage,row in byid.items():
 expected_review=P+stage+('/review/RELATIONAL_PERFECTION_TRANSPORT.md' if stage=='wise-determination-continuation' else '-review/REVIEW.md')
 assert row['review']['path']==expected_review

def result(stage):return byid[stage]['author']['sha256']
r=read(P+'modal-identity-transport/REVIEW_RECEIPT.json');assert r['status']=='PASS' and r['unresolved_findings']==0 and r['report_sha256']==result('modal-identity-transport')
r=read(P+'modal-grounding-source-review/REVIEW_RECEIPT.json');assert not r['blocking_findings'] and r['all_input_bindings_rechecked'] and r['all_five_frozen_author_snapshots_equal_current']
for f in ['REPORT.md','MAPPING_TEST.md','MANIFEST.json','READING_LEDGER.json','SOURCE_EXTRACTION_CHECK.json']:
 assert sha(R/P/'modal-grounding-source'/f)==sha(R/P/'modal-grounding-source-review/input-snapshot'/f)
r=read(P+'wise-determination-continuation/VERIFICATION.json');assert r['all_checks_passed'] and r['report_sha256']==result('wise-determination-continuation')
assert result('wise-determination-continuation') in (R/P/'wise-determination-continuation/review/RELATIONAL_PERFECTION_TRANSPORT.md').read_text()
r=read(P+'collective-explanation-adequacy-review/VERIFICATION.json');assert r['verdict']=='PASS_WITH_NONBLOCKING_PRECISION_GUARDS' and r['blocking_findings']==0
r=read(P+'de-se-sovereignty/REVIEW_STATUS.json');assert r['accepted_result_sha256']==result('de-se-sovereignty') and r['review_report_sha256']==sha(R/P/'de-se-sovereignty-review/REVIEW.md')
assert result('de-se-sovereignty')=='e1e958cafbc550ee457ba21ceb98512dee56deda34bf6a2e506bd887950c5a8d'
assert sha(R/P/'de-se-sovereignty-review/reviewed_RESULT.final.md')==result('de-se-sovereignty')
assert sha(R/P/'de-se-sovereignty/history/RESULT-before-basing-clarification.md')==sha(R/P/'de-se-sovereignty-review/reviewed_RESULT.initial.md')=='b67a08c6750baa1b2bfb81e9b79bbd5ceb81e7a36e711c30decb86b93293aa91'
r=read(P+'de-se-perfection-sources-review/VERIFICATION.json');assert r['report_sha256']==result('de-se-perfection-sources') and r['all_bound_inputs_unchanged'] and r['final_input_count']==38
assert r['author_manifest_sha256']==sha(R/P/'de-se-perfection-sources/MANIFEST.json')
assert result('de-se-perfection-sources')=='38b5e3966106994a033b07005787ea135cef5195df75fbec366c8e24b73e435b'
auth=read('PACKING/FINAL_REVIEW_AUTHORIZATION.json')
for x in auth['files']:verify(x|{'path':P+x['path']})
for x in idx['separately_classified_notes']:assert x['classification']=='ALLOCATION_OR_TARGETED_SOURCE_SCOPE_NOTE_NOT_PROOF_CREDIT';verify(x)
plan=read('PACKING/CONTROL_PLAN.json');assert len(plan['commands'])==2
for x in plan['commands']:verify({'path':x['script'],'sha256':x['script_sha256']})
programs={x for x in listed if x.endswith('.py') and not x.startswith('PACKING/')}
assert programs=={x['script'] for x in plan['commands']}|{x['path'] for x in plan['preserved_not_replayed']}
assert sha(R/P/'modal-identity-transport/controls.py')==sha(R/P/'modal-identity-transport-review/author_controls_snapshot.py')
assert sha(R/P/'modal-identity-transport/CONTROL_RESULTS.json')==sha(R/P/'modal-identity-transport-review/AUTHOR_REPLAY.json')
assert not any(Path(x).suffix.lower() in {'.pdf','.png','.jpg','.html','.zip','.pyc','.olean','.ilean'} for x in listed)
assert not any('/necessary-concordance-power/' in x for x in listed)
bounds=read('EVIDENCE_BOUNDARIES.json');assert bounds['checkpoint_ordinal']==13 and bounds['T20_status']=='ACTIVE' and bounds['historical_six_hour_active_compliance']=='UNVERIFIED'
assert bounds['de_se_basing']=='Action-guiding epistemic basing explicitly NOT established by inherited policy code.'
assert 'necessary-concordance-power' in bounds['excluded_active_or_later']
assert set(bounds['membership_cutoff'])==expected_stages
assert bounds['research_duration_credit_seconds']==0 and bounds['source_claim_limit']==idx['scope']['source_claim_limit']
print(json.dumps({'status':'PASS','payload_files':len(listed),'source_copies':len(read('PACKING/SOURCE_COPY_BINDINGS.json')),'explicit_path_hash_bindings':len(b['explicit_path_hash_rows']),'external_retained_dependencies':len(ext),'prior_archives':12,'accepted_stages':6,'separately_classified_notes':len(idx['separately_classified_notes']),'fresh_control_commands':2,'source_reading_and_metaphysical_certification':False},indent=2))
