#!/usr/bin/env python3
"""Check delivered bytes and included original bindings, with explicit omissions."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(row):
 p=ROOT/row['path'];assert p.is_file(),row['path'];assert sha(p)==row['sha256'],row['path']
 if 'bytes' in row:assert p.stat().st_size==row['bytes'],row['path']
m=json.loads((ROOT/'MANIFEST.json').read_text())
assert (ROOT/'MANIFEST.sha256').read_text().split()[0]==sha(ROOT/'MANIFEST.json')
assert len(m['files'])==m['file_count']
seen=set()
for row in m['files']:
 p=Path(row['path']);assert not p.is_absolute() and '..' not in p.parts and row['path'] not in seen;seen.add(row['path']);verify(row)
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
assert actual==seen|{'MANIFEST.json','MANIFEST.sha256'},actual^seen
copies=json.loads((ROOT/'PACKING/SOURCE_COPY_BINDINGS.json').read_text())
for row in copies:verify(row)
bound=json.loads((ROOT/'PACKING/ORIGINAL_AND_REVIEW_BINDING_CHECKS.json').read_text())
n=0
for row in bound['entries']:
 if row['inclusion']=='INCLUDED_UNCHANGED':verify({**row,'path':row['source_path']});n+=1
 else:assert not (ROOT/row['source_path']).exists(),row['source_path']
index=json.loads((ROOT/'INCREMENTAL_RESULT_SOURCE_EVIDENCE_DEPENDENCY_MANIFEST.json').read_text())
for row in index['results']:
 for x in row['artifacts']+row['separate_internal_review']:verify(x)

for candidate in index['candidate_history']:verify(candidate['artifact'])
ids={r['id'] for r in index['results']}|set(index['external_dependency_registry'])
for row in index['results']:assert set(row['depends_on'])<=ids

for row in json.loads((ROOT/'PACKING/CONTROL_PLAN.json').read_text())['commands']:verify({'path':row['script'],'sha256':row['script_sha256']})
print(json.dumps({'status':'PASS','payload_files':len(seen),'unchanged_source_copies':len(copies),'included_original_bindings':n,'external_or_omitted_binding_only_entries':len(bound['entries'])-n,'whole_original_verifiers_replayed':False,'scope':'File integrity and included bindings only; explicit omitted-source full-verifier boundaries remain.'},indent=2))
