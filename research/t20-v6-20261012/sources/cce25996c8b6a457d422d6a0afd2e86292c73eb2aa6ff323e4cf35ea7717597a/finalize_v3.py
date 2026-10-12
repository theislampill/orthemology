from pathlib import Path
import collections,difflib,hashlib,json,re,subprocess,sys,tempfile,shutil,datetime
W=Path(__file__).resolve().parents[2];D=W/'t20-depth-reassessment-20261011';A=D/'assembly';P=W/'t20-consolidation-20261011/projection/package-v3';V=P.with_name('package-v2')
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
# Summaries bind exact suite files, distinguish historical receipts and fresh observations.
runs=[]
for f in sorted(A.glob('replay-*.json')):
 d=json.loads(f.read_text());assert d['status']=='PASS'
 suite=d['suite'];spec=json.loads((P/'REPLAY_SCOPE.json').read_text())['suites'][suite]
 sourcefiles=[]
 for p in sorted((P/'replay'/spec['directory']).rglob('*')):
  if p.is_file():sourcefiles.append({'path':p.relative_to(P).as_posix(),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size})
 out={k:d[k] for k in ['status','suite','python_version','dependencies','scope']};out['commands']=[{k:r[k] for k in ['python_arguments','exit_code','output_sha256']} for r in d['results']];out['suite_sources']=sourcefiles;out['local_receipt_sha256']=sha(f.read_bytes());out['scope_note']='Fresh disposable-copy selected replay. Interpreter reruns do not multiply scientific suites/results.';runs.append(out)
dump(P/'REASSESSMENT_REPLAY_VERIFICATION.json',{'status':'PASS','phase':'intermediate consolidation-depth checkpoint','date_utc':'2026-10-11','runs':runs,'not_performed':['whole corpus re-execution','new Lean kernel build','current repository-wide validation','repository adoption','external human peer review'],'unchanged_v2_other_selected_suites':'Historical SELECTED_REPLAY_VERIFICATION remains exact, unchanged and separately scoped.'})
# Original currentness report mapped without exporting private custody paths.
orig=json.loads((D/'independent_review/FINAL_CURRENTNESS.json').read_text());pb=json.loads((P/'reassessment/independent_review/PORTABLE_REVIEW_BINDINGS.json').read_text())
dump(P/'reassessment/independent_review/CURRENTNESS.json',{'status':orig['status'],'checked_utc':orig['checked_utc'],'original_receipt_sha256':sha((D/'independent_review/FINAL_CURRENTNESS.json').read_bytes()),'targets':pb['targets'],'inherited_input_match_count':len(orig['sources']),'all_original_inherited_inputs_matched':all(x['matches'] for x in orig['sources']),'portable_binding_scope':'Original reviewer custody validation is distinct from portable public-source locator projection; original report/checker target bytes are exact.'})
# Preserve reviewed source reader versions and account for all content precisely.
projection=json.loads((P/'PUBLIC_PROJECTION.json').read_text());r=projection['files'];old=json.loads((V/'PUBLIC_PROJECTION.json').read_text())['files'];oldhash={x['original_sha256'] for x in old}
account={'status':'INTERMEDIATE_REASSESSMENT_CHECKPOINT','T20':'ACTIVE','distinct_original_source_identities':len(r),'included_distinct_original_identities':sum(x['disposition']=='included' for x in r),'pinned_public_distinct_original_identities':sum(x['disposition']=='pinned_existing_public_source' for x in r),'required_replay_copy_records':sum(len(x.get('required_replay_copies',[])) for x in r),'additional_audit_fixture_copies':11,'new_original_identities_since_v2':len({x['original_sha256'] for x in r}-oldhash),'claim_entries':json.loads((P/'CLAIM_REGISTER.json').read_text())['claim_count'],'typed_edges':json.loads((P/'DEPENDENCY_INDEX.json').read_text())['edge_count'],'copy_count_scope':'Required replay-copy records and 11 portable audit fixtures are physical layout items, not distinct scientific results; the complete file inventory is PACKAGE_CONTENTS. Some sources have original/public projections with distinct hashes.','scientific_replay_scope':'Seven selected delta targets plus old26 baseline, not sum of all individual assertions, configurations, modes or all inherited sources.'}
dump(P/'reassessment/SOURCE_ACCOUNTING.json',account)
# Qualified review note resolves preserved original report-custody pointers and pending headings.
(P/'reassessment/README.md').write_text('''# Consolidation-depth reassessment: intermediate checkpoint\n\n11 October 2026. T20 remains active. Owner acceptance is pending. This complete working edition records a bounded reassessment while the broader cross-front investigation continues; it neither calls T20 closed nor starts T21.\n\nStart with OWNER_ASSESSMENT.md and COMBINED_RESEARCH_SYNTHESIS.md, then CLAIMS.json. Reports are under audit_symmetries, restricted_controls and foundational_interface. The independent scientific review is under independent_review; reconstructed code review is under contract_repair. SOURCE_OWNERS.json resolves inherited proof owners to the selected included bytes or verified pinned public owners.\n\nOriginal scientific reports and original review bodies retain their exact authored wording and historical custody references. An original “review pending” status records its author-freeze stage; the exact subsequent independent REVIEW.md and CURRENTNESS.json control this checkpoint's review state. No review is enlarged to cover claims outside its declared scope. The tagged-instrument corollary proof was contributed by the reviewer and therefore does not receive independent corroboration credit from the same review.\n\nPublic source-binding registries are declared locator projections. The reviewer’s original private snapshots and absolute/workspace custody paths are not a portable execution promise. PORTABLE_REVIEW_BINDINGS.json binds the exact report/checker targets. Historical v2 authored reader snapshots remain under inherited-reader-v2 so current headers cannot alter the inspected reader bytes. These duplicate reader copies are provenance, not instructions to integrate multiple editions.\n\nThe audit-refinement replay uses an unchanged mathematical checker plus a derived ROOT relocation and public fixture registry. Original scientific inputs remain exact; selected assembly/index/ancestry counterparts are explicitly bound public projections. This validates the portable fixtures and mathematical controls, not the absent private assembly. Other selected suites are run in disposable copies by replay_selected.py. The contract-downstream probe carries unchanged caller/fixture bytes with a disclosed repaired dependency substitution; the old hash-pin rejection is retained, and the historical rational-hase-j source family is untouched.\n\nCUSTODY_UPDATE.json in intake closes the newly supplied full-archive seal only. The original trimmed failure and unavailable R3 state remain. Transfer helpers, raw user instructions/chat, private operational notes, signed file URLs and bulk corpus archives are not included.\n''')
# Source whitespace must remain original; newly authored problems are rejected.
with tempfile.TemporaryDirectory(prefix='t20-v3-whitespace-',dir=A) as tmp:
 root=Path(tmp);shutil.copytree(P,root/'candidate');subprocess.run(['git','init','-q',str(root)],check=True);subprocess.run(['git','-C',str(root),'add','--all'],check=True)
 check=subprocess.run(['git','-C',str(root),'diff','--cached','--check'],capture_output=True,text=True)
 diagnostics=[]
 for line in check.stdout.splitlines():
  m=re.match(r'candidate/(.+):(\d+): (.+)',line)
  if m:diagnostics.append({'path':m[1],'line':int(m[2]),'diagnostic':m[3]})
