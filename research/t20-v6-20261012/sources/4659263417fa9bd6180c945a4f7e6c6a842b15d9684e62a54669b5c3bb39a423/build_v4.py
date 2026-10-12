from pathlib import Path
import json,hashlib,shutil,re,sys
W=Path(__file__).resolve().parents[2];D=W/'t20-depth-reassessment-20261011';A=Path(__file__).parent;V=W/'t20-consolidation-20261011/projection/package-v3';P=V.with_name('package-v4')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dumps(x):return json.dumps(x,indent=2,ensure_ascii=False)+'\n'
def put(rel,x):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str) else dumps(x));return p
if P.exists():shutil.rmtree(P)
shutil.copytree(V,P)
projection=json.loads((V/'PUBLIC_PROJECTION.json').read_text()); rows=projection['files'];byhash={r['original_sha256']:r for r in rows};hashpath={};transforms=[];selected=[]
for p in sorted(P.rglob('*')):
 if p.is_file():hashpath.setdefault(sha(p),p.relative_to(P).as_posix())
def add(src,rel,public=None):
 raw=src.read_bytes();h=hashlib.sha256(raw).hexdigest();out=raw if public is None else (public.encode() if isinstance(public,str) else public)
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(out);ph=sha(p)
 if h not in byhash:
  r={'original_sha256':h,'original_bytes':len(raw),'owners':[{'track':'T20-depth-v4','source_id':src.parent.name+'/'+src.name}], 'original_member_bindings':[{'member':src.name,'context':'Selected for 11 October 2026 T20 successor research; original authorship and date unchanged.'}],'original_identity_scope':'Scientific source identity; custody locator projections are separately disclosed.','disposition':'included','projection':'EXACT' if raw==out else 'AMENDED','public_path':rel,'public_sha256':ph,'public_bytes':len(out)}
  if raw!=out:r['transformations']=['Custody locator projection; original scientific identities and public member identities are distinct. Original execution/review observations retain their own scopes.']
  rows.append(r);byhash[h]=r
 else:
  r=byhash[h]
  if rel!=r.get('public_path') and not any(x['path']==rel for x in r.get('required_replay_copies',[])):r.setdefault('required_replay_copies',[]).append({'path':rel,'sha256':ph,'bytes':len(out),'reason':'Exact dated source or import-relative dependency layout; duplicate bytes do not multiply results.'})
 if raw==out:hashpath.setdefault(h,rel)
 else:transforms.append({'path':rel,'original_sha256':h,'public_sha256':ph,'original_bytes':len(raw),'public_bytes':len(out),'transformation':'Private/workspace custody addresses replaced by explicit portable source locators or custody-only omission. This is not an exact original replay receipt.'})
 return rel
lanes=['joint_correction','joint_correction_review','semantic_geometry','semantic_geometry_review','proof_inquiry','proof_inquiry_review','uncertainty_inquiry','uncertainty_inquiry_review','grounding_provenance','grounding_provenance_review','decision_representation','decision_representation_review','cross_front_synthesis','cross_front_review','collective_continuation','collective_continuation_review','occurrence_warrant','occurrence_warrant_review']
exclude={'make_bindings.py','build_bindings.py','build_edges.py','explore.py','explore_audit.py','explore_general.py','RED_STAGE.py.txt'}
for lane in lanes:
 if not (D/lane).exists():continue
 for src in sorted((D/lane).rglob('*')):
  if not src.is_file() or '__pycache__' in src.parts or src.name in exclude:continue
  if src.suffix not in {'.md','.py','.json','.diff','.patch'}:continue
  # only selected research/report/receipt material; no raw logs or transfer helpers
  rel='depth/'+lane+'/'+src.relative_to(D/lane).as_posix();selected.append((src,rel))
  if src.suffix!='.json':add(src,rel)
