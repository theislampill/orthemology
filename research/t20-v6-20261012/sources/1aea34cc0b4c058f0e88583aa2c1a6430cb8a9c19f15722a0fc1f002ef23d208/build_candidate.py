"""Additive public research supplement. Does not modify any v4 or author source."""
from pathlib import Path
import json,hashlib,shutil,re
W=Path(__file__).resolve().parents[2];D=W/'t20-closure-audit-20261011';A=Path(__file__).parent
V=W/'deliverables/t20-v4-sealed';P=W/'deliverables/t20-v5-candidate';H=P/'historical_coverage'
PIN='7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(rel,x):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def safe(p):
 if p.is_symlink():raise RuntimeError('symlink source '+str(p))
 text=p.read_text(errors='ignore')
 if re.search(r'/(workspace/scratch|home/agent)/[^\s\"\']+',text):raise RuntimeError('private absolute locator: '+str(p.relative_to(W)))
 if re.search(r'(?:[?&](?:sig|token)=|sediment://|file-[A-Za-z0-9]{20,})',text):raise RuntimeError('private transfer token: '+str(p.relative_to(W)))
# Existing candidate is only our previous unsealed build. Rebuild from delivered immutable envelope.
if P.exists():shutil.rmtree(P)
shutil.copytree(V,P)
byhash={};routes=[];selected=[];source_objects={};exceptions=[];source_promises=[]
for p in sorted(P.rglob('*')):
 if p.is_file():byhash.setdefault(sha(p),p.relative_to(P).as_posix())
lanes=['early_mathematics','early_foundations','early_operations','root_types','later_scopes','review_early_math','review_foundations_operations','review_later']
exclude={'FETCH_PLAN.json','depth_read_candidates.json','INPUT_SNAPSHOT.json','AUTHOR_REPLAY.json'}
# Reports, source-reading ledgers and safe author/review evidence. Work-in-progress review files are not final qualification.
for lane in lanes:
 if not (D/lane).exists():continue
 for p in sorted((D/lane).iterdir()):
  if p.is_file() and not p.name.startswith('.') and p.suffix in {'.md','.json','.py'} and p.name not in exclude:
   safe(p);rel='historical_coverage/'+lane+'/'+p.name;q=P/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);selected.append((p,rel));byhash.setdefault(sha(p),rel)
for name in ['FINAL_COVERAGE.json','FINAL_COVERAGE.md','OWNER_REVIEW_CASE.md','SYNTHESIS.md','HISTORICAL_CROSS_FRONT_SYNTHESIS.md','OWNER_CLOSURE_CASE.md','REVIEW_DISPOSITIONS.json','SUPPLEMENT_INTERFACES.json','ROOT_FRESH_CONTROLS.normal.json','ROOT_FRESH_CONTROLS.optimized.json','FINAL_BASELINE_READBACK.json']:
 p=D/name
 if p.is_file():
  safe(p);rel='historical_coverage/'+name;q=P/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);selected.append((p,rel));byhash.setdefault(sha(p),rel)
for p in sorted((D/'pinned-baseline').glob('*.json')):
 if p.name=='FETCH_RECEIPTS.json':continue
 safe(p);rel='historical_coverage/pinned-baseline/'+p.name;q=P/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);selected.append((p,rel));byhash.setdefault(sha(p),rel)
# Enumerate available fetched scientific bodies by actual content hash; this is custody, not reading credit.
available={}
for lane in lanes:
 if not (D/lane).exists():continue
 for p in (D/lane).rglob('*'):
  if p.is_file() and not any(part.startswith('.') for part in p.relative_to(D/lane).parts) and (p.suffix in {'.lean','.md','.json','.py'} or (p.suffix=='.txt' and p.name.startswith('src-'))):available.setdefault(sha(p),p)
def copy_body(src,owner):
 digest=sha(src);catalogue='catalogue/objects' in src.as_posix()
 if digest in byhash and not catalogue:return byhash[digest]
 if digest in source_objects:return source_objects[digest]['included_path']
 safe(src);suffix=src.suffix if src.suffix in {'.lean','.md','.json','.py','.toml'} else '.txt'
 rel='historical_coverage/supplement/source_objects/'+digest+suffix;q=P/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,q)
 source_objects[digest]={'included_path':rel,'sha256':digest,'bytes':src.stat().st_size,'owner_bindings':[],'identity':'EXACT_SUPPLIED_SOURCE_BYTES; existing source projection status belongs to original ledger, not changed here.'}
 byhash.setdefault(digest,rel);return rel
