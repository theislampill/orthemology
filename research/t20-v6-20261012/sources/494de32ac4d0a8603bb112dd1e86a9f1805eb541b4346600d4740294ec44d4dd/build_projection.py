#!/usr/bin/env python3
"""Local assembly only. This preparation file and private custody inputs are not public payload."""
from pathlib import Path
import collections,hashlib,json,re,sqlite3,shutil
W=Path(__file__).resolve().parents[3]; B=W/'t20-consolidation-20261011'; P=B/'projection/package';C=B/'catalogue'
DB=sqlite3.connect(C/'catalogue.sqlite3');DB.row_factory=sqlite3.Row
COMMIT='7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
URL='https://github.com/theislampill/orthemology/blob/'+COMMIT+'/'
rows={};excluded=[];private=[]
for generated in ('sources','source-suites','lean','replay','proof-families'):
 if (P/generated).exists():shutil.rmtree(P/generated)
public={}
for x in map(json.loads,(C/'published_file_identity_map.jsonl').open()):
 for h in x['held_exact_public_byte_matches']:public.setdefault(h['sha256'],(x['repository_path'],h['sha256'],h['bytes'],'EXACT'))
for x in map(json.loads,(C/'original_member_to_public_projection.jsonl').open()):
 if x['matched_repository_path']:
  p=x['matched_repository_path'];match=next((v for v in public.values() if v[0]==p),None)
  if match:public.setdefault(x['original_sha256'],(p,match[1],match[2],'EXACT' if x['original_sha256']==match[1] else 'INHERITED_AMENDED'))
# Additional baseline file identities verified through read-only connector on 2026-10-11.
public['4da3849144d33d0df00dc55d7eb66afe60529a59869f04c564c1ea6923454a45']=('docs/decisions/0010-orthability-sense-and-argument-boundary.md','4da3849144d33d0df00dc55d7eb66afe60529a59869f04c564c1ea6923454a45',3457,'EXACT')
public['cd5070341a46658c0e4ac2c077d343d276cf16e50f0305f61ebb90ba0b624c2e']=('theory/lineages/h-formalisation/orthing_formalisation_v1.md','cd5070341a46658c0e4ac2c077d343d276cf16e50f0305f61ebb90ba0b624c2e',93523,'EXACT')
flags={x['sha256']:x['exclusion_reasons'] for x in map(json.loads,(C/'private_publication_exclusions.jsonl').open())}
# Manual content inspection: NumPy matrix multiplication dd@np.linalg.solve is not an email.
flags.pop('dda057694b1deab9f08d815e58cb04259dd89180e34317a032438b997ee0dd95',None)

def sha(b):return hashlib.sha256(b).hexdigest()
def obj(h):return C/'objects'/h[:2]/h

def metadata(h,owner,track):
 raw=obj(h).read_bytes();assert sha(raw)==h
 locs=[dict(x) for x in DB.execute('select * from locations where sha256=?',(h,))]
 mem=[dict(x) for x in DB.execute('select * from members where sha256=?',(h,))]
 mem=sorted(mem,key=lambda x:(x['member'].count('/'),len(x['member']),x['archive_sha256']))
 provenance=[{'archive_sha256':x['archive_sha256'],'member':x['member']} for x in mem[:1]]
 return {'original_sha256':h,'original_bytes':len(raw),'owners':[{'track':track,'source_id':owner}],
         'original_member_bindings':provenance,'original_identity_scope':'Exact retained original bytes; custody does not imply new execution.'}

def add(h,owner,track,source=None,dest=None,required=False):
 if h in rows:
  r=rows[h]
  if {'track':track,'source_id':owner} not in r['owners']:r['owners'].append({'track':track,'source_id':owner})
  if dest and dest!=r.get('public_path'):
   raw=obj(h).read_bytes();p=P/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
   r.setdefault('required_replay_copies',[]).append({'path':dest,'sha256':h,'bytes':len(raw),'reason':'Import-relative or source-bound replay dependency.'})
  return r
 f=flags.get(h,[])
 if f and f not in (['nonselected_text_or_log_extension'],['private_machine_locators']):
  excluded.append({'source_id':owner,'track':track,'original_sha256':h,'reasons':f,'disposition':'withheld_pending_bounded_public_projection_review'});return None
 raw=obj(h).read_bytes();r=metadata(h,owner,track)
 if h in public and not required:
  path,ph,n,relation=public[h]
  r.update(disposition='pinned_existing_public_source',projection=relation,public_url=URL+path,repository_path=path,public_sha256=ph,public_bytes=n)
  if relation!='EXACT':r['transformations']=['Existing adopted public projection; original and public bytes remain distinct. No new transformation performed.']
 else:
  if not dest:
   names=[x[0] for x in DB.execute('select name from locations where sha256=?',(h,))]
   name=Path(source or '').name
   if not Path(name).suffix:name=next((x for x in names if Path(x).suffix in {'.md','.lean','.py','.patch','.json'}),'SOURCE.md')
   name=re.sub(r'[^A-Za-z0-9._-]','_',name)
   dest='sources/'+h[:16]+'/'+name
  p=P/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
  r.update(disposition='included',projection='EXACT',public_path=dest,public_sha256=h,public_bytes=len(raw))
 rows[h]=r;return r

