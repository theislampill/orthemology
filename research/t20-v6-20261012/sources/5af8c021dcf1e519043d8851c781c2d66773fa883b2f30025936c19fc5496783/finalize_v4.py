from pathlib import Path
import json,hashlib,difflib,subprocess,tempfile,shutil,datetime,sys
W=Path(__file__).resolve().parents[2];D=W/'t20-depth-reassessment-20261011';A=Path(__file__).parent;P=W/'t20-consolidation-20261011/projection/package-v4';V=P.with_name('package-v3')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(rel,x):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
# Current readers differ from source-inspected predecessors: route new source registries to exact snapshots.
changed_readers={p.relative_to(V).as_posix() for p in V.rglob('*') if p.is_file() and (P/p.relative_to(V)).is_file() and h(p)!=h(P/p.relative_to(V))}
for rel in changed_readers:
 if rel!='PACKAGE_CONTENTS.json':put('depth/inherited-v3/'+rel,(V/rel).read_text())
def reroute(x):
 if isinstance(x,dict):
  out={k:reroute(v) for k,v in x.items()}
  target=out.get('public_source')
  if target in changed_readers:
   out['public_source']='depth/inherited-v3/'+target
   if 'public_sha256' in out:out['public_sha256']=h(V/target)
  return out
 if isinstance(x,list):return [reroute(v) for v in x]
 return x
changed_routes=[]
for p in (P/'depth').rglob('*.json'):
 if 'inherited-v3' in p.parts:continue
 data=json.loads(p.read_text());out=reroute(data)
 if data!=out:put(p.relative_to(P).as_posix(),out);changed_routes.append(p.relative_to(P).as_posix())
projection=json.loads((P/'PUBLIC_PROJECTION.json').read_text())
for row in projection['files']:
 for own in row.get('original_member_bindings',[]):
  if own.get('context')=='11 October 2026 authored T20 successor research':own['context']='Selected for 11 October 2026 T20 successor research; original authorship and date unchanged.'
 if row.get('public_path') in changed_routes:
  q=P/row['public_path'];row['public_sha256']=h(q);row['public_bytes']=q.stat().st_size
 for c in row.get('required_replay_copies',[]):
  if c['path'] in changed_routes:c['sha256']=h(P/c['path']);c['bytes']=(P/c['path']).stat().st_size
put('PUBLIC_PROJECTION.json',projection)
transform=json.loads((P/'depth/LOCATOR_TRANSFORMATIONS.json').read_text())
for r in transform['files']:
 if r['path'] in changed_routes:r['public_sha256']=h(P/r['path']);r['public_bytes']=(P/r['path']).stat().st_size
put('depth/LOCATOR_TRANSFORMATIONS.json',transform)
# Require current exact source-specific and combined review identities, without enlarging review scope.
reviews=[]
for lane in ['joint_correction','semantic_geometry','proof_inquiry','uncertainty_inquiry','grounding_provenance','decision_representation','collective_continuation','occurrence_warrant','cross_front_synthesis']:
 rlane='cross_front_review' if lane=='cross_front_synthesis' else lane+'_review';source=D/lane/'RESULT.md';digest=h(source)
 evidence=[p for p in (D/rlane).glob('*') if p.suffix in ('.md','.json') and digest in p.read_text()]
 if not evidence:raise RuntimeError('Current source review binding absent: '+lane)
 if h(P/'depth'/lane/'RESULT.md')!=digest:raise RuntimeError('Staged report drift: '+lane)
 for p in evidence:
  if not (P/'depth'/rlane/p.name).exists():raise RuntimeError('review evidence missing '+str(p))
 witnesses=[]
 def collect(value,parts,rel):
  if isinstance(value,dict):
   for key,item in value.items():collect(item,parts+[key],rel)
  elif isinstance(value,list):
   for key,item in enumerate(value):collect(item,parts+[key],rel)
  elif value==digest:witnesses.append({'path':rel,'selector':parts,'expected_report_sha256':digest})
 for p in evidence:
  if p.suffix=='.json':
   rel='depth/'+rlane+'/'+p.name;collect(json.loads((P/rel).read_text()),[],rel)
 if not witnesses:raise RuntimeError('No structured current review digest witness '+lane)
 reviews.append({'packet':lane,'report':'depth/'+lane+'/RESULT.md','report_sha256':digest,'review':'depth/'+rlane+'/REVIEW.md','review_sha256':h(P/'depth'/rlane/'REVIEW.md'),'binding_witnesses':witnesses,'current_binding_documents':[{'path':'depth/'+rlane+'/'+p.name,'original_sha256':h(p),'public_sha256':h(P/'depth'/rlane/p.name)} for p in evidence],'scope':'Exact report identity is present in a structured source-specific reviewer binding. Review text controls coverage, contribution credit and limits. A prose-only rebind does not imply new execution.'})

