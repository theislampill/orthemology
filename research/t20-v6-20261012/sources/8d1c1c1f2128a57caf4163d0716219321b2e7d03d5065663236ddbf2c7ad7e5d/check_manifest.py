#!/usr/bin/env python3
"""Read-only byte inventory and normalized declared evidence bindings; no proof checking."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];P='t20-next-frontier-20261008/'
EXPECTED={'sharp-skyline-information':'52a9c53ca5d1765de2956e685701532529efca9a0292165f8f9e738b43b7a870','finite-geometric-score':'d7cfa67248e06786e1c4acaae6e61138498ef8e6dc1f14287d7d2664302ee96f','rational-basing-continuation':'4c48b7ec591654c39f9a8bc93c2e15c7e7f8bf67fd3de202d51fec0da07d8972'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(rel):return json.loads((ROOT/rel).read_text())
def verify(r):
 rel=Path(r['path']);assert not rel.is_absolute() and '..' not in rel.parts,r
 p=ROOT/rel;assert p.is_file() and not p.is_symlink(),str(rel)
 assert sha(p)==r['sha256'],str(rel)
 if 'bytes' in r:assert p.stat().st_size==r['bytes'],str(rel)
def normalized(raw):
 if raw.startswith('private-locator:45fe10b770ecaeaedfcf'+P):return raw.split(P,1)[1]
 if raw.startswith('../'):return raw[3:]
 assert not Path(raw).is_absolute() and '..' not in Path(raw).parts,raw
 return raw
m=read('MANIFEST.json');assert sha(ROOT/'MANIFEST.json')==(ROOT/'MANIFEST.sha256').read_text().split()[0]
rows=m['files'];listed={r['path'] for r in rows};assert len(rows)==len(listed)==m['file_count']
for row in rows:verify(row)
assert not any(p.is_symlink() for p in ROOT.rglob('*'))
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
assert actual==listed|{'MANIFEST.json','MANIFEST.sha256'}
copies=read('PACKING/SOURCE_COPY_BINDINGS.json')
for r in copies:verify(r)
b=read('PACKING/REVIEW_AND_DEPENDENCY_BINDINGS.json');external={r['origin_relative_to_research_root']:r for r in b['external_predecessor_bindings']}
assert len(external)==len(b['external_predecessor_bindings'])
def binding(raw,digest,size=None):
 rel=normalized(raw);p=ROOT/P/rel
 if p.is_file():assert sha(p)==digest,rel
 else:
  assert rel in external,rel;assert external[rel]['sha256']==digest,rel
  if size is not None:assert external[rel]['bytes']==size,rel
 if size is not None and p.is_file():assert p.stat().st_size==size,rel
prior=read('COMPONENT_AND_PRIOR_IDENTITIES.json')['prior_checkpoints'];assert len(prior)==11
assert all(r['included'] is False for r in prior)
assert prior[8]['sha256']=='81089a1bd1497982bf80310d191a6b1019462bcb922b1f2fffbefc696853f1ef'
assert prior[10]['sha256']=='76bec736f7345358f43b82409592a52167d627103b53a97d7939f9ae56b3534d'
bysha={r['sha256']:r for r in prior}
for r in external.values():
 assert not (ROOT/r['path']).exists();assert r['verified_against']=='EXACT_ARCHIVE_MEMBER'
 assert r['predecessor_archive_sha256'] in bysha
 assert r['archive_member'].endswith('/'+r['path'])
for r in b['included_current_bindings']:verify(r)
source_rows=0
for component in ['sharp-skyline-information','sharp-skyline-information-review','finite-geometric-score','finite-geometric-score-review']:
 for r in read(P+component+'/SOURCE_BINDINGS.json')['sources']:
  binding(r['path'],r['sha256'],r.get('bytes'));source_rows+=1
rb=read(P+'rational-basing-continuation/INPUT_BINDINGS.json')
for r in rb['inputs']+rb['additional_read_inputs']:
 binding(r['path'],r['sha256']);source_rows+=1
native=0;native_rows=0
for c in b['components']:
 f=ROOT/P/c/'MANIFEST.json'
 if f.exists():
  obj=json.loads(f.read_text())
  for r in obj.get('files',obj.get('payloads',[])):
   verify(r|{'path':P+c+'/'+r['path']});native_rows+=1
  native+=1
 for filename in ['SHA256SUMS','MANIFEST.sha256']:
  p=ROOT/P/c/filename
  if p.exists():
   for line in p.read_text().splitlines():
    h,n=line.split(maxsplit=1);n=n.lstrip('*');rel=n if n.startswith(c+'/') else c+'/'+n;binding(rel,h)
   native+=1
accepted=b['accepted_results'];assert len(accepted)==3
assert {r['stage'] for r in accepted}==set(EXPECTED)
for r in accepted:
 assert r['author']['path']==P+r['stage']+'/RESULT.md'
 assert r['author']['sha256']==EXPECTED[r['stage']]
 verify(r['author']);verify(r['review']);verify(r['binding_record'])
 assert r['author']['sha256'] in (ROOT/r['binding_record']['path']).read_text()
 assert r['status']=='PASS_WITHIN_SCOPED_INTERNAL_REVIEW'
for stage in ['sharp-skyline-information','finite-geometric-score']:
 r=read(P+stage+'-review/REVIEW_RECEIPT.json');assert r['result']=='PASS' and not r['blocking_findings']
 assert r['accepted_author_result_sha256']==EXPECTED[stage]
 for filename,key,dir_ in [('RESULT.md','accepted_author_result_sha256',stage),('MANIFEST.json','author_manifest_sha256',stage),('REVIEW.md','review_sha256',stage+'-review'),('SOURCE_BINDINGS.json','source_bindings_sha256',stage+'-review')]:
  assert sha(ROOT/P/dir_/filename)==r[key]
 v=read(P+stage+'-review/VERIFICATION.json');assert v['status']=='PASS' and v['accepted_author_result_sha256']==r['accepted_author_result_sha256']
 row=next(x for x in accepted if x['stage']==stage)
 assert row['review']['path']==P+stage+'-review/REVIEW.md' and row['binding_record']['path']==P+stage+'-review/REVIEW_RECEIPT.json'
 assert r['historical_floor']=='UNVERIFIED'
assert sha(ROOT/P/'finite-geometric-score-review/REVIEW_RECEIPT.json')=='8b0a58c0b7e69af7ba946f9d6eb14fbe7b9417b2668216dffe5e9029403eba6b'
assert read(P+'finite-geometric-score-review/REVIEW_RECEIPT.json')['explicit_cutoff_certified'] is False
r=read(P+'rational-basing-continuation/REVIEW_RECEIPT.json')
assert r['verdict']=='No remaining substantive blocker within scoped review'
for x in r['review_files']:binding(x['path'],x['sha256'])
for x in r['exact_reviewed_arguments']:binding('rational-basing-continuation/'+x['path'],x['sha256'])
row=next(x for x in accepted if x['stage']=='rational-basing-continuation')
assert row['review']['path']==P+'rational-basing-continuation-review/INFERENTIAL_TEST_ADDENDUM.md'
assert row['binding_record']['path']==P+'rational-basing-continuation/REVIEW_RECEIPT.json'
assert EXPECTED['rational-basing-continuation'] in (ROOT/row['review']['path']).read_text()
for x in b['duplicate_replay_sources']:
 verify(x['original']);verify(x['copy']);assert x['original']['sha256']==x['copy']['sha256']
idx=read('INCREMENTAL_RESULT_SOURCE_EVIDENCE_DEPENDENCY_MANIFEST.json');assert len(idx['results'])==3
assert idx['checkpoint_ordinal']==12 and idx['kernel_status']=='NO_NEW_LEAN_THEOREMS_OR_REPLAYS'
plan=read('PACKING/CONTROL_PLAN.json');commands=plan['commands'];assert len(commands)==3
ids={r['id'] for r in idx['results']}|set(idx['external_dependency_registry']);control_ids={r['id'] for r in commands}
for r in idx['results']:
 for x in r['artifacts']+r['separate_internal_review']:verify(x)
 assert set(r['depends_on'])<=ids and set(r['control_ids'])<=control_ids and set(r['source_ids'])<=set(idx['source_registry'])
for r in idx['source_registry'].values():
 for x in r['records']:verify(x)
for r in commands:verify({'path':r['script'],'sha256':r['script_sha256']})
programs={x for x in listed if x.endswith('.py') and not x.startswith('PACKING/')}
assert programs=={r['script'] for r in commands}|{r['path'] for r in plan['preserved_not_replayed']}
assert not any(Path(x).suffix.lower() in {'.pdf','.png','.jpg','.jpeg','.html','.pyc','.olean','.ilean','.zip'} for x in listed)
assert not any('/__pycache__/' in x or '/modal-identity-transport/' in x for x in listed)
print(json.dumps({'status':'PASS','payload_files':len(rows),'unchanged_source_copies':len(copies),'bound_author_review_pairs':len(accepted),'native_manifests_or_sum_lists':native,'native_manifest_rows':native_rows,'source_binding_rows':source_rows,'fresh_math_control_runs_declared':len(commands),'preserved_programs_not_replayed':len(plan['preserved_not_replayed']),'external_predecessor_members':len(external),'prior_archive_references':len(prior),'source_body_checks':'NOT_RERUN_SOURCE_BODIES_OMITTED','scope':'Frozen artifact identity and declared review/dependency relationships, not new proof or source-reading certification.'},indent=2))