def addfile(path,dest,owner,track='replay'):
 path=W/path if not Path(path).is_absolute() else Path(path)
 h=sha(path.read_bytes())
 if not obj(h).exists():raise ValueError('Uncatalogued source '+str(path))
 return add(h,owner,track,str(path),dest,required=True)

# Preserve executable module-relative layout before report de-duplication.
s=json.loads((B/'evidence/SOURCE_MAP.json').read_text())
for name,h in [('contracts.py',s['code26']['sha256']),('test_contracts.py','3b4d9843672753dbbca6f353bfe3a26a884c5938e6e19e936cd20077349e3ee3'),('exhaustive_oracle.py','423cee2356215f9e7e8372fb1adc183d9099243f256011bcacc78af694e139f2')]:
 add(h,'Pro-26-'+name,'evidence',dest='replay/finite-contracts/'+name,required=True)
for dirname,names in {
 'grouped-source-audit-gradient-20261011':['check_exact.py','RESULT.md'],
 'grouped-audit-independent-review':['check_grouped_covariance.py','independent-review.md'],
 'positive-high-order-correction-20261011':['check.py','RESULT.md'],
 'high-order-law-independent-review-20261011':['check_independent.py','REVIEW.md'],
}.items():
 for name in names:addfile(W/dirname/name,'replay/'+dirname+'/'+name,dirname)
# Exact baseline closure for literal-source compiler probability: 34 prerequisite modules,
# seven execution modules and five probability modules remain isolated from all other suites.
R=W/'literal-shift-probability-20261011';baseline=R/'inherited/baseline'
pins=json.loads((R/'PREREQUISITE_REBUILD.json').read_text())['modules']
module_rows=[]
for x in pins:
 mod=x['module'];path=baseline/Path(mod.replace('.','/')+'.lean');assert sha(path.read_bytes())==x['source_sha256']
 dest='lean/literal-shift/src/'+mod.replace('.','/')+'.lean';addfile(path,dest,mod,'proofs');module_rows.append({'module':mod,'path':dest,'sha256':x['source_sha256'],'role':'unchanged-prerequisite'})
for path in sorted((R/'inherited/literal').glob('*.lean'))+sorted(R.glob('LiteralShift*.lean')):
 dest='lean/literal-shift/src/'+path.name;addfile(path,dest,path.stem,'proofs');module_rows.append({'module':path.stem,'path':dest,'sha256':sha(path.read_bytes()),'role':'literal-source-frontier'})
for srcdir,category in [(R/'negative-controls','probability'),(W/'literal-shift-kernel-refinement-20261011/negative-controls','execution')]:
 for path in sorted(srcdir.glob('*.lean')):addfile(path,'lean/literal-shift/negative/'+category+'/'+path.name,path.stem,'proofs')
for path in [W/'literal-shift-kernel-refinement-20261011/LiteralShiftControls.lean']:
 addfile(path,'lean/literal-shift/controls/'+path.name,path.stem,'proofs')
