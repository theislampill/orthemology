#!/usr/bin/env python3
"""Verify sealed payload bytes and declared current result/source/review relationships."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(r):
 rel=Path(r['path']);assert not rel.is_absolute() and '..' not in rel.parts,r
 p=ROOT/rel;assert p.is_file() and not p.is_symlink(),rel;assert sha(p)==r['sha256'],rel
 if 'bytes' in r:assert p.stat().st_size==r['bytes'],rel
m=json.loads((ROOT/'MANIFEST.json').read_text());assert (ROOT/'MANIFEST.sha256').read_text().split()[0]==sha(ROOT/'MANIFEST.json')
assert len(m['files'])==m['file_count'];seen=set()
for r in m['files']:assert r['path'] not in seen;seen.add(r['path']);verify(r)
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
assert actual==seen|{'MANIFEST.json','MANIFEST.sha256'},actual^seen
assert not any(p.is_symlink() for p in ROOT.rglob('*'))
copies=json.loads((ROOT/'PACKING/SOURCE_COPY_BINDINGS.json').read_text())
for r in copies:verify(r)
bindings=json.loads((ROOT/'PACKING/ORIGINAL_AND_REVIEW_BINDING_CHECKS.json').read_text());included=0
for r in bindings['entries']:
 if r['inclusion']=='INCLUDED_UNCHANGED':verify({'path':r['source_path'],'sha256':r['sha256']});included+=1
 else:
  assert r['inclusion']=='EXTERNAL_OR_OMITTED_BINDING_ONLY'
  if not Path(r['source_path']).is_absolute():assert not (ROOT/r['source_path']).exists()
for r in bindings['accepted_results']:
 verify({'path':r['author_path'],'sha256':r['author_sha256']});verify({'path':r['review_path'],'sha256':r['review_sha256']})
idx=json.loads((ROOT/'INCREMENTAL_RESULT_SOURCE_EVIDENCE_DEPENDENCY_MANIFEST.json').read_text());assert len(idx['results'])==5
controls=json.loads((ROOT/'PACKING/CONTROL_PLAN.json').read_text())['commands'];assert len(controls)==9
ids={r['id'] for r in idx['results']}|set(idx['external_dependency_registry']);controlids={r['id'] for r in controls}
for r in idx['results']:
 for a in r['artifacts']+r['separate_internal_review']:verify(a)
 assert set(r['depends_on'])<=ids;assert set(r['control_ids'])<=controlids;assert set(r['source_ids'])<=set(idx['source_registry'])
for r in idx['source_registry'].values():verify(r['record'])
for r in idx['external_dependency_registry'].values():
 for a in r.get('artifacts',[]):verify(a)
 for key in ['manifest','module_inventory','package_manifest','toolchain_pin']:
  if key in r:verify(r[key])
 if r.get('included') is False and 'path' in r:assert not (ROOT/r['path']).exists()
verify(idx['kernel_component']['source'])
for r in controls:verify({'path':r['script'],'sha256':r['script_sha256']})
programs={p for p in seen if p.endswith('.py') and not p.startswith('PACKING/')}
expected={r['script'] for r in controls}|{'t20-next-frontier-20261008/retained-interior-certificate-review/AUTHOR_CONTROLS_REPLAY.py','t20-next-frontier-20261008/retained-interior-certificate-review/VERIFY_BINDINGS.py'}
assert programs==expected,(programs-expected,expected-programs)
prior=json.loads((ROOT/'COMPONENT_AND_PRIOR_IDENTITIES.json').read_text())['prior_checkpoints'];assert len(prior)==8 and all(r['included'] is False for r in prior)
assert not any(Path(p).suffix.lower() in ['.pdf','.png','.jpg','.jpeg','.html','.pyc','.olean','.ilean','.zip'] for p in seen)
assert not any('/source-images/' in p or '/__pycache__/' in p for p in seen)
print(json.dumps({'status':'PASS','payload_files':len(seen),'unchanged_source_copies':len(copies),'included_original_bindings':included,'external_or_omitted_binding_only_entries':len(bindings['entries'])-included,'bound_author_review_pairs':len(bindings['accepted_results']),'declared_control_runs':len(controls),'distinct_program_contents':len({r['script_sha256'] for r in controls}),'prior_archive_references':len(prior),'source_body_checks':'UNREPLAYED','self_contained_lean':False,'scope':'Byte integrity and declared included mappings, not proof of omitted sources or physical/philosophical semantics.'},indent=2))
