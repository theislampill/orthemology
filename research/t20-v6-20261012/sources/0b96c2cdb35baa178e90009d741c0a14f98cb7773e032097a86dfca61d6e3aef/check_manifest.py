#!/usr/bin/env python3
"""Read-only exact inventory, source-copy, author-review and dependency validation."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
P='t20-next-frontier-20261008/'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(rel): return json.loads((ROOT/rel).read_text())
def verify(row):
    rel=Path(row['path']); assert not rel.is_absolute() and '..' not in rel.parts,row
    p=ROOT/rel; assert p.is_file() and not p.is_symlink(),str(rel)
    assert sha(p)==row['sha256'],str(rel)
    if 'bytes' in row: assert p.stat().st_size==row['bytes'],str(rel)
def path_digest(rel,digest):
    if (ROOT/(P+rel)).is_file(): assert sha(ROOT/(P+rel))==digest,rel
    else: assert rel in external and external[rel]['sha256']==digest,rel
manifest=read('MANIFEST.json')
assert sha(ROOT/'MANIFEST.json')==(ROOT/'MANIFEST.sha256').read_text().split()[0]
rows=manifest['files']; assert len(rows)==manifest['file_count']
listed=[r['path'] for r in rows]; assert len(listed)==len(set(listed))
for row in rows: verify(row)
assert not any(p.is_symlink() for p in ROOT.rglob('*'))
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
assert actual==set(listed)|{'MANIFEST.json','MANIFEST.sha256'}
copies=read('PACKING/SOURCE_COPY_BINDINGS.json')
for row in copies: verify(row)
bindings=read('PACKING/REVIEW_AND_DEPENDENCY_BINDINGS.json')
external={r['origin_relative_to_research_root']:r for r in bindings['external_predecessor_bindings']}
prior=read('COMPONENT_AND_PRIOR_IDENTITIES.json')['prior_checkpoints']
assert len(prior)==10 and all(r['included'] is False for r in prior)
prior_by_sha={r['sha256']:r for r in prior}
assert prior[8]['sha256']=='81089a1bd1497982bf80310d191a6b1019462bcb922b1f2fffbefc696853f1ef'
assert prior[9]['sha256']=='a9f2a64c0ac30324c40993ca2a7e3d995858af3242226d7091e50d251acd622a'
for row in external.values():
    assert not (ROOT/row['path']).exists()
    assert row['verified_against']=='EXACT_ARCHIVE_MEMBER'
    assert row['predecessor_archive_sha256'] in prior_by_sha
    assert row['archive_member'].endswith('/'+row['path'])
for row in bindings['included_current_bindings']: verify(row)
# Every source-binding record is checked independently of the consolidated map.
for component in ['skyline-likelihood-score-review','full-skyline-reverse-kl-review','full-skyline-log-squared-review']:
    data=read(P+component+'/SOURCE_BINDINGS.json')
    for row in data.get('files',data.get('sources',[])):
        rel=row['path'][3:] if row['path'].startswith('../') else row['path']
        path_digest(rel,row['sha256'])
for component in ['full-skyline-reverse-kl','full-skyline-log-squared']:
    for row in read(P+component+'/SOURCE_BINDINGS.json')['sources']:
        assert row['path'].startswith('../'); path_digest(row['path'][3:],row['sha256'])
for rel,digest in read(P+'baseline-skyline-moments-review/CHECK_RESULTS.json')['source_digests'].items(): path_digest(rel,digest)
source_review=read(P+'skyline-probability-prior-art-review/VERIFICATION_MANIFEST.json')
assert source_review['verdict']=='PASS_WITHIN_STATED_SCOPE' and not source_review['blocking_findings']
for name,digest in source_review['author_files_sha256'].items(): path_digest('skyline-probability-prior-art/'+name,digest)
for rel,digest in source_review['dependency_files_sha256'].items(): path_digest(rel,digest)
for name,digest in source_review['review_files_sha256'].items(): path_digest('skyline-probability-prior-art-review/'+name,digest)
# Native author/reviewer file manifests and sum lists are preserved and checked.
native_manifest_count=0
for component in bindings['components']:
    p=ROOT/P/component/'MANIFEST.json'
    if p.exists():
        data=json.loads(p.read_text()); records=data.get('files',data.get('artifacts'))
        if isinstance(records,dict): records=[{'path':rel,'sha256':digest} for rel,digest in records.items()]
        for row in records: verify(row|{'path':P+component+'/'+row['path']})
        native_manifest_count+=1
    p=ROOT/P/component/'SHA256SUMS'
    if p.exists():
        for line in p.read_text().splitlines():
            digest,name=line.split(maxsplit=1)
            rel=name if name.startswith(component+'/') else component+'/'+name
            path_digest(rel,digest)
        native_manifest_count+=1
accepted=bindings['accepted_results']; assert len(accepted)==5
for row in accepted:
    verify(row['author']); verify(row['review']); verify(row['binding_record'])
    assert row['author']['sha256'] in (ROOT/row['review']['path']).read_text(),row['id']
    assert row['author']['sha256'] in (ROOT/row['binding_record']['path']).read_text(),row['id']
    assert row['status']=='PASS_WRITTEN_PROOF_WITH_SCOPED_INTERNAL_REVIEW'
for component in ['skyline-likelihood-score-review','full-skyline-reverse-kl-review','full-skyline-log-squared-review']:
    receipt=read(P+component+'/REVIEW_RECEIPT.json'); author=component.removesuffix('-review')
    assert receipt['result']=='PASS' and not receipt['blocking_findings']
    assert receipt['review_sha256']==sha(ROOT/P/component/'REVIEW.md')
    assert receipt['accepted_author_result_sha256']==sha(ROOT/P/author/'RESULT.md')
    verification=read(P+component+'/VERIFICATION.json'); assert verification['status']=='PASS'
    assert verification['accepted_author_result_sha256']==receipt['accepted_author_result_sha256']
    assert verification['review_sha256']==receipt['review_sha256']
for row in bindings['duplicate_replay_sources']:
    verify(row['copy']); verify(row['original']); assert row['copy']['sha256']==row['original']['sha256']
idx=read('INCREMENTAL_RESULT_SOURCE_EVIDENCE_DEPENDENCY_MANIFEST.json')
assert len(idx['results'])==5 and idx['kernel_status']=='NO_NEW_LEAN_THEOREMS_OR_REPLAYS'
controls=read('PACKING/CONTROL_PLAN.json')['commands']; assert len(controls)==11
ids={r['id'] for r in idx['results']}|set(idx['external_dependency_registry']); control_ids={r['id'] for r in controls}
for row in idx['results']:
    for a in row['artifacts']+row['separate_internal_review']: verify(a)
    assert set(row['depends_on'])<=ids
    assert set(row['control_ids'])<=control_ids
    assert set(row['source_ids'])<=set(idx['source_registry'])
for row in idx['source_registry'].values():
    for a in row['records']: verify(a)
for row in controls: verify({'path':row['script'],'sha256':row['script_sha256']})
programs={p for p in listed if p.endswith('.py') and not p.startswith('PACKING/')}
assert programs=={r['script'] for r in controls}|{r['copy']['path'] for r in bindings['duplicate_replay_sources'] if r['copy']['path'].endswith('.py')}
assert not any(Path(p).suffix.lower() in {'.pdf','.png','.jpg','.jpeg','.html','.pyc','.olean','.ilean','.zip'} for p in listed)
assert not any('/__pycache__/' in p or '/sharp-skyline-information' in p for p in listed)
print(json.dumps({'status':'PASS','payload_files':len(rows),'unchanged_source_copies':len(copies),'bound_author_review_pairs':len(accepted),'native_manifests_or_sum_lists':native_manifest_count,'declared_control_runs':len(controls),'external_predecessor_members':len(external),'prior_archive_references':len(prior),'kernel_replay':'NOT_APPLICABLE_NO_NEW_LEAN','source_body_checks':'NOT_RERUN_SOURCE_BODIES_OMITTED','scope':'Exact frozen artifact identity and declared author-review/dependency bindings; not a new proof or source-reading certification.'},indent=2))