# Retain bounded scientific implementation sources for every selected report family.
# These are source-only unless a checked replay entrypoint below explicitly covers them.
# Historical packaging/acquisition utilities and hidden vendor/cache trees are outside scope.
family_records=[]
owner_entries=[]
owner_entries += [(x['semantic_owner'], x['sha256'], x['path'], 'geometry') for x in json.loads((B/'geometry/SOURCE_REGISTER.json').read_text())['sources']]
owner_entries += [(x['source_id'], x['sha256'], x['original_read_path'], 'foundations') for x in json.loads((B/'foundations/SOURCES_AND_READING.json').read_text())['sources']]
owner_entries += [(k,x['sha256'],x['path'],'evidence') for k,x in s.items() if k not in {'daee_checker','daee_schema','daee_patch','support_code','timing_code','inquiry_code','code26','authorial'}]
views={x['sha256']:W/x['view_path'] for x in json.loads((C/'archive_views.json').read_text()) if 'view_path' in x}
seen_dirs=set()
for owner,h,source,track in owner_entries:
 path=W/source
 if 'catalogue/objects/' in source:
  possibilities=[]
  for m in DB.execute('select * from members where sha256=?',(h,)):
   if m['archive_sha256'] in views:
    q=views[m['archive_sha256']]/m['member']
    if q.exists():possibilities.append(q)
  if possibilities:path=min(possibilities,key=lambda p:(len(p.parts),len(str(p))))
 if not path.exists():continue
 directory=path.parent
 key=str(directory)
 if key in seen_dirs:continue
 seen_dirs.add(key)
 if directory.name in {'inputs','sources','reviewed_sources'}:continue
 files=sorted(set(directory.glob('*.py'))|set(directory.glob('*.lean'))|set(directory.glob('negative-controls/*.lean'))|set(directory.glob('tests/test_*.py')))
 files=[p for p in files if p.name not in {'acquire.py','verify_packet.py','verify_manifest.py','package.py','build_release.py'}]
 if not files:
  family_records.append({'owner':owner,'track':track,'report_original_sha256':h,'disposition':'written_result_owner','implementation':'No direct scientific Python/Lean source adjacent to selected report; other owner suites remain separate.'});continue
 suite='source-suites/'+re.sub(r'[^A-Za-z0-9._-]','_',directory.name)
 records=[]
 for p in files:
  raw=p.read_bytes();ph=sha(raw);rel=p.relative_to(directory).as_posix();dest=suite+'/'+rel
  r=addfile(p,dest,owner,track)
  records.append({'member':rel,'original_sha256':ph,'public_path':dest if r else None,'disposition':'source_included' if r else 'withheld_for_projection_review'})
 # A source-bound script may read its authored report; include that exact dependency.
 if path.suffix=='.md':add(h,owner,track,str(path),suite+'/'+path.name,required=True)
 family_records.append({'owner':owner,'track':track,'report_original_sha256':h,'suite':suite,'disposition':'scientific_implementation_sources_included','files':records,'replay_scope':'Source preservation only unless selected in REPLAY_SCOPE.json. Acquisition, packet-manifest checks, source snapshots and environment assumptions may require the original custody packet; no suite-wide PASS is inferred.'})
(P/'FAMILY_DISPOSITIONS.json').write_text(json.dumps({'status':'PROPOSED','families':family_records,'note':'Every included report is further bound in PUBLIC_PROJECTION.json. Source-only status is explicit; no cache or bulk archive is needed to read and extend the selected science.'},indent=2)+'\n')
# Scientific source closure of named later formal preservation families.
# Preserve original relative layouts, keeping conflicting module versions isolated.
proof_families=[]
for prefix,short in [('fd5ff4c23019','rational-hase-j'),('218d50e1373b','rational-threshold'),('2ca475be25d8','warranted-discrimination'),('549cfec83f68','effective-source'),('7b612c7c5385','constructive-guarded'),('83f7d576dbe5','guarded-supplement'),('de019f745936','full-functional'),('a9724de4dc5f','polynomial-extension'),('2ef24fd480b2','tensor-realizability'),('487d5fee7d1e','finite-moment-recovery'),('a98b3583207f','positive-hierarchy'),('38c951260105','initial-positivity')]:
 view=next(x for x in views.values() if x.name.endswith('--'+prefix))
 files=sorted(p for p in view.rglob('*') if p.is_file() and (p.suffix in {'.lean','.py','.sh','.toml'} or p.name=='lean-toolchain') and not any(q in p.relative_to(view).parts for q in {'.lake','__pycache__','build','logs','.git'}))
 entries=[]
 for path in files:
  rel=path.relative_to(view).as_posix();dest='proof-families/'+short+'/'+rel
  r=addfile(path,dest,short,'geometry' if short in {'full-functional','polynomial-extension','tensor-realizability','finite-moment-recovery','positive-hierarchy','initial-positivity'} else 'proofs')
  entries.append({'original_member':rel,'original_sha256':sha(path.read_bytes()),'public_path':dest if r else None,'disposition':'included_scientific_source' if r else 'withheld_pending_public_review'})
 proof_families.append({'family':short,'archive_sha256':next(h for h,v in views.items() if v==view),'files':entries,'scope':'Source-preserved isolated original layout. Official dependencies, compiled caches, historic logs and archival delivery wrappers omitted. No turnkey historical script or fresh proof replay claim; affected closures require the source-specific declared environment and review.'})