# Hash-bound dependencies are resolved to existing exact selected bodies or materialized once.
def resolve_source(row):
 h=row.get('sha256') or row.get('verified_local_sha256')
 if not isinstance(h,str) or len(h)!=64:return None
 if h in hashpath:return hashpath[h]
 if h in byhash and byhash[h].get('public_path') and (P/byhash[h]['public_path']).exists():return byhash[h]['public_path']
 if h in globals().get('selected_by_hash',{}) and (P/selected_by_hash[h]).exists():return selected_by_hash[h]
 for key in ['path','copy','local_path','public_source']:
  s=row.get(key)
  if not isinstance(s,str) or '!' in s:continue
  q=Path(s)
  for p in [q if q.is_absolute() else W/q,D/q,V/q,D/'occurrence_warrant'/q]:
   if p.is_file() and sha(p)==h:
    if p.suffix in {'.md','.py','.lean','.toml'} or p.name==h:
     return add(p,'depth/sources/'+h+(p.suffix or '.txt'))

 for key in ['path','local_path']:
  s=row.get(key,'');prefix='t20-consolidation-20261011/'
  if isinstance(s,str) and s.startswith(prefix) and (V/s[len(prefix):]).is_file():return s[len(prefix):]
 return None
selected_by_hash={sha(src):rel for src,rel in selected}
bound=[]
def walk(x):
 if isinstance(x,dict):
  if x.get('sha256'):
   p=resolve_source(x)
   if p:bound.append({'original_sha256':x['sha256'],'public_source':p,'public_sha256':sha(P/p),'reading_scope':x.get('read_scope',x.get('inspection',x.get('fresh_read_scope'))),'attribution':'Named source author/reviewer inspection; assembly lookup is not fresh reading.'})
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for src,rel in selected:
 if src.suffix=='.json':walk(json.loads(src.read_text()))
# Projection keeps ordinary scientific facts and removes only custody metadata/addresses.
private_tokens=('/workspace/','/tmp/','private-locator:b1f29effa90a29bba636','catalogue/objects/','catalogue/archive-views/','recovery-20261011/','t20-synthesis-owner-input-20261011/')
def clean(x):
 if isinstance(x,dict):
  out={};target=resolve_source(x)
  for k,v in x.items():
   if k in {'original_provenance','original_locations'}:
    out[k+'_scope']='Original custody locations withheld; original hash retained and public counterparts listed separately.';continue
   if k in {'path','copy','local_path'} and isinstance(v,str) and (any(t in v for t in private_tokens) or v.startswith('t20-')):
    out['public_source' if k=='path' else 'public_'+k]=target or 'CUSTODY_ONLY_NOT_A_PORTABLE_REPLAY_TARGET';continue
   out[k]=clean(v)
  if target:
   out['public_source']=target
   if out.get('sha256')==sha(P/target):out['public_sha256']=sha(P/target);out['public_projection']='EXACT'
   else:
    out.pop('public_sha256',None);out['public_projection']='DERIVED';out['public_digest_binding']='PUBLIC_PROJECTION.json supplies current public digest; original SHA is retained here.'
  return out
 if isinstance(x,list):return [clean(v) for v in x]
 if isinstance(x,str):
  x=re.sub(r'/(?:workspace|tmp|home/agent)/[^\s\"\']+', '<OMITTED_PRIVATE_CUSTODY_LOCATOR>', x)
 if isinstance(x,str) and any(t in x for t in private_tokens):
  if x.startswith('https://'):return x
  # preserve scientific narrative, substitute only an address-shaped entire value
  if '\n' not in x and ('/' in x) and len(x)<1500:return 'Custody locator omitted; see original source identity and public source closure.'
 return x
for src,rel in selected:
 if src.suffix=='.json':put(rel,clean(json.loads(src.read_text())))
for src,rel in selected:
 if src.suffix=='.json':
  original=json.loads(src.read_text());public=clean(original)
  add(src,rel,None if original==public else dumps(public))
put('depth/SOURCE_CLOSURE.json',{'scope':'Exact included scientific owner bodies for the new packet references. Reading is attributed to source authors/reviewers; hash lookup is not new semantic reading. Nonincluded custody records are not replay promises.','sources':list({(r['original_sha256'],r['public_source']):r for r in bound}.values())})
add(D/'FINAL_BASELINE_READBACK.json','depth/FINAL_BASELINE_READBACK.json')
# Preserve all original v3 readers before changing current navigation/indexes.
change_names=['CODEX_START_HERE.md','README_FIRST.md','T21_CHARTER.md','CONSOLIDATION_CONTRACT.md','CLAIM_REGISTER.json','DEPENDENCY_INDEX.json','PUBLIC_PROJECTION.json','REPLAY_SCOPE.json','replay_selected.py']
for name in change_names:
 if (V/name).is_file():put('depth/inherited-v3/'+name,(V/name).read_text())