source_paths={}
for row in r:
 if row.get('public_path'):source_paths[row['public_path']]=row['original_sha256']
 for extra in row.get('required_replay_copies',[]):source_paths[extra['path']]=row['original_sha256']
advisories=[]
for rel in sorted({x['path'] for x in diagnostics}):
 raw=(P/rel).read_bytes();expected=source_paths.get(rel)
 if expected!=sha(raw):raise ValueError('New authored/derived whitespace defect: '+rel)
 advisories.append({'path':rel,'original_sha256':expected,'public_sha256':sha(raw),'bytes':len(raw),'diagnostics':[x for x in diagnostics if x['path']==rel],'disposition':'Exact-source formatting preserved; not an authored/derived whitespace defect.'})
dump(P/'EXACT_SOURCE_WHITESPACE.json',{'whole_delta_strict_exit_code':check.returncode,'whole_delta_strict_pass':check.returncode==0,'authored_and_amended_files_strict_pass':True,'advisories':advisories,'policy':'No whitespace normalization of old scientific originals or received exact new sources. Whole-delta strict PASS is not asserted. Exact per-file proposals remain review-only.'})
(P/'PROPOSED_EXACT_SOURCE_ATTRIBUTES.txt').write_text('# Proposed only; not applied. Exact paths/hashes are inventoried in EXACT_SOURCE_WHITESPACE.json.\n# Requires integration review; installer never changes protected root attributes.\n'+'\n'.join('research/t20-consolidated-20261011/'+x['path']+' -text whitespace=-trailing-space' for x in advisories)+'\n')
# Source safety and immutable predecessor check.
for name in ['apply_additive.py','INTEGRATION_PINS.json','validate_package.py']:
 assert (P/name).read_bytes()==(V/name).read_bytes(),name
pres=[]
for row in old:
 for rel in ([row['public_path']] if row.get('public_path') else [])+[x['path'] for x in row.get('required_replay_copies',[])]:
  assert (P/rel).read_bytes()==(V/rel).read_bytes(),rel
  pres.append({'path':rel,'sha256':sha((P/rel).read_bytes())})