(P/'PROOF_FAMILY_LAYOUTS.json').write_text(json.dumps({'families':proof_families,'scope':'Actual later kernel source chains, generated checker parts and Python implementation sources. Equal names in different family/member paths are never flattened.'},indent=2)+'\n')
# Reconcile selected entries and the exact dependency maps, beyond directory adjacency.
formal=json.loads((B/'proofs/FORMAL_REPLAY_MAP.json').read_text())
for cluster in formal['clusters']:
 sources=cluster.get('minimal_unchanged_source_closure',{}).get('source_files',[])+cluster.get('selected_entry_modules',[])+cluster.get('source_scripts',[])
 for x in sources:
  if x['sha256'] not in rows:
   add(x['sha256'],cluster['cluster_id'],'proofs',x['path'])
# Preserve actual copied upstream/adapted-code licence and attribution bytes.
add('b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1','Mathlib-Apache-2.0','licences',dest='LICENSES/Mathlib-LICENSE.txt',required=True)
add('5f2f42c8cccd68560c72021cbfe69c21d24c716ea813ac21f10b465a791b0ecf','constructive-third-party-notices','licences',dest='LICENSES/THIRD_PARTY_NOTICES.md',required=True)
# Actual bound grouped control inputs, including its independent-review source.
for x in json.loads((W/'grouped-source-audit-gradient-20261011/INPUT_BINDINGS.json').read_text()):
 add(x['sha256'],'grouped-control-input','geometry',str(W/'grouped-source-audit-gradient-20261011'/x['copy']))
# All selected actual owner reports, not archive wrappers.
for x in json.loads((B/'foundations/SOURCES_AND_READING.json').read_text())['sources']:
 add(x['sha256'],x['source_id'],'foundations',x['original_read_path'])
for x in json.loads((B/'geometry/SOURCE_REGISTER.json').read_text())['sources']:
 add(x['sha256'],x['semantic_owner'],'geometry',x['path'])
for owner,x in s.items():
 # Baseline DAEE implementation/schema are upstream-owned: retain the reviewed delta separately.
 if owner in {'daee_checker','daee_schema'}:
  excluded.append({'source_id':owner,'original_sha256':x['sha256'],'disposition':'upstream_dependency_not_republished','reason':'Protected DAEE source is outside this additive reader; no candidate patch application promised.'});continue
 add(x['sha256'],owner,'evidence',x['path'])
for d in ['literal-shift-kernel-refinement-20261011','literal-shift-probability-20261011','literal-shift-kernel-independent-review-20261011','literal-shift-probability-independent-review-20261011']:
 for name in ['RESULT.md','SOURCE_BRIDGE.md','REVIEW.md']:
  p=W/d/name
  if p.exists():add(sha(p.read_bytes()),d+'-'+name,'proofs',str(p))
for ident,x in json.loads((B/'proofs/SOURCE_REGISTRY.json').read_text())['sources'].items():
 add(x['sha256'],ident,'proofs',x['source_path'])
# Later older-architecture source restorations are explicit owners.
for owner,h in [('controlled-information-restoration','bd83f4c2bb1a41151405872a6aa57fe9bdc352f0b63db4cfb302e0068c8b0d4a'),('correlated-restoration','7163cb536782ccb8a91a10be4b91cdcc1113bbab3c467d6ac66dee0d59cb0caf')]:add(h,owner,'inherited-architecture')
# Selected companion diagnostics and older programme owners carry actual bodies;
# private methodology/Drive ledgers remain identity-and-summary only.
for x in json.loads((B/'coverage/SELECTED_SOURCE_READS.json').read_text()):
 if int(x['id'][1:])<=13 or x['id'] in {'S22','S23','S24'}:
  add(x['sha256'],x['label'],'coverage',x.get('local_path'))
# Additional track-owned source selections can be supplied without changing original bytes.
extra=B/'projection/private/extra_sources.json'
if extra.exists():
 for x in json.loads(extra.read_text()):add(x['sha256'],x['source_id'],x['track'],x.get('path'))