# Bind original report/ledger path names without changing their bytes.
for src,rel in selected:routes.append({'binding_document':rel,'selector':[],'locator_field':'source_packet_member','original_locator':src.relative_to(W).as_posix(),'workspace_alias':src.relative_to(W).as_posix(),'sha256':sha(src),'included_path':rel,'identity':'EXACT','purpose':'Unchanged author/report/ledger member, not fresh reading or proof execution.'})
pathfields=('path','local_path','file','public_path','source_path','copy','actual_path')
def record(row,document,selector,lane):
 hashes=[row.get(k) for k in ['actual_sha256','public_sha256','sha256','expected_public_sha256','original_sha256']]
 hashes=[x for x in hashes if isinstance(x,str) and re.fullmatch(r'[0-9a-f]{64}',x)]
 if not hashes:return
 locs=[(k,row[k]) for k in pathfields if isinstance(row.get(k),str) and row[k] and not row[k].startswith(('https://','http://'))]
 if not locs:return
 owner={k:row[k] for k in ['id','source_id','label','member','row','read_scope','reading_depth','credit','reading_credit','projection','original_sha256','public_sha256'] if k in row}
 for field,loc in locs:
  candidates=[W/loc,D/lane/loc,D/loc]
  original=row.get('original_sha256');declared=row.get('public_sha256') or row.get('sha256') or row.get('actual_sha256')
  # Catalogue paths bind their named exact source, never substitute a differently projected hash.
  physical=next((p for p in candidates if p.is_file() and sha(p) in hashes),None)
  if physical is None:
   for digest in hashes:
    if digest in byhash:
     # Public locator fields select public/declared bytes first; original hashes remain separate metadata.
     physical=P/byhash[digest];break
    if digest in available:physical=available[digest];break
  if physical is not None:
   direct_alias=next((p.relative_to(W).as_posix() for p in candidates if p.is_file() and sha(p) in hashes),None)
   alias=direct_alias or loc
   digest=sha(physical);target=physical.relative_to(P).as_posix() if physical.is_relative_to(P) else copy_body(physical,owner)
   if 'catalogue/objects/' in loc:
    direct=W/loc
    if not direct.is_file() or sha(direct) not in hashes:raise RuntimeError('unresolved catalogue source '+loc)
    digest=sha(direct);target=copy_body(direct,owner)
   if digest in source_objects and owner not in source_objects[digest]['owner_bindings']:source_objects[digest]['owner_bindings'].append(owner)
   routes.append({'binding_document':document,'selector':selector,'locator_field':field,'original_locator':loc,'workspace_alias':alias,'included_path':target,'sha256':digest,'bytes':(P/target).stat().st_size,'identity':'EXACT_TO_BOUND_SOURCE_BYTES','source_projection':row.get('projection'),'original_source_sha256':original,'declared_public_sha256':row.get('public_sha256'),'owner':owner})
  else:
   urls=[row.get(k) for k in ['url','public_url','source_url'] if isinstance(row.get(k),str)]
   if loc.startswith(('docs/','experiments/','src/','tests/')):urls.append('https://github.com/theislampill/orthemology/blob/'+PIN+'/'+loc)
   urls=[u for u in urls if '/'+PIN+'/' in u]
   exception={'binding_document':document,'selector':selector,'locator_field':field,'original_locator':loc,'sha256_candidates':hashes,'owner':owner}
   if urls:exception.update(disposition='PINNED_PUBLIC_ONLY_NOT_INCLUDED',public_url=urls[0],scope='Registry-owned pinned route; no local body or fresh reading/execution claim.')
   else:exception.update(disposition='UNRESOLVED_BINDING',scope='Needs author clarification before final delivery.')
   exceptions.append(exception)
def walk(value,document,selector,lane):
 if isinstance(value,dict):
  record(value,document,selector,lane)
  for key,item in value.items():walk(item,document,selector+[key],lane)
 elif isinstance(value,list):
  for key,item in enumerate(value):walk(item,document,selector+[key],lane)
# Binding/reading manifests, not a promise to copy every object mentioned in the full registry.
for src,rel in selected:
 if src.suffix=='.json' and src.parent.name!='pinned-baseline' and src.name!='MANIFEST.json':walk(json.loads(src.read_text()),rel,[],src.parent.name)