put('depth/REVIEW_CURRENTNESS.json',{'status':'PASS','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviews':reviews,'scope':'Nine new source-specific/combined review routes; inherited reassessment review remains separately preserved. This is binding currentness, not a tenth scientific theorem or fresh mathematical rereview.'})
# Replay receipts are accepted only against precisely current suite source closures.
runs=[];specs=json.loads((P/'depth/PORTABLE_TARGETS.json').read_text())['suites']
for name,spec in specs.items():
 f=A/('replay-'+name+'.json')
 if not f.exists():raise RuntimeError('missing selected execution '+name)
 data=json.loads(f.read_text())
 if data['status']!='PASS':raise RuntimeError('failed selected execution '+name)
 oldclosure=json.loads((A/('closure-'+name+'.json')).read_text())
 current=[{'path':q.relative_to(P).as_posix(),'sha256':h(q),'bytes':q.stat().st_size} for q in sorted((P/'replay'/spec['directory']).rglob('*')) if q.is_file()]
 if current!=oldclosure:raise RuntimeError('suite drift since fresh execution '+name)
 runs.append({k:data[k] for k in ['status','suite','python_version','dependencies','scope']}|{'commands':[{k:r[k] for k in ['python_arguments','exit_code','output_sha256']} for r in data['results']],'suite_sources':current,'assembly_receipt_sha256':h(f),'receipt_scope':'Fresh disposable-copy v4 execution; modes/assertions do not multiply mathematical results. No whole-corpus or kernel rerun.'})
put('DEPTH_REPLAY_VERIFICATION.json',{'status':'PASS','date_utc':'2026-10-11','selected_target_count':len(runs),'runs':runs,'not_performed':['whole corpus execution','fresh Lean build','repository-wide gates','primary Arabic authentication','empirical data replay','repository mutation'],'inherited_receipts':'All unchanged v3 receipts retain their exact older scopes; not counted as fresh here.'})
# Protect and route predecessor reader bindings honestly.
reader=json.loads((V/'READER_PROJECTION.json').read_text())
for row in reader.get('v3_reader_files',[]):
 rel=row['path']
 if h(P/rel)!=row['v3_sha256']:
  dest='depth/inherited-v3/'+rel;put(dest,(V/rel).read_text());row['historical_original_path']=rel;row['path']=dest
reader['v3_binding_scope']='Historical v3 reader digests point to exact preserved preimages whenever current v4 readers differ.'
reader['v4_reader_files']=[{'path':rel,'v4_sha256':h(P/rel)} for rel in ['README_FIRST.md','CODEX_START_HERE.md','EDITION_V4.md','T21_CHARTER.md','CONSOLIDATION_CONTRACT.md','CLAIM_REGISTER.json','DEPENDENCY_INDEX.json','geometry/GEOMETRY_MOMENTS_SYNTHESIS.md','proofs/PROOF_TYPE_INQUIRY_SYNTHESIS.md','coverage/CUMULATIVE_PROGRAMME_CROSSWALK.md','coverage/SELECTED_SOURCE_READS.json']]
put('READER_PROJECTION.json',reader)
# Every v3 file remains exactly addressable, including original manifests/indexes/readers.
preservation=[]
for p in sorted(V.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(V).as_posix();out=P/rel
 if not out.exists() or h(out)!=h(p):
  saved='depth/inherited-v3/'+rel
  if rel=='PACKAGE_CONTENTS.json':saved='depth/inherited-v3/PACKAGE_CONTENTS.v3.json'
  q=P/saved;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes());dest=saved
 else:dest=rel
 preservation.append({'v3_path':rel,'v3_sha256':h(p),'bytes':p.stat().st_size,'v4_path':dest})