manifest={'schema':'t20-consolidated-public-projection-v1','status':'PROPOSED_OWNER_REVIEW_LOCAL_ONLY','cutoff_utc':'2026-10-11T11:32:55Z',
 'convention':'Package-local extension of published original/public SHA256 bindings; does not add or amend repository-wide schemas.',
 'repository':{'name':'theislampill/orthemology','commit':COMMIT,'pinned_blob_prefix':URL},
 'files':sorted(rows.values(),key=lambda r:(r.get('public_path','~'+r.get('repository_path','')),r['original_sha256'])),
 'exclusions':excluded,'raw_custody':'Raw archives, transcripts, private source collections, private locators and original-to-private alias maps are not included.',
 'execution_scope':'Original source inclusion is not a fresh execution receipt. REPLAY_SCOPE.json distinguishes runnable finite controls and supplied Lean closure.'}
(P/'PUBLIC_PROJECTION.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
(P/'SOURCE_INDEX.md').write_text('# Current source owners\n\nOriginal source statements, corrections and limitations retain their authored status. Historical relative references inside exact sources are original-member citations, not promises of complete packet replication. The source binding register is authoritative for this candidate.\n\n'+'\n'.join('- '+', '.join(x['source_id'] for x in r['owners'])+': ['+r['original_sha256'][:12]+']('+r.get('public_path',r.get('public_url'))+')'+(' (existing public projection)' if r['disposition']!='included' else '') for r in manifest['files'])+'\n')
# Original baseline IDs are derived from read-only byte receipts, never guessed.
receipt=json.loads((C/'repository-evidence/FETCHED_FILE_BYTE_RECEIPT.json').read_text())
preimages=[]
for x in receipt:
 name=Path(x['file']).name
 if name in ['.gitattributes','scripts__validate_repo.py','scripts__validate_internal_references.py','scripts__generate_current_state.py','scripts__validate_v5_successors.py']:
  preimages.append({'path':name.replace('__','/'),'git_blob_sha1':x['expected_git_blob_sha1'],'sha256':x['sha256'],'bytes':x['bytes']})
(P/'INTEGRATION_PINS.json').write_text(json.dumps({'commit':COMMIT,'tree':'906b592fb2591ed918c5f0caf485ef79dca513ab','destination':'research/t20-consolidated-20261011','preimages':preimages},indent=2)+'\n')
# Module closure is checked here, separate from proof execution.
mods={x['module']:x for x in module_rows};deps={};external=set()
for m,x in mods.items():
 imports=[t for line in (P/x['path']).read_text().splitlines() if line.startswith('import ') for t in line.split()[1:]]
 deps[m]=[d for d in imports if d in mods];external.update(d for d in imports if d not in mods)
 if any(d != 'Mathlib' and not d.startswith(('Mathlib.','Batteries.','Std.','Lean.','Init')) for d in external):raise ValueError('Unclosed nonofficial import '+repr(external))
order=[]
while len(order)<len(mods):
 ready=sorted(m for m in mods if m not in order and set(deps[m])<=set(order))
 if not ready:raise ValueError('cyclic imports')
 order.extend(ready)
ml=json.loads((W/'.toolchains/mathlib4-c44e0c8/lake-manifest.json').read_text())
# SOURCE_TOOLCHAIN.json binds exact upstream closure without copying package caches.
base_pin=json.loads((R/'inputs/TOOLCHAIN_ACQUISITION.json').read_text())
(P/'lean/literal-shift/MODULES.json').write_text(json.dumps({'modules':module_rows,'order':order,'external_imports':sorted(external),'scope':'Exact supplied source closure. Compilation/axiom inspection/negative controls must be rerun in declared pinned official environment; historical PASS is not a fresh projected-source run.'},indent=2)+'\n')
(P/'lean/literal-shift/DEPENDENCIES.json').write_text(json.dumps({'lean_version':'4.19.0','mathlib_commit':'c44e0c8ee63ca166450922a373c7409c5d26b00b','mathlib_repository':'https://github.com/leanprover-community/mathlib4','packages':ml['packages'],'note':'No dependency installation occurs. Exact mathlib commit must be checked against inherited toolchain acquisition before replay.'},indent=2)+'\n')
private.append({'toolchain_acquisition':base_pin})
(B/'projection/private/TOOLCHAIN_INSPECTION.json').write_text(json.dumps(private,indent=2)+'\n')
summary={'source_objects':len(rows),'included_objects':sum(r['disposition']=='included' for r in rows.values()),'pinned_existing':sum(r['disposition']!='included' for r in rows.values()),'selected_original_bytes':sum(r['original_bytes'] for r in rows.values()),'payload_files':sum(p.is_file() for p in P.rglob('*')),'payload_bytes':sum(p.stat().st_size for p in P.rglob('*') if p.is_file()),'exclusions':excluded,'literal_modules':len(module_rows),'closure_checked':True}
(B/'projection/private/ASSEMBLY_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