# Independent alias entries expose files under the exact original code-relative source layout.
put('historical_coverage/SOURCE_PATH_RESOLVER.json',{'schema':'t20-v5-exact-source-path-resolver-v1','status':'UNSEALED_PENDING_REVIEW','path_base':'Delivery root, the parent of historical_coverage and package.','scope':'Resolve original workspace-relative/source-member locators without rewriting original reports or ledgers. Exact means exact to the ledger-bound source bytes, which may itself be an explicitly derived historical public projection. Original and public hashes are never equated.','routes':routes,'exceptions':exceptions,'source_objects':list(source_objects.values()),'not_claimed':['Full Lean import closure','new source reading by hash lookup','fresh kernel execution','repository adoption']})
put('historical_coverage/V4_PRESERVATION.json',{'status':'PASS','source_envelope':'Delivered v4 unpacked envelope','files':[{'path':p.relative_to(V).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(V.rglob('*')) if p.is_file()],'scope':'Every delivered v4 member is preserved at the same relative path, including original package manifest, installer and qualification. The old DELIVERY_CONTENTS manifest remains the exact v4 inventory, not the v5 envelope inventory.'})
put('READ_V5_FIRST.md','''# T20 historical-coverage supplement: unsealed candidate\n\nThis additive working candidate preserves every delivered v4 file unchanged under package/, qualification/ and the original v4 envelope files. historical_coverage/ adds an individually tracked historical audit, particularly T1–T6. Independent reviews, owner synthesis and final dispositions are pending. This candidate is not ready for integration or delivery.\n\nThe assigned early ledgers cover 34 mathematics, 11 foundations, 20 operations and 3 type rows, intended to partition the exact 68-row early registry. The later audit has 262 rows with reading and execution scopes kept separate. Row accounting is not whole-corpus deep reading. No original scientific status or claim is changed by this supplement.\n\nStart with the new source-specific REPORT.md files; then use SOURCE_PATH_RESOLVER.json to find their exact included source bytes or explicit pinned-public-only exceptions. Original report and ledger paths remain historical; they are not requests to reconstruct the author's private workspace.\n\nThe retained package/CODEX_START_HERE.md still controls the unchanged v4 integration candidate. The new CODEX_ADDENDUM.md explains how to handle this separate supplement once its review is finished and the owner issues authority. No repository action or T21 initiation is authorised here.\n''')
put('historical_coverage/CODEX_ADDENDUM.md','''# Draft Codex addendum: preserve the delivered v4 payload\n\nThis supplement is currently unsealed and independently reviewed dispositions are pending. Do not integrate it yet. The delivered v4 scientific package, installer, pinned baseline and manifests must remain byte-identical.\n\nFor verification, run the supplement verifier from the delivery root, then the unchanged package validators. SOURCE_PATH_RESOLVER.json maps an original report/ledger locator and selector to actual included bytes. It does not rewrite originals or turn a derived source projection into original-source identity. Pinned-public-only entries are explicit exceptions, with no new local reading or execution claim.\n\nIf the owner later authorises one additive research integration, include the complete unchanged v4 package and this reviewed historical supplement in their separately named subtrees. The existing v4 installer only applies its original package. It does not install or validate this sibling supplement; do not alter that installer or its manifest to imply otherwise. Follow the final owner prompt for the exact supplement destination and PR authority. Stop on baseline drift and preserve all source/result owners and repository conventions.\n\nDo not reopen unchanged proofs or rerun all inherited families. The audit distinguishes individually read bodies, selected endpoints, source identity, metadata triage and inherited execution. Fresh bounded application controls do not amount to kernel, empirical, Arabic-primary or universal-theorem revalidation. Final closure and T21 remain separate owner decisions.\n''')
put('historical_coverage/PORTABILITY_AND_EVIDENCE.md','''# Exact sources, portable lookup and bounded replay

The supplement copies the final author/reviewer files exactly; pre-correction versions are retained where used by review. Every original v4 delivery member remains unchanged. Old workspace-relative paths are historical locators. SOURCE_PATH_RESOLVER.json binds each document/selector/locator to exact included bytes or an explicit pinned-public-only exception. Exact here means the bytes actually bound in that ledger; a historical public projection can have a different original-source hash, and both identities remain distinct.

From the delivery root:

    python -B historical_coverage/verify_supplement.py
    python -B historical_coverage/resolve_source.py SHA256_OR_ORIGINAL_LOCATOR
    python -B historical_coverage/replay_supplement.py --list

The verifier checks all original v4 members, source-route bytes and original ledger selectors, and the exact 68/262 coverage populations when FINAL_COVERAGE is present. It does not decide scientific truth or independent review readiness. The original package validators remain unchanged and operate only inside package/.

The replay wrapper creates a disposable directory, materializes only declared aliases and runs a selected unchanged author/reviewer script. The later accounting suite also materializes the complete immutable v4 package because its checker explicitly verifies the full old file population. Nothing is written into the delivered scientific package. No installation, network request or Lean compilation occurs.

The foundations author verifier is normal-only and only checks hashes, coverage and stored application flags. Its historical optimized run carries no validation credit. The independent foundations/operations checker actually reconstructs source-bound repair maps and evaluates finite relation/menu controls with explicit checks in normal and optimized Python. Universal inherited proofs, philosophical premises, historical statuses and actual empirical/Arabic source interpretation keep their separately stated evidence levels. Modes and enumerated cases do not multiply scientific results.

Original source packet manifests describe the original packets, including some helpers or raw logs intentionally not selected for public delivery. They are preserved attribution records, not supplement file inventories. The supplement's own content manifest controls its included files. AUTHOR_REPLAY.json is omitted because it contains private absolute command custody; PUBLIC_AUTHOR_REPLAY.json discloses its original hash and safe scoped summary. Raw stdout/stderr logs, dotfiles, transfer helpers and exploratory triage dumps are not included.
''')
summary={'status':'STAGED_NOT_SEALED','v4_members':sum(p.is_file() for p in V.rglob('*')),'selected_packet_members':len(selected),'resolver_routes':len(routes),'new_source_objects':len(source_objects),'pinned_public_only':sum(x['disposition']=='PINNED_PUBLIC_ONLY_NOT_INCLUDED' for x in exceptions),'unresolved':sum(x['disposition']=='UNRESOLVED_BINDING' for x in exceptions)}
(A/'STAGING_STATUS.json').write_text(json.dumps(summary,indent=2)+'\n');(A/'PORTABILITY_GAPS.json').write_text(json.dumps(exceptions,indent=2)+'\n');print(json.dumps(summary,indent=2))