# Portable replay keeps original checker bytes and separates relocated source checks.
suites={};portable=[]
def copy_suite(lane,names):
 folder='depth-'+lane.replace('_','-');base='replay/'+folder
 for name in names:
  src=D/lane/name
  if src.is_dir():
   for f in sorted(src.rglob('*')):
    if f.is_file() and '__pycache__' not in f.parts and f.suffix in {'.py','.json','.md','.lean','.toml'}:add(f,base+'/'+f.relative_to(D/lane).as_posix())
  else:add(src,base+'/'+name)
 return folder,base
def suite(lane,names,commands,deps,scope):
 folder,base=copy_suite(lane,names);suites[folder]={'directory':folder,'commands':commands,'dependencies':deps,'scope':scope};return base
base=suite('joint_correction',['check_joint.py','RESULT.md'],[['-B','check_joint.py','--output','REPLAY.json'],['-O','-B','check_joint.py','--output','REPLAY_OPTIMIZED.json']],['sympy','mpmath'],'Exact author mathematical program and portable exact source fixtures; finite controls and high-precision diagnostics, not universal proof or R3 comparison.')
orig=json.loads((D/'joint_correction/SOURCE_BINDINGS.json').read_text());fixtures=[]
for i,r in enumerate(orig['readings']):
 p=resolve_source(r)
 if not p:raise RuntimeError('missing joint fixture '+str(r))
 dest='inputs/source-%02d'%i;add(P/p,base+'/'+dest);fixtures.append({**{k:v for k,v in r.items() if k!='path'},'path':dest,'original_source_sha256':r['sha256'],'sha256':sha(P/p),'fixture_projection':'EXACT' if sha(P/p)==r['sha256'] else 'DERIVED_PUBLIC_LOCATOR'})
put(base+'/SOURCE_BINDINGS.json',{'readings':fixtures,'scope':'Derived portable locator registry; exact source body hashes retained.'})
base=suite('semantic_geometry',['check_controls.py','RESULT.md'],[['-B','check_controls.py'],['-O','-B','check_controls.py']],['sympy'],'Exact author symbolic and finite controls using portable source fixtures; not an enumeration proof of uncountable semantic claims.')
fixtures=[]
for i,r in enumerate(json.loads((D/'semantic_geometry/SOURCE_BINDINGS.json').read_text())):
 p=resolve_source(r)
 if not p:raise RuntimeError('missing semantic fixture')
 dest='inputs/source-%02d'%i;add(P/p,base+'/'+dest);fixtures.append({**r,'path':dest,'original_source_sha256':r['sha256'],'sha256':sha(P/p),'fixture_projection':'EXACT' if sha(P/p)==r['sha256'] else 'DERIVED_PUBLIC_LOCATOR'})
put(base+'/SOURCE_BINDINGS.json',fixtures)
suite('proof_inquiry',['cache_transport.py','test_cache_transport.py','test_policy_contracts.py','false_claim.py','inherited'],[['-B','-m','unittest','discover','-s','.','-p','test_*.py','-v'],['-O','-B','-m','unittest','discover','-s','.','-p','test_*.py','-v']],[],'19 portable cache/policy tests with three exact inherited modules. Original workspace preservation verifier is retained as source, not advertised as portable.')
base=suite('uncertainty_inquiry',['check_exact.py','inputs'],[['-B','check_exact.py'],['-O','-B','check_exact.py']],[],'Exact rational finite controls with fourteen exact read-ledger fixtures, normal and optimized. Written continuum and minimax proofs remain separate.')
ledger=json.loads((D/'uncertainty_inquiry/READ_LEDGER.json').read_text())
for r in ledger:
 p=resolve_source(r)
 if not p:raise RuntimeError('missing uncertainty fixture')
 dest='inputs/'+r['id']+'.md';add(P/p,base+'/'+dest);r['path']=dest;r['copy']=dest
