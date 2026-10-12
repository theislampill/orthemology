#!/usr/bin/env python3
"""Check delivered bytes and included bindings; never substitute for omitted-source replay."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(row):
 rel=Path(row['path']);assert not rel.is_absolute() and '..' not in rel.parts,row
 p=ROOT/rel;assert p.is_file(),row['path'];assert sha(p)==row['sha256'],row['path']
 if 'bytes' in row:assert p.stat().st_size==row['bytes'],row['path']
m=json.loads((ROOT/'MANIFEST.json').read_text())
assert (ROOT/'MANIFEST.sha256').read_text().split()[0]==sha(ROOT/'MANIFEST.json')
assert len(m['files'])==m['file_count']
seen=set()
for row in m['files']:
 assert row['path'] not in seen;seen.add(row['path']);verify(row)
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
assert actual==seen|{'MANIFEST.json','MANIFEST.sha256'},actual^seen
copies=json.loads((ROOT/'PACKING/SOURCE_COPY_BINDINGS.json').read_text())
for row in copies:verify(row)
bound=json.loads((ROOT/'PACKING/ORIGINAL_AND_REVIEW_BINDING_CHECKS.json').read_text());n=0
for row in bound['entries']:
 if row['inclusion']=='INCLUDED_UNCHANGED':verify({**row,'path':row['source_path']});n+=1
 else:
  assert row['inclusion']=='NOT_INCLUDED_BINDING_ONLY'
  if not Path(row['source_path']).is_absolute():assert not (ROOT/row['source_path']).exists(),row['source_path']
index=json.loads((ROOT/'INCREMENTAL_RESULT_SOURCE_EVIDENCE_DEPENDENCY_MANIFEST.json').read_text())
for row in index['results']:
 for x in row['artifacts']+row['separate_internal_review']:verify(x)
for row in index['source_registry'].values():
 for x in row['records']:verify(x)
for row in index['external_dependency_registry'].values():
 for x in row.get('artifacts',[]):verify(x)
 if row.get('sha256'):verify(row)
for row in index['reading_scope_records']:verify(row['artifact'])
ids={r['id'] for r in index['results']}|set(index['external_dependency_registry'])
controls=json.loads((ROOT/'PACKING/CONTROL_PLAN.json').read_text())['commands'];control_ids={r['id'] for r in controls}
for row in index['results']:
 assert set(row['depends_on'])<=ids
 assert set(row['source_ids'])<=set(index['source_registry'])
 assert set(row['control_ids'])<=control_ids
for row in controls:verify({'path':row['script'],'sha256':row['script_sha256']})
# Only declared current-stage runnable programs, a duplicate snapshot, and one explicitly omitted-input extraction helper.
programs={p for p in seen if p.endswith('.py') and not p.startswith('PACKING/')}
expected={r['script'] for r in controls}|{'t20-next-frontier-20261008/existential-law-source-bridge/sources/extract_received.py'}
assert programs==expected,(programs-expected,expected-programs)
assert len(m['previous_checkpoints'])==7
assert not any('/full-face-threshold-information/' in p or p.endswith('/FULL_THRESHOLD_INFORMATION_CANDIDATE.md') for p in seen)
assert not any(Path(p).suffix.lower() in ['.pdf','.png','.jpg','.jpeg','.html','.pyc','.olean','.ilean'] for p in seen)
assert not any('/source-images/' in p or '/sources/' in p and Path(p).suffix in ['.txt','.pdf','.html'] for p in seen)
print(json.dumps({'status':'PASS','payload_files':len(seen),'unchanged_source_copies':len(copies),'included_original_bindings':n,'external_or_omitted_binding_only_entries':len(bound['entries'])-n,'declared_control_runs':len(controls),'distinct_program_contents':len({r['script_sha256'] for r in controls}),'source_body_verifiers':'UNREPLAYED','scope':'File integrity, declared dependency links and included bindings only; omitted-source, proof and interpretation boundaries remain.'},indent=2))