dump(P/'reassessment/V2_SOURCE_PRESERVATION.json',{'status':'PASS','v2_manifest_sha256':sha((V/'PACKAGE_CONTENTS.json').read_bytes()),'checked_source_copy_records':len(pres),'installer_validator_and_pins_unchanged':True,'sources':pres,'scope':'Every old PUBLIC_PROJECTION included scientific source and required replay copy remains byte-identical; authored current-reader changes are separately inventoried.'})
# Detailed diff excluding itself and final manifest self-reference, which are separately bound.
exclusions={'PACKAGE_CONTENTS.json','reassessment/V2_TO_V3_DIFF.json','reassessment/V2_TO_V3.patch'}
oldfiles={x.relative_to(V).as_posix():x for x in V.rglob('*') if x.is_file()};newfiles={x.relative_to(P).as_posix():x for x in P.rglob('*') if x.is_file()}
added=[];changed=[];removed=[];patch=[]
for rel in sorted(set(oldfiles)|set(newfiles)):
 if rel in exclusions:continue
 a=oldfiles.get(rel);b=newfiles.get(rel)
 if a is None:added.append({'path':rel,'sha256':sha(b.read_bytes()),'bytes':b.stat().st_size})
 elif b is None:removed.append({'path':rel,'sha256':sha(a.read_bytes()),'bytes':a.stat().st_size})
 elif a.read_bytes()!=b.read_bytes():
  changed.append({'path':rel,'v2_sha256':sha(a.read_bytes()),'v3_sha256':sha(b.read_bytes()),'v2_bytes':a.stat().st_size,'v3_bytes':b.stat().st_size})
  try:patch.extend(difflib.unified_diff(a.read_text().splitlines(True),b.read_text().splitlines(True),fromfile='v2/'+rel,tofile='v3/'+rel,n=0))
  except UnicodeError:pass
assert not removed
dump(P/'reassessment/V2_TO_V3_DIFF.json',{'scope':'Exact added/changed/deleted member accounting; excludes this diff, its patch and manifest to avoid self-reference. Final manifest/delivery seal account for every byte.','v2_manifest_sha256':sha((V/'PACKAGE_CONTENTS.json').read_bytes()),'added':added,'changed':changed,'removed':removed,'old_scientific_source_copy_records_preserved':len(pres),'authored_reader_changes_do_not_replace_original_sources':True})
(P/'reassessment/V2_TO_V3.patch').write_text(''.join(patch))
# Every file covered, excluding manifest self-reference.
files=[]
for path in sorted(P.rglob('*')):
 if path.is_symlink():raise ValueError('symlink')
 if path.is_file() and path.name!='PACKAGE_CONTENTS.json':
  raw=path.read_bytes();files.append({'path':path.relative_to(P).as_posix(),'sha256':sha(raw),'bytes':len(raw)})
dump(P/'PACKAGE_CONTENTS.json',{'schema':'t20-consolidated-package-contents-v1','scope':'Exact intermediate public checkpoint; no scientific closure. Manifest excludes itself; checkpoint seal binds its hash.','files':files})
# Full exact diff identities outside payload have no circularity.
final={'status':'INTERMEDIATE_REASSESSMENT_CHECKPOINT','T20':'ACTIVE','owner_acceptance':'pending','T21_started':False,'manifest_sha256':sha((P/'PACKAGE_CONTENTS.json').read_bytes()),'v2_manifest_sha256':sha((V/'PACKAGE_CONTENTS.json').read_bytes()),'file_count':len(files)+1,'bytes':sum(x['bytes'] for x in files)+(P/'PACKAGE_CONTENTS.json').stat().st_size,'added_files':len(added)+2,'changed_files':len(changed)+1,'removed_files':0,'source_accounting':account,'selected_replay_status':'PASS','selected_replay_targets':len(runs),'source_preservation_records':len(pres),'repository_checks':'Not run; integration-time gates under separate authority','local_package':str(P.relative_to(W))}
dump(A/'CHECKPOINT_SEAL.json',final)
# Exact final comparison outside the archive includes all self-excluded members and manifest.
exact=[]
for rel in sorted(set(oldfiles)|{x.relative_to(P).as_posix() for x in P.rglob('*') if x.is_file()}):
 a=V/rel;b=P/rel
 if not a.is_file():exact.append({'path':rel,'change':'added','v3_sha256':sha(b.read_bytes()),'v3_bytes':b.stat().st_size})
 elif not b.is_file():exact.append({'path':rel,'change':'removed','v2_sha256':sha(a.read_bytes()),'v2_bytes':a.stat().st_size})
 elif a.read_bytes()!=b.read_bytes():exact.append({'path':rel,'change':'changed','v2_sha256':sha(a.read_bytes()),'v3_sha256':sha(b.read_bytes()),'v2_bytes':a.stat().st_size,'v3_bytes':b.stat().st_size})
dump(A/'EXACT_V2_TO_V3_DELTA.json',{'v2_manifest_sha256':sha((V/'PACKAGE_CONTENTS.json').read_bytes()),'v3_manifest_sha256':final['manifest_sha256'],'files':exact})
print(json.dumps(final,indent=2))