put(base+'/READ_LEDGER.json',ledger)
base=suite('grounding_provenance',['verify.py','RESULT.md'],[['-B','run_portable.py']],[],'Exact author finite relation controls and unchanged engine. Normal only: bare assertions make optimized execution non-evidence. Derived driver changes only catalogue ROOT.')
h='6b06c7cec417a961052971d605b54570c34e44d3e0f0ddfc1a2021e384038268';p=resolve_source({'sha256':h,'path':'t20-consolidation-20261011/catalogue/objects/'+h[:2]+'/'+h})
add(P/p,base+'/inputs/'+h[:2]+'/'+h)
put(base+'/run_portable.py',"from pathlib import Path\nimport runpy\ns=runpy.run_path(str(Path(__file__).with_name('verify.py')))\nf=s['main']\nf.__globals__['CAT']=Path(__file__).resolve().parent/'inputs'\nf()\n")
suite('decision_representation',['check_exact.py'],[['-B','check_exact.py'],['-O','-B','check_exact.py']],[],'Exact finite loss/profile certificates. Not a continuum proof by enumeration or fresh Lean build.')
if (D/'collective_continuation/CONTROL_CHECKS.py').is_file():suite('collective_continuation',['CONTROL_CHECKS.py'],[['-B','CONTROL_CHECKS.py'],['-O','-B','CONTROL_CHECKS.py']],[],'Exact finite linked-signal Bayes risk, recalibration, rank and migration controls; not empirical or infinite-continuation proof replay.')
if (D/'occurrence_warrant/RESULT.md').exists():
 base=suite('occurrence_warrant',['controls','sources/source_rows.json'],[['-B','controls/contract_check.py'],['-O','-B','controls/contract_check.py'],['-B','controls/verify_boundaries.py'],['-O','-B','controls/verify_boundaries.py'],['-B','controls/inherited_t16/check.py']],[],'Exact frozen seven-record source-view controls, deliberate boundary mutations, and inherited T16 checker normal-only. No Arabic authentication or human-warrant inference.')
# Bounded inherited methodology fields, prepared by the coverage reviewer.
method=D/'coverage_review/methodology'
if method.exists():
 bindings=json.loads((method/'PROJECTION_BINDINGS.json').read_text())
 coverage=json.loads((V/'coverage/SELECTED_SOURCE_READS.json').read_text())
 put('depth/inherited-v3/coverage/SELECTED_SOURCE_READS.json',(V/'coverage/SELECTED_SOURCE_READS.json').read_text())
 for b in bindings:
  h=b['original_sha256'];src=W/'t20-consolidation-20261011/catalogue/objects'/h[:2]/h
  rel='coverage/methodology/'+b['file'];add(src,rel,(method/b['file']).read_bytes())
  for r in coverage:
   if r['id']==b['source_id']:r.update(public_source=rel,public_sha256=b['public_sha256'],public_bytes=b['public_bytes'],projection=b['projection_kind'],projection_scope=b['scope'])
 put('coverage/SELECTED_SOURCE_READS.json',coverage);put('coverage/methodology/PROJECTION_BINDINGS.json',bindings)
# Inherited runner and specs remain separately source-preserved.
runner=(V/'replay_selected.py').read_text();runner=runner.replace('\n\ndef main():','\n\nSUITES.update('+repr(suites)+')\n\ndef main():');put('replay_selected.py',runner)
scope=json.loads((V/'REPLAY_SCOPE.json').read_text());scope['suites'].update(suites);scope['v4_scope']='Historical receipts are retained unchanged and not counted as fresh. New depth suites have separately bound disposable-copy executions.';put('REPLAY_SCOPE.json',scope)
put('depth/PORTABLE_TARGETS.json',{'suites':suites,'qualification':'Exact mathematical code bytes are preserved. Only named fixture registries and the grounding CAT relocation are derived. No dependency installation or network fetch. No original private custody check is claimed reproduced.'})
put('depth/LOCATOR_TRANSFORMATIONS.json',{'files':transforms,'scope':'Each row binds original custody bytes and derived public bytes; only exact copies can inherit original exact-byte identity.'})
projection['files']=sorted(rows,key=lambda r:(r.get('public_path',''),r['original_sha256']));put('PUBLIC_PROJECTION.json',projection)
print('Staged',len(selected),'new packet files and',len(suites),'portable targets')