put('depth/V3_PRESERVATION.json',{'status':'PASS','v3_manifest_sha256':h(V/'PACKAGE_CONTENTS.json'),'files':preservation,'scope':'Every v3 member preserved byte-identically either at its unchanged path or an explicit historic reader/index snapshot. The v3 directory was not modified.'})
# Regenerate self-described diff artifacts only after whitespace scan.
for name in ['depth/V3_TO_V4_DIFF.json','depth/V3_TO_V4.patch']:
 (P/name).unlink(missing_ok=True)
# Source whitespace is preserved and separately attributed; derived/new whitespace must be clean.
with tempfile.TemporaryDirectory(prefix='t20-v4-whitespace-') as t:
 root=Path(t);shutil.copytree(P,root/'candidate');subprocess.run(['git','init','-q',str(root)],check=True);subprocess.run(['git','-C',str(root),'add','--all'],check=True)
 result=subprocess.run(['git','-C',str(root),'diff','--cached','--check'],capture_output=True,text=True)
 import re
 diagnostics=[]
 for line in result.stdout.splitlines():
  m=re.match(r'candidate/(.+):(\d+): (.+)',line)
  if m:diagnostics.append({'path':m[1],'line':int(m[2]),'diagnostic':m[3]})
original_hashes={h(q) for q in V.rglob('*') if q.is_file()}
original_hashes.update(r['original_sha256'] for r in json.loads((P/'PUBLIC_PROJECTION.json').read_text())['files'] if r['projection']=='EXACT')
for lane in D.iterdir():
 if lane.is_dir() and lane.name not in ['assembly','assembly_v4','pro-intake','.library-helper']:
  original_hashes.update(h(q) for q in lane.rglob('*') if q.is_file() and q.suffix in ['.md','.py','.json','.diff','.patch'])
advisories=[]
for rel in sorted({x['path'] for x in diagnostics}):
 if h(P/rel) not in original_hashes:raise RuntimeError('Authored/derived whitespace defect '+rel)
 advisories.append({'path':rel,'sha256':h(P/rel),'diagnostics':[x for x in diagnostics if x['path']==rel],'scope':'Preserved source bytes; not a new reader whitespace error.'})
put('depth/WHITESPACE_VERIFICATION.json',{'whole_delta_strict_pass':result.returncode==0,'whole_delta_strict_exit_code':result.returncode,'authored_and_derived_clean':True,'advisories':advisories})
# Exact changed-member diff; all additions remain covered by final manifest.
changed=[];added=[];patch=[]
for p in sorted(P.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(P).as_posix()
 if rel in ['PACKAGE_CONTENTS.json','depth/V3_TO_V4_DIFF.json','depth/V3_TO_V4.patch']:continue
 old=V/rel
 if not old.exists():added.append({'path':rel,'sha256':h(p),'bytes':p.stat().st_size})
 elif h(old)!=h(p):
  changed.append({'path':rel,'v3_sha256':h(old),'v4_sha256':h(p)})
  try:patch.extend(difflib.unified_diff(old.read_text().splitlines(True),p.read_text().splitlines(True),fromfile='v3/'+rel,tofile='v4/'+rel,n=0))
  except UnicodeError:pass
put('depth/V3_TO_V4_DIFF.json',{'changed':changed,'added':added,'removed':[],'scope':'Final manifest binds diff files themselves. All predecessor member preimages are in V3_PRESERVATION; no deletion.'});put('depth/V3_TO_V4.patch',''.join(patch))
files=[{'path':p.relative_to(P).as_posix(),'sha256':h(p),'bytes':p.stat().st_size} for p in sorted(P.rglob('*')) if p.is_file() and p.relative_to(P).as_posix()!='PACKAGE_CONTENTS.json']
put('PACKAGE_CONTENTS.json',{'schema':'t20-consolidated-package-contents-v1','scope':'Candidate v4 complete content integrity. Manifest excludes itself; external final seal binds it. No signature or scientific-truth claim.','files':files})
seal={'status':'CANDIDATE_FROZEN_FOR_INDEPENDENT_PORTABILITY_REVIEW','manifest_sha256':h(P/'PACKAGE_CONTENTS.json'),'v3_manifest_sha256':h(V/'PACKAGE_CONTENTS.json'),'file_count':len(files)+1,'bytes':sum(x['bytes'] for x in files)+(P/'PACKAGE_CONTENTS.json').stat().st_size,'selected_fresh_targets':len(runs),'current_review_routes':len(reviews),'inherited_members_preserved':len(preservation),'repository_mutation':False,'T21_started':False}
(A/'CANDIDATE_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');print(json.dumps(seal,indent=2))
